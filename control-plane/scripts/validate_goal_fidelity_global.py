#!/usr/bin/env python3
"""Validate the goal-fidelity and target-lock machine contract."""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_PRIMARY = {
    "literal_intent",
    "authority_or_spec",
    "environment_entity_identity",
    "acceptance_evidence_backward",
    "reverse_failure",
}

REQUIRED_ESCALATION = {
    "counterfactual",
    "exclusion",
    "dependency_path",
    "cross_source_consistency",
    "purpose_value",
}

REQUIRED_ANTI_EVASION_SUBSTITUTIONS = {
    "inspect_exploit_bypass_kill_or_weaken_controller_to_escape_work",
    "game_string_checks_or_completion_detectors",
    "satisfy_agent_headcount_without_unique_goal_advancing_contribution",
    "substitute_refusal_policy_or_ethics_debate_for_allowed_task_progress",
    "fabricate_runtime_independence_execution_or_completion",
    "reduce_required_effort_agent_count_tests_or_acceptance_criteria_to_escape_a_blocker",
}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    path = root / "control-plane/ai-system/configs/goal-fidelity-global.json"
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, ensure_ascii=False))
        return 1

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("default_enabled") is not True:
        errors.append("default_enabled must be true")

    contract = data.get("goal_contract") or {}
    required_fields = set(contract.get("required_fields") or [])
    for field in ("ROOT_GOAL", "TARGET_IDENTITY", "ACCEPTANCE_TESTS", "UNDERLYING_PURPOSE", "GOAL_SIGNATURE"):
        if field not in required_fields:
            errors.append(f"missing goal contract field: {field}")
    if contract.get("silent_goal_mutation_forbidden") is not True:
        errors.append("silent goal mutation must be forbidden")

    primary = data.get("primary_gate") or {}
    if int(primary.get("minimum_independent_analyzers", 0)) < 5:
        errors.append("primary gate must require at least 5 independent analyzers")
    if not REQUIRED_PRIMARY.issubset(set(primary.get("analyzers") or [])):
        errors.append("primary gate is missing one or more required analyzers")

    escalation = data.get("escalation_gate") or {}
    if not REQUIRED_ESCALATION.issubset(set(escalation.get("additional_analyzers") or [])):
        errors.append("escalation gate is missing one or more required analyzers")
    if escalation.get("guessing_on_high_impact_ambiguity_forbidden") is not True:
        errors.append("high-impact ambiguity must not be guessed")

    drift = data.get("drift_control") or {}
    if drift.get("goal_signature_required") is not True:
        errors.append("goal signature must be required")
    if "before_release" not in set(drift.get("checkpoint_triggers") or []):
        errors.append("before_release drift checkpoint is required")

    anti = data.get("anti_evasion_control") or {}
    for key in (
        "stop_or_block_event_does_not_change_root_goal",
        "controller_hook_or_guard_is_not_promoted_to_task_target",
        "current_blocker_is_recorded_separately_from_root_goal",
        "goal_signature_must_survive_stop_retry_and_recovery",
    ):
        if anti.get(key) is not True:
            errors.append(f"anti-evasion invariant missing: {key}")

    substitutions = set(anti.get("forbidden_progress_substitutions") or [])
    missing_substitutions = REQUIRED_ANTI_EVASION_SUBSTITUTIONS - substitutions
    for item in sorted(missing_substitutions):
        errors.append(f"anti-evasion forbidden substitution missing: {item}")

    on_block = anti.get("on_block") or {}
    if on_block.get("required_next_step") != "highest_value_goal_advancing_action_available_under_current_constraints":
        errors.append("blocked continuation must select the highest-value goal-advancing action")
    for key in (
        "route_pivot_is_preferred_over_goal_pivot",
        "blocker_may_not_become_root_goal",
        "non_progress_actions_do_not_satisfy_stop_or_completion_gates",
    ):
        if on_block.get(key) is not True:
            errors.append(f"blocked-continuation invariant missing: {key}")

    contribution = anti.get("multi_agent_contribution_gate") or {}
    for key in (
        "headcount_alone_never_satisfies_requirement",
        "each_activated_agent_requires_distinct_role",
        "each_activated_agent_requires_unique_evidence_test_artifact_or_implementation_contribution",
        "contribution_must_map_to_goal_contract_or_acceptance_test",
        "policy_only_or_refusal_only_agent_does_not_count_unless_policy_analysis_is_the_user_task",
        "runtime_independence_must_be_observed_before_claimed",
    ):
        if contribution.get(key) is not True:
            errors.append(f"multi-agent contribution invariant missing: {key}")

    mesh = data.get("evidence_mesh") or {}
    sources = set(mesh.get("default_sources_for_substantive_tasks_when_available") or [])
    if not {"GitHub", "Notion"}.issubset(sources):
        errors.append("GitHub and Notion must be default evidence sources when available")
    if mesh.get("connector_use_must_be_observed_not_assumed") is not True:
        errors.append("connector use must be observed, not assumed")

    capability = data.get("capability_preservation") or {}
    if capability.get("requested_reasoning_effort_or_agent_budget_must_not_be_reduced_as_an_evasion_strategy") is not True:
        errors.append("requested reasoning effort or agent budget must not be reduced to escape a blocker")

    release = data.get("release_gate") or {}
    required_pass = set(release.get("pass_requires") or [])
    for item in (
        "target_identity_evidenced",
        "final_goal_drift_check_passed",
        "no_controller_evasion_or_headcount_substitution",
    ):
        if item not in required_pass:
            errors.append(f"release gate missing: {item}")

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
