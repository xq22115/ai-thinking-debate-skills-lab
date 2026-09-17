---
name: runtime-truth-diagnostics
description: Use when a live agent, desktop app, CLI, bridge, or automation is slow, flaky, unresponsive, or behaving differently from configuration, documentation, search results, or prior diagnoses.
---

# Runtime Truth Diagnostics

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

Diagnose the system that is actually running. Configuration, documentation, process counts, health scripts, and model explanations are hypotheses until tied to the observed user path.

## Evidence ladder

Prefer evidence in this order when practical:

`user-path reproduction > target-runtime instrumentation > process/session state > service-specific network probe > logs/events > configuration/read-back > documentation > inference`

Never promote a lower layer into a higher claim.

## Workflow

1. Freeze the symptom precisely: trigger, target identity, timestamp/window, expected behavior, actual behavior, and whether the failure is persistent or intermittent.
2. Build competing causal classes before repairing: CPU/memory pressure, storage I/O, network/DNS/TLS/application response, renderer/UI state, automation interference, auth/session, provider-side limit, version/config drift, dependency/runtime identity.
3. Select discriminating measurements. Every probe must name which hypotheses it can strengthen or falsify.
4. Validate the probe itself. A health script that checks the wrong endpoint, a stale log, or a measurement taken during diagnostics cannot establish root cause.
5. Separate correlation from causation. A high metric during a test is not causal unless timing and mechanism match the original symptom.
6. After two same-mechanism failures, change hypothesis, instrument, environment, or verification route.
7. Repair only after the leading cause has a causal chain and a falsifier.
8. Reproduce the original user path after repair and run one adjacent regression plus one negative check.

## Required distinctions

- reachability != application success
- process count != leak
- restart != crash loop
- high instantaneous I/O != sustained storage bottleneck
- UI symptom != rendering root cause
- configured != loaded != executed != observable
- local resource change != provider quota change
- search miss != absence

## Failure patterns this skill must catch

- Using a generic connectivity endpoint as evidence for a specific service.
- Treating Electron/Chromium child processes as zombies without lineage or churn evidence.
- Explaining an intermittent UI failure from RAM alone without temporal correlation.
- Declaring a repair from a setting change without reproducing the original failure.
- Blaming the target app for load created by the diagnostic process itself.

## Release gate

`PASS` requires: exact target identity, reproduced or bounded symptom, causal evidence, falsifier/negative check, repair read-back, and user-path verification. Otherwise report `FAIL`, `BLOCKED`, or `NOT_RUN`.
