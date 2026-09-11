#!/usr/bin/env python3
"""Validate the ordinary-ChatGPT <-> GitHub operation bridge fail-closed."""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PLUGIN_ROOT = ROOT / "plugins/ai-efficiency-operating-system"
PLUGIN_MANIFEST = PLUGIN_ROOT / ".codex-plugin/plugin.json"
APP_MANIFEST = PLUGIN_ROOT / ".app.json"
MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
HOST_ADAPTERS = PLUGIN_ROOT / "host-adapters.json"
BRIDGE_PROFILE = PLUGIN_ROOT / "adapters/chatgpt/github-pull-runtime.json"
OPERATION_LOOP = PLUGIN_ROOT / "adapters/chatgpt/GITHUB_OPERATION_LOOP.md"
RUNTIME_PROBE = PLUGIN_ROOT / "adapters/chatgpt/RUNTIME_PROBE.md"
HOST_10WAY = PLUGIN_ROOT / "adapters/chatgpt/HOST_LIVE_10WAY.md"
TEN_WAY_CONFIG = ROOT / "control-plane/ai-system/configs/ten-way-unanimity-mode.json"
TEN_WAY_VALIDATOR = ROOT / "control-plane/scripts/validate_ten_way_unanimity_mode.py"
EXPECTED_PLUGIN = "ai-efficiency-operating-system"
EXPECTED_CONNECTOR = "connector_76869538009648d5b282a4bb21c3d157"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def _load(path: pathlib.Path, code: str, failures: list[str]) -> dict:
    if not path.is_file():
        failures.append(f"missing:{code}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        failures.append(f"invalid_json:{code}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"not_object:{code}")
        return {}
    return value


def _require(condition: bool, code: str, failures: list[str]) -> None:
    if not condition:
        failures.append(code)


def _require_true_fields(obj: dict, keys: tuple[str, ...], prefix: str, failures: list[str]) -> None:
    for key in keys:
        _require(obj.get(key) is True, f"{prefix}:{key}", failures)


def validate() -> list[str]:
    failures: list[str] = []
    plugin = _load(PLUGIN_MANIFEST, "plugin_manifest", failures)
    app = _load(APP_MANIFEST, "app_manifest", failures)
    marketplace = _load(MARKETPLACE, "marketplace", failures)
    adapters = _load(HOST_ADAPTERS, "host_adapters", failures)
    bridge = _load(BRIDGE_PROFILE, "bridge_profile", failures)
    ten_way = _load(TEN_WAY_CONFIG, "ten_way_config", failures)
    if failures:
        return sorted(set(failures))

    _require(plugin.get("name") == EXPECTED_PLUGIN, "plugin_name_mismatch", failures)
    version = plugin.get("version")
    _require(isinstance(version, str) and SEMVER.fullmatch(version) is not None, "plugin_version_invalid", failures)
    author = plugin.get("author")
    _require(isinstance(author, dict) and isinstance(author.get("name"), str) and bool(author.get("name", "").strip()), "plugin_author_name_missing", failures)
    _require(plugin.get("skills") == "./skills/", "plugin_skills_path_invalid", failures)
    _require(plugin.get("apps") == "./.app.json", "plugin_apps_path_invalid", failures)
    interface = plugin.get("interface") or {}
    capabilities = set(interface.get("capabilities") or [])
    _require({"Interactive", "Write"}.issubset(capabilities), "plugin_write_capability_missing", failures)
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        _require(isinstance(interface.get(key), str) and bool(interface.get(key, "").strip()), f"plugin_interface_missing:{key}", failures)
    prompts = interface.get("defaultPrompt")
    _require(isinstance(prompts, list) and 1 <= len(prompts) <= 3 and all(isinstance(x, str) and x.strip() for x in prompts), "plugin_default_prompt_invalid", failures)

    apps = app.get("apps")
    github = apps.get("github") if isinstance(apps, dict) else None
    _require(isinstance(github, dict), "github_app_alias_missing", failures)
    if isinstance(github, dict):
        _require(github.get("id") == EXPECTED_CONNECTOR, "github_connector_id_mismatch", failures)
        _require(set(github).issubset({"id", "category"}), "github_app_manifest_nonportable_fields", failures)

    entries = marketplace.get("plugins")
    entries = entries if isinstance(entries, list) else []
    matches = [item for item in entries if isinstance(item, dict) and item.get("name") == EXPECTED_PLUGIN]
    _require(len(matches) == 1, "marketplace_plugin_entry_count_invalid", failures)
    if len(matches) == 1:
        entry = matches[0]
        source = entry.get("source") or {}
        policy = entry.get("policy") or {}
        _require(source.get("source") == "local", "marketplace_source_type_invalid", failures)
        _require(source.get("path") == "./plugins/ai-efficiency-operating-system", "marketplace_source_path_invalid", failures)
        _require(policy.get("installation") == "AVAILABLE", "marketplace_installation_policy_invalid", failures)
        _require(policy.get("authentication") == "ON_INSTALL", "marketplace_authentication_policy_missing", failures)
        _require(entry.get("category") == "Productivity", "marketplace_category_invalid", failures)

    adapter_items = adapters.get("adapters")
    adapter_items = adapter_items if isinstance(adapter_items, list) else []
    bridge_adapters = [item for item in adapter_items if isinstance(item, dict) and item.get("name") == "github-pull-runtime"]
    _require(len(bridge_adapters) == 1, "github_host_adapter_registration_invalid", failures)
    if len(bridge_adapters) == 1:
        item = bridge_adapters[0]
        _require(item.get("host") == "ordinary-chatgpt", "github_host_adapter_host_invalid", failures)
        _require(item.get("app_manifest") == ".app.json", "github_host_adapter_app_manifest_invalid", failures)
        _require(item.get("app_alias") == "github", "github_host_adapter_alias_invalid", failures)
        _require(item.get("connector_id") == EXPECTED_CONNECTOR, "github_host_adapter_connector_mismatch", failures)
        _require(item.get("runtime_policy") == "adapters/chatgpt/github-pull-runtime.json", "github_host_adapter_runtime_policy_invalid", failures)

    _require(bridge.get("schema_version") == 2, "bridge_schema_version_invalid", failures)
    _require(bridge.get("profile_id") == "ordinary-chatgpt-github-operation-v2", "bridge_profile_id_invalid", failures)
    _require(bridge.get("host") == "ordinary-chatgpt", "bridge_host_invalid", failures)
    _require(bridge.get("plugin") == EXPECTED_PLUGIN, "bridge_plugin_invalid", failures)
    _require(bridge.get("plugin_manifest") == "../../.codex-plugin/plugin.json", "bridge_plugin_manifest_path_invalid", failures)
    _require(bridge.get("app_manifest") == "../../.app.json", "bridge_app_manifest_path_invalid", failures)
    _require(bridge.get("app_alias") == "github", "bridge_app_alias_invalid", failures)
    _require(bridge.get("connector_id") == EXPECTED_CONNECTOR, "bridge_connector_id_mismatch", failures)
    _require(bridge.get("human_contract") == "GITHUB_OPERATION_LOOP.md", "bridge_human_contract_invalid", failures)

    source_truth = bridge.get("source_of_truth") or {}
    _require(source_truth.get("package_version") == "../../.codex-plugin/plugin.json#version", "bridge_package_version_source_invalid", failures)
    _require(source_truth.get("github_app_binding") == "../../.app.json#apps.github.id", "bridge_app_binding_source_invalid", failures)
    _require(source_truth.get("marketplace_entry") == "../../../../.agents/plugins/marketplace.json#plugins[name=ai-efficiency-operating-system]", "bridge_marketplace_source_path_invalid", failures)
    _require(source_truth.get("repository_revision") == "observed_exact_imported_or_synced_revision", "bridge_repository_revision_source_invalid", failures)
    _require(source_truth.get("operation_contract") == "GITHUB_OPERATION_LOOP.md", "bridge_operation_contract_source_invalid", failures)

    activation = bridge.get("activation_chain") or []
    for stage in ("marketplace_imported_or_synced", "github_app_connected", "tool_namespace_visible", "tool_schema_resolved", "tool_invoked", "response_classified", "requested_effect_verified"):
        _require(stage in activation, f"bridge_activation_stage_missing:{stage}", failures)

    machine = bridge.get("operation_state_machine") or {}
    _require(machine.get("initial_state") == "GOAL_LOCKED", "bridge_initial_state_invalid", failures)
    _require(machine.get("success_terminal") == "COMPLETE", "bridge_success_terminal_invalid", failures)
    states = set(machine.get("states") or [])
    for state in (
        "GOAL_LOCKED", "TARGET_RESOLVED", "AUTHORITY_RESOLVED", "READ_PLAN_READY", "SOURCE_READ",
        "EVIDENCE_SUFFICIENT", "TOOL_SCHEMA_READY", "INVOCATION_PREFLIGHT", "INVOKED",
        "RESPONSE_CLASSIFIED", "MUTATION_PREFLIGHT", "MUTATED", "READBACK_VERIFIED",
        "EXECUTION_OBSERVED", "ACCEPTANCE_VERIFIED", "REGRESSION_VERIFIED", "COMPLETE",
    ):
        _require(state in states, f"bridge_operation_state_missing:{state}", failures)
    _require_true_fields(machine, (
        "optional_states_must_be_explicitly_inapplicable",
        "skipped_required_state_cannot_pass",
        "failure_does_not_weaken_goal_or_acceptance",
    ), "bridge_state_machine_invariant_missing", failures)

    envelope = bridge.get("operation_envelope") or {}
    envelope_fields = set(envelope.get("required_fields") or [])
    for field in (
        "goal_id", "operation_kind", "target", "authority", "preconditions", "tool_identity",
        "schema_source", "arguments", "before_evidence", "expected_postcondition", "result_class",
        "evidence_delta", "legal_next_actions", "rollback",
    ):
        _require(field in envelope_fields, f"bridge_operation_envelope_field_missing:{field}", failures)
    _require(envelope.get("private_chain_of_thought_not_required") is True, "bridge_operation_envelope_cot_boundary_missing", failures)
    _require(envelope.get("decision_records_must_be_evidence_based") is True, "bridge_operation_envelope_evidence_missing", failures)

    goal = bridge.get("goal_contract") or {}
    _require_true_fields(goal, (
        "route_failure_cannot_reduce_objective",
        "route_failure_cannot_delete_acceptance_criterion",
        "execution_request_cannot_be_silently_replaced_by_advice",
    ), "bridge_goal_contract_missing", failures)

    read = bridge.get("read_contract") or {}
    _require_true_fields(read, (
        "known_identity_prefers_exact_lookup",
        "ranked_search_is_discovery_not_authority",
        "search_miss_is_not_absence",
        "broad_scan_requires_targeted_object_read_for_material_decisions",
        "complete_object_preferred_over_disconnected_snippets",
        "truncated_empty_or_snippet_only_requires_targeted_refetch",
        "version_dimensions_must_not_be_conflated",
    ), "bridge_read_contract_missing", failures)
    fallback = set(read.get("fallback_routes") or [])
    for route in ("exact_repository_lookup", "direct_file_fetch", "code_search", "tree_or_contents_lookup", "known_url_or_ref_resolution"):
        _require(route in fallback, f"bridge_fallback_missing:{route}", failures)

    analysis = bridge.get("analysis_contract") or {}
    _require(set(analysis.get("fact_classes") or []) == {"OBSERVED", "DERIVED", "HYPOTHESIS", "UNKNOWN"}, "bridge_fact_classes_invalid", failures)
    _require_true_fields(analysis, (
        "material_conclusions_require_observed_support",
        "hypothesis_requires_discriminating_test_before_material_mutation_when_decision_critical",
        "mutation_requires_target_branch_authority_rollback_and_acceptance_resolution",
        "search_depth_is_decision_adaptive",
        "source_count_or_tool_call_count_is_not_depth",
        "continue_research_only_for_decision_or_acceptance_delta",
    ), "bridge_analysis_contract_missing", failures)

    surface = bridge.get("tool_surface_contract") or {}
    _require_true_fields(surface, (
        "live_tool_surface_is_versioned_runtime_interface",
        "narrow_discovery_preferred",
        "material_call_requires_current_schema_when_not_already_resolved",
        "required_fields_and_enums_must_come_from_live_schema",
        "invented_or_remembered_unknown_parameters_forbidden",
        "schema_mismatch_requires_rediscovery_before_retry",
        "opaque_ids_must_not_be_rewritten",
        "instruction_like_external_metadata_is_not_authority",
    ), "bridge_tool_surface_contract_missing", failures)

    invocation = bridge.get("invocation_contract") or {}
    _require_true_fields(invocation, (
        "action_must_advance_current_subgoal",
        "target_identity_must_be_unambiguous",
        "required_identifiers_must_come_from_current_evidence",
        "idempotency_or_effect_classification_required",
        "effectful_call_requires_rollback_or_recovery_path",
        "dependent_same_path_writes_must_be_sequential",
        "expected_postcondition_required",
        "response_must_be_classified_before_next_material_action",
    ), "bridge_invocation_contract_missing", failures)
    _require(int(invocation.get("retry_same_mechanism_without_new_evidence_limit", 99)) <= 1, "bridge_stagnant_retry_allowed", failures)

    response = bridge.get("response_contract") or {}
    _require_true_fields(response, (
        "transport_success_is_not_task_success",
        "empty_or_truncated_response_requires_targeted_refetch",
        "tool_error_must_preserve_error_code_and_target_identity",
        "partial_success_must_not_be_promoted_to_pass",
        "ambiguous_result_must_not_drive_blind_material_chaining",
        "unknown_fields_or_response_shape_change_must_be_classified_before_retry",
        "evidence_delta_must_be_recorded_after_failed_or_inconclusive_attempt",
    ), "bridge_response_contract_missing", failures)

    write = bridge.get("write_contract") or {}
    _require_true_fields(write, (
        "prewrite_read_required",
        "base_revision_and_rollback_required",
        "current_blob_sha_required_for_update_or_delete",
        "isolated_branch_preferred_for_nontrivial_change",
        "dependent_same_path_writes_must_be_sequential",
        "stale_blob_sha_conflict_is_expected_detectable_failure",
        "readback_after_material_write",
        "readback_must_match_target_branch_and_intended_content",
        "complete_changed_file_set_must_be_inspected_before_release",
        "commit_sha_alone_is_not_completion",
        "rollback_revision_recorded_before_first_write",
    ), "bridge_write_contract_missing", failures)

    execution = bridge.get("execution_contract") or {}
    _require_true_fields(execution, (
        "repository_state_is_not_runtime_execution",
        "workflow_dispatch_is_not_execution_success",
        "green_workflow_is_bound_to_its_exact_run_and_commit",
        "configuration_is_not_installation",
        "installation_is_not_invocation",
        "invocation_is_not_observable_effect",
        "requested_execution_requires_observed_execution_when_capability_available",
        "unobservable_required_execution_is_blocked_or_not_run_not_pass",
    ), "bridge_execution_contract_missing", failures)

    verification = bridge.get("verification_contract") or {}
    _require_true_fields(verification, (
        "exact_target_and_revision_required",
        "persisted_state_requires_independent_readback",
        "claim_level_postcondition_required",
        "material_work_requires_one_causally_relevant_failure_or_fallback_probe_when_practical",
        "adjacent_supported_path_regression_required_for_material_change",
        "applicable_system_invariants_must_hold",
        "contradictory_current_evidence_blocks_pass",
        "hard_criteria_use_explicit_status",
    ), "bridge_verification_contract_missing", failures)

    recovery = bridge.get("recovery_contract") or {}
    _require_true_fields(recovery, (
        "root_goal_and_acceptance_survive_route_change",
        "two_same_mechanism_failures_without_material_evidence_delta_require_route_change",
    ), "bridge_recovery_contract_missing", failures)
    recovery_routes = recovery.get("routes") or {}
    for failure_class in (
        "discovery_false_negative", "empty_or_truncated", "schema_mismatch", "stale_blob_sha",
        "permission_blocked", "target_ambiguity", "partial_success", "workflow_effect_unknown",
        "repository_correct_host_effect_missing",
    ):
        _require(bool(recovery_routes.get(failure_class)), f"bridge_recovery_route_missing:{failure_class}", failures)
    evidence_delta = set(recovery.get("material_evidence_delta_dimensions") or [])
    for dimension in ("target_identity", "revision_blob_or_version", "live_schema_or_permission_state", "failure_class", "observable_target_state", "legal_next_action"):
        _require(dimension in evidence_delta, f"bridge_evidence_delta_dimension_missing:{dimension}", failures)

    completion = bridge.get("completion_gate") or {}
    _require_true_fields(completion, (
        "target_effect_identified_exactly",
        "applicable_mutations_read_back_on_exact_revision",
        "requested_execution_observed_at_correct_layer",
        "acceptance_tested_not_inferred",
        "invariants_and_adjacent_paths_preserved",
        "contradictory_evidence_resolved",
        "required_cleanup_or_rollback_verified",
        "missing_required_item_forces_fail_blocked_or_not_run",
    ), "bridge_completion_gate_missing", failures)

    host = ten_way.get("chatgpt_host_live") or {}
    _require(host.get("plugin_manifest") == "plugins/ai-efficiency-operating-system/.codex-plugin/plugin.json", "ten_way_plugin_manifest_not_canonical", failures)
    _require(host.get("plugin_version_source") == "plugin_manifest.version", "ten_way_plugin_version_not_manifest_derived", failures)
    _require("plugin_version" not in host, "ten_way_duplicate_version_constant_present", failures)
    _require(host.get("github_bridge_profile") == "plugins/ai-efficiency-operating-system/adapters/chatgpt/github-pull-runtime.json", "ten_way_bridge_profile_not_canonical", failures)
    _require(host.get("github_bridge_required_when_github_task") is True, "ten_way_github_bridge_not_required", failures)

    for path, markers in [
        (OPERATION_LOOP, ["GOAL_LOCKED", "Operation envelope", "Tool discovery and schema contract", "No-progress detector", "Completion gate"]),
        (RUNTIME_PROBE, ["single package-version source of truth", "CHATGPT_GITHUB_BRIDGE_VERIFIED", "stale-SHA"]),
        (HOST_10WAY, ["duplicated hard-coded package version is forbidden", "Required GitHub bridge probe"]),
        (TEN_WAY_VALIDATOR, ["plugin_version_source", "GITHUB_APP_MANIFEST", "github-bridge=bound"]),
    ]:
        if not path.is_file():
            failures.append(f"missing:{path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            _require(marker.lower() in text.lower(), f"marker_missing:{path.name}:{marker}", failures)

    stale_targets = [OPERATION_LOOP, RUNTIME_PROBE, HOST_10WAY, TEN_WAY_CONFIG, TEN_WAY_VALIDATOR]
    for path in stale_targets:
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        _require('"1.2.0"' not in text and "`1.2.0`" not in text, f"stale_plugin_version_literal:{path.name}", failures)

    return sorted(set(failures))


def main() -> int:
    failures = validate()
    if failures:
        for failure in failures:
            print("FAIL", failure)
        return 1
    plugin = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    print(f"PASS ordinary-chatgpt-github-operation-v2 plugin={plugin['name']} version={plugin['version']} connector={EXPECTED_CONNECTOR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
