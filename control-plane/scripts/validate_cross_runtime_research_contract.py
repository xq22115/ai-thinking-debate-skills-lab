#!/usr/bin/env python3
"""Fail closed when deep-research semantics drift across runtime entry points."""
from __future__ import annotations

import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PROFILE = REPO_ROOT / "control-plane/ai-system/configs/continuous-thinking-global.json"
CODEX_INSTALLER = REPO_ROOT / "control-plane/scripts/install_codex_global_quality.py"
CLAUDE_SETTINGS = REPO_ROOT / ".claude/settings.json"
CLAUDE_STOP_HOOK = REPO_ROOT / ".claude/hooks/enforce-a03-research-cycle.py"
QUALITY_WORKFLOW = REPO_ROOT / "control-plane/scripts/run_quality_bound_workflow.py"
A03_ROLE = REPO_ROOT / "control-plane/ai-system/control-plane/agents/A03-source-research.md"


def _require(condition: bool, code: str, failures: list[str]) -> None:
    if not condition:
        failures.append(code)


def _stop_hook_registered(settings: dict) -> bool:
    rows = ((settings.get("hooks") or {}).get("Stop") or [])
    if not isinstance(rows, list):
        return False
    for row in rows:
        if not isinstance(row, dict):
            continue
        for handler in row.get("hooks") or []:
            if (
                isinstance(handler, dict)
                and handler.get("type") == "command"
                and "enforce-a03-research-cycle.py" in str(handler.get("command") or "")
            ):
                return True
    return False


def validate_values(
    profile: dict,
    codex_installer_text: str,
    claude_settings: dict,
    stop_hook_text: str,
    workflow_text: str,
    a03_role_text: str,
) -> list[str]:
    failures: list[str] = []
    research = profile.get("research_and_experience") or {}
    saturation = research.get("adaptive_saturation") or {}
    structure = saturation.get("minimum_falsification_structure") or []

    _require(
        saturation.get("applies_when_research_triggered_for_material_or_critical") is True,
        "canonical_adaptive_saturation_not_required",
        failures,
    )
    _require(
        isinstance(structure, list) and len(structure) == 4,
        "canonical_falsification_structure_not_four_stage",
        failures,
    )
    joined_structure = " ".join(str(item).lower() for item in structure)
    for token, code in [
        ("discover", "canonical_discover_stage_missing"),
        ("inspect", "canonical_inspect_stage_missing"),
        ("challenge", "canonical_challenge_stage_missing"),
        ("follow-up", "canonical_followup_stage_missing"),
        ("reconcile", "canonical_reconcile_stage_missing"),
    ]:
        _require(token in joined_structure, code, failures)
    _require(
        saturation.get("structure_is_not_source_quota") is True,
        "canonical_structure_can_degrade_into_source_quota",
        failures,
    )
    _require(
        saturation.get("repeated_query_is_not_distinct_route") is True,
        "canonical_repeated_query_can_fake_challenge",
        failures,
    )
    _require(
        saturation.get("same_source_reinspection_is_not_followup_evidence") is True,
        "canonical_same_source_can_fake_followup",
        failures,
    )
    _require(
        saturation.get("continue_while_high_impact_unknown_or_material_conflict_remains") is True,
        "canonical_minimum_cycle_can_force_premature_stop",
        failures,
    )
    _require(
        saturation.get("instruction_compliance_alone_is_not_runtime_attestation") is True,
        "canonical_instruction_text_can_fake_runtime_evidence",
        failures,
    )
    _require(
        saturation.get("release_revalidation_required_when_runtime_can_attest") is True,
        "canonical_release_revalidation_missing",
        failures,
    )
    _require(
        saturation.get("runtime_neutral_contract") is True,
        "canonical_saturation_contract_not_runtime_neutral",
        failures,
    )

    attestation = research.get("runtime_attestation") or {}
    _require(attestation.get("stop_hook_event") == "Stop", "claude_attestation_stop_event_missing", failures)
    _require(
        attestation.get("accepted_receipt_requires_ordering_timestamp") is True,
        "claude_attestation_ordering_not_required",
        failures,
    )
    _require(
        attestation.get("adaptive_saturation_gate_required") is True,
        "claude_attestation_saturation_gate_optional",
        failures,
    )
    _require(
        attestation.get("release_revalidates_saturation") is True,
        "claude_attestation_release_revalidation_missing",
        failures,
    )

    codex_tokens = [
        "POLICY_VERSION = \"continuous-quality-v2-falsification-research\"",
        "perform actual tool-backed research",
        "minimum falsification structure",
        "materially different route",
        "distinct follow-up source",
        "repeating the same query with cosmetic wording",
        "instruction compliance alone is not runtime-attested research evidence",
        "higher reasoning effort is not a substitute for explicit evidence and stopping criteria",
    ]
    for token in codex_tokens:
        _require(token in codex_installer_text, f"codex_contract_missing:{token}", failures)
    _require(
        "WebSearch" not in codex_installer_text and "WebFetch" not in codex_installer_text,
        "codex_runtime_neutral_policy_leaks_claude_tool_names",
        failures,
    )

    _require(_stop_hook_registered(claude_settings), "claude_stop_hook_not_registered", failures)
    for token, code in [
        ("materially different", "claude_stop_hook_distinct_challenge_missing"),
        ("distinct follow-up source", "claude_stop_hook_distinct_followup_missing"),
        ("repeating the same query", "claude_stop_hook_repeat_query_guard_missing"),
    ]:
        _require(token in stop_hook_text, code, failures)
    for token, code in [
        ("_research_cycle_state", "release_cycle_revalidation_function_missing"),
        ("research_cycle_distinct_challenge_search_missing", "release_challenge_gate_missing"),
        ("research_cycle_distinct_followup_inspection_missing", "release_followup_gate_missing"),
        ("adaptive_research_saturation_verified", "release_saturation_result_missing"),
    ]:
        _require(token in workflow_text, code, failures)
    for token, code in [
        ("Discover", "A03_discover_stage_missing"),
        ("Inspect", "A03_inspect_stage_missing"),
        ("Challenge", "A03_challenge_stage_missing"),
        ("Reconcile", "A03_reconcile_stage_missing"),
        ("minimum causal falsification structure", "A03_structure_not_explicitly_nonquota"),
    ]:
        _require(token in a03_role_text, code, failures)

    return sorted(set(failures))


def validate() -> list[str]:
    paths = [PROFILE, CODEX_INSTALLER, CLAUDE_SETTINGS, CLAUDE_STOP_HOOK, QUALITY_WORKFLOW, A03_ROLE]
    missing = [f"missing:{path.relative_to(REPO_ROOT)}" for path in paths if not path.is_file()]
    if missing:
        return missing
    try:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        settings = json.loads(CLAUDE_SETTINGS.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"cross_runtime_contract_parse_failure:{type(exc).__name__}"]
    if not isinstance(profile, dict) or not isinstance(settings, dict):
        return ["cross_runtime_contract_json_not_object"]
    return validate_values(
        profile,
        CODEX_INSTALLER.read_text(encoding="utf-8"),
        settings,
        CLAUDE_STOP_HOOK.read_text(encoding="utf-8"),
        QUALITY_WORKFLOW.read_text(encoding="utf-8"),
        A03_ROLE.read_text(encoding="utf-8"),
    )


def main() -> int:
    failures = validate()
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("PASS cross-runtime adaptive research contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
