#!/usr/bin/env python3
"""Validate Goal Intelligence v2 integration extensions without replacing the base validator."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    path = root / "control-plane/ai-system/configs/goal-fidelity-global.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    fields = set((data.get("goal_contract") or {}).get("required_fields") or [])
    for field in ("PREFERENCE_PROFILE", "ASSUMPTION_LEDGER"):
        if field not in fields:
            errors.append(f"missing goal field: {field}")

    belief = data.get("intent_belief_graph") or {}
    for key in (
        "required_for_substantive_tasks",
        "inferred_nodes_require_confidence_and_provenance",
        "low_confidence_hidden_intent_may_not_become_hard_requirement",
    ):
        if belief.get(key) is not True:
            errors.append(f"intent belief graph invariant missing: {key}")
    if "obsolete_constraint" not in set(belief.get("node_types") or []):
        errors.append("intent graph must model obsolete_constraint")
    if "supersedes" not in set(belief.get("edge_types") or []):
        errors.append("intent graph must model supersedes")

    delta = data.get("semantic_delta_tracker") or {}
    for key in (
        "required_on_each_substantive_user_turn",
        "superseded_constraints_marked_obsolete",
        "stale_constraints_may_not_silently_survive_intent_shift",
    ):
        if delta.get(key) is not True:
            errors.append(f"semantic delta invariant missing: {key}")

    research = data.get("research_evidence_mesh") or {}
    if int(research.get("distinct_lane_target", 0)) < 20:
        errors.append("research evidence mesh must target >=20 distinct lanes")
    if len(research.get("lanes") or []) < 20:
        errors.append("research evidence mesh must define >=20 distinct lanes")
    if research.get("do_not_pad_with_duplicate_or_derivative_sources") is not True:
        errors.append("research evidence mesh must forbid duplicate padding")
    if research.get("rare_signal_value_requires_decision_discrimination") is not True:
        errors.append("rare evidence must have decision-discrimination value")

    clarify = data.get("clarification_gate") or {}
    for key in ("clarification_allowed_anytime", "never_ask_user_to_repeat_known_information"):
        if clarify.get(key) is not True:
            errors.append(f"clarification invariant missing: {key}")

    sources = set((data.get("evidence_mesh") or {}).get("default_sources_for_substantive_tasks_when_available") or [])
    if not {"GitHub", "Notion", "Hugging Face"}.issubset(sources):
        errors.append("GitHub + Notion + Hugging Face evidence mesh missing")

    metrics = set((data.get("optimization_loop") or {}).get("metrics") or [])
    if "stale_constraint_violation_rate" not in metrics:
        errors.append("optimizer must track stale_constraint_violation_rate")

    required_pass = set((data.get("release_gate") or {}).get("pass_requires") or [])
    if "no_stale_constraint_violation" not in required_pass:
        errors.append("release gate must reject stale-constraint violations")

    provenance = set(data.get("design_provenance") or [])
    if "UserIntentBench_latent_shifting_intent_and_belief_graphs" not in provenance:
        errors.append("UserIntentBench design provenance missing")

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
