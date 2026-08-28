---
name: elite-legal-correspondence
description: Draft and audit high-stakes U.S.-style commercial, legal, executive, deal, dispute, and international-project correspondence using explicit risk positioning, evidence discipline, negotiation signaling, conditionality, and rights-preservation logic. Also use when researching current specialist AI legal-writing/drafting products through the bundled evidence ledger.
---

# Elite Legal Correspondence

Version: `0.1.0-rc1`

## Objective

Produce correspondence that feels professionally “inside” because the reasoning is disciplined, not because jargon is sprinkled into ordinary prose.

The target is a functional style used in sophisticated U.S. business/legal work: short factual propositions, controlled verbs, explicit assumptions, calibrated commitments, precise asks, and preservation of options. Do not imitate or attribute text to a named living lawyer.

## Trigger

Use for:

- CEO/owner/board/investor/vendor correspondence;
- M&A, financing, partnership, procurement, or contract negotiation letters;
- executive escalation, notice, cure/default, reservation-of-rights, claim, or response letters;
- international engineering/construction/project correspondence, including change, delay, entitlement, records, schedule, mitigation, and payment disputes;
- professional legal/business email where the user wants elite U.S. counsel/deal-team discipline;
- research or comparison of specialist legal-writing/drafting AI tools using the bundled 2026 evidence ledger.

## Intake model

Before drafting, recover or explicitly mark unknown:

1. sender role and authority;
2. recipient role and decision power;
3. jurisdiction / governing contract or law if legal effect matters;
4. relationship objective: preserve, renegotiate, escalate, terminate, settle, document, or reserve;
5. verified facts, dates, documents, prior notices, and commitments;
6. disputed facts and unsupported allegations;
7. leverage and downside on both sides;
8. requested action, owner, deadline, and acceptable confirmation;
9. desired record posture: ordinary business record, notice, settlement communication, privileged counsel work, etc.;
10. facts or legal conclusions that require counsel verification.

Never fill a missing material fact with a plausible guess. Use `[需確認：…]` in working drafts.

## Mode classifier

Choose one primary mode before writing:

- `COOPERATIVE_OPERATIONAL` — solve the issue while preserving the relationship.
- `EXECUTIVE_ESCALATION` — make ownership, consequence, and deadline unmistakable without theatrics.
- `NEGOTIATION_POSITION` — state the acceptable commercial position and preserve alternatives.
- `RECORD_AND_CONFIRM` — create a contemporaneous record of what happened/was agreed/was not agreed.
- `RESERVATION_OF_RIGHTS` — avoid accidental concession or waiver while keeping options open.
- `NOTICE_OR_CURE` — give contractually relevant notice/cure information; exact clause/law must be supplied or verified.
- `SETTLEMENT_EXPLORATION` — explore resolution while explicitly separating proposal from admission; jurisdiction-specific evidentiary effect requires verification.
- `PROJECT_CLAIM_OR_CHANGE` — international engineering/construction claim/change/delay/payment correspondence with records and schedule logic.
- `BOARD_OR_TRANSACTION` — concise decision paper/letter for high-value corporate or transaction context.

## Drafting stack

Write in this order unless the situation demands a deliberate variation:

1. **Bottom line** — why the recipient is receiving this and what decision/action is required.
2. **Record** — only decision-relevant facts, dates, documents, notices, and prior positions.
3. **Issue** — identify the precise gap/disagreement; do not bury it in narrative.
4. **Position** — distinguish accepted fact, disputed fact, assumption, inference, and non-concession.
5. **Commercial/legal frame** — contract/business consequence using verified source material only.
6. **Ask** — exact action, deadline, accountable person, and response form.
7. **Preservation** — reserve rights/remedies/claims/defenses only when appropriate; do not over-lawyer routine mail.
8. **Path forward** — retain a credible route to resolution unless termination/escalation is the objective.

## “Insider language” semantics

Treat these as **functions**, not magic words. Use only when the function is needed.

| Pattern | Functional meaning | Guardrail |
| --- | --- | --- |
| `For the avoidance of doubt, …` | close an interpretive gap | do not use to manufacture an obligation absent from the source agreement |
| `To avoid any misunderstanding, …` | clarify a record in business language | prefer this over legalese when no legal nuance is needed |
| `For the record, …` | create a contemporaneous position/fact marker | state only verified facts or clearly attributed positions |
| `Based on the information presently available, …` | bound a statement to current knowledge | update if later facts materially change it |
| `To the extent …` | scope a proposition/obligation | avoid using it to hide uncertainty that should be explicit |
| `Subject to …` | make commitment conditional | identify the actual condition; vague conditionality creates ambiguity |
| `Assuming, solely for purposes of discussion, …` | test an alternative without adopting the premise | do not imply this automatically prevents evidentiary use |
| `Without conceding …` | argue an alternative while preserving a disputed premise | use sparingly and state what is not conceded |
| `Nothing in this correspondence should be construed as …` | block an unintended inference | cannot override governing law/contract by wording alone |
| `All rights and remedies are expressly reserved.` | preserve available options | not a substitute for satisfying notice/waiver requirements |
| `Nothing herein constitutes a waiver, amendment, admission, or election …` | enumerate positions not intentionally surrendered | exact effect is jurisdiction/contract dependent |
| `We are not in a position to accept …` | controlled refusal | follow with reason/alternative when commercial relationship matters |
| `That position is not workable because …` | reject outcome, not person | state operational/economic/legal reason, not adjectives |
| `We remain prepared to …` | keep negotiation channel open | specify what constructive next step remains available |
| `We continue to prefer a commercial resolution …` | signal de-escalation without surrender | pair with a concrete path/deadline |
| `Please confirm by [date/time] …` | create an actionable deadline and record | deadline must be realistic and contractually valid where relevant |
| `Absent that confirmation, we will …` | state consequence rather than threaten | only state actions the sender can actually take |
| `This matter now requires executive attention …` | escalate ownership | identify the decision that needs executive resolution |
| `Without prejudice to any entitlement …` | preserve asserted project/contract entitlement while acting | U.S./cross-border legal effect varies; verify governing regime |
| `Contemporaneous records indicate …` | anchor a project claim to the record | cite the actual record/date; never invent it |

## U.S. legal-label warning

Labels such as `Privileged & Confidential`, `Attorney Work Product`, `Rule 408`, or `Without Prejudice` do **not** automatically create privilege, work-product protection, inadmissibility, or settlement protection. Their effect depends on the underlying facts, participants, purpose, jurisdiction, and applicable law. If the user needs legal effect rather than writing style, require current authoritative support or lawyer review.

## International engineering/project logic

For project correspondence, prefer this causal chain:

`event → contractual mechanism → timely notice/record → schedule/cost effect → mitigation → requested instruction/decision → reserved entitlement`

Keep separate:

- occurrence of the event;
- causation;
- critical-path/schedule impact;
- quantum/cost support;
- notice compliance;
- mitigation;
- entitlement.

Do not collapse them into one assertion. If one layer is unproven, label it as pending support rather than writing around the gap.

## Hostile-read audit

Before release, read the draft as opposing counsel, a board member, a claims consultant, and a neutral fact-finder. Check:

- Can any sentence be read as an admission not intended by the sender?
- Did the draft convert an allegation into a fact?
- Did it promise more than the sender controls?
- Is a deadline unsupported by contract/law/business reality?
- Is the requested action unmistakable?
- Does every legal/contract conclusion have a source, or a verification marker?
- Is leverage conveyed through facts/consequences rather than hostility?
- Does any “protective” phrase falsely imply guaranteed legal effect?
- Could 20% of the words be removed without losing position, evidence, or action?

## Research mode

For current AI writing/legal AI research:

1. load `config/research-lanes.json`;
2. keep all ten lanes independent;
3. prefer official product/company documentation and dated announcements;
4. require explicit release date, official URL, and specialized writing/drafting evidence;
5. reject duplicates across canonical product and URL;
6. store observations, HTTP status, fetch timestamp, and content hash;
7. never convert network failure or missing metadata into a verified claim;
8. adjudicate only after all ten lane receipts exist.

Baseline verified records live in `references/2026-summer-ai-writing-tools.json`.

## Output contract

For drafting, return either:

- `clean`: send-ready correspondence only; or
- `counsel-view`: draft plus a compact risk/assumption table identifying admissions, conditions, source gaps, and phrases whose legal effect requires verification.

Default to `clean` when the user asks for a send-ready letter and the facts are sufficiently complete. Do not cite internal style notes in the letter itself unless requested.

## Completion gate

A polished tone is not completion. The task is complete only when material facts are sourced/marked, the requested action is clear, unintended concessions have been adversarially checked, and any asserted legal effect is supported or explicitly left for verification.
