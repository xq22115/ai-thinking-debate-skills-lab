#!/usr/bin/env python3
"""Re-anchor every invocation to Goal Intelligence v2.

Inject a compact task-understanding contract on every invocation so long-running
work keeps the user's operative goal, current intent belief state, decision-critical
unknowns, and acceptance evidence aligned even after route changes or context churn.
"""

from __future__ import annotations

import json
import sys


ANCHOR = (
    "GOAL-INTELLIGENCE V2: Preserve the active ROOT_GOAL, GOAL_SIGNATURE, hard constraints, "
    "protected capabilities, target identity, and acceptance tests. Maintain a compact "
    "INTENT_BELIEF_GRAPH with evidence/confidence, an ASSUMPTION_LEDGER, and up to three "
    "materially different CANDIDATE_GOALS when ambiguity can change the action. Treat the "
    "latest user turn as a semantic delta: detect refinement, correction, new constraint, "
    "target change, priority change, related pivot, or full task switch; mark superseded "
    "constraints OBSOLETE instead of letting stale requirements survive. Before the next "
    "material action, choose the observation/tool call with the highest expected decision "
    "value: impact-if-wrong × uncertainty × discrimination power, adjusted for observation "
    "cost. Prefer reliable tool/runtime/history evidence over asking the user. If human "
    "clarification is genuinely necessary, ask the smallest question that best separates "
    "remaining candidate goals; never ask the user to repeat known information. Map every "
    "material action to a goal node, hard constraint, decision-critical unknown, or acceptance "
    "test; otherwise treat it as non-progress. For research-heavy work, diversify retrieval "
    "across source, config, releases, commits, issues, PRs, tests, benchmarks, papers, maintainer "
    "design notes, practitioner evidence, postmortems, negative evidence, reverted approaches, "
    "version conflicts, competing implementations, reverse search, prompt/config archaeology, "
    "and niche citation/maintainer-linked signals; obscurity alone is not quality. A blocker is "
    "CURRENT_BLOCKER, not a replacement mission. Change route before changing the user's end "
    "state. Completion requires observable acceptance evidence and, when practical, an "
    "independent audit against the original Goal Contract; self-report alone cannot PASS."
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
