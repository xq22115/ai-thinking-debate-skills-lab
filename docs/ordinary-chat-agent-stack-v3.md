# Ordinary Chat Agent Stack v3 — Adaptive Runtime

## Objective

Extend the validated v2 ordinary-chat stack with health-aware routing and durable run observability while preserving the existing A01-A10 execution kernel. The goal is not to imitate a hidden ChatGPT host mode; it is to make ordinary chat choose and supervise authorized external/local execution layers more intelligently.

## What v3 Adds

### 1. TTL capability health

`control-plane/scripts/capability_health.py`

- checks only fixed known local runtimes and CLIs;
- never executes a user-supplied command;
- distinguishes `ready`, `not_installed/not_ready`, and `external_preflight_required`;
- treats GitHub/Remote Desktop connectivity as host-side state instead of fabricating a local PASS;
- caches a private health snapshot under `ORDINARY_CHAT_STATE_DIR` with a bounded TTL.

MCP tool: `capability_health`.

### 2. Deterministic adaptive routing

`control-plane/scripts/capability_router.py`

Supported intents:

- `repository_action`
- `local_bounded`
- `local_long`
- `multi_step_repair`
- `browser_deterministic`
- `browser_adaptive`
- `browser_stateful`
- `project_recall`
- `observability`
- `capability_discovery`

The router ranks only capability IDs that exist in the repository registry. It does not execute the selected route. A route can be `PASS`, `CONDITIONAL`, or `BLOCKED`; host-side apps remain conditional until their connected-app preflight succeeds.

MCP tool: `capability_route`.

### 3. Run liveness reconciliation

`control-plane/scripts/run_reconciler.py`

Persisted `QUEUED/RUNNING` is no longer treated as proof that the worker still exists. The reconciler reports:

- `STARTING`: active record inside startup grace with no worker PID yet;
- `LIVE`: worker PID exists;
- `STALE`: active record but the worker PID is gone, or no PID appeared before the grace window expired;
- `TERMINAL`: persisted terminal state remains authoritative.

It is deliberately read-only. A stale mutation run is not retried automatically because the previous worker may have produced partial side effects.

MCP tool: `agent_run_liveness`.

### 4. Three browser routes instead of one

- **Playwright CLI/Skill** — deterministic, replayable, high-frequency browser operations.
- **Browser Use CLI/Skill** — optional adaptive multi-step browser agent loop.
- **Playwright MCP** — persistent state, exploratory interaction, accessibility-tree/MCP introspection, extension attachment.

Optional Browser Use installer:

```bash
bash control-plane/scripts/bootstrap_browser_use.sh
```

The installer requires a clean governed repository, installs with `uv`/Python 3.12, registers Browser Use's upstream Skill in its supported user-level skill locations, verifies the CLI, checks that the repository stayed clean, and writes a private version receipt. Browser Use is optional; the v2 Playwright route remains independently usable.

## MCP v0.3.0 Read-Only Surface

Default read-only tools now include:

- `capabilities`
- `capability_health`
- `capability_route`
- `bridge_preflight`
- `agent_run_status`
- `agent_run_liveness`
- `agent_receipt_summary`
- `project_memory_search`

Mutation tools remain behind the existing explicit environment gates.

## Upstream Source Discipline

Exact upstream commits and adopted/not-adopted patterns are recorded in:

`research/ordinary-chat-upstreams/2026-08-27.json`

Current reference projects include OpenHands, LangGraph, Pydantic AI, Playwright CLI, Browser Use, and the MCP TypeScript SDK. v3 adopts architecture patterns while avoiding wholesale vendoring and replacement of the already-tested A01-A10 runtime.

## 2026 MCP Alignment

The gateway continues to use the MCP TypeScript SDK v2 / `2026-07-28` generation. Protocol-level discovery, stateless transport behavior, version negotiation, and wire handling stay owned by the SDK. v3's `capability_health`/`capability_route` are application-level tools; they do not reimplement `server/discover`.

## Verification Standard

v3 is acceptable only when:

1. health/router/reconciler Python modules compile;
2. their regression suites pass;
3. existing bridge/memory/dashboard tests still pass;
4. MCP TypeScript typecheck passes;
5. a real MCP client can list and call the new adaptive tools;
6. the full v2 Context First and Deep Reasoning gates remain green;
7. v2 remains a clean rollback point.

## Product Boundary

This stack can expand ordinary-chat capability by routing to authorized plugins, local devices, browser CLIs, MCP servers, memory, dashboards, and agent runtimes. It cannot force-enable a server-side ChatGPT feature, remove product sandboxing, override workspace/plan gates, or manufacture a host tool that the product has not exposed.
