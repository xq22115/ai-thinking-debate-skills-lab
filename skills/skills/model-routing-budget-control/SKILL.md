---
name: model-routing-budget-control
description: Use when a workflow can choose among models, providers, reasoning levels, service tiers, or agent topologies and quality, latency, cost, token use, quotas, or reliability tradeoffs must be controlled.
---

# Model Routing and Budget Control

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

Route by required capability and decision risk first, then optimize cost/latency inside the set of routes that satisfy the task contract. Cheap failure is still failure.

## Route contract

For each stage classify:

- task type and required capabilities/tools/modalities;
- hard quality/safety/authorization constraints;
- uncertainty and cost of error;
- latency/deadline requirement;
- context size and expected output/tool-call volume;
- concurrency/rate-limit pressure;
- whether the stage is reversible or effectful;
- budget ceiling and escalation allowance.

## Routing pattern

1. Use deterministic rules for hard capability constraints before any learned router.
2. Use measured eval performance, not model branding or self-description, for quality-sensitive routing.
3. Allow stage-specific routing: cheap classification/retrieval may coexist with a stronger planner, verifier, or effectful decision model.
4. Escalate when uncertainty, evaluator disagreement, repeated tool failure, or high-cost irreversible action crosses a predeclared threshold.
5. Do not downgrade a hard criterion to stay under a soft token/cost budget; instead stop, simplify context, change method, or report a budget blocker.
6. Track usage per run/stage. Session history can make later turns more expensive even when each run reports its own usage.
7. Distinguish provider-side rate/quota/service-tier constraints from local CPU/RAM constraints.
8. Prefer caching, context pruning, tool deferral, batching, or lower-cost stages before weakening acceptance-critical reasoning.

## Budget dimensions

Track separately when useful: input/output/cached/reasoning tokens, model cost, wall latency, queue time, tool/API cost, retry waste, concurrency slots, and human review cost. One scalar budget can hide a catastrophic tail or quality regression.

## Evaluation

Maintain a routing benchmark with representative task families and hard failures. Compare candidate routes on task success, hard-constraint violation, latency distribution, cost, tool success, and recovery. Re-run when models, prices, service tiers, tool surfaces, or prompts materially change.

## Anti-patterns

- always using the strongest model regardless of task;
- always using the cheapest model until it fails in production;
- selecting models from advertised context size without long-context evals;
- switching service tier and claiming model capability changed;
- ignoring retry/token amplification when estimating cost;
- routing a verifier to the same failure mode with no independent evidence.

## Release gate

A routing policy is `PASS` only when hard constraints remain satisfied across the protected eval set and its budget/latency benefit is measured against a frozen baseline. Untested model/provider changes require re-evaluation before promotion.
