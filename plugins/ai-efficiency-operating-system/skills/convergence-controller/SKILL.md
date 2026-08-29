---
name: convergence-controller
description: Use when repeated review, iterative repair, many reviewer comments, skill evolution, or keep-improving loops risk scope creep, stagnation, regression or endless retries.
---

# Convergence Controller

Iteration is useful only when it produces a measurable causal delta.

## Stop loop theater

Fingerprint each round by changed hypothesis, mechanism, evidence family, implementation delta and acceptance result. Two materially equivalent no-progress rounds trigger a pivot; they do not justify a third cosmetic retry.

Default review cap is three rounds unless the user's acceptance contract explicitly requires a different workload. A reviewer may identify risk but cannot silently add a new hard gate after the contract is frozen.

## Failure-driven evolution

For skill/process changes:

1. preserve the failing case before editing;
2. localize the earliest causal failure layer — contract, routing, host, state, verifier, tool, infrastructure, skill prose/reference/script;
3. change the smallest correct owner, which may be `SKILL.md`, a reference, script, config or test;
4. run target cases;
5. run neighboring protection cases;
6. run holdout/full regression;
7. promote only with demonstrated improvement and no protected regression;
8. keep rollback/version history.

The skill being modified cannot be its sole approver. Keep eval/gold data separate from the skill when practical so optimization does not learn the answers.

Read `references/evolution.md` for the whole-folder and Git-audit model.
