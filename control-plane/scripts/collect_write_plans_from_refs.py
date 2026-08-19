#!/usr/bin/env python3
"""Collect per-actor write plans from isolated Git refs without shared writes.

Each writer commits its own plan only on its own branch. The orchestrator reads
those immutable snapshots with `git show` into a temporary directory, then feeds
the collected files to `check_write_plan_conflicts.py`. No shared plan ledger is
mutated by concurrent writers.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess

ACTOR_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
REF_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,239}$")


def _valid_actor(actor: str) -> bool:
    return bool(ACTOR_RE.fullmatch(actor))


def _valid_ref(ref: str) -> bool:
    if not REF_RE.fullmatch(ref):
        return False
    if ref.endswith(("/", ".")) or ".." in ref or "//" in ref or "@{" in ref:
        return False
    return not any(char in ref for char in " ~^:?*[\\")


def _claim_path(issue_number: int, run_id: str, actor_id: str) -> str:
    return (
        f"ai-system/control-plane/runs/{issue_number}/{run_id}/claims/"
        f"{actor_id}.json"
    )


def _plan_path(issue_number: int, run_id: str, actor_id: str) -> str:
    return (
        f"ai-system/control-plane/runs/{issue_number}/{run_id}/plans/"
        f"{actor_id}.json"
    )


def _resolve_ref(repo: pathlib.Path, ref: str) -> tuple[str | None, str | None]:
    completed = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", f"{ref}^{{commit}}"],
        text=True, capture_output=True, check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip().splitlines()
        summary = detail[-1] if detail else f"git rev-parse exit {completed.returncode}"
        return None, summary
    return completed.stdout.strip(), None


def _git_show(repo: pathlib.Path, ref: str, path: str) -> tuple[str | None, str | None]:
    completed = subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{path}"],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip().splitlines()
        summary = detail[-1] if detail else f"git show exit {completed.returncode}"
        return None, summary
    return completed.stdout, None


def collect_plans(
    repo: pathlib.Path,
    assignments: dict[str, str],
    issue_number: int,
    run_id: str,
    output_dir: pathlib.Path,
) -> dict[str, object]:
    errors: list[str] = []
    collected: dict[str, dict] = {}

    if not repo.is_dir() or not (repo / ".git").exists():
        errors.append("repository_not_git_worktree")
    if issue_number < 1:
        errors.append("invalid_issue_number")
    if not run_id or "/" in run_id or ".." in run_id:
        errors.append("invalid_run_id")
    if not assignments:
        errors.append("no_assignments")

    refs = list(assignments.values())
    if len(set(refs)) != len(refs):
        errors.append("duplicate_ref")

    for actor_id, ref in assignments.items():
        if not _valid_actor(actor_id):
            errors.append(f"invalid_actor:{actor_id}")
        if not _valid_ref(ref):
            errors.append(f"invalid_ref:{actor_id}:{ref}")

    if output_dir.exists() and any(output_dir.iterdir()):
        errors.append("output_dir_not_empty")

    if errors:
        return {
            "schemaVersion": 1,
            "collected": [],
            "errors": errors,
            "result": "VETO",
        }

    snapshots: dict[str, dict] = {}
    for actor_id, ref in sorted(assignments.items()):
        resolved_sha, resolve_error = _resolve_ref(repo, ref)
        if resolve_error is not None or not resolved_sha:
            errors.append(f"ref_resolution_failed:{actor_id}:{ref}:{resolve_error}")
            continue

        path = _plan_path(issue_number, run_id, actor_id)
        text, show_error = _git_show(repo, resolved_sha, path)
        if show_error is not None:
            errors.append(f"plan_missing:{actor_id}:{ref}:{show_error}")
            continue
        claim_path = _claim_path(issue_number, run_id, actor_id)
        claim_text, claim_error = _git_show(repo, resolved_sha, claim_path)
        if claim_error is not None:
            errors.append(f"claim_missing:{actor_id}:{ref}:{claim_error}")
            continue
        try:
            plan = json.loads(text or "")
        except Exception as exc:
            errors.append(f"invalid_plan_json:{actor_id}:{exc}")
            continue
        try:
            claim = json.loads(claim_text or "")
        except Exception as exc:
            errors.append(f"invalid_claim_json:{actor_id}:{exc}")
            continue
        if plan.get("actor_id") != actor_id:
            errors.append(f"actor_mismatch:{actor_id}:{plan.get('actor_id')}")
        if plan.get("issue_number") != issue_number:
            errors.append(f"issue_mismatch:{actor_id}")
        if plan.get("run_id") != run_id:
            errors.append(f"run_id_mismatch:{actor_id}")
        if plan.get("branch") != ref:
            errors.append(f"branch_mismatch:{actor_id}:{plan.get('branch')}:{ref}")
        if claim.get("actor_id") != actor_id:
            errors.append(f"claim_actor_mismatch:{actor_id}:{claim.get('actor_id')}")
        if claim.get("issue_number") != issue_number:
            errors.append(f"claim_issue_mismatch:{actor_id}")
        if claim.get("run_id") != run_id:
            errors.append(f"claim_run_id_mismatch:{actor_id}")
        if claim.get("branch") != ref:
            errors.append(f"claim_branch_mismatch:{actor_id}:{claim.get('branch')}:{ref}")
        if claim.get("base_sha") != plan.get("base_sha"):
            errors.append(f"claim_base_sha_mismatch:{actor_id}")
        if claim.get("status") != "CLAIMED":
            errors.append(f"claim_status:{actor_id}:{claim.get('status')}")
        for field in ["claim_id", "executor_id", "execution_id"]:
            if not str(claim.get(field, "")).strip():
                errors.append(f"claim_missing_{field}:{actor_id}")
        collected[actor_id] = plan
        snapshots[actor_id] = {
            "branch": ref,
            "plan_head_sha": resolved_sha,
            "plan_sha256": hashlib.sha256((text or "").encode("utf-8")).hexdigest(),
            "claim_sha256": hashlib.sha256((claim_text or "").encode("utf-8")).hexdigest(),
            "claim_id": claim.get("claim_id"),
            "executor_id": claim.get("executor_id"),
            "execution_id": claim.get("execution_id"),
        }

    if errors:
        return {
            "schemaVersion": 2,
            "collected": sorted(collected),
            "snapshots": snapshots,
            "errors": errors,
            "result": "VETO",
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    for actor_id, plan in sorted(collected.items()):
        (output_dir / f"{actor_id}.json").write_text(
            json.dumps(plan, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return {
        "schemaVersion": 2,
        "collected": sorted(collected),
        "snapshots": snapshots,
        "errors": [],
        "output_directory": str(output_dir),
        "result": "PASS",
    }


def _parse_entries(values: list[str]) -> tuple[dict[str, str], list[str]]:
    assignments: dict[str, str] = {}
    errors: list[str] = []
    for value in values:
        if "=" not in value:
            errors.append(f"entry_missing_equals:{value}")
            continue
        actor, ref = value.split("=", 1)
        if actor in assignments:
            errors.append(f"duplicate_actor_entry:{actor}")
            continue
        assignments[actor] = ref
    return assignments, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--issue", type=int, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--entry", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--receipt")
    args = parser.parse_args()

    assignments, entry_errors = _parse_entries(args.entry)
    if entry_errors:
        result = {
            "schemaVersion": 1,
            "collected": [],
            "errors": entry_errors,
            "result": "VETO",
        }
    else:
        result = collect_plans(
            pathlib.Path(args.repo),
            assignments,
            args.issue,
            args.run_id,
            pathlib.Path(args.output_dir),
        )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.receipt:
        pathlib.Path(args.receipt).write_text(text, encoding="utf-8")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
