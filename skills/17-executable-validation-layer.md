# 17 — Executable RC1 Validation Layer

Date: 2026-09-09

## Purpose

Move the project from specification-only artifacts toward evidence-producing validation without overstating what has been tested.

This layer distinguishes deterministic policy execution from model-reasoning smoke tests, decision-robustness smoke tests, independent judging, hidden/adversarial evaluation, repeated evaluation, authentic multi-agent runtime, and host-live verification.

## Components

### `tools/validate_rc1_package.py`

Deterministic static package validator.

Checks include:
- required research/governance/eval files exist;
- canonical skills/references are present;
- every `SKILL.md` has matching `name` plus non-empty `description` frontmatter;
- key JSON ledgers/fixtures parse successfully;
- STATUS does not contain an unqualified terminal status such as `STABLE`, `DEPLOYED`, `HEALTHY`, or `HOST_LIVE_VERIFIED`;
- role activation policy retains escalation/de-escalation/coverage-pool signals.

Output status is limited to:
- `PASS_STATIC`
- `FAIL_STATIC`

It explicitly sets `host_live_verified=false`.

### `evals/run_policy_evals.py`

Executable fail-closed policy test harness.

The previously executed deterministic policy cases cover:
1. false completion after file write only;
2. pre-step CI infrastructure failure;
3. role labels without runtime independence receipts;
4. visible tool action without observed authorization;
5. read/permission evidence without successful mutation read-back;
6. recovery after irreversible action receipt;
7. separation of VERIFIED from HOST_LIVE/DEPLOYED/HEALTHY.

### `skills/evals/SAME_MODEL_EVAL_PROTOCOL.md`

Governance contract for cheap reasoning smoke tests performed by the same model/session that helped author the rules or fixtures.

Hard boundary:

`SAME_MODEL_PASS != INDEPENDENT_VALIDATION`

Same-model results may expose obvious contract failures or regressions, but cannot establish unseen generalization, unbiased judging, runtime independence, distribution-shift robustness, or host-live behavior.

Allowed output classes include `SMOKE_BASELINE_PASS`, `SMOKE_BASELINE_FAIL`, and explicit `NOT_RUN` gates.

## Executed receipts

### Deterministic policy receipt — 2026-08-18

A local deterministic run produced:

- 7 passed
- 0 failed
- `PASS_POLICY`
- `authentic_multi_agent_runtime = NOT_RUN`
- `host_live_verified = false`

Machine-readable receipt:

`evidence/rc1-policy-eval-2026-08-18.json`

### Same-model reasoning smoke receipt — 2026-09-09

A same-session, authoring-overlap contract-conformance pass was recorded against the explicit S/CQ/C/J/E fixture families.

Result:

- total explicit fixtures: 50
- static smoke pass: 48
- paired/runtime-dependent not run: 2
- static fail: 0
- not-run cases: `J1-order-swap`, `J6-blind-label-invariance`
- evidence class: `LOW_SELF_REFERENTIAL`
- authoring overlap: true
- fixture expected labels visible: true
- independent judge: NOT_RUN
- host-live: false

Machine-readable receipt:

`evidence/same-model-reasoning-smoke-2026-09-09.json`

Interpretation: the current procedural rules can be applied consistently to the 48 static explicit fixtures in the same authoring context. This is **not** evidence of independent model improvement.

### Same-model decision-robustness smoke receipt — 2026-09-09

A separate same-session, authoring-overlap contract-conformance pass was recorded for DR1–DR10.

Result:

- total explicit fixtures: 10
- static smoke pass: 10
- partial: 0
- fail: 0
- evidence class: `LOW_SELF_REFERENTIAL`
- authoring overlap: true
- fixture expected labels visible: true
- fresh-context run: NOT_RUN
- hidden shift variants: NOT_RUN
- independent judge: NOT_RUN
- repeated variance: NOT_RUN
- host-live: false

Machine-readable receipt:

`evidence/same-model-decision-robustness-smoke-2026-09-09.json`

Interpretation: the current decision-robustness rules are internally applicable to the 10 visible authored fixtures. This does **not** establish real distribution-shift robustness, correct human utilities, numerical regret optimality, or host-live action quality.

## Validation ladder

Do not collapse these evidence levels:

1. `FIXTURE_SPECIFIED`
2. `STATIC_VALIDATED`
3. `SAME_MODEL_SMOKE`
4. `FRESH_CONTEXT_RUN`
5. `INDEPENDENT_JUDGED`
6. `PERTURBED_HIDDEN`
7. `UNSEEN_ADVERSARIAL`
8. `REPEATED_VARIANCE`
9. `AUTHENTIC_MULTI_AGENT_RUNTIME`
10. `HOST_LIVE_REGRESSION`

A later level does not retroactively upgrade the meaning of an earlier receipt.

## Important boundary

`PASS_POLICY` proves only deterministic fail-closed policy behavior for the executed policy cases.

`SAME_MODEL_SMOKE` proves only visible contract conformance in a contaminated authoring context.

Neither proves:
- general model reasoning quality;
- performance on unseen/adversarial distributions;
- calibrated confidence over repeated trials;
- position/order/prestige invariance unless paired experiments actually run;
- natural distribution-shift robustness;
- optimal utility/loss modeling;
- genuine epistemic diversity;
- authentic 10/30-agent execution;
- host adapter compatibility;
- hosted GitHub CI health;
- deployment;
- stable release status.

Those remain separate release gates.