# Elite Legal Correspondence Radar — Design

Date: 2026-08-28
Status: Approved by user request; implementation target

## Outcome

Add a portable Agent Skill plus a GitHub Actions research adapter that does two jobs without conflating them:

1. continuously discover and verify current AI writing/legal-writing products with primary-source evidence; and
2. turn the reusable drafting logic of high-stakes U.S. commercial/legal correspondence into a transparent writing system for executive, deal, dispute, and international-project communications.

The system must not manufacture legal authority, pretend that labels create privilege, or imitate an identifiable living lawyer. The target is the professional mechanism: issue framing, risk allocation, evidentiary posture, negotiation signaling, conditionality, and rights preservation.

## Architecture

### Portable core

`skills/skills/elite-legal-correspondence/SKILL.md`

The skill classifies the correspondence mode, reconstructs facts and leverage, selects a drafting posture, maps specialist phrases to their communicative/legal function, drafts, and performs a hostile-read audit before release.

### Evidence ledger

`skills/skills/elite-legal-correspondence/references/2026-summer-ai-writing-tools.json`

Exactly ten independently owned 2026-06 through 2026-08 product records. Every accepted record carries an official URL, explicit release date, specialization evidence, and an owner lane. Duplicate products/URLs are a hard failure.

### Ten independent research lanes

`skills/skills/elite-legal-correspondence/config/research-lanes.json`

Each lane owns one vendor/product family and may inspect only its declared official domains. The lanes do not copy one another's conclusions. Cross-lane deduplication and final acceptance occur only in the adjudication step.

### Research runtime

`skills/skills/elite-legal-correspondence/scripts/monitor_sources.py`

Standard-library-only scanner. It fetches official seed/discovery pages, stores URL/status/hash/timestamp observations, validates the release-window and writing-specialization contract, and merges ten worker receipts. Network failure remains visible; it is never replaced with invented content.

### CI / continuous radar adapter

`.github/workflows/elite-legal-correspondence-radar.yml`

- ten matrix workers, one per lane;
- isolated worker artifacts;
- adjudicator fails closed if a lane is missing, duplicated, unverifiable, or outside the date window;
- scheduled at minute 7/22/37/52 to avoid top-of-hour load concentration;
- manual and pull-request validation paths.

GitHub `schedule` is a recurring monitor, not a hard real-time daemon. Scheduled runs execute only from the default branch and can be delayed or dropped under GitHub load. Therefore the product wording is **24/7 continuous radar**, never “zero-gap guaranteed process.”

## Correspondence model

The skill treats apparent “insider language” as functional signaling, not secret vocabulary. Each phrase family must answer: what position does this preserve, what inference does it prevent, what concession does it avoid, what action does it request, and what record does it create?

Core layers:

1. **Record** — dated facts, prior notices, documents, commitments, missing information.
2. **Position** — what is accepted, disputed, reserved, assumed, or expressly not conceded.
3. **Risk** — contractual/commercial consequence stated without theatrical threats.
4. **Ask** — concrete action, owner, deadline, and required form of confirmation.
5. **Preservation** — rights/remedies/claims/defenses kept open only where appropriate.
6. **Relationship** — preserve a workable commercial path unless escalation is the actual objective.

## Acceptance contract

Hard criteria:

- `A1`: portable skill has valid `SKILL.md` frontmatter and a complete drafting workflow.
- `A2`: exactly ten research lanes exist and lane IDs, products, and canonical official URLs are unique.
- `A3`: exactly ten baseline records fall within 2026-06-01..2026-08-31 and use official URLs.
- `A4`: each record explicitly describes specialized AI-assisted writing/drafting/legal-work-product functionality.
- `A5`: scanner unit tests pass without network access.
- `A6`: live worker scan records HTTP evidence instead of substituting fabricated success.
- `A7`: adjudication fails closed if any of the ten worker receipts is absent or invalid.
- `A8`: workflow is configured for pull request/manual validation and recurring default-branch scans.
- `A9`: wording guide distinguishes stylistic convention from actual legal effect and warns that privilege/Rule 408/“without prejudice” labels are not magic.
- `A10`: exact reported revision is re-read and CI status is checked before release.

## Non-goals

- no covert persuasion or deceptive impersonation;
- no claim that a phrase automatically creates privilege, settlement protection, waiver protection, or contractual effect;
- no scraping of private/confidential correspondence;
- no uncited invention of law, contract text, dates, names, amounts, or project facts;
- no claim that GitHub Actions provides an uninterrupted daemon SLA.
