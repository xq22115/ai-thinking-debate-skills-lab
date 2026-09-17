# AI Runtime Specialist Pack v1

Status: `EXPERIMENTAL / STACKED ON AI_ENGINEERING_GAP_PACK_v1 / NOT HOST-LIVE VERIFIED`
Date: 2026-09-18
Base pack revision: `ce75567d063e6ac3e7a1c042728ced400a529325` (PR #58 head at creation)

## Purpose

Add narrowly scoped runtime specialists that the broader AI Engineering Gap Pack intentionally does not duplicate. These skills convert recurring Windows/desktop/bridge incidents into reusable diagnostics with explicit falsifiers and runtime evidence requirements.

## New specialists

| Runtime failure family | Specialist | Existing skills composed |
|---|---|---|
| Electron/Chromium process-count, renderer churn, suspected leak/crash loop | `electron-chromium-process-forensics` | `agent-observability-slos`, `agent-runtime-forensics` |
| Windows/macOS desktop UI automation, DPI/coordinate space, layout/focus/input races | `desktop-ui-automation-reliability` | `identity-session-isolation`, `agent-containment-and-rollback` |
| MCP/native-host/bridge lifecycle, stale sessions, reconnect/affinity failures | `mcp-bridge-reliability` | `mcp-surface-engineering`, `identity-session-isolation`, `agent-concurrency-backpressure` |

## What is deliberately not duplicated

The base pack already owns:

- general observability/SLOs → `agent-observability-slos`;
- evaluation operations → `agent-evaluation-operations`;
- identity/session/account isolation → `identity-session-isolation`;
- containment/rollback → `agent-containment-and-rollback`;
- concurrency/backpressure → `agent-concurrency-backpressure`;
- long-horizon context → `long-horizon-context-engineering`;
- tool contracts → `tool-contract-testing`;
- release parity → `runtime-release-parity`;
- model routing/budget → `model-routing-budget-control`;
- generic runtime causality → `agent-runtime-forensics`.

## Runtime incident composition

Start with the base pack owner, then load at most one specialist unless evidence shows two independent mechanisms:

`goal/target identity → base owner → runtime specialist if trigger matches → evidence/read-back → regression → completion gate`

Examples:

- many ChatGPT.exe processes → observability + Electron specialist, not immediate zombie diagnosis;
- missing desktop composer at 200% scaling → identity/session + desktop UI specialist + containment if a recovery guard can reload;
- MCP server listed but reconnect uses stale session/device → MCP surface + bridge specialist + identity/session isolation.

## Promotion boundary

Repository presence proves package source state only. Fresh-context skill invocation, plugin discovery, target-host activation, Windows/macOS behavior, and regression stability remain separate gates.

See:

- `evals/AI_RUNTIME_SPECIALIST_PACK_v1.md`
- `references/AI_RUNTIME_SPECIALIST_SOURCES_2026_09.md`
