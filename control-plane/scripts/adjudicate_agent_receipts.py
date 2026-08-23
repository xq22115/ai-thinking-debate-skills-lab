#!/usr/bin/env python3
"""Fail-closed adjudication of ten independent agent execution receipts.

This does not prove that an executor ID corresponds to a physically independent
model/process. It enforces the repository contract: exactly A01-A10, zero VETO,
zero missing/non-PASS receipts, distinct executor/execution/evidence partitions,
no direct failing evidence inside a PASS receipt, and machine-checkable reasoning
quality with no unresolved high-impact unknowns on PASS.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import Counter

EXPECTED = {
    "A01": "編排代理",
    "A02": "主張代理",
    "A03": "原始來源研究代理",
    "A04": "根因分析代理",
    "A05": "反方代理",
    "A06": "交叉詰問代理",
    "A07": "實作代理",
    "A08": "驗證代理",
    "A09": "風險代理",
    "A10": "裁決代理",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
VALID_RESULTS = {"PASS", "VETO", "FAIL", "BLOCKED", "NOT_RUN"}
VALID_VERIFICATION_LEVELS = {"source", "inspection", "static", "readback", "integration", "runtime"}
STRONG_VERIFICATION_ACTORS = {"A08", "A10"}


def _duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if value and count > 1)


def _load_receipts(receipt_dir: pathlib.Path) -> tuple[dict[str, dict], list[str]]:
    records: dict[str, dict] = {}
    errors: list[str] = []
    if not receipt_dir.is_dir():
        return records, [f"receipt_directory_missing:{receipt_dir}"]
    for path in sorted(receipt_dir.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid_json:{path.name}:{exc}")
            continue
        agent_id = record.get("agent_id")
        if agent_id not in EXPECTED:
            errors.append(f"unexpected_agent_id:{path.name}:{agent_id}")
            continue
        if agent_id in records:
            errors.append(f"duplicate_agent_receipt:{agent_id}")
            continue
        record["_file"] = path.name
        records[agent_id] = record
    return records, errors


def _validate_reasoning_quality(agent_id: str, result: object, quality: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(quality, dict):
        return [f"missing_reasoning_quality:{agent_id}"]
    required = [
        "task_class", "objective_model", "causal_model", "high_impact_unknowns",
        "evidence_delta", "stagnation_state", "verification_level",
        "adversarial_check", "research_stop_reason",
    ]
    for field in required:
        if quality.get(field) in (None, ""):
            errors.append(f"reasoning_quality_missing_{field}:{agent_id}")
    unknowns = quality.get("high_impact_unknowns")
    if not isinstance(unknowns, list):
        errors.append(f"reasoning_quality_unknowns_invalid:{agent_id}")
        unknowns = []
    verification_level = quality.get("verification_level")
    if verification_level not in VALID_VERIFICATION_LEVELS:
        errors.append(f"reasoning_quality_verification_level_invalid:{agent_id}")
    if result == "PASS":
        if unknowns:
            errors.append(f"pass_has_high_impact_unknowns:{agent_id}")
        if quality.get("research_stop_reason") == "blocked":
            errors.append(f"pass_research_blocked:{agent_id}")
        if agent_id in STRONG_VERIFICATION_ACTORS and verification_level not in {"readback", "integration", "runtime"}:
            errors.append(f"pass_weak_verification_level:{agent_id}")
    return errors


def adjudicate(receipt_dir: pathlib.Path, issue_number: int | None = None, run_id: str | None = None) -> dict[str, object]:
    records, errors = _load_receipts(receipt_dir)
    expected_ids = list(EXPECTED)
    missing = [agent_id for agent_id in expected_ids if agent_id not in records]
    statuses: dict[str, str] = {}
    vetoes: list[dict[str, str]] = []
    direct_failures: list[str] = []

    for agent_id, record in sorted(records.items()):
        result = record.get("result")
        statuses[agent_id] = str(result)
        schema_version = record.get("schema_version")
        if schema_version not in {1, 2, 3}:
            errors.append(f"schema_version:{agent_id}:{schema_version}")
        if record.get("role") != EXPECTED[agent_id]:
            errors.append(f"role_mismatch:{agent_id}")
        if result not in VALID_RESULTS:
            errors.append(f"invalid_result:{agent_id}:{result}")
        if issue_number is not None and record.get("issue_number") != issue_number:
            errors.append(f"issue_mismatch:{agent_id}")
        if run_id is not None and record.get("run_id") != run_id:
            errors.append(f"run_id_mismatch:{agent_id}")
        branch = str(record.get("branch", ""))
        if f"/{agent_id}/" not in branch:
            errors.append(f"branch_not_agent_scoped:{agent_id}")
        if result == "VETO":
            vetoes.append({"agent_id": agent_id, "reason": str(record.get("veto_reason", "missing veto reason"))})
        if result in {"PASS", "VETO"}:
            if schema_version != 3:
                errors.append(f"pass_veto_requires_schema_v3:{agent_id}")
            if record.get("independent_agent_execution") is not True:
                errors.append(f"independence_not_asserted:{agent_id}")
            for field in ["claim_id", "executor_id", "execution_id", "evidence_partition"]:
                if not str(record.get(field, "")).strip():
                    errors.append(f"missing_{field}:{agent_id}")
            errors.extend(_validate_reasoning_quality(agent_id, result, record.get("reasoning_quality")))
            attestation = record.get("runtime_attestation")
            if not isinstance(attestation, dict):
                errors.append(f"missing_runtime_attestation:{agent_id}")
            else:
                required_attestation = [
                    "provider", "observer", "process_instance_id", "process_id",
                    "spawn_monotonic_ns", "backend_session_sha256",
                    "stdout_sha256", "stderr_sha256",
                ]
                for field in required_attestation:
                    if attestation.get(field) in (None, ""):
                        errors.append(f"runtime_attestation_missing_{field}:{agent_id}")
                if not isinstance(attestation.get("process_id"), int) or attestation.get("process_id", 0) <= 0:
                    errors.append(f"runtime_attestation_invalid_process_id:{agent_id}")
                if not isinstance(attestation.get("spawn_monotonic_ns"), int) or attestation.get("spawn_monotonic_ns", 0) <= 0:
                    errors.append(f"runtime_attestation_invalid_spawn:{agent_id}")
                for field in ["backend_session_sha256", "stdout_sha256", "stderr_sha256"]:
                    if not re.fullmatch(r"[0-9a-f]{64}", str(attestation.get(field, ""))):
                        errors.append(f"runtime_attestation_invalid_{field}:{agent_id}")
            if not SHA40.match(str(record.get("plan_head_sha", ""))):
                errors.append(f"invalid_plan_head_sha:{agent_id}")
            if not SHA40.match(str(record.get("head_sha", ""))):
                errors.append(f"invalid_head_sha:{agent_id}")
            evidence = record.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"missing_evidence:{agent_id}")
            else:
                for index, item in enumerate(evidence):
                    if not isinstance(item, dict) or not item.get("reference"):
                        errors.append(f"invalid_evidence:{agent_id}:{index}")
                        continue
                    if item.get("result") in {"FAIL", "BLOCKED"}:
                        direct_failures.append(f"{agent_id}:{index}:{item.get('result')}")
        if result == "NOT_RUN" and record.get("independent_agent_execution") is not False:
            errors.append(f"not_run_must_be_nonexecution:{agent_id}")

    pass_records = [records[agent_id] for agent_id in expected_ids if statuses.get(agent_id) == "PASS"]
    if len(pass_records) == 10:
        duplicate_executors = _duplicates([str(r.get("executor_id", "")) for r in pass_records])
        duplicate_executions = _duplicates([str(r.get("execution_id", "")) for r in pass_records])
        duplicate_partitions = _duplicates([str(r.get("evidence_partition", "")) for r in pass_records])
        duplicate_branches = _duplicates([str(r.get("branch", "")) for r in pass_records])
        duplicate_process_instances = _duplicates([
            str((r.get("runtime_attestation") or {}).get("process_instance_id", "")) for r in pass_records
        ])
        duplicate_backend_sessions = _duplicates([
            str((r.get("runtime_attestation") or {}).get("backend_session_sha256", "")) for r in pass_records
        ])
    else:
        duplicate_executors = []
        duplicate_executions = []
        duplicate_partitions = []
        duplicate_branches = []
        duplicate_process_instances = []
        duplicate_backend_sessions = []

    if duplicate_executors:
        errors.append(f"duplicate_executor_id:{duplicate_executors}")
    if duplicate_executions:
        errors.append(f"duplicate_execution_id:{duplicate_executions}")
    if duplicate_partitions:
        errors.append(f"duplicate_evidence_partition:{duplicate_partitions}")
    if duplicate_branches:
        errors.append(f"duplicate_branch:{duplicate_branches}")
    if duplicate_process_instances:
        errors.append(f"duplicate_process_instance:{duplicate_process_instances}")
    if duplicate_backend_sessions:
        errors.append(f"duplicate_backend_session:{duplicate_backend_sessions}")

    if errors or direct_failures:
        aggregate = "FAIL"
    elif vetoes:
        aggregate = "VETO"
    elif missing:
        aggregate = "BLOCKED"
    elif any(statuses.get(agent_id) != "PASS" for agent_id in expected_ids):
        aggregate = "BLOCKED"
    else:
        aggregate = "PASS"

    return {
        "schemaVersion": 3,
        "receipt_directory": str(receipt_dir),
        "expected_agents": expected_ids,
        "found_agents": sorted(records),
        "statuses": statuses,
        "missing_agents": missing,
        "vetoes": vetoes,
        "direct_failures": direct_failures,
        "duplicate_executor_ids": duplicate_executors,
        "duplicate_execution_ids": duplicate_executions,
        "duplicate_evidence_partitions": duplicate_partitions,
        "duplicate_branches": duplicate_branches,
        "duplicate_process_instances": duplicate_process_instances,
        "duplicate_backend_sessions": duplicate_backend_sessions,
        "errors": errors,
        "result": aggregate,
        "independence_note": "PASS/VETO receipts carry wrapper-observed runtime attestations plus machine-checkable reasoning-quality evidence. Distinct process-instance and backend-session hashes make runtime evidence durable across chats; this remains evidence from the trusted wrapper rather than cryptographic proof of model internals."
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt_dir")
    parser.add_argument("--issue", type=int)
    parser.add_argument("--run-id")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    receipt = adjudicate(pathlib.Path(args.receipt_dir), args.issue, args.run_id)
    text = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0 if receipt["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
