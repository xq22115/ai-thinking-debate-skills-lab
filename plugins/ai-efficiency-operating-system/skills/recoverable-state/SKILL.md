---
name: recoverable-state
description: Use when long-running or effectful work must resume after interruption, compaction, restart, handoff, delayed feedback, or partial external mutation without replaying unsafe side effects or trusting a stale checkpoint.
---

# Recoverable State

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Packaging provenance

This plugin-local skill is the **packaged adapter/snapshot** of the repository-level semantic owner at `skills/skills/recoverable-state/SKILL.md`. It exists here so the plugin can register and route the capability on hosts that load only plugin-local skills; it is **not** a second independent semantic owner and is not counted among the 12 production specialists.

Changes to recovery semantics must be reconciled with the repository-level owner before promotion. Plugin-specific packaging may add registration/host-boundary details, but it must not silently fork the checkpoint, freshness, unsafe-replay, delayed-feedback, or trajectory-integrity contract.


## Core principle

A transcript is not a state machine, and a checkpoint is not present-time truth. Resume from durable state only after revalidating the current goal, target identity/revision and effect receipts.

## Invariants

- `CHECKPOINT_EXISTS != CHECKPOINT_IS_FRESH`
- `ATTESTED != COMPLETED`
- `ACKNOWLEDGED != VERIFIED`
- `UNKNOWN_EFFECT != SAFE_TO_REPLAY`
- `LOCAL_STEP_SUCCESS != TRAJECTORY_SUCCESS`
- `CURRENT_STATE != CHECKPOINT_STATE`
- `DELAYED_FEEDBACK != NO_FEEDBACK`

## Durable checkpoint

Persist only what a fresh executor needs to continue safely: run/task ID and Goal Contract revision; objective/acceptance/unresolved gates; target identity/environment/revision; state-machine state and last verified checkpoint; completed external actions with non-secret receipts; irreversible commitments and unsafe-to-repeat actions; pending actions/dependencies/delayed observations; evidence pointers/freshness/provenance; global budgets; rollback target; viable branches; and assumptions requiring revalidation.

## Resume workflow

1. Create a checkpoint before high-impact or long-delay execution.
2. After each irreversible/external action, write a bounded receipt with action, target, revision, time, claimed state and postcondition evidence pointer.
3. Keep `PENDING_OBSERVATION` distinct from PASS.
4. On resume/restart/compaction, re-read mutable external state and compare current goal/target/revision with the checkpoint.
5. Preserve completed irreversible receipts, but invalidate stale planned actions whose prerequisites changed.
6. Replay only operations proven idempotent or proven not to have occurred.
7. If effect confirmation was lost, set `UNKNOWN` and read back the owning postcondition before retrying.
8. Reconcile conflicting state/evidence before continuing.
9. Re-evaluate trajectory/global constraints and choose `KEEP_STRATEGY`, `LOCAL_REPAIR`, `REPLAN_BRANCH`, `ROLLBACK` or `ABANDON_BRANCH`.

## Terminal evidence

Where available, keep `REQUESTED → SENT → DELIVERED → ACKNOWLEDGED → INCORPORATED → VERIFIED` separate. Bind material terminal claims to the strongest available independent planes: worker/thread health, completion event or terminal state, owning-system read-back, and persisted receipt/checkpoint. Missing planes remain explicit evidence debt.

Receipts fail closed. Unknown schema generations, malformed types, stale target generations, ambiguous identity or secret-bearing payloads are invalid/`UNKNOWN`, never PASS.

## Checkpoint freshness

Use `FRESH`, `STALE_BUT_COMPATIBLE`, `STALE_REPLAN_REQUIRED`, `TARGET_MISMATCH`, `GOAL_REVISION_MISMATCH`.

## Recovery test

A fresh executor with only the checkpoint plus current target read-back must identify what is done, what remains, what changed, what must not be repeated, pending feedback, missing evidence, and whether to keep/repair/replan/rollback/abandon.

**REQUIRED SUB-SKILL:** use `memory-policy` for durable-authority/provenance, `evidence-watchdog` for terminal claims, `agent-containment-and-rollback` for blast-radius/reversal, and `runtime-release-parity` when source/artifact/live-runtime identity may have drifted.

**REFERENCE:** read `references/temporal-trajectory-integrity.md` when delayed feedback, asynchronous ordering, option value, stale checkpoints or long trajectory composition are material.
