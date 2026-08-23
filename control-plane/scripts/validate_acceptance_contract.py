#!/usr/bin/env python3
"""Fail-closed validator for evidence-bound acceptance contracts.

The JSON Schema documents the interchange format. This validator enforces the
cross-field semantics that matter for completion: PASS is impossible while any
hard criterion is not SATISFIED, while a SATISFIED criterion lacks resolvable
PASS evidence, or while a blocker is underspecified.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

VALID_TASK_CLASSES = {"simple", "material", "critical"}
VALID_STATES = {"UNSATISFIED", "SATISFIED", "BLOCKED", "NOT_APPLICABLE"}
VALID_STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN"}
VALID_EVIDENCE_RESULTS = {"PASS", "FAIL", "BLOCKED"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_contract(contract: object) -> list[str]:
    failures: list[str] = []
    if not isinstance(contract, dict):
        return ["contract_not_object"]

    if contract.get("schema_version") != 1:
        failures.append("schema_version_mismatch")
    if not _nonempty(contract.get("task_id")):
        failures.append("task_id_missing")
    if contract.get("task_class") not in VALID_TASK_CLASSES:
        failures.append("task_class_invalid")
    status = contract.get("status")
    if status not in VALID_STATUSES:
        failures.append("status_invalid")

    evidence_index = contract.get("evidence_index", {})
    if not isinstance(evidence_index, dict):
        failures.append("evidence_index_invalid")
        evidence_index = {}
    else:
        for evidence_id, evidence in evidence_index.items():
            if not _nonempty(evidence_id):
                failures.append("evidence_id_empty")
                continue
            if not isinstance(evidence, dict):
                failures.append(f"evidence_invalid:{evidence_id}")
                continue
            if not _nonempty(evidence.get("kind")):
                failures.append(f"evidence_kind_missing:{evidence_id}")
            if not _nonempty(evidence.get("reference")):
                failures.append(f"evidence_reference_missing:{evidence_id}")
            if evidence.get("result") not in VALID_EVIDENCE_RESULTS:
                failures.append(f"evidence_result_invalid:{evidence_id}")

    criteria = contract.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        failures.append("criteria_missing")
        return sorted(set(failures))

    seen_ids: set[str] = set()
    hard_criteria = 0
    for index, criterion in enumerate(criteria):
        prefix = f"criterion[{index}]"
        if not isinstance(criterion, dict):
            failures.append(f"{prefix}:not_object")
            continue
        criterion_id = criterion.get("criterion_id")
        if not _nonempty(criterion_id):
            failures.append(f"{prefix}:id_missing")
            criterion_id = prefix
        elif criterion_id in seen_ids:
            failures.append(f"duplicate_criterion_id:{criterion_id}")
        else:
            seen_ids.add(criterion_id)
        if not _nonempty(criterion.get("statement")):
            failures.append(f"criterion_statement_missing:{criterion_id}")
        if not isinstance(criterion.get("hard"), bool):
            failures.append(f"criterion_hard_invalid:{criterion_id}")
        elif criterion.get("hard") is True:
            hard_criteria += 1
        if not _nonempty(criterion.get("observable_test")):
            failures.append(f"criterion_test_missing:{criterion_id}")
        state = criterion.get("state")
        if state not in VALID_STATES:
            failures.append(f"criterion_state_invalid:{criterion_id}")
        evidence_ids = criterion.get("evidence_ids")
        if not isinstance(evidence_ids, list) or any(not _nonempty(item) for item in evidence_ids):
            failures.append(f"criterion_evidence_ids_invalid:{criterion_id}")
            evidence_ids = []
        elif len(set(evidence_ids)) != len(evidence_ids):
            failures.append(f"criterion_evidence_ids_duplicate:{criterion_id}")

        if state == "BLOCKED" and not _nonempty(criterion.get("blocker")):
            failures.append(f"criterion_blocker_missing:{criterion_id}")

        if state == "SATISFIED":
            if not evidence_ids:
                failures.append(f"satisfied_without_evidence:{criterion_id}")
            for evidence_id in evidence_ids:
                evidence = evidence_index.get(evidence_id)
                if not isinstance(evidence, dict):
                    failures.append(f"evidence_unresolved:{criterion_id}:{evidence_id}")
                    continue
                if evidence.get("result") != "PASS":
                    failures.append(f"satisfied_with_nonpass_evidence:{criterion_id}:{evidence_id}")

    if status == "PASS":
        for criterion in criteria:
            if not isinstance(criterion, dict):
                continue
            if criterion.get("hard") is True and criterion.get("state") != "SATISFIED":
                failures.append(f"pass_with_unsatisfied_hard_criterion:{criterion.get('criterion_id','unknown')}")
        if hard_criteria == 0:
            failures.append("pass_without_hard_criteria")

    if status == "BLOCKED" and not _nonempty(contract.get("blocker")):
        failures.append("blocked_without_blocker")

    return sorted(set(failures))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=pathlib.Path)
    args = parser.parse_args(argv)
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL contract_read_error:{type(exc).__name__}:{exc}")
        return 1
    failures = validate_contract(contract)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("PASS evidence-bound acceptance contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
