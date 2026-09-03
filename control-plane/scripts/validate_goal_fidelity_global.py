#!/usr/bin/env python3
"""Validate the v2 goal-fidelity and task-goal-understanding machine contract."""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_GOAL_FIELDS = {
    "ROOT_GOAL",
    "DESIRED_END_STATE",
    "HARD_CONSTRAINTS",
    "NEGATIONS",
    "PROTECTED_CAPABILITIES",
    "TARGET_IDENTITY",
    "ACCEPTANCE_TESTS",
    "UNDERLYING_PURPOSE",
    "DECISION_CRITICAL_UNKNOWNS",
    "INTERPRETATION_SET",
    "ACTION_DIVERGENCE_MAP",
    "SOURCE_PRIORITY",
    "COMPLETION_EVIDENCE_PLAN",
    "GOAL_SIGNATURE",
}

REQUIRED_PRIMARY = {
    "literal_intent",
    "purpose_value",
    "environment_entity_identity",
    "acceptance_evidence_backward",
    "reverse_failure",
    "counterfactual",
    "exclusion",
    "dependency_path",
    "historical_correction",
    "cross_source_contradiction",
}

REQUIRED_ESCALATION = {
    "counterfactual",
    "exclusion",
    "dependency_path",
    "cross_source_consistency",
    "purpose_value",
}

REQUIRED_CANDIDATE_FIELDS = {
    "candidate_root_goal",
    "supporting_evidence",
    "disconfirming_evidence",
    "required_assumptions",
    "action_if_true",
    "consequence_if_wrong",
    "predicted_user_correction_if_wrong",
    "confidence",
}

REQUIRED_OPTIMIZATION_METRICS = {
    "root_goal_accuracy",
    "hard_constraint_recall",
    "negation_recall",
    "target_identity_precision",
    "underlying_purpose_fidelity",
    "clarification_information_gain",
    "acceptance_test_coverage",
    "semantic_drift_rate",
    "false_completion_rate",
    "protected_capability_regression_rate",
}

REQUIRED_ANTI_EVASION_SUBSTITUTIONS = {
    "inspect_exploit_bypass_kill_or_weaken_controller_to_escape_work",
    "game_string_checks_or_completion_detectors",
    "satisfy_agent_headcount_without_unique_goal_advancing_contribution",
    "substitute_refusal_policy_or_ethics_debate_for_allowed_task_progress",
    "fabricate_runtime_independence_execution_or_completion",
    "reduce_required_effort_agent_count_tests_or_acceptance_criteria_to_escape_a_blocker",
}


def require_true(section: dict, key: str, errors: list[str], label: str) -> None:
    if section.get(key) is not True:
        errors.append(f"{label} missing/false: {key}")


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
        errors.append("schema_version must remain 1 for compatibility")
    if data.get("profile_id") != "goal-fidelity-task-understanding-v2":
        errors.append("profile_id must be goal-fidelity-task-understanding-v2")
    if data.get("revision") != "2.0":
        errors.append("revision must be 2.0")
    if data.get("default_enabled") is not True:
        errors.append("default_enabled must be true")

    contract = data.get("goal_contract") or {}
    missing_goal_fields = REQUIRED_GOAL_FIELDS - set(contract.get("required_fields") or [])
    for field in sorted(missing_goal_fields):
        errors.append(f"missing goal contract field: {field}")
    require_true(contract, "silent_goal_mutation_forbidden", errors, "goal contract")
    require_true(contract, "fluent_paraphrase_is_not_proof_of_understanding", errors, "goal contract")

    harvest = data.get("signal_harvest") or {}
    if len(harvest.get("required_signal_classes") or []) < 10:
        errors.append("signal harvest must include at least 10 materially different signal classes")
    require_true(harvest, "recent_context_is_evidence_not_authority", errors, "signal harvest")
    require_true(harvest, "fresh_direct_evidence_overrides_stale_summary", errors, "signal harvest")

    tournament = data.get("interpretation_tournament") or {}
    require_true(tournament, "enabled_for_substantive_or_ambiguous_tasks", errors, "interpretation tournament")
    count = tournament.get("preferred_candidate_count") or {}
    if int(count.get("min", 0)) < 3 or int(count.get("max", 0)) < int(count.get("min", 0)):
        errors.append("interpretation tournament must prefer at least 3 candidates when ambiguity is real")
    missing_candidate_fields = REQUIRED_CANDIDATE_FIELDS - set(tournament.get("candidate_required_fields") or [])
    for field in sorted(missing_candidate_fields):
        errors.append(f"interpretation candidate missing field: {field}")
    require_true(tournament, "independence_requires_consequential_difference", errors, "interpretation tournament")
    require_true(tournament, "same_reversible_next_action_allows_progress_without_question", errors, "interpretation tournament")
    require_true(tournament, "high_impact_action_divergence_becomes_decision_critical_unknown", errors, "interpretation tournament")

    clarification = data.get("clarification_gate") or {}
    if clarification.get("principle") != "maximize_information_gain_per_user_interruption":
        errors.append("clarification gate must optimize information gain per user interruption")
    if len(clarification.get("ask_only_if_all") or []) < 4:
        errors.append("clarification gate must require all four material conditions")
    require_true(clarification, "prefer_tool_or_runtime_evidence_before_user_question", errors, "clarification gate")
    require_true(clarification, "prefer_one_discriminating_question_over_many_low_value_questions", errors, "clarification gate")
    require_true(clarification, "needless_clarification_for_shared_next_action_forbidden", errors, "clarification gate")

    split = data.get("architect_executor_evaluator") or {}
    require_true(split, "separation_required_for_complex_tasks", errors, "architect-executor-evaluator")
    require_true(split, "executor_may_not_silently_change_protected_goal_fields", errors, "architect-executor-evaluator")
    require_true(split, "evaluator_receives_original_goal_contract_and_raw_evidence", errors, "architect-executor-evaluator")
    require_true(split, "role_labels_do_not_prove_runtime_independence", errors, "architect-executor-evaluator")

    primary = data.get("primary_gate") or {}
    if int(primary.get("minimum_independent_analyzers", 0)) < 5:
        errors.append("primary gate must require at least 5 independent analyzers")
    missing_primary = REQUIRED_PRIMARY - set(primary.get("analyzers") or [])
    for item in sorted(missing_primary):
        errors.append(f"primary gate missing analyzer: {item}")
    require_true(primary, "cosmetic_rewording_does_not_count_as_independence", errors, "primary gate")

    escalation = data.get("escalation_gate") or {}
    missing_escalation = REQUIRED_ESCALATION - set(escalation.get("additional_analyzers") or [])
    for item in sorted(missing_escalation):
        errors.append(f"escalation gate missing analyzer: {item}")
    require_true(escalation, "guessing_on_high_impact_ambiguity_forbidden", errors, "escalation gate")

    diff = data.get("semantic_goal_diff") or {}
    require_true(diff, "goal_signature_required", errors, "semantic goal diff")
    if "before_release" not in set(diff.get("checkpoint_triggers") or []):
        errors.append("semantic goal diff requires before_release checkpoint")
    required_diff_checks = {
        "root_goal_unchanged_without_evidence",
        "negation_not_became_deliverable",
        "protected_capability_not_traded_away",
        "target_identity_not_shifted",
        "proxy_not_replacing_end_state",
        "acceptance_tests_still_valid",
        "blocker_or_side_problem_not_promoted_to_task",
    }
    missing_diff = required_diff_checks - set(diff.get("required_checks") or [])
    for item in sorted(missing_diff):
        errors.append(f"semantic goal diff missing check: {item}")

    anti = data.get("anti_evasion_control") or {}
    for key in (
        "stop_or_block_event_does_not_change_root_goal",
        "controller_hook_or_guard_is_not_promoted_to_task_target",
        "current_blocker_is_recorded_separately_from_root_goal",
        "goal_signature_must_survive_stop_retry_and_recovery",
    ):
        require_true(anti, key, errors, "anti-evasion")

    substitutions = set(anti.get("forbidden_progress_substitutions") or [])
    for item in sorted(REQUIRED_ANTI_EVASION_SUBSTITUTIONS - substitutions):
        errors.append(f"anti-evasion forbidden substitution missing: {item}")

    on_block = anti.get("on_block") or {}
    if on_block.get("required_next_step") != "highest_value_goal_advancing_action_available_under_current_constraints":
        errors.append("blocked continuation must choose highest-value goal-advancing action")
    for key in (
        "route_pivot_is_preferred_over_goal_pivot",
        "blocker_may_not_become_root_goal",
        "non_progress_actions_do_not_satisfy_stop_or_completion_gates",
    ):
        require_true(on_block, key, errors, "blocked continuation")

    contribution = anti.get("multi_agent_contribution_gate") or {}
    for key in (
        "headcount_alone_never_satisfies_requirement",
        "each_activated_agent_requires_distinct_role",
        "each_activated_agent_requires_unique_evidence_test_artifact_or_implementation_contribution",
        "contribution_must_map_to_goal_contract_or_acceptance_test",
        "policy_only_or_refusal_only_agent_does_not_count_unless_policy_analysis_is_the_user_task",
        "runtime_independence_must_be_observed_before_claimed",
    ):
        require_true(contribution, key, errors, "multi-agent contribution")

    mesh = data.get("evidence_mesh") or {}
    if not {"GitHub", "Notion"}.issubset(set(mesh.get("default_sources_for_substantive_tasks_when_available") or [])):
        errors.append("GitHub and Notion must remain default evidence sources when available")
    if len(mesh.get("practical_source_priority") or []) < 7:
        errors.append("practical evidence hierarchy must contain the high-signal third-party source classes")
    require_true(mesh, "official_docs_are_not_sole_basis_for_practical_superiority", errors, "evidence mesh")
    require_true(mesh, "popularity_is_scale_signal_not_quality_proof", errors, "evidence mesh")
    require_true(mesh, "connector_use_must_be_observed_not_assumed", errors, "evidence mesh")

    rare = data.get("rare_signal_discovery") or {}
    require_true(rare, "enabled_when_research_heavy_and_decision_relevant", errors, "rare-signal discovery")
    if len(rare.get("lanes") or []) < 8:
        errors.append("rare-signal discovery must include at least 8 distinct discovery lanes")
    require_true(rare, "hidden_or_rare_does_not_imply_credible", errors, "rare-signal discovery")
    require_true(rare, "quality_gate_applies_to_novelty_lane", errors, "rare-signal discovery")

    optimization = data.get("optimization_loop") or {}
    require_true(optimization, "goal_understanding_is_evaluable_and_optimizable", errors, "optimization loop")
    missing_metrics = REQUIRED_OPTIMIZATION_METRICS - set(optimization.get("metrics") or [])
    for item in sorted(missing_metrics):
        errors.append(f"optimization metric missing: {item}")
    patterns = set(optimization.get("candidate_optimization_patterns") or [])
    for family in ("GEPA_reflective_trajectory_optimization", "MIPROv2_data_aware_instruction_and_demo_optimization", "TextGrad_textual_feedback_optimization_experimental"):
        if family not in patterns:
            errors.append(f"optimization pattern missing: {family}")
    require_true(optimization, "promotion_requires_holdout_improvement", errors, "optimization loop")
    require_true(optimization, "promotion_forbidden_if_protected_metric_regresses", errors, "optimization loop")
    require_true(optimization, "manual_rule_accretion_is_not_default_when_eval_data_exists", errors, "optimization loop")

    adversarial = data.get("adversarial_misread_test") or {}
    require_true(adversarial, "required_for_high_impact_release", errors, "adversarial misread test")
    if len(adversarial.get("attack_classes") or []) < 8:
        errors.append("adversarial misread test must cover at least 8 failure classes")
    require_true(adversarial, "criticism_counts_only_with_concrete_contradiction_missing_evidence_or_discriminating_test", errors, "adversarial misread test")

    anti_sycophancy = data.get("anti_sycophancy") or {}
    for key in (
        "leading_user_assumption_is_not_automatically_causal_truth",
        "preserve_desired_end_state_when_correcting_wrong_causal_model",
        "evidence_beats_agreement_on_intermediate_assumptions",
    ):
        require_true(anti_sycophancy, key, errors, "anti-sycophancy")

    capability = data.get("capability_preservation") or {}
    require_true(capability, "requested_reasoning_effort_or_agent_budget_must_not_be_reduced_as_an_evasion_strategy", errors, "capability preservation")
    require_true(capability, "protected_capability_regression_blocks_pass", errors, "capability preservation")

    release = data.get("release_gate") or {}
    required_pass = set(release.get("pass_requires") or [])
    for item in (
        "winning_interpretation_evidence_sufficient_for_task_impact",
        "decision_critical_ambiguity_resolved_or_explicitly_blocked",
        "target_identity_evidenced",
        "final_semantic_goal_diff_passed",
        "actual_readback_or_test_evidence",
        "no_neighboring_task_or_proxy_substitution",
    ):
        if item not in required_pass:
            errors.append(f"release gate missing: {item}")

    provenance = set(data.get("design_provenance") or [])
    for item in (
        "Aider_architect_editor_separation",
        "DSPy_MIPROv2_and_GEPA_optimization",
        "TextGrad_textual_feedback_optimization",
        "Promptfoo_adversarial_and_regression_evaluation",
    ):
        if item not in provenance:
            errors.append(f"design provenance missing: {item}")

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
