#!/usr/bin/env python3
"""Deterministic high-stakes legal/business letter compiler.

No model/API is required. It deliberately uses a constrained, reviewable drafting pattern
rather than pretending to provide legal advice or to impersonate a named lawyer.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

MODES = {"executive-counsel", "deal-negotiation", "project-escalation", "reservation-of-rights"}


def _clean(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def validate_payload(payload: dict[str, Any]) -> None:
    required = ["matter", "purpose", "facts", "asks"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")
    mode = payload.get("mode", "executive-counsel")
    if mode not in MODES:
        raise ValueError(f"unsupported mode: {mode}")
    if not isinstance(payload["facts"], list) or not isinstance(payload["asks"], list):
        raise ValueError("facts and asks must be arrays")


def draft_letter(payload: dict[str, Any]) -> str:
    validate_payload(payload)
    matter = _clean(payload["matter"])
    purpose = _clean(payload["purpose"])
    mode = payload.get("mode", "executive-counsel")
    recipient = _clean(payload.get("recipient", "Counsel"))
    deadline = _clean(payload.get("deadline"))
    conditions = [_clean(x) for x in payload.get("conditions", []) if _clean(x)]
    facts = [_clean(x) for x in payload["facts"] if _clean(x)]
    asks = [_clean(x) for x in payload["asks"] if _clean(x)]
    disputed = bool(payload.get("disputed"))
    reserve_rights = bool(payload.get("reserve_rights"))

    lines = [f"Subject: {matter}", "", f"{recipient},", "", f"We write regarding {matter}. {purpose}"]

    if facts:
        lines += ["", "For present purposes, the relevant record is straightforward:"]
        lines += [f"- {fact}" for fact in facts]

    if disputed:
        lines += ["", "We do not accept any characterization inconsistent with the record above. On the current record, our position is as follows."]
    else:
        lines += ["", "Against that backdrop, our position is as follows."]

    if conditions:
        lines.append("Any proposed path forward is subject to " + "; ".join(conditions) + ".")

    if mode == "deal-negotiation":
        lines.append("We remain prepared to pursue a commercially workable resolution, provided the agreed allocation of risk and the operative documents remain aligned.")
    elif mode == "project-escalation":
        lines.append("The immediate objective is to protect the critical path while preserving the parties' respective contractual positions.")
    elif mode == "reservation-of-rights":
        lines.append("Our participation in further discussions should not be construed as acceptance of the present position or as a waiver of any available right or remedy.")

    lines += ["", "Accordingly, please:"]
    lines += [f"{idx}. {ask}" for idx, ask in enumerate(asks, 1)]
    if deadline:
        lines += ["", f"Please confirm the foregoing by {deadline}."]

    if reserve_rights:
        lines += ["", "Nothing in this correspondence constitutes an admission, waiver, amendment, or election of remedies. All rights and remedies are expressly reserved."]

    lines += ["", "We would welcome a focused discussion if it will resolve the remaining points promptly.", ""]
    return "\n".join(lines)


def compile_prompt(payload: dict[str, Any]) -> str:
    """Create a model-agnostic prompt if the user later routes drafting through an LLM."""
    validate_payload(payload)
    return (
        "Draft a high-stakes U.S. legal-business letter using public professional conventions, "
        "not the personal style of any named lawyer. Use controlled, concise partner-level prose. "
        "Separate record, position, conditions, asks, deadlines, and rights reservations. Avoid fake "
        "privilege labels, empty threats, decorative legalese, invented facts, and unsupported legal conclusions.\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--prompt", action="store_true", help="emit a model-agnostic drafting prompt")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    print(compile_prompt(payload) if args.prompt else draft_letter(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
