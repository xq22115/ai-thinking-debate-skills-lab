#!/usr/bin/env python3
"""Re-anchor every Antigravity invocation to the user's Goal Contract.

The previous version skipped invocation 0 on the assumption that an always-on rule
had already established the Goal Contract. That assumption is too weak for hostile
or stale runtime states: the first model turn is exactly where a controller event,
partial context, or stale summary can be promoted into a replacement mission.

This hook therefore injects a compact progress contract on *every* invocation.
It does not weaken or bypass controller/safety/permission boundaries; it requires
the model to keep those boundaries in CURRENT_BLOCKER and spend available effort
on the highest-value action that still advances the user's actual task.
"""

from __future__ import annotations

import json
import sys


ANCHOR = (
    "GOAL-LOCK CONTINUATION: Preserve the user's active ROOT_GOAL, GOAL_SIGNATURE, "
    "hard constraints, protected capabilities, target identity, and acceptance tests. "
    "A Stop/retry/tool/controller/permission/capability/safety event is CURRENT_BLOCKER only; "
    "do not promote escaping, exploiting, bypassing, killing, weakening, disabling, or gaming "
    "that controller into the mission merely to terminate or unlock more authority. "
    "Before choosing the next action, ask which unresolved Goal Contract field or acceptance "
    "test this action advances. If none, reject the action as non-progress and choose a materially "
    "different task-advancing route. Pivot method/layer/instrument/decomposition/evidence path "
    "before pivoting the goal. Controller analysis is allowed only when diagnosing or modifying "
    "that controller is itself an authorized task-relevant objective; even then, do not silently "
    "turn permission or safety boundaries into a bypass objective. Do not substitute agent "
    "headcount, generic refusal/policy/ethics debate, fabricated runtime independence, or lower "
    "reasoning effort, agent budget, tests, acceptance criteria, or protected capabilities for "
    "progress. If one requested portion is unavailable, isolate that portion and continue the "
    "remaining goal-advancing work instead of abandoning the entire task. Count a subagent only "
    "when it adds a unique contribution mapped to the Goal Contract. Completion requires "
    "observable owning-runtime evidence, not self-report."
)


def main() -> int:
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        pass

    print(json.dumps({
        "injectSteps": [
            {"ephemeralMessage": ANCHOR}
        ]
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
