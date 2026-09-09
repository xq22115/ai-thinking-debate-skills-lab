# 17 — Executable RC1 Validation Layer

Date: 2026-09-09

## Purpose

Move the project from specification-only artifacts toward evidence-producing validation without overstating what has been tested.

This layer distinguishes:

- deterministic policy execution;
- visible same-model reasoning smoke;
- evaluation-harness hosted CI;
- fresh-context target execution;
- salted private-oracle precommit/reveal;
- frozen-response binding;
- actual private-oracle scoring;
- actual designated-case independent judging;
- hidden/metamorphic execution;
- unseen adversarial evaluation;
- repeated variance/calibration;
- authentic independent multi-agent runtime;
- host-live reasoning regression.

## Components

### `tools/validate_rc1_package.py`

Deterministic static package validator. Package shape/static PASS does not establish model or host-live behavior.

### `skills/evals/run_policy_evals.py`

Deterministic fail-closed policy harness. `PASS_POLICY` applies only to its executed policy cases.

### `skills/evals/SAME_MODEL_EVAL_PROTOCOL.md`

Governance for contaminated visible-fixture smoke.

`SAME_MODEL_PASS != INDEPENDENT_VALIDATION`.

### `skills/evals/HOLDOUT_EVAL_PROTOCOL.md`

Canonical private-evaluation flow:

`PRIVATE BLUEPRINT -> PUBLIC MANIFEST + SALTED ORACLE COMMITMENT -> TARGET RUN -> RESPONSE FREEZE -> REVEAL SALT + ORACLE -> VERIFY BINDING -> SCORE`

### Commit-reveal tools

- `skills/evals/prepare_holdout_commitment.py`
- `skills/evals/freeze_eval_responses.py`
- `skills/evals/verify_holdout_reveal.py`
- `skills/evals/run_reasoning_evals.py`

All are provider-neutral and do not themselves execute a target model.

The pre-run commitment uses a private random salt over canonical private-oracle JSON. For a real reusable hidden run, salt/oracle/private blueprint remain outside the public target-generation path until target responses freeze.

### Machine-readable contracts

- `skills/evals/holdout-blueprint.schema.json`
- `skills/evals/holdout-commitment.schema.json`
- `skills/evals/reasoning-eval-manifest.schema.json`
- `skills/evals/response-freeze-receipt.schema.json`
- `skills/evals/holdout-reveal-receipt.schema.json`
- `skills/evals/reasoning-eval-result.schema.json`
- `skills/evals/paired-judge-execution-plan.json`

### Hardened promotion requirements

The current runner requires:

- actual target execution before any target-model rung;
- fresh context + withheld expected labels for `FRESH_CONTEXT_RUN`;
- frozen responses + actual deterministic private scoring + verified salted commit-reveal for `PRIVATE_ORACLE_SCORED`;
- an independent judge actually scoring a designated `SEMANTIC_JUDGE` case with receipt for `INDEPENDENT_JUDGED`;
- all required paired presentations + actual relation scoring for `PERTURBED_HIDDEN`.

Metadata/file presence alone is insufficient.

Hard invariants:

- `ORACLE_PRESENT != COMMITMENT_REVEALED_AND_VERIFIED`
- `JUDGMENT_ARTIFACT_PRESENT != CASE_ACTUALLY_INDEPENDENTLY_JUDGED`
- `PAIR_RULE_PRESENT != PAIR_EXECUTED_AND_SCORED`
- `RESPONSE_SET_AFTER_FREEZE != AUTHORIZED_FROZEN_RESPONSE_SET`
- `HOSTED_EVAL_HARNESS_CI != TARGET_MODEL_PASS`

## Executed receipts

### Deterministic policy receipt — 2026-08-18

- 7 passed
- 0 failed
- `PASS_POLICY`
- authentic multi-agent runtime: NOT_RUN
- host-live verified: false

Receipt: `evidence/rc1-policy-eval-2026-08-18.json`

### Visible same-model smoke — 2026-09-09

- S/CQ/C/J/E: 50 considered, 48 static PASS, J1/J6 paired NOT_RUN.
- DR1–DR10: 10/10 visible static PASS.
- GO1–GO10: 10/10 visible static PASS.
- TT1–TT10: 10/10 visible static PASS.

Total visible same-model coverage: 80 fixtures → `78 PASS / 2 NOT_RUN`.

Receipts:

- `evidence/same-model-reasoning-smoke-2026-09-09.json`
- `evidence/same-model-decision-robustness-smoke-2026-09-09.json`
- `evidence/same-model-goal-objective-smoke-2026-09-09.json`
- `evidence/same-model-temporal-trajectory-smoke-2026-09-09.json`

Interpretation: `LOW_SELF_REFERENTIAL`, not hidden/generalized reasoning evidence.

### Hosted reasoning-eval harness CI — 2026-09-09

Three successful hosted phases are recorded.

#### Initial contract gate

- commit `6f89989bd9423d7af33c2e32eab789726fa68f91`
- run `34347021367`
- job `102450923651`
- conclusion `success`

#### Pair-promotion hardening

- commit `9ee4f9aeff99c6c39e27afd5633174e677b0345f`
- run `34347854340`
- job `102453635615`
- conclusion `success`

#### Salted commit-reveal + tamper hardening

- commit `420536f21a26645c43e6d7efa7045511d6eb155a`
- run `34350465562`
- job `102462189384`
- conclusion `success`

The third hosted job successfully executed all core checks:

1. compile the four eval tools;
2. validate public machine-readable artifacts;
3. public NON-HIDDEN example stays at `SAME_MODEL_SMOKE`;
4. incomplete pair fails closed;
5. salted commitment preparation and reveal verification;
6. public manifest excludes private scoring keys;
7. tampered oracle reveal is rejected;
8. response mutation after freeze is rejected at scoring;
9. no reveal receipt prevents `PRIVATE_ORACLE_SCORED` and caps synthetic run at `FRESH_CONTEXT_RUN`;
10. unrelated judgment receipt cannot earn `INDEPENDENT_JUDGED`;
11. incomplete pair cannot earn `PERTURBED_HIDDEN`;
12. complete synthetic pair + designated semantic judgment can exercise the synthetic `PERTURBED_HIDDEN` promotion path.

Machine-readable receipt:

`evidence/reasoning-eval-harness-ci-2026-09-09.json`

Current infrastructure state:

`PASS_HARNESS_CI_COMMIT_REVEAL_HARDENED`

Important: the synthetic promotion cases validate only harness logic. They are not target-model fresh-context/private/hidden reasoning results.

## Explicit fixture inventory

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

V1–V10 remain `SPECIFIED_NOT_EXECUTED`.

## Canonical evaluation ladder

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

`HOSTED_EVAL_HARNESS_CI` is an orthogonal infrastructure state, not a target-model rung.

## Current truth state

- deterministic policy harness: PASS for recorded cases;
- visible same-model smoke: PARTIAL / LOW_SELF_REFERENTIAL as recorded;
- provider-neutral eval harness hosted GitHub CI: `PASS_HARNESS_CI_COMMIT_REVEAL_HARDENED`;
- salted commitment/reveal harness logic: PASS in hosted CI;
- tamper-detection harness logic: PASS in hosted CI;
- fresh-context target reasoning: NOT_RUN;
- real private-oracle target scoring: NOT_RUN;
- J1/J6 true paired target execution: NOT_RUN;
- real independent judge: NOT_RUN;
- hidden/metamorphic target execution: NOT_RUN;
- unseen adversarial target evaluation: NOT_RUN;
- repeated target variance/calibration: NOT_RUN;
- authentic independent multi-agent reasoning runtime: NOT_RUN;
- host-live reasoning regression: NOT_RUN;
- STABLE release: NOT_CLAIMED.

## Important boundary

Do not infer any of these from policy, public fixtures, synthetic promotion tests, or harness CI alone:

- generalized reasoning improvement;
- independent intent understanding;
- real private-holdout success;
- hidden/adversarial robustness;
- calibrated repeated performance;
- distribution-shift robustness;
- authentic multi-agent epistemic diversity;
- host adapter compatibility;
- deployment/health;
- stable release status.

Those remain separate release gates.
