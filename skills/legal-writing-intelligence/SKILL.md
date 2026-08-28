---
name: legal-writing-intelligence
description: Continuously research verified legal AI writing tools, preflight high-stakes correspondence strategy, and compile evidence-bound U.S. legal/business writing.
---

# Legal Writing Intelligence

## Objective

Provide three linked capabilities in one fail-closed chain:

1. **Research:** run ten independent research branches that discover and re-check legal AI writing/drafting products, with official-source, exact-date, redirect-provenance and uniqueness gates.
2. **Strategy:** analyze the correspondence before drafting: record, issue, position, decision ownership, conditions, evidence bridges, asks/deadlines, deal risk allocation, major-project causation, privilege/settlement context and scoped signal language.
3. **Writing:** turn a strategy-ready payload into concise high-stakes U.S. legal/business correspondence using public professional conventions rather than imitating any named lawyer.

## Activation

Use when the user asks for legal/business correspondence, executive dispute/project letters, deal/board negotiation letters, international engineering/project escalation, contract/drafting AI research, legal-AI product monitoring, or a current evidence-backed comparison of legal writing tools.

## Non-goals

- Do not claim a phrase creates privilege, settlement protection, non-waiver, entitlement, causation, critical-path delay, quantum or any other legal effect by itself.
- Do not invent releases, dates, customer results, legal authority, quotes, confidential practices, contractual provisions, project records or deal terms.
- Do not present the tool as a lawyer or replace jurisdiction-specific legal review.
- Do not imitate the personal style of a named living lawyer; use professional category-level conventions.
- Do not call a configured URL “officially verified” if its HTTP redirect terminates outside the configured official domains.
- Do not turn an event into causation, causation into schedule impact, schedule impact into cost, or cost into entitlement without the missing evidence bridge.

## Workflow

1. Parse the task into matter, audience, purpose, facts, issue, position, asks, conditions, deadline/timezone, decision owner, risk posture and path forward.
2. If the task concerns a major project/engineering claim, separately capture event, governing mechanism, notice/contemporaneous record, causation, schedule/critical-path effect, cost/quantum support if claimed, mitigation and requested instruction.
3. If the task concerns a deal, separately capture settled points, open points, actual risk allocation, trade space, conditionality and package dependencies.
4. If privilege or settlement-style labels are contemplated, identify the underlying legal-advice/compromise purpose, recipients/distribution and governing jurisdiction/regime before treating the label as meaningful.
5. Run `src/strategy.py` before drafting. Any high-severity evidence/architecture gap yields `REVISE`; do not polish around it.
6. Apply signal language from `resources/signals.json` only when its stated functional precondition is true. Apparent “insider language” is a controlled signal, not secret code or decoration.
7. If rights-preservation wording is requested, require `reservation_scope` and keep the language tied to that stated position rather than automatically inserting broad “all rights” boilerplate.
8. For current product claims, activate the ten distinct research branches defined in `agents.json`. Discovery may produce leads, but acceptance requires the configured official source and all evidence gates.
9. Capture requested URL, final redirect URL, HTTP status, fetch timestamp and content fingerprint for live official-source evidence. Reject duplicates, identity drift, partial dates, cross-domain redirects and unsupported writing relevance.
10. Once strategy status is `READY`, use `src/writer.py` or its output contract. Keep record, position, conditions, consequence, asks, deadline and any scoped reservation visibly separable.
11. Before release, perform the four-way hostile read: recipient, opposing counsel, board/auditor and neutral fact-finder.

## Strategy evidence model

A strong letter should be reducible to observable components rather than “lawyerly tone”:

- **bottom line** — why the recipient is receiving the communication;
- **record** — decision-relevant dates, documents, actions and prior positions;
- **issue** — the precise unresolved question;
- **position** — accepted, disputed, assumed, conditional and non-conceded points;
- **consequence** — commercial, contractual, schedule, cost or governance mechanics;
- **ask** — exact action/decision, accountable owner, deadline and required form of confirmation;
- **path forward / scoped preservation** — workable resolution route and only the position genuinely requiring preservation.

For major projects, use the proof chain:

`event → mechanism → notice/record → causation → schedule effect → cost/quantum → mitigation → requested instruction → scoped preservation`

Missing layers must remain visible as evidence gaps. Do not bridge them with rhetoric.

For transactions, separate:

`agreed → open → risk allocation → conditionality → trade space → package dependency → decision/approval`

## Research evidence requirements

Each accepted research record must include: unique agent ID, unique vendor, product/tool, exact-day release date, official source kind, configured official URL, specific writing/drafting relevance, adversarial check, and exact `verified` status.

Each live worker must leave a receipt. A successful worker receipt must show an HTTP 2xx/3xx response and an allowed final URL after redirects. Ten distinct receipts are required for adjudication to pass.

`resources/authority-ledger.json` records public-source mechanisms and limitations used to shape strategy rules. It is a provenance ledger, not a substitute for matter-specific legal authority.

## “Insider language” model

Treat apparently insider phrases as functional switches. Before using one, identify what it is meant to do:

- narrow the present issue;
- clarify a material ambiguity;
- bind a conclusion to current evidence;
- reject the counterparty's framing;
- make a proposal/commitment genuinely conditional;
- test a hypothetical or alternative without conceding the primary position;
- signal controlled trade space;
- preserve linked package concessions;
- create an auditable action/deadline;
- state an executable consequence instead of a theatrical threat;
- move a defined decision to executive ownership;
- create a contemporaneous record marker;
- preserve one specifically identified position while practical work continues.

If the function or precondition is absent, omit the phrase.

## Output contract

A research answer returns ten independent reports plus limitations. A strategy answer returns `READY` or `REVISE`, risk flags, evidence gaps, architecture, firmness level, signal recommendations and the hostile-read checklist. A writing answer is generated only from a strategy-ready factual payload and keeps record, position, asks, deadline, conditions, consequences and any scoped reservation visibly separable.

## Compatibility boundary

The core scripts use Python 3.11+ standard library only. Scheduled research is implemented with GitHub Actions. GitHub scheduled workflows are best-effort and can be delayed; this package must never describe the schedule as hard real-time or guaranteed uninterrupted service.

## Completion gate

`PASS` for repository logic requires:

- the ten-agent research seed contract and redirect/source validation;
- syntax validation of the signal and authority ledgers;
- strategy preflight regression tests for project causation/quantum, deal package dependency, privilege/settlement labels and scoped reservation;
- writer regressions;
- all required checks to pass on the exact reported revision.

`PASS` for a hosted live-monitor claim additionally requires owning-runtime read-back on the merged default-branch revision: validation job, all ten research jobs/receipts, adjudicator job, and final `report.json` must be present and successful. A merged file, configured cron, unrelated green CI, or historical run is not sufficient.
