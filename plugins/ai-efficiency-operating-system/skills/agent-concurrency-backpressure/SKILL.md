---
name: agent-concurrency-backpressure
description: Use when multiple agents, model calls, tools, workers, retries, queues, or background tasks run concurrently and hidden serialization, overload, duplicate side effects, starvation, rate limits, or unstable latency are plausible.
---

# Agent Concurrency and Backpressure

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

`AGENT_COUNT != PARALLELISM`. Parallelism is a capacity decision, not a speed setting. Prove useful overlap at the constrained resource and increase concurrency only while the bottleneck has headroom.

## Capacity model

Identify the actual constrained resource before tuning: provider request/token limits, model queue, CPU, RAM, disk, browser/renderer, connector session, MCP server, database, filesystem lock, external API, or human approval lane.

Track at least:

- enqueue/start/end timestamps and resource lane;
- in-flight operations by resource;
- queue depth, wait and age;
- throughput plus p50/p95/p99 latency;
- success/error/429/timeout rates;
- retry count and retry amplification across SDK/worker/orchestrator layers;
- cancellation/abandonment and orphan work;
- duplicate side effects;
- per-run token/cost usage when relevant.

## Control rules

1. Draw the critical path and every lock/queue/semaphore before increasing workers.
2. Compute useful concurrency from wall-clock overlap, not child/thread/agent count.
3. Use separate concurrency budgets per bottleneck; one global worker count hides local overload.
4. Parallelize only work without unresolved write/order dependencies.
5. Bound every queue. Decide explicitly whether overflow blocks, sheds, coalesces, defers, or fails.
6. Propagate backpressure upstream instead of spawning more work when downstream is saturated.
7. Make effectful operations idempotent or deduplicated before retrying them.
8. Honor server retry guidance such as `Retry-After`; otherwise use bounded backoff with jitter for transient failures. Do not stack hidden retry loops.
9. Add deadlines and cooperative cancellation. A timed-out parent must not leave expensive orphan work running unless continuation is intentional.
10. Prefer event/condition-based waits over aggressive polling; repeated `busy` responses are load, not free monitoring.
11. Use fairness or per-tenant/per-task limits when one long job can starve others.
12. Reduce concurrency when error rate, tail latency, queue age, memory, or rate-limit pressure rises.

## Verification

Run controlled load steps rather than one maximum blast. Compare overlap ratio, throughput, queue wait/age, tail latency, errors, saturation, cancellation leakage and duplicate effects at increasing concurrency. Select an operating point below the first unstable knee and verify recovery after a transient limit event.

A lower wall-clock time with duplicated effects, dropped work, hidden starvation, or violated ordering is `FAIL`.

**REQUIRED SUB-SKILL:** use `agent-observability-slos` for trace/metric evidence and `tool-contract-testing` when retries touch effectful tools.

## Output

Return the concurrency graph, constrained resources, hidden serialization points, per-resource budgets, queue/backpressure policy, retry/cancellation semantics, measured stable operating region, and regression results.
