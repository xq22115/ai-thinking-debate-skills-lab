---
name: agent-observability-slos
description: Use when an AI agent is slow, flaky, expensive, hard to debug, or produces disputed outcomes and the cause may span model calls, tools, queues, runtime processes, UI automation, retries, client lifecycle, or external services.
---

# Agent Observability and SLOs

## Core principle

Instrument the **trajectory**, not just the final answer. A snapshot is a symptom; a correlated trace is evidence.

## Required signals

For each material run, preserve a stable run/task ID and correlate when available:

- model/provider/model-version, latency, token counts, retry/fallback;
- tool/server/tool-name, queue wait, execution time, result class;
- agent/subagent/span parentage and handoffs;
- UI/client-render/browser span identity and parentage linked to the stable run/task ID; report a correlation gap when unavailable;
- client/page lifecycle state when continuity matters: visible/hidden/frozen/discarded, renderer/background-throttling state, stream/subscription identity and reattachment event;
- process/runtime/session/profile identity;
- external effect and read-back result;
- error type, timeout/cancellation and recovery path.

Prompt/completion/tool content is **opt-in** telemetry. Redact or omit sensitive content while retaining operational metadata.

## SLO workflow

1. Define user-facing SLOs before tuning: success rate, p50/p95/p99 latency, cost/task, tool-error rate, recovery rate.
2. Trace one request end-to-end before blaming CPU, RAM, network, disk, model or UI.
3. Split latency into queue wait, model time, tool time, retries, serialization, client delivery and render time.
4. When output appears to stop after a tab/chat/app switch, separate execution-owner progress from client subscription/delivery/render state before classifying the run as paused or dead.
5. Use saturation/throughput metrics to distinguish load from causal failure.
6. Compare good and bad runs with the same identity dimensions.
7. Record the first span where behavior diverges; do not infer downstream causes from later symptoms.
8. Verify a repair by showing the targeted span/SLO changed without adjacent regression.

**REQUIRED SUB-SKILL:** use `agent-runtime-forensics` when causality or provenance is disputed, and `durable-agent-control-plane` / `recoverable-state` when execution must survive client interruption or reattachment.

## Red flags

- one instantaneous perf counter is called the root cause;
- HTTP reachability is confused with application success;
- “tool success” has no postcondition span/read-back;
- logs cannot distinguish Account 1 vs Account 2;
- traces omit queue wait, retry or fallback;
- the UI stops rendering and this is declared “the backend stopped” without execution-owner evidence;
- a run ID still exists and this is declared “the run is progressing” without fresh progress evidence;
- p95 improves while success rate or cost regresses.

## Output

Return SLOs, trace identity, execution owner, client lifecycle/subscription state when relevant, latency/error budget, bottleneck span, causal evidence, missing telemetry, and pre/post repair comparison.
