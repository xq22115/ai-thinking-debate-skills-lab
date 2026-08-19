# OpenClaw Automation Research

## Goal
Beginner-friendly desktop setup with high automation, error recovery, multi-AI routing and an explicit production/lab split.

## Archived 2026-08 research snapshot
Prior cross-chat research recorded:
- stable: `v2026.7.1-2` (GitHub latest date noted as 2026-08-04),
- extended-stable: `2026.6.34` (noted 2026-08-08),
- beta/dev/main should not be treated as production,
- 2026-08-16 main showed configuration drift from stable.

Because this archive was generated 2026-08-18 and upstream was moving quickly, these values are **not automatically treated as current installation instructions**.

## Production / lab split

### Production
- stable/extended-stable only,
- backups,
- rollback plan,
- constrained automation,
- explicit publish/send gates where consequences are material.

### Lab
- beta/dev/main experiments,
- new config schema,
- new agent/task mechanisms,
- isolated state and credentials,
- disposable test tasks.

## Desktop topology retained from prior research

### macOS
`OpenClaw.app → Local Gateway → local tools/services`

### Windows
`Hub → app-owned WSL Gateway → native node → Local MCP`

## Agent role pool concept
A prior design used roles such as:
- Commander
- Researcher
- Fact Checker
- Trend Hunter
- Browser Operator
- Social Publisher
- AI Router
- QA
- Security
- Recovery

The important idea is not the labels; it is independent responsibility and evidence.

## Automation behaviors targeted
- cross-AI input/output routing,
- automated posting/publishing,
- self-recovery after tool errors,
- retry with alternate path,
- task/flow orchestration,
- scheduled/conditional operations,
- bounded agent concurrency.

## Important warning
Do not mix stable documentation/config fields with main-branch fields without a compatibility check.
