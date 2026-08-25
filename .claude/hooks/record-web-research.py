#!/usr/bin/env python3
"""Record successful Claude Code web-tool calls as fresh runtime evidence.

PostToolUse invokes this script only after a matching tool succeeds. The audit
location is supplied by the quality-bound workflow so receipts cannot be reused
across runs accidentally. No page contents are persisted; only call metadata
and a response hash are recorded.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import sys

WEB_TOOLS = {"WebSearch", "WebFetch"}


def _safe(value: object, fallback: str) -> str:
    text = str(value or fallback)
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text)[:180] or fallback


def main() -> int:
    audit_root = os.environ.get("QUALITY_RESEARCH_AUDIT_DIR")
    actor_id = os.environ.get("CONTROL_PLANE_ACTOR_ID")
    if not audit_root or not actor_id:
        return 0
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    if not isinstance(payload, dict):
        return 0
    tool_name = str(payload.get("tool_name") or "")
    if tool_name not in WEB_TOOLS:
        return 0

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}
    tool_response = payload.get("tool_response")
    response_bytes = json.dumps(
        tool_response, ensure_ascii=False, sort_keys=True, default=str
    ).encode("utf-8")
    tool_use_id = _safe(payload.get("tool_use_id"), "unknown-tool-use")
    actor = _safe(actor_id, "UNKNOWN")

    receipt = {
        "schemaVersion": 1,
        "actor_id": actor,
        "hook_event_name": str(payload.get("hook_event_name") or "PostToolUse"),
        "tool_name": tool_name,
        "tool_use_id": str(payload.get("tool_use_id") or ""),
        "session_id": str(payload.get("session_id") or ""),
        "duration_ms": payload.get("duration_ms"),
        "query": str(tool_input.get("query") or "") if tool_name == "WebSearch" else "",
        "url": str(tool_input.get("url") or "") if tool_name == "WebFetch" else "",
        "tool_response_sha256": hashlib.sha256(response_bytes).hexdigest(),
        "post_tool_success": True,
    }
    target = pathlib.Path(audit_root) / actor
    target.mkdir(parents=True, exist_ok=True)
    path = target / f"{tool_use_id}.json"
    path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
