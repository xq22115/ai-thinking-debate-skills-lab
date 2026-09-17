---
name: agent-concurrency-backpressure
description: Use when multiple agents, model calls, tools, workers, retries, queues, or background tasks run concurrently and rate limits, overload, duplicate side effects, starvation, or unstable latency are plausible.
---

# Agent Concurrency and Backpressure

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

Parallelism is a capacity decision, not a speed setting. Increase concurrency only while the bottleneck has headroom and the work is causally independent.

## Capacity model

Identify the actual constrained resource before tuning: provider request/token limits, model queue, CPU, RAM, disk, browser/renderer, connector session, MCP server, database, filesystem lock, or human approval lane.

Track at least:

- in-flight operations by resource;
- queue depth and age;
- success/error/429/timeout rates;
- p50/p95 latency and throughput;
- retry count and retry amplification;
- cancellation/abandonment;
- duplicate side effects;
- per-run token/cost usage when relevant.

## Control rules

1. Parallelize only tasks without unresolved write/order dependencies.
2. Use separate concurrency budgets per bottleneck; one global worker count hides local overload.
3. Bound every queue. Decide explicitly whether overflow blocks, sheds, coalesces, or fails.
4. Propagate backpressure upstream instead of spawning more work when the downstream consumer is saturated.
5. Make effectful operations idempotent or deduplicated before retrying them.
6. Honor server retry guidance such as `Retry-After`; otherwise use bounded exponential backoff with jitter for transient failures. Do not stack retry loops unknowingly across SDK, worker, and orchestrator layers.
7. Add deadlines and cooperative cancellation. A timed-out parent must not leave expensive orphan work running unless continuation is intentional.
8. Use fairness or per-tenant/per-task limits when one long job can starve others.
9. Reduce concurrency when error rate, tail latency, queue age, memory, or rate-limit pressure rises; do not wait for total failure.
10. Record the chosen concurrency budget and the evidence that justified it.

## Failure patterns

- spawning more agents after latency rises;
- parallel writes to the same target;
- retry storms where failed requests consume more rate-limit budget;
- hidden SDK retries multiplied by application retries;
- unlimited task queues that convert overload into RAM pressure;
- measuring average latency while p95/p99 and queue age explode;
- treating provider quota as a local hardware problem.

## Verification

Run controlled load steps rather than one maximum blast. Compare throughput, tail latency, errors, queue age, and side effects at increasing concurrency. The selected operating point should be below the first unstable knee and should recover after a transient limit event.

## Release gate

`PASS` requires bounded queues, explicit resource budgets, retry/cancellation behavior, no duplicate effectful actions under retry, and a measured stable operating region. Otherwise mark the untested layer `NOT_RUN`.
