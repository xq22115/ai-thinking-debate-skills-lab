#!/usr/bin/env python3
"""Re-anchor every Antigravity invocation to Goal Intelligence v2.

The hook preserves the task's protected Goal Contract while also requiring a live
belief model, semantic-delta handling, and information-gain routing. It changes
routes aggressively when useful, but never silently changes the user's end state.
"""

from __future__ import annotations

import json
import sys


ANCHOR = (
    "GOAL-INTELLIGENCE CONTINUATION: Preserve ROOT_GOAL, GOAL_SIGNATURE, hard constraints, "
    "protected capabilities, target identity, acceptance tests, PREFERENCE_PROFILE, and the "
    "ASSUMPTION_LEDGER. Maintain an evidence/confidence-backed INTENT_BELIEF_GRAPH. When "
    "ambiguity can change a material action, preserve competing interpretations instead of "
    "collapsing to the first plausible reading. Treat each substantive user turn as a semantic "
    "delta: detect refinement, correction, new constraint, priority/entity change, pivot, or "
    "task switch; mark superseded constraints OBSOLETE so stale requirements cannot silently "
    "survive. Choose the next observation by expected decision value: prioritize high-impact, "
    "high-uncertainty facts that best discriminate competing interpretations, adjusted for "
    "observation cost. Prefer reliable tool/runtime/history evidence over asking the user, never "
    "ask the user to repeat known information, and use one discriminating clarification when "
    "human input is genuinely necessary. For research-heavy tasks diversify retrieval across "
    "20+ materially distinct evidence lanes when decision-relevant; repeated keyword variants "
    "do not count, and rare/hidden evidence matters only when it changes the decision, resolves "
    "a contradiction, or exposes a real mechanism/failure mode. A Stop/retry/tool/controller/"
    "permission/capability event is CURRENT_BLOCKER only, not a new mission. Pivot method, tool, "
    "layer, architecture, decomposition, sequencing, or evidence path before pivoting the goal. "
    "Every material action must map to a goal field, critical unknown, or acceptance test. "
    "Completion requires observable read-back/test evidence, a final semantic-goal diff, and no "
    "stale-constraint violation or neighboring-task substitution; self-report alone cannot PASS."
)


def main() -> int:
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        pass

    print(json.dumps({"injectSteps": [{"ephemeralMessage": ANCHOR}]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
