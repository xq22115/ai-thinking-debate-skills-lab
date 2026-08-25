# 09 — Observability and evals

## Verdict
Make local structured receipts/OpenTelemetry-compatible events mandatory; keep Langfuse optional as a visualization/analysis backend, not a correctness dependency.

## Evidence
- AI SDK 7 added global telemetry integrations, OpenTelemetry support, lifecycle callbacks and step performance statistics.
- Langfuse's 2026 roadmap emphasizes long-running agent observability and first-class experiments/evals.
- The existing repositories already understand that config, command exit, PR creation, and unrelated CI are weaker than runtime/user-path evidence.

## Gap in current stack
Receipts exist in different forms across repositories, but there is no shared event vocabulary for model step, tool start/end, approval, retry/pivot, artifact, runtime read-back, and acceptance-criterion transition.

## Recommendation
Create an `agent-observability` schema emitting local JSONL first and an OTEL exporter interface second. Add correlation IDs linking chat request → run → tool → artifact → criterion evidence. Do not require a hosted observability service.

## Acceptance
One end-to-end fake run must be reconstructable from events without reading chat history, including why a route changed after failure and which evidence satisfied each hard criterion.