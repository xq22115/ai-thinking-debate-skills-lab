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

    mesh = data.get("evidence_mesh") or {}
    sources = set(mesh.get("default_sources_for_substantive_tasks_when_available") or [])
    if not {"GitHub", "Notion"}.issubset(sources):
        errors.append("GitHub and Notion must be default evidence sources when available")
    if mesh.get("connector_use_must_be_observed_not_assumed") is not True:
        errors.append("connector use must be observed, not assumed")

    release = data.get("release_gate") or {}
    required_pass = set(release.get("pass_requires") or [])
    for item in ("target_identity_evidenced", "final_goal_drift_check_passed"):
        if item not in required_pass:
            errors.append(f"release gate missing: {item}")

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
