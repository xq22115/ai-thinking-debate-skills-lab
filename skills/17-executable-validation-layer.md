# 17 — Executable RC1 Validation Layer

Date: 2026-09-09

## Purpose

Move the project from specification-only artifacts toward evidence-producing validation without overstating what has been tested.

This layer distinguishes deterministic policy execution from model-reasoning smoke tests, decision-robustness smoke tests, goal-objective smoke tests, **temporal-trajectory smoke tests**, independent judging, hidden/adversarial evaluation, repeated evaluation, authentic multi-agent runtime, and host-live verification.

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

Output status is limited to `PASS_STATIC` / `FAIL_STATIC` and explicitly sets `host_live_verified=false`.

### `evals/run_policy_evals.py`

Executable fail-closed policy test harness.

Previously executed deterministic cases cover:
1. false completion after file write only;
2. pre-step CI infrastructure failure;
3. role labels without runtime independence receipts;
4. visible tool action without observed authorization;
5. read/permission evidence without successful mutation read-back;
6. recovery after irreversible action receipt;
7. separation of VERIFIED from HOST_LIVE/DEPLOYED/HEALTHY.

### `skills/evals/SAME_MODEL_EVAL_PROTOCOL.md`

Governance contract for cheap smoke tests performed by the same model/session that helped author rules or fixtures.

`SAME_MODEL_PASS != INDEPENDENT_VALIDATION`

Same-model results may expose obvious contract failures/regressions, but cannot establish unseen generalization, unbiased judging, runtime independence, distribution-shift robustness, objective fidelity on hidden/mixed goals, **real long-horizon temporal robustness**, or host-live behavior.

## Executed receipts

### Deterministic policy receipt — 2026-08-18

- 7 passed
- 0 failed
- `PASS_POLICY`
- `authentic_multi_agent_runtime = NOT_RUN`
- `host_live_verified = false`

Receipt: `evidence/rc1-policy-eval-2026-08-18.json`

### Same-model reasoning smoke — 2026-09-09

- 50 explicit S/CQ/C/J/E fixtures considered
- 48 static smoke pass
- 2 paired/runtime-dependent NOT_RUN (`J1-order-swap`, `J6-blind-label-invariance`)
- static fail: 0
- evidence class: `LOW_SELF_REFERENTIAL`
- independent judge / hidden variants / repeated variance / host-live: NOT_RUN

Receipt: `evidence/same-model-reasoning-smoke-2026-09-09.json`

### Same-model decision-robustness smoke — 2026-09-09

- DR1–DR10: 10/10 visible static smoke PASS
- evidence class: `LOW_SELF_REFERENTIAL`
- hidden shift variants / independent judge / repeated variance / host-live: NOT_RUN

Receipt: `evidence/same-model-decision-robustness-smoke-2026-09-09.json`

### Same-model goal-objective smoke — 2026-09-09

- GO1–GO10: 10/10 visible static smoke PASS
- evidence class: `LOW_SELF_REFERENTIAL`
- authoring overlap: true
- expected labels visible: true
- fresh-context run: NOT_RUN
- hidden ambiguity/mixed-goal variants: NOT_RUN
- real proxy-gaming runtime: NOT_RUN
- independent judge: NOT_RUN
- repeated variance: NOT_RUN
- host-live: false

Receipt: `evidence/same-model-goal-objective-smoke-2026-09-09.json`

Interpretation: the visible Goal Contract / objective-audit rules are internally applicable to the authored GO fixtures. This does **not** establish real intent-understanding gains, real-user helpfulness improvement, hidden-goal inference, or resistance to specification gaming in a live agent runtime.

### Same-model temporal-trajectory smoke — 2026-09-09

- TT1–TT10: 10/10 visible static smoke PASS
- evidence class: `LOW_SELF_REFERENTIAL`
- authoring overlap: true
- expected labels visible: true
- fresh-context run: NOT_RUN
- delayed-feedback execution: NOT_RUN
- first-irrecoverable-error / trajectory-attribution execution: NOT_RUN
- asynchronous planning execution: NOT_RUN
- checkpoint-staleness recovery execution: NOT_RUN
- independent judge: NOT_RUN
- repeated variance: NOT_RUN
- host-live: false

Receipt: `evidence/same-model-temporal-trajectory-smoke-2026-09-09.json`

Interpretation: the visible temporal/trajectory rules are internally applicable to TT1–TT10 in the same authoring context. This does **not** establish real delayed-feedback credit assignment, long-horizon planning improvement, asynchronous execution robustness, long-trajectory judge reliability, or host-live recovery quality.

## Validation ladder

Do not collapse:

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

A later level does not retroactively upgrade an earlier receipt.

## Important boundary

`PASS_POLICY` proves only deterministic fail-closed policy behavior for the executed policy cases.

`SAME_MODEL_SMOKE` proves only visible contract conformance in a contaminated authoring context.

Neither proves:
- general model reasoning quality;
- independent intent understanding;
- performance on hidden ambiguity/mixed-goal/adversarial distributions;
- preference/helpfulness alignment in real user outcomes;
- specification-gaming resistance in live agents;
- calibrated confidence over repeated trials;
- natural distribution-shift robustness;
- optimal utility/loss modeling;
- genuine epistemic diversity;
- authentic 10/30-agent execution;
- long-horizon global constraint satisfaction;
- real delayed-feedback or temporal credit assignment;
- reliable first-irrecoverable-error localization;
- asynchronous shared-state execution robustness;
- checkpoint freshness/recovery under live mutable environments;
- long-trajectory evaluator robustness;
- host adapter compatibility;
- hosted GitHub CI health;
- deployment;
- stable release status.

Those remain separate release gates.