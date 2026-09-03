#!/usr/bin/env python3
"""Validate Task Goal Intelligence v3.1 truth-maintenance integration.

This validator is additive: v2.2 and v3 validators remain authoritative for their
protected surfaces. v3.1 must pass them and then prove the new deterministic behavior,
registration, provenance, and non-regression invariants.
"""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_UNCERTAINTY = {
    "specification",
    "target_identity",
    "environment_state",
    "capability",
    "evidence",
    "model",
    "temporal",
}

REQUIRED_CASE_FAMILIES = {
    "correction_cascade",
    "non_binding_example_distractor",
    "field_sensitive_authority",
    "low_authority_retract_rejection",
    "same_value_authority_downgrade_rejection",
    "stronger_same_value_provenance_promotion",
    "stale_summary_suppression",
    "uncertainty_resolver_routing",
    "rare_source_grading",
    "ach_disconfirmation",
    "counterexample_recovery",
    "traceability",
    "metamorphic_invariance",
}

REQUIRED_RELEASE = {
    "v2_base_invariants_preserved",
    "v3_runtime_extension_invariants_preserved",
    "v31_truth_maintenance_is_manifest_registered",
    "v31_auto_invoke_projection_contains_truth_maintenance",
    "behavioral_goal_state_tests_pass",
    "no_source_authority_violation",
    "no_stale_dependent_conclusion",
    "no_orphan_hard_requirement_or_material_action",
    "no_unresolved_failed_acceptance_counterexample",
}

PLUGIN_MARKERS = {
    "Runtime projection revision: `3.0.0`",
    "Integrated truth-maintenance revision: `3.1.0`",
    "Field-sensitive authority",
    "Assumption-based truth maintenance",
    "Structured uncertainty",
    "Anti-loophole / anti-minimization gate",
    "Analysis of Competing Hypotheses",
    "Counterexample-guided refinement",
    "Requirements traceability + metamorphic goal tests",
    "Progress Ledger: effort is not progress",
    "Two consecutive material steps",
    "blocked slice",
    "underground",
    "onion",
    "`LEAD`",
    "first upstream failure",
    "claim → acceptance test → owning evidence → current goal version → causal path",
    "Failure-driven optimization",
}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    config_path = root / "control-plane/ai-system/configs/task-goal-intelligence-v31-truth-maintenance.json"
    v3_path = root / "control-plane/ai-system/configs/task-goal-intelligence-v3-extension.json"
    base_skill_path = root / "skills/skills/task-goal-intelligence/SKILL.md"
    plugin_skill_path = root / "plugins/ai-efficiency-operating-system/skills/task-goal-intelligence/SKILL.md"
    engine_path = root / "control-plane/scripts/task_goal_state_engine.py"
    tests_path = root / "control-plane/tests/test_task_goal_state_engine.py"
    manifest_path = root / "control-plane/ai-system/configs/global-policy-manifest.json"
    kernel_path = root / "docs/GLOBAL_POLICY_KERNEL.md"
    agents_path = root / "AGENTS.md"
    errors: list[str] = []

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        v3 = json.loads(v3_path.read_text(encoding="utf-8"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, ensure_ascii=False))
        return 1

    base_skill = base_skill_path.read_text(encoding="utf-8")
    plugin_skill = plugin_skill_path.read_text(encoding="utf-8")
    engine = engine_path.read_text(encoding="utf-8")
    tests = tests_path.read_text(encoding="utf-8")
    kernel = kernel_path.read_text(encoding="utf-8")
    agents = agents_path.read_text(encoding="utf-8")

    require(config.get("profile_id") == "task-goal-intelligence-v31-truth-maintenance", "wrong v3.1 profile_id", errors)
    require(config.get("revision") == "3.1.0", "wrong v3.1 revision", errors)
    require(config.get("default_enabled") is True, "v3.1 must be default_enabled", errors)
    require(v3.get("profile_id") == "task-goal-intelligence-v3-extension", "v3 extension missing or changed identity", errors)
    require(v3.get("revision") == "3.0.0", "v3 extension revision must remain 3.0.0", errors)
    require("Version: `2.2.0`" in base_skill, "portable v2.2 base contract must remain intact", errors)

    for marker in sorted(PLUGIN_MARKERS):
        if marker.lower() not in plugin_skill.lower():
            errors.append(f"plugin projection marker missing: {marker}")

    authority = config.get("authority_lattice") or {}
    for key in (
        "field_sensitive",
        "summary_is_cache_not_authority",
        "model_inference_is_hypothesis_not_authority",
        "external_retrieval_is_evidence_not_goal_authority",
        "weaker_same_value_signal_cannot_downgrade_authority",
        "retract_or_override_requires_sufficient_field_authority",
        "conflicts_remain_explicit_until_resolved",
    ):
        require(authority.get(key) is True, f"authority invariant missing: {key}", errors)

    routing = config.get("uncertainty_routing") or {}
    require(REQUIRED_UNCERTAINTY.issubset(set(routing.get("required_classes") or [])), "uncertainty classes incomplete", errors)
    require(REQUIRED_UNCERTAINTY.issubset(set((routing.get("resolvers") or {}).keys())), "uncertainty resolvers incomplete", errors)
    require(routing.get("do_not_ask_user_for_tool_resolvable_facts") is True, "tool-resolvable facts should not be pushed to user", errors)
    require(routing.get("do_not_let_tool_facts_own_user_specification") is True, "tool facts must not own user specification", errors)

    truth = config.get("truth_maintenance") or {}
    require(truth.get("enabled") is True, "truth maintenance must be enabled", errors)
    require(truth.get("event_sourced_goal_state_is_preserved") is True, "v3 event-sourced goal state must be preserved", errors)
    require(truth.get("stale_dependent_conclusion_cannot_remain_active") is True, "dependent invalidation invariant missing", errors)
    require("verify_field_authority" in set(truth.get("on_override_or_retract") or []), "override/retract authority check missing", errors)
    require("invalidate_dependent_conclusions" in set(truth.get("on_override_or_retract") or []), "correction cascade missing", errors)

    hypotheses = config.get("competing_hypotheses") or {}
    require(hypotheses.get("disconfirmation_first") is True, "ACH must be disconfirmation-first", errors)
    require(hypotheses.get("strong_contradiction_outweighs_many_weak_confirmations") is True, "strong contradiction rule missing", errors)

    grading = config.get("source_grading") or {}
    require(grading.get("separate_source_reliability_and_information_credibility") is True, "source reliability/credibility must be separate", errors)
    require(grading.get("opaque_v3_lead_state_is_preserved") is True, "v3 opaque LEAD state must be preserved", errors)
    require(grading.get("rare_or_darkweb_unverified_starts_low_authority") is True, "rare-source initial authority rule missing", errors)
    require(grading.get("rare_sources_cannot_directly_mutate_normative_goal") is True, "rare-source normative mutation must be forbidden", errors)
    require(grading.get("derivative_copies_do_not_count_as_independent_corroboration") is True, "evidence laundering guard missing", errors)

    cegar = config.get("counterexample_guided_refinement") or {}
    require(cegar.get("failed_acceptance_test_is_counterexample") is True, "failed acceptance must become counterexample", errors)
    require(cegar.get("counterexample_must_not_weaken_root_goal_by_default") is True, "counterexample must not weaken goal", errors)
    require(cegar.get("first_upstream_failure_analysis_is_preserved") is True, "v3 first-upstream-failure analysis must be preserved", errors)

    trace = config.get("traceability") or {}
    require(trace.get("bidirectional") is True, "traceability must be bidirectional", errors)
    require(trace.get("every_hard_requirement_has_source_id") is True, "hard requirement provenance missing", errors)
    require(trace.get("every_material_action_maps_to_goal_unknown_hypothesis_or_acceptance") is True, "material action traceability missing", errors)
    require(trace.get("completion_reverse_walk_must_bind_current_goal_version") is True, "traceability must bind current goal version", errors)

    metamorphic = config.get("metamorphic_goal_tests") or {}
    require(metamorphic.get("required") is True, "metamorphic tests must be required", errors)
    require(len(metamorphic.get("invariants") or []) >= 6, "too few metamorphic invariants", errors)

    gate = config.get("behavioral_gate") or {}
    require(gate.get("marker_only_validation_is_insufficient") is True, "marker-only validation must be insufficient", errors)
    require(gate.get("offline_deterministic_tests_required") is True, "offline deterministic tests must be required", errors)
    require(int(gate.get("minimum_behavioral_cases", 0)) >= 15, "behavioral case floor too low", errors)
    require(REQUIRED_CASE_FAMILIES.issubset(set(gate.get("required_case_families") or [])), "behavioral case families incomplete", errors)
    require(REQUIRED_RELEASE.issubset(set(config.get("release_gate_additions") or [])), "release additions incomplete", errors)

    policies = {entry.get("id"): entry for entry in manifest.get("canonical_policies") or []}
    require((policies.get("task-goal-intelligence-skill") or {}).get("path") == "skills/skills/task-goal-intelligence/SKILL.md", "portable skill is not manifest-registered", errors)
    require((policies.get("task-goal-intelligence-v3-extension") or {}).get("path") == "control-plane/ai-system/configs/task-goal-intelligence-v3-extension.json", "v3 extension is not manifest-registered", errors)
    require((policies.get("task-goal-intelligence-v31-truth-maintenance") or {}).get("path") == "control-plane/ai-system/configs/task-goal-intelligence-v31-truth-maintenance.json", "v3.1 truth-maintenance is not manifest-registered", errors)
    require((policies.get("task-goal-intelligence-plugin-projection") or {}).get("path") == "plugins/ai-efficiency-operating-system/skills/task-goal-intelligence/SKILL.md", "auto-invoke projection is not manifest-registered", errors)

    require("task-goal-intelligence-v3-extension.json" in kernel, "kernel cannot discover v3 extension", errors)
    require("task-goal-intelligence-v31-truth-maintenance.json" in kernel, "kernel cannot discover v3.1 extension", errors)
    require("skills/skills/task-goal-intelligence/SKILL.md" in kernel, "kernel cannot discover portable goal skill", errors)
    require("docs/GLOBAL_POLICY_KERNEL.md" in agents, "AGENTS does not point to kernel", errors)
    require("control-plane/ai-system/configs/global-policy-manifest.json" in agents, "AGENTS does not point to manifest", errors)

    require("class GoalState" in engine, "GoalState engine missing", errors)
    for marker in ("def apply_signal", "def apply_counterexample", "def traceability_audit", "def rank_hypotheses"):
        require(marker in engine, f"engine behavior missing: {marker}", errors)
    require(tests.count("def test_") >= 15, "fewer than 15 executable behavioral tests", errors)
    for test_marker in (
        "test_low_authority_retract_cannot_remove_current_user_requirement",
        "test_same_value_weaker_signal_cannot_downgrade_active_authority",
        "test_same_value_stronger_factual_readback_promotes_authority_without_breaking_dependents",
    ):
        require(test_marker in tests, f"authority regression missing: {test_marker}", errors)

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
