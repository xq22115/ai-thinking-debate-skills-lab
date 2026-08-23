#!/usr/bin/env python3
"""Verify that an actor execution remains bound to an approved Git snapshot."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

try:
    from scripts.verify_write_plan_scope import verify_scope
except ModuleNotFoundError:  # direct script execution
    from verify_write_plan_scope import verify_scope

SHA40 = re.compile(r"^[0-9a-f]{40}$")
STRONG_VERIFICATION_ACTORS = {"A08", "A10"}
VALID_VERIFICATION_LEVELS = {"source", "inspection", "static", "readback", "integration", "runtime"}


def _run_git(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def _resolve_commit(repo: pathlib.Path, revision: str) -> tuple[str | None, str | None]:
    completed = _run_git(repo, "rev-parse", "--verify", f"{revision}^{{commit}}")
    if completed.returncode != 0:
        detail = completed.stderr.strip().splitlines()
        return None, detail[-1] if detail else "revision_not_found"
    return completed.stdout.strip(), None


def _show(repo: pathlib.Path, revision: str, path: str) -> tuple[str | None, str | None]:
    completed = _run_git(repo, "show", f"{revision}:{path}")
    if completed.returncode != 0:
        detail = completed.stderr.strip().splitlines()
        return None, detail[-1] if detail else "git_show_failed"
    return completed.stdout, None


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _is_ancestor(repo: pathlib.Path, ancestor: str, descendant: str) -> bool:
    return _run_git(repo, "merge-base", "--is-ancestor", ancestor, descendant).returncode == 0


def _changed_paths(repo: pathlib.Path, start: str, end: str) -> tuple[list[str], str | None]:
    completed = _run_git(
        repo, "diff", "--name-only", "--no-renames", "-z", start, end
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip().splitlines()
        return [], detail[-1] if detail else "git_diff_failed"
    return sorted({item for item in completed.stdout.split("\0") if item}), None


def _plan_path(issue_number: int, run_id: str, actor_id: str) -> str:
    return (
        f"ai-system/control-plane/runs/{issue_number}/{run_id}/plans/"
        f"{actor_id}.json"
    )


def _claim_path(issue_number: int, run_id: str, actor_id: str) -> str:
    return (
        f"ai-system/control-plane/runs/{issue_number}/{run_id}/claims/"
        f"{actor_id}.json"
    )


def _receipt_path(issue_number: int, run_id: str, actor_id: str) -> str:
    return (
        f"ai-system/control-plane/runs/{issue_number}/{run_id}/receipts/"
        f"{actor_id}.json"
    )


def _reasoning_quality_failures(actor_id: str, receipt: dict) -> list[str]:
    failures: list[str] = []
    quality = receipt.get("reasoning_quality")
    if not isinstance(quality, dict):
        return ["receipt_reasoning_quality_missing"]
    required = [
        "task_class", "objective_model", "causal_model", "high_impact_unknowns",
        "evidence_delta", "stagnation_state", "verification_level",
        "adversarial_check", "research_stop_reason",
    ]
    for field in required:
        if quality.get(field) in (None, ""):
            failures.append(f"receipt_reasoning_quality_missing_{field}")
    unknowns = quality.get("high_impact_unknowns")
    if not isinstance(unknowns, list):
        failures.append("receipt_reasoning_quality_unknowns_invalid")
        unknowns = []
    level = quality.get("verification_level")
    if level not in VALID_VERIFICATION_LEVELS:
        failures.append("receipt_reasoning_quality_verification_level_invalid")
    if receipt.get("result") == "PASS":
        if unknowns:
            failures.append("receipt_pass_has_high_impact_unknowns")
        if quality.get("research_stop_reason") == "blocked":
            failures.append("receipt_pass_research_blocked")
        if actor_id in STRONG_VERIFICATION_ACTORS and level not in {"readback", "integration", "runtime"}:
            failures.append("receipt_pass_weak_verification_level")
    return failures


def verify_execution(
    repo: pathlib.Path,
    issue_number: int,
    run_id: str,
    actor_id: str,
    snapshot: dict,
    final_head_sha: str,
) -> dict[str, object]:
    failures: list[str] = []
    branch = str(snapshot.get("branch", ""))
    plan_head = str(snapshot.get("plan_head_sha", ""))
    if not repo.is_dir() or not (repo / ".git").exists():
        failures.append("repository_not_git_worktree")
    if issue_number < 1 or not run_id or not actor_id:
        failures.append("invalid_execution_identity")
    if not SHA40.fullmatch(plan_head):
        failures.append("invalid_plan_head_sha")
    if not SHA40.fullmatch(final_head_sha):
        failures.append("invalid_final_head_sha")

    current_head, current_error = _resolve_commit(repo, branch)
    if current_error is not None:
        failures.append(f"branch_resolution_failed:{current_error}")
    elif current_head != final_head_sha:
        failures.append("final_head_not_current_branch_head")

    final_resolved, final_error = _resolve_commit(repo, final_head_sha)
    if final_error is not None or final_resolved != final_head_sha:
        failures.append("final_head_not_resolvable_commit")
    if SHA40.fullmatch(plan_head) and SHA40.fullmatch(final_head_sha):
        if not _is_ancestor(repo, plan_head, final_head_sha):
            failures.append("plan_snapshot_not_ancestor")

    plan_path = _plan_path(issue_number, run_id, actor_id)
    claim_path = _claim_path(issue_number, run_id, actor_id)
    approved_plan_text, approved_plan_error = _show(repo, plan_head, plan_path)
    approved_claim_text, approved_claim_error = _show(repo, plan_head, claim_path)
    final_plan_text, final_plan_error = _show(repo, final_head_sha, plan_path)
    final_claim_text, final_claim_error = _show(repo, final_head_sha, claim_path)

    if approved_plan_error is not None:
        failures.append("approved_plan_missing")
    if approved_claim_error is not None:
        failures.append("approved_claim_missing")
    if final_plan_error is not None:
        failures.append("final_plan_missing")
    if final_claim_error is not None:
        failures.append("final_claim_missing")

    if approved_plan_text is not None:
        if _sha256(approved_plan_text) != snapshot.get("plan_sha256"):
            failures.append("approved_plan_hash_mismatch")
    if approved_claim_text is not None:
        if _sha256(approved_claim_text) != snapshot.get("claim_sha256"):
            failures.append("approved_claim_hash_mismatch")
    if final_plan_text is not None:
        if _sha256(final_plan_text) != snapshot.get("plan_sha256"):
            failures.append("plan_snapshot_changed")
    if final_claim_text is not None:
        if _sha256(final_claim_text) != snapshot.get("claim_sha256"):
            failures.append("claim_snapshot_changed")

    plan: dict = {}
    claim: dict = {}
    if approved_plan_text is not None:
        try:
            plan = json.loads(approved_plan_text)
        except Exception:
            failures.append("approved_plan_invalid_json")
    if approved_claim_text is not None:
        try:
            claim = json.loads(approved_claim_text)
        except Exception:
            failures.append("approved_claim_invalid_json")

    identity_checks = {
        "plan_issue_mismatch": plan.get("issue_number") == issue_number,
        "plan_run_id_mismatch": plan.get("run_id") == run_id,
        "plan_actor_mismatch": plan.get("actor_id") == actor_id,
        "plan_branch_mismatch": plan.get("branch") == branch,
        "claim_issue_mismatch": claim.get("issue_number") == issue_number,
        "claim_run_id_mismatch": claim.get("run_id") == run_id,
        "claim_actor_mismatch": claim.get("actor_id") == actor_id,
        "claim_branch_mismatch": claim.get("branch") == branch,
        "claim_id_mismatch": claim.get("claim_id") == snapshot.get("claim_id"),
        "executor_id_mismatch": claim.get("executor_id") == snapshot.get("executor_id"),
        "execution_id_mismatch": claim.get("execution_id") == snapshot.get("execution_id"),
    }
    for failure, valid in identity_checks.items():
        if not valid:
            failures.append(failure)

    own_receipt = _receipt_path(issue_number, run_id, actor_id)
    final_receipt_text, receipt_error = _show(repo, final_head_sha, own_receipt)
    receipt: dict = {}
    receipt_failures: list[str] = []
    work_head = final_head_sha
    if receipt_error is not None:
        receipt_failures.append("final_receipt_missing")
    else:
        try:
            receipt = json.loads(final_receipt_text or "")
        except Exception:
            receipt_failures.append("final_receipt_invalid_json")

    if receipt:
        receipt_checks = {
            "receipt_schema_version_not_v3": receipt.get("schema_version") == 3,
            "receipt_issue_mismatch": receipt.get("issue_number") == issue_number,
            "receipt_run_id_mismatch": receipt.get("run_id") == run_id,
            "receipt_agent_id_mismatch": receipt.get("agent_id") == actor_id,
            "receipt_branch_mismatch": receipt.get("branch") == branch,
            "receipt_claim_id_mismatch": receipt.get("claim_id") == snapshot.get("claim_id"),
            "receipt_executor_id_mismatch": receipt.get("executor_id") == snapshot.get("executor_id"),
            "receipt_execution_id_mismatch": receipt.get("execution_id") == snapshot.get("execution_id"),
            "receipt_plan_head_sha_mismatch": receipt.get("plan_head_sha") == plan_head,
            "receipt_independence_not_asserted": receipt.get("independent_agent_execution") is True,
            "receipt_result_not_pass_or_veto": receipt.get("result") in {"PASS", "VETO"},
        }
        for failure, valid in receipt_checks.items():
            if not valid:
                receipt_failures.append(failure)
        receipt_failures.extend(_reasoning_quality_failures(actor_id, receipt))
        candidate_work_head = str(receipt.get("head_sha", ""))
        if not SHA40.fullmatch(candidate_work_head):
            receipt_failures.append("receipt_invalid_work_head_sha")
        else:
            resolved_work_head, work_error = _resolve_commit(repo, candidate_work_head)
            if work_error is not None or resolved_work_head != candidate_work_head:
                receipt_failures.append("receipt_work_head_not_resolvable")
            else:
                work_head = candidate_work_head
                if SHA40.fullmatch(plan_head) and not _is_ancestor(repo, plan_head, work_head):
                    receipt_failures.append("receipt_work_head_before_plan_snapshot")
                if SHA40.fullmatch(final_head_sha) and not _is_ancestor(repo, work_head, final_head_sha):
                    receipt_failures.append("receipt_work_head_not_ancestor_of_final")

    if receipt and SHA40.fullmatch(work_head) and SHA40.fullmatch(final_head_sha):
        parent_run = _run_git(repo, "rev-list", "--parents", "-n", "1", final_head_sha)
        parent_fields = parent_run.stdout.strip().split() if parent_run.returncode == 0 else []
        if len(parent_fields) != 2 or parent_fields[0] != final_head_sha or parent_fields[1] != work_head:
            receipt_failures.append("receipt_commit_not_immediate_child_of_work_head")

    failures.extend(receipt_failures)
    receipt_identity_bound = bool(receipt) and not receipt_failures

    changed_paths: list[str] = []
    task_changed_paths: list[str] = []
    post_work_paths: list[str] = []
    if SHA40.fullmatch(plan_head) and SHA40.fullmatch(final_head_sha):
        changed_paths, diff_error = _changed_paths(repo, plan_head, final_head_sha)
        if diff_error is not None:
            failures.append(f"diff_failed:{diff_error}")
    if SHA40.fullmatch(plan_head) and SHA40.fullmatch(work_head):
        task_changed_paths, task_diff_error = _changed_paths(repo, plan_head, work_head)
        if task_diff_error is not None:
            failures.append(f"task_diff_failed:{task_diff_error}")
    if receipt and SHA40.fullmatch(work_head) and SHA40.fullmatch(final_head_sha):
        post_work_paths, post_diff_error = _changed_paths(repo, work_head, final_head_sha)
        if post_diff_error is not None:
            failures.append(f"post_work_diff_failed:{post_diff_error}")
        elif post_work_paths != [own_receipt]:
            failures.append("post_work_diff_not_receipt_only")

    scope = verify_scope(plan, task_changed_paths) if plan else {
        "result": "VETO", "invalid_changed_paths": [], "undeclared_paths": task_changed_paths
    }
    invalid_paths = list(scope.get("invalid_changed_paths") or [])
    undeclared_paths = list(scope.get("undeclared_paths") or [])
    if scope.get("result") != "PASS":
        failures.append("write_scope_veto")

    evidence_exception_paths = (
        [own_receipt] if receipt and post_work_paths == [own_receipt] else []
    )
    return {
        "schemaVersion": 3,
        "issue_number": issue_number,
        "run_id": run_id,
        "actor_id": actor_id,
        "branch": branch,
        "plan_head_sha": plan_head,
        "work_head_sha": work_head,
        "final_head_sha": final_head_sha,
        "current_branch_head": current_head,
        "changed_paths": changed_paths,
        "task_changed_paths": task_changed_paths,
        "post_work_paths": post_work_paths,
        "receipt_identity_bound": receipt_identity_bound,
        "evidence_exception_paths": evidence_exception_paths,
        "invalid_changed_paths": invalid_paths,
        "undeclared_paths": undeclared_paths,
        "failures": sorted(set(failures)),
        "result": "PASS" if not failures else "VETO",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--issue", type=int, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--snapshot-json", required=True)
    parser.add_argument("--final-head", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    snapshot = json.loads(pathlib.Path(args.snapshot_json).read_text(encoding="utf-8"))
    result = verify_execution(
        pathlib.Path(args.repo), args.issue, args.run_id, args.actor,
        snapshot, args.final_head,
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
