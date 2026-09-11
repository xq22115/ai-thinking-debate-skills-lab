---
name: openclaw-lobster-workflows
description: Use when OpenClaw needs a deterministic multi-step tool pipeline, resumable approval gate, replayable workflow, or fewer model round trips.
---

# OpenClaw Lobster Workflows

Use Lobster for the deterministic part of a task after the uncertain reasoning has been resolved.

Do not confuse the three coordination planes:

- **Sub-agents / Swarm** — parallelize uncertain research, competing hypotheses, implementation, falsification, and review.
- **Lobster** — execute a known multi-step pipeline with typed outputs, bounded runtime, approval checkpoints, and resume tokens.
- **Evidence Gate** — verify the real postcondition after either path finishes.

## When Lobster is the stronger route

Use it when the steps are already known and repeated model-by-model orchestration would add latency or inconsistency, especially for:

- collect → transform → validate → apply;
- recurring triage or maintenance workflows;
- state-changing flows that must pause before send/post/delete/apply;
- workflows that must resume without rerunning earlier successful steps;
- replayable procedures where the pipeline itself should be reviewable data.

Do not force Lobster onto open-ended investigation. Resolve uncertainty first with the orchestrator/research/falsification roles, then compile the stable action path into a Lobster workflow.

## Workflow contract

Prefer a checked-in `.lobster`, YAML, or JSON workflow when the procedure is reusable. Keep each step narrow and machine-readable.

For side effects, require an explicit approval step before the irreversible action. Treat `needs_approval` as paused, not failed and not complete. Resume with the returned token/approval id; do not rerun already completed steps merely to recreate state.

Enforce finite `timeoutMs` and output caps. If one pipeline becomes too large to inspect or retry safely, split it into smaller workflows with explicit artifacts between them.

## Embedded-runner limitation

The bundled Lobster tool runs in-process inside the Gateway. Do **not** assume nested `openclaw.invoke` automatically inherits Gateway URL/auth context. In particular, do not build an embedded workflow around nested `openclaw.invoke --tool llm-task` and call it reliable.

When an LLM decision is needed:

- use a direct `llm-task` outside embedded Lobster; or
- make the LLM/sub-agent produce a structured artifact first, then let Lobster consume that artifact deterministically; or
- use standalone Lobster only when its OpenClaw gateway/auth context is explicitly configured and verified.

## Sandboxing / capability mismatch

The bundled Lobster tool is unavailable in sandboxed tool contexts. If the effective runtime hides it, record the capability mismatch and fall back to the equivalent bounded ordinary tool sequence. Do not weaken the goal or falsely claim that Lobster ran.

## Verification

A Lobster envelope with `ok` means the workflow runtime completed; it does not automatically prove the user's end state.

After the pipeline:

1. use `openclaw-evidence-gate`;
2. read back the owning state/artifact/delivery result;
3. bind the evidence to the current goal version and target;
4. only then declare the acceptance condition verified.

If the workflow becomes stable after repeated verified use, hand it to `openclaw-learning-loop` as a reusable procedure with a positive case, counterexample/protection case, and rollback path.
