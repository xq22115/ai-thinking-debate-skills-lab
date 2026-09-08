---
name: durable-agent-control-plane
description: Coordinate multi-agent work with durable goal/task identity, isolated writer ownership, claim-bound execution, receipts, resumable lifecycle, infrastructure-state classification, goal-drift detection, and fail-closed integration. Use when multi-agent work spans branches, interruptions, or externally visible changes.
---

# Durable Agent Control Plane

Version: `0.2.0-rc1`

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Objective

Turn multi-agent collaboration from conversational role-play into an auditable execution system that can distinguish task results from execution-infrastructure state **and preserve the user-authorized objective throughout execution**.

A perfectly logged run against the wrong objective is still a failed run.

## Core Invariants

1. Assign one durable task/run identity before execution.
2. Bind that identity to a compact Goal Contract snapshot: `ROOT_GOAL`, `HARD_CONSTRAINTS`, `ACCEPTANCE_TESTS`, `NON_GOALS`, target identity/environment, and material open specification uncertainty.
3. Pin moving refs/config inputs to immutable revisions when reproducibility matters.
4. Give each writing actor an isolated workspace/branch and explicit write-set ownership.
5. Record an ownership/claim before mutation.
6. Bind execution receipts to task, run, actor, claim, revision, **goal-contract revision**, and result.
7. Treat model text asserting independence, permission, objective fidelity, or completion as non-evidence.
8. Downstream actors execute only after required dependency receipts are valid and still goal-compatible.
9. Integrate only after receipt adjudication, fresh-base checks, write-set verification, and Goal Contract consistency checks.
10. Distinguish local integration, remote publication, final merge, deployment, and health.
11. Preserve branches/checkpoints/receipts so a fresh process can rehydrate without replaying completed unsafe actions.
12. Keep task-result state separate from infrastructure state.
13. Keep blocker state separate from `ROOT_GOAL`; method changes do not authorize goal changes.
14. Only a user-authorized goal update may change the desired terminal state.
15. Do not overwrite a terminal veto, failed hard constraint, or failed acceptance gate with a later optimistic model answer.
16. Acceptance tests are evidence instruments, not objectives to manipulate for score.

## Goal Contract Binding

Before consequential execution, capture only fields that materially constrain the terminal state:

- `ROOT_GOAL`
- `USER_STATED_REQUEST`
- `HARD_CONSTRAINTS`
- `ACCEPTANCE_TESTS`
- `PROXIES / METRICS` when present
- `NON_GOALS`
- `TARGET_IDENTITY / ENVIRONMENT`
- `OPEN_SPECIFICATION_UNCERTAINTY`
- `GOAL_CONTRACT_REVISION`

Consult `GOAL_OBJECTIVE_AUDIT.md` when the goal is ambiguous, mixed, changing, proxy-scored, or vulnerable to specification gaming.

Do not infer hidden personal motives. Normalize only task-relevant intent supported by the conversation/context.

## Goal-Change Classification

When new information arrives, classify it as one of:

- `METHOD_UPDATE` — same terminal goal, different route;
- `WORLD_STATE_UPDATE` — new evidence changes feasibility or uncertainty;
- `AUTHORIZED_GOAL_UPDATE` — user explicitly changes the desired terminal state, priority, or hard constraint;
- `UNAUTHORIZED_GOAL_DRIFT` — system/agent silently changes what success means.

Only `AUTHORIZED_GOAL_UPDATE` increments the authoritative goal meaning. Method/world-state changes may require a new plan but not a new root goal.

## Task Result States

Suggested task lifecycle:

`PLANNED → CLAIMED → RUNNING → PASS|VETO|FAIL|BLOCKED → FINALIZED → INTEGRATED_LOCAL → INTEGRATION_PUBLISHED → MERGED`

`BLOCKED` may resume after blocker removal and revalidation. A terminal `VETO` for a run must not be silently replaced.

Optional goal-related states:

- `SPECIFICATION_UNCERTAIN`
- `GOAL_DRIFT_DETECTED`
- `GOAL_UPDATE_PENDING_AUTHORITY`
- `ACCEPTANCE_PROXY_UNVALIDATED`

These are not infrastructure failures.

## Infrastructure States

Track execution infrastructure separately, for example:

- `READY`
- `AUTH_BLOCKED`
- `PERMISSION_BLOCKED`
- `BILLING_BLOCKED`
- `RUNNER_UNAVAILABLE`
- `DEPENDENCY_UNAVAILABLE`
- `QUEUED`
- `CANCELLED`
- `UNKNOWN_INFRASTRUCTURE_FAILURE`

A task must not be marked `FAIL` merely because its runner never started the relevant steps, and infrastructure failure must not become a replacement goal.

## Capability Truth

For any action requiring host/tool capability, preserve:

`VISIBLE → AUTHORIZED → VERIFIED`

A connector schema proves visibility. Authorization requires backing permission. Verification requires a real consumer call/read-back appropriate to the claim.

## Runtime Evidence

When independent-agent execution matters, prefer wrapper-observed evidence such as:

- distinct execution identities;
- process/session attestations;
- workspaces/branches;
- claim-bound receipts;
- input/output hashes;
- dependency and timing records where relevant;
- goal-contract revision bound to each consequential receipt.

Do not count role labels or model prose as runtime independence or goal fidelity.

## Multi-Agent Goal Coherence

All participating roles must share the same current:

- root goal;
- hard constraints;
- acceptance tests;
- non-goals;
- target identity;
- goal-contract revision.

Agents may disagree about facts, hypotheses, methods, risks, or tests. They do not gain authority to choose a different terminal outcome merely because they are independent roles.

A proposed objective change is returned as a proposal to the coordinator/user-authoritative layer rather than silently adopted.

## Proxy / Acceptance Integrity

When progress is measured by a proxy or test:

1. record what user outcome the proxy is intended to indicate;
2. check whether the proxy can improve while the outcome worsens;
3. keep tests/evaluators/audit logs outside ordinary optimization/write scope when runtime separation permits;
4. do not count test/evaluator manipulation as task progress;
5. include an outcome-oriented check when proxy gaming is materially plausible.

`PASSING_THE_PROXY != ACHIEVING_THE_GOAL`

## Recovery

A rehydrated run must reconstruct:

- current Goal Contract and revision;
- latest authorized goal update;
- pinned inputs;
- actor ownership;
- dependency state;
- completed receipts;
- pending actors/actions;
- task-result state;
- infrastructure/blocker state;
- integration/publication state;
- unsafe-to-repeat actions.

Before resuming a blocked run, revalidate the blocker, mutable prerequisites, and goal-contract freshness rather than assuming the old diagnosis or objective interpretation is still current.

## Integration Gate

Before integration:

1. adjudicate all required receipts;
2. verify no missing/VETO/blocking dependency remains;
3. verify write-set and artifact identity;
4. verify current base/revision freshness;
5. verify all integrated work maps to the current Goal Contract;
6. reject artifacts optimized for superseded/unauthorized goal states;
7. distinguish already-verified task output from newly changed infrastructure state;
8. verify acceptance evidence still represents the intended outcome rather than a gamed proxy;
9. preserve exact evidence for what was actually integrated/published.

## Completion Gate

Repository/control-plane implementation, deterministic fake-backend tests, local unit tests, configured role names, a high benchmark score, or a failed pre-step CI job are not proof that authentic multi-agent model execution or user-goal completion occurred.

Claim only the highest status directly evidenced, report infrastructure blockers independently from task correctness, and require the final artifact/state to satisfy the current Goal Contract rather than only its easiest measurable proxy.

## Evaluation

Primary objective-fidelity regression spec:

`skills/evals/goal-objective-audit-fixtures.json` — GO1–GO10.

Fixture presence is not target-model execution evidence. Clarification-value, proxy-gaming, goal-drift, independent judging, and host-live regression remain separate gates.