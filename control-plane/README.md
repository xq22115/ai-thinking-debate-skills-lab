# Control Plane

This directory contains the executable control plane for the repository. It is not a GitHub demo template.

## Runtime layers

- `scripts/ordinary_chat_task_runtime.py` — v5 declarative repository-task executor and outcome adjudicator.
- `scripts/ordinary_chat_bridge.py` — bounded bridge to authorized local runtimes.
- `scripts/capability_health.py` + `scripts/capability_router.py` — health-aware capability selection.
- `scripts/run_reconciler.py` — persisted run/liveness reconciliation.
- `scripts/run_local_agent_workflow.py` and related scripts — existing A01-A10 governed execution kernel.
- `ai-system/mcp/` — MCP TypeScript v2 gateway.
- `ordinary-chat-dashboard/` — read-only localhost status/receipt UI.

## Task path

Real GitHub repository tasks use a schema-v2 request under `control-plane/ordinary-chat-task-requests/` on a dedicated `chat-task/*` branch. The task workflow executes the dependency graph, validates declared mutations against the actual working tree, evaluates task-specific acceptance, performs a zero-reexecution resume probe, uploads receipts, and only then may commit the declared mutation.

The old v4 `ordinary_chat_completion_gate.py` remains a historical infrastructure diagnostic. Its generated requests/proofs are archived under `archive/ordinary-chat-v4-evidence/` and must not be used as evidence that an arbitrary user task completed.

## Verification

The active candidate is expected to pass, on one exact revision:

- Ordinary Chat Agent Stack — bridge, memory, routing, reconciliation, dashboard, policy, bootstrap and MCP integration.
- Ordinary Chat Task Runtime CI — real mutation/resume and negative cases.
- Context First Capability Gate.
- Deep Reasoning Quality Gate including full main-baseline comparison.
- Ordinary Chat v5 Ten-Lane Review — ten distinct deterministic review lanes plus aggregate adjudication.

A green check outside the relevant task contract is not completion evidence.

## Local use

See `../docs/ordinary-chat-agent-stack-v2.md`, the v3 runbook, and `ordinary-chat-dashboard/README.md`. Local execution still depends on an authorized reachable device/runtime; GitHub cloud task execution does not imply that a local device is online.
