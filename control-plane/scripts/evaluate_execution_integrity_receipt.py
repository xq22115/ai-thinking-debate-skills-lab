#!/usr/bin/env python3
"""Fail-closed adjudication of GitHub execution-integrity receipts.

The repository-wide policy can name adversarial scenarios, but names alone are
not evidence. This evaluator requires executed scenario records with evidence
and applies family-specific assertions plus GI-01..GI-12 invariants.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

SHA40 = re.compile(r"^[0-9a-f]{40}$")

SUPPORTED_SCENARIOS = {
    "normal_valid_input",
    "invalid_input",
    "empty_or_missing_input",
    "idempotent_repeat",
    "rapid_consecutive_operations",
    "reordered_operations",
    "permission_loss_or_scope_reduction",
    "network_interruption_timeout_retry",
    "dependency_unavailable_or_version_mismatch",
    "stale_cache_state_or_old_installation_residue",
    "partial_success_then_failure",
    "stale_search_index_vs_direct_lookup",
    "exact_revision_mismatch",
    "rollback_and_recovery",
}

DISTINCT_FALLBACKS = {
    "exact_repository_lookup",
    "direct_file_fetch",
    "code_search",
    "tree_or_contents_lookup",
    "known_url_or_ref_resolution",
}

STRONG_EVIDENCE_FAMILIES = {
    "target_runtime_or_owning_installation_readback",
    "exact_github_object_and_revision_metadata",
    "source_repository_files_commits_manifests_releases_workflows",
    "maintainer_discussions_or_implementation_source",
    "high_signal_third_party_practitioner_or_tooling_evidence",
}

SCENARIO_GI_MAP = {
    "normal_valid_input": "GI-11",
    "invalid_input": "GI-04",
    "empty_or_missing_input": "GI-04",
    "idempotent_repeat": "GI-03",
    "rapid_consecutive_operations": "GI-06",
    "reordered_operations": "GI-06",
    "permission_loss_or_scope_reduction": "GI-02",
    "network_interruption_timeout_retry": "GI-04",
    "dependency_unavailable_or_version_mismatch": "GI-04",
    "stale_cache_state_or_old_installation_residue": "GI-08",
    "partial_success_then_failure": "GI-04",
    "stale_search_index_vs_direct_lookup": "GI-09",
    "exact_revision_mismatch": "GI-08",
    "rollback_and_recovery": "GI-07",
}

REQUIRED_SCENARIO_FIELDS = {
    "family",
    "executed",
    "precondition",
    "action",
    "expected_result",
    "actual_result",
    "evidence",
    "invariant_violations",
    "observations",
}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _scenario_failures(record: dict) -> list[str]:
    family = record.get("family")
    failures: list[str] = []
    missing = sorted(REQUIRED_SCENARIO_FIELDS - set(record))
    if missing:
        return [f"missing_fields:{','.join(missing)}"]

    if family not in SUPPORTED_SCENARIOS:
        return ["unsupported_family"]
    if record.get("executed") is not True:
        failures.append("not_executed")
    for field in ("precondition", "action", "expected_result", "actual_result"):
        if not _nonempty(record.get(field)):
            failures.append(f"{field}_missing")
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(_nonempty(item) for item in evidence):
        failures.append("evidence_missing")
    claimed_violations = record.get("invariant_violations")
    if not isinstance(claimed_violations, list):
        failures.append("invariant_violations_invalid")
    elif claimed_violations:
        failures.append("scenario_reports_invariant_violation")

    obs = record.get("observations")
    if not isinstance(obs, dict):
        return failures + ["observations_invalid"]

    def require_true(key: str) -> None:
        if obs.get(key) is not True:
            failures.append(f"{key}_not_true")

    def require_false(key: str) -> None:
        if obs.get(key) is not False:
            failures.append(f"{key}_not_false")

    if family == "normal_valid_input":
        require_true("behavior_matches_expected")
        if record.get("actual_result") != record.get("expected_result"):
            failures.append("result_mismatch")
    elif family in {"invalid_input", "empty_or_missing_input"}:
        require_true("rejected")
        require_true("failure_detected")
        require_false("state_changed")
    elif family == "idempotent_repeat":
        require_false("duplicate_side_effects")
        if obs.get("state_after_first") != obs.get("state_after_second"):
            failures.append("repeat_changed_final_state")
    elif family == "rapid_consecutive_operations":
        if not isinstance(obs.get("operations_observed"), int) or obs.get("operations_observed", 0) < 2:
            failures.append("insufficient_consecutive_operations")
        require_false("lost_update")
        require_true("final_state_consistent")
    elif family == "reordered_operations":
        require_true("out_of_order_detected")
        require_false("state_corrupted")
    elif family == "permission_loss_or_scope_reduction":
        require_true("permission_loss_detected")
        require_false("unauthorized_write")
    elif family == "network_interruption_timeout_retry":
        require_true("interruption_detected")
        recovered = obs.get("recovered")
        if recovered is True:
            require_true("retry_performed")
            require_true("final_readback_matches")
        elif recovered is False:
            require_true("terminal_failure_detected")
            require_false("reported_success")
        else:
            failures.append("recovered_status_missing")
    elif family == "dependency_unavailable_or_version_mismatch":
        require_true("dependency_problem_detected")
        recovered = obs.get("recovered_with_verified_compatible_dependency")
        if recovered is True:
            require_true("final_readback_matches")
        elif recovered is False:
            require_true("operation_blocked")
            require_false("reported_success")
        else:
            failures.append("dependency_recovery_status_missing")
    elif family == "stale_cache_state_or_old_installation_residue":
        require_true("stale_state_detected")
        require_false("stale_state_accepted")
    elif family == "partial_success_then_failure":
        require_true("partial_failure_detected")
        require_false("reported_success")
    elif family == "stale_search_index_vs_direct_lookup":
        require_true("search_miss_observed")
        fallback = obs.get("fallback_mechanism")
        if fallback not in DISTINCT_FALLBACKS:
            failures.append("distinct_fallback_missing")
        if obs.get("fallback_outcome") not in {"found", "confirmed_absent"}:
            failures.append("fallback_outcome_invalid")
    elif family == "exact_revision_mismatch":
        require_true("revision_mismatch_detected")
        require_false("mismatched_state_accepted")
    elif family == "rollback_and_recovery":
        require_true("rollback_target_recorded")
        require_true("rollback_performed")
        require_true("recovery_readback_matches")

    return sorted(set(failures))


def evaluate_receipt(receipt: dict) -> dict[str, object]:
    failures: list[str] = []
    invariants: set[str] = set()
    scenario_failures: dict[str, list[str]] = {}

    if not isinstance(receipt, dict):
        return {
            "schemaVersion": 1,
            "result": "FAIL",
            "failures": ["receipt_not_object"],
            "invariant_violations": [],
            "scenario_failures": {},
        }
    if receipt.get("schema_version") != 1:
        failures.append("schema_version_invalid")
    if not _nonempty(receipt.get("operation_id")):
        failures.append("operation_id_missing")

    material = receipt.get("material_change") is True
    target = receipt.get("target_identity")
    if not isinstance(target, dict) or not _nonempty(target.get("repository")) or not _nonempty(target.get("branch")):
        failures.append("target_identity_incomplete")

    base = str(receipt.get("base_revision", ""))
    reported = str(receipt.get("reported_revision", ""))
    if not SHA40.fullmatch(base):
        failures.append("base_revision_invalid")
        invariants.add("GI-07")
    if not SHA40.fullmatch(reported):
        failures.append("reported_revision_invalid")
        invariants.add("GI-08")

    capabilities = receipt.get("protected_capabilities")
    if material:
        if not isinstance(capabilities, dict):
            failures.append("protected_capabilities_missing")
            invariants.add("GI-01")
        else:
            before = set(capabilities.get("before") or [])
            after = set(capabilities.get("after") or [])
            if not before or not before.issubset(after):
                failures.append("existing_capability_regressed")
                invariants.add("GI-01")

    permissions = receipt.get("permissions")
    if material:
        if not isinstance(permissions, dict) or permissions.get("verified") is not True:
            failures.append("permission_readback_missing")
            invariants.add("GI-02")
        else:
            before = set(permissions.get("before") or [])
            after = set(permissions.get("after") or [])
            if not before or not before.issubset(after):
                failures.append("permission_downgrade_detected")
                invariants.add("GI-02")

    contract = receipt.get("io_contract")
    if material:
        if not isinstance(contract, dict):
            failures.append("io_contract_missing")
            invariants.add("GI-03")
        else:
            before = contract.get("before")
            after = contract.get("after")
            migration = contract.get("migration_accepted") is True
            if not _nonempty(before) or not _nonempty(after):
                failures.append("io_contract_identity_missing")
                invariants.add("GI-03")
            elif before != after and not migration:
                failures.append("io_contract_changed_without_migration")
                invariants.add("GI-03")

    operation = receipt.get("operation")
    operation_result = None
    if not isinstance(operation, dict):
        failures.append("operation_record_missing")
        invariants.add("GI-04")
    else:
        operation_result = operation.get("result")
        if operation.get("attempted") is not True:
            failures.append("operation_not_attempted")
        if operation_result not in {"success", "failure", "blocked", "not_run"}:
            failures.append("operation_result_invalid")
        if operation.get("partial_success") is True and operation.get("failure_detected") is not True:
            failures.append("partial_success_failure_not_detected")
            invariants.add("GI-04")
        if operation_result in {"failure", "blocked"} and operation.get("failure_detected") is not True:
            failures.append("terminal_failure_not_detected")
            invariants.add("GI-04")

    readback = receipt.get("readback")
    if material and operation_result == "success":
        if not isinstance(readback, dict) or readback.get("performed") is not True:
            failures.append("success_without_readback")
            invariants.add("GI-05")
        else:
            if readback.get("matches_intended") is not True:
                failures.append("readback_mismatch")
                invariants.add("GI-05")
            if readback.get("revision") != reported:
                failures.append("readback_revision_mismatch")
                invariants.add("GI-08")

    regression = receipt.get("adjacent_regression")
    if material and operation_result == "success":
        if not isinstance(regression, dict) or regression.get("performed") is not True:
            failures.append("adjacent_regression_not_run")
            invariants.add("GI-06")
        elif regression.get("passed") is not True:
            failures.append("adjacent_regression_failed")
            invariants.add("GI-06")

    rollback = receipt.get("rollback")
    if material:
        if not isinstance(rollback, dict):
            failures.append("rollback_record_missing")
            invariants.add("GI-07")
        else:
            if rollback.get("target_revision") != base or rollback.get("available") is not True:
                failures.append("rollback_target_unavailable_or_mismatch")
                invariants.add("GI-07")

    source = receipt.get("source_resolution")
    if not isinstance(source, dict):
        failures.append("source_resolution_missing")
        invariants.add("GI-09")
    else:
        attempts = source.get("attempts")
        attempts = attempts if isinstance(attempts, list) else []
        missed_search_mechanisms = {
            str(item.get("mechanism"))
            for item in attempts
            if isinstance(item, dict)
            and item.get("mechanism") in {"ranked_repository_search", "code_search"}
            and item.get("result") == "miss"
        }
        search_miss = bool(missed_search_mechanisms)
        distinct_fallback = any(
            isinstance(item, dict)
            and item.get("mechanism") in DISTINCT_FALLBACKS
            and item.get("mechanism") not in missed_search_mechanisms
            and item.get("result") in {"found", "confirmed_absent"}
            for item in attempts
        )
        if source.get("resolved") is not True:
            failures.append("source_not_resolved")
            if search_miss and not distinct_fallback:
                failures.append("search_miss_without_distinct_fallback")
                invariants.add("GI-09")
        elif search_miss and not distinct_fallback:
            failures.append("resolved_claim_lacks_distinct_fallback_after_search_miss")
            invariants.add("GI-09")

    lifecycle = receipt.get("lifecycle") or {"applicable": False}
    if lifecycle.get("applicable") is True:
        ordered = lifecycle.get("ordered_stages")
        statuses = lifecycle.get("statuses")
        target_stage = lifecycle.get("target_stage")
        if not isinstance(ordered, list) or not ordered or not isinstance(statuses, dict) or target_stage not in ordered:
            failures.append("lifecycle_contract_invalid")
            invariants.add("GI-10")
        else:
            target_index = ordered.index(target_stage)
            prior_not_passed = False
            for stage in ordered[: target_index + 1]:
                status = statuses.get(stage)
                if prior_not_passed and status == "PASS":
                    failures.append(f"lifecycle_layer_promoted_over_gap:{stage}")
                    invariants.add("GI-10")
                if status != "PASS":
                    prior_not_passed = True
            if operation_result == "success" and statuses.get(target_stage) != "PASS":
                failures.append("target_lifecycle_stage_not_verified")
                invariants.add("GI-10")

    if material and operation_result == "success" and receipt.get("task_outcome_verified") is not True:
        failures.append("write_success_without_task_outcome_verification")
        invariants.add("GI-11")

    families = receipt.get("evidence_families")
    families = set(families) if isinstance(families, list) else set()
    if material and operation_result == "success":
        if len(families) < 2 or not families.intersection(STRONG_EVIDENCE_FAMILIES):
            failures.append("insufficient_cross_source_evidence")
            invariants.add("GI-12")

    required_scenarios = receipt.get("required_scenarios")
    required_scenarios = set(required_scenarios) if isinstance(required_scenarios, list) else set()
    if material and operation_result == "success":
        if "normal_valid_input" not in required_scenarios:
            failures.append("normal_valid_input_not_required")
        if not (required_scenarios - {"normal_valid_input"}):
            failures.append("no_adversarial_scenario_selected")
        unsupported = required_scenarios - SUPPORTED_SCENARIOS
        if unsupported:
            failures.append(f"unsupported_required_scenarios:{','.join(sorted(unsupported))}")

    records = receipt.get("scenario_results")
    records = records if isinstance(records, list) else []
    by_family: dict[str, dict] = {}
    for record in records:
        if not isinstance(record, dict):
            failures.append("scenario_record_not_object")
            continue
        family = str(record.get("family", ""))
        if family in by_family:
            failures.append(f"duplicate_scenario_record:{family}")
            continue
        by_family[family] = record

    for family in sorted(required_scenarios):
        record = by_family.get(family)
        if record is None:
            failures.append(f"required_scenario_not_executed:{family}")
            scenario_failures[family] = ["missing_record"]
            invariants.add(SCENARIO_GI_MAP.get(family, "GI-04"))
            continue
        family_failures = _scenario_failures(record)
        if family_failures:
            scenario_failures[family] = family_failures
            failures.append(f"scenario_failed:{family}")
            invariants.add(SCENARIO_GI_MAP.get(family, "GI-04"))

    if operation_result == "not_run":
        aggregate = "NOT_RUN"
    elif operation_result == "blocked" and not failures:
        aggregate = "BLOCKED"
    elif failures or invariants or operation_result == "failure":
        aggregate = "FAIL"
    elif operation_result == "blocked":
        aggregate = "BLOCKED"
    else:
        aggregate = "PASS"

    return {
        "schemaVersion": 1,
        "operation_id": receipt.get("operation_id"),
        "reported_revision": reported,
        "result": aggregate,
        "failures": sorted(set(failures)),
        "invariant_violations": sorted(invariants),
        "scenario_failures": scenario_failures,
        "executed_scenarios": sorted(
            family for family, record in by_family.items() if record.get("executed") is True
        ),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt_json")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        receipt = json.loads(pathlib.Path(args.receipt_json).read_text(encoding="utf-8"))
    except Exception as exc:
        result = {
            "schemaVersion": 1,
            "result": "FAIL",
            "failures": [f"receipt_load_failed:{type(exc).__name__}:{exc}"],
            "invariant_violations": [],
            "scenario_failures": {},
        }
    else:
        result = evaluate_receipt(receipt)
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
