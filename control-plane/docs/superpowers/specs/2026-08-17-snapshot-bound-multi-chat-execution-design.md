# Snapshot-Bound Multi-Chat Execution Design

## Scope

Strengthen the existing GitHub agent control plane against long-running multi-chat races without weakening the ten-代理 fail-closed gate.

## Chosen design

Use a one-shot actor ownership claim plus immutable plan snapshots. Do not use time-based lease expiry in the first implementation. A failed/stale owner causes the run to BLOCK; recovery starts a new `run_id` rather than silently transferring ownership inside the same run.

## Why this design

A time lease adds clock, renewal and split-brain failure modes. GitHub Actions concurrency and merge queues remain useful at CI/merge time, but they do not prove actor ownership before mutation and cannot replace repository-level coordination.

## Ownership claim

Each actor branch owns one create-only claim at:

`ai-system/control-plane/runs/<issue>/<run_id>/claims/<actor_id>.json`

The claim binds issue, run, actor, branch, executor ID, execution ID and pinned base SHA. Overwrite/force-push takeover is forbidden. If the claim already exists for another execution, the run is VETO/BLOCKED and a fresh run is required.

## Snapshot collection

A01 resolves each assigned branch name to an exact commit SHA before reading the plan. The collector reads the plan from that resolved SHA, not from the moving branch name, and records a SHA-256 digest of the plan plus the claim identity.

The collection output is ephemeral evidence. It is not a shared mutable ledger.

## Snapshot-bound execution

Before fan-in, verification must prove:

1. the approved plan commit is an ancestor of the final actor head;
2. the actor branch currently resolves to the final head being verified;
3. the plan content at final head is byte-identical to the approved snapshot;
4. the ownership claim at final head matches the approved claim;
5. changed task paths after the plan commit are a subset of the approved `write_set`;
6. only the actor's exact namespaced receipt path is allowed as control-plane evidence after the plan snapshot.

Any failure is VETO. A success receipt cannot override it.

## Cross-run isolation

Change the integration branch template from a per-issue shared branch to:

`task/<issue>/<run_id>/integration`

This prevents two valid runs for one issue from sharing a mutable fan-in branch.

## Base drift and replay

At integration time, the pinned base SHA must still match the trusted current base used for final verification. If another run or human merge advances the base, the old run cannot reuse prior PASS evidence; it must re-pin/replan under a new run ID.

## State machine

Add explicit states/gates for CLAIMED, PLANS_SNAPSHOTTED, PREFLIGHT_PASS, EXECUTION_VERIFIED and BASE_FRESH. Forbidden shortcuts include branch-name-only approval, plan-hash mismatch acceptance, claim takeover, stale-base merge and force-push ownership transfer.

## Testing

Use TDD negative tests for duplicate/foreign claims, moving branch refs, plan mutation after preflight, non-descendant final heads, undeclared diff paths, stale base SHA, shared integration branch templates and replay of evidence from an older snapshot.

## Completion semantics

Repository/static PASS remains separate from the ten truly independent runtime 代理 gate. These controls make execution evidence harder to forge or accidentally stale; they do not create independent agents where the runtime does not provide them.

## Addendum: claim-bound receipt evidence

A correct receipt path is not sufficient evidence. PASS/VETO receipts use schema v2 and bind `claim_id`, approved `plan_head_sha`, actor branch, executor ID, execution ID, and `head_sha` defined as the exact pre-receipt work head.

The receipt is committed only after task work is frozen. Snapshot verification proves the chain `plan_head_sha -> work_head(receipt.head_sha) -> final receipt commit`, verifies the receipt identity against the immutable claim snapshot, checks task scope only through the work head, and requires the post-work diff to contain exactly the actor's own receipt path. Historical schema-v1 `NOT_RUN` receipts remain archival blocker evidence; schema-v1 PASS/VETO cannot adjudicate to runtime PASS.
