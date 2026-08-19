#!/usr/bin/env python3
"""Converge GitHub repository admin settings and the Agent Core V4 Ruleset.

Default mode is read-only. Pass ``--apply`` to mutate GitHub through an already
authenticated ``gh`` CLI credential with repository Administration: write.

The tool converges two live-admin surfaces:
1. repository merge/update settings;
2. a repository-level ``protect-main`` Ruleset requiring exactly the app-bound
   ``Merge Readiness`` check.

Writes are ordered Ruleset-first, repository-settings-second. The previous live
state is backed up before mutation. If the repository settings write/readback
fails after the Ruleset changed, the tool attempts to restore the previous
Ruleset (or delete a newly-created Ruleset) before returning BLOCKED.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import shutil
import subprocess
import sys
from typing import Any

API_VERSION = "2026-03-10"
DEFAULT_RULESET_NAME = "protect-main"
GITHUB_ACTIONS_INTEGRATION_ID = 15368
REQUIRED_CHECKS = [
    {"context": "Merge Readiness", "integration_id": GITHUB_ACTIONS_INTEGRATION_ID},
]
DESIRED_REPOSITORY_SETTINGS = {
    "allow_auto_merge": True,
    "allow_merge_commit": False,
    "allow_squash_merge": True,
    "allow_rebase_merge": True,
    "allow_update_branch": True,
}


class AdminConvergenceError(RuntimeError):
    pass


def default_pull_request_rule() -> dict[str, Any]:
    return {
        "type": "pull_request",
        "parameters": {
            "required_approving_review_count": 0,
            "dismiss_stale_reviews_on_push": False,
            "require_code_owner_review": False,
            "require_last_push_approval": False,
            "required_review_thread_resolution": True,
            "allowed_merge_methods": ["squash", "rebase"],
        },
    }


def default_ruleset_base() -> dict[str, Any]:
    return {
        "name": DEFAULT_RULESET_NAME,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [
            {"actor_id": None, "actor_type": "OrganizationAdmin", "bypass_mode": "always"}
        ],
        "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {"type": "required_linear_history"},
            default_pull_request_rule(),
        ],
    }


def required_status_rule() -> dict[str, Any]:
    return {
        "type": "required_status_checks",
        "parameters": {
            "strict_required_status_checks_policy": False,
            "do_not_enforce_on_create": True,
            "required_status_checks": REQUIRED_CHECKS,
        },
    }


def _update_shape(current: dict[str, Any]) -> dict[str, Any]:
    """Return only fields accepted by create/update Ruleset APIs."""
    return {
        "name": current.get("name", DEFAULT_RULESET_NAME),
        "target": current.get("target", "branch"),
        "enforcement": current.get("enforcement", "active"),
        "bypass_actors": current.get("bypass_actors", []),
        "conditions": current.get(
            "conditions", {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}}
        ),
        "rules": list(current.get("rules") or []),
    }


def build_ruleset_payload(current: dict[str, Any] | None) -> dict[str, Any]:
    payload = default_ruleset_base() if current is None else _update_shape(current)
    rules = [rule for rule in payload.get("rules") or [] if rule.get("type") != "required_status_checks"]
    present = {rule.get("type") for rule in rules}
    defaults = {
        "deletion": {"type": "deletion"},
        "non_fast_forward": {"type": "non_fast_forward"},
        "required_linear_history": {"type": "required_linear_history"},
        "pull_request": default_pull_request_rule(),
    }
    for rule_type in ["deletion", "non_fast_forward", "required_linear_history", "pull_request"]:
        if rule_type not in present:
            rules.append(defaults[rule_type])
    rules.append(required_status_rule())
    payload["rules"] = rules
    payload["name"] = DEFAULT_RULESET_NAME
    payload["target"] = "branch"
    payload["enforcement"] = "active"
    payload["conditions"] = {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}}
    return payload


def verify_repository_settings(meta: dict[str, Any]) -> tuple[bool, dict[str, dict[str, Any]]]:
    diff: dict[str, dict[str, Any]] = {}
    for key, desired in DESIRED_REPOSITORY_SETTINGS.items():
        actual = meta.get(key)
        if actual != desired:
            diff[key] = {"actual": actual, "desired": desired}
    return (not diff, diff)


def verify_ruleset(ruleset: dict[str, Any]) -> tuple[bool, str]:
    errors: list[str] = []
    if ruleset.get("name") != DEFAULT_RULESET_NAME:
        errors.append(f"name={ruleset.get('name')!r}")
    if ruleset.get("target") != "branch":
        errors.append(f"target={ruleset.get('target')!r}")
    if ruleset.get("enforcement") != "active":
        errors.append(f"enforcement={ruleset.get('enforcement')!r}")
    ref = ((ruleset.get("conditions") or {}).get("ref_name") or {})
    if "~DEFAULT_BRANCH" not in (ref.get("include") or []):
        errors.append("default branch is not included")

    rules = ruleset.get("rules") or []
    types = [rule.get("type") for rule in rules]
    for required in ["deletion", "non_fast_forward", "required_linear_history", "pull_request"]:
        if required not in types:
            errors.append(f"missing rule type {required}")
    pr_rules = [rule for rule in rules if rule.get("type") == "pull_request"]
    if len(pr_rules) != 1:
        errors.append(f"expected one pull_request rule, found {len(pr_rules)}")
    else:
        params = pr_rules[0].get("parameters") or {}
        if params.get("required_approving_review_count") != 0:
            errors.append("pull_request approvals must remain 0 for single-user autonomy")
        if params.get("required_review_thread_resolution") is not True:
            errors.append("review thread resolution must be required")
        methods = set(params.get("allowed_merge_methods") or [])
        if not {"squash", "rebase"}.issubset(methods) or "merge" in methods:
            errors.append(f"unexpected allowed merge methods: {sorted(methods)}")

    status_rules = [rule for rule in rules if rule.get("type") == "required_status_checks"]
    if len(status_rules) != 1:
        errors.append(f"expected one required_status_checks rule, found {len(status_rules)}")
    else:
        params = status_rules[0].get("parameters") or {}
        actual = params.get("required_status_checks") or []
        if actual != REQUIRED_CHECKS:
            errors.append(f"required checks mismatch: {actual!r}")
        if params.get("strict_required_status_checks_policy") is not False:
            errors.append("strict_required_status_checks_policy must be false")
        if params.get("do_not_enforce_on_create") is not True:
            errors.append("do_not_enforce_on_create must be true")
    return (not errors, "; ".join(errors) if errors else "PASS")


def require_gh() -> None:
    if shutil.which("gh") is None:
        raise AdminConvergenceError("GitHub CLI `gh` is not installed or not on PATH")


def _run(args: list[str], *, input_text: str | None = None) -> str:
    completed = subprocess.run(
        args,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise AdminConvergenceError(
            f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stderr.strip()}"
        )
    return completed.stdout


def resolve_repo(explicit: str | None) -> str:
    if explicit:
        if "/" not in explicit:
            raise AdminConvergenceError("--repo must be OWNER/REPO")
        return explicit
    value = _run(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"]).strip()
    if not value or "/" not in value:
        raise AdminConvergenceError("could not resolve current GitHub repository")
    return value


def gh_api_json(path: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
    args = [
        "gh", "api", path,
        "-H", "Accept: application/vnd.github+json",
        "-H", f"X-GitHub-Api-Version: {API_VERSION}",
    ]
    input_text = None
    if method != "GET":
        args += ["--method", method]
    if payload is not None:
        args += ["--input", "-"]
        input_text = json.dumps(payload)
    raw = _run(args, input_text=input_text)
    return json.loads(raw) if raw.strip() else None


def find_repository_ruleset(summaries: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    matches = [
        item for item in summaries
        if item.get("name") == name and item.get("source_type") == "Repository"
    ]
    if len(matches) > 1:
        raise AdminConvergenceError(f"multiple repository rulesets named {name!r}")
    return matches[0] if matches else None


def backup_state(repo: str, repo_meta: dict[str, Any], ruleset: dict[str, Any] | None) -> pathlib.Path:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root = pathlib.Path.home() / ".github-agent-core" / "backups" / repo.replace("/", "__")
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"admin-state-{stamp}.json"
    payload = {"repository": repo, "repository_meta": repo_meta, "ruleset": ruleset}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _old_repo_settings(meta: dict[str, Any]) -> dict[str, Any]:
    return {key: meta.get(key) for key in DESIRED_REPOSITORY_SETTINGS}


def _restore_ruleset(repo: str, previous: dict[str, Any] | None, created_id: int | None) -> str:
    try:
        if previous is not None:
            ruleset_id = int(previous["id"])
            gh_api_json(
                f"repos/{repo}/rulesets/{ruleset_id}",
                method="PUT",
                payload=_update_shape(previous),
            )
            return "restored-previous-ruleset"
        if created_id is not None:
            gh_api_json(f"repos/{repo}/rulesets/{created_id}", method="DELETE")
            return "deleted-new-ruleset"
    except Exception as exc:  # best-effort rollback is evidence, not a hidden success
        return f"ROLLBACK_FAILED: {exc}"
    return "no-ruleset-change-to-rollback"


def converge(repo: str, *, mutate: bool) -> int:
    repo_meta = gh_api_json(f"repos/{repo}")
    if not isinstance(repo_meta, dict):
        raise AdminConvergenceError("invalid repository metadata response")
    settings_ok, settings_diff = verify_repository_settings(repo_meta)

    summaries = gh_api_json(f"repos/{repo}/rulesets") or []
    if not isinstance(summaries, list):
        raise AdminConvergenceError("invalid ruleset list response")
    summary = find_repository_ruleset(summaries, DEFAULT_RULESET_NAME)
    current_ruleset = None
    if summary is not None:
        current_ruleset = gh_api_json(f"repos/{repo}/rulesets/{int(summary['id'])}")
        if not isinstance(current_ruleset, dict):
            raise AdminConvergenceError("invalid existing ruleset response")

    desired_ruleset = build_ruleset_payload(current_ruleset)
    ruleset_ok, ruleset_detail = verify_ruleset(current_ruleset or {})
    desired_ok, desired_detail = verify_ruleset(desired_ruleset)
    if not desired_ok:
        raise AdminConvergenceError(f"internal desired Ruleset is invalid: {desired_detail}")

    report: dict[str, Any] = {
        "repository": repo,
        "mode": "apply" if mutate else "dry-run",
        "repository_settings": {
            "compliant": settings_ok,
            "diff": settings_diff,
            "desired": DESIRED_REPOSITORY_SETTINGS,
        },
        "ruleset": {
            "exists": current_ruleset is not None,
            "compliant": ruleset_ok,
            "detail": ruleset_detail,
            "desired_required_checks": REQUIRED_CHECKS,
        },
    }
    report["would_change"] = (not settings_ok) or (not ruleset_ok)

    if not mutate:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    backup = backup_state(repo, repo_meta, current_ruleset)
    report["backup"] = str(backup)
    created_id: int | None = None
    ruleset_changed = False

    try:
        if not ruleset_ok:
            if current_ruleset is None:
                created = gh_api_json(f"repos/{repo}/rulesets", method="POST", payload=desired_ruleset)
                if not isinstance(created, dict) or created.get("id") is None:
                    raise AdminConvergenceError("Ruleset create returned invalid response")
                created_id = int(created["id"])
                ruleset_id = created_id
            else:
                ruleset_id = int(current_ruleset["id"])
                updated = gh_api_json(
                    f"repos/{repo}/rulesets/{ruleset_id}", method="PUT", payload=desired_ruleset
                )
                if not isinstance(updated, dict):
                    raise AdminConvergenceError("Ruleset update returned invalid response")
            readback = gh_api_json(f"repos/{repo}/rulesets/{ruleset_id}")
            ok, detail = verify_ruleset(readback or {})
            if not ok:
                raise AdminConvergenceError(f"Ruleset read-back verification failed: {detail}")
            ruleset_changed = True

        if not settings_ok:
            patched = gh_api_json(
                f"repos/{repo}", method="PATCH", payload=DESIRED_REPOSITORY_SETTINGS
            )
            if not isinstance(patched, dict):
                raise AdminConvergenceError("repository settings PATCH returned invalid response")
            readback_meta = gh_api_json(f"repos/{repo}")
            ok, diff = verify_repository_settings(readback_meta or {})
            if not ok:
                raise AdminConvergenceError(f"repository settings read-back mismatch: {diff}")

    except Exception as exc:
        rollback: dict[str, Any] = {}
        if not settings_ok:
            try:
                gh_api_json(f"repos/{repo}", method="PATCH", payload=_old_repo_settings(repo_meta))
                rollback["repository_settings"] = "restored-previous-values"
            except Exception as restore_exc:
                rollback["repository_settings"] = f"ROLLBACK_FAILED: {restore_exc}"
        if ruleset_changed or created_id is not None:
            rollback["ruleset"] = _restore_ruleset(repo, current_ruleset, created_id)
        report["rollback"] = rollback
        report["verification"] = "BLOCKED"
        report["error"] = str(exc)
        print(json.dumps(report, indent=2, sort_keys=True))
        raise AdminConvergenceError(
            f"admin convergence failed; rollback={rollback}; original_error={exc}"
        ) from exc

    final_meta = gh_api_json(f"repos/{repo}")
    final_settings_ok, final_diff = verify_repository_settings(final_meta or {})
    final_summaries = gh_api_json(f"repos/{repo}/rulesets") or []
    final_summary = find_repository_ruleset(final_summaries, DEFAULT_RULESET_NAME)
    if final_summary is None:
        raise AdminConvergenceError("post-apply Ruleset missing")
    final_ruleset = gh_api_json(f"repos/{repo}/rulesets/{int(final_summary['id'])}")
    final_ruleset_ok, final_ruleset_detail = verify_ruleset(final_ruleset or {})
    if not final_settings_ok or not final_ruleset_ok:
        raise AdminConvergenceError(
            f"final read-back failed: settings={final_diff}; ruleset={final_ruleset_detail}"
        )

    report["verification"] = "PASS"
    report["final"] = {
        "repository_settings": "PASS",
        "ruleset": "PASS",
        "ruleset_id": final_summary.get("id"),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Dry-run/apply Agent Core V4 repository merge settings and the protect-main Ruleset."
        )
    )
    parser.add_argument("--repo", help="OWNER/REPO; defaults to current gh checkout")
    parser.add_argument("--apply", action="store_true", help="perform admin writes; default is dry-run")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        require_gh()
        repo = resolve_repo(args.repo)
        return converge(repo, mutate=args.apply)
    except (AdminConvergenceError, ValueError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
