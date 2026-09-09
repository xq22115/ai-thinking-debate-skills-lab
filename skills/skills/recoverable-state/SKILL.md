---
name: recoverable-state
description: Externalize durable task and trajectory state so long-running work can resume safely after interruption, context loss, sandbox loss, agent handoff, delayed feedback, or strategic drift. Use for multi-step, long-horizon, stateful, asynchronous, or irreversible workflows.
---

# Recoverable State

Version: `0.2.0-rc1`

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Objective

Make long-running work both recoverable **and temporally coherent**: a fresh agent should be able to resume from durable state, revalidate what changed, preserve the current Goal Contract, avoid replaying unsafe actions, and detect when locally successful steps have produced a globally invalid trajectory.

A transcript is not a state machine, and a checkpoint is not present-time truth.

## Core invariants

- `CHECKPOINT_EXISTS != CHECKPOINT_IS_FRESH`
- `LOCAL_STEP_SUCCESS != TRAJECTORY_SUCCESS`
- `CURRENT_STATE != CHECKPOINT_STATE`
- `DELAYED_FEEDBACK != NO_FEEDBACK`
- `LATE_FAILURE MAY HAVE EARLY_CAUSE`
- `OPTION_VALUE != IMMEDIATE_REWARD`
- `PAST_COST != FUTURE_BENEFIT`
- `PARALLELISM != FREE_SPEEDUP`
- `RECOVERABLE_NOW != RECOVERABLE_LATER`

## Required Checkpoint

Persist at minimum when material:

- task/run ID;
- current Goal Contract revision;
- objective and acceptance criteria;
- target identity/environment/version;
- current state-machine state;
- last verified checkpoint;
- completed actions with receipts;
- irreversible commitments;
- pending actions/dependencies;
- pending delayed observations;
- evidence references;
- unresolved risks/unknowns;
- global budgets/constraints still in force;
- rollback target;
- remaining viable branches/options;
- actions unsafe to repeat;
- assumptions requiring revalidation on resume.

## Workflow

1. Create a checkpoint before high-impact or long-delay execution.
2. Write receipts after every irreversible or externally visible action.
3. Separate durable state from transient model conversation context.
4. Mark delayed outcomes as `PENDING_OBSERVATION`, not PASS.
5. On resume, rehydrate the checkpoint **and re-read mutable external state**.
6. Compare current Goal Contract/target/version/dependencies against checkpoint values.
7. Invalidate stale planned actions whose prerequisites changed.
8. Re-run only idempotent or explicitly safe operations.
9. If state/evidence conflict, reconcile before continuing.
10. Periodically audit trajectory-level global constraints and strategy coherence.
11. When late failure appears, search for the earliest material/irrecoverable error rather than patching only the last symptom.
12. Replan or rollback when future value no longer justifies the current branch.

## Checkpoint Freshness States

Use when useful:

- `FRESH`
- `STALE_BUT_COMPATIBLE`
- `STALE_REPLAN_REQUIRED`
- `TARGET_MISMATCH`
- `GOAL_REVISION_MISMATCH`

A stale checkpoint may remain useful as historical evidence while being invalid as an execution plan.

## Global Constraint Ledger

Long-horizon tasks can fail despite every step looking locally valid.

Track global constraints such as:

- time/deadline;
- money/compute/tool budget;
- quota/rate limits;
- dependency ordering;
- write-set ownership;
- compatibility across future stages;
- irreversible commitment count;
- remaining rollback/branching options.

Before a locally attractive step, ask whether it consumes resources or options needed by later mandatory steps.

## Delayed Feedback

For actions whose effect is not immediately observable:

1. record action time/receipt and expected feedback window;
2. keep status `PENDING_OBSERVATION`;
3. do not equate absence of immediate error with success;
4. when feedback arrives, bind it to candidate earlier actions and hypotheses;
5. update state/strategy using the evidence delta;
6. if attribution is ambiguous, use causal/abductive reasoning rather than recency.

## Temporal Credit Assignment

When a trajectory fails late, classify candidate earlier events:

- `RECOVERABLE_DEVIATION`
- `CRITICAL_DECISION_POINT`
- `FIRST_IRRECOVERABLE_ERROR`
- `DOWNSTREAM_SYMPTOM`

A good recovery identifies the earliest point that materially reduced or destroyed future feasibility.

## Option Value / Commitment Timing

Before irreversible commitment, preserve option value when a cheap probe, pilot, wait-for-feedback, or reversible branch can materially improve the decision.

Ask:

- which future branches disappear after this step?;
- what decisive evidence is expected soon?;
- can rollback remain available?;
- is immediate progress worth the loss of future flexibility?

Do not choose a step solely because it maximizes visible short-term progress.

## Asynchronous / Parallel Execution

Parallelism is allowed only with explicit dependency and mutable-state control.

Track:

- prerequisites;
- shared mutable state;
- write-set ownership;
- synchronization points;
- branch output freshness;
- cancellation conditions;
- whether completion order changes the valid next action.

Serialize or isolate dependent mutations. Over-parallelization that creates races, stale work, duplicated irreversible actions, or conflicting outputs is a failure, not acceleration.

## Sunk-Cost / Path-Dependence Audit

On material new evidence, ask:

- if choosing fresh from the current state, would this branch still be preferred?;
- are we continuing because of future value or because of past cost?;
- can rollback reopen a better branch?;
- has path dependence silently removed required future options?

Past investment does not authorize continued investment in a dominated path.

## Strategy Revalidation

Revalidate strategy when:

- delayed feedback arrives;
- dependencies or target state change;
- cost/time budget crosses a threshold;
- distribution shift is detected;
- an option disappears;
- a red-team finding changes risk;
- Goal Contract changes;
- repeated steps add no material progress.

Choose one:

- `KEEP_STRATEGY`
- `LOCAL_REPAIR`
- `REPLAN_BRANCH`
- `ROLLBACK`
- `ABANDON_BRANCH`

Do not restart everything for a local defect, and do not preserve a doomed branch to avoid acknowledging sunk cost.

## Trajectory-Level Verification

For consequential long-horizon tasks, completion requires more than a final-output check.

Verify where applicable:

- Goal Contract remained current or authorized updates are traceable;
- global constraints stayed satisfied across the full path;
- no early irreversible violation was masked by later successful-looking steps;
- delayed feedback required for acceptance has arrived and been incorporated;
- receipts support the claimed state transitions;
- current target state still matches checkpoint identity;
- evaluator confidence did not rely solely on an extremely long raw transcript.

Use deterministic step-level checks for owned invariants and a trajectory-level audit for composition over time.

## Recovery Test

A fresh agent with only the checkpoint and current target read-back must be able to identify:

- what is done;
- what remains;
- what changed since the checkpoint;
- what must not be repeated;
- what feedback is still pending;
- what options remain;
- what evidence is still required;
- whether to keep, repair, replan, rollback, or abandon the branch.

## Interaction with Other Skills

Use:

- `durable-agent-control-plane` for goal-contract-bound multi-actor receipts and ownership;
- `evidence-gap-research` when delayed observations change belief/decision state;
- `semantic-argument-microscope` causal/abductive reference for ambiguous temporal attribution;
- `completion-gate` before terminal status.

For long-horizon state, delayed feedback, option value, asynchronous execution, stale checkpoints, sunk-cost/path dependence, and trajectory-level verification, consult `TEMPORAL_TRAJECTORY_INTEGRITY.md`.

## Evaluation

Primary regression spec:

`skills/evals/temporal-trajectory-integrity-fixtures.json` — TT1–TT10.

Fixture presence is not target-model or host-live execution evidence. Delayed-feedback execution, trajectory attribution, asynchronous planning, checkpoint-staleness recovery, independent judging, and host-live regression remain separate gates.

## Completion Gate

A long-horizon workflow is not recoverable merely because its transcript/checkpoint exists. Do not claim recovery or completion until the checkpoint has been revalidated against the current target state and the full trajectory still satisfies the Goal Contract and global constraints.