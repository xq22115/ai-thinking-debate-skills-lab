# Legal Writing Radar Implementation Plan

> **For agentic workers:** implement this plan task-by-task with an independent verification pass between tasks.

**Goal:** Build a repository-native GitHub Action + Python CLI + writing skill that continuously monitors official legal-AI product sources, preserves a verified June–August 2026 catalog of ten non-duplicate writing/drafting products, and converts user facts into an elite U.S. legal/business correspondence blueprint without inventing law, clauses, privilege, or facts.

**Architecture:** `systems/legal-writing-radar/legal_writing_radar.py` is a standard-library-only CLI. Ten configured research lanes each own one vendor/product and only follow official-domain URLs. The scheduled GitHub workflow fans out ten independent lane scans, persists per-lane evidence artifacts, and runs a separate adjudication job against a pre-verified catalog. A repository Skill defines the drafting logic: conclusion-first, record/authority anchors, calibrated commitments, explicit ask/deadline, rights-preservation controls, and international-project notice structure.

**Tech Stack:** Python 3.12 standard library, JSON, GitHub Actions, `unittest`.

**Spec:** This plan implements the user request dated 2026-08-28 for ten independent research branches, verifiable official sources dated 2026-06-01 through 2026-08-31, continuous online discovery, and U.S. elite legal/business writing logic.

## Global Constraints

- Output intended for the user is Traditional Chinese (Taiwan usage); source records preserve official English product names.
- Never fabricate publication dates, version numbers, source URLs, legal authority, contract clauses, privilege status, or test results.
- A catalog item is accepted only when its official source date is within 2026-06-01..2026-08-31 inclusive and its URL host matches that lane's official-domain allowlist.
- Exactly ten accepted seed records are required; tool IDs and evidence URLs must be unique.
- Ten lanes are independent discovery scopes; no vendor/product is assigned to more than one lane.
- Scheduled GitHub Actions are best-effort, not a literal uninterrupted daemon. A `watch` CLI mode provides continuous polling for an authorized always-on/self-hosted runtime.
- No external Python dependency and no search-engine/API key is required.
- Legal correspondence output is a drafting aid, not a claim of legal advice; context-dependent labels such as privilege, settlement protection, `without prejudice`, or `subject to contract` are disabled unless the user supplies an applicable legal/contractual basis.

---

### Task 1: Lock the acceptance contract in executable tests

**Files:**
- Create: `systems/legal-writing-radar/tests/test_legal_writing_radar.py`
- Create: `.github/workflows/legal-writing-radar.yml`

**Interfaces:**
- Consumes: none.
- Produces: expected module functions `validate_catalog`, `extract_published_date`, `discover_official_links`, `build_correspondence_blueprint`, plus CLI commands `verify`, `scan`, `adjudicate`, and `watch`.

- [ ] Write tests proving the missing implementation fails first.
- [ ] Push the tests and workflow without production code.
- [ ] Read back the workflow run and record the expected failure caused by the missing module/CLI.

### Task 2: Implement evidence validation and official-source discovery

**Files:**
- Create: `systems/legal-writing-radar/legal_writing_radar.py`
- Create: `systems/legal-writing-radar/config/research_lanes.json`
- Create: `systems/legal-writing-radar/evidence/verified-tools-2026-06-08.json`

**Interfaces:**
- `validate_catalog(catalog, lanes, since, until) -> list[str]`: returns validation errors; an empty list is PASS.
- `extract_published_date(html) -> str | None`: extracts an ISO date only from explicit page metadata/time/date text.
- `discover_official_links(base_url, html, allowed_hosts, keywords) -> list[str]`: returns de-duplicated same-domain candidate URLs only.
- CLI `scan --lane XX --output FILE`: fetches the lane's official seed/discovery pages, records status/hash/date/keyword evidence, and never upgrades an unknown date to accepted.
- CLI `verify`: validates the ten-record seed catalog.
- CLI `adjudicate`: validates lane artifacts independently of scanner self-report.
- CLI `watch`: repeats all ten lane scans at a user-supplied interval on an always-on authorized runtime.

- [ ] Implement the smallest standard-library code that passes the tests.
- [ ] Run `python -m unittest discover -s systems/legal-writing-radar/tests -p 'test_*.py'`.
- [ ] Run `python systems/legal-writing-radar/legal_writing_radar.py verify`.

### Task 3: Encode elite legal/business correspondence logic

**Files:**
- Create: `systems/legal-writing-radar/config/style_playbook.json`
- Create: `skills/13-elite-us-legal-business-correspondence.md`

**Interfaces:**
- `build_correspondence_blueprint(facts, mode) -> dict`: produces position, record, authority/contract anchors, analysis, commercial/project effect, ask, deadline, and reservations; absent authority remains an explicit verification placeholder.
- Modes: `executive-counsel`, `transactional`, `dispute-preservation`, `international-project`.

- [ ] Encode functional legal signals rather than fake "secret codes": commitment level, evidentiary record, risk allocation, escalation posture, and rights preservation.
- [ ] Encode international-project correspondence around contract/project reference, chronology, notice basis, cause/effect/entitlement/quantum, requested instruction, deadline, and contemporaneous records.
- [ ] Fail closed on unsupported privilege/settlement labels and invented clause numbers.

### Task 4: Continuous GitHub operation and independent adjudication

**Files:**
- Modify: `.github/workflows/legal-writing-radar.yml`
- Create: `systems/legal-writing-radar/README.md`

**Interfaces:**
- GitHub matrix jobs `01`..`10` execute independently with `fail-fast: false`.
- Schedule is offset from the top of the hour and also supports `workflow_dispatch` and normal branch/PR verification.
- Each lane uploads a JSON artifact; a separate adjudication job downloads and validates all ten artifacts plus the seed catalog.

- [ ] Verify ten lane IDs are unique and the matrix contains exactly ten entries.
- [ ] Verify permissions remain `contents: read`.
- [ ] Document GitHub schedule limitations and the self-hosted `watch` alternative without claiming literal 24/7 guarantees.

### Task 5: Release gate

**Files:** all files above.

- [ ] Read back every created file from the exact branch.
- [ ] Confirm the seed catalog contains exactly ten unique official URLs and dates in range.
- [ ] Confirm the feature workflow passes on the exact implementation commit.
- [ ] Confirm the repository's existing quality workflows introduce no new failure on the exact implementation commit.
- [ ] Open a draft PR to `main`; do not merge merely because files exist or a PR was created.
