# AI Engineering Gap Pack v1

Status: `EXPERIMENTAL / NOT HOST-LIVE VERIFIED`
Date: 2026-09-18
Base revision: `b3b10ef0cf09cafb29a5fa4ae3e53f0549ad8154`

## Why this pack exists

Recent work repeatedly exposed a gap between strong reasoning/verification skills and production AI-engineering execution. The existing system is already strong on evidence, competing hypotheses, root-cause analysis, durable state, capability/MCP/runtime forensics, and completion gates. The missing layer is operational engineering: concurrency, traces/SLOs, eval operations, context-budget control, release/runtime parity, tool contract tests, session isolation, blast-radius containment, and model-routing economics.

## Recurring failure patterns converted into skills

| Observed failure class | New owner |
|---|---|
| Global queue or hidden serialization makes “multi-agent” work sequential | `agent-concurrency-backpressure` |
| CPU/RAM/network guesses without end-to-end traces | `agent-observability-slos` |
| Same-model votes or green fixtures mistaken for product truth | `agent-evaluation-operations` |
| Long tasks accumulate stale/noisy context and lose the goal | `long-horizon-context-engineering` |
| Source tests pass while a stale daemon/runtime is still live | `runtime-release-parity` |
| Tool call returns success but schema/effects/retry semantics are wrong | `tool-contract-testing` |
| Two accounts/profiles/workspaces contaminate state or target identity | `identity-session-isolation` |
| Automation has excessive blast radius or weak rollback boundaries | `agent-containment-and-rollback` |
| One model is used for every subtask without quality/cost/latency evidence | `model-routing-budget-control` |

## Existing owners reused, not duplicated

- `agent-runtime-forensics` for causal reconstruction outside model prose.
- `mcp-surface-engineering` for live tool-surface identity, schema drift, entitlement and trust boundaries.
- `memory-policy` for persistent-state provenance and rehydration.
- `evidence-watchdog` / `completion-gate` for evidence-bound release claims.
- `durable-agent-control-plane` / `recoverable-state` for durable task state and resume.

## Runtime specialist extension

A stacked specialist layer covers recurring live-runtime failure modes that are too narrow for the general owners:

- `electron-chromium-process-forensics` — Electron/Chromium process lineage, renderer churn, leak/crash-loop falsification.
- `desktop-ui-automation-reliability` — UIAutomation/Accessibility targeting, DPI coordinate space, layout/focus/input races, recovery-guard reliability.
- `mcp-bridge-reliability` — MCP/native-host/bridge lifecycle, stale sessions, reconnect idempotency, device/session affinity.

See `AI_RUNTIME_SPECIALIST_PACK_v1.md`. These specialists compose with the general owners above; they do not replace them.

## Composition

For a production agent incident or build:

`goal contract → identity/session isolation → current tool/MCP surface → context budget → concurrency/resource model → observability → execution → tool contract checks → runtime/release parity → eval operations → containment/rollback → completion gate`

When a narrow runtime trigger is present, insert at most one runtime specialist after the relevant general owner unless evidence shows two independent mechanisms.

Omit layers whose trigger conditions are absent.

## Promotion ladder

`SPECIFIED → STATIC/READBACK → FRESH-CONTEXT → HOST-LIVE → REGRESSION → STABLE`

This branch may prove only the first two layers. A GitHub commit or PR is not evidence that ChatGPT, Codex, Claude, Cursor, Antigravity, MCP clients, or desktop runtimes have loaded or executed these skills.

## Primary-source learning inputs

Mechanisms were distilled from current OpenAI agent harness/API guidance, Anthropic context-engineering/eval/containment work, MCP specification `2026-07-28`, OpenTelemetry GenAI observability conventions, and current agent-workflow observability guidance. See `references/AI_ENGINEERING_2026_SOURCE_NOTES.md` and `references/AI_RUNTIME_SPECIALIST_SOURCES_2026_09.md`.

## Evaluation

General pressure scenarios live in `evals/AI_ENGINEERING_GAP_PACK_v1.md`; runtime specialist cases live in `evals/AI_RUNTIME_SPECIALIST_PACK_v1.md`. They are deliberately marked `SPECIFIED_NOT_EXECUTED` until run in a fresh context without and with each skill, followed by host-live regression where available.
