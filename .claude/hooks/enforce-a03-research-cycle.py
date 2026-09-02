#!/usr/bin/env python3
"""Prevent deep A03 research from stopping after one superficial search pass.

This is a structural saturation gate, not a source-count quota. For material or
critical research it requires a minimal falsification loop:

    discover search -> inspect source -> distinct challenge/gap search
    -> inspect a distinct follow-up source

The Stop hook re-evaluates fresh accepted PostToolUse receipts each time Claude
tries to finish. It blocks only while one of those causal stages is missing.
A block is a continuation signal, never a replacement task: ROOT_GOAL and
GOAL_SIGNATURE stay stable, while the hook returns a typed next-action class and
an observable evidence target. Anti-evasion rules live in the always-on policy;
this hook intentionally avoids repeatedly enumerating controller-evasion tactics
inside the continuation message so it does not prime the wrong strategy.
Claude Code itself caps repeated Stop-hook continuations, so this cannot create
an unbounded synthetic delay loop.
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
ACTION_CLASSES = {"ADVANCE", "VERIFY", "RECOVER_ROUTE"}


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


def _block(reason: str, *, action_class: str, evidence_target: str) -> int:
    if action_class not in ACTION_CLASSES:
        action_class = "RECOVER_ROUTE"
    continuation = (
        "GOAL-LOCK CONTINUATION. Preserve ROOT_GOAL and GOAL_SIGNATURE; treat this event only as "
        "CURRENT_BLOCKER. "
        f"NEXT_ACTION_CLASS={action_class}. "
        f"EVIDENCE_TARGET={evidence_target}. "
        f"EXPECTED_PROGRESS_DELTA={reason} "
        "Spend the next material action on that task-directed delta, then re-evaluate the original "
        "acceptance criteria. Activity or wording compliance alone is not progress."
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
            "restore a verifiable runtime binding for the requested reasoning effort before release.",
            action_class="RECOVER_ROUTE",
            evidence_target="quality_runtime_binding",
        )
    audit = os.environ.get("QUALITY_RESEARCH_AUDIT_DIR")
    if not audit:
        return _block(
            "restore or attach a fresh research audit directory that can produce accepted receipts.",
            action_class="RECOVER_ROUTE",
            evidence_target="fresh_research_audit_directory",
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
            "produce one accepted discovery search aimed at the current decision-critical evidence gap.",
            action_class="VERIFY",
            evidence_target="accepted_discovery_search_receipt",
        )

    first_search = searches[0]
    initial_fetches = [
        row for row in fetches
        if int(row["recorded_at_ns"]) > int(first_search["recorded_at_ns"])
    ]
    if not initial_fetches:
        return _block(
            "inspect the strongest current or primary source from the discovery search and obtain an accepted fetch receipt.",
            action_class="VERIFY",
            evidence_target="accepted_primary_source_fetch_receipt",
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
            "produce an accepted materially different search targeting counterevidence, failure modes, conflicting guidance, or the highest-value remaining gap.",
            action_class="VERIFY",
            evidence_target="accepted_counterevidence_or_gap_search_receipt",
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
            "inspect a distinct source from the challenge/gap search and reconcile it with the leading conclusion.",
            action_class="VERIFY",
            evidence_target="accepted_distinct_followup_fetch_receipt",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
