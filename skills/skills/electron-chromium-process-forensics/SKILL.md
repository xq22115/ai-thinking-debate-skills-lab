---
name: electron-chromium-process-forensics
description: Use when an Electron or Chromium-based application shows many child processes, high memory or handle counts, renderer restarts, suspected zombies, crash loops, or unexplained UI lag.
---

# Electron Chromium Process Forensics

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

A multi-process tree is normal architecture. Diagnose abnormal lifecycle behavior, not raw process count.

## Minimum model

Classify each observed process when possible: root/main, renderer, GPU, utility/service, crash handler, extension/worker, or unknown. Build parent-child lineage before interpreting counts.

## Diagnostic sequence

1. Identify every top-level app root and map it to account/profile/window identity.
2. Snapshot child count, role/command line, PID start time, working set/private bytes, CPU, handles, and parent PID.
3. Repeat snapshots over time. Churn and monotonic growth matter more than one large value.
4. Check crash evidence independently: crash reports, event logs, exit codes, crashpad artifacts, renderer termination reasons, or repeated root replacement.
5. Separate expected renderer multiplicity from orphaning: a child whose parent is gone, repeated same-role recreation, or unbounded resource growth is stronger evidence than quantity alone.
6. Correlate lifecycle events with the user-visible lag. A PID change during unrelated configuration work is not automatically a crash-loop cause.
7. Compare per-root behavior. Two isolated accounts should normally have separate roots and supporting processes; do not merge them into one leak diagnosis.
8. Only after evidence supports a lifecycle defect should repair target session restoration, stale background work, extension/worker churn, or app restart strategy.

## Falsifiers

A zombie/crash-loop hypothesis is weakened when:

- children have live parents;
- crash handlers roughly match independent roots;
- no crash/termination evidence exists;
- renderer counts are stable across repeated snapshots;
- memory/handles plateau under equivalent workload;
- user lag occurs without lifecycle churn.

A leak/churn hypothesis strengthens when repeated controlled samples show unbounded growth, frequent renderer replacement, orphaned descendants, or resource recovery only after removing a specific workload.

## Common mistakes

- Calling every renderer a zombie.
- Killing processes before recording lineage and timing.
- Treating a single 800 MB renderer as proof of a leak.
- Ignoring service workers, embedded web contents, extensions, or multiple independent app roots.
- Using a restart as a repair without proving the restart mechanism caused the symptom.

## Release gate

State the strongest evidenced classification: `EXPECTED_MULTIPROCESS`, `SUSPICIOUS_CHURN`, `LEAK_EVIDENCE`, `CRASH_LOOP_EVIDENCE`, or `UNRESOLVED`. Do not overclaim root cause from process count alone.
