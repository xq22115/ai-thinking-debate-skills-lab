---
name: agent-observability-evals
description: Use when an AI agent spans multiple turns, tools, handoffs, retries, or external systems and failures must be attributed, compared across versions, or prevented from recurring with production-grade evaluation evidence.
---

# Agent Observability and Evals

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

Evaluate the trajectory, not only the final sentence. A useful agent can fail through wrong tool selection, stale context, bad handoff, repeated side effects, recovery failure, latency/cost explosion, or an apparently correct answer reached through unsafe state.

## Trace contract

Give one end-to-end run a durable trace/run ID and record spans/events for the operations that matter: model calls, tool calls, handoffs, guardrails, retrieval, external requests, checkpoints, retries, approvals, and verification.

For each span preserve when available: operation, actor/runtime, target identity, start/end, result/error class, retry relation, input/output hashes or bounded metadata, model/tool/version, and goal-contract revision. Sensitive prompt/user content is opt-in; telemetry must not become a privacy leak.

## Evaluation layers

Use the weakest layer only for early feedback, never as final proof:

`static/schema → deterministic unit → simulated tool → recorded trajectory → fresh-context scenario → holdout/adversarial → target-runtime E2E → production canary/regression`

Score multiple dimensions separately: task success, hard-constraint violations, tool correctness, side-effect correctness, recovery, latency, cost, token/context growth, and user-path completion.

## Evals that matter

1. Build fixtures from real failures, not only synthetic happy paths.
2. Include negative and ambiguous-trigger cases so a skill is not over-invoked.
3. Test perturbations: reordered context, stale state, dependency failure, timeout, duplicate call, partial success, version change, and irrelevant noisy evidence.
4. Keep evaluator/test artifacts outside ordinary optimization scope when possible.
5. Compare new model/skill/harness revisions against a frozen baseline and inspect regressions, not only average score.
6. A judge model is evidence, not ground truth; use deterministic checks or independent runtime evidence for objective properties.

## Current standards anchors

OpenAI Agents SDK tracing models traces as end-to-end workflows containing spans for generations, tools, handoffs, guardrails, and custom events. OpenTelemetry provides shared span/metric/log conventions; use standard operation naming when available rather than inventing incompatible telemetry.

## Release gate

Do not promote a skill because its file exists or a public fixture passes. Promotion requires executed evidence appropriate to the claimed layer, regression comparison, and at least one real-failure fixture that previously failed or would have exposed the defect.
