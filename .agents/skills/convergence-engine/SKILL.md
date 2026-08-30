---
name: convergence-engine
description: Use when repeated repair, review, iteration, skill evolution or retry loops risk stagnation, cosmetic churn, scope creep or regression.
---

# Convergence Engine

## Purpose
Make every iteration earn its cost through a measurable causal delta.

## Activate when
Use after repeated failures, reviewer rounds, iterative debugging, evolving skills/policies or any keep-improving loop.

## Do not activate
Do not add review rounds to a simple task that already satisfies acceptance tests.

## Antigravity-native execution
Persist the failing case, current hypothesis, implementation delta and acceptance result in project artifacts. Use version control as the audit trail and keep skill text thin; large evals belong in test fixtures.

## Workflow
1. Preserve the failure before editing.
2. Localize earliest causal layer.
3. Change the smallest correct owner.
4. Run target and neighboring protection tests.
5. Run holdout/regression checks.
6. Pivot after two materially equivalent no-delta attempts.
7. Promote only demonstrated improvement; retain rollback.

## Validation
Fingerprint each round by changed hypothesis, mechanism, evidence family, implementation and acceptance result. A reviewer cannot silently invent a new hard gate after the task contract is fixed.

## Boundaries
More rounds, roles or tokens are not progress. The skill being changed must not be its sole approver for material promotion.