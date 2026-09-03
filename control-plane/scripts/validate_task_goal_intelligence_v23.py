#!/usr/bin/env python3
"""Validate Task Goal Intelligence v2.3 registration and machine invariants."""

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
    "stale_summary_suppression",
    "uncertainty_resolver_routing",
    "rare_source_grading",
    "ach_disconfirmation",
    "counterexample_recovery",
    "traceability",
    "metamorphic_invariance",
}

REQUIRED_RELEASE = {
    "task_goal_skill_is_manifest_registered",
    "task_goal_skill_is_kernel_discoverable",
    "behavioral_goal_state_tests_pass",
    "no_source_authority_violation",
    "no_stale_dependent_conclusion",
    "no_orphan_hard_requirement_or_material_action",
    "no_unresolved_failed_acceptance_counterexample",
}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    config_path = root / "control-plane/ai-system/configs/task-goal-intelligence-v23.json"
    skill_path = root / "skills/skills/task-goal-intelligence/SKILL.md"
    engine_path = root / "control-plane/scripts/task_goal_state_engine.py"
    tests_path = root / "control-plane/tests/test_task_goal_state_engine.py"
    manifest_path = root / "control-plane/ai-system/configs/global-policy-manifest.json"
    kernel_path = root / "docs/GLOBAL_POLICY_KERNEL.md"
    agents_path = root / "AGENTS.md"
    errors: list[str] = []

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, ensure_ascii=False))
        return 1

    skill = skill_path.read_text(encoding="utf-8")
    engine = engine_path.read_text(encoding="utf-8")
    tests = tests_path.read_text(encoding="utf-8")
    kernel = kernel_path.read_text(encoding="utf-8")
    agents = agents_path.read_text(encoding="utf-8")

    require(config.get("profile_id") == "task-goal-intelligence-v23", "wrong v2.3 profile_id", errors)
    require(config.get("revision") == "2.3.0", "wrong v2.3 revision", errors)
    require(config.get("default_enabled") is True, "v2.3 must be default_enabled", errors)
    require("Version: `2.3.0`" in skill, "canonical skill is not v2.3.0", errors)

    authority = config.get("authority_lattice") or {}
    for key in (
        "field_sensitive",
        "summary_is_cache_not_authority",
        "model_inference_is_hypothesis_not_authority",
        "external_retrieval_is_evidence_not_goal_authority",
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
    require(truth.get("stale_dependent_conclusion_cannot_remain_active") is True, "dependent invalidation invariant missing", errors)
    require("invalidate_dependent_conclusions" in set(truth.get("on_override_or_retract") or []), "correction cascade missing", errors)

    hypotheses = config.get("competing_hypotheses") or {}
    require(hypotheses.get("disconfirmation_first") is True, "ACH must be disconfirmation-first", errors)
    require(hypotheses.get("strong_contradiction_outweighs_many_weak_confirmations") is True, "strong contradiction rule missing", errors)

    grading = config.get("source_grading") or {}
    require(grading.get("separate_source_reliability_and_information_credibility") is True, "source reliability/credibility must be separate", errors)
    require(grading.get("rare_or_darkweb_unverified_starts_low_authority") is True, "rare source initial authority rule missing", errors)
    require(grading.get("rare_sources_cannot_directly_mutate_normative_goal") is True, "rare source normative mutation must be forbidden", errors)
    require(grading.get("derivative_copies_do_not_count_as_independent_corroboration") is True, "evidence laundering guard missing", errors)

    cegar = config.get("counterexample_guided_refinement") or {}
    require(cegar.get("failed_acceptance_test_is_counterexample") is True, "failed acceptance must become counterexample", errors)
    require(cegar.get("counterexample_must_not_weaken_root_goal_by_default") is True, "counterexample must not weaken goal", errors)

    trace = config.get("traceability") or {}
    require(trace.get("bidirectional") is True, "traceability must be bidirectional", errors)
    require(trace.get("every_hard_requirement_has_source_id") is True, "hard requirement provenance missing", errors)
    require(trace.get("every_material_action_maps_to_goal_unknown_hypothesis_or_acceptance") is True, "material action traceability missing", errors)

    metamorphic = config.get("metamorphic_goal_tests") or {}
    require(metamorphic.get("required") is True, "metamorphic tests must be required", errors)
    require(len(metamorphic.get("invariants") or []) >= 5, "too few metamorphic invariants", errors)

    gate = config.get("behavioral_gate") or {}
    require(gate.get("marker_only_validation_is_insufficient") is True, "marker-only validation must be insufficient", errors)
    require(gate.get("offline_deterministic_tests_required") is True, "offline deterministic tests must be required", errors)
    require(int(gate.get("minimum_behavioral_cases", 0)) >= 10, "behavioral case floor too low", errors)
    require(REQUIRED_CASE_FAMILIES.issubset(set(gate.get("required_case_families") or [])), "behavioral case families incomplete", errors)
    require(REQUIRED_RELEASE.issubset(set(config.get("release_gate_additions") or [])), "release additions incomplete", errors)

    # Registration/loadability: an existing file is not enough. AGENTS may discover the
    # skill transitively through the kernel+manifest to preserve progressive disclosure.
    policies = {entry.get("id"): entry for entry in manifest.get("canonical_policies") or []}
    skill_entry = policies.get("task-goal-intelligence-skill") or {}
    machine_entry = policies.get("task-goal-intelligence-v23-machine") or {}
    require(skill_entry.get("path") == "skills/skills/task-goal-intelligence/SKILL.md", "skill is not registered in manifest", errors)
    require(machine_entry.get("path") == "control-plane/ai-system/configs/task-goal-intelligence-v23.json", "v2.3 machine config is not registered in manifest", errors)
    require("skills/skills/task-goal-intelligence/SKILL.md" in kernel, "kernel cannot discover task-goal skill", errors)
    require("docs/GLOBAL_POLICY_KERNEL.md" in agents, "AGENTS does not point to the global policy kernel", errors)
    require("control-plane/ai-system/configs/global-policy-manifest.json" in agents, "AGENTS does not point to the global policy manifest", errors)

    # Executable behavior, not just prose markers.
    require("class GoalState" in engine, "GoalState engine missing", errors)
    require("def apply_signal" in engine, "state transition function missing", errors)
    require("def apply_counterexample" in engine, "counterexample refinement function missing", errors)
    require("def traceability_audit" in engine, "traceability audit missing", errors)
    require("def rank_hypotheses" in engine, "ACH ranking function missing", errors)
    require(tests.count("def test_") >= 10, "fewer than 10 executable behavioral tests", errors)

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
