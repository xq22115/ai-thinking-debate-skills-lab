---
name: competing-hypotheses
description: Use when multiple materially different explanations could fit the observed failure or evidence and choosing the wrong one would change the fix, research path or risk.
---

# Competing Hypotheses

## Purpose
Prevent first-story lock-in by maintaining a small set of causally distinct explanations and tests that can separate them.

## Activate when
Use for ambiguous bugs, conflicting evidence, causal diagnosis, performance regressions, reliability failures or uncertain external behavior.

## Do not activate
Do not manufacture alternatives after one cause is already directly proven and alternatives cannot change the action.

## Antigravity-native execution
Keep 2–5 live hypotheses in a compact project note or task state. Use native inspection/tooling to run discriminators; do not load long debate prose into context.

## Workflow
For each hypothesis record mechanism, predicted observation, falsifier, required evidence, cheapest discriminator and implication for the fix. Prefer tests that eliminate whole branches. Update posterior confidence only from evidence, not reviewer votes.

## Validation
A good discriminator must produce different expected outcomes for at least two live hypotheses. If every result can be explained by every hypothesis, redesign the test.

## Boundaries
Consensus is not correctness. Preserve unresolved uncertainty and do not convert weak correlation into a root-cause claim.