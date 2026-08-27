# AI Thinking, Debate, and Skills Lab

This repository is an executable agent-control-plane lab. Its primary goal is not to accumulate prompts or green checks; it is to turn an explicit task goal into bounded execution, observable state, task-specific acceptance evidence, and recoverable results while preserving the existing A01-A10 execution kernel.

## Active truth map

- **Active ordinary-chat candidate:** `ordinary-chat-agent-stack-v5-task-runtime`.
- **Stable merged baseline:** `main`.
- **v2:** local bridge, MCP v2 gateway, browser routing, scoped memory, dashboard, and A01-A10 integration foundation.
- **v3 / v3.1 / v3.2:** adaptive routing, liveness, adversarial verification, and chaos/recovery hardening.
- **v4:** historical infrastructure self-test. It is diagnostic evidence only and is **not** a general task executor.
- **v5:** real declarative repository-task runtime with dependency ordering, task-specific acceptance, durable resume, changed-path adjudication, receipt integrity, and dedicated `chat-task/*` mutation branches.

Historical evidence is retained under `archive/`; generated proof bundles do not belong in the active runtime source tree.

## Execution routes

1. Use an already-connected provider tool when it directly supports the requested operation.
2. Use the v5 GitHub task runtime for dependency-aware repository tasks that can run on GitHub Actions.
3. Use the authorized local bridge for bounded local inspection/editing when an authorized device is online.
4. Use Playwright CLI for deterministic browser work and Playwright MCP for stateful browser sessions.
5. Use the existing A01-A10 runtime for long, governed local workflows with dependency waves, receipts, and final adjudication.

A route is selected because it can satisfy the task contract, not because it has a convenient PASS label.

## Completion rule

A task is not complete merely because a workflow started, a PR exists, files were written, or unrelated CI is green. For the v5 task path, completion requires all of the following on the same request revision:

- the goal/request contract is bound and hashed;
- required execution or effects actually occur;
- task-specific acceptance checks pass;
- durable resume proves zero unintended side-effect replay;
- receipts and changed-path provenance are internally consistent.

The heterogeneous A01-A10 review jobs are deterministic verification lanes. They are **not** represented as ten independent AI model agents.

## Repository map

- `control-plane/scripts/` — execution, bridge, routing, reconciliation, validation, and task runtime code.
- `control-plane/ai-system/` — machine-readable configs, MCP gateway, contracts, and agent definitions.
- `control-plane/tests/` — regression, adversarial, chaos, resume, and provenance tests.
- `control-plane/ordinary-chat-dashboard/` — read-only local observability UI.
- `skills/ordinary-chat-agent-router/` — ordinary-chat routing contract.
- `docs/` — architecture and operating policies.
- `research/ordinary-chat-upstreams/` — dated upstream/evidence ledger.
- `archive/ordinary-chat-v4-evidence/` — preserved v4 self-test requests/proofs after source/evidence separation.

## Important boundary

This repository can expand authorized capability through GitHub Actions, plugins/connectors, local bridges, MCP, browser tooling, scoped memory, and agent runtimes. It does not force-enable product features, hidden model routes, plan-gated capabilities, or host permissions that the product has not exposed.

## Engineering policy

Prefer preserving and strengthening working foundations over deleting capability to make a test pass. When a verifier and the implementation disagree, inspect the real execution semantics first. A failed gate is evidence to investigate, not something to weaken until it turns green.
