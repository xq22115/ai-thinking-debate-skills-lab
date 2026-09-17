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
| Tool call succeeds while schema/effects/retry/control semantics are wrong | `tool-contract-testing` |
| Accounts/profiles/workspaces contaminate state or target identity | `identity-session-isolation` |
| Automation has excessive blast radius or weak rollback boundaries | `agent-containment-and-rollback` |
| One model is used for every subtask without measured quality/cost/latency | `model-routing-budget-control` |
| UIAutomation/DPI/focus/layout transitions cause false actions or misses | `desktop-ui-automation-reliability` |
| Electron renderer count is mistaken for zombies/leaks without lifecycle evidence | `electron-chromium-process-forensics` |
| MCP/local bridges appear alive but fail auth/affinity/reconnect/end-to-end health | `mcp-bridge-reliability` |
| A long-running task appears to pause only because its chat/tab/client is hidden, frozen or detached | `agent-observability-slos` + existing `durable-agent-control-plane` / `recoverable-state` |
| Dictation/clipboard/remote input is emitted but the intended target control never commits the text | `desktop-ui-automation-reliability`, `tool-contract-testing` |

## Existing owners reused, not duplicated

- `agent-runtime-forensics` — causal reconstruction outside model prose.
- `mcp-surface-engineering` — live tool-surface identity, schema drift, entitlement and trust boundaries.
- `capability-forensics` — visible/authorized/invokable/effective capability-layer diagnosis.
- `memory-policy` — persistent-state provenance, injection firewall and rehydration authority.
- `evidence-watchdog` / `completion-gate` — evidence-bound release claims.
- `durable-agent-control-plane` remains a repository-level orchestration owner. `recoverable-state` keeps the repository-level semantic owner at `skills/skills/recoverable-state/SKILL.md` and is packaged inside this plugin only as a registered adapter/snapshot for host-local routing; it is not a second semantic owner and is not counted among the 12 production specialists.

## Routing architecture

The 12 production specialists are `conditional_implicit`, not default-loaded. Deterministic eligibility uses observable predicates and keeps composition bounded to at most three implicit skills:

`task-goal-intelligence → one primary specialist → evidence-watchdog`

Specialists are intentionally narrow. Examples:

- generic Desktop capability mismatch → `capability-forensics`; UIAutomation/DPI/focus fault → `desktop-ui-automation-reliability`;
- many MCP tools/schema drift → `mcp-surface-engineering`; bridge/auth/application-affinity/reconnect fault → `mcp-bridge-reliability`;
- tool reports success but no state change → `agent-runtime-forensics`; pagination/idempotency/partial-success/guardrail-boundary contract → `tool-contract-testing`;
- generic long multi-stage orchestration → `chief-of-staff-core`; context compaction/rehydration pressure → `long-horizon-context-engineering`, with persistent authority/provenance delegated to `memory-policy`.

## Evaluation evidence

Routing TDD fixture set: `evals/routing-cases.jsonl`.

- Existing protection cases: R01–R61.
- New production-specialist cases: R62–R85.
- Client-lifecycle/input-transport integration cases: R86–R89.
- Recoverable-state/control-plane integration cases: R90–R92.
- The original specialist RED evidence remains `85 cases / 24 failures`: all 24 failures mapped to the 12 newly specified production specialists while legacy cases stayed protected. R86–R92 were added later as integration hard-negatives and must not be misreported as part of that historical RED run.

Scenario-level engineering pressure cases are canonicalized in `evals/AI_ENGINEERING_GAP_PACK_v1.md`: **30 scenarios total** — 18 base engineering cases plus 12 distinct runtime-specialist adversarial cases reconciled from the same-day runtime branch. These remain `SPECIFIED_NOT_EXECUTED` for real baseline-vs-skill fresh-context/model-behavior evaluation. Cross-cutting assertions additionally require path-specific guardrail evidence, provenance/invalidation evidence for persistent memory, client-lifecycle/run-ownership evidence, end-to-end input-transport target read-back, terminal receipt/attestation evidence, and authorization-before-relevance evidence; they do not inflate the scenario count.

## MCP compatibility boundary

MCP lifecycle assumptions are version-sensitive. For `2026-07-28`, the protocol core is stateless and the legacy `initialize`/`initialized` handshake plus `Mcp-Session-Id` transport session are retired. Bridge skills therefore distinguish explicit application/account/device affinity and cached capabilities from protocol transport sessions. Every request requires protocol version and client capabilities in `_meta`; optional `clientInfo` is self-reported metadata, not an authorization/account identity. On Streamable HTTP, every request POST must also include `MCP-Protocol-Version` equal to `_meta.io.modelcontextprotocol/protocolVersion`; a mismatch is rejected with HTTP 400 and `HeaderMismatch`. Header routing (`Mcp-Method` / `Mcp-Name`), cache hints, extensions/tasks and authorization behavior remain part of the versioned contract. Older protocol revisions require their own lifecycle adapter.

## Tool-control boundary

`GUARDRAIL_CONFIGURED != TOOL_PATH_COVERED`.

A tool/control claim is valid only when the actual execution path is identified and tested. Current OpenAI Agents SDK local function tools and tools converted from local MCP server objects can participate in the local tool-guardrail pipeline when configured; handoffs, hosted MCP/hosted tools and built-in execution tools have different control paths and must not inherit that proof by name similarity.

## Persistent context boundary

Persistent memory is storage plus an authority boundary, not a free trust upgrade. Retrieved repository/web/tool content and old summaries retain provenance across compaction/restart; stale, contradictory, poisoned or provenance-unknown entries must be quarantined/superseded/invalidated before they can steer effectful work. The canonical enforcement owner remains `memory-policy`; `long-horizon-context-engineering` is responsible for preserving those trust/provenance semantics through context pressure and rehydration.

## Client lifecycle boundary

`UI_NOT_RENDERING != RUN_STOPPED` and `RUN_EXISTS != RUN_PROGRESSING`.

A long-running agent must distinguish durable run/task identity and actual execution ownership from the client renderer, page/chat visibility and output subscription. Hidden/frozen/discarded/background-throttled client state can delay or stop client-side tasks/rendering without proving what the owning backend/worker did. Reattachment must recover state without replaying unsafe completed effects. The canonical owner inside this plugin is `agent-observability-slos` for correlated evidence. Repository-level `durable-agent-control-plane` / `recoverable-state` should be used for resumable execution only when the host actually exposes those skills; otherwise the active skill must emit the equivalent checkpoint contract directly and report the external dependency unavailable.

## Input transport boundary

`INPUT_SENT != TARGET_COMMITTED`.

Text entry across local/remote desktop boundaries is an end-to-end transport: source text, clipboard/IME, remote-session transport, host input/clipboard, foreground target control and committed target value. Clipboard sync, key mapping, foreground ownership and Windows integrity/UIPI can fail independently. The canonical owner is `desktop-ui-automation-reliability`, with `tool-contract-testing` used where lower-layer APIs report success without target effect.

## Terminal evidence boundary

`ATTESTED != COMPLETED`. For asynchronous or interrupted work, distinguish `SENT → DELIVERED → ACKNOWLEDGED → INCORPORATED → VERIFIED` where those states exist. A terminal claim should bind the strongest available independent planes — worker/thread health, completion event or terminal state, owning-target read-back, and a persisted receipt/checkpoint. Missing, malformed, stale or unknown-generation receipts produce `UNKNOWN`, not success; receipts must not persist secrets.

## Authorization-before-relevance boundary

Relevance cannot widen authority. Retrieval and tool discovery must constrain candidates by current principal/account/tenant/entitlement identity before semantic relevance, utility or risk ranking. Re-authorize before sensitive execution when identity, entitlement or target state can drift.

## Promotion ladder

`SPECIFIED → STATIC/READBACK → DETERMINISTIC_ROUTING_CI → FRESH-CONTEXT → HOST-LIVE → REGRESSION → STABLE`

Repository/CI success does not prove that ChatGPT, Codex, Claude, Cursor, Antigravity, desktop apps, or MCP clients have loaded or executed these skills. Host activation must be separately observed.

## Current-source learning inputs

Mechanisms were checked against current primary sources: OpenAI Agents API and Agents SDK tracing/guardrails/tool boundaries, Anthropic context-engineering/eval/containment engineering notes, MCP specification `2026-07-28`, OpenTelemetry GenAI semantic conventions/observability, Microsoft Agent Framework workflow observability, OWASP 2026 Memory & Context Poisoning guidance, Chromium Page Lifecycle/Page Visibility, Electron background throttling/process lifecycle, Windows UI Automation/SendInput integrity behavior, and Parsec copy/paste/key-mapping guidance. See `references/AI_ENGINEERING_2026_SOURCE_NOTES.md`.

## Invalidation rule

Product-specific facts are not timeless skill axioms. Before relying on a provider API, protocol lifecycle, SDK feature, guardrail pipeline, desktop coordinate behavior, Electron process signal or semantic convention after a material version/runtime change, re-check the current owning source and update the version-specific adapter without weakening the portable mechanism.
