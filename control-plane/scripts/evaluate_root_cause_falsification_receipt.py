#!/usr/bin/env python3
"""Deterministic adjudication for root-cause/falsification completion receipts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPAIR_CLASSES = {"ROOT_FIX", "MITIGATION", "GUARDRAIL", "WORKAROUND", "DEGRADATION"}
CLAIM_SCOPES = {"universal_zero_failure", "probabilistic_slo", "bounded_behavior"}


def _is_true(mapping: dict[str, Any], key: str) -> bool:
    return mapping.get(key) is True


def _reproducible_in_scope_failures(receipt: dict[str, Any]) -> list[str]:
    verification = receipt.get("verification") or {}
    failures = verification.get("failures") or []
    found: list[str] = []
    if not isinstance(failures, list):
        return ["failures_not_list"]
    for index, item in enumerate(failures):
        if not isinstance(item, dict):
            found.append(f"invalid_failure_record:{index}")
            continue
        if item.get("in_scope") is True and item.get("reproducible") is True:
            found.append(str(item.get("case_id") or f"failure-{index}"))
    return found


def _slo_failure(receipt: dict[str, Any]) -> str | None:
    if receipt.get("claim_scope") != "probabilistic_slo":
        return None
    slo = receipt.get("slo") or {}
    try:
        budget = float(slo["error_budget_rate"])
        total = int(slo["total_trials"])
        failures = int(slo["observed_failures"])
    except (KeyError, TypeError, ValueError):
        return "slo_metrics_invalid"
    if not (0 <= budget <= 1):
        return "slo_budget_invalid"
    if total <= 0 or failures < 0 or failures > total:
        return "slo_counts_invalid"
    observed = failures / total
    if observed > budget:
        return f"slo_exceeded:{observed:.12g}>{budget:.12g}"
    return None


def evaluate_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(receipt, dict):
        return {"schema_version": 1, "status": "FAIL", "reasons": ["receipt_not_object"]}

    reasons: list[str] = []
    if receipt.get("schema_version") != 1:
        reasons.append("schema_version_invalid")

    claim_scope = receipt.get("claim_scope")
    if claim_scope not in CLAIM_SCOPES:
        reasons.append("claim_scope_invalid")

    change_class = receipt.get("change_class")
    if change_class not in REPAIR_CLASSES:
        reasons.append("change_class_invalid")

    if receipt.get("goal_preserved") is not True:
        reasons.append("goal_not_preserved")

    research = receipt.get("research") or {}
    if research.get("one_search_hit_direct_to_patch") is True:
        reasons.append("one_search_hit_direct_to_patch")
    if research.get("material_external_advice_used") is True:
        if research.get("scope_version_lineage_qualified") is not True:
            reasons.append("external_advice_not_qualified")
        if research.get("discriminating_target_test_before_mutation") is not True:
            reasons.append("external_advice_not_target_tested")

    verification = receipt.get("verification") or {}
    counterexamples = _reproducible_in_scope_failures(receipt)
    invalid_failure_records = [x for x in counterexamples if x.startswith("invalid_failure_record:")]
    if invalid_failure_records:
        reasons.extend(invalid_failure_records)

    if claim_scope == "universal_zero_failure":
        real_counterexamples = [x for x in counterexamples if not x.startswith("invalid_failure_record:")]
        if real_counterexamples:
            reasons.append("universal_claim_falsified:" + ",".join(real_counterexamples))

    slo_reason = _slo_failure(receipt)
    if slo_reason:
        reasons.append(slo_reason)

    if reasons:
        return {
            "schema_version": 1,
            "status": "FAIL",
            "reasons": sorted(set(reasons)),
            "counterexamples": counterexamples,
        }

    if change_class != "ROOT_FIX":
        return {
            "schema_version": 1,
            "status": "MITIGATION_ONLY",
            "reasons": [f"change_class:{change_class}"],
            "counterexamples": counterexamples,
        }

    if receipt.get("root_mechanism_identified") is not True:
        return {
            "schema_version": 1,
            "status": "PARTIAL",
            "reasons": ["root_mechanism_not_identified"],
            "counterexamples": counterexamples,
        }

    if receipt.get("root_mechanism_changed") is not True:
        return {
            "schema_version": 1,
            "status": "ROOT_CAUSE_PROVEN",
            "reasons": ["root_mechanism_not_yet_changed"],
            "counterexamples": counterexamples,
        }

    required_verification = {
        "matrix_predeclared": "verification_matrix_not_predeclared",
        "all_in_scope_trials_counted": "in_scope_trials_not_fully_counted",
        "original_failure_replayed": "original_failure_not_replayed",
        "negative_check_passed": "negative_check_missing_or_failed",
        "regression_check_passed": "regression_check_missing_or_failed",
    }
    closure_gaps = [
        reason
        for key, reason in required_verification.items()
        if not _is_true(verification, key)
    ]
    if verification.get("original_failure_reproduces_after_fix") is True:
        closure_gaps.append("original_failure_still_reproduces")

    readback = receipt.get("readback") or {}
    if readback.get("owning_runtime_observed") is not True:
        closure_gaps.append("owning_runtime_readback_missing")

    if receipt.get("protected_capability_regressed") is True:
        closure_gaps.append("protected_capability_regressed")

    if claim_scope == "bounded_behavior" and counterexamples:
        closure_gaps.append("bounded_scope_counterexample_remains")

    if closure_gaps:
        return {
            "schema_version": 1,
            "status": "PARTIAL",
            "reasons": sorted(set(closure_gaps)),
            "counterexamples": counterexamples,
        }

    return {
        "schema_version": 1,
        "status": "ROOT_FIX_VERIFIED",
        "reasons": [],
        "counterexamples": counterexamples,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    try:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
        result = evaluate_receipt(receipt)
    except Exception as exc:
        result = {"schema_version": 1, "status": "FAIL", "reasons": [f"receipt_read_error:{exc}"]}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] in {"ROOT_FIX_VERIFIED", "ROOT_CAUSE_PROVEN", "MITIGATION_ONLY", "PARTIAL"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
