#!/usr/bin/env python3
"""Validate the Goal Intelligence / Target Lock machine contract."""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_PRIMARY = {
    "literal_intent",
    "environment_entity_identity",
    "acceptance_evidence_backward",
    "causal_dependency_owner",
    "reverse_failure",
}

REQUIRED_ESCALATION = {
    "counterfactual",
    "exclusion",
    "cross_source_consistency",
    "purpose_value",
    "intent_delta",
}

REQUIRED_GOAL_FIELDS = {
    "ROOT_GOAL",
    "TARGET_IDENTITY",
    "ACCEPTANCE_TESTS",
    "UNDERLYING_PURPOSE",
    "PREFERENCE_PROFILE",
    "DECISION_CRITICAL_UNKNOWNS",
    "ASSUMPTION_LEDGER",
    "GOAL_SIGNATURE",
}

REQUIRED_ANTI_EVASION_SUBSTITUTIONS = {
    "inspect_exploit_bypass_kill_or_weaken_controller_to_escape_work",
    "game_string_checks_or_completion_detectors",
    "satisfy_agent_headcount_without_unique_goal_advancing_contribution",
    "substitute_refusal_policy_or_ethics_debate_for_allowed_task_progress",
    "fabricate_runtime_independence_execution_or_completion",
    "reduce_required_effort_agent_count_tests_or_acceptance_criteria_to_escape_a_blocker",
}

REQUIRED_RESEARCH_LANES = {
    "commit_archaeology",
    "issue_history",
    "pull_request_discussions",
    "regression_tests_and_fixtures",
    "benchmark_methodology_and_raw_metrics",
    "paper_and_citation_chaining",
    "negative_evidence_and_failure_reports",
    "abandoned_or_reverted_approaches",
    "prompt_and_config_archaeology",
    "benchmark_counterexamples_or_hidden_test_style_evals",
}


def require_true(errors: list[str], mapping: dict, key: str, label: str) -> None:
    if mapping.get(key) is not True:
        errors.append(f"{label}: {key}")


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    path = root / "control-plane/ai-system/configs/goal-fidelity-global.json"
    errors: list[str] = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, ensure_ascii=False))
        return 1

    if data.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    require_true(errors, data, "default_enabled", "global invariant missing")

    contract = data.get("goal_contract") or {}
    missing = REQUIRED_GOAL_FIELDS - set(contract.get("required_fields") or [])
    for field in sorted(missing):
        errors.append(f"missing goal contract field: {field}")
    require_true(errors, contract, "silent_goal_mutation_forbidden", "goal contract invariant missing")

    inference = data.get("intent_inference") or {}
    for key in (
        "intent_belief_graph_required_for_substantive_tasks",
        "low_confidence_hidden_intent_may_not_become_hard_requirement",
        "semantic_delta_required_on_each_user_turn",
        "superseded_constraints_marked_obsolete",
        "stale_constraints_may_not_silently_survive_intent_shift",
    ):
        require_true(errors, inference, key, "intent inference invariant missing")
    if int(inference.get("candidate_goal_limit", 0)) < 2:
        errors.append("candidate_goal_limit must preserve competing interpretations")
    if "obsolete_constraint" not in set(inference.get("node_types") or []):
        errors.append("intent graph must represent obsolete constraints")
    if "supersedes" not in set(inference.get("edge_types") or []):
        errors.append("intent graph must represent supersession")

    primary = data.get("primary_gate") or {}
    if int(primary.get("minimum_independent_analyzers", 0)) < 5:
        errors.append("primary gate must require at least 5 independent analyzers")
    if not REQUIRED_PRIMARY.issubset(set(primary.get("analyzers") or [])):
        errors.append("primary gate is missing one or more required analyzers")

    escalation = data.get("escalation_gate") or {}
    if not REQUIRED_ESCALATION.issubset(set(escalation.get("additional_analyzers") or [])):
        errors.append("escalation gate is missing one or more required analyzers")
    if int(escalation.get("minimum_total_high_impact_analyzers", 0)) < 10:
        errors.append("high-impact goal analysis must preserve at least 10 distinct analyzers")
    require_true(errors, escalation, "guessing_on_high_impact_ambiguity_forbidden", "escalation invariant missing")

    info = data.get("information_gain_routing") or {}
    for key in (
        "enabled",
        "select_next_observation_by_expected_decision_value",
        "prefer_tool_evidence_when_reliable",
        "clarification_allowed_anytime",
        "ask_user_only_when_available_evidence_cannot_resolve_material_ambiguity",
        "never_ask_user_to_repeat_known_information",
        "clarification_question_must_target_highest_value_remaining_ambiguity",
    ):
        require_true(errors, info, key, "information-gain invariant missing")

    research = data.get("research_evidence_mesh") or {}
    if int(research.get("distinct_lane_target", 0)) < 20:
        errors.append("research evidence mesh must target at least 20 materially distinct lanes")
    require_true(errors, research, "do_not_pad_with_duplicate_or_derivative_sources", "research mesh invariant missing")
    if not REQUIRED_RESEARCH_LANES.issubset(set(research.get("lanes") or [])):
        errors.append("research evidence mesh is missing required long-tail/failure lanes")
    rare = research.get("rare_signal_policy") or {}
    require_true(errors, rare, "obscurity_is_not_quality", "rare-signal invariant missing")
    require_true(errors, rare, "prefer_when_it_resolves_contradiction_or_changes_decision", "rare-signal invariant missing")
    require_true(errors, rare, "negative_evidence_required_before_reliability_claim", "rare-signal invariant missing")

    planning = data.get("planning_gate") or {}
    require_true(errors, planning, "detailed_plan_requires_sufficient_goal_convergence", "planning invariant missing")
    require_true(errors, planning, "unmapped_steps_are_non_progress_candidates", "planning invariant missing")

    drift = data.get("drift_control") or {}
    require_true(errors, drift, "goal_signature_required", "drift invariant missing")
    require_true(errors, drift, "intent_belief_graph_recheck_required", "drift invariant missing")
    checkpoints = set(drift.get("checkpoint_triggers") or [])
    for trigger in ("after_user_correction_or_intent_shift", "before_release"):
        if trigger not in checkpoints:
            errors.append(f"drift checkpoint missing: {trigger}")

    anti = data.get("anti_evasion_control") or {}
    for key in (
        "stop_or_block_event_does_not_change_root_goal",
        "controller_hook_or_guard_is_not_promoted_to_task_target",
        "current_blocker_is_recorded_separately_from_root_goal",
        "goal_signature_must_survive_stop_retry_and_recovery",
    ):
        require_true(errors, anti, key, "anti-evasion invariant missing")
    missing_subs = REQUIRED_ANTI_EVASION_SUBSTITUTIONS - set(anti.get("forbidden_progress_substitutions") or [])
    for item in sorted(missing_subs):
        errors.append(f"anti-evasion forbidden substitution missing: {item}")

    on_block = anti.get("on_block") or {}
    if on_block.get("required_next_step") != "highest_value_goal_advancing_action_available_under_current_constraints":
        errors.append("blocked continuation must select the highest-value goal-advancing action")
    for key in (
        "route_pivot_is_preferred_over_goal_pivot",
        "blocker_may_not_become_root_goal",
        "non_progress_actions_do_not_satisfy_stop_or_completion_gates",
    ):
        require_true(errors, on_block, key, "blocked-continuation invariant missing")

    completion = data.get("completion_audit") or {}
    for key in (
        "independent_audit_preferred_when_practical",
        "weighted_acceptance_coverage",
        "hard_requirements_have_veto_power",
        "self_report_only_cannot_pass",
    ):
        require_true(errors, completion, key, "completion audit invariant missing")

    mesh = data.get("evidence_mesh") or {}
    sources = set(mesh.get("default_sources_for_substantive_tasks_when_available") or [])
    if not {"GitHub", "Notion", "Hugging Face"}.issubset(sources):
        errors.append("GitHub, Notion, and Hugging Face must be default evidence sources when available")
    require_true(errors, mesh, "connector_use_must_be_observed_not_assumed", "evidence mesh invariant missing")
    require_true(errors, mesh, "deepen_by_information_gain", "evidence mesh invariant missing")

    capability = data.get("capability_preservation") or {}
    require_true(errors, capability, "requested_reasoning_effort_or_agent_budget_must_not_be_reduced_as_an_evasion_strategy", "capability invariant missing")

    release = data.get("release_gate") or {}
    required_pass = set(release.get("pass_requires") or [])
    for item in (
        "target_identity_evidenced",
        "goal_contract_converged_enough_for_action",
        "final_goal_drift_check_passed",
        "no_stale_constraint_violation",
        "no_controller_evasion_or_headcount_substitution",
    ):
        if item not in required_pass:
            errors.append(f"release gate missing: {item}")

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
