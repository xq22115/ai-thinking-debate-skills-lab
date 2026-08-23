#!/usr/bin/env python3
"""Trusted finalizer for one wrapper-observed local agent execution."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

try:
    from scripts.adjudicate_agent_receipts import EXPECTED
    from scripts.verify_snapshot_bound_execution import verify_execution
    from scripts.verify_write_plan_scope import verify_scope
except ModuleNotFoundError:
    from adjudicate_agent_receipts import EXPECTED
    from verify_snapshot_bound_execution import verify_execution
    from verify_write_plan_scope import verify_scope

VALID_MODEL_DECISIONS = {"PASS", "VETO", "FAIL", "BLOCKED"}
STRONG_VERIFICATION_ACTORS = {"A08", "A10"}


def _git(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def _git_text(repo: pathlib.Path, *args: str) -> str | None:
    cp = _git(repo, *args)
    return cp.stdout.strip() if cp.returncode == 0 else None


def _show_json(repo: pathlib.Path, revision: str, path: str) -> dict | None:
    text = _git_text(repo, "show", f"{revision}:{path}")
    if text is None:
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _receipt_path(issue: int, run_id: str, actor: str) -> str:
    return f"ai-system/control-plane/runs/{issue}/{run_id}/receipts/{actor}.json"


def _plan_path(issue: int, run_id: str, actor: str) -> str:
    return f"ai-system/control-plane/runs/{issue}/{run_id}/plans/{actor}.json"


def _split_z(text: str) -> list[str]:
    return [item for item in text.split("\0") if item]


def _working_paths(repo: pathlib.Path) -> tuple[list[str], bool, list[str]]:
    failures: list[str] = []
    staged = _git(repo, "diff", "--cached", "--quiet")
    staged_dirty = staged.returncode != 0
    tracked = _git(repo, "diff", "--name-only", "--no-renames", "-z", "HEAD")
    untracked = _git(repo, "ls-files", "--others", "--exclude-standard", "-z")
    if tracked.returncode != 0:
        failures.append("working_diff_failed")
        tracked_paths: list[str] = []
    else:
        tracked_paths = _split_z(tracked.stdout)
    if untracked.returncode != 0:
        failures.append("untracked_scan_failed")
        untracked_paths: list[str] = []
    else:
        untracked_paths = _split_z(untracked.stdout)
    return sorted(set(tracked_paths + untracked_paths)), staged_dirty, failures


def _commit_paths(repo: pathlib.Path, paths: list[str], message: str) -> str | None:
    if not paths:
        return _git_text(repo, "rev-parse", "HEAD")
    add = _git(repo, "add", "-A", "--", *paths)
    if add.returncode != 0:
        return None
    commit = _git(
        repo, "-c", "user.name=Agent Control Plane",
        "-c", "user.email=agent-control-plane@local.invalid",
        "commit", "-m", message,
    )
    return _git_text(repo, "rev-parse", "HEAD") if commit.returncode == 0 else None


def _reasoning_quality_failures(actor: str, decision: dict) -> list[str]:
    failures: list[str] = []
    quality = decision.get("reasoning_quality")
    if not isinstance(quality, dict):
        return ["decision_reasoning_quality_missing"]
    required = [
        "task_class", "objective_model", "causal_model", "high_impact_unknowns",
        "evidence_delta", "stagnation_state", "verification_level",
        "adversarial_check", "research_stop_reason",
    ]
    for field in required:
        if quality.get(field) in (None, ""):
            failures.append(f"decision_reasoning_quality_missing_{field}")
    unknowns = quality.get("high_impact_unknowns")
    if not isinstance(unknowns, list):
        failures.append("decision_reasoning_quality_unknowns_invalid")
    if decision.get("decision") == "PASS":
        if unknowns:
            failures.append("decision_pass_has_high_impact_unknowns")
        if quality.get("research_stop_reason") == "blocked":
            failures.append("decision_pass_research_blocked")
        if actor in STRONG_VERIFICATION_ACTORS and quality.get("verification_level") not in {"readback", "integration", "runtime"}:
            failures.append("decision_pass_weak_verification_level")
    return failures


def _identity_failures(actor: str, snapshot: dict, execution: dict) -> list[str]:
    failures: list[str] = []
    expected = {
        "actor_id": actor,
        "branch": snapshot.get("branch"),
        "claim_id": snapshot.get("claim_id"),
        "executor_id": snapshot.get("executor_id"),
        "execution_id": snapshot.get("execution_id"),
        "plan_head_sha": snapshot.get("plan_head_sha"),
    }
    for field, value in expected.items():
        if execution.get(field) != value:
            failures.append(f"{field}_mismatch")
    if execution.get("exit_code") != 0:
        failures.append("executor_exit_nonzero")
    if execution.get("failures"):
        failures.append("executor_reported_failures")
    if not str(execution.get("session_id", "")).strip():
        failures.append("backend_session_missing")
    if not isinstance(execution.get("pid"), int) or execution.get("pid", 0) <= 0:
        failures.append("process_id_invalid")
    if not str(execution.get("process_instance_id", "")).strip():
        failures.append("process_instance_missing")
    if not isinstance(execution.get("spawn_monotonic_ns"), int) or execution.get("spawn_monotonic_ns", 0) <= 0:
        failures.append("spawn_monotonic_ns_invalid")
    decision = execution.get("decision")
    if not isinstance(decision, dict):
        failures.append("decision_missing")
    else:
        if decision.get("agent_id") != actor:
            failures.append("decision_agent_mismatch")
        if decision.get("decision") not in VALID_MODEL_DECISIONS:
            failures.append("decision_invalid")
        failures.extend(_reasoning_quality_failures(actor, decision))
    return failures


def finalize_execution(
    repo: pathlib.Path,
    actor: str,
    snapshot: dict,
    execution: dict,
) -> dict[str, object]:
    failures: list[str] = []
    if actor not in EXPECTED:
        return {"result": "VETO", "failures": ["unknown_actor"]}
    if not repo.is_dir() or not (repo / ".git").exists():
        return {"result": "VETO", "failures": ["repository_not_git_worktree"]}

    failures.extend(_identity_failures(actor, snapshot, execution))
    branch = str(snapshot.get("branch", ""))
    plan_head = str(snapshot.get("plan_head_sha", ""))
    current_branch = _git_text(repo, "branch", "--show-current")
    current_head = _git_text(repo, "rev-parse", "HEAD")
    if current_branch != branch:
        failures.append("current_branch_mismatch")
    if current_head != plan_head:
        failures.append("workspace_head_not_plan_snapshot")

    issue = execution.get("issue_number")
    run_id = str(execution.get("run_id", ""))
    if not isinstance(issue, int) or issue < 1:
        failures.append("invalid_issue_number")
    if not run_id:
        failures.append("run_id_missing")

    plan: dict = {}
    if isinstance(issue, int) and issue >= 1 and run_id and plan_head:
        plan = _show_json(repo, plan_head, _plan_path(issue, run_id, actor)) or {}
    if not plan:
        failures.append("approved_plan_missing_or_invalid")
    else:
        if plan.get("issue_number") != issue:
            failures.append("plan_issue_mismatch")
        if plan.get("run_id") != run_id:
            failures.append("plan_run_id_mismatch")
        if plan.get("actor_id") != actor:
            failures.append("plan_actor_mismatch")
        if plan.get("branch") != branch:
            failures.append("plan_branch_mismatch")

    receipt_path = _receipt_path(issue, run_id, actor) if isinstance(issue, int) else ""
    if receipt_path and (repo / receipt_path).exists():
        failures.append("receipt_already_exists")

    changed_paths, staged_dirty, path_failures = _working_paths(repo)
    failures.extend(path_failures)
    if staged_dirty:
        failures.append("preexisting_staged_changes")

    decision = execution.get("decision") if isinstance(execution.get("decision"), dict) else {}
    decision_value = decision.get("decision")
    if decision_value != "PASS" and changed_paths:
        failures.append("nonpass_workspace_modified")
    if actor != "A07" and changed_paths:
        failures.append("readonly_workspace_modified")

    if actor == "A07" and decision_value == "PASS" and changed_paths and plan:
        scope = verify_scope(plan, changed_paths)
        if scope.get("result") != "PASS":
            failures.append("write_scope_veto")
    if failures:
        return {
            "schemaVersion": 1,
            "actor_id": actor,
            "changed_paths": changed_paths,
            "failures": sorted(set(failures)),
            "result": "VETO",
        }

    if decision_value in {"FAIL", "BLOCKED"}:
        return {
            "schemaVersion": 1,
            "actor_id": actor,
            "changed_paths": [],
            "failures": [],
            "result": decision_value,
        }

    if decision_value not in {"PASS", "VETO"}:
        return {
            "schemaVersion": 1,
            "actor_id": actor,
            "failures": ["unsupported_receipt_decision"],
            "result": "VETO",
        }

    work_head = plan_head
    if actor == "A07" and changed_paths:
        work_head = _commit_paths(repo, changed_paths, f"feat(run): materialize {actor} work")
        if not work_head:
            return {"result": "FAIL", "failures": ["work_commit_failed"]}

    post_work_paths, post_staged, post_failures = _working_paths(repo)
    if post_failures or post_staged or post_work_paths:
        return {
            "result": "FAIL",
            "failures": ["workspace_not_clean_after_work_commit", *post_failures],
        }

    session_id = str(execution["session_id"])
    session_sha256 = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    evidence_partition = f"local-executor/{run_id}/{actor}/{session_sha256}"
    receipt = {
        "schema_version": 3,
        "issue_number": issue,
        "run_id": run_id,
        "agent_id": actor,
        "role": EXPECTED[actor],
        "branch": branch,
        "claim_id": str(execution["claim_id"]),
        "plan_head_sha": plan_head,
        "head_sha": work_head,
        "result": decision_value,
        "independent_agent_execution": True,
        "executor_id": str(execution["executor_id"]),
        "execution_id": str(execution["execution_id"]),
        "evidence_partition": evidence_partition,
        "reasoning_quality": decision["reasoning_quality"],
        "runtime_attestation": {
            "provider": "claude-code",
            "observer": "scripts/local_agent_executor.py",
            "process_instance_id": str(execution["process_instance_id"]),
            "process_id": int(execution["pid"]),
            "spawn_monotonic_ns": int(execution["spawn_monotonic_ns"]),
            "backend_session_sha256": session_sha256,
            "stdout_sha256": str(execution.get("stdout_sha256", "")),
            "stderr_sha256": str(execution.get("stderr_sha256", "")),
        },
        "evidence": [{
            "kind": "tool",
            "reference": f"local-agent-executor-session-sha256:{session_sha256}",
            "result": "PASS",
            "sha": work_head,
            "summary": (
                f"pid={execution['pid']}; stdout_sha256={execution.get('stdout_sha256','')}; "
                f"decision={decision_value}; {decision.get('summary','')}"
            ),
        }],
    }
    if decision_value == "VETO":
        receipt["veto_reason"] = str(decision.get("summary") or "local agent veto")

    receipt_file = repo / receipt_path
    receipt_file.parent.mkdir(parents=True, exist_ok=True)
    receipt_file.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    final_head = _commit_paths(repo, [receipt_path], f"chore(run): record {actor} receipt")
    if not final_head:
        return {"result": "FAIL", "failures": ["receipt_commit_failed"]}

    snapshot_result = verify_execution(
        repo, int(issue), run_id, actor, snapshot, final_head
    )
    if snapshot_result.get("result") != "PASS":
        return {
            "schemaVersion": 1,
            "actor_id": actor,
            "work_head_sha": work_head,
            "final_head_sha": final_head,
            "snapshot_verification": snapshot_result,
            "failures": ["snapshot_verification_failed"],
            "result": "VETO",
        }
    return {
        "schemaVersion": 1,
        "actor_id": actor,
        "work_head_sha": work_head,
        "final_head_sha": final_head,
        "receipt_path": receipt_path,
        "snapshot_verification": snapshot_result,
        "failures": [],
        "result": decision_value,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--actor", required=True)
    parser.add_argument("--snapshot-json", required=True)
    parser.add_argument("--execution-json", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    snapshot = json.loads(pathlib.Path(args.snapshot_json).read_text(encoding="utf-8"))
    execution = json.loads(pathlib.Path(args.execution_json).read_text(encoding="utf-8"))
    result = finalize_execution(
        pathlib.Path(args.repo), args.actor, snapshot, execution
    )
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
