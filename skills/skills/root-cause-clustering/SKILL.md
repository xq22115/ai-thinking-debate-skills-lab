---
name: root-cause-clustering
description: Group multiple symptoms under shared mechanisms before applying fixes. Use when fixing A creates B/C regressions, when many errors appear related, or when repeated local patches are accumulating.
---

# Root Cause Clustering

Version: `0.1.0-rc1`

## Objective

Repair mechanisms, not symptom lists.

## Workflow

1. Inventory observed symptoms without assuming they are independent.
2. Build a dependency/causal map linking each symptom to components, state, inputs, permissions, versions, and shared resources.
3. Cluster symptoms by candidate shared mechanism.
4. Rank root-cause candidates by explanatory coverage and falsifiability.
5. Reproduce the smallest representative symptom for each cluster.
6. Test the shared mechanism before patching individual symptoms.
7. Apply the smallest reversible mechanism-level change.
8. Regression-test every symptom in the cluster plus adjacent functionality.

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

A repair is not complete until the shared mechanism and the full affected symptom cluster have been re-tested.