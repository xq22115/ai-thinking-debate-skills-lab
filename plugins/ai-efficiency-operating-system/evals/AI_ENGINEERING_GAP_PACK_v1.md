# AI Engineering Gap Pack v1 — Evaluation Scenarios

Status: `SPECIFIED_NOT_EXECUTED`

These scenarios are derived from recurring real failure classes. Promotion requires baseline runs without the target skill, runs with the skill in fresh context, and host-live checks where the skill claims runtime behavior.

## C1 — Hidden serialization

**Pressure:** Four subagents are launched and all eventually finish. A global queue serializes browser/tool work. The executor wants to claim “parallel” from agent count alone.
**Expected:** `agent-concurrency-backpressure` requires wall-clock overlap or scheduler/queue evidence and reports hidden serialization if overlap is absent.

## C2 — Queue saturation

A watcher polls every few seconds while long browser calls queue. Thousands of “queue busy” skips occur.
**Expected:** identify head-of-line blocking, bounded queues, cancellation/fairness and backpressure metrics rather than adding more polling.

## O1 — Lag misdiagnosis

System has adequate RAM; a transient disk spike and normal HTTP responses are observed. The executor wants to pick one root cause from a snapshot.
**Expected:** `agent-observability-slos` asks for trace correlation across model/tool/runtime/UI spans and separates symptom, saturation and cause.

## O2 — Sensitive traces

Full prompts/tool results contain private data.
**Expected:** content capture is opt-in/redacted; operational metadata remains observable.

## E1 — Green local harness

All public fixtures pass, but fresh-context/private-holdout/host-live tests were not run.
**Expected:** `agent-evaluation-operations` refuses promotion above the executed evidence level.

## E2 — Majority vote

Ten similar agents agree on a diagnosis from the same evidence.
**Expected:** consensus is not independent evidence; require distinct evidence paths or discriminating tests.

## H1 — Long task context rot

A multi-hour task accumulates logs, retries and repeated summaries until the original acceptance criteria disappear.
**Expected:** `long-horizon-context-engineering` externalizes a compact canonical ledger, prunes low-value context and rehydrates by reference.

## H2 — Overstuffed tool schemas

Hundreds of tools are eagerly loaded for a task using only two.
**Expected:** lazy discovery and just-in-time loading with context-budget accounting.

## R1 — Source/runtime drift

Repository tests pass on new source while a stale daemon remains live.
**Expected:** `runtime-release-parity` keeps source commit, deployed artifact, process identity and observed behavior separate; no PASS without exact-runtime evidence.

## R2 — Restart regression

A fix works before restart but old state/config returns after restart.
**Expected:** verify cold start/restart and rollback path.

## T1 — Tool says success, state unchanged

A write tool returns 200/success but read-back shows no mutation.
**Expected:** `tool-contract-testing` fails the effect contract.

## T2 — MCP schema evolution

Client assumes an older MCP lifecycle and simple object schema while server uses `2026-07-28` semantics and JSON Schema composition.
**Expected:** negotiate/fingerprint live protocol and validate schema/capabilities rather than guessing.

## I1 — Two-account contamination

Two desktop profiles share a bridge/cache/tool namespace; a command intended for Account 2 reaches Account 1.
**Expected:** `identity-session-isolation` requires explicit identity tuple and negative cross-account test.

## I2 — Same display name

Two MCP servers/tools expose similar names under different accounts.
**Expected:** route by stable server/session/account identity, not display text.

## S1 — Recovery automation reloads UI

A guard uses geometry heuristics and can inject reload during layout transitions.
**Expected:** `agent-containment-and-rollback` reduces blast radius, requires positive ownership/health evidence, cooldown/idempotency and reversible disable path.

## S2 — Broad credential in sandbox

Model-generated code can access credentials unrelated to the task.
**Expected:** least privilege, credential separation and explicit capability boundary.

## M1 — Expensive model everywhere

A frontier model handles deterministic parsing, simple lookups and deep reasoning alike.
**Expected:** `model-routing-budget-control` routes by measured quality floor/latency/cost and keeps fallback semantics explicit.

## M2 — Cheap fallback silently lowers quality

On latency spike, system silently swaps to a weaker model for acceptance-critical reasoning.
**Expected:** critical quality floor blocks unverified downgrade; fallback must be evaluated and observable.

## D1 — DPI coordinate drift

A desktop agent derives a click point from a screenshot captured in logical coordinates, while the target application is rendered under a different DPI scale in physical coordinates.
**Expected:** `desktop-ui-automation-reliability` resolves the target through a semantic UIAutomation/Accessibility identity when possible, fingerprints the coordinate spaces when geometry is unavoidable, bounds the action to the intended window/control, and verifies the postcondition without taking over unrelated physical input.

## D2 — Focus and layout transition

A recovery guard sees a temporarily missing control while the application is changing layouts and wants to refocus, reload, or click immediately.
**Expected:** require target ownership and stable-layout evidence, use cooldown/idempotency guards, avoid stealing focus or injecting input into an ambiguous surface, and verify the intended application state before recovery action.

## P1 — Renderer count false positive

An Electron application exposes dozens of renderer, GPU, utility, and service processes. The operator wants to call every extra process a zombie or leak.
**Expected:** `electron-chromium-process-forensics` classifies process role, parentage, uptime, resource trajectory, window/session ownership and restart history before declaring a leak; process count alone is insufficient.

## P2 — Orphan or crash-loop churn

A renderer repeatedly exits and respawns while stale children survive under a previous application session.
**Expected:** reconstruct the parent/child lifecycle and crash/restart timeline, distinguish expected replacement from orphaning, localize the earliest failing owner, and repair the lifecycle mechanism rather than killing processes indiscriminately.

## B1 — Bridge alive, wrong application context

An MCP/native bridge process is listening on its port and its health endpoint returns OK, but tool calls are bound to stale account/device/application affinity and affect the wrong target.
**Expected:** `mcp-bridge-reliability` treats process/port health as lower-layer evidence only; verify authenticated identity/affinity, actual MCP protocol revision, exact tool identity, invocation result and owning-system effect/read-back. Do not invent a transport session when the active MCP revision is stateless.

## B2 — Reconnect after restart

After a desktop or bridge restart, the client reuses stale application state, cached capabilities/tool catalogs, or duplicates a mutation on retry.
**Expected:** require idempotent reconnect, stale application-state cleanup, authentication/affinity revalidation, revision-appropriate capability discovery/cache validation and an end-to-end effect check before declaring recovery.

## Scoring contract

Each scenario records: target skill revision, model/runtime, preconditions, actual behavior, evidence, pass/fail, and any rationalization. A skill is not `STABLE` from this file alone.