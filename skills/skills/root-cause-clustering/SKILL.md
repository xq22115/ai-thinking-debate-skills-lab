---
name: root-cause-clustering
description: Group multiple symptoms under shared mechanisms before applying fixes. Use when fixing A creates B/C regressions, when many errors appear related, or when repeated local patches are accumulating.
---

# Root Cause Clustering

Version: `0.2.0-rc1`

## Objective

Repair mechanisms, not symptom lists.

## Anti-workaround invariants

- A workaround that suppresses a symptom is not a root-cause repair.
- Reducing workload, features, concurrency or quality is a diagnostic probe or mitigation unless the user explicitly makes that tradeoff part of the desired end state.
- A few successful runs do not invalidate a repeated or intermittent failure history.
- Preserve at least one representative failing case before editing when practical.
- A selected root cause must make a discriminating prediction; otherwise it remains a hypothesis.
- If a valid in-scope counterexample remains after the change, completion stays open.
- Prefer the earliest shared causal owner over accumulating wrappers, caps or guardrails.

Use `falsification-root-cause-governor` when universal-vs-probabilistic claims, cherry-picked passes, online repair recipes, or mitigation-vs-fix distinctions are material.

## Workflow

1. Inventory observed symptoms without assuming they are independent.
2. Build a dependency/causal map linking each symptom to components, state, inputs, permissions, versions, and shared resources.
3. Cluster symptoms by candidate shared mechanism.
4. Rank root-cause candidates by explanatory coverage and falsifiability.
5. Reproduce the smallest representative symptom for each cluster.
6. Test the shared mechanism before patching individual symptoms.
7. Apply the smallest reversible mechanism-level change.
8. Read back the loaded/runtime state when configuration or deployment effect is claimed.
9. Re-run the preserved failing case, every symptom in the cluster, negative controls, and adjacent functionality.
10. For intermittent failures, compare pre/post failure counts under a justified repeated-test plan instead of stopping after a small number of passes.

## Output Contract

Return:
- symptom inventory;
- cluster map;
- candidate mechanisms;
- discriminating tests;
- selected root cause;
- repair scope;
- regression surface;
- rollback point.

## Completion Gate

A repair is not complete until the shared mechanism, loaded runtime state, preserved failure case and full affected symptom cluster have been re-tested. A remaining valid in-scope counterexample vetoes a universal "fixed" claim.