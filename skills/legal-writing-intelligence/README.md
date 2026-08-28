# Legal Writing Intelligence

A GitHub-native skill for two jobs that should not be separated: **current legal-AI writing research** and **high-stakes legal/business drafting logic**.

## What is implemented

- 10 independent research branches (`agent-01` … `agent-10`), each with a different vendor, search query and official source set.
- A June–August 2026 seed ledger containing 10 verified legal-writing/drafting releases.
- Keyless discovery through Bing News RSS plus official-page re-fetch/fingerprinting.
- An adjudicator that fails on duplicate agents/vendors/URLs, missing agents, non-official URLs, out-of-window releases, or inability to re-fetch at least one official source for every live agent.
- A deterministic U.S. legal-business letter compiler that does not require an LLM/API.
- An hourly GitHub Actions schedule plus push/manual execution and artifact retention.

## Run locally

```bash
python -m unittest discover -s skills/legal-writing-intelligence/tests -p 'test_*.py'
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
  "reserve_rights": true
}
```

## 24/7 meaning

The workflow is scheduled hourly (`17 * * * *`) and can also run on demand. GitHub does **not** guarantee exact start times or uninterrupted wall-clock execution, so the correct claim is persistent best-effort monitoring with ten independent hourly research jobs—not a fake always-running daemon.
