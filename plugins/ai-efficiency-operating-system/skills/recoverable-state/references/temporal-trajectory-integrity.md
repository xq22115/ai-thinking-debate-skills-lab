# Temporal & Long-Horizon Trajectory Integrity

Status: `EXPERIMENTAL REFERENCE / USE ON DEMAND`

Use this reference when locally valid actions can compose into a globally invalid long-horizon trajectory.

## Global state

Track goal revision, target identity/revision, global budgets, completed/irreversible actions and receipts, pending dependencies, delayed observations, stale assumptions, rollback target, remaining branches and current strategy.

## Delayed feedback

Record the action plus expected observation window and keep it `PENDING_OBSERVATION`. When feedback arrives, bind it to candidate earlier causes rather than automatically blaming the latest step.

## Temporal credit assignment

Classify late failures as `RECOVERABLE_DEVIATION`, `CRITICAL_DECISION_POINT`, `FIRST_IRRECOVERABLE_ERROR` or `DOWNSTREAM_SYMPTOM`.

## Asynchronous ordering

For each parallel branch record prerequisites, shared mutable state, write-set ownership, synchronization point, output freshness and cancellation condition. Parallel work that creates races, stale output or duplicate irreversible effects is a failure, not acceleration.

## Option value and sunk cost

Before irreversible commitment, ask what future branches disappear and whether a cheap probe preserves better options. Past cost does not justify a dominated branch.

## Terminal integrity

`ATTESTED != COMPLETED`. A hook/task/worker/receipt can only prove the layer it observes. Bind terminal claims to independent available planes and owning-system postconditions; malformed/stale/unknown-generation receipts are `UNKNOWN`.

## Recovery check

After interruption, a fresh executor must re-read current mutable state, compare it with the checkpoint, preserve completed irreversible receipts, invalidate stale plans and avoid unsafe replay.
