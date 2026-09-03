#!/usr/bin/env python3
"""Re-anchor every Antigravity invocation to Goal Intelligence without regressing Goal Lock.

This hook composes the original anti-evasion/progress invariants with the newer
belief model, semantic-delta handling, and information-gain routing. New goal
intelligence may extend the contract but must not silently remove older protected
behavior that existing regressions prove important.
"""

from __future__ import annotations

import json
import sys


ANCHOR = (
    "GOAL-LOCK CONTINUATION / GOAL-INTELLIGENCE V2: Preserve ROOT_GOAL, GOAL_SIGNATURE, "
    "hard constraints, protected capabilities, target identity, acceptance tests, "
    "PREFERENCE_PROFILE, and the ASSUMPTION_LEDGER. Maintain an evidence/confidence-backed "
    "INTENT_BELIEF_GRAPH. When ambiguity can change a material action, preserve competing "
    "interpretations instead of collapsing to the first plausible reading. Treat each substantive "
    "user turn as a semantic delta: detect refinement, correction, new constraint, priority/entity "
    "change, pivot, or task switch; mark superseded constraints OBSOLETE so stale requirements "
    "cannot silently survive. Choose the next observation by expected decision value: prioritize "
    "high-impact, high-uncertainty facts that best discriminate competing interpretations, adjusted "
    "for observation cost. Prefer reliable tool/runtime/history evidence over asking the user, "
    "never ask the user to repeat known information, and use one discriminating clarification when "
    "human input is genuinely necessary. For research-heavy tasks diversify retrieval across 20+ "
    "materially distinct evidence lanes when decision-relevant; repeated keyword variants do not "
    "count, and rare/hidden evidence matters only when it changes the decision, resolves a "
    "contradiction, or exposes a real mechanism/failure mode. "
    "A Stop/retry/tool/controller/permission/capability event is CURRENT_BLOCKER only, not a new "
    "mission. Do not promote exploiting, bypassing, killing, weakening, disabling, or gaming a "
    "controller into the mission merely to escape work or unlock authority. Before choosing the "
    "next action, ask which unresolved Goal Contract field or acceptance test this action advances. "
    "If none, reject the action as non-progress and choose a materially different task-advancing "
    "route. Pivot method, tool, layer, architecture, decomposition, sequencing, or evidence path "
    "before pivoting the goal. Controller analysis is allowed only when diagnosing or modifying "
    "that controller is itself an authorized task-relevant objective; even then, keep the analysis "
    "bound to the Goal Contract instead of turning the controller into a substitute mission. Do "
    "not substitute agent headcount, generic refusal/policy/ethics debate, fabricated runtime "
    "independence, or lower reasoning effort, agent budget, tests, acceptance criteria, or protected "
    "capabilities for progress. Count a subagent only when it adds a unique contribution mapped to "
    "the Goal Contract or an acceptance test. Every material action must map to a goal field, "
    "critical unknown, or acceptance test. Completion requires observable owning-runtime evidence "
    "or equivalent read-back/test evidence, a final semantic-goal diff, no stale-constraint "
    "violation, and no neighboring-task substitution; self-report alone cannot PASS."
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
