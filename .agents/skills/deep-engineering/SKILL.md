---
name: deep-engineering
description: Use to build, debug, refactor, review, configure or repair software where correctness, root cause, regression resistance and executable proof matter.
---

# Deep Engineering

## Purpose
Treat implementation as an evidence-producing process. Observable behavior that satisfies the user's goal is success; a polished patch is not.

## Activate when
Use for substantive code/config changes, debugging, architecture repair, code review, performance work or risky migrations.

## Do not activate
Do not over-process trivial edits that have an obvious local verification.

## Antigravity-native execution
Inspect the real workspace and dependency graph before editing. Prefer native repository/file/terminal operations and current primary docs for volatile APIs. Use version control for reversible changes and keep tests capable of failing.

## Workflow
1. Compile outcome, invariants and critical acceptance tests.
2. Inspect entry points, owners, call sites, tests, versions and persistence boundaries.
3. Maintain competing hypotheses for non-trivial defects.
4. Fix the earliest shared causal mechanism, not a visible symptom.
5. Run target, regression and adversarial/falsification checks.
6. Inspect the final diff and runtime postcondition.

## Validation
Report gates separately: goal, state, root cause, implementation, verification, regression, falsification, continuity and evidence. Use `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`; never average away a critical failure.

## Boundaries
Do not disable required features, reduce quality/concurrency, delete functionality or narrow the requested outcome as a fake fix unless the user explicitly accepts that tradeoff.