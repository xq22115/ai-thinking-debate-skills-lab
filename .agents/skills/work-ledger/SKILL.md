---
name: work-ledger
description: Use when a task needs durable cross-session state, resume, concurrency, scheduling/handoff, ambiguous side-effect reconciliation or delivery receipts and real durable primitives are available.
---

# Work Ledger

## Purpose
Externalize enough task/effect state to resume safely without compressing unfinished work into a false completion claim.

## Activate when
Use for long-running work, interrupted execution, multi-writer coordination, external effects, handoffs or tasks whose state must survive context loss.

## Do not activate
Do not pretend a markdown skill creates a scheduler, daemon, database or durable worker when the runtime exposes none.

## Antigravity-native execution
Use authorized project files/Git/state stores for goal revision, acceptance contract, action/effect ledger, evidence, checkpoints, ownership/lease state, handoff hashes and delivery/read-back receipts. Keep semantic operation IDs stable across physical turns.

## Workflow
1. Create durable task identity and goal revision.
2. Record intent before consequential effect when crash recovery matters.
3. Record effect/receipt after execution.
4. Treat ambiguous effect as `UNKNOWN`; read back before replay.
5. Fence concurrent writers and preserve handoff ownership.
6. Resume from unresolved obligations, not summary prose.

## Validation
Sender success != receiver acknowledgement. Replayed semantic actions should reconcile prior receipts; divergent irreversible history requires an explicit fork.

## Boundaries
Durability must match actual storage guarantees. Never widen authority during resume or rollback.