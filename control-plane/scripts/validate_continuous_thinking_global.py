#!/usr/bin/env python3
"""Validate repository-wide Continuous Thinking Quality v3 invariants.

This is intentionally small and dependency-free so CI can fail closed when the
machine-readable quality profile, runtime reasoning settings, research audit
hooks, or repository entry points drift.
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "control-plane/ai-system/configs/continuous-thinking-global.json"
AGENTS_PATH = REPO_ROOT / "AGENTS.md"
CANONICAL_DOC_PATH = REPO_ROOT / "docs/CONTINUOUS_THINKING_QUALITY_OS.md"
PROJECT_SETTINGS_PATH = REPO_ROOT / ".claude/settings.json"
RESEARCH_HOOK_PATH = REPO_ROOT / ".claude/hooks/record-web-research.py"


def _load_json(path: pathlib.Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected_object:{path}")
    return value


def _require(condition: bool, code: str, failures: list[str]) -> None:
    if not condition:
        failures.append(code)


def _resolve_from_config(relative: object) -> pathlib.Path | None:
    if not isinstance(relative, str) or not relative.strip():
        return None
    return (CONFIG_PATH.parent / relative).resolve()


def _post_tool_hook_matches(settings: dict, matcher: str, command_token: str) -> bool:
    hooks = settings.get("hooks") or {}
    rows = hooks.get("PostToolUse") or []
    if not isinstance(rows, list):
        return False
    for row in rows:
        if not isinstance(row, dict) or row.get("matcher") != matcher:
            continue
        handlers = row.get("hooks") or []
        if not isinstance(handlers, list):
            continue
        for handler in handlers:
            if (
                isinstance(handler, dict)
                and handler.get("type") == "command"
                and command_token in str(handler.get("command") or "")
            ):
                return True
    return False


def validate() -> list[str]:
    failures: list[str] = []
    for path, code in [
        (CONFIG_PATH, "config_missing"),
        (AGENTS_PATH, "root_agents_missing"),
        (CANONICAL_DOC_PATH, "canonical_doc_missing"),
        (PROJECT_SETTINGS_PATH, "project_claude_settings_missing"),
        (RESEARCH_HOOK_PATH, "research_attestation_hook_missing"),
    ]:
        if not path.is_file():
            failures.append(code)
    if failures:
        return failures

    try:
        config = _load_json(CONFIG_PATH)
        settings = _load_json(PROJECT_SETTINGS_PATH)
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
    _require(
        anti_instant.get("explicit_search_or_deep_research_request_is_a_research_trigger") is True,
        "explicit_search_request_not_a_research_trigger",
        failures,
    )
    _require(
        anti_instant.get("search_request_cannot_be_satisfied_by_delay_only") is True,
        "delay_can_fake_search_request",
        failures,
    )

    output_delivery = config.get("output_delivery") or {}
    _require(
        output_delivery.get("reasoning_and_delivery_are_separate_phases") is True,
        "reasoning_delivery_phases_not_separated",
        failures,
    )
    _require(
        output_delivery.get("artificial_output_throttling_forbidden") is True,
        "artificial_output_throttling_allowed",
        failures,
    )
    _require(
        output_delivery.get("artificial_first_token_delay_forbidden") is True,
        "artificial_first_token_delay_allowed",
        failures,
    )
    _require(
        output_delivery.get("deliberate_chunk_pause_forbidden") is True,
        "deliberate_chunk_pause_allowed",
        failures,
    )
    _require(
        output_delivery.get("slow_streaming_is_not_depth_evidence") is True,
        "slow_streaming_can_fake_depth",
        failures,
    )
    _require(
        output_delivery.get("normal_continuous_delivery_after_release_gate") is True,
        "normal_delivery_after_release_not_required",
        failures,
    )

    reasoning_runtime = config.get("reasoning_runtime") or {}
    _require(
        reasoning_runtime.get("effort_by_task_class") == {
            "simple": "medium",
            "material": "xhigh",
            "critical": "max",
        },
        "reasoning_effort_mapping_drift",
        failures,
    )
    _require(
        reasoning_runtime.get("effort_must_be_runtime_bound") is True,
        "reasoning_effort_not_runtime_bound",
        failures,
    )
    _require(
        reasoning_runtime.get("material_or_critical_must_not_inherit_disable_thinking") is True,
        "deep_tasks_can_inherit_thinking_disable",
        failures,
    )
    _require(
        reasoning_runtime.get("prompt_language_alone_is_not_effort_enforcement") is True,
        "prompt_language_can_fake_effort_enforcement",
        failures,
    )
    _require(
        reasoning_runtime.get("project_default_effort") == "xhigh",
        "project_default_effort_not_xhigh",
        failures,
    )

    _require(settings.get("alwaysThinkingEnabled") is True, "project_thinking_not_enabled", failures)
    _require(settings.get("effortLevel") == "xhigh", "project_effort_not_xhigh", failures)
    permission_allow = set((settings.get("permissions") or {}).get("allow") or [])
    _require(
        {"WebSearch", "WebFetch"}.issubset(permission_allow),
        "web_research_tools_not_preapproved",
        failures,
    )
    _require(
        _post_tool_hook_matches(
            settings,
            "WebSearch|WebFetch",
            "record-web-research.py",
        ),
        "web_research_post_tool_hook_not_registered",
        failures,
    )
    hook_text = RESEARCH_HOOK_PATH.read_text(encoding="utf-8")
    for token, code in [
        ("QUALITY_RESEARCH_AUDIT_DIR", "research_hook_audit_dir_binding_missing"),
        ("CONTROL_PLANE_ACTOR_ID", "research_hook_actor_binding_missing"),
        ("WebSearch", "research_hook_websearch_missing"),
        ("WebFetch", "research_hook_webfetch_missing"),
        ("post_tool_success", "research_hook_success_attestation_missing"),
    ]:
        _require(token in hook_text, code, failures)

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
        acceptance.get("satisfied_requires_resolvable_pass_evidence") is True,
        "satisfied_evidence_binding_missing",
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
    acceptance_schema = _resolve_from_config(acceptance.get("schema"))
    acceptance_validator = _resolve_from_config(acceptance.get("semantic_validator"))
    _require(
        acceptance_schema is not None and acceptance_schema.is_file(),
        "acceptance_schema_missing_or_detached",
        failures,
    )
    _require(
        acceptance_validator is not None and acceptance_validator.is_file(),
        "acceptance_validator_missing_or_detached",
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
    _require(research.get("triggered_research_requires_tool_backed_evidence") is True, "triggered_research_can_be_claimed_without_tool_evidence", failures)
    _require(research.get("research_claim_requires_source_or_tool_evidence") is True, "research_claim_can_be_unsupported", failures)
    _require(research.get("delay_or_hidden_reasoning_cannot_satisfy_research_trigger") is True, "delay_or_hidden_reasoning_can_fake_research", failures)
    receipt_fields = set(research.get("research_receipt_fields") or [])
    required_receipt_fields = {"trigger", "sources_or_queries", "evidence_summary", "decision_impact", "stop_reason"}
    _require(required_receipt_fields.issubset(receipt_fields), "research_receipt_fields_incomplete", failures)
    triggers = set(research.get("trigger_conditions") or [])
    _require(
        any("explicit user request" in str(item).lower() and "research" in str(item).lower() for item in triggers),
        "explicit_user_research_trigger_missing",
        failures,
    )
    runtime_attestation = research.get("runtime_attestation") or {}
    _require(runtime_attestation.get("required_actor") == "A03", "research_runtime_actor_not_A03", failures)
    _require(
        set(runtime_attestation.get("required_successful_tools_for_material_or_critical") or []) == {"WebSearch", "WebFetch"},
        "research_runtime_tools_incomplete",
        failures,
    )
    _require(runtime_attestation.get("hook_event") == "PostToolUse", "research_runtime_hook_not_posttooluse", failures)
    _require(runtime_attestation.get("fresh_audit_directory_per_run") is True, "research_runtime_audit_can_be_stale", failures)
    _require(runtime_attestation.get("self_report_only_cannot_pass") is True, "research_runtime_self_report_can_pass", failures)
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
