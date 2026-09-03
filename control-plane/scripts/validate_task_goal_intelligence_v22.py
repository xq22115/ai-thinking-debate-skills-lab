#!/usr/bin/env python3
"""Validate Task Goal Intelligence v2.2 invariants, including compatible v2.3 supersets."""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_SKILL_MARKERS = {
    "Contrastive Consistency Probe",
    "NET_INFORMATION_VALUE",
    "P_CHANGE",
    "IMPACT_IF_WRONG",
    "EVIDENCE_GAIN",
    "FRESHNESS",
    "INDEPENDENCE",
    "TOTAL_COST",
    "`ADD`",
    "`UPDATE`",
    "`OVERRIDE`",
    "`RETRACT`",
    "`EXAMPLE`",
    "`DISTRACTOR`",
    "Semantic-Neighbor Expansion",
    "Value / Expected Value of Information",
    "structured uncertainty",
    "specification mining",
    "Anti-Neighbor-Task Gate",
    "invalidat",
    "owning-system read-back",
}

REQUIRED_NEIGHBOR_SUBSTITUTIONS = {
    "explaining how to change something instead of changing it",
    "installing/configuring a tool instead of proving it is invokable and useful",
    "finding a repository instead of reproducing the requested capability",
    "returning more sources instead of resolving the decision",
    "creating an artifact instead of verifying the requested effect in the owning system",
}

REQUIRED_CONFIG_SECTIONS = {
    "interpretation_tournament",
    "clarification_gate",
    "rare_signal_discovery",
    "intent_belief_graph",
    "semantic_delta_tracker",
    "research_evidence_mesh",
    "release_gate",
}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    skill_path = root / "skills/skills/task-goal-intelligence/SKILL.md"
    config_path = root / "control-plane/ai-system/configs/goal-fidelity-global.json"
    errors: list[str] = []

    skill = skill_path.read_text(encoding="utf-8")
    config = json.loads(config_path.read_text(encoding="utf-8"))

    if not any(version in skill for version in ("Version: `2.2.0`", "Version: `2.3.0`")):
        errors.append("skill version must preserve v2.2 invariants or be the v2.3 compatible superset")

    for marker in sorted(REQUIRED_SKILL_MARKERS):
        if marker.lower() not in skill.lower():
            errors.append(f"skill marker missing: {marker}")

    for marker in sorted(REQUIRED_NEIGHBOR_SUBSTITUTIONS):
        if marker.lower() not in skill.lower():
            errors.append(f"anti-neighbor substitution missing: {marker}")

    for section in sorted(REQUIRED_CONFIG_SECTIONS):
        if section not in config:
            errors.append(f"canonical goal config section missing: {section}")

    tournament = config.get("interpretation_tournament") or {}
    if tournament.get("same_reversible_next_action_allows_progress_without_question") is not True:
        errors.append("canonical config must allow progress when candidates share the same reversible next action")
    if tournament.get("high_impact_action_divergence_becomes_decision_critical_unknown") is not True:
        errors.append("canonical config must promote material action divergence to a decision-critical unknown")

    clarification = config.get("clarification_gate") or {}
    if clarification.get("prefer_tool_or_runtime_evidence_before_user_question") is not True:
        errors.append("canonical config must prefer tool/runtime evidence before user interruption")
    if clarification.get("never_ask_user_to_repeat_known_information") is not True:
        errors.append("canonical config must forbid asking the user to repeat known information")

    belief = config.get("intent_belief_graph") or {}
    if belief.get("low_confidence_hidden_intent_may_not_become_hard_requirement") is not True:
        errors.append("low-confidence latent intent must not become a hard requirement")

    delta = config.get("semantic_delta_tracker") or {}
    if delta.get("superseded_constraints_marked_obsolete") is not True:
        errors.append("superseded constraints must be marked obsolete")
    if delta.get("stale_constraints_may_not_silently_survive_intent_shift") is not True:
        errors.append("stale constraints must not survive intent shifts")

    research = config.get("research_evidence_mesh") or {}
    if int(research.get("distinct_lane_target", 0)) < 20:
        errors.append("canonical research evidence mesh must retain >=20 distinct lanes")
    if research.get("do_not_pad_with_duplicate_or_derivative_sources") is not True:
        errors.append("research evidence mesh must forbid duplicate padding")

    release = set((config.get("release_gate") or {}).get("pass_requires") or [])
    for required in ("no_neighboring_task_or_proxy_substitution", "no_stale_constraint_violation", "actual_readback_or_test_evidence"):
        if required not in release:
            errors.append(f"release gate missing: {required}")

    # The v2.2 evidence hierarchy remains a protected compatibility surface in v2.3.
    for phrase in (
        "world-class third-party practitioners",
        "Official/canonical material",
        "Popularity is a scale signal, not proof",
        "opposite hypothesis",
        "rare/high-discrimination/semantic-neighbor",
    ):
        if phrase.lower() not in skill.lower():
            errors.append(f"practical evidence/search invariant missing: {phrase}")

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
