---
name: agent-concurrency-backpressure
description: Use when multiple agents, tool calls, browser sessions, workers, watchers, or queues are expected to run concurrently but throughput is poor, work appears serialized, queue wait grows, or retries/polling amplify load.
---

# Agent Concurrency and Backpressure

## Core principle

`AGENT_COUNT != PARALLELISM`. Prove overlap at the constrained resource.

## Model the scheduler

Identify:

- work units and ownership;
- shared locks/queues/semaphores;
- resource classes: model, browser, filesystem, network, CPU, external API;
- max concurrency per class;
- queue discipline, fairness and cancellation;
- retry/poll sources and admission limits.

## Workflow

1. Draw the actual critical path and every serialization point.
2. Measure enqueue time, start time, end time and resource lane for representative work.
3. Compute useful concurrency from **wall-clock overlap**, not child/thread count.
4. If unrelated work shares one global queue, partition by the narrowest safe isolation key: session, browser, target, account or resource class.
5. Bound queues; reject, defer or shed low-value work before memory/latency becomes unbounded.
6. Propagate cancellation/deadlines so abandoned parent work does not keep consuming capacity.
7. Replace aggressive polling with event/condition-based waits when available.
8. Test fairness, burst load, slow consumer, partial failure and shutdown/cleanup.

## Hard rules

- Never increase worker count before locating the bottleneck.
- A watcher that repeatedly receives `busy` is load, not free monitoring.
- Retries consume concurrency budget and need jitter/bounds.
- Parallel writes to one dependent target require a serialization contract; unrelated targets should not inherit that lock.
- Throughput gains must not violate ordering, identity isolation or rate limits.

## Verification

Report baseline and repaired: overlap ratio, queue wait p95, throughput, cancellation leakage, error rate and resource saturation. A lower wall-clock time with duplicated effects or dropped work is `FAIL`.

## Output

Return concurrency graph, hidden serialization points, backpressure policy, cancellation semantics, measured overlap and regression results.
