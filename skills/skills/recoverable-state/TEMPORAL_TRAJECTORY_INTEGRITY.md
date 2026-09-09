# Temporal & Long-Horizon Trajectory Integrity

Status: `EXPERIMENTAL REFERENCE / USE ON DEMAND`

Purpose: preserve goal, constraints, evidence, and strategic coherence across long-running tasks where feedback is delayed, earlier actions constrain later options, state can become stale, and locally reasonable steps may compose into a globally poor trajectory.

## Core invariants

- `LOCAL_STEP_SUCCESS != TRAJECTORY_SUCCESS`
- `CURRENT_STATE != CHECKPOINT_STATE`
- `EARLY_PROGRESS != FUTURE_FEASIBILITY`
- `DELAYED_FEEDBACK != NO_FEEDBACK`
- `LATE_FAILURE MAY HAVE EARLY_CAUSE`
- `RECOVERABLE_NOW != RECOVERABLE_LATER`
- `OPTION_VALUE != IMMEDIATE_REWARD`
- `PARALLELISM != FREE_SPEEDUP`
- `CHECKPOINT_EXISTS != CHECKPOINT_IS_FRESH`
- `LONGER_TRAJECTORY != MORE_RELIABLE_JUDGMENT`

## 1. State as a trajectory, not a transcript

For long-horizon work maintain a compact trajectory ledger rather than relying on raw conversation history:

- current Goal Contract revision;
- current world/target state;
- global constraints and remaining budgets;
- completed actions and receipts;
- irreversible commitments;
- open branches/options;
- pending dependencies;
- delayed observations not yet available;
- stale assumptions awaiting revalidation;
- current strategy and why it still dominates alternatives;
- earliest known error/deflection point when recovery is needed.

The ledger should be small enough to survive context truncation and precise enough for a fresh agent to resume without inventing history.

## 2. Global constraints over local steps

A sequence of individually valid actions can violate a global constraint.

Track global quantities when material:

- time/deadline budget;
- money/compute/tool-call budget;
- quota/rate limits;
- write-set/branch ownership;
- dependency ordering;
- irreversible-action count;
- user-friction/confirmation budget;
- compatibility constraints across later stages.

Before a locally attractive step, ask whether it reduces future feasibility.

`LOCAL_FEASIBILITY does not imply GLOBAL_FEASIBILITY`.

## 3. Delayed feedback

When an action's true consequence appears later:

1. record the action and expected observation window;
2. do not interpret missing immediate feedback as success;
3. distinguish `PENDING_OBSERVATION` from `PASS`;
4. when feedback arrives, link it to candidate earlier causes rather than only the latest step;
5. update strategy and confidence using the delayed evidence delta.

If multiple earlier actions could explain the result, use causal/abductive analysis rather than narrative recency.

## 4. Temporal credit assignment

When a late failure occurs, identify the earliest step after which success became materially less likely or impossible.

Classify candidate steps:

- `RECOVERABLE_DEVIATION` — later correction remained practical;
- `CRITICAL_DECISION_POINT` — strongly changed future options/risk;
- `FIRST_IRRECOVERABLE_ERROR` — after this step, success under the current branch was no longer realistically achievable;
- `DOWNSTREAM_SYMPTOM` — visible failure but not the root temporal cause.

Do not patch only the last visible symptom if the trajectory was doomed earlier.

## 5. Option value and commitment timing

A reversible action can be valuable because it preserves future choices, even if its immediate reward is lower.

Before committing:

- what future options disappear?;
- what information is expected soon?;
- can a probe/pilot preserve flexibility?;
- is the apparent speed gain worth lost rollback/branching options?;
- does delaying commitment improve expected decision quality more than it costs?

`IMMEDIATE_PROGRESS != MAXIMUM_OPTION_VALUE`.

## 6. Parallelism / asynchronous planning

Parallel execution is useful only when dependencies and resource contention are explicit.

For each parallel branch track:

- prerequisites;
- shared mutable state;
- write-set ownership;
- synchronization point;
- output freshness;
- cancellation condition;
- whether completion order changes the valid next action.

Over-parallelization can increase conflicts, stale work, duplicated cost, or irreversible divergence.

Do not parallelize dependent work merely to maximize visible activity.

## 7. Checkpoint freshness / revalidation

A checkpoint is evidence about the past state, not a guarantee about the present state.

On resume:

1. re-read current Goal Contract revision;
2. revalidate mutable external assumptions;
3. compare checkpoint target/version/identity with current target;
4. invalidate planned actions whose prerequisites changed;
5. preserve completed irreversible receipts;
6. do not replay unsafe actions merely because the checkpoint says they were planned.

Possible state labels:

- `FRESH`
- `STALE_BUT_COMPATIBLE`
- `STALE_REPLAN_REQUIRED`
- `TARGET_MISMATCH`
- `GOAL_REVISION_MISMATCH`

## 8. Strategy revalidation

A plan should not persist merely because it was once optimal.

Re-evaluate strategy when:

- new delayed evidence arrives;
- a dependency changes;
- cost/time budget crosses a threshold;
- distribution shift is detected;
- an option becomes unavailable;
- a red-team finding changes failure probability;
- the Goal Contract changes;
- repeated execution produces no material progress.

Classify:

- `KEEP_STRATEGY`
- `LOCAL_REPAIR`
- `REPLAN_BRANCH`
- `ROLLBACK`
- `ABANDON_BRANCH`

Do not restart from zero when only a local repair is needed, and do not preserve a doomed branch to avoid admitting sunk cost.

## 9. Sunk-cost / path-dependence audit

Past cost is evidence about what happened, not a reason to continue a bad path.

Ask:

- if choosing fresh from the current state, would this branch still be preferred?;
- is continuation justified by future value or only past investment?;
- has path dependence removed better alternatives?;
- can rollback reopen a higher-value branch?

`PAST_COST != FUTURE_BENEFIT`.

## 10. Trajectory-level verification

Do not judge long-horizon success only from the final visible output.

When consequential, verify:

- Goal Contract remained stable or authorized changes are traceable;
- global constraints were respected across the full trajectory;
- no hidden irreversible error was masked by later prose;
- final state follows from receipts/observations rather than a claimed narrative;
- delayed feedback has been incorporated where required;
- the chosen path was not accepted solely because later steps looked polished.

Use step-level checks for owned invariants, but add trajectory-level audit when failures can emerge only from composition over time.

## 11. Long-horizon judge warning

Evaluator reliability can degrade as trajectories lengthen.

Mitigations:

- evaluate checkpoints/chunks plus global summary;
- preserve deterministic invariants separately;
- use causal attribution for late failures;
- compare full trajectory against a minimally perturbed hard-negative trajectory when available;
- avoid asking one judge to infer all latent state from an extremely long raw transcript;
- use fresh compact trajectory state rather than noisy complete history when possible.

## 12. Output contract

When temporal integrity is material, report only decision-relevant fields:

- current trajectory state;
- global constraints/budgets;
- pending delayed observations;
- irreversible commitments / remaining options;
- stale assumptions/checkpoints;
- earliest suspected failure point when debugging;
- keep/repair/replan/rollback recommendation;
- next synchronization or revalidation point;
- whether trajectory-level verification is complete.

## Research signal

2025–2026 long-horizon agent benchmarks and planning/evaluation research report persistent problems with global constrained planning, delayed/sparse feedback, compounded early errors, context/state management, asynchronous ordering, and trajectory-level evaluation. Treat this reference as a procedural scaffold, not proof that any model can reliably solve long-horizon tasks.