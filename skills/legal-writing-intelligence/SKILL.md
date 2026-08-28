---
name: legal-writing-intelligence
description: Continuously research verified legal AI writing tools and compile high-stakes U.S. legal/business correspondence using evidence-bound, partner-level drafting logic.
---

# Legal Writing Intelligence

## Objective

Provide two linked capabilities:

1. **Research:** run ten independent research branches that discover and re-check legal AI writing/drafting products, with official-source and date-window gates.
2. **Writing:** turn structured facts and asks into concise high-stakes U.S. legal/business correspondence using public professional conventions rather than imitating any named lawyer.

## Activation

Use when the user asks for legal/business correspondence, executive dispute/project letters, contract/drafting AI research, legal-AI product monitoring, or a current evidence-backed comparison of legal writing tools.

## Non-goals

- Do not claim a phrase creates privilege, settlement protection, non-waiver, or legal effect by itself.
- Do not invent releases, dates, customer results, legal authority, quotes, or confidential practices.
- Do not present the tool as a lawyer or replace jurisdiction-specific legal review.
- Do not imitate the personal style of a named living lawyer; use professional category-level conventions.

## Workflow

1. Parse the task into matter, audience, purpose, facts, positions, asks, conditions, deadline, and risk posture.
2. For current product claims, activate the ten distinct research branches defined in `agents.json`.
3. Discovery may use keyless web search, but acceptance requires an official vendor page or official hosted help center.
4. Reject duplicates, out-of-window dates, generic AI products with no legal drafting/work-product capability, and unverifiable launch claims.
5. For writing, use `src/writer.py` or its output contract. Keep facts separate from inferences and requested actions.
6. Apply signal language only when its legal/commercial precondition is true; do not use legal phrases as decoration.
7. Before release, perform an adversarial check: ambiguity, accidental admission, accidental waiver, missing owner/date/evidence, unsupported threat, unsupported legal conclusion, and fake privilege labeling.

## Evidence requirements

Each accepted research record must include: unique agent ID, unique vendor, product/tool, release date (with precision), source kind, official URL, specific writing/drafting relevance, adversarial check, and verification status.

## Output contract

A research answer returns the ten independent reports plus limitations. A writing answer returns a concise letter or drafting prompt whose record, position, asks, deadline and reservations are visibly separable.

## Compatibility boundary

The core scripts use Python 3.11+ standard library only. Scheduled research is implemented with GitHub Actions. GitHub scheduled workflows are best-effort and can be delayed; this package must never describe the schedule as hard real-time or guaranteed uninterrupted service.

## Completion gate

`PASS` requires all ten research branches to be present and unique, seed records to pass date/source validation, tests to pass on the exact revision, and the GitHub workflow to be syntactically present on the merged default branch before scheduled execution can be claimed.
