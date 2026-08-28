# Legal Writing Intelligence

A GitHub-native skill for two jobs that should not be separated: **current legal-AI writing research** and **high-stakes legal/business drafting logic**.

## What is implemented

- 10 independent research branches (`agent-01` … `agent-10`), each with a distinct vendor, query and official source set.
- A June–August 2026 evidence ledger containing exactly 10 legal-writing/drafting releases with exact-day dates.
- Keyless discovery through Bing News RSS plus official-page re-fetch, redirect destination capture, fetch timestamp and SHA-256 fingerprinting.
- A fail-closed adjudicator that rejects duplicate/missing agents, vendor identity drift, non-official URLs, cross-domain redirects, partial dates, partial verification status, missing writing relevance, out-of-window releases, or inability to re-fetch at least one official source for every live agent.
- A deterministic U.S. legal-business letter compiler that does not require an LLM/API.
- Scoped reservation language: `reserve_rights` or `reservation-of-rights` mode requires an explicit `reservation_scope`; the compiler does not spray blanket non-waiver boilerplate into a letter.
- GitHub Actions research every 15 minutes plus push/manual execution, ten worker artifacts, and one adjudicated artifact.

## Run locally

```bash
python -m unittest discover -s skills/legal-writing-intelligence/tests -p 'test_*.py' -v
python skills/legal-writing-intelligence/src/research.py --agent agent-01 --out /tmp/agent-01.json
python skills/legal-writing-intelligence/src/writer.py input.json
```

Example `input.json`:

```json
{
  "matter": "Project Falcon — Milestone 4",
  "purpose": "We need written confirmation of the recovery plan.",
  "recipient": "Counsel",
  "mode": "project-escalation",
  "facts": ["Milestone 4 was due August 20, 2026."],
  "asks": ["Provide the revised critical-path schedule."],
  "deadline": "August 29, 2026 at 5:00 p.m. New York time",
  "reserve_rights": true,
  "reservation_scope": "our position regarding responsibility for delay"
}
```

## Evidence contract

A baseline record is accepted only when all of these are true:

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
