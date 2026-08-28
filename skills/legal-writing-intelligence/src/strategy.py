#!/usr/bin/env python3
"""Deterministic strategy preflight for high-stakes legal/business correspondence.

This module does not decide legal rights. It tests whether a proposed letter has the
record, decision architecture, scoped signaling and evidence bridges that sophisticated
counsel/executive correspondence normally needs before prose polishing begins.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SIGNALS_PATH = ROOT / "resources" / "signals.json"


def _clean(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _truthy_text(value: Any) -> bool:
    return bool(_clean(value))


def load_signals(path: Path = SIGNALS_PATH) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    signals = data.get("signals", [])
    return {str(item["id"]): item for item in signals}


def _add_flag(
    flags: list[dict[str, str]], code: str, severity: str, message: str
) -> None:
    if not any(item["code"] == code for item in flags):
        flags.append({"code": code, "severity": severity, "message": message})


def _recommend(
    out: list[dict[str, Any]],
    library: dict[str, dict[str, Any]],
    sid: str,
    reason: str,
) -> None:
    item = library[sid]
    out.append(
        {
            "id": sid,
            "template": item["template"],
            "function": item["function"],
            "reason": reason,
            "preconditions": item.get("preconditions", []),
            "misuse": item.get("misuse", ""),
        }
    )


def analyze(
    payload: dict[str, Any], signals_path: Path = SIGNALS_PATH
) -> dict[str, Any]:
    library = load_signals(signals_path)
    mode = str(payload.get("mode", "executive-counsel"))
    facts = [x for x in payload.get("facts", []) if _truthy_text(x)]
    asks = [x for x in payload.get("asks", []) if _truthy_text(x)]
    deadline = _clean(payload.get("deadline"))
    timezone = _clean(payload.get("timezone"))
    disputed = bool(payload.get("disputed"))
    conditions = [x for x in payload.get("conditions", []) if _truthy_text(x)]
    consequences = [
        x for x in payload.get("consequences", []) if _truthy_text(x)
    ]
    reserve_rights = bool(payload.get("reserve_rights")) or mode == "reservation-of-rights"
    reservation_scope = _clean(payload.get("reservation_scope"))

    flags: list[dict[str, str]] = []
    gaps: list[str] = []
    recommendations: list[dict[str, Any]] = []

    if not facts:
        _add_flag(
            flags,
            "NO_DECISION_RECORD",
            "high",
            "No decision-relevant factual record was supplied.",
        )
        gaps.append("decision-relevant facts/dates/documents")
    if not asks:
        _add_flag(
            flags,
            "NO_ACTION_ASK",
            "high",
            "No explicit action or decision request was supplied.",
        )
        gaps.append("specific requested action/decision")
    if asks and not deadline:
        _add_flag(
            flags,
            "ASK_WITHOUT_DEADLINE",
            "medium",
            "The letter asks for action but creates no auditable decision deadline.",
        )
    if deadline and not timezone and any(
        token in deadline.lower() for token in ("am", "pm", ":", "a.m.", "p.m.")
    ):
        _add_flag(
            flags,
            "DEADLINE_WITHOUT_TIMEZONE",
            "medium",
            "A clock-time deadline is present without an explicit timezone.",
        )
    if consequences and not asks:
        _add_flag(
            flags,
            "CONSEQUENCE_WITHOUT_CURE_PATH",
            "high",
            "A consequence is stated without a corresponding requested cure/action.",
        )

    if disputed:
        _recommend(
            recommendations,
            library,
            "current-record",
            "The matter is disputed; anchor conclusions to the current evidence set.",
        )
        _recommend(
            recommendations,
            library,
            "reject-premise",
            "Use only if the counterparty's framing itself is disputed.",
        )
    if conditions:
        _recommend(
            recommendations,
            library,
            "subject-to",
            "The payload contains real conditions that should remain visibly conditional.",
        )
    if payload.get("hypothetical_branch"):
        _recommend(
            recommendations,
            library,
            "discussion-only",
            "A hypothetical branch is being tested without adoption.",
        )
    if payload.get("alternative_argument"):
        _recommend(
            recommendations,
            library,
            "without-conceding",
            "An alternative position is advanced while a primary disagreement remains.",
        )
    if payload.get("trade_space"):
        _recommend(
            recommendations,
            library,
            "prepared-to",
            "The sender intends to signal controlled negotiating flexibility.",
        )
    if asks and deadline:
        _recommend(
            recommendations,
            library,
            "confirm-by",
            "The requested action can be turned into an auditable decision point.",
        )
    if consequences:
        _recommend(
            recommendations,
            library,
            "absent-confirmation",
            "A real next step is available if the requested action is not taken.",
        )
    if payload.get("executive_escalation"):
        _recommend(
            recommendations,
            library,
            "executive-attention",
            "Operational resolution is exhausted and a defined executive decision is needed.",
        )
    if payload.get("record_marker"):
        _recommend(
            recommendations,
            library,
            "for-record",
            "A verified contemporaneous fact/position should be marked for future readers.",
        )

    if reserve_rights:
        if not reservation_scope:
            _add_flag(
                flags,
                "UNSCOPED_RESERVATION",
                "high",
                "Rights-preservation wording was requested without naming the position to preserve.",
            )
            gaps.append("reservation_scope")
        else:
            _recommend(
                recommendations,
                library,
                "scoped-reservation",
                "Practical engagement continues while a specific position must remain open.",
            )

    deal = payload.get("deal") or {}
    if mode == "deal-negotiation" or deal:
        agreed = deal.get("agreed") or []
        open_items = deal.get("open") or []
        risk_allocation = _clean(deal.get("risk_allocation"))
        trade_space = deal.get("trade_space") or payload.get("trade_space")
        if not agreed:
            _add_flag(
                flags,
                "DEAL_AGREED_SET_MISSING",
                "medium",
                "The draft does not distinguish settled points from open points.",
            )
        if not open_items:
            _add_flag(
                flags,
                "DEAL_OPEN_SET_MISSING",
                "medium",
                "The remaining decision points are not enumerated.",
            )
        if not risk_allocation:
            _add_flag(
                flags,
                "DEAL_RISK_ALLOCATION_MISSING",
                "high",
                "The commercial/legal risk allocation at issue is not stated.",
            )
        if trade_space:
            _recommend(
                recommendations,
                library,
                "principle-v-risk",
                "Separate conceptual agreement from the remaining allocation of risk.",
            )
        if deal.get("package_proposal"):
            if not _truthy_text(deal.get("package_dependency")):
                _add_flag(
                    flags,
                    "PACKAGE_DEPENDENCY_UNSTATED",
                    "high",
                    "A package proposal is asserted without identifying which concessions are interdependent.",
                )
            else:
                _recommend(
                    recommendations,
                    library,
                    "package-proposal",
                    "Linked concessions should not be read as standalone agreements.",
                )
        if deal.get("prior_commercial_allocation_date"):
            _recommend(
                recommendations,
                library,
                "commercial-alignment",
                "A reliable prior commercial allocation can anchor the drafting position.",
            )

    project = payload.get("project_claim") or {}
    if mode == "project-escalation" or project:
        required = {
            "event": "project event",
            "mechanism": "governing contractual/project mechanism",
            "notice_record": "notice/contemporaneous record",
            "causation": "causation bridge",
            "schedule_effect": "schedule/critical-path effect",
            "mitigation": "mitigation actually attempted",
            "instruction_requested": "specific instruction/decision requested",
        }
        for key, label in required.items():
            if not _truthy_text(project.get(key)):
                gaps.append(label)
                _add_flag(
                    flags,
                    f"PROJECT_{key.upper()}_MISSING",
                    "high",
                    f"Major-project claim architecture is missing: {label}.",
                )
        if project.get("seeks_money") and not _truthy_text(project.get("cost_effect")):
            _add_flag(
                flags,
                "PROJECT_QUANTUM_GAP",
                "high",
                "A monetary position is contemplated without a stated cost/quantum evidence bridge.",
            )
            gaps.append("cost/quantum support")
        if _truthy_text(project.get("event")) and not _truthy_text(
            project.get("causation")
        ):
            _add_flag(
                flags,
                "EVENT_IS_NOT_CAUSATION",
                "high",
                "The draft risks treating occurrence of an event as proof of delay/impact causation.",
            )
        if _truthy_text(project.get("schedule_effect")) and not _truthy_text(
            project.get("causation")
        ):
            _add_flag(
                flags,
                "SCHEDULE_EFFECT_WITHOUT_CAUSATION",
                "high",
                "A schedule effect is asserted without explaining the causal bridge to the event.",
            )

    privilege = payload.get("privilege") or {}
    if privilege.get("label_privileged"):
        if not privilege.get("legal_advice_purpose"):
            _add_flag(
                flags,
                "PRIVILEGE_LABEL_WITHOUT_LEGAL_PURPOSE",
                "high",
                "A privilege label is requested without an identified legal-advice purpose.",
            )
        if privilege.get("third_party_recipients") and not _truthy_text(
            privilege.get("confidentiality_basis")
        ):
            _add_flag(
                flags,
                "PRIVILEGE_DISTRIBUTION_RISK",
                "high",
                "Third-party distribution is present without an identified basis for preserving confidentiality/protection.",
            )
        _add_flag(
            flags,
            "PRIVILEGE_JURISDICTION_CHECK",
            "info",
            "Privilege is fact- and jurisdiction-dependent; a label or copied lawyer is not dispositive.",
        )

    settlement = payload.get("settlement") or {}
    if settlement.get("rule_408_label") or settlement.get("without_prejudice_label"):
        if not settlement.get("disputed_claim"):
            _add_flag(
                flags,
                "SETTLEMENT_LABEL_WITHOUT_DISPUTED_CLAIM",
                "high",
                "Settlement-style labeling is requested without identifying a disputed claim.",
            )
        if not settlement.get("compromise_purpose"):
            _add_flag(
                flags,
                "SETTLEMENT_CONTEXT_UNCLEAR",
                "medium",
                "The communication's compromise/settlement purpose is not established.",
            )
        _add_flag(
            flags,
            "SETTLEMENT_EFFECT_NOT_GUARANTEED",
            "info",
            "Do not promise that a label makes the communication inadmissible or protected for every purpose/regime.",
        )

    if payload.get("clarification_needed"):
        _recommend(
            recommendations,
            library,
            "avoid-doubt",
            "A specific interpretive ambiguity needs to be closed.",
        )
    if payload.get("narrow_issue_only"):
        _recommend(
            recommendations,
            library,
            "present-purpose",
            "The writer intends to address a narrow issue while leaving broader matters open.",
        )

    hard = [flag for flag in flags if flag["severity"] == "high"]
    firmness = 1
    if disputed:
        firmness = 2
    if reserve_rights:
        firmness = max(firmness, 3)
    if consequences:
        firmness = max(firmness, 4)

    return {
        "status": "READY" if not hard else "REVISE",
        "mode": mode,
        "firmness_level": firmness,
        "architecture": {
            "bottom_line": _clean(payload.get("purpose")),
            "record_items": len(facts),
            "issue": _clean(payload.get("issue")),
            "position": _clean(payload.get("position")),
            "consequences": consequences,
            "asks": asks,
            "deadline": deadline,
            "path_forward": _clean(payload.get("path_forward")),
        },
        "risk_flags": flags,
        "evidence_gaps": list(dict.fromkeys(gaps)),
        "signal_recommendations": recommendations,
        "hostile_read": {
            "recipient": "Can the recipient identify the exact decision/action and deadline?",
            "opposing_counsel": "Which sentence could be quoted as an unintended admission, waiver, promise or concession?",
            "board_auditor": "Can a future reviewer reconstruct who knew what, when, and from which record?",
            "neutral_fact_finder": "Are facts, allegations, assumptions, causation and conclusions visibly separated?",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = analyze(payload)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result["status"] == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
