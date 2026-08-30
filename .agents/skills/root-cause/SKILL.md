---
name: root-cause
description: Use when several symptoms may share an upstream mechanism or when a proposed fix risks patching symptoms instead of correcting the causal owner.
---

# Root Cause

## Purpose
Cluster failures by mechanism and repair the earliest shared cause that explains the observed behavior while preserving required functionality.

## Activate when
Use for repeated regressions, correlated failures, freezes, latency spikes, state corruption, routing mistakes or many seemingly separate bugs.

## Do not activate
Do not invent a grand common cause when evidence supports independent failures; keep independent clusters separate.

## Antigravity-native execution
Inspect target identity, event timing, dependency graph, state transitions, retries, queues, caches, serialization, resource pressure, permissions and version/config boundaries. Prefer reversible discriminating probes before broad edits.

## Workflow
1. Build symptom/event timeline.
2. Group by shared dependency/state/timing.
3. Maintain competing upstream mechanisms.
4. Probe high-centrality causes first.
5. Repair the smallest owning layer.
6. Re-test all symptoms and protected capabilities.

## Validation
A root cause must predict more than one observation or decisively explain the target defect and be falsifiable. Reproduction should fail before and pass after the fix where practical.

## Boundaries
Do not call feature deletion, lower quality, reduced concurrency or less usage a root-cause fix unless the user explicitly accepts that outcome.