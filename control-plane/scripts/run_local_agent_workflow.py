#!/usr/bin/env python3
"""Dependency-aware local A01-A10 workflow using trusted executor/finalizer gates."""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

try:
    from scripts.adjudicate_agent_receipts import adjudicate
    from scripts.finalize_local_agent_execution import finalize_execution
    from scripts.local_agent_executor import (
        EXPECTED_ACTORS,
        _assignment_failures,
        _run_actor,
        probe_claude,
    )
    from scripts.verify_run_freshness import verify_freshness
    from scripts.verify_snapshot_bound_execution import verify_execution
except ModuleNotFoundError:
    from adjudicate_agent_receipts import adjudicate
    from finalize_local_agent_execution import finalize_execution
    from local_agent_executor import EXPECTED_ACTORS, _assignment_failures, _run_actor, probe_claude
    from verify_run_freshness import verify_freshness
    from verify_snapshot_bound_execution import verify_execution


def _git_text(repo: pathlib.Path, *args: str) -> str | None:
    cp = subprocess.run(
        ["git", "-C", str(repo), *args], text=True,
        capture_output=True, check=False,
    )
    return cp.stdout.strip() if cp.returncode == 0 else None


def _write_json(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _dependency_failures(assignments: list[dict]) -> list[str]:
    failures: list[str] = []
    actors = {str(row.get("actor_id")) for row in assignments}
    graph: dict[str, list[str]] = {}
    for row in assignments:
        actor = str(row.get("actor_id"))
        deps = row.get("depends_on") or []
        if not isinstance(deps, list) or not all(isinstance(dep, str) for dep in deps):
            failures.append(f"invalid_dependencies:{actor}")
            deps = []
        if len(set(deps)) != len(deps):
            failures.append(f"duplicate_dependency:{actor}")
        if actor in deps:
            failures.append(f"self_dependency:{actor}")
        for dep in deps:
            if dep not in actors:
                failures.append(f"unknown_dependency:{actor}:{dep}")
        graph[actor] = list(deps)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(actor: str) -> None:
        if actor in visited or actor not in graph:
            return
        if actor in visiting:
            failures.append("dependency_cycle")
            return
        visiting.add(actor)
        for dep in graph[actor]:
            visit(dep)
        visiting.remove(actor)
        visited.add(actor)

    for actor in sorted(graph):
        visit(actor)
    return sorted(set(failures))


def _receipt_file(workspace: pathlib.Path, issue: int, run_id: str, actor: str) -> pathlib.Path:
    return workspace / (
        f"ai-system/control-plane/runs/{issue}/{run_id}/receipts/{actor}.json"
    )


def _dependency_packets(
    actor: str,
    dependencies: list[str],
    assignment_map: dict[str, dict],
    finalizations: dict[str, dict],
) -> list[dict]:
    packets: list[dict] = []
    for dep in dependencies:
        workspace = pathlib.Path(str(assignment_map[dep]["workspace"]))
        issue = int(assignment_map[dep]["issue_number"])
        run_id = str(assignment_map[dep]["run_id"])
        receipt_path = _receipt_file(workspace, issue, run_id, dep)
        receipt = {}
        if receipt_path.is_file():
            try:
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                receipt = {"error": "invalid dependency receipt"}
        packets.append({
            "actor_id": dep,
            "workspace": str(workspace),
            "final_head_sha": finalizations.get(dep, {}).get("final_head_sha"),
            "receipt": receipt,
        })
    return packets


def _enrich_assignment(
    assignment: dict,
    assignment_map: dict[str, dict],
    finalizations: dict[str, dict],
) -> dict:
    row = dict(assignment)
    actor = str(row["actor_id"])
    dependencies = list(row.get("depends_on") or [])
    packets = _dependency_packets(actor, dependencies, assignment_map, finalizations)
    base_prompt = str(row.get("prompt") or "")
    if packets:
        base_prompt += (
            "\nTrusted finalized dependency receipts/summaries follow. "
            "Treat them as read-only evidence:\n" +
            json.dumps(packets, ensure_ascii=False, sort_keys=True)
        )
    row["prompt"] = base_prompt
    if actor == "A07":
        row["read_dirs"] = []
    else:
        row["read_dirs"] = [
            str(pathlib.Path(str(assignment_map[dep]["workspace"])).resolve())
            for dep in dependencies
        ]
    return row


def _seed_existing_receipts(
    preparation: dict,
    assignment_map: dict[str, dict],
    snapshots: dict[str, dict],
) -> tuple[dict[str, str], dict[str, dict], list[str], list[str], list[str]]:
    statuses: dict[str, str] = {}
    finalizations: dict[str, dict] = {}
    resumed: list[str] = []
    failures: list[str] = []
    terminal_vetoes: list[str] = []
    issue = int(preparation["issue_number"])
    run_id = str(preparation["run_id"])
    for actor in EXPECTED_ACTORS:
        assignment = assignment_map[actor]
        workspace = pathlib.Path(str(assignment["workspace"]))
        receipt_path = _receipt_file(workspace, issue, run_id, actor)
        if not receipt_path.is_file():
            continue
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except Exception:
            failures.append(f"existing_receipt_invalid_json:{actor}")
            continue
        current_head = _git_text(workspace, "rev-parse", "HEAD") or ""
        snapshot_result = verify_execution(
            workspace, issue, run_id, actor, snapshots[actor], current_head
        )
        receipt_check = adjudicate(receipt_path.parent, issue, run_id)
        if snapshot_result.get("result") != "PASS":
            failures.append(f"existing_receipt_snapshot_invalid:{actor}")
            continue
        if receipt_check.get("errors") or receipt_check.get("direct_failures"):
            failures.append(f"existing_receipt_attestation_invalid:{actor}")
            continue
        result = str(receipt.get("result", ""))
        if result not in {"PASS", "VETO"}:
            failures.append(f"existing_receipt_not_reusable:{actor}:{result}")
            continue
        statuses[actor] = result
        finalizations[actor] = {
            "schemaVersion": 1,
            "actor_id": actor,
            "work_head_sha": receipt.get("head_sha"),
            "final_head_sha": current_head,
            "receipt_path": str(receipt_path.relative_to(workspace)),
            "snapshot_verification": snapshot_result,
            "failures": [],
            "result": result,
            "resumed_from_existing_receipt": True,
        }
        resumed.append(actor)
        if result == "VETO":
            terminal_vetoes.append(actor)
    return statuses, finalizations, resumed, failures, terminal_vetoes


def run_workflow(
    preparation: dict,
    claude_path: pathlib.Path | str,
    output_dir: pathlib.Path | str,
    *,
    max_parallel: int = 3,
    timeout_seconds: float = 180.0,
    max_budget_usd: float = 0.05,
    model: str | None = None,
    resume_existing: bool = False,
) -> dict[str, object]:
    output_dir = pathlib.Path(output_dir)
    failures: list[str] = []
    if preparation.get("result") != "PASS":
        return {
            "schemaVersion": 1,
            "failures": ["preparation_not_pass"],
            "executions": {},
            "waves": [],
            "result": "VETO",
        }
    assignments = preparation.get("assignments") or []
    snapshots = preparation.get("snapshots") or {}
    if not isinstance(assignments, list):
        assignments = []
        failures.append("assignments_not_array")
    failures.extend(_assignment_failures(assignments))
    failures.extend(_dependency_failures(assignments))
    if set(snapshots) != set(EXPECTED_ACTORS):
        failures.append("snapshot_actor_set_mismatch")
    source_repo = pathlib.Path(str(preparation.get("source_repo", "")))
    if not source_repo.is_dir() or _git_text(source_repo, "rev-parse", "HEAD") is None:
        failures.append("source_repo_unavailable")
    if failures:
        return {
            "schemaVersion": 1,
            "failures": sorted(set(failures)),
            "executions": {},
            "waves": [],
            "result": "VETO",
        }

    assignment_map = {str(row["actor_id"]): row for row in assignments}
    dependency_map = {
        actor: list(assignment_map[actor].get("depends_on") or [])
        for actor in EXPECTED_ACTORS
    }
    statuses: dict[str, str] = {}
    executions: dict[str, dict] = {}
    finalizations: dict[str, dict] = {}
    resumed_actors: list[str] = []
    blocked_dependencies: dict[str, list[str]] = {}
    waves: list[list[str]] = []
    seen_process_instances: set[str] = set()
    seen_session_hashes: set[str] = set()
    executor_output = output_dir / "executor"
    finalizer_output = output_dir / "finalizations"
    global_failures: list[str] = []

    if resume_existing:
        statuses, finalizations, resumed_actors, resume_failures, terminal_vetoes = _seed_existing_receipts(
            preparation, assignment_map, snapshots
        )
        for actor in resumed_actors:
            if statuses.get(actor) == "PASS":
                missing_pass_dependencies = [
                    dep for dep in dependency_map[actor] if statuses.get(dep) != "PASS"
                ]
                if missing_pass_dependencies:
                    resume_failures.append(f"resumed_dependency_not_pass:{actor}")
            receipt_path = _receipt_file(
                pathlib.Path(str(assignment_map[actor]["workspace"])),
                int(preparation["issue_number"]), str(preparation["run_id"]), actor,
            )
            try:
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            attestation = receipt.get("runtime_attestation") or {}
            process_instance = str(attestation.get("process_instance_id", ""))
            session_hash = str(attestation.get("backend_session_sha256", ""))
            if process_instance:
                seen_process_instances.add(process_instance)
            if session_hash:
                seen_session_hashes.add(session_hash)
        if resume_failures:
            result = {
                "schemaVersion": 1,
                "backend_probe": {"result": "NOT_RUN"},
                "failures": sorted(set(resume_failures)),
                "executions": {},
                "finalizations": finalizations,
                "resumed_actors": sorted(resumed_actors),
                "statuses": statuses,
                "blocked_dependencies": {},
                "waves": [],
                "adjudication": {"result": "NOT_RUN"},
                "base_freshness": {"result": "NOT_RUN"},
                "result": "FAIL",
            }
            _write_json(output_dir / "workflow.json", result)
            return result
        if terminal_vetoes:
            result = {
                "schemaVersion": 1,
                "backend_probe": {"result": "NOT_RUN"},
                "failures": [f"existing_veto_receipt:{actor}" for actor in sorted(terminal_vetoes)],
                "executions": {},
                "finalizations": finalizations,
                "resumed_actors": sorted(resumed_actors),
                "statuses": statuses,
                "blocked_dependencies": {},
                "waves": [],
                "adjudication": {"result": "NOT_RUN"},
                "base_freshness": {"result": "NOT_RUN"},
                "result": "VETO",
            }
            _write_json(output_dir / "workflow.json", result)
            return result

    pending = set(EXPECTED_ACTORS) - set(resumed_actors)
    if pending:
        probe = probe_claude(claude_path)
        if probe.get("result") != "PASS":
            result = {
                "schemaVersion": 1,
                "backend_probe": probe,
                "failures": ["backend_not_authenticated"],
                "executions": {},
                "finalizations": finalizations,
                "resumed_actors": sorted(resumed_actors),
                "statuses": statuses,
                "blocked_dependencies": {},
                "waves": [],
                "adjudication": {"result": "NOT_RUN"},
                "base_freshness": {"result": "NOT_RUN"},
                "result": "BLOCKED",
            }
            _write_json(output_dir / "workflow.json", result)
            return result
    else:
        probe = {"result": "NOT_RUN", "reason": "all_actors_resumed"}

    while pending:
        blocked_now: list[str] = []
        for actor in sorted(pending):
            bad = [
                dep for dep in dependency_map[actor]
                if dep in statuses and statuses[dep] != "PASS"
            ]
            if bad:
                statuses[actor] = "BLOCKED"
                blocked_dependencies[actor] = bad
                blocked_now.append(actor)
        for actor in blocked_now:
            pending.remove(actor)
        if not pending:
            break

        ready = [
            actor for actor in EXPECTED_ACTORS
            if actor in pending and all(statuses.get(dep) == "PASS" for dep in dependency_map[actor])
        ]
        if not ready:
            global_failures.append("dependency_deadlock")
            for actor in sorted(pending):
                statuses[actor] = "FAIL"
            pending.clear()
            break
        wave = ready
        waves.append(list(wave))
        enriched = {
            actor: _enrich_assignment(
                assignment_map[actor], assignment_map, finalizations
            )
            for actor in wave
        }
        for actor, row in enriched.items():
            if actor == "A07" and row.get("read_dirs"):
                global_failures.append("A07_external_dependency_dirs")
            for directory in row.get("read_dirs") or []:
                if not pathlib.Path(directory).is_dir():
                    global_failures.append(f"dependency_read_dir_missing:{actor}")

        wave_rows: dict[str, dict] = {}
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=max(1, min(max_parallel, len(wave)))
        ) as pool:
            future_map = {
                pool.submit(
                    _run_actor,
                    enriched[actor],
                    claude_path,
                    executor_output,
                    timeout_seconds=timeout_seconds,
                    max_budget_usd=max_budget_usd,
                    model=model,
                ): actor
                for actor in wave
            }
            for future in concurrent.futures.as_completed(future_map):
                actor = future_map[future]
                try:
                    wave_rows[actor] = future.result()
                except Exception as exc:
                    wave_rows[actor] = {
                        "actor_id": actor,
                        "exit_code": -1,
                        "failures": [f"wrapper_exception:{type(exc).__name__}"],
                    }

        wave_instance_ids = [
            str(row.get("process_instance_id", ""))
            for row in wave_rows.values()
            if row.get("process_instance_id")
        ]
        wave_session_hashes = [
            hashlib.sha256(str(row.get("session_id", "")).encode("utf-8")).hexdigest()
            for row in wave_rows.values()
            if row.get("session_id")
        ]
        duplicate_wave_instances = {
            value for value in wave_instance_ids if wave_instance_ids.count(value) > 1
        }
        duplicate_wave_sessions = {
            value for value in wave_session_hashes if wave_session_hashes.count(value) > 1
        }

        for actor in wave:
            row = wave_rows[actor]
            executions[actor] = row
            row_failures = list(row.get("failures") or [])
            instance_id = str(row.get("process_instance_id", ""))
            session_id = str(row.get("session_id", ""))
            session_hash = hashlib.sha256(session_id.encode("utf-8")).hexdigest() if session_id else ""
            if not instance_id:
                row_failures.append(f"process_instance_missing:{actor}")
            elif instance_id in seen_process_instances or instance_id in duplicate_wave_instances:
                row_failures.append(f"duplicate_process_instance:{actor}")
            if not session_id:
                row_failures.append(f"backend_session_missing:{actor}")
            elif session_hash in seen_session_hashes or session_hash in duplicate_wave_sessions:
                row_failures.append(f"duplicate_backend_session:{actor}")
            if not isinstance(row.get("pid"), int) or row.get("pid", 0) <= 0:
                row_failures.append(f"process_id_invalid:{actor}")
            if instance_id:
                seen_process_instances.add(instance_id)
            if session_hash:
                seen_session_hashes.add(session_hash)
            if row_failures:
                row["failures"] = sorted(set(row_failures))
                statuses[actor] = "FAIL"
                global_failures.extend(row["failures"])
                continue

            finalization = finalize_execution(
                pathlib.Path(str(assignment_map[actor]["workspace"])),
                actor,
                snapshots[actor],
                row,
            )
            finalizations[actor] = finalization
            _write_json(finalizer_output / f"{actor}.json", finalization)
            statuses[actor] = str(finalization.get("result", "FAIL"))
            if statuses[actor] == "FAIL":
                global_failures.extend(
                    f"finalizer:{actor}:{item}"
                    for item in finalization.get("failures", [])
                )

        for actor in wave:
            pending.remove(actor)

    adjudication: dict[str, object] = {"result": "NOT_RUN"}
    base_freshness: dict[str, object] = {"result": "NOT_RUN"}

    if any(status == "FAIL" for status in statuses.values()) or global_failures:
        aggregate = "FAIL"
    elif any(status == "VETO" for status in statuses.values()):
        aggregate = "VETO"
    elif any(status == "BLOCKED" for status in statuses.values()):
        aggregate = "BLOCKED"
    elif set(statuses) == set(EXPECTED_ACTORS) and all(
        statuses[actor] == "PASS" for actor in EXPECTED_ACTORS
    ):
        receipt_dir = output_dir / "receipts"
        receipt_dir.mkdir(parents=True, exist_ok=True)
        receipt_collection_failures: list[str] = []
        for actor in EXPECTED_ACTORS:
            workspace = pathlib.Path(str(assignment_map[actor]["workspace"]))
            expected_head = str(finalizations[actor].get("final_head_sha", ""))
            current_head = _git_text(workspace, "rev-parse", "HEAD")
            if current_head != expected_head:
                receipt_collection_failures.append(f"finalized_head_drift:{actor}")
                continue
            receipt_rel = str(finalizations[actor].get("receipt_path", ""))
            receipt_source = workspace / receipt_rel
            if not receipt_rel or not receipt_source.is_file():
                receipt_collection_failures.append(f"receipt_missing:{actor}")
                continue
            shutil.copy2(receipt_source, receipt_dir / f"{actor}.json")
        if receipt_collection_failures:
            global_failures.extend(receipt_collection_failures)
            aggregate = "FAIL"
        else:
            issue = int(preparation["issue_number"])
            run_id = str(preparation["run_id"])
            adjudication = adjudicate(receipt_dir, issue, run_id)
            _write_json(output_dir / "adjudication.json", adjudication)
            if adjudication.get("result") != "PASS":
                aggregate = str(adjudication.get("result", "FAIL"))
            else:
                base_ref = str(preparation.get("base_ref", ""))
                current_base = _git_text(
                    source_repo, "rev-parse", "--verify", f"{base_ref}^{{commit}}"
                ) or ""
                base_freshness = verify_freshness(
                    str(preparation.get("base_sha", "")), current_base
                )
                _write_json(output_dir / "base-freshness.json", base_freshness)
                aggregate = "PASS" if base_freshness.get("result") == "PASS" else "VETO"
    else:
        aggregate = "FAIL"
        global_failures.append("incomplete_status_set")

    result = {
        "schemaVersion": 1,
        "backend_probe": probe,
        "issue_number": preparation.get("issue_number"),
        "run_id": preparation.get("run_id"),
        "waves": waves,
        "resumed_actors": sorted(resumed_actors),
        "statuses": dict(sorted(statuses.items())),
        "blocked_dependencies": dict(sorted(blocked_dependencies.items())),
        "model_process_count": len(executions),
        "process_instance_count": len({
            str(row.get("process_instance_id"))
            for row in executions.values() if row.get("process_instance_id")
        }),
        "executions": dict(sorted(executions.items())),
        "finalizations": dict(sorted(finalizations.items())),
        "adjudication": adjudication,
        "base_freshness": base_freshness,
        "failures": sorted(set(global_failures)),
        "result": aggregate,
    }
    _write_json(output_dir / "workflow.json", result)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preparation-json", required=True)
    parser.add_argument("--claude-path", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-parallel", type=int, default=3)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--max-budget-usd", type=float, default=0.05)
    parser.add_argument("--model")
    parser.add_argument("--resume-existing", action="store_true")
    args = parser.parse_args(argv)
    preparation = json.loads(
        pathlib.Path(args.preparation_json).read_text(encoding="utf-8")
    )
    result = run_workflow(
        preparation,
        args.claude_path,
        args.output_dir,
        max_parallel=args.max_parallel,
        timeout_seconds=args.timeout_seconds,
        max_budget_usd=args.max_budget_usd,
        model=args.model,
        resume_existing=args.resume_existing,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
