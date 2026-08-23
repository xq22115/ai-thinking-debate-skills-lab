#!/usr/bin/env python3
"""Validate repository-wide Continuous Thinking Quality v3 invariants.

This is intentionally small and dependency-free so CI can fail closed when the
machine-readable quality profile or its repository entry points drift.
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "control-plane/ai-system/configs/continuous-thinking-global.json"
AGENTS_PATH = REPO_ROOT / "AGENTS.md"
CANONICAL_DOC_PATH = REPO_ROOT / "docs/CONTINUOUS_THINKING_QUALITY_OS.md"


def _load_json(path: pathlib.Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected_object:{path}")
    return value


def _require(condition: bool, code: str, failures: list[str]) -> None:
    if not condition:
        failures.append(code)


def validate() -> list[str]:
    failures: list[str] = []
    for path, code in [
        (CONFIG_PATH, "config_missing"),
        (AGENTS_PATH, "root_agents_missing"),
        (CANONICAL_DOC_PATH, "canonical_doc_missing"),
    ]:
        if not path.is_file():
            failures.append(code)
    if failures:
        return failures

    try:
        config = _load_json(CONFIG_PATH)
    except Exception as exc:
        return [f"config_invalid:{type(exc).__name__}:{exc}"]

    _require(config.get("schema_version") == 1, "schema_version_mismatch", failures)
    _require(config.get("scope") == "repository-wide", "scope_not_repository_wide", failures)
    _require(config.get("default_enabled") is True, "profile_not_default_enabled", failures)

    anti_instant = config.get("anti_instant_response") or {}
    _require(
        anti_instant.get("material_or_critical_must_not_release_first_plausible_answer") is True,
        "first_plausible_answer_not_blocked",
        failures,
    )
    _require(
        anti_instant.get("elapsed_time_is_not_evidence") is True,
        "elapsed_time_misused_as_evidence",
        failures,
    )

    acceptance = config.get("acceptance_contract") or {}
    _require(
        acceptance.get("criterion_default_state") == "UNSATISFIED",
        "acceptance_default_not_fail_closed",
        failures,
    )
    _require(
        acceptance.get("pass_requires_all_hard_criteria_satisfied") is True,
        "partial_acceptance_can_pass",
        failures,
    )
    _require(
        acceptance.get("self_report_only_evidence_forbidden") is True,
        "self_report_only_evidence_allowed",
        failures,
    )
    _require(
        acceptance.get("direct_contradiction_overrides_pass") is True,
        "contradiction_does_not_override_pass",
        failures,
    )

    research = config.get("research_and_experience") or {}
    internalization = set(research.get("experience_internalization_fields") or [])
    required_internalization = {
        "mechanism", "preconditions", "failure_modes", "verification",
        "portable_lesson", "invalidation_condition",
    }
    _require(
        required_internalization.issubset(internalization),
        "experience_internalization_incomplete",
        failures,
    )
    _require(research.get("fixed_source_quota_forbidden") is True, "fixed_source_quota_allowed", failures)
    _require(research.get("stop_when_decision_saturated") is True, "research_stop_rule_missing", failures)

    routes = config.get("multi_path_reasoning") or {}
    _require(routes.get("route_aliases_do_not_count_as_diversity") is True, "alias_diversity_allowed", failures)
    _require(routes.get("first_plausible_route_lock_in_forbidden") is True, "first_route_lock_in_allowed", failures)

    stagnation = config.get("stagnation_control") or {}
    _require(stagnation.get("materially_similar_failure_limit") == 2, "two_strike_pivot_missing", failures)
    _require(stagnation.get("next_attempt_must_change_major_dimension") is True, "pivot_not_enforced", failures)
    _require(stagnation.get("retry_without_information_gain_forbidden") is True, "stagnant_retry_allowed", failures)

    continuity = config.get("continuity") or {}
    _require(continuity.get("externalize_state_for_long_tasks") is True, "long_task_state_not_externalized", failures)
    _require(continuity.get("fresh_context_reset_when_context_quality_degrades") is True, "fresh_context_reset_missing", failures)

    evaluation = config.get("evaluation") or {}
    _require(
        evaluation.get("builder_may_not_be_sole_final_evaluator_for_material_or_critical_work") is True,
        "builder_self_evaluation_sufficient",
        failures,
    )
    _require(evaluation.get("fresh_context_evaluator_preferred") is True, "fresh_context_evaluator_missing", failures)
    _require(evaluation.get("evaluate_against_predeclared_contract") is True, "predeclared_contract_not_required", failures)

    verification = config.get("verification") or {}
    ladder = verification.get("ladder") or []
    _require(bool(ladder) and ladder[0] == "runtime_or_user_path", "runtime_not_top_verification_level", failures)
    _require(verification.get("use_highest_practical_level") is True, "highest_practical_verification_not_required", failures)
    _require(
        verification.get("configuration_presence_does_not_prove_runtime_effect") is True,
        "config_presence_can_fake_runtime",
        failures,
    )

    release = config.get("release") or {}
    pass_requires = set(release.get("pass_requires") or [])
    required_release = {
        "all hard acceptance criteria satisfied",
        "no unresolved high-impact unknowns",
        "no direct contradictory evidence",
        "required verification executed",
        "protected capabilities not degraded",
        "fresh state confirmed",
    }
    _require(required_release.issubset(pass_requires), "release_gate_incomplete", failures)
    _require(release.get("not_run_must_never_be_relabelled_pass") is True, "not_run_can_pass", failures)
    _require(release.get("continue_same_task_until_pass_or_concrete_blocker") is True, "same_task_continuity_missing", failures)

    efficiency = config.get("efficiency") or {}
    _require(efficiency.get("fixed_wait_time_forbidden") is True, "fixed_wait_required", failures)
    _require(efficiency.get("fixed_source_count_forbidden") is True, "fixed_source_count_required", failures)
    _require(efficiency.get("fixed_agent_count_is_not_a_quality_metric") is True, "fixed_agent_count_treated_as_quality", failures)
    _require(efficiency.get("prefer_high_information_gain_actions") is True, "information_gain_rule_missing", failures)

    agents_text = AGENTS_PATH.read_text(encoding="utf-8")
    doc_text = CANONICAL_DOC_PATH.read_text(encoding="utf-8")
    for text, name in [(agents_text, "AGENTS"), (doc_text, "DOC")]:
        _require("continuous-thinking-global.json" in text, f"{name.lower()}_does_not_reference_global_profile", failures)
        _require("UNSATISFIED" in text, f"{name.lower()}_missing_default_fail_acceptance", failures)
        _require("fresh-context" in text.lower() or "fresh context" in text.lower(), f"{name.lower()}_missing_fresh_context_evaluator", failures)
        _require("evidence" in text.lower(), f"{name.lower()}_missing_evidence_language", failures)

    return sorted(set(failures))


def main() -> int:
    failures = validate()
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("PASS continuous-thinking-quality-v3 global invariants")
    return 0


if __name__ == "__main__":
    sys.exit(main())
