#!/usr/bin/env python3
"""Launch ten independently attributable local Claude Code processes fail-closed."""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time
import uuid

EXPECTED_ACTORS = [f"A{i:02d}" for i in range(1, 11)]
VALID_DECISIONS = {"PASS", "VETO", "FAIL", "BLOCKED"}
REASONING_LEVELS = {"source", "inspection", "static", "readback", "integration", "runtime"}
STRONG_VERIFICATION_ACTORS = {"A08", "A10"}
DECISION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["agent_id", "decision", "summary", "evidence", "reasoning_quality"],
    "properties": {
        "agent_id": {"enum": EXPECTED_ACTORS},
        "decision": {"enum": sorted(VALID_DECISIONS)},
        "summary": {"type": "string"},
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["kind", "reference"],
                "properties": {
                    "kind": {"type": "string"},
                    "reference": {"type": "string"},
                },
            },
        },
        "reasoning_quality": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "task_class",
                "objective_model",
                "causal_model",
                "high_impact_unknowns",
                "evidence_delta",
                "stagnation_state",
                "verification_level",
                "adversarial_check",
                "research_stop_reason",
            ],
            "properties": {
                "task_class": {"enum": ["simple", "material", "critical"]},
                "objective_model": {"type": "string", "minLength": 1},
                "causal_model": {"type": "string", "minLength": 1},
                "high_impact_unknowns": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                },
                "evidence_delta": {"type": "string", "minLength": 1},
                "stagnation_state": {"enum": ["NOT_APPLICABLE", "CLEAR", "PIVOTED"]},
                "verification_level": {"enum": sorted(REASONING_LEVELS)},
                "adversarial_check": {"type": "string", "minLength": 1},
                "research_stop_reason": {"enum": ["not_needed", "decision_saturated", "blocked"]},
                "remaining_risks": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                },
            },
        },
    },
}


def _run(command: list[str], *, timeout: float = 10.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def probe_claude(claude_path: pathlib.Path | str) -> dict[str, object]:
    path = pathlib.Path(claude_path)
    if not path.is_file() or not os.access(path, os.X_OK):
        return {
            "backend": "claude",
            "path": str(path),
            "logged_in": False,
            "failures": ["backend_executable_missing"],
            "result": "BLOCKED",
        }
    try:
        version_run = _run([str(path), "--version"])
        auth_run = _run([str(path), "auth", "status"])
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "backend": "claude",
            "path": str(path),
            "logged_in": False,
            "failures": [f"backend_probe_failed:{type(exc).__name__}"],
            "result": "BLOCKED",
        }
    failures: list[str] = []
    if version_run.returncode != 0:
        failures.append(f"version_probe_exit:{version_run.returncode}")
    if auth_run.returncode != 0:
        failures.append(f"auth_probe_exit:{auth_run.returncode}")
    try:
        auth = json.loads(auth_run.stdout or "{}")
    except json.JSONDecodeError:
        auth = {}
        failures.append("auth_status_invalid_json")
    logged_in = auth.get("loggedIn") is True
    if not logged_in:
        failures.append("backend_not_authenticated")
    return {
        "backend": "claude",
        "path": str(path),
        "version": version_run.stdout.strip(),
        "logged_in": logged_in,
        "auth": auth,
        "failures": failures,
        "result": "PASS" if not failures else "BLOCKED",
    }


def build_claude_command(
    claude_path: pathlib.Path | str,
    actor_id: str,
    prompt: str,
    *,
    max_budget_usd: float,
    model: str | None = None,
    read_dirs: list[str] | None = None,
) -> list[str]:
    command = [
        str(claude_path),
        "-p",
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(DECISION_SCHEMA, separators=(",", ":")),
        "--max-budget-usd",
        str(max_budget_usd),
    ]
    read_dirs = list(read_dirs or [])
    if actor_id == "A07" and read_dirs:
        raise ValueError("write_role_external_read_dir_forbidden")
    if read_dirs:
        command += ["--add-dir", *read_dirs]
    allowed_tools = "Read,Glob,Grep,Edit,Write" if actor_id == "A07" else "Read,Glob,Grep"
    command += ["--allowedTools", allowed_tools]
    if model:
        command += ["--model", model]
    command.append(prompt)
    return command


def _is_sha40(value: object) -> bool:
    text = str(value or "")
    return len(text) == 40 and all(ch in "0123456789abcdef" for ch in text)


def _assignment_failures(assignments: list[dict]) -> list[str]:
    failures: list[str] = []
    actors = [str(row.get("actor_id", "")) for row in assignments]
    if sorted(actors) != EXPECTED_ACTORS:
        failures.append("actor_set_mismatch")
    workspaces = [str(row.get("workspace", "")) for row in assignments]
    branches = [str(row.get("branch", "")) for row in assignments]
    claim_ids = [str(row.get("claim_id", "")) for row in assignments]
    executor_ids = [str(row.get("executor_id", "")) for row in assignments]
    execution_ids = [str(row.get("execution_id", "")) for row in assignments]
    if len(set(workspaces)) != len(workspaces):
        failures.append("duplicate_workspace")
    if len(set(branches)) != len(branches):
        failures.append("duplicate_branch")
    if len(set(filter(None, claim_ids))) != len(list(filter(None, claim_ids))):
        failures.append("duplicate_claim_id")
    if len(set(filter(None, executor_ids))) != len(list(filter(None, executor_ids))):
        failures.append("duplicate_executor_id")
    if len(set(filter(None, execution_ids))) != len(list(filter(None, execution_ids))):
        failures.append("duplicate_execution_id")
    for row in assignments:
        actor = str(row.get("actor_id", ""))
        workspace = pathlib.Path(str(row.get("workspace", "")))
        branch = str(row.get("branch", ""))
        for field in ["issue_number", "run_id", "claim_id", "executor_id", "execution_id", "plan_head_sha"]:
            if row.get(field) in (None, ""):
                failures.append(f"missing_{field}:{actor}")
        issue_number = row.get("issue_number")
        if not isinstance(issue_number, int) or issue_number < 1:
            failures.append(f"invalid_issue_number:{actor}")
        if row.get("plan_head_sha") not in (None, "") and not _is_sha40(row.get("plan_head_sha")):
            failures.append(f"invalid_plan_head_sha:{actor}")
        if not workspace.is_dir():
            failures.append(f"workspace_missing:{actor}")
        if actor and f"/{actor}/" not in branch:
            failures.append(f"branch_not_actor_scoped:{actor}")
        run_id = str(row.get("run_id", ""))
        if run_id and not branch.endswith(f"/{run_id}"):
            failures.append(f"branch_run_id_mismatch:{actor}")
        read_dirs = row.get("read_dirs") or []
        if not isinstance(read_dirs, list) or not all(isinstance(item, str) and item for item in read_dirs):
            failures.append(f"invalid_dependency_read_dirs:{actor}")
            read_dirs = []
        if actor == "A07" and read_dirs:
            failures.append(f"write_role_external_read_dir_forbidden:{actor}")
        if len(set(read_dirs)) != len(read_dirs):
            failures.append(f"duplicate_dependency_read_dir:{actor}")
        if actor != "A07":
            for item in read_dirs:
                if not pathlib.Path(item).is_dir():
                    failures.append(f"dependency_read_dir_missing:{actor}")
    return failures


def _load_backend_json(stdout: str) -> dict:
    text = stdout.strip()
    if not text:
        raise ValueError("empty_backend_output")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        for line in reversed(text.splitlines()):
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                return value
        raise ValueError("backend_output_not_json")


def _reasoning_quality_failures(decision: dict, actor_id: str) -> list[str]:
    failures: list[str] = []
    quality = decision.get("reasoning_quality")
    if not isinstance(quality, dict):
        return [f"reasoning_quality_missing:{actor_id}"]
    required = [
        "task_class", "objective_model", "causal_model", "high_impact_unknowns",
        "evidence_delta", "stagnation_state", "verification_level",
        "adversarial_check", "research_stop_reason",
    ]
    for field in required:
        if quality.get(field) in (None, ""):
            failures.append(f"reasoning_quality_missing_{field}:{actor_id}")
    unknowns = quality.get("high_impact_unknowns")
    if not isinstance(unknowns, list):
        failures.append(f"reasoning_quality_unknowns_invalid:{actor_id}")
    if quality.get("verification_level") not in REASONING_LEVELS:
        failures.append(f"reasoning_quality_verification_level_invalid:{actor_id}")
    if decision.get("decision") == "PASS":
        if unknowns:
            failures.append(f"pass_has_high_impact_unknowns:{actor_id}")
        if quality.get("research_stop_reason") == "blocked":
            failures.append(f"pass_research_blocked:{actor_id}")
        if actor_id in STRONG_VERIFICATION_ACTORS and quality.get("verification_level") not in {"readback", "integration", "runtime"}:
            failures.append(f"pass_weak_verification_level:{actor_id}")
    return failures


def _normalize_decision(payload: dict, actor_id: str) -> tuple[dict | None, list[str]]:
    failures: list[str] = []
    decision = payload.get("structured_output")
    if decision is None:
        result = payload.get("result")
        if isinstance(result, dict):
            decision = result
        elif isinstance(result, str):
            try:
                decision = json.loads(result)
            except json.JSONDecodeError:
                decision = None
    if not isinstance(decision, dict):
        return None, [f"structured_decision_missing:{actor_id}"]
    if decision.get("agent_id") != actor_id:
        failures.append(f"agent_id_mismatch:{actor_id}:{decision.get('agent_id')}")
    if decision.get("decision") not in VALID_DECISIONS:
        failures.append(f"invalid_decision:{actor_id}:{decision.get('decision')}")
    if not isinstance(decision.get("summary"), str):
        failures.append(f"summary_missing:{actor_id}")
    evidence = decision.get("evidence")
    if not isinstance(evidence, list):
        failures.append(f"evidence_missing:{actor_id}")
    elif decision.get("decision") == "PASS" and not evidence:
        failures.append(f"pass_evidence_empty:{actor_id}")
    failures.extend(_reasoning_quality_failures(decision, actor_id))
    return decision, failures


def _run_actor(
    assignment: dict,
    claude_path: pathlib.Path | str,
    output_dir: pathlib.Path,
    *,
    timeout_seconds: float,
    max_budget_usd: float,
    model: str | None,
) -> dict[str, object]:
    actor = str(assignment["actor_id"])
    workspace = pathlib.Path(str(assignment["workspace"]))
    branch = str(assignment["branch"])
    execution_id = str(assignment["execution_id"])
    executor_id = str(assignment["executor_id"])
    claim_id = str(assignment["claim_id"])
    plan_head_sha = str(assignment["plan_head_sha"])
    issue_number = int(assignment["issue_number"])
    run_id = str(assignment["run_id"])
    prompt = str(assignment.get("prompt") or (
        f"You are {actor}. Inspect the repository in the current workspace. "
        "Follow AGENTS.md and the role contract. Return only the required structured decision, "
        "including reasoning_quality evidence; do not substitute elapsed time or source count for depth."
    ))
    command = build_claude_command(
        claude_path,
        actor,
        prompt,
        max_budget_usd=max_budget_usd,
        model=model,
        read_dirs=list(assignment.get("read_dirs") or []),
    )
    env = os.environ.copy()
    env["CONTROL_PLANE_ACTOR_ID"] = actor
    env["CONTROL_PLANE_EXECUTION_ID"] = execution_id
    env["CONTROL_PLANE_EXECUTOR_ID"] = executor_id
    env["CONTROL_PLANE_CLAIM_ID"] = claim_id
    spawn_monotonic_ns = time.monotonic_ns()
    process_instance_id = f"popen-{actor}-{uuid.uuid4().hex}"
    process = subprocess.Popen(
        command,
        cwd=workspace,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    pid = process.pid
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        stdout, stderr = process.communicate()
    finish_monotonic_ns = time.monotonic_ns()
    exit_code = process.returncode if process.returncode is not None else -1
    failures: list[str] = []
    if timed_out:
        failures.append(f"child_timeout:{actor}")
    if exit_code != 0:
        failures.append(f"child_exit:{actor}:{exit_code}")
    payload: dict = {}
    decision: dict | None = None
    if exit_code == 0:
        try:
            payload = _load_backend_json(stdout)
        except ValueError as exc:
            failures.append(f"{exc}:{actor}")
        if payload:
            session_id = payload.get("session_id")
            if not isinstance(session_id, str) or not session_id.strip():
                failures.append(f"missing_session_id:{actor}")
            decision, decision_failures = _normalize_decision(payload, actor)
            failures.extend(decision_failures)
    else:
        session_id = None
    row = {
        "schemaVersion": 1,
        "issue_number": issue_number,
        "run_id": run_id,
        "actor_id": actor,
        "branch": branch,
        "workspace": str(workspace),
        "dependency_read_dirs": list(assignment.get("read_dirs") or []),
        "claim_id": claim_id,
        "executor_id": executor_id,
        "execution_id": execution_id,
        "plan_head_sha": plan_head_sha,
        "pid": pid,
        "process_instance_id": process_instance_id,
        "spawn_monotonic_ns": spawn_monotonic_ns,
        "finish_monotonic_ns": finish_monotonic_ns,
        "runtime_duration_ns": max(0, finish_monotonic_ns - spawn_monotonic_ns),
        "exit_code": exit_code,
        "session_id": session_id,
        "decision": decision,
        "stdout_sha256": hashlib.sha256(stdout.encode("utf-8")).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode("utf-8")).hexdigest(),
        "failures": failures,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{actor}.json").write_text(
        json.dumps(row, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return row


def _duplicates(values: list[object]) -> bool:
    filtered = [value for value in values if value not in (None, "")]
    return len(filtered) != len(set(filtered))


def _concurrency_summary(rows: dict[str, dict], *, require_all_concurrent: bool) -> dict[str, object]:
    required_count = len(EXPECTED_ACTORS)
    observed_count = len(rows)
    starts: list[int] = []
    finishes: list[int] = []
    timing_complete = observed_count == required_count
    if timing_complete:
        for row in rows.values():
            start = row.get("spawn_monotonic_ns")
            finish = row.get("finish_monotonic_ns")
            if not isinstance(start, int) or not isinstance(finish, int) or finish <= start:
                timing_complete = False
                break
            starts.append(start)
            finishes.append(finish)
    if timing_complete:
        overlap_start = max(starts)
        overlap_end = min(finishes)
        common_overlap_ns = max(0, overlap_end - overlap_start)
    else:
        overlap_start = None
        overlap_end = None
        common_overlap_ns = 0
    common_overlap_proven = bool(
        observed_count == required_count and timing_complete and common_overlap_ns > 0
    )
    return {
        "require_all_concurrent": require_all_concurrent,
        "required_count": required_count,
        "observed_count": observed_count,
        "timing_complete": timing_complete,
        "common_overlap_start_monotonic_ns": overlap_start,
        "common_overlap_end_monotonic_ns": overlap_end,
        "common_overlap_ns": common_overlap_ns,
        "common_overlap_proven": common_overlap_proven,
    }


def execute_agents(
    assignments: list[dict],
    claude_path: pathlib.Path | str,
    output_dir: pathlib.Path | str,
    *,
    max_parallel: int = 10,
    timeout_seconds: float = 180.0,
    max_budget_usd: float = 0.05,
    model: str | None = None,
    require_all_concurrent: bool = False,
) -> dict[str, object]:
    probe = probe_claude(claude_path)
    empty_concurrency = _concurrency_summary({}, require_all_concurrent=require_all_concurrent)
    if probe.get("result") != "PASS":
        return {
            "schemaVersion": 1,
            "backend_probe": probe,
            "failures": ["backend_not_authenticated"],
            "executions": [],
            "concurrency": empty_concurrency,
            "result": "BLOCKED",
        }
    failures = _assignment_failures(assignments)
    if failures:
        return {
            "schemaVersion": 1,
            "backend_probe": probe,
            "failures": sorted(set(failures)),
            "executions": [],
            "concurrency": empty_concurrency,
            "result": "VETO",
        }
    out = pathlib.Path(output_dir)
    rows: dict[str, dict] = {}
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max(1, min(max_parallel, len(assignments)))
    ) as pool:
        future_map = {
            pool.submit(
                _run_actor,
                row,
                claude_path,
                out,
                timeout_seconds=timeout_seconds,
                max_budget_usd=max_budget_usd,
                model=model,
            ): str(row["actor_id"])
            for row in assignments
        }
        for future in concurrent.futures.as_completed(future_map):
            actor = future_map[future]
            try:
                rows[actor] = future.result()
            except Exception as exc:
                rows[actor] = {
                    "actor_id": actor,
                    "failures": [f"wrapper_exception:{type(exc).__name__}"],
                    "exit_code": -1,
                }
    aggregate_failures: list[str] = []
    for actor, row in sorted(rows.items()):
        aggregate_failures.extend(str(item) for item in row.get("failures", []))
    if any(not isinstance(row.get("pid"), int) or row.get("pid", 0) <= 0 for row in rows.values()):
        aggregate_failures.append("invalid_process_id")
    if _duplicates([row.get("process_instance_id") for row in rows.values()]):
        aggregate_failures.append("duplicate_process_instance_id")
    if _duplicates([row.get("execution_id") for row in rows.values()]):
        aggregate_failures.append("duplicate_execution_id")
    if _duplicates([row.get("session_id") for row in rows.values()]):
        aggregate_failures.append("duplicate_session_id")

    concurrency = _concurrency_summary(rows, require_all_concurrent=require_all_concurrent)
    if require_all_concurrent and not concurrency["common_overlap_proven"]:
        aggregate_failures.append("ten_way_common_overlap_missing")

    decisions = {
        actor: ((row.get("decision") or {}).get("decision"))
        for actor, row in rows.items()
    }
    if aggregate_failures:
        aggregate = "FAIL"
    elif any(value == "VETO" for value in decisions.values()):
        aggregate = "VETO"
    elif any(value == "FAIL" for value in decisions.values()):
        aggregate = "FAIL"
    elif any(value == "BLOCKED" for value in decisions.values()):
        aggregate = "BLOCKED"
    elif set(decisions.values()) == {"PASS"} and len(decisions) == 10:
        aggregate = "PASS"
    else:
        aggregate = "FAIL"
        aggregate_failures.append("incomplete_decision_set")

    result = {
        "schemaVersion": 1,
        "backend_probe": probe,
        "failures": sorted(set(aggregate_failures)),
        "executions": dict(sorted(rows.items())),
        "concurrency": concurrency,
        "result": aggregate,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "aggregate.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claude-path", required=True)
    parser.add_argument("--assignments-json")
    parser.add_argument("--output-dir")
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--max-parallel", type=int, default=10)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--max-budget-usd", type=float, default=0.05)
    parser.add_argument("--model")
    parser.add_argument("--require-all-concurrent", action="store_true")
    args = parser.parse_args(argv)

    if args.probe_only:
        result = probe_claude(args.claude_path)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["result"] == "PASS" else 1
    if not args.assignments_json or not args.output_dir:
        parser.error("--assignments-json and --output-dir are required unless --probe-only")
    assignments = json.loads(
        pathlib.Path(args.assignments_json).read_text(encoding="utf-8")
    )
    if not isinstance(assignments, list):
        raise SystemExit("assignments JSON must be an array")
    result = execute_agents(
        assignments,
        args.claude_path,
        args.output_dir,
        max_parallel=args.max_parallel,
        timeout_seconds=args.timeout_seconds,
        max_budget_usd=args.max_budget_usd,
        model=args.model,
        require_all_concurrent=args.require_all_concurrent,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
