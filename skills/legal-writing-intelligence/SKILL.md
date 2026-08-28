---
name: legal-writing-intelligence
description: Continuously research verified legal AI writing tools and compile high-stakes U.S. legal/business correspondence using evidence-bound, partner-level drafting logic.
---

# Legal Writing Intelligence

## Objective

Provide two linked capabilities:

1. **Research:** run ten independent research branches that discover and re-check legal AI writing/drafting products, with official-source, exact-date, redirect-provenance and uniqueness gates.
2. **Writing:** turn structured facts and asks into concise high-stakes U.S. legal/business correspondence using public professional conventions rather than imitating any named lawyer.

## Activation

Use when the user asks for legal/business correspondence, executive dispute/project letters, contract/drafting AI research, legal-AI product monitoring, or a current evidence-backed comparison of legal writing tools.

## Non-goals

- Do not claim a phrase creates privilege, settlement protection, non-waiver, or legal effect by itself.
- Do not invent releases, dates, customer results, legal authority, quotes, or confidential practices.
- Do not present the tool as a lawyer or replace jurisdiction-specific legal review.
- Do not imitate the personal style of a named living lawyer; use professional category-level conventions.
- Do not call a configured URL “officially verified” if its HTTP redirect terminates outside the configured official domains.

## Workflow

1. Parse the task into matter, audience, purpose, facts, positions, asks, conditions, deadline, and risk posture.
2. For current product claims, activate the ten distinct research branches defined in `agents.json`.
3. Discovery may use keyless web search, but acceptance requires a configured official vendor page or official hosted help center.
4. Capture the requested URL, final redirect URL, HTTP status, fetch timestamp and content fingerprint for live official-source evidence.
5. Reject duplicates, identity drift, month-only/partial release dates, out-of-window dates, generic AI products with no explicit legal drafting/work-product relevance, unverifiable launch claims, and cross-domain redirects.
6. For writing, use `src/writer.py` or its output contract. Keep facts separate from inferences and requested actions.
7. Apply signal language only when its legal/commercial precondition is true; do not use legal phrases as decoration.
8. If rights-preservation wording is requested, require `reservation_scope` and keep the language tied to that stated position rather than automatically inserting broad “all rights” boilerplate.
9. Before release, perform an adversarial check: ambiguity, accidental admission, accidental waiver, missing owner/date/evidence, unsupported threat, unsupported legal conclusion, and fake privilege labeling.

## Evidence requirements

Each accepted research record must include: unique agent ID, unique vendor, product/tool, exact-day release date, official source kind, configured official URL, specific writing/drafting relevance, adversarial check, and exact `verified` status.

Each live worker must leave a receipt. A successful worker receipt must show an HTTP 2xx/3xx response and an allowed final URL after redirects. Ten distinct receipts are required for adjudication to pass.

## “Insider language” model

Treat apparently insider phrases as functional signals, not secret code. Before using one, identify what it is meant to do:

- define the record;
- reject a premise without accepting its framing;
- narrow a proposition to current information;
- make an offer/commitment conditional;
- prevent an unintended concession;
- create an auditable action/deadline;
- state the next consequence without theatrical threats;
- preserve a practical path to resolution.

If the function is absent, omit the phrase.

## Output contract

A research answer returns the ten independent reports plus limitations. A writing answer returns a concise letter or drafting prompt whose record, position, asks, deadline, conditions and any scoped reservation are visibly separable.

## Compatibility boundary

The core scripts use Python 3.11+ standard library only. Scheduled research is implemented with GitHub Actions. GitHub scheduled workflows are best-effort and can be delayed; this package must never describe the schedule as hard real-time or guaranteed uninterrupted service.

## Completion gate

`PASS` for repository logic requires the ten-agent seed contract and regression tests to pass on the exact revision.

`PASS` for a hosted live-monitor claim additionally requires owning-runtime read-back on the merged default-branch revision: validation job, all ten research jobs/receipts, adjudicator job, and final `report.json` must be present and successful. A merged file, configured cron, unrelated green CI, or historical run is not sufficient.
