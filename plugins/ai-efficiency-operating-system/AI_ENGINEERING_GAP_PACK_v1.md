# AI Engineering Gap Pack v1

Status: `EXPERIMENTAL / NOT HOST-LIVE VERIFIED`
Date: 2026-09-18
Base revision: `b3b10ef0cf09cafb29a5fa4ae3e53f0549ad8154`

## Why this pack exists

Recent work repeatedly exposed a gap between strong reasoning/verification skills and production AI-engineering execution. The existing system is already strong on evidence, competing hypotheses, root-cause analysis, durable state, capability/MCP/runtime forensics, and completion gates. The missing layer is operational engineering: concurrency, traces/SLOs, eval operations, context-budget control, release/runtime parity, tool contract tests, session/application-context isolation, blast-radius containment, model-routing economics, desktop automation reliability, Electron/Chromium lifecycle forensics, and MCP bridge recovery.

## Production specialists

| Observed failure class | Skill owner |
|---|---|
| Global queue or hidden serialization makes “multi-agent” work sequential | `agent-concurrency-backpressure` |
| CPU/RAM/network guesses without end-to-end traces | `agent-observability-slos` |
| Same-model votes or green fixtures mistaken for product truth | `agent-evaluation-operations` |
| Long tasks accumulate stale/noisy context and lose the goal | `long-horizon-context-engineering` |
| Source/CI passes while a stale daemon/runtime is live | `runtime-release-parity` |
| Tool call succeeds while schema/effects/retry semantics are wrong | `tool-contract-testing` |
| Accounts/profiles/workspaces contaminate state or target identity | `identity-session-isolation` |
| Automation has excessive blast radius or weak rollback boundaries | `agent-containment-and-rollback` |
| One model is used for every subtask without measured quality/cost/latency | `model-routing-budget-control` |
| UIAutomation/DPI/focus/layout transitions cause false actions or misses | `desktop-ui-automation-reliability` |
| Electron renderer count is mistaken for zombies/leaks without lifecycle evidence | `electron-chromium-process-forensics` |
| MCP/local bridges appear alive but fail auth/affinity/reconnect/end-to-end health | `mcp-bridge-reliability` |

## Existing owners reused, not duplicated

- `agent-runtime-forensics` — causal reconstruction outside model prose.
- `mcp-surface-engineering` — live tool-surface identity, schema drift, entitlement and trust boundaries.
- `capability-forensics` — visible/authorized/invokable/effective capability-layer diagnosis.
- `memory-policy` — persistent-state provenance and rehydration.
- `evidence-watchdog` / `completion-gate` — evidence-bound release claims.
- `durable-agent-control-plane` / `recoverable-state` — durable task state and resume.

## Routing architecture

The 12 production specialists are `conditional_implicit`, not default-loaded. Deterministic eligibility uses observable predicates and keeps composition bounded to at most three implicit skills:

`task-goal-intelligence → one primary specialist → evidence-watchdog`

Specialists are intentionally narrow. Examples:

- generic Desktop capability mismatch → `capability-forensics`; UIAutomation/DPI/focus fault → `desktop-ui-automation-reliability`;
- many MCP tools/schema drift → `mcp-surface-engineering`; bridge/auth/application-affinity/reconnect fault → `mcp-bridge-reliability`;
- tool reports success but no state change → `agent-runtime-forensics`; pagination/idempotency/partial-success contract → `tool-contract-testing`;
- generic long multi-stage orchestration → `chief-of-staff-core`; context compaction/rehydration pressure → `long-horizon-context-engineering`.

## Evaluation evidence

Routing TDD fixture set: `evals/routing-cases.jsonl`.

- Existing protection cases: R01–R61.
- New production-specialist cases: R62–R85.
- RED evidence was captured before routing implementation: `85 cases / 24 failures`, with all 24 failures corresponding to the new specialists and no newly failing legacy cases.

Scenario-level engineering pressure cases are canonicalized in `evals/AI_ENGINEERING_GAP_PACK_v1.md`: **30 scenarios total** — 18 base engineering cases plus 12 distinct runtime-specialist adversarial cases reconciled from the same-day runtime branch. These remain `SPECIFIED_NOT_EXECUTED` for real baseline-vs-skill fresh-context/model-behavior evaluation.

## MCP compatibility boundary

MCP lifecycle assumptions are version-sensitive. For `2026-07-28`, the protocol core is stateless and the legacy `initialize`/`initialized` handshake plus `Mcp-Session-Id` transport session are retired. Bridge skills therefore distinguish explicit application/account/device affinity and cached capabilities from protocol transport sessions. Older protocol revisions require their own lifecycle adapter.

## Promotion ladder

`SPECIFIED → STATIC/READBACK → DETERMINISTIC_ROUTING_CI → FRESH-CONTEXT → HOST-LIVE → REGRESSION → STABLE`

Repository/CI success does not prove that ChatGPT, Codex, Claude, Cursor, Antigravity, desktop apps, or MCP clients have loaded or executed these skills. Host activation must be separately observed.

## Current-source learning inputs

Mechanisms were checked against current primary sources: OpenAI Agents API and Agents SDK tracing/guardrails, Anthropic context-engineering/eval/containment engineering notes, MCP specification `2026-07-28`, OpenTelemetry GenAI semantic conventions/observability, Microsoft Agent Framework workflow observability, Windows UI Automation/DPI guidance, and Electron process/lifecycle evidence APIs. See `references/AI_ENGINEERING_2026_SOURCE_NOTES.md`.

## Invalidation rule

Product-specific facts are not timeless skill axioms. Before relying on a provider API, protocol lifecycle, SDK feature, desktop coordinate behavior, Electron process signal or semantic convention after a material version/runtime change, re-check the current owning source and update the version-specific adapter without weakening the portable mechanism.