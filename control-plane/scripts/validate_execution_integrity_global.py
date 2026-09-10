#!/usr/bin/env python3
"""Validate repository-wide GitHub and execution-integrity invariants."""
from __future__ import annotations

import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "control-plane/ai-system/configs/execution-integrity-global.json"
POLICY_PATH = REPO_ROOT / "docs/GITHUB_EXECUTION_INTEGRITY_POLICY.md"
MANIFEST_PATH = REPO_ROOT / "control-plane/ai-system/configs/global-policy-manifest.json"
AGENTS_PATH = REPO_ROOT / "AGENTS.md"
WORKFLOW_PATH = REPO_ROOT / ".github/workflows/deep-reasoning-quality-gate.yml"

REQUIRED_INVARIANTS = {f"GI-{n:02d}" for n in range(1, 13)}
REQUIRED_FALLBACKS = {
    "exact_repository_lookup",
    "direct_file_fetch",
    "code_search",
    "tree_or_contents_lookup",
    "known_url_or_ref_resolution",
}
REQUIRED_VERSION_DIMENSIONS = {
    "default_branch",
    "head_commit_sha",
    "source_path",
    "file_blob_sha",
    "release_tag_or_package_marketplace_version_when_applicable",
    "installed_revision_when_applicable",
}
REQUIRED_SKILL_LAYERS = {
    "source_resolved",
    "registration_resolved",
    "version_resolved",
    "installed",
    "read_back",
    "discovered_or_registered",
    "executed",
    "observable_effect",
    "regression_preserved",
}
REQUIRED_SCENARIOS = {
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


def _load_json(path: pathlib.Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected_object:{path}")
    return value


def _require(condition: bool, code: str, failures: list[str]) -> None:
    if not condition:
        failures.append(code)


def _all_true(section: dict, keys: set[str], failures: list[str], prefix: str) -> None:
    for key in sorted(keys):
        _require(section.get(key) is True, f"{prefix}_{key}_missing_or_false", failures)


def validate() -> list[str]:
    failures: list[str] = []
    required_paths = [CONFIG_PATH, POLICY_PATH, MANIFEST_PATH, AGENTS_PATH, WORKFLOW_PATH]
    for path in required_paths:
        if not path.is_file():
            failures.append(f"missing:{path.relative_to(REPO_ROOT)}")
    if failures:
        return sorted(set(failures))

    try:
        config = _load_json(CONFIG_PATH)
        manifest = _load_json(MANIFEST_PATH)
    except Exception as exc:
        return [f"json_invalid:{type(exc).__name__}:{exc}"]

    _require(config.get("schema_version") == 1, "schema_version_mismatch", failures)
    _require(config.get("profile_id") == "execution-integrity-v1", "profile_id_mismatch", failures)
    _require(config.get("scope") == "repository-wide", "scope_not_repository_wide", failures)
    _require(config.get("default_enabled") is True, "profile_not_default_enabled", failures)

    invariants = config.get("system_invariants") or {}
    _require(REQUIRED_INVARIANTS.issubset(set(invariants)), "system_invariants_incomplete", failures)

    gate = config.get("invariant_gate") or {}
    _all_true(
        gate,
        {
            "declare_before_material_change",
            "retest_after_change",
            "any_applicable_violation_blocks_pass",
            "unknown_is_not_pass",
            "protected_capability_regression_is_fail",
        },
        failures,
        "invariant_gate",
    )

    triangulation = config.get("source_triangulation") or {}
    _all_true(
        triangulation,
        {
            "material_work_requires_multiple_evidence_families_when_practical",
            "official_documentation_alone_is_not_execution_proof",
            "third_party_instruction_alone_is_not_execution_proof",
            "popularity_alone_is_not_proof",
            "unsupported_or_undocumented_must_not_be_rewritten_as_impossible_without_corrobation",
            "conflicts_require_discriminating_runtime_or_revision_test",
            "higher_priority_platform_authorization_and_safety_constraints_remain_binding",
        },
        failures,
        "source_triangulation",
    )
    evidence_families = set(triangulation.get("evidence_families") or [])
    _require("target_runtime_or_owning_installation_readback" in evidence_families, "runtime_evidence_family_missing", failures)
    _require("high_signal_third_party_practitioner_or_tooling_evidence" in evidence_families, "third_party_evidence_family_missing", failures)
    _require("official_documentation" in evidence_families, "official_evidence_family_missing", failures)

    source = config.get("github_source_resolution") or {}
    _all_true(
        source,
        {
            "exact_target_identity_required",
            "ranked_search_not_sufficient_when_exact_identity_is_known",
            "search_miss_requires_distinct_fallback_before_absence_claim",
            "search_hit_commit_and_default_branch_head_must_not_be_conflated",
            "wrapper_cli_or_marketplace_source_must_be_cross_checked_against_repository",
            "reproducible_install_prefers_tag_or_commit_pin",
        },
        failures,
        "github_source",
    )
    _require(REQUIRED_FALLBACKS.issubset(set(source.get("fallback_routes") or [])), "github_fallback_routes_incomplete", failures)
    _require(
        REQUIRED_VERSION_DIMENSIONS.issubset(set(source.get("required_version_dimensions") or [])),
        "github_version_dimensions_incomplete",
        failures,
    )

    write = config.get("github_write_integrity") or {}
    _all_true(
        write,
        {
            "record_base_commit_before_material_write",
            "record_prewrite_blob_sha",
            "isolated_branch_preferred_for_nontrivial_repair",
            "readback_after_each_material_write",
            "compare_intended_and_returned_content",
            "inspect_complete_changed_file_set",
            "test_exact_repair_revision",
            "adjacent_path_regression_required",
            "workflow_verification_must_bind_exact_run_and_commit",
            "commit_pr_or_green_ci_alone_cannot_satisfy_behavior",
            "same_path_dependent_writes_must_not_run_in_parallel",
        },
        failures,
        "github_write",
    )

    skill = config.get("skill_plugin_integrity") or {}
    _require(REQUIRED_SKILL_LAYERS.issubset(set(skill.get("layers") or [])), "skill_plugin_layers_incomplete", failures)
    _all_true(
        skill,
        {
            "lower_layer_must_not_claim_higher_layer",
            "implementation_file_and_manifest_both_verified_when_manifest_exists",
            "installed_bytes_or_state_must_match_intended_source_identity",
            "representative_execution_required_for_activation_claim",
        },
        failures,
        "skill_plugin",
    )

    scenarios = config.get("adversarial_scenarios") or {}
    _require(scenarios.get("select_by_causal_relevance_not_ceremony") is True, "scenario_selection_rule_missing", failures)
    _require(REQUIRED_SCENARIOS.issubset(set(scenarios.get("families") or [])), "adversarial_scenarios_incomplete", failures)
    _require(
        {"precondition", "action", "expected_result", "actual_result", "evidence", "invariant_violations"}.issubset(
            set(scenarios.get("record_fields") or [])
        ),
        "scenario_record_fields_incomplete",
        failures,
    )

    maturity = config.get("tool_maturity") or {}
    _all_true(
        maturity,
        {
            "prefer_exact_identifiers_once_known",
            "pivot_from_search_to_exact_lookup_on_false_negative_signal",
            "two_similar_failures_require_mechanism_change",
            "permissions_must_come_from_returned_repository_metadata_when_available",
            "update_delete_requires_current_blob_sha",
            "truncated_response_requires_targeted_refetch",
            "readback_required_before_persistence_claim",
        },
        failures,
        "tool_maturity",
    )

    release = config.get("release") or {}
    _require(set(release.get("statuses") or []) == {"PASS", "FAIL", "BLOCKED", "NOT_RUN"}, "release_statuses_invalid", failures)
    _all_true(
        release,
        {
            "pass_requires_all_hard_criteria_and_applicable_invariants",
            "not_run_cannot_be_pass",
            "symptom_removed_but_invariant_broken_is_fail",
            "contradictory_evidence_overrides_pass",
        },
        failures,
        "release",
    )

    canonical = manifest.get("canonical_policies") or []
    policy_index = {item.get("id"): item for item in canonical if isinstance(item, dict)}
    _require(
        (policy_index.get("github-execution-integrity") or {}).get("path") == "docs/GITHUB_EXECUTION_INTEGRITY_POLICY.md",
        "manifest_github_execution_policy_missing",
        failures,
    )
    _require(
        (policy_index.get("execution-integrity-machine") or {}).get("path")
        == "control-plane/ai-system/configs/execution-integrity-global.json",
        "manifest_execution_integrity_machine_missing",
        failures,
    )

    entrypoints = manifest.get("entrypoints") or []
    roles = {item.get("role"): item for item in entrypoints if isinstance(item, dict)}
    validator_entry = roles.get("execution_integrity_machine_validator") or {}
    _require(
        validator_entry.get("path") == "control-plane/scripts/validate_execution_integrity_global.py",
        "manifest_execution_integrity_validator_missing",
        failures,
    )

    agents_text = AGENTS_PATH.read_text(encoding="utf-8")
    policy_text = POLICY_PATH.read_text(encoding="utf-8")
    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8")

    for token in ["GITHUB_EXECUTION_INTEGRITY_POLICY.md", "execution-integrity-global.json"]:
        _require(token in agents_text, f"agents_missing_reference:{token}", failures)
    for invariant in sorted(REQUIRED_INVARIANTS):
        _require(invariant in policy_text, f"policy_missing:{invariant}", failures)
    for token in [
        "validate_execution_integrity_global.py",
        "execution-integrity-global.json",
        "tests/test_execution_integrity_global.py",
    ]:
        _require(token in workflow_text, f"workflow_missing:{token}", failures)

    return sorted(set(failures))


def main() -> int:
    failures = validate()
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("PASS execution-integrity-v1 global invariants")
    return 0


if __name__ == "__main__":
    sys.exit(main())
