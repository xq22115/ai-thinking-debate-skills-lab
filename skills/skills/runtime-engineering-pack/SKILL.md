---
name: runtime-engineering-pack
description: Use when a complex AI engineering task crosses live runtime diagnosis, desktop automation, Electron/Chromium behavior, MCP or bridge reliability, multiple accounts/devices, agent observability, or high-risk repair boundaries.
---

# Runtime Engineering Pack

Status: `EXPERIMENTAL / PACK ROUTER`

## Purpose

Route live AI-engineering incidents to the smallest set of specialized skills instead of solving everything with generic reasoning or a monolithic checklist.

## Skill map

| Symptom / task | Load |
|---|---|
| Slow, flaky, contradictory runtime evidence | `runtime-truth-diagnostics` |
| Many Electron/Chromium processes, renderer churn, suspected leak/crash loop | `electron-chromium-process-forensics` |
| Missing UI controls, DPI/layout flakiness, focus/input interference | `desktop-ui-automation-reliability` |
| MCP/connector/native-host/bridge disconnects or stale sessions | `mcp-bridge-reliability` |
| Two accounts/devices/profiles/runtimes can cross-pollute | `multi-runtime-account-isolation` |
| Need traces, evals, trajectory attribution, regression measurement | `agent-observability-evals` |
| Live repair must preserve capabilities and remain rollback-safe | `reversible-repair-engineering` |

Also compose with existing repository skills when triggered:

- `task-goal-intelligence` for ambiguous target/outcome;
- `competing-hypotheses` for materially different explanations;
- `root-cause-clustering` for mechanism-level grouping;
- `durable-agent-control-plane` for multi-agent execution and durable receipts;
- `recoverable-state` for long-horizon checkpoints;
- `completion-gate` before claiming success;
- `compatibility-audit` for version/host/product-surface uncertainty.

## Composition rule

Load only what the incident needs. Typical live incident path:

`goal/target identity → runtime-truth-diagnostics → one or more domain skills → reversible-repair-engineering → agent-observability-evals when regression evidence is needed → completion-gate`

For long-running or multi-agent work, add `recoverable-state` and `durable-agent-control-plane` before mutation.

## Pack invariants

- `CONFIGURATION != RUNTIME_TRUTH`
- `PROCESS_COUNT != LEAK`
- `REACHABILITY != APPLICATION_SUCCESS`
- `FRIENDLY_NAME != TARGET_IDENTITY`
- `CONNECTED_ONCE != BRIDGE_RELIABILITY`
- `SENT_INPUT != INPUT_RECEIVED`
- `CORRECT_FINAL_TEXT != CORRECT_TRAJECTORY`
- `RESTART_RECOVERY != ROOT_CAUSE_REPAIR`
- `REPOSITORY_ARTIFACT != HOST_LIVE_ACTIVATION`
- `LOCAL_RESOURCE_CHANGE != PROVIDER_SIDE_LIMIT_CHANGE`

## Regression assets

- `skills/evals/runtime-engineering-fixtures.json`
- `skills/references/RUNTIME_ENGINEERING_SOURCE_MATRIX_2026-09.md`

The fixture suite is intentionally marked `NOT_YET_TARGET_MODEL_EXECUTED`; file presence is not promoted into evaluation success.
