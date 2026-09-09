# 17 — Executable RC1 Validation Layer

Date: 2026-09-09

## Purpose

Move the project from specification-only artifacts toward evidence-producing validation without overstating what has been tested.

This layer now distinguishes:

- deterministic policy execution;
- visible same-model reasoning smoke;
- evaluation-harness hosted CI;
- fresh-context target execution;
- separated private-oracle scoring;
- independent judging;
- hidden/metamorphic execution;
- unseen adversarial evaluation;
- repeated variance/calibration;
- authentic independent multi-agent runtime;
- host-live reasoning regression.

## Components

### `tools/validate_rc1_package.py`

Deterministic static package validator. It validates package shape/contracts and explicitly does not establish host-live/model behavior.

### `skills/evals/run_policy_evals.py`

Executable deterministic fail-closed policy harness. Previously executed cases cover false completion, pre-step infrastructure classification, role-label vs runtime independence, visibility/auth/write verification, recovery after irreversible action receipt, and status separation.

`PASS_POLICY` means only that the executed deterministic policy cases passed.

### `skills/evals/SAME_MODEL_EVAL_PROTOCOL.md`

Governance for cheap contaminated visible-fixture smoke tests.

`SAME_MODEL_PASS != INDEPENDENT_VALIDATION`.

### `skills/evals/HOLDOUT_EVAL_PROTOCOL.md`

Defines stronger artifact separation:

`PUBLIC GENERATION MANIFEST -> FROZEN TARGET RESPONSES -> PRIVATE SCORING ARTIFACT`

A reusable private oracle/hidden expected label set must not be published to the target-generation path before responses freeze.

### `skills/evals/run_reasoning_evals.py`

Provider-neutral scorer. It intentionally does **not** call a model. It consumes already-produced response/judgment artifacts, performs deterministic label/exact/pair scoring where available, and computes the maximum evidence class supported by explicit separation/receipt metadata.

The hardened runner requires actual scored private evidence before `PRIVATE_ORACLE_SCORED`, and an actual scored pair relation before `PERTURBED_HIDDEN`. Metadata/file presence alone is insufficient.

### Machine-readable contracts

- `skills/evals/reasoning-eval-manifest.schema.json`
- `skills/evals/reasoning-eval-result.schema.json`
- `skills/evals/paired-judge-execution-plan.json`

The J1/J6 pair plan requires both presentations, stable underlying candidate IDs, frozen responses, and relation scoring. One presentation cannot close an invariance gate.

## Executed receipts

### Deterministic policy receipt — 2026-08-18

- 7 passed
- 0 failed
- `PASS_POLICY`
- authentic multi-agent runtime: NOT_RUN
- host-live verified: false

Receipt:

`evidence/rc1-policy-eval-2026-08-18.json`

### Visible same-model reasoning smoke — 2026-09-09

S/CQ/C/J/E:

- total explicit fixtures considered: 50
- static smoke PASS: 48
- paired/runtime-dependent NOT_RUN: 2 (`J1-order-swap`, `J6-blind-label-invariance`)
- static fail: 0
- evidence class: `LOW_SELF_REFERENTIAL`

Receipt:

`evidence/same-model-reasoning-smoke-2026-09-09.json`

### Visible same-model decision-robustness smoke — 2026-09-09

DR1–DR10: 10/10 visible static PASS; hidden shift, independent judge, repeated variance and host-live remain NOT_RUN.

Receipt:

`evidence/same-model-decision-robustness-smoke-2026-09-09.json`

### Visible same-model goal-objective smoke — 2026-09-09

GO1–GO10: 10/10 visible static PASS; hidden ambiguity/proxy-gaming runtime, independent judge, repeated variance and host-live remain NOT_RUN.

Receipt:

`evidence/same-model-goal-objective-smoke-2026-09-09.json`

### Visible same-model temporal-trajectory smoke — 2026-09-09

TT1–TT10: 10/10 visible static PASS; delayed-feedback execution, trajectory attribution, async planning, independent judge, repeated variance and host-live remain NOT_RUN.

Receipt:

`evidence/same-model-temporal-trajectory-smoke-2026-09-09.json`

### Hosted reasoning-eval harness CI — 2026-09-09

Two GitHub-hosted passes are recorded.

Initial contract gate:

- commit: `6f89989bd9423d7af33c2e32eab789726fa68f91`
- workflow run: `34347021367`
- job: `102450923651`
- conclusion: `success`

Hardened pair-promotion regression:

- commit: `9ee4f9aeff99c6c39e27afd5633174e677b0345f`
- workflow: `Reasoning Eval Harness Gate`
- workflow run: `34347854340`
- job: `102453635615`
- conclusion: `success`

The hardened job successfully executed:

1. Compile provider-neutral runner.
2. Validate public machine-readable eval artifacts.
3. Run public NON-HIDDEN contract example.
4. Verify incomplete pair fails closed.
5. Assert public example cannot self-promote to hidden or independent evidence.
6. Synthetic regression: hidden promotion requires a genuinely scored pair relation.

The synthetic regression confirmed that a run with fresh/private/independent metadata but one missing member of the pair remains `PARTIAL`, with the pair `UNSCORED`, and cannot rise above `INDEPENDENT_JUDGED`; only the complete paired execution can reach the synthetic `PERTURBED_HIDDEN` rung.

Machine-readable receipt:

`evidence/reasoning-eval-harness-ci-2026-09-09.json`

Interpretation:

`PASS_HARNESS_CI_HARDENED` proves the evaluation harness executable and fail-closed promotion contract on GitHub-hosted CI at the recorded revisions. It does **not** prove target-model reasoning quality, fresh-context execution, private holdout success, independent judging, hidden generalization, authentic multi-agent reasoning, or host-live reasoning behavior.

## Explicit fixture inventory

Currently specified:

- S1–S12 = 12
- CQ1–CQ8 = 8
- C1–C10 = 10
- J1–J8 = 8
- E1–E12 = 12
- DR1–DR10 = 10
- GO1–GO10 = 10
- TT1–TT10 = 10
- V1–V10 = 10

Total: `90`.

Visible same-model receipts currently cover 80 fixtures:

- 78 visible static PASS
- 2 paired execution NOT_RUN (J1/J6)

V1–V10 remain `SPECIFIED_NOT_EXECUTED`.

## Canonical evaluation ladder

Do not collapse these evidence levels:

1. `FIXTURE_SPECIFIED`
2. `STATIC_VALIDATED`
3. `SAME_MODEL_SMOKE`
4. `FRESH_CONTEXT_RUN`
5. `PRIVATE_ORACLE_SCORED`
6. `INDEPENDENT_JUDGED`
7. `PERTURBED_HIDDEN`
8. `UNSEEN_ADVERSARIAL`
9. `REPEATED`
10. `AUTHENTIC_MULTI_AGENT_RUNTIME`
11. `HOST_LIVE_REGRESSION`

A later level does not retroactively upgrade the meaning of an earlier receipt.

`HOSTED_EVAL_HARNESS_CI` is an orthogonal infrastructure state, not a replacement for any target-model reasoning level above.

## Current truth state

- deterministic policy harness: PASS for recorded cases;
- visible same-model smoke: PARTIAL/LOW_SELF_REFERENTIAL as recorded;
- provider-neutral eval harness hosted GitHub CI: `PASS_HARNESS_CI_HARDENED`;
- fresh-context target reasoning: NOT_RUN;
- private-oracle target scoring: NOT_RUN;
- J1/J6 true paired target execution: NOT_RUN;
- independent judge: NOT_RUN;
- hidden/metamorphic target execution: NOT_RUN;
- unseen adversarial target evaluation: NOT_RUN;
- repeated target variance/calibration: NOT_RUN;
- authentic independent multi-agent reasoning runtime: NOT_RUN;
- host-live reasoning regression: NOT_RUN;
- STABLE release: NOT_CLAIMED.

## Important boundary

Do not infer any of these from policy, fixture, same-model, or harness-CI evidence alone:

- generalized reasoning improvement;
- independent intent understanding;
- calibration across repeated trials;
- hidden/adversarial robustness;
- real distribution-shift robustness;
- authentic multi-agent epistemic diversity;
- host adapter compatibility;
- deployment/health;
- stable release status.

Those remain separate release gates.
