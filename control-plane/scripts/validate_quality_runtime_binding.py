#!/usr/bin/env python3
"""Fail closed if the continuous-thinking runtime binding drifts or detaches."""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROFILE = ROOT / "ai-system/configs/continuous-thinking-global.json"
REGISTRY = ROOT / "ai-system/registry.yml"
BINDER = ROOT / "scripts/continuous_thinking_runtime_binding.py"
WORKFLOW = ROOT / "scripts/run_quality_bound_workflow.py"


def validate() -> list[str]:
    failures: list[str] = []
    for path, code in [
        (PROFILE, "quality_profile_missing"),
        (REGISTRY, "ai_registry_missing"),
        (BINDER, "quality_runtime_binder_missing"),
        (WORKFLOW, "quality_bound_workflow_missing"),
    ]:
        if not path.is_file():
            failures.append(code)
    if failures:
        return failures

    try:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"quality_profile_invalid:{type(exc).__name__}"]
    if profile.get("default_enabled") is not True:
        failures.append("quality_profile_not_default_enabled")
    if not str(profile.get("profile_id") or "").strip():
        failures.append("quality_profile_id_missing")
    if not ((profile.get("release") or {}).get("continue_same_task_until_pass_or_concrete_blocker") is True):
        failures.append("same_task_continuity_not_enabled")
    if not ((profile.get("anti_instant_response") or {}).get("material_or_critical_must_not_release_first_plausible_answer") is True):
        failures.append("first_plausible_answer_not_blocked")

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
    ]:
        if token not in workflow:
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
