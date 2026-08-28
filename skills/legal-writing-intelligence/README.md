# Legal Writing Intelligence

A GitHub-native skill that keeps three jobs in one evidence chain: **current legal-AI writing research**, **high-stakes correspondence strategy preflight**, and **controlled U.S. legal/business drafting**.

## What is implemented

- 10 independent research branches (`agent-01` … `agent-10`), each with a distinct vendor, query and official source set.
- A June–August 2026 evidence ledger containing exactly 10 legal-writing/drafting releases with exact-day dates.
- Keyless discovery through Bing News RSS plus official-page re-fetch, redirect destination capture, fetch timestamp and SHA-256 fingerprinting.
- A fail-closed adjudicator that rejects duplicate/missing agents, vendor identity drift, non-official URLs, cross-domain redirects, partial dates, partial verification status, missing writing relevance, out-of-window releases, or inability to re-fetch at least one official source for every live agent.
- A deterministic strategy preflight (`src/strategy.py`) that checks the letter's record, decision architecture, evidence bridges, signal-language preconditions, project causation chain, deal package logic, privilege/settlement labeling risk, and four-way hostile read **before** prose polishing.
- A machine-readable signal library (`resources/signals.json`) that treats apparent “insider language” as functional switches with explicit preconditions and misuse warnings—not secret codes.
- An authority ledger (`resources/authority-ledger.json`) recording the mechanism, intended engine use and limitation of public sources used to shape the strategy rules.
- A deterministic U.S. legal-business letter compiler (`src/writer.py`) that does not require an LLM/API.
- Scoped reservation language: `reserve_rights` or `reservation-of-rights` mode requires an explicit `reservation_scope`; the compiler does not spray blanket non-waiver boilerplate into a letter.
- GitHub Actions research at minutes `7,22,37,52` of every hour plus push/manual execution, ten worker artifacts, and one adjudicated artifact.

## Run locally

```bash
python -m unittest discover -s skills/legal-writing-intelligence/tests -p 'test_*.py' -v
python skills/legal-writing-intelligence/src/research.py --agent agent-01 --out /tmp/agent-01.json
python skills/legal-writing-intelligence/src/strategy.py input.json --out /tmp/strategy.json
python skills/legal-writing-intelligence/src/writer.py input.json
```

The strategy preflight exits `0` for `READY` and `2` for `REVISE`, so it can be used as a fail-closed gate before drafting/sending.

## Strategy input model

A minimal executive letter can use:

```json
{
  "matter": "Project Falcon — Milestone 4",
  "purpose": "Obtain written confirmation of the recovery decision.",
  "mode": "executive-counsel",
  "facts": ["The steering committee deferred the decision on August 27, 2026."],
  "asks": ["Confirm the accountable executive and approved recovery action."],
  "deadline": "August 29, 2026 at 5:00 p.m.",
  "timezone": "New York time"
}
```

A major-project escalation should additionally separate the proof chain instead of collapsing it into “delay occurred”:

```json
{
  "mode": "project-escalation",
  "project_claim": {
    "event": "Late IFC drawing issued August 20.",
    "mechanism": "Drawing release/interface dependency under the governing contract.",
    "notice_record": "Notice N-104 and contemporaneous daily records.",
    "causation": "The drawing prevented release of fabrication package FP-12, whose successor installation activity had no available float in the current accepted schedule.",
    "schedule_effect": "The current analysis identifies a five-day effect to milestone M4, subject to update.",
    "mitigation": "Unaffected fabrication was resequenced and a second review shift added.",
    "instruction_requested": "Confirm the revised IFC release sequence and responsible owner.",
    "seeks_money": true,
    "cost_effect": "Cost records are being segregated by affected resource and period."
  }
}
```

The engine deliberately treats these as different proof layers:

`event → mechanism → notice/record → causation → schedule effect → cost/quantum → mitigation → requested instruction → any scoped reservation`

An event is **not** automatically proof of causation, critical-path delay, cost or entitlement.

## Deal / board-level strategy

For `deal-negotiation`, use a structured `deal` object to separate:

- `agreed` — settled items;
- `open` — remaining decision points;
- `risk_allocation` — the actual commercial/legal risk being allocated;
- `trade_space` — what can move;
- `package_proposal` + `package_dependency` — only when concessions are genuinely linked.

This is designed to prevent a common failure mode: polished prose that obscures which risk, condition, approval, covenant, fee, remedy or closing dependency is actually being negotiated.

## Privilege / settlement labels

The strategy engine treats labels as review triggers, never magic protection. If a payload asks for privilege or settlement-style labeling, the engine checks for the underlying purpose/context and emits jurisdiction/effect warnings. Copying counsel, typing `Privileged & Confidential`, `Rule 408`, or `Without Prejudice` does not by itself establish the requested legal effect.

## Evidence contract

A baseline research record is accepted only when all of these are true:

1. its agent, vendor and watch URL match `agents.json`;
2. the official source gives an exact `YYYY-MM-DD` date inside 2026-06-01 through 2026-08-31;
3. the source kind is official and the record explains the specialized legal writing/drafting/redlining/work-product relevance;
4. the verification status is exactly `verified`;
5. the live worker receives HTTP success from the configured official URL **and** the final URL after redirects remains on an allowed official domain;
6. all ten distinct worker receipts are present when the adjudicator runs.

Discovery/news results are leads only. They never promote a tool to verified status by themselves.

## 24/7 meaning

The workflow runs at minutes `7,22,37,52` of every hour and can also run on demand. GitHub does **not** guarantee exact scheduled start times or uninterrupted wall-clock execution. The accurate claim is **24/7 best-effort continuous radar with four scheduled research cycles per hour**, not a fake zero-gap daemon.

Before claiming the hosted monitor is live on a revision, read back the default-branch workflow run, ten worker jobs/artifacts, adjudicator job and final `report.json`; repository files or a green unrelated check are not sufficient proof.
