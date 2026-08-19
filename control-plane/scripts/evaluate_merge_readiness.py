#!/usr/bin/env python3
"""Trusted-base evaluator for the Agent Core Merge Readiness gate.

This script is designed to be fetched from the pull request's base SHA by a
`pull_request_target` workflow. It must never be loaded from the PR head.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEPENDENCY_RE = re.compile(
    r"(^|/)(package(-lock)?\.json|pnpm-lock\.yaml|yarn\.lock|pyproject\.toml|uv\.lock|"
    r"requirements[^/]*\.txt|go\.mod|go\.sum|Cargo\.toml|Cargo\.lock|Gemfile(\.lock)?|"
    r"composer\.json|composer\.lock)$"
)


def path_matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    return fnmatch.fnmatchcase(path, pattern)


def determine_risk(changed_paths: list[str], policy: dict[str, Any]) -> dict[str, Any]:
    control = policy.get("control_plane") or {}
    control_patterns = list(control.get("paths") or [])
    dependabot_allow = list(control.get("dependabot_protected_allowlist") or [])
    failures: list[str] = []
    if not control_patterns:
        failures.append("trusted policy control_plane.paths is missing/empty")

    protected = [
        path for path in changed_paths
        if any(path_matches(path, pattern) for pattern in control_patterns)
    ]
    is_control = bool(protected)
    is_dependency = any(
        path == ".github/dependabot.yml" or DEPENDENCY_RE.search(path)
        for path in changed_paths
    )
    return {
        "control_plane": is_control,
        "dependencies": is_dependency,
        "protected_paths": protected,
        "control_patterns": control_patterns,
        "dependabot_allow": dependabot_allow,
        "failures": failures,
    }


def required_workflow_names(changed_paths: list[str], manifest: dict[str, Any]) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    config = manifest.get("required_checks") or {}
    entries = config.get("workflows") or []
    if manifest.get("version") != 1 or not isinstance(entries, list) or not entries:
        return [], ["trusted required-checks manifest is missing/invalid"]

    required: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("name"):
            failures.append(f"malformed required workflow entry: {entry!r}")
            continue
        name = str(entry["name"])
        mode = entry.get("mode")
        if name == "Merge Readiness":
            failures.append("manifest must not recursively require Merge Readiness")
            continue
        if mode == "always":
            required.append(name)
        elif mode == "paths":
            patterns = entry.get("paths") or []
            if not isinstance(patterns, list) or not patterns:
                failures.append(f"workflow {name} has paths mode without paths")
            elif any(
                any(path_matches(path, str(pattern)) for pattern in patterns)
                for path in changed_paths
            ):
                required.append(name)
        else:
            failures.append(f"workflow {name} has unknown mode: {mode!r}")
    return sorted(set(required)), failures


def latest_run_for(runs: list[dict[str, Any]], workflow_name: str, head_sha: str) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    matches = [
        run for run in runs
        if run.get("name") == workflow_name and run.get("head_sha") == head_sha
    ]
    matches.sort(
        key=lambda run: (str(run.get("created_at") or ""), int(run.get("id") or 0)),
        reverse=True,
    )
    selected = matches[0] if matches else None
    return selected, matches


def _run_state(run: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": run.get("id"),
        "created_at": run.get("created_at"),
        "status": run.get("status"),
        "conclusion": run.get("conclusion"),
    }


def selected_run_succeeded(run: dict[str, Any] | None) -> bool:
    return bool(
        run
        and run.get("status") == "completed"
        and run.get("conclusion") == "success"
    )


def make_getter(api: str, token: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "agent-core-merge-readiness-v5",
    }

    def get(path: str):
        req = urllib.request.Request(f"{api}/{path}", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            return exc.code, {"error": raw[:500]}
        except Exception as exc:
            return 0, {"error": str(exc)}

    return get


def evaluate(manifest: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    repo = os.environ["REPO"]
    pr_number = int(os.environ["PR_NUMBER"])
    expected_head_sha = os.environ["PR_HEAD_SHA"]
    trusted_base_sha = os.environ["TRUSTED_BASE_SHA"]
    api = os.environ["GITHUB_API_URL"]
    token = os.environ["GH_TOKEN"]
    get = make_getter(api, token)
    failures: list[str] = []
    observations: list[str] = []

    status, pr = get(f"repos/{repo}/pulls/{pr_number}")
    if status != 200:
        raise SystemExit(f"Cannot read PR metadata: http={status}")

    actual_head_sha = ((pr.get("head") or {}).get("sha"))
    actual_base_sha = ((pr.get("base") or {}).get("sha"))
    if actual_head_sha != expected_head_sha:
        failures.append(f"event head SHA changed: event={expected_head_sha} api={actual_head_sha}")
    if actual_base_sha != trusted_base_sha:
        failures.append(f"base SHA changed since gate event: event={trusted_base_sha} api={actual_base_sha}")
    if pr.get("state") != "open":
        failures.append(f"PR state is {pr.get('state')}, expected open")
    if pr.get("draft") is True:
        failures.append("draft PRs are not merge-ready")

    reported_files = int(pr.get("changed_files") or 0)
    files: list[dict[str, Any]] = []
    page = 1
    while True:
        s, batch = get(f"repos/{repo}/pulls/{pr_number}/files?per_page=100&page={page}")
        if s != 200 or not isinstance(batch, list):
            failures.append(f"cannot read changed files page {page}: http={s}")
            break
        files.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    if len(files) < reported_files:
        failures.append(
            f"incomplete changed-file evidence: retrieved={len(files)} reported={reported_files}"
        )

    changed_paths: set[str] = set()
    for item in files:
        if item.get("filename"):
            changed_paths.add(item["filename"])
        if item.get("previous_filename"):
            changed_paths.add(item["previous_filename"])
    paths = sorted(changed_paths)

    risk = determine_risk(paths, policy)
    failures.extend(risk.pop("failures"))
    is_control = bool(risk["control_plane"])
    is_dependency = bool(risk["dependencies"])

    author = ((pr.get("user") or {}).get("login")) or ""
    author_permission = "not-required"
    trusted_author = not is_control
    if is_control:
        dependabot_safe = author == "dependabot[bot]" and all(
            any(path_matches(path, pattern) for pattern in risk["dependabot_allow"])
            for path in risk["protected_paths"]
        )
        if dependabot_safe:
            trusted_author = True
            author_permission = "dependabot-narrow-allowlist"
        else:
            s, permission = get(
                f"repos/{repo}/collaborators/{urllib.parse.quote(author, safe='')}/permission"
            )
            author_permission = (
                (permission or {}).get("permission", "unknown")
                if s == 200 else f"unknown-http-{s}"
            )
            trusted_permissions = set((policy.get("control_plane") or {}).get("trusted_permissions") or ["write", "admin"])
            trusted_author = author_permission in trusted_permissions
        if not trusted_author:
            failures.append(
                f"control-plane author is not trusted: author={author} permission={author_permission}"
            )

    required, manifest_failures = required_workflow_names(paths, manifest)
    failures.extend(manifest_failures)

    attempts = int(((policy.get("merge_readiness") or {}).get("polling") or {}).get("attempts") or 12)
    interval = int(((policy.get("merge_readiness") or {}).get("polling") or {}).get("interval_seconds") or 10)
    observed: dict[str, Any] = {}
    all_success = False
    if not failures:
        for attempt in range(1, attempts + 1):
            s, runs_payload = get(
                f"repos/{repo}/actions/runs?event=pull_request&head_sha={urllib.parse.quote(expected_head_sha)}&per_page=100"
            )
            if s != 200:
                failures.append(f"cannot read workflow runs: http={s}")
                break
            runs = (runs_payload or {}).get("workflow_runs") or []
            observed = {}
            all_success = True
            for name in required:
                selected, matches = latest_run_for(runs, name, expected_head_sha)
                observed[name] = {
                    "selected": _run_state(selected) if selected else None,
                    "all_current_head_runs": [_run_state(run) for run in matches],
                }
                if not selected_run_succeeded(selected):
                    all_success = False
            if all_success:
                observations.append(
                    f"latest required workflow runs all succeeded on poll {attempt}"
                )
                break
            if attempt < attempts:
                time.sleep(interval)

        if not all_success and not any(item.startswith("cannot read workflow runs") for item in failures):
            for name in required:
                selected = (observed.get(name) or {}).get("selected")
                if not (
                    selected
                    and selected.get("status") == "completed"
                    and selected.get("conclusion") == "success"
                ):
                    failures.append(
                        f"latest required current-head workflow not successful: {name} selected={selected}"
                    )

    s, fresh_pr = get(f"repos/{repo}/pulls/{pr_number}")
    labels = {
        item.get("name")
        for item in ((fresh_pr or {}).get("labels") or [])
        if item.get("name")
    } if s == 200 else set()
    if is_control:
        for expected in {"risk:control-plane", "agent:extra-review"}:
            if expected not in labels:
                failures.append(f"missing control-plane routing label: {expected}")
    if is_dependency and "risk:dependencies" not in labels:
        failures.append("missing dependency routing label: risk:dependencies")

    return {
        "schemaVersion": 2,
        "repository": repo,
        "pr": pr_number,
        "head_sha": expected_head_sha,
        "base_sha": trusted_base_sha,
        "reported_changed_files": reported_files,
        "retrieved_changed_files": len(files),
        "changed_paths": paths,
        "risk": {
            "control_plane": is_control,
            "dependencies": is_dependency,
            "protected_paths": risk["protected_paths"],
        },
        "author": {
            "login": author,
            "permission": author_permission,
            "trusted": trusted_author,
        },
        "required_workflows": required,
        "observed_workflows": observed,
        "labels": sorted(labels),
        "observations": observations,
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", required=True)
    parser.add_argument("--policy-json", required=True)
    parser.add_argument("--receipt", default="/tmp/merge-readiness-receipt.json")
    args = parser.parse_args()
    manifest = json.loads(Path(args.manifest_json).read_text(encoding="utf-8"))
    policy = json.loads(Path(args.policy_json).read_text(encoding="utf-8"))
    receipt = evaluate(manifest, policy)
    Path(args.receipt).write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=False))

    summary = [
        "# Merge Readiness", "",
        f"Result: **{receipt['result']}**",
        f"PR: **#{receipt['pr']}**",
        f"Head SHA: `{receipt['head_sha']}`",
        f"Base SHA: `{receipt['base_sha']}`",
        f"Control plane: **{receipt['risk']['control_plane']}**",
        f"Dependency sensitive: **{receipt['risk']['dependencies']}**",
        f"Author trust: **{receipt['author']['trusted']}** (`{receipt['author']['permission']}`)",
        "", "## Required workflows",
    ]
    summary += [f"- `{name}`" for name in receipt["required_workflows"]] or ["- none"]
    summary += ["", "## Failures"]
    summary += [f"- {item}" for item in receipt["failures"]] or ["- none"]
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        Path(os.environ["GITHUB_STEP_SUMMARY"]).write_text(
            "\n".join(summary) + "\n", encoding="utf-8"
        )
    if receipt["failures"]:
        raise SystemExit("Merge Readiness failed: " + "; ".join(receipt["failures"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
