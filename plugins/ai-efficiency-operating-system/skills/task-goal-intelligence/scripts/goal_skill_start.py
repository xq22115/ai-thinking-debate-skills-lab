#!/usr/bin/env python3
"""Deterministic runtime preamble for Task Goal Intelligence.

Inspired by runtime-first skill harnesses: emit small machine-readable status lines
that a host can consume before the language-model workflow. No network, model, or
third-party dependency is required.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any

PROTO = 1
CORE_FIELDS = ("root_goal", "desired_end_state", "target_identity", "acceptance_tests")
PHASES = ("ORIENT", "DISCRIMINATE", "COMMIT", "EXECUTE", "VERIFY", "RECOVER", "LEARN")


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (list, tuple, dict, str)):
        return bool(value)
    return bool(value)


def canonical_goal_payload(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "root_goal": state.get("root_goal"),
        "desired_end_state": state.get("desired_end_state"),
        "hard_constraints": state.get("hard_constraints") or [],
        "negations": state.get("negations") or [],
        "target_identity": state.get("target_identity"),
        "acceptance_tests": state.get("acceptance_tests") or [],
        "protected_capabilities": state.get("protected_capabilities") or [],
    }


def goal_fingerprint(state: dict[str, Any]) -> str:
    payload = json.dumps(canonical_goal_payload(state), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def missing_core_fields(state: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for field in CORE_FIELDS:
        if not _truthy(state.get(field)):
            missing.append(field)
    return missing


def evaluate_state(state: dict[str, Any]) -> dict[str, Any]:
    """Return the next phase plus hard gates. Pure and deterministic for evals."""
    missing = missing_core_fields(state)
    correction = _truthy(state.get("user_correction"))
    completion_claim = _truthy(state.get("completion_claim"))
    blocker = _truthy(state.get("blocker"))
    route_failure = _truthy(state.get("route_failure"))
    no_delta_steps = int(state.get("no_delta_steps") or 0)
    same_mechanism_repairs = int(state.get("same_mechanism_failed_repairs") or 0)
    action_divergence = _truthy(state.get("action_divergence"))
    unknowns = state.get("decision_critical_unknowns") or []
    committed = _truthy(state.get("goal_contract_committed"))
    learned = _truthy(state.get("acceptance_verified")) and _truthy(state.get("learning_reviewed"))

    if correction:
        phase = "ORIENT"
    elif completion_claim:
        phase = "VERIFY"
    elif blocker or route_failure or no_delta_steps >= 2:
        phase = "RECOVER"
    elif missing:
        phase = "ORIENT"
    elif unknowns and action_divergence:
        phase = "DISCRIMINATE"
    elif not committed:
        phase = "COMMIT"
    elif learned:
        phase = "LEARN"
    else:
        phase = "EXECUTE"

    state_sensitive_claim = _truthy(state.get("state_sensitive_claim"))
    mutation_claim = _truthy(state.get("mutation_claim"))
    historical_claim = _truthy(state.get("historical_claim"))
    fresh_owning_evidence = _truthy(state.get("fresh_owning_evidence"))
    separable_work = _truthy(state.get("separable_work"))
    scope_reduction_without_user_change = _truthy(state.get("scope_reduction_without_user_change"))

    gates = {
        "fresh_verification_required": completion_claim or state_sensitive_claim or mutation_claim,
        "historical_revalidation_required": historical_claim and not fresh_owning_evidence,
        "causal_pivot_required": no_delta_steps >= 2 or same_mechanism_repairs >= 2,
        "architectural_review_required": same_mechanism_repairs >= 3,
        "continue_separable_work": (blocker or route_failure) and separable_work,
        "reject_semantic_minimization": scope_reduction_without_user_change,
        "discriminate_before_effect": bool(unknowns and action_divergence),
        "reverse_acceptance_required": completion_claim,
        "route_failure_does_not_change_root_goal": route_failure,
    }

    return {
        "protocol": PROTO,
        "phase": phase,
        "path": state.get("task_path") or "DIRECT",
        "goal_version": int(state.get("goal_version") or 1),
        "goal_fingerprint": goal_fingerprint(state),
        "missing_core_fields": missing,
        "gates": gates,
    }


def parse_state(args: argparse.Namespace) -> dict[str, Any]:
    if args.state_json:
        raw = args.state_json
    else:
        try:
            raw = input()
        except EOFError:
            raw = "{}"
    if not raw.strip():
        return {}
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError("state must be a JSON object")
    return obj


def emit_lines(result: dict[str, Any]) -> None:
    print(f"GOAL_NATIVE_PROTO: {result['protocol']}")
    print(f"GOAL_PHASE: {result['phase']}")
    print(f"GOAL_PATH: {result['path']}")
    print(f"GOAL_VERSION: {result['goal_version']}")
    print(f"GOAL_FINGERPRINT: {result['goal_fingerprint']}")
    print("MISSING_CORE_FIELDS: " + ",".join(result["missing_core_fields"]))
    for key, value in sorted(result["gates"].items()):
        print(f"GATE_{key.upper()}: {'true' if value else 'false'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-json", help="Current goal-state JSON. If omitted, read one JSON object from stdin.")
    parser.add_argument("--json", action="store_true", help="Emit one JSON object instead of status lines.")
    args = parser.parse_args()
    try:
        result = evaluate_state(parse_state(args))
    except (ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"protocol": PROTO, "status": "ERROR", "error": str(exc)}, ensure_ascii=False))
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        emit_lines(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
