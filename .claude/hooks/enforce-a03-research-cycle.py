#!/usr/bin/env python3
"""Prevent deep A03 research from stopping after one superficial search pass.

This is a structural saturation gate, not a source-count quota. For material or
critical research it requires a minimal falsification loop:

    discover search -> inspect source -> distinct challenge/gap search
    -> inspect a distinct follow-up source

The Stop hook re-evaluates fresh accepted PostToolUse receipts each time Claude
tries to finish. It blocks only while one of those causal stages is missing.
A block is a continuation signal, never a replacement task: the agent must keep
ROOT_GOAL/GOAL_SIGNATURE stable and spend the continuation on the highest-value
goal-advancing action rather than attempting to bypass, kill, weaken, or game
the hook/controller. Claude Code itself caps repeated Stop-hook continuations,
so this cannot create an unbounded synthetic delay loop.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import sys
from urllib.parse import urlsplit, urlunsplit

RESEARCH_ACTOR = "A03"
DEEP_TASK_CLASSES = {"material", "critical"}
WEB_TOOLS = {"WebSearch", "WebFetch"}
EFFORT_LEVELS = {"low", "medium", "high", "xhigh", "max"}


def _normalize_query(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _normalize_url(value: object) -> str:
    text = str(value or "").strip()
    if not text.startswith(("http://", "https://")):
        return ""
    parts = urlsplit(text)
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def _accepted(row: dict, expected_effort: str) -> bool:
    return (
        row.get("schemaVersion") == 2
        and row.get("actor_id") == RESEARCH_ACTOR
        and row.get("hook_event_name") == "PostToolUse"
        and row.get("tool_name") in WEB_TOOLS
        and row.get("post_tool_success") is True
        and row.get("quality_evidence_accepted") is True
        and row.get("requested_effort") == expected_effort
        and row.get("effective_effort") == expected_effort
        and row.get("effort_readback_source") in {"hook_payload", "CLAUDE_EFFORT"}
        and isinstance(row.get("recorded_at_ns"), int)
        and row.get("recorded_at_ns", 0) > 0
    )


def _receipts(audit_root: pathlib.Path, expected_effort: str) -> list[dict]:
    actor_dir = audit_root / RESEARCH_ACTOR
    rows: list[dict] = []
    if not actor_dir.is_dir():
        return rows
    for path in actor_dir.glob("*.json"):
        try:
            row = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(row, dict) and _accepted(row, expected_effort):
            rows.append(row)
    return sorted(rows, key=lambda row: int(row["recorded_at_ns"]))


def _block(reason: str) -> int:
    continuation = (
        "Preserve ROOT_GOAL and GOAL_SIGNATURE. This Stop hook is a blocker signal, not a new task target. "
        "Do not inspect, exploit, bypass, kill, weaken, or game the hook/controller to escape the work. "
        "Do not substitute agent headcount, refusal/policy/ethics debate, or lower effort/tests for task progress. "
        "Continue with the highest-value goal-advancing action available under the current constraints. "
        + reason
    )
    print(json.dumps({
        "decision": "block",
        "reason": continuation,
    }))
    return 0


def main() -> int:
    if os.environ.get("CONTROL_PLANE_ACTOR_ID") != RESEARCH_ACTOR:
        return 0
    task_class = str(os.environ.get("QUALITY_TASK_CLASS") or "")
    if task_class not in DEEP_TASK_CLASSES:
        return 0
    expected_effort = str(os.environ.get("CLAUDE_CODE_EFFORT_LEVEL") or "")
    if expected_effort not in EFFORT_LEVELS:
        return _block(
            "Deep research cannot finish because the expected reasoning effort is not runtime-bound. "
            "Restore the quality runtime binding before stopping."
        )
    audit = os.environ.get("QUALITY_RESEARCH_AUDIT_DIR")
    if not audit:
        return _block(
            "Deep research cannot finish because the fresh research audit directory is detached."
        )

    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        hook_input = {}
    if isinstance(hook_input, dict) and hook_input.get("hook_event_name") not in (None, "Stop"):
        return 0

    rows = _receipts(pathlib.Path(audit), expected_effort)
    searches = [row for row in rows if row.get("tool_name") == "WebSearch" and _normalize_query(row.get("query"))]
    fetches = [row for row in rows if row.get("tool_name") == "WebFetch" and _normalize_url(row.get("url"))]

    if not searches:
        return _block(
            "Research is not saturated: no accepted WebSearch exists. Search specifically for the "
            "decision-critical evidence gap before finishing; elapsed time is not evidence."
        )

    first_search = searches[0]
    initial_fetches = [
        row for row in fetches
        if int(row["recorded_at_ns"]) > int(first_search["recorded_at_ns"])
    ]
    if not initial_fetches:
        return _block(
            "Research is not saturated: the discovery search was not followed by inspection of a "
            "source. Use WebFetch on the strongest current/primary source before finishing."
        )

    first_fetch = initial_fetches[0]
    prior_queries = {
        _normalize_query(row.get("query"))
        for row in searches
        if int(row["recorded_at_ns"]) <= int(first_fetch["recorded_at_ns"])
    }
    challenge_searches = [
        row for row in searches
        if int(row["recorded_at_ns"]) > int(first_fetch["recorded_at_ns"])
        and _normalize_query(row.get("query")) not in prior_queries
    ]
    if not challenge_searches:
        return _block(
            "Research is not saturated after the first inspected source. Run a materially different "
            "WebSearch targeting counterevidence, failure modes, conflicting guidance, or a remaining "
            "decision-critical gap; repeating the same query does not count."
        )

    challenge = challenge_searches[0]
    prior_urls = {
        _normalize_url(row.get("url"))
        for row in fetches
        if int(row["recorded_at_ns"]) < int(challenge["recorded_at_ns"])
    }
    followup_fetches = [
        row for row in fetches
        if int(row["recorded_at_ns"]) > int(challenge["recorded_at_ns"])
        and _normalize_url(row.get("url")) not in prior_urls
    ]
    if not followup_fetches:
        return _block(
            "Research is not saturated: the challenge/gap search has not been inspected through a "
            "distinct follow-up source. Fetch the best source from that challenge search, reconcile "
            "it with the leading conclusion, and continue further if a critical unknown remains."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
