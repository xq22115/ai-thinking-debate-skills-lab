#!/usr/bin/env python3
"""Deterministic baseline for OpenClaw adaptive specialist selection."""

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


def select_roles(state: dict[str, Any]) -> tuple[list[str], list[str]]:
    complexity = str(state.get("complexity", "direct")).lower()
    if complexity not in {"direct", "investigative", "architectural"}:
        raise ValueError("complexity must be direct, investigative, or architectural")

    research = bool(state.get("research"))
    state_change = bool(state.get("state_change"))
    runtime_mismatch = bool(state.get("runtime_mismatch"))
    compatibility_risk = bool(state.get("compatibility_risk"))
    repeated_failure = bool(state.get("repeated_failure"))
    learning_candidate = bool(state.get("learning_candidate"))
    high_impact = bool(state.get("high_impact"))
    conflicting_evidence = bool(state.get("conflicting_evidence"))

    wanted: set[str] = set()
    reasons: list[str] = []

    if complexity == "architectural":
        wanted.add("architecture-arbiter")
        wanted.add("evidence-gate")
        reasons.append("architectural")
    if research or complexity == "investigative":
        wanted.add("researcher")
        reasons.append("research")
    if conflicting_evidence or high_impact:
        wanted.add("falsifier")
        reasons.append("disconfirmation")
    if compatibility_risk:
        wanted.add("compatibility-reviewer")
        reasons.append("compatibility")
    if state_change:
        wanted.add("implementer")
        wanted.add("evidence-gate")
        reasons.append("state-change")
    if runtime_mismatch:
        wanted.add("runtime-forensics")
        wanted.add("evidence-gate")
        reasons.append("runtime-mismatch")
    if repeated_failure:
        wanted.add("recovery")
        wanted.add("evidence-gate")
        reasons.append("recovery")
    if high_impact:
        wanted.add("evidence-gate")
        reasons.append("high-impact")
    if learning_candidate:
        wanted.add("learning-curator")
        reasons.append("learning")

    # Direct, low-impact requests can stay in the parent. No minimum child count.
    roles = [role for role in ROLE_ORDER if role in wanted]
    return roles, list(dict.fromkeys(reasons))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-json", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    state = json.loads(args.state_json)
    if not isinstance(state, dict):
        raise SystemExit("state must be a JSON object")
    roles, reasons = select_roles(state)
    print(
        json.dumps(
            {
                "schema": 1,
                "roles": roles,
                "count": len(roles),
                "reason_codes": reasons,
                "fixed_agent_count": False,
                "parent_completion_authority": True,
                "default_child_context": "isolated",
            },
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
