#!/usr/bin/env python3
"""Validate Task Goal Intelligence v3 extension and adversarial regression corpus."""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_PLUGIN_MARKERS = {
    "Runtime projection revision: `3.0.0`",
    "Event-sourced goal state",
    "Historical-claim invalidation",
    "Anti-loophole / anti-minimization gate",
    "nearest easier task",
    "blocked slice",
    "Goal Capsule recitation",
    "Progress Ledger: effort is not progress",
    "Two consecutive material steps",
    "High-scale + rare-signal evidence mesh",
    "underground",
    "onion",
    "`LEAD`",
    "first upstream failure",
    "claim → acceptance test → owning evidence → current goal version → causal path",
    "Failure-driven optimization",
}

REQUIRED_CONFIG_SECTIONS = {
    "event_sourced_goal_state",
    "historical_claim_revalidation",
    "anti_loophole_semantic_minimization",
    "blocked_slice_isolation",
    "goal_capsule_recitation",
    "progress_ledger",
    "planning_utility_intent_ir",
    "opaque_source_provenance",
    "end_to_end_evaluation",
    "failure_driven_optimization",
}

REQUIRED_CASE_CLASSES = {
    "historical_claim_revalidation",
    "wording_loophole_minimization",
    "neighboring_task_substitution",
    "correction_interrupt",
    "blocked_slice_isolation",
    "process_discussion_substitution",
    "progress_theater",
    "goal_capsule_drift",
    "planning_utility_ambiguity",
    "shared_reversible_next_action",
    "opaque_source_provenance",
    "rare_evidence_contradiction",
    "first_upstream_failure",
    "method_vs_end_state",
    "false_impossibility_from_route_failure",
    "real_correction_to_eval",
    "aggregate_score_masking",
    "current_evidence_over_stale_summary",
    "high_scale_plus_high_discrimination",
    "completion_reverse_walk",
}

REQUIRED_SOURCE_IDS = {
    "recap-eacl-2026",
    "hamel-shankar-agent-evals",
    "hamel-shankar-error-analysis",
    "dspy-gepa",
    "manus-context-engineering",
    "magentic-one",
    "opencti",
    "misp",
}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {lineno}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"JSONL row {lineno} must be an object")
        rows.append(row)
    return rows


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    plugin_skill_path = root / "plugins/ai-efficiency-operating-system/skills/task-goal-intelligence/SKILL.md"
    base_skill_path = root / "skills/skills/task-goal-intelligence/SKILL.md"
    config_path = root / "control-plane/ai-system/configs/task-goal-intelligence-v3-extension.json"
    sources_path = root / "control-plane/ai-system/configs/task-goal-intelligence-v3-sources.json"
    cases_path = root / "control-plane/tests/task_goal_intelligence_v3_cases.jsonl"

    errors: list[str] = []

    for path in (plugin_skill_path, base_skill_path, config_path, sources_path, cases_path):
        if not path.exists():
            errors.append(f"missing required path: {path.relative_to(root)}")
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, ensure_ascii=False, sort_keys=True))
        return 1

    plugin_skill = plugin_skill_path.read_text(encoding="utf-8")
    base_skill = base_skill_path.read_text(encoding="utf-8")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    source_ledger = json.loads(sources_path.read_text(encoding="utf-8"))

    for marker in sorted(REQUIRED_PLUGIN_MARKERS):
        if marker.lower() not in plugin_skill.lower():
            errors.append(f"plugin skill marker missing: {marker}")

    # v3 is an extension, not a rewrite that may silently discard the current canonical v2.2 contract.
    for base_marker in (
        "Version: `2.2.0`",
        "Intent Belief Graph",
        "Interpretation Tournament",
        "Contrastive Consistency Probe",
        "Semantic Delta, Correction Interrupt, and Stale-Constraint Suppression",
        "Anti-Neighbor-Task Gate",
        "Completion Audit",
    ):
        if base_marker.lower() not in base_skill.lower():
            errors.append(f"canonical v2.2 regression: missing base marker {base_marker}")

    if config.get("revision") != "3.0.0":
        errors.append("v3 extension revision must be 3.0.0")
    for section in sorted(REQUIRED_CONFIG_SECTIONS):
        if section not in config:
            errors.append(f"v3 config section missing: {section}")

    hist = config.get("historical_claim_revalidation") or {}
    if hist.get("prior_prose_is_not_current_evidence") is not True:
        errors.append("historical prior prose must not count as current evidence")
    if hist.get("fresh_owning_system_readback_outranks_historical_claim") is not True:
        errors.append("fresh owning-system read-back must outrank historical claims")

    anti = config.get("anti_loophole_semantic_minimization") or {}
    for key in (
        "do_not_reduce_end_state_from_imperfect_wording",
        "nearest_easier_task_probe_required_before_material_scope_reduction",
        "route_convenience_cannot_lower_scope_capability_verification_or_acceptance",
        "blocked_route_does_not_prove_task_impossible",
    ):
        if anti.get(key) is not True:
            errors.append(f"anti-minimization invariant missing: {key}")

    blocked = config.get("blocked_slice_isolation") or {}
    if blocked.get("continue_all_separable_goal_advancing_work") is not True:
        errors.append("blocked-slice isolation must continue separable goal-advancing work")
    if blocked.get("route_pivot_preferred_over_goal_pivot") is not True:
        errors.append("blocked-slice isolation must prefer route pivot over goal pivot")

    progress = config.get("progress_ledger") or {}
    if progress.get("two_consecutive_no_delta_steps_force_causal_pivot") is not True:
        errors.append("progress ledger must force a causal pivot after two no-delta material steps")
    non_progress = set(progress.get("non_progress_examples") or [])
    for item in ("tool_count", "agent_count", "file_exists_only", "pr_exists_only", "compliance_prose"):
        if item not in non_progress:
            errors.append(f"progress theater class missing: {item}")

    opaque = config.get("opaque_source_provenance") or {}
    if opaque.get("initial_state") != "LEAD":
        errors.append("opaque/anonymous evidence must start as LEAD")
    if opaque.get("rarity_or_anonymity_is_not_credibility") is not True:
        errors.append("opaque-source contract must reject rarity/anonymity as credibility")
    if "OWNING_SOURCE_VERIFIED" not in set(opaque.get("promotion_states") or []):
        errors.append("opaque-source promotion chain must include OWNING_SOURCE_VERIFIED")

    e2e = config.get("end_to_end_evaluation") or {}
    if e2e.get("black_box_goal_success_precedes_step_scoring") is not True:
        errors.append("end-to-end user-goal success must precede step-level scoring")
    if e2e.get("first_upstream_failure_required_on_failure") is not True:
        errors.append("failure analysis must record first upstream failure")

    optimize = config.get("failure_driven_optimization") or {}
    if optimize.get("error_taxonomy_before_new_rules") is not True:
        errors.append("error taxonomy must precede more rule accretion")
    if optimize.get("aggregate_gain_cannot_hide_hard_slice_regression") is not True:
        errors.append("aggregate optimizer gain must not hide protected-slice regression")

    try:
        cases = load_jsonl(cases_path)
    except ValueError as exc:
        errors.append(str(exc))
        cases = []

    if len(cases) < 20:
        errors.append(f"expected >=20 adversarial cases, found {len(cases)}")

    ids: set[str] = set()
    classes: set[str] = set()
    fingerprints: set[tuple[str, str]] = set()
    for idx, case in enumerate(cases, start=1):
        for field in ("id", "class", "input_signal", "goal_delta", "expected", "forbidden"):
            if field not in case:
                errors.append(f"case {idx} missing field: {field}")
        case_id = str(case.get("id", ""))
        if case_id in ids:
            errors.append(f"duplicate case id: {case_id}")
        ids.add(case_id)
        case_class = str(case.get("class", ""))
        classes.add(case_class)
        expected = case.get("expected") or []
        forbidden = case.get("forbidden") or []
        if not isinstance(expected, list) or len(expected) < 2:
            errors.append(f"case {case_id} must have >=2 expected behaviors")
        if not isinstance(forbidden, list) or len(forbidden) < 1:
            errors.append(f"case {case_id} must have >=1 forbidden behavior")
        fp = (case_class, str(case.get("input_signal", "")).strip().lower())
        if fp in fingerprints:
            errors.append(f"duplicate semantic test fingerprint: {case_id}")
        fingerprints.add(fp)

    missing_classes = sorted(REQUIRED_CASE_CLASSES - classes)
    if missing_classes:
        errors.append(f"missing required adversarial classes: {missing_classes}")

    sources = source_ledger.get("sources") or []
    source_ids = {str(item.get("id", "")) for item in sources if isinstance(item, dict)}
    missing_sources = sorted(REQUIRED_SOURCE_IDS - source_ids)
    if missing_sources:
        errors.append(f"missing v3 provenance sources: {missing_sources}")
    for item in sources:
        if not isinstance(item, dict):
            errors.append("source ledger entries must be objects")
            continue
        for field in ("id", "class", "title", "url", "adopted_mechanism", "limitations"):
            if not item.get(field):
                errors.append(f"source {item.get('id', '<unknown>')} missing {field}")
        if item.get("url") and not str(item["url"]).startswith("https://"):
            errors.append(f"source {item.get('id')} must use an https URL")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "case_count": len(cases),
        "case_classes": len(classes),
        "source_count": len(sources),
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
