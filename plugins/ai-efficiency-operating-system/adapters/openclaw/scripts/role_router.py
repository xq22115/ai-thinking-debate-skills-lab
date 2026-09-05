#!/usr/bin/env python3
"""Deterministic baseline for OpenClaw adaptive specialist and execution-plane selection."""

from __future__ import annotations

import argparse
import json
from typing import Any

ROLE_ORDER = [
    "architecture-arbiter",
    "researcher",
    "falsifier",
    "compatibility-reviewer",
    "implementer",
    "runtime-forensics",
    "recovery",
    "evidence-gate",
    "learning-curator",
]


def _signals(state: dict[str, Any]) -> dict[str, Any]:
    complexity = str(state.get("complexity", "direct")).lower()
    if complexity not in {"direct", "investigative", "architectural"}:
        raise ValueError("complexity must be direct, investigative, or architectural")
    return {
        "complexity": complexity,
        "research": bool(state.get("research")),
        "state_change": bool(state.get("state_change")),
        "runtime_mismatch": bool(state.get("runtime_mismatch")),
        "compatibility_risk": bool(state.get("compatibility_risk")),
        "repeated_failure": bool(state.get("repeated_failure")),
        "learning_candidate": bool(state.get("learning_candidate")),
        "high_impact": bool(state.get("high_impact")),
        "conflicting_evidence": bool(state.get("conflicting_evidence")),
        "deterministic_workflow": bool(state.get("deterministic_workflow")),
    }


def unresolved_uncertainty(signals: dict[str, Any]) -> bool:
    return bool(
        signals["complexity"] != "direct"
        or signals["research"]
        or signals["runtime_mismatch"]
        or signals["compatibility_risk"]
        or signals["repeated_failure"]
        or signals["high_impact"]
        or signals["conflicting_evidence"]
    )


def select_roles(state: dict[str, Any]) -> tuple[list[str], list[str]]:
    s = _signals(state)
    lobster_only = s["deterministic_workflow"] and not unresolved_uncertainty(s)
    wanted: set[str] = set()
    reasons: list[str] = []

    if s["complexity"] == "architectural":
        wanted.add("architecture-arbiter")
        wanted.add("evidence-gate")
        reasons.append("architectural")
    if s["research"] or s["complexity"] == "investigative":
        wanted.add("researcher")
        reasons.append("research")
    if s["conflicting_evidence"] or s["high_impact"]:
        wanted.add("falsifier")
        reasons.append("disconfirmation")
    if s["compatibility_risk"]:
        wanted.add("compatibility-reviewer")
        reasons.append("compatibility")
    if s["state_change"]:
        # A verified known procedure belongs to Lobster, not to an implementer child
        # that merely replays the same deterministic sequence. Uncertain state
        # changes still use specialists before the known path is executed.
        if not s["deterministic_workflow"]:
            wanted.add("implementer")
        if not lobster_only:
            wanted.add("evidence-gate")
        reasons.append("state-change")
    if s["runtime_mismatch"]:
        wanted.add("runtime-forensics")
        wanted.add("evidence-gate")
        reasons.append("runtime-mismatch")
    if s["repeated_failure"]:
        wanted.add("recovery")
        wanted.add("evidence-gate")
        reasons.append("recovery")
    if s["high_impact"]:
        wanted.add("evidence-gate")
        reasons.append("high-impact")
    if s["learning_candidate"]:
        wanted.add("learning-curator")
        reasons.append("learning")
    if s["deterministic_workflow"]:
        reasons.append("deterministic-workflow")

    # Direct, low-impact requests and known deterministic workflows can avoid
    # child fan-out entirely. No minimum child count exists.
    roles = [role for role in ROLE_ORDER if role in wanted]
    return roles, list(dict.fromkeys(reasons))


def select_execution_plane(state: dict[str, Any], roles: list[str] | None = None) -> str:
    s = _signals(state)
    selected = roles if roles is not None else select_roles(state)[0]
    if s["deterministic_workflow"]:
        return "hybrid" if unresolved_uncertainty(s) else "lobster"
    if selected:
        return "agents"
    return "parent"


def route(state: dict[str, Any]) -> dict[str, Any]:
    roles, reasons = select_roles(state)
    return {
        "schema": 2,
        "roles": roles,
        "count": len(roles),
        "execution_plane": select_execution_plane(state, roles),
        "reason_codes": reasons,
        "fixed_agent_count": False,
        "parent_completion_authority": True,
        "default_child_context": "isolated",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-json", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    state = json.loads(args.state_json)
    if not isinstance(state, dict):
        raise SystemExit("state must be a JSON object")
    print(json.dumps(route(state), separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
