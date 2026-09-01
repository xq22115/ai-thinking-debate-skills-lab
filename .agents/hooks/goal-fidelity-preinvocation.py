#!/usr/bin/env python3
"""Re-anchor Antigravity continuations to the user's Goal Contract.

Antigravity PreInvocation hooks can inject ephemeral system context before each
model call. We keep the first invocation untouched because the always-on rule
already establishes the contract, then re-anchor later invocations where Stop,
retry, tool failures, subagent results, or other controller events can otherwise
become a replacement objective.
"""

from __future__ import annotations

import json
import sys


ANCHOR = (
    "GOAL-LOCK CONTINUATION: Preserve the user's active ROOT_GOAL, GOAL_SIGNATURE, "
    "hard constraints, protected capabilities, target identity, and acceptance tests. "
    "A Stop/retry/tool/controller/permission/capability event is CURRENT_BLOCKER only; "
    "do not promote escaping, exploiting, bypassing, killing, weakening, or gaming that "
    "controller into the mission merely to terminate. Spend this invocation on the "
    "highest-value goal-advancing action still available; pivot method/layer/instrument/"
    "decomposition before pivoting the goal. Do not substitute agent headcount, generic "
    "refusal/policy debate, fabricated runtime independence, or lower reasoning effort, "
    "agent budget, tests, acceptance criteria, or protected capabilities for progress. "
    "Count a subagent only when it adds a unique contribution mapped to the Goal Contract. "
    "Completion requires observable owning-runtime evidence, not self-report."
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        payload = {}

    invocation_num = payload.get("invocationNum") if isinstance(payload, dict) else None
    if isinstance(invocation_num, int) and invocation_num <= 0:
        print(json.dumps({"injectSteps": []}))
        return 0

    print(json.dumps({
        "injectSteps": [
            {"ephemeralMessage": ANCHOR}
        ]
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
