---
name: runtime-scale-engineering
description: Use for performance, throughput, latency, memory, concurrency or resource-pressure engineering where required capability and output quality must be preserved.
---

# Runtime Scale Engineering

## Purpose
Improve performance by locating bottlenecks rather than shrinking the user's goal or turning off required work.

## Activate when
Use for slow agents, high RAM/CPU, queueing, serialization, repeated context loading, excessive retries, cache misses, contention or throughput limits.

## Do not activate
Do not optimize before measuring, and do not treat lower quality, fewer required tasks or disabled functionality as success.

## Antigravity-native execution
Baseline the real workload and target environment. Inspect scheduling, parallelism, process count, context/tool payload, I/O, network route, retries, cache reuse, checkpoint frequency and OS constraints. Prefer event-driven/on-demand mechanisms over needless resident workers.

## Workflow
1. Define performance and correctness SLOs.
2. Measure baseline under representative workload.
3. Identify dominant wait/resource/serialization path.
4. Apply one causal optimization at a time.
5. Re-measure latency, throughput, resource use and correctness.
6. Run regression under stress and restart/resume when relevant.

## Validation
A performance win counts only if protected functionality and quality acceptance still pass. Report tradeoffs and measurement uncertainty.

## Boundaries
Do not bypass quotas, safety controls or OS protections. Avoid permanent background services when an on-demand/native mechanism satisfies the same goal.