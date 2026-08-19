# AI Research Vault 2026

> Cross-chat AI research archive snapshot — generated 2026-08-18.

## Purpose

This repository-ready package consolidates AI-related research recovered from prior ChatGPT conversations and retained cross-chat context. It is designed to be imported into GitHub as a long-lived research vault.

## Critical provenance rule

This is **not a raw export of every historical chat transcript**. It is a structured archive built from the cross-chat material currently retrievable in this session: retained summaries, named artifacts, version histories, validation notes, and prior assistant outputs.

Every item should be read with one of these statuses:

- `VERIFIED_ARTIFACT` — artifact/tests were reported as actually produced and checked.
- `PARTIALLY_VERIFIED` — some local/static tests passed, but live deployment or end-to-end behavior was not verified.
- `UNVERIFIED_LIVE` — concept/package existed, but real product/account/runtime behavior was not verified.
- `ARCHIVAL_CLAIM` — preserved from prior chat context; re-check before using as a current 2026 fact.
- `BLOCKED` — an explicit blocker prevented completion.

## Repository map

- `INDEX.md` — master navigation.
- `research/00_master_timeline.md` — version and project timeline.
- `research/01_agent_systems.md` — multi-agent / continuous-agent architecture.
- `research/02_continuous_thinking_antigravity.md` — Antigravity / Continuous Thinking.
- `research/03_openclaw_automation.md` — OpenClaw desktop automation.
- `research/04_prompt_memory_skillpacks.md` — prompt engineering, memory, reusable skills.
- `research/05_mcp_github_governance.md` — MCP, GitHub, evidence and governance.
- `research/06_domain_skillpacks.md` — legal, animation, dialogue and other domain systems.
- `governance/STATUS_MATRIX.md` — validation and risk matrix.
- `governance/30_PERSPECTIVE_DELIBERATION.md` — 30-role audit/debate synthesis.
- `data/research_registry.json` — machine-readable registry.
- `data/SOURCE_SCOPE.md` — what was and was not recoverable.
- `GITHUB_IMPORT_STATUS.md` — current GitHub connector status.

## Current GitHub write status

Authenticated GitHub user: `xq22115-pixel`.

The GitHub App is also installed on organization `xq22115`. The personal account currently exposes 0 repositories to the connector, while the organization exposes writable private repositories.

Because the connector does **not** expose a `create repository` action, a dedicated new repository cannot be truthfully created from this session. To avoid blocking the archive, the current package is being staged non-destructively in:

- repository: `xq22115/demo-repository`
- branch: `ai-research-vault-2026-import`
- directory: `ai-research-vault-2026/`

The intended eventual dedicated repository remains:

`ai-research-vault-2026`

The staging import is deliberately isolated on a branch so it does not directly modify `main`.
