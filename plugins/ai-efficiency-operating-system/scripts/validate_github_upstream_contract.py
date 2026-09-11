#!/usr/bin/env python3
"""Fail-closed structural validator for the ordinary-ChatGPT GitHub root-control contract."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "adapters" / "chatgpt" / "github-upstream-capability-contract.json"
APP = ROOT / ".app.json"
HOST_ADAPTERS = ROOT / "host-adapters.json"
SKILL = ROOT / "skills" / "github-operation-orchestrator" / "SKILL.md"
HUMAN = ROOT / "adapters" / "chatgpt" / "GITHUB_ROOT_CONTROL_PLANE.md"
EXPECTED_CONNECTOR = "connector_76869538009648d5b282a4bb21c3d157"
EXPECTED_CANONICAL_PLUGIN = "plugin_connector_1p_1a69035c238881919c4190932b2df699"
EXPECTED_CANONICAL_REF = "github@openai-curated"


def main():
    errors = []
    for path in (CONTRACT, APP, HOST_ADAPTERS, SKILL, HUMAN):
        if not path.exists():
            errors.append(f"missing:{path.relative_to(ROOT)}")
    if errors:
        print("GITHUB UPSTREAM CONTRACT FAIL")
        for e in errors:
            print("-", e)
        return 1

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    app = json.loads(APP.read_text(encoding="utf-8"))
    adapters = json.loads(HOST_ADAPTERS.read_text(encoding="utf-8"))
    skill = SKILL.read_text(encoding="utf-8")
    human = HUMAN.read_text(encoding="utf-8")

    canonical = contract.get("canonical_plugin") or {}
    if canonical.get("reference") != EXPECTED_CANONICAL_REF:
        errors.append("canonical plugin reference drift")
    if canonical.get("canonical_plugin_id") != EXPECTED_CANONICAL_PLUGIN:
        errors.append("canonical plugin id drift")
    if canonical.get("connector_id") != EXPECTED_CONNECTOR:
        errors.append("canonical connector id drift")
    if canonical.get("upstream_repository") != "openai/plugins":
        errors.append("upstream repository drift")
    if canonical.get("upstream_plugin_path") != "plugins/github":
        errors.append("upstream plugin path drift")
    if canonical.get("codex_mcp_is_separate_surface") is not True:
        errors.append("ordinary-chat vs codex MCP boundary missing")

    local_connector = (((app.get("apps") or {}).get("github") or {}).get("id"))
    if local_connector != EXPECTED_CONNECTOR:
        errors.append("local app binding does not match canonical connector")

    adapter_rows = adapters.get("adapters") or []
    github_rows = [row for row in adapter_rows if isinstance(row, dict) and row.get("name") == "github-pull-runtime"]
    if len(github_rows) != 1:
        errors.append("github host adapter count must equal one")
    else:
        adapter = github_rows[0]
        expected_adapter = {
            "host": "ordinary-chatgpt",
            "app_alias": "github",
            "connector_id": EXPECTED_CONNECTOR,
            "canonical_plugin_reference": EXPECTED_CANONICAL_REF,
            "canonical_plugin_id": EXPECTED_CANONICAL_PLUGIN,
            "runtime_policy": "adapters/chatgpt/github-pull-runtime.json",
            "upstream_capability_contract": "adapters/chatgpt/github-upstream-capability-contract.json",
            "human_contract": "adapters/chatgpt/GITHUB_OPERATION_LOOP.md",
            "root_control_plane": "adapters/chatgpt/GITHUB_ROOT_CONTROL_PLANE.md",
        }
        for key, expected in expected_adapter.items():
            if adapter.get(key) != expected:
                errors.append(f"host adapter drift:{key}")
        if adapter.get("allow_implicit_invocation") is not True:
            errors.append("github host adapter implicit invocation disabled")

    expected_order = [
        "chatgpt_host_permission_and_plugin_state",
        "canonical_openai_github_plugin_dependency",
        "live_github_connector_tool_namespace_and_action_schema",
        "github_remote_repository_state",
        "local_ai_efficiency_orchestrator_policy",
    ]
    if contract.get("ownership_order") != expected_order:
        errors.append("ownership order drift")

    ownership = contract.get("ownership_contract") or {}
    for key in ("chatgpt_host_owns", "openai_github_connector_owns", "github_remote_owns", "local_orchestrator_owns"):
        if not isinstance(ownership.get(key), list) or not ownership.get(key):
            errors.append(f"missing ownership class:{key}")

    ceiling = contract.get("local_capability_ceiling") or {}
    forbidden = set(ceiling.get("may_not_claim_or_create") or [])
    for item in (
        "new_connector_actions",
        "new_connector_endpoint_families",
        "oauth_or_github_app_scopes",
        "administration_or_secrets_access",
        "arbitrary_remote_shell_execution",
        "workflow_dispatch_when_no_live_dispatch_action_exists",
    ):
        if item not in forbidden:
            errors.append(f"missing local capability ceiling:{item}")
    for key in (
        "host_allow_all_actions_does_not_expand_action_inventory",
        "app_manifest_binding_does_not_prove_invokable_or_effective",
        "repository_policy_cannot_override_live_connector_schema",
    ):
        if ceiling.get(key) is not True:
            errors.append(f"missing capability truth:{key}")

    surface = contract.get("live_surface_rules") or {}
    for key in (
        "discover_before_material_call_when_schema_not_current",
        "live_tool_schema_is_authoritative",
        "absence_must_be_checked_by_narrow_tool_discovery_not_memory",
        "unknown_action_must_not_be_invented",
        "connector_error_or_schema_change_requires_rediscovery",
        "permission_setting_and_connector_capability_are_separate_dimensions",
    ):
        if surface.get(key) is not True:
            errors.append(f"missing live-surface invariant:{key}")

    observed = contract.get("observed_live_surface_capabilities") or {}
    if observed.get("chatgpt_app_permission_observed") != "Allow all actions":
        errors.append("observed host action permission baseline drift")
    if observed.get("workflow_dispatch_action_discovered") is not False:
        errors.append("workflow dispatch observation must remain an observation of absence")
    if observed.get("observations_are_not_permanent_contract") is not True:
        errors.append("live capability observations must not become permanent authority")

    search = contract.get("search_depth_contract") or {}
    for key in (
        "numeric_user_result_target_must_be_preserved",
        "single_default_search_call_is_not_exhaustive",
        "broad_search_may_request_topn_up_to_observed_supported_100",
        "response_truncation_is_not_result_exhaustion",
        "use_query_fanout_when_one_query_cannot_meet_breadth_target",
        "dedupe_by_canonical_repository_object_identity",
        "search_snippets_are_discovery_evidence_only",
        "material_claim_requires_targeted_object_read",
        "never_report_only_a_few_exist_from_one_shallow_query",
    ):
        if search.get(key) is not True:
            errors.append(f"missing search-depth invariant:{key}")
    if len(search.get("fanout_dimensions") or []) < 5:
        errors.append("insufficient search fanout dimensions")
    if "explicit_user_target_met" not in set(search.get("continue_until") or []):
        errors.append("search completion does not preserve explicit user target")

    execution = contract.get("execution_contract") or {}
    for key in (
        "connector_is_not_arbitrary_code_executor",
        "existing_workflow_rerun_is_not_new_workflow_dispatch",
        "automatic_trigger_must_be_bound_to_exact_commit",
        "green_ci_proves_declared_checks_only",
        "host_runtime_effect_requires_owning_surface_observation",
        "missing_required_execution_path_is_blocked_not_pass",
    ):
        if execution.get(key) is not True:
            errors.append(f"missing execution boundary:{key}")

    failures = contract.get("failure_classes") or {}
    for name in (
        "UPSTREAM_CAPABILITY_GAP",
        "HOST_PERMISSION_POLICY",
        "GITHUB_REMOTE_PERMISSION",
        "CALLER_SEARCH_UNDERFETCH",
        "CALLER_SCHEMA_STALE",
        "CALLER_RESPONSE_TRUNCATION",
        "CALLER_CHAIN_BREAK",
    ):
        if name not in failures:
            errors.append(f"missing root failure class:{name}")

    gate = contract.get("root_completion_gate") or {}
    for key in (
        "root_owner_identified_before_fix",
        "capability_gap_localized_to_owner",
        "local_fix_must_target_only_local_owner",
        "upstream_gap_must_not_be_papered_over_with_prompt_text",
        "search_breadth_target_must_be_measured_on_unique_results",
        "material_write_requires_exact_remote_readback",
        "execution_claim_requires_exact_run_or_runtime_effect_evidence",
    ):
        if gate.get(key) is not True:
            errors.append(f"missing root completion gate:{key}")

    for marker in (
        "Root-owner gate",
        "CALLER_SEARCH_UNDERFETCH",
        "Search breadth protocol",
        "UPSTREAM_CAPABILITY_GAP",
        "ordinary-ChatGPT GitHub connector is not an arbitrary shell executor",
    ):
        if marker.lower() not in skill.lower():
            errors.append(f"skill missing root marker:{marker}")

    for marker in (
        "first layer that actually owns",
        "Allow all actions",
        "Search-depth repair",
        "UPSTREAM_CAPABILITY_GAP",
        "Machine-readable companion",
    ):
        if marker.lower() not in human.lower():
            errors.append(f"human contract missing root marker:{marker}")

    if errors:
        print("GITHUB UPSTREAM CONTRACT FAIL")
        for e in errors:
            print("-", e)
        return 1

    print("GITHUB UPSTREAM CONTRACT PASS")
    print("canonical=github@openai-curated connector=" + EXPECTED_CONNECTOR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
