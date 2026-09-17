---
name: model-routing-budget-control
description: Use when an agent can choose among multiple models, reasoning levels, providers, or fallbacks and quality, latency, token use, cost, rate limits, or availability differ materially by subtask.
---

# Model Routing and Budget Control

## Core principle

Route by measured task requirements, not model prestige or price alone. A fallback is a behavior change and must be observable.

## Routing contract

For each task class define:

- minimum verified quality floor;
- latency/SLO target;
- context/tool requirements;
- acceptable model/provider set;
- reasoning/effort range when configurable;
- budget ceiling and retry budget;
- fallback behavior and forbidden downgrades.

## Workflow

1. Classify the subtask by consequence and capability need: deterministic transform, retrieval, coding, ambiguous reasoning, review/judging, multimodal, long-horizon orchestration, etc.
2. Use eval results on representative slices to establish the cheapest/fastest route meeting the quality floor.
3. Keep model identity, version, effort, fallback and token/cost telemetry in the run trace.
4. Prefer small/fast models only where measured quality remains above the route's threshold.
5. For acceptance-critical reasoning or evaluation, block silent fallback below the verified floor.
6. Bound retry cascades; repeated failure should change route or surface a blocker rather than burn budget indefinitely.
7. Re-evaluate routes when model versions, pricing, context limits, tool support or observed quality change.
8. Optimize total task cost, including retries, failed tool calls and review/remediation—not only first-call price.

## Hard rules

- `CHEAPER CALL != CHEAPER TASK`.
- `STRONGER MODEL != BETTER ROUTE FOR EVERY SUBTASK`.
- Fallback must never be invisible in acceptance evidence.
- A routing rule without slice-level eval evidence is a hypothesis.
- Provider/model swaps can change tool semantics, context behavior and failure modes.

**REQUIRED SUB-SKILL:** use `agent-evaluation-operations` to qualify routes and `agent-observability-slos` to measure production behavior.

## Output

Return task classes, routing matrix, quality floors, budget/retry policy, fallback rules, measured cost/latency/quality evidence and revalidation triggers.
