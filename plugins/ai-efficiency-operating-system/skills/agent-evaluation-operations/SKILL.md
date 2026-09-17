---
name: agent-evaluation-operations
description: Use when changing an agent's prompts, models, tools, routing, memory, orchestration, skills, or runtime and quality must be measured beyond anecdotal examples or same-context self-review.
---

# Agent Evaluation Operations

## Core principle

Evaluate the **behavioral trajectory and user outcome**, then bind promotion claims to the strongest evaluation actually executed.

## Evaluation stack

Separate:

- unit/contract tests for deterministic code and tools;
- trajectory tests for tool choice, ordering, state and recovery;
- rubric/task evals for outcome quality;
- fresh-context or holdout tests for generalization;
- adversarial/metamorphic tests for invariants;
- host-live regression for the actual owning runtime;
- online SLO/feedback monitoring after release.

## Workflow

1. Convert user-visible failures into versioned fixtures before tuning.
2. Stratify by failure class, difficulty, host/version and criticality.
3. Freeze the target revision, model/runtime and evaluator contract.
4. Run baseline before the change when practical.
5. Score both final outcome and acceptance-critical trajectory properties.
6. Use judges only with explicit rubrics; test order, verbosity and self-preference bias where consequential.
7. Keep builder, evaluator and evidence paths independent when practical.
8. Compare deltas with uncertainty and slice-level regressions, not one aggregate score.
9. Promote only to the highest evidence tier actually run.

## Hard rules

- `CONSENSUS != INDEPENDENT EVIDENCE`.
- Same-model self-critique does not become a holdout by changing role names.
- A public fixture pass does not prove hidden generalization.
- Green harness CI proves harness behavior unless target-model behavior also ran.
- A better mean score cannot hide a critical-regression slice.
- Evals that do not reproduce a real decision or failure mode are weak release gates.

**REQUIRED SUB-SKILL:** use `completion-gate` before a stable/passed release claim.

## Output

Return fixture set, evidence tier, baseline/change scores, slice regressions, judge limitations, exact evaluated revision and promotion status.
