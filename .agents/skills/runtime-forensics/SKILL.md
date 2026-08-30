---
name: runtime-forensics
description: Use when a failure crosses model, tool, process, file, network, artifact or postcondition boundaries and causal replay/telemetry is needed to locate the first broken transition.
---

# Runtime Forensics

## Purpose
Build a causal execution trace from requested action to observed postcondition without confusing logs, tool replies or missing telemetry with truth.

## Activate when
Use for intermittent failures, split-brain state, ambiguous side effects, stuck agents, process/network issues, lost acknowledgements or runtime-only defects.

## Do not activate
Do not add heavy tracing to a deterministic local error already explained by direct evidence.

## Antigravity-native execution
Fingerprint workspace, process/session, tool/MCP revision, environment and artifact identities. Use the lightest available logs/process/file/network observations and preserve timestamps/correlation IDs when supported.

## Workflow
1. Define expected causal chain and postcondition.
2. Capture each observable transition: model decision -> tool invocation -> process/network/file effect -> read-back.
3. Identify the earliest divergence or dark segment.
4. Reproduce with one variable changed at a time.
5. Reconcile ambiguous effects before replay.
6. Save a compact forensic manifest for handoff/regression.

## Validation
An acknowledgement is not an effect and an effect is not the final postcondition. Telemetry absence is `UNKNOWN`; verify through an independent state route when possible.

## Boundaries
Do not collect unrelated sensitive data or weaken security solely for observability. Scope traces to the user's authorized target.