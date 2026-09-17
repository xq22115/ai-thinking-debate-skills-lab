---
name: ai-engineering-gap-pack
description: Use when a complex AI engineering task spans agent runtime reliability, long-horizon execution, tool/MCP contracts, concurrency, release parity, account isolation, observability/evals, repair safety, or model-routing economics.
---

# AI Engineering Gap Pack 2026-09

Status: `EXPERIMENTAL / PORTABLE PACK / HOST-LIVE NOT PRECLAIMED`

## Objective

Close the recurring gap between strong reasoning and production-grade AI engineering. Route each incident to the smallest set of mechanism-specific skills, then verify at the real runtime boundary.

## Newly added specialists

| Area | Skill |
|---|---|
| Runtime truth / root-cause evidence | `runtime-truth-diagnostics` |
| Electron/Chromium lifecycle | `electron-chromium-process-forensics` |
| Desktop UIAutomation / DPI / focus | `desktop-ui-automation-reliability` |
| MCP/bridge lifecycle | `mcp-bridge-reliability` |
| Account/device/profile isolation | `multi-runtime-account-isolation` |
| Trace/eval/trajectory evidence | `agent-observability-evals` |
| Reversible live repair | `reversible-repair-engineering` |
| Agent concurrency / backpressure | `agent-concurrency-backpressure` |
| Long-horizon context | `long-horizon-context-engineering` |
| Source/package/host parity | `runtime-release-parity` |
| Tool/connector contracts | `tool-contract-testing` |
| Model/provider/tier routing | `model-routing-budget-control` |

## Existing skills to compose instead of duplicate

Reuse the repository's mature `task-goal-intelligence`, `executive-research`, `evidence-watchdog`, `completion-gate`, `competing-hypotheses`, `root-cause-clustering`, `compatibility-audit`, `recoverable-state`, `durable-agent-control-plane`, `agent-runtime-forensics`, `mcp-surface-engineering`, and `memory-policy` when their trigger conditions apply.

## Default composition

For a material incident:

`goal/target identity → evidence acquisition → one primary domain specialist → causal repair or architecture change → exact-state read-back → user-path regression → completion gate`

Add `recoverable-state`/`long-horizon-context-engineering` for long runs; add `durable-agent-control-plane` for multi-agent writes; add `agent-observability-evals` when promotion or recurrence prevention matters.

Never load every skill merely because the task is complex.

## Pack invariants

- `CONFIGURATION != RUNTIME_TRUTH`
- `PROCESS_COUNT != LEAK`
- `REACHABILITY != APPLICATION_SUCCESS`
- `PARALLELISM != FREE_SPEEDUP`
- `QUEUE_EXISTS != BACKPRESSURE`
- `SUMMARY != SOURCE_OF_TRUTH`
- `SOURCE_GREEN != HOST_LIVE`
- `SCHEMA_VALID != TOOL_EFFECT_VERIFIED`
- `FRIENDLY_NAME != TARGET_IDENTITY`
- `CONNECTED_ONCE != BRIDGE_RELIABILITY`
- `CORRECT_FINAL_TEXT != CORRECT_TRAJECTORY`
- `CHEAPER_ROUTE != ACCEPTABLE_ROUTE`
- `LOCAL_RESOURCE_CHANGE != REMOTE_QUOTA_CHANGE`
- `RESTART_RECOVERY != ROOT_CAUSE_REPAIR`

## Evaluation assets

- `skills/evals/runtime-engineering-fixtures.json`
- `skills/evals/ai-engineering-gap-pack-fixtures.json`
- `skills/references/RUNTIME_ENGINEERING_SOURCE_MATRIX_2026-09.md`
- `skills/references/AI_ENGINEERING_GAP_PACK_SOURCE_MATRIX_2026-09.md`

## Promotion boundary

Repository read-back proves only repository state. Do not claim plugin installation, host activation, model behavior improvement, or host-live regression success until the owning runtime actually loads the intended revision and executes the protected evals/user paths.
