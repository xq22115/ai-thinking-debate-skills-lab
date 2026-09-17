---
name: electron-chromium-process-forensics
description: Use when an Electron or Chromium-based application shows many child processes, high memory or handle counts, renderer restarts, suspected zombies, crash loops, or unexplained UI lag.
---

# Electron Chromium Process Forensics

Status: `EXPERIMENTAL / RUNTIME SPECIALIST`

## Core principle

A multi-process tree is normal architecture. Diagnose abnormal lifecycle behavior, not raw process count.

## Minimum model

Classify observed processes when possible as root/main, renderer, GPU, utility/service, crash handler, extension/worker, or unknown. Build parent-child lineage before interpreting counts.

## Diagnostic sequence

1. Identify every top-level app root and map it to account/profile/window identity.
2. Snapshot child count, role/command line, PID start time, working set/private bytes, CPU, handles, and parent PID.
3. Repeat snapshots over time. Churn and monotonic growth matter more than one large value.
4. Check crash evidence independently: crash reports, event logs, exit codes, crashpad artifacts, renderer termination reasons, or repeated root replacement.
5. Separate expected renderer multiplicity from orphaning: a child whose parent is gone, repeated same-role recreation, or unbounded resource growth is stronger evidence than quantity alone.
6. Correlate lifecycle events with user-visible lag. A PID change during unrelated configuration work is not automatically a crash-loop cause.
7. Compare per-root behavior. Independent accounts should be analyzed as separate roots; do not merge them into one leak diagnosis.
8. Only after evidence supports a lifecycle defect should repair target session restoration, stale background work, extension/worker churn, or restart strategy.

**REQUIRED SUB-SKILLS:** use `agent-observability-slos` for correlated timing/SLO evidence and `agent-runtime-forensics` when causal provenance is disputed.

## Falsifiers

A zombie/crash-loop hypothesis is weakened when children have live parents, crash handlers roughly match independent roots, no crash/termination evidence exists, renderer counts are stable, resources plateau, and lag occurs without lifecycle churn.

A leak/churn hypothesis strengthens when repeated controlled samples show unbounded growth, frequent renderer replacement, orphaned descendants, or resource recovery only after removing a specific workload.

## Output

Return root/process map, time-series deltas, crash evidence, strongest classification (`EXPECTED_MULTIPROCESS`, `SUSPICIOUS_CHURN`, `LEAK_EVIDENCE`, `CRASH_LOOP_EVIDENCE`, or `UNRESOLVED`), falsifiers, and next discriminating test.
