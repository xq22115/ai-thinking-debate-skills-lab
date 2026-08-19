---
name: durable-agent-control-plane
description: Coordinate multi-agent work with durable task identity, isolated writer ownership, claim-bound execution, receipts, resumable lifecycle, infrastructure-state classification, and fail-closed integration. Use when multi-agent work spans branches, interruptions, or externally visible changes.
---

# Durable Agent Control Plane

Version: `0.1.1-rc1`

## Objective

Turn multi-agent collaboration from conversational role-play into an auditable execution system that can distinguish task results from execution-infrastructure state.

## Core Invariants

1. Assign one durable task/run identity before execution.
2. Pin moving refs/config inputs to immutable revisions when reproducibility matters.
3. Give each writing actor an isolated workspace/branch and explicit write-set ownership.
4. Record an ownership/claim before mutation.
5. Bind execution receipts to task, run, actor, claim, revision, and result.
6. Treat model text asserting independence, permission, or completion as non-evidence.
7. Downstream actors execute only after required dependency receipts are valid.
8. Integrate only after receipt adjudication, fresh-base checks, and write-set verification.
9. Distinguish local integration, remote publication, final merge, deployment, and health.
10. Preserve branches/checkpoints/receipts so a fresh process can rehydrate without replaying completed unsafe actions.
11. Keep task-result state separate from infrastructure state.
12. Do not overwrite a terminal veto or failed safety gate with a later optimistic model answer.

## Task Result States

Suggested task lifecycle:

`PLANNED → CLAIMED → RUNNING → PASS|VETO|FAIL|BLOCKED → FINALIZED → INTEGRATED_LOCAL → INTEGRATION_PUBLISHED → MERGED`

`BLOCKED` may resume after blocker removal and revalidation. A terminal `VETO` for a run must not be silently replaced.

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

A task must not be marked `FAIL` merely because its runner never started the relevant steps.

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
- dependency and timing records where relevant.

Do not count role labels or model prose as runtime independence.

## Recovery

A rehydrated run must reconstruct:
- pinned inputs;
- actor ownership;
- dependency state;
- completed receipts;
- pending actors/actions;
- task-result state;
- infrastructure/blocker state;
- integration/publication state;
- unsafe-to-repeat actions.

Before resuming a blocked run, revalidate the blocker and all mutable prerequisites rather than assuming the old diagnosis is still current.

## Integration Gate

Before integration:

1. adjudicate all required receipts;
2. verify no missing/VETO/blocking dependency remains;
3. verify write-set and artifact identity;
4. verify current base/revision freshness;
5. distinguish already-verified task output from newly changed infrastructure state;
6. preserve exact evidence for what was actually integrated/published.

## Completion Gate

Repository/control-plane implementation, deterministic fake-backend tests, local unit tests, configured role names, or a failed pre-step CI job are not proof that authentic multi-agent model execution occurred.

Claim only the highest status directly evidenced, and report infrastructure blockers independently from task correctness.
