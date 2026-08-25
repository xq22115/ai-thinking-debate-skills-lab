# 05 — Durable workflows

## Verdict
Adopt the durable-agent pattern, not a Vercel dependency as a hard requirement. Use AI SDK 7 WorkflowAgent as the 2026 reference architecture: explicit runtime context, resumable steps, timeouts, approvals, and telemetry; implement the same invariants in the existing local control plane.

## Evidence
- AI SDK 7 (June 25, 2026) added WorkflowAgent, tool approvals, total/per-step/per-chunk/per-tool timeouts, typed runtime context, harness adapters, and telemetry.
- Durable execution survives process restarts and delayed approvals; this is the missing property in chat-only agent loops that depend on a single conversation turn.

## Gap in current stack
Continuous thinking and GitHub continuity exist, but ordinary-chat local execution does not have one canonical resumable run receipt with step state, approval state, timeout reason, and next action.

## Recommendation
Create a provider-neutral `durable-run-contract` in Braintrust and map chatgpt-mcp-codex task/plan state to it. Keep implementation local/free; do not require Vercel hosted services.

## Acceptance
Interrupt a multi-step fake run after one completed tool step, restart the worker, resume without replaying the completed side effect, and verify the final receipt identifies the exact resumed revision and approval state.