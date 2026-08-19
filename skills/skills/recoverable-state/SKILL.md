---
name: recoverable-state
description: Externalize durable task state so long-running work can resume safely after interruption, context loss, sandbox loss, or agent handoff. Use for multi-step or irreversible workflows.
---

# Recoverable State

Version: `0.1.0-rc1`

## Required Checkpoint

Persist at minimum:
- task ID;
- objective and acceptance criteria;
- current state-machine state;
- last verified checkpoint;
- completed actions with receipts;
- pending actions;
- evidence references;
- unresolved risks/unknowns;
- rollback target;
- actions unsafe to repeat.

## Workflow

1. Create a checkpoint before high-impact execution.
2. Write receipts after every irreversible or externally visible action.
3. Separate durable state from transient model conversation context.
4. On resume, rehydrate state and verify the external world has not changed materially.
5. Re-run only idempotent or explicitly safe operations.
6. If state/evidence conflict, stop and reconcile before continuing.

## Recovery Test

A fresh agent with only the checkpoint must be able to identify what is done, what remains, what must not be repeated, and what evidence is still required.

## Completion Gate

A long-horizon workflow is not recoverable merely because its transcript exists.