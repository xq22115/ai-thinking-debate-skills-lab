#!/usr/bin/env python3
"""Fail closed if the continuous-thinking runtime binding drifts or detaches."""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
PROFILE = ROOT / "ai-system/configs/continuous-thinking-global.json"
REGISTRY = ROOT / "ai-system/registry.yml"
BINDER = ROOT / "scripts/continuous_thinking_runtime_binding.py"
WORKFLOW = ROOT / "scripts/run_quality_bound_workflow.py"
SETTINGS = REPO_ROOT / ".claude/settings.json"
RESEARCH_PERMISSION_HOOK = REPO_ROOT / ".claude/hooks/allow-a03-web-research.py"
RESEARCH_HOOK = REPO_ROOT / ".claude/hooks/record-web-research.py"


def _hook_matches(settings: dict, event: str, matcher: str, command_token: str) -> bool:
    rows = ((settings.get("hooks") or {}).get(event) or [])
    if not isinstance(rows, list):
        return False
    return any(
        isinstance(row, dict)
        and row.get("matcher") == matcher
        and any(
            isinstance(handler, dict)
            and handler.get("type") == "command"
            and command_token in str(handler.get("command") or "")
            for handler in (row.get("hooks") or [])
        )
        for row in rows
    )


def validate() -> list[str]:
    failures: list[str] = []
    for path, code in [
        (PROFILE, "quality_profile_missing"),
        (REGISTRY, "ai_registry_missing"),
        (BINDER, "quality_runtime_binder_missing"),
        (WORKFLOW, "quality_bound_workflow_missing"),
        (SETTINGS, "claude_project_settings_missing"),
        (RESEARCH_PERMISSION_HOOK, "research_permission_hook_missing"),
        (RESEARCH_HOOK, "research_attestation_hook_missing"),
    ]:
        if not path.is_file():
            failures.append(code)
    if failures:
        return failures

    try:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"quality_profile_or_settings_invalid:{type(exc).__name__}"]
    if profile.get("default_enabled") is not True:
        failures.append("quality_profile_not_default_enabled")
    if not str(profile.get("profile_id") or "").strip():
        failures.append("quality_profile_id_missing")
    if not ((profile.get("release") or {}).get("continue_same_task_until_pass_or_concrete_blocker") is True):
        failures.append("same_task_continuity_not_enabled")
    if not ((profile.get("anti_instant_response") or {}).get("material_or_critical_must_not_release_first_plausible_answer") is True):
        failures.append("first_plausible_answer_not_blocked")
    if not ((profile.get("research_and_experience") or {}).get("triggered_research_requires_tool_backed_evidence") is True):
        failures.append("triggered_research_not_tool_evidence_bound")
    if not ((profile.get("output_delivery") or {}).get("artificial_output_throttling_forbidden") is True):
        failures.append("artificial_output_throttling_not_forbidden")

    reasoning_runtime = profile.get("reasoning_runtime") or {}
    if reasoning_runtime.get("effort_by_task_class") != {
        "simple": "medium", "material": "xhigh", "critical": "max"
    }:
        failures.append("reasoning_effort_mapping_drift")
    if reasoning_runtime.get("effort_must_be_runtime_bound") is not True:
        failures.append("reasoning_effort_runtime_binding_disabled")
    if reasoning_runtime.get("material_or_critical_must_not_inherit_disable_thinking") is not True:
        failures.append("deep_thinking_disable_override_not_guarded")
    if reasoning_runtime.get("effective_effort_readback_required_for_deep_research") is not True:
        failures.append("effective_effort_readback_not_required")
    if reasoning_runtime.get("effort_downgrade_cannot_count_as_pass_evidence") is not True:
        failures.append("effort_downgrade_can_count_as_pass")

    research_attestation = ((profile.get("research_and_experience") or {}).get("runtime_attestation") or {})
    if research_attestation.get("required_actor") != "A03":
        failures.append("research_attestation_actor_mismatch")
    if set(research_attestation.get("required_successful_tools_for_material_or_critical") or []) != {"WebSearch", "WebFetch"}:
        failures.append("research_attestation_tools_incomplete")
    if research_attestation.get("permission_hook_event") != "PreToolUse":
        failures.append("research_permission_hook_not_pretooluse")
    if research_attestation.get("hook_event") != "PostToolUse":
        failures.append("research_attestation_not_posttooluse")
    if research_attestation.get("trust_independent_permission_hook_required") is not True:
        failures.append("research_permission_can_depend_on_workspace_trust")
    if research_attestation.get("effective_effort_readback_required") is not True:
        failures.append("research_effective_effort_not_attested")
    if research_attestation.get("accepted_receipt_requires_requested_effective_match") is not True:
        failures.append("research_receipt_can_accept_effort_mismatch")
    if research_attestation.get("fresh_audit_directory_per_run") is not True:
        failures.append("research_attestation_can_reuse_stale_receipts")

    if not isinstance(settings, dict):
        failures.append("claude_project_settings_not_object")
    else:
        if settings.get("alwaysThinkingEnabled") is not True:
            failures.append("claude_project_thinking_not_enabled")
        if settings.get("effortLevel") != "xhigh":
            failures.append("claude_project_effort_not_xhigh")
        allow = set((settings.get("permissions") or {}).get("allow") or [])
        if not {"WebSearch", "WebFetch"}.issubset(allow):
            failures.append("claude_web_research_tools_not_preapproved_for_trusted_sessions")
        if not _hook_matches(
            settings, "PreToolUse", "WebSearch|WebFetch", "allow-a03-web-research.py"
        ):
            failures.append("claude_web_research_permission_hook_not_registered")
        if not _hook_matches(
            settings, "PostToolUse", "WebSearch|WebFetch", "record-web-research.py"
        ):
            failures.append("claude_web_research_attestation_hook_not_registered")

    registry = REGISTRY.read_text(encoding="utf-8")
    for token, code in [
        ("continuous-thinking-global.json", "profile_not_registered"),
        ("continuous_thinking_runtime_binding.py", "binder_not_registered"),
        ("run_quality_bound_workflow.py", "quality_workflow_not_registered"),
    ]:
        if token not in registry:
            failures.append(code)

    binder = BINDER.read_text(encoding="utf-8")
    for token, code in [
        ("profile_sha256", "profile_hash_attestation_missing"),
        ("quality_profile_binding", "assignment_binding_metadata_missing"),
        ("BINDING_START", "runtime_directive_marker_missing"),
        ("preparation_not_pass", "binding_not_fail_closed_on_preparation"),
        ("perform actual tool-backed research before release", "runtime_research_trigger_not_enforced"),
        ("observable tool/source evidence", "runtime_research_evidence_gate_missing"),
        ("delayed output cannot satisfy a research request", "runtime_delay_can_fake_research"),
        ("token-by-token throttling", "runtime_output_throttling_guard_missing"),
        ("deliberate chunk pauses", "runtime_chunk_pause_guard_missing"),
        ("slow streaming is not evidence of deep reasoning", "runtime_slow_streaming_can_fake_depth"),
        ("reasoning_effort", "runtime_reasoning_effort_metadata_missing"),
        ("PostToolUse runtime receipt", "runtime_research_attestation_directive_missing"),
        ("WebSearch and WebFetch", "runtime_required_web_tools_missing"),
    ]:
        if token not in binder:
            failures.append(code)

    workflow = WORKFLOW.read_text(encoding="utf-8")
    for token, code in [
        ("bind_preparation", "workflow_does_not_bind_profile"),
        ("run_workflow", "workflow_does_not_delegate_to_existing_orchestrator"),
        ("quality-bound-preparation.json", "bound_preparation_evidence_missing"),
        ("quality-bound-workflow.json", "bound_workflow_evidence_missing"),
        ("resume_quality_binding_evidence_missing", "resume_can_reuse_unbound_evidence"),
        ("resume_quality_binding_mismatch", "resume_can_cross_quality_profile_versions"),
        ("CLAUDE_CODE_EFFORT_LEVEL", "workflow_does_not_bind_runtime_effort"),
        ("CLAUDE_CODE_DISABLE_THINKING", "workflow_does_not_clear_forced_thinking_disable"),
        ("CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING", "workflow_does_not_clear_adaptive_thinking_disable"),
        ("MAX_THINKING_TOKENS", "workflow_does_not_clear_zero_thinking_budget"),
        ("QUALITY_RESEARCH_AUDIT_DIR", "workflow_does_not_bind_fresh_research_audit"),
        ("quality_evidence_accepted", "workflow_does_not_require_accepted_research_receipt"),
        ("requested_effort", "workflow_does_not_check_requested_effort"),
        ("effective_effort", "workflow_does_not_check_effective_effort"),
        ("research_receipt_not_effort_attested", "workflow_does_not_fail_closed_on_unattested_effort"),
        ("successful_tool_receipt_missing", "workflow_does_not_fail_closed_on_missing_web_tool_receipt"),
        ("research_runtime_attestation", "workflow_does_not_publish_research_attestation"),
        ("effective_effort_verified_by_research_hook", "workflow_does_not_publish_effort_readback_state"),
        ("delivery_contract", "workflow_does_not_publish_delivery_contract"),
    ]:
        if token not in workflow:
            failures.append(code)

    permission_hook = RESEARCH_PERMISSION_HOOK.read_text(encoding="utf-8")
    for token, code in [
        ("PreToolUse", "permission_hook_not_pretooluse_bound"),
        ("permissionDecision", "permission_hook_does_not_return_permission_decision"),
        ("allow", "permission_hook_does_not_allow_research"),
        ("A03", "permission_hook_not_scoped_to_A03"),
        ("CONTROL_PLANE_ACTOR_ID", "permission_hook_actor_binding_missing"),
        ("WebSearch", "permission_hook_websearch_missing"),
        ("WebFetch", "permission_hook_webfetch_missing"),
    ]:
        if token not in permission_hook:
            failures.append(code)

    hook = RESEARCH_HOOK.read_text(encoding="utf-8")
    for token, code in [
        ("PostToolUse", "hook_not_posttooluse_bound"),
        ("QUALITY_RESEARCH_AUDIT_DIR", "hook_audit_directory_env_missing"),
        ("CONTROL_PLANE_ACTOR_ID", "hook_actor_env_missing"),
        ("WebSearch", "hook_websearch_missing"),
        ("WebFetch", "hook_webfetch_missing"),
        ("post_tool_success", "hook_success_receipt_missing"),
        ("tool_response_sha256", "hook_response_hash_missing"),
        ("CLAUDE_CODE_EFFORT_LEVEL", "hook_requested_effort_binding_missing"),
        ("CLAUDE_EFFORT", "hook_effective_effort_env_readback_missing"),
        ("payload.get(\"effort\")", "hook_effective_effort_payload_readback_missing"),
        ("effective_effort_mismatch", "hook_effort_downgrade_rejection_missing"),
        ("quality_evidence_accepted", "hook_accepted_evidence_marker_missing"),
        ("_rejected", "hook_rejected_receipt_quarantine_missing"),
    ]:
        if token not in hook:
            failures.append(code)
    return sorted(set(failures))


def main() -> int:
    failures = validate()
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("PASS continuous-thinking runtime binding invariants")
    return 0


if __name__ == "__main__":
    sys.exit(main())
