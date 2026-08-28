#!/usr/bin/env python3
"""Record successful Claude Code web-tool calls as fresh runtime evidence.

PostToolUse invokes this script only after a matching tool succeeds. The audit
location is supplied by the quality-bound workflow so receipts cannot be reused
across runs accidentally. No page contents are persisted; only call metadata,
effective reasoning effort, ordering metadata, and a response hash are recorded.

A web call is accepted as quality evidence only when the hook reads back the
same effective effort that the quality workflow requested. Organization effort
caps, model capability downgrades, unsupported effort, or detached runtime
binding therefore produce a rejected receipt instead of false PASS evidence.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import sys
import time

WEB_TOOLS = {"WebSearch", "WebFetch"}
EFFORT_LEVELS = {"low", "medium", "high", "xhigh", "max"}


def _safe(value: object, fallback: str) -> str:
    text = str(value or fallback)
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text)[:180] or fallback


def _effective_effort(payload: dict) -> tuple[str, str]:
    effort = payload.get("effort")
    if isinstance(effort, dict):
        level = str(effort.get("level") or "")
        if level:
            return level, "hook_payload"
    inherited = str(os.environ.get("CLAUDE_EFFORT") or "")
    if inherited:
        return inherited, "CLAUDE_EFFORT"
    return "", "missing"


def _write_json(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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
    requested_effort = str(os.environ.get("CLAUDE_CODE_EFFORT_LEVEL") or "")
    effective_effort, effort_source = _effective_effort(payload)

    common = {
        "schemaVersion": 2,
        "actor_id": actor,
        "hook_event_name": str(payload.get("hook_event_name") or "PostToolUse"),
        "tool_name": tool_name,
        "tool_use_id": str(payload.get("tool_use_id") or ""),
        "session_id": str(payload.get("session_id") or ""),
        "duration_ms": payload.get("duration_ms"),
        "recorded_at_ns": time.time_ns(),
        "query": str(tool_input.get("query") or "") if tool_name == "WebSearch" else "",
        "url": str(tool_input.get("url") or "") if tool_name == "WebFetch" else "",
        "tool_response_sha256": hashlib.sha256(response_bytes).hexdigest(),
        "requested_effort": requested_effort,
        "effective_effort": effective_effort,
        "effort_readback_source": effort_source,
        "post_tool_success": True,
    }

    rejection_reason = ""
    if requested_effort not in EFFORT_LEVELS:
        rejection_reason = "requested_effort_missing_or_invalid"
    elif effective_effort not in EFFORT_LEVELS:
        rejection_reason = "effective_effort_missing_or_unsupported"
    elif effective_effort != requested_effort:
        rejection_reason = "effective_effort_mismatch"

    if rejection_reason:
        rejected = dict(common)
        rejected["quality_evidence_accepted"] = False
        rejected["rejection_reason"] = rejection_reason
        _write_json(
            pathlib.Path(audit_root) / "_rejected" / actor / f"{tool_use_id}.json",
            rejected,
        )
        return 0

    receipt = dict(common)
    receipt["quality_evidence_accepted"] = True
    _write_json(
        pathlib.Path(audit_root) / actor / f"{tool_use_id}.json",
        receipt,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
