---
name: plan-arbiter
description: Use when choosing between implementation routes, architectures, sequencing options, tradeoffs, or recovery plans before effectful execution.
---

# Plan Arbiter

Choose the route most likely to reach the frozen acceptance state, not the route that is easiest to describe.

## Build a decision set

For each materially different route record:

- causal mechanism;
- prerequisites and host capability;
- acceptance criteria it unlocks;
- high-impact assumptions;
- reversibility and blast radius;
- cheapest discriminating test;
- evidence already available;
- rollback/fallback.

Do not count cosmetic variants as alternatives.

## Order work by leverage

Prefer:

1. identity/target mistakes that invalidate all downstream work;
2. assumptions that can cheaply falsify a whole branch;
3. shared upstream causes that explain multiple symptoms;
4. reversible probes before irreversible changes;
5. implementation only after the route has enough evidence.

Use destination/frontier/fog rather than over-planning uncertain downstream detail.

## Keep planning distinct from research

If the blocker is a factual/current unknown, hand only that obligation to `executive-research`, then resume plan ownership. The presence of words such as "verify" or "research" does not by itself transfer the whole task.

Before effectful execution, hand the chosen plan and its acceptance mapping back to `chief-of-staff-core`. Completion remains owned by `evidence-watchdog`.

## Output

Return the recommended route, why it dominates, rejected alternatives, the first discriminating action, rollback boundary and acceptance mapping. Preserve unresolved uncertainty rather than hiding it inside a confident plan.
