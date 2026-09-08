# Same-Model Reasoning Evaluation Protocol

Status: `EXPERIMENTAL / EVALUATION GOVERNANCE`

## Purpose

Allow cheap reasoning smoke tests in the same model/session that helped author the rules, while preventing those tests from being misreported as independent validation.

## Hard boundary

A same-model evaluation is **not independent evidence** of reasoning improvement.

`SAME_MODEL_PASS != INDEPENDENT_VALIDATION`

`AUTHORING_MODEL_GRADES_ITS_OWN_FIXTURES != UNBIASED_JUDGE`

`FIXTURE_FAMILIARITY != GENERALIZATION`

Same-model evaluation may detect obvious regressions, contradictions, missing fields, or inability to apply the declared procedure. It cannot establish robustness on unseen distributions or host-live behavior.

## Allowed status vocabulary

- `SMOKE_BASELINE_PASS` — the current model can apply the declared rules to the explicit fixtures without an obvious contradiction.
- `SMOKE_BASELINE_FAIL` — one or more explicit fixtures expose a failure in the current procedure/application.
- `INDEPENDENT_JUDGE_NOT_RUN` — no appropriately separated evaluator has graded the outputs.
- `UNSEEN_GENERALIZATION_NOT_RUN` — no hidden/unseen adversarial set has been executed.
- `REPEATED_VARIANCE_NOT_RUN` — no repeated sampling has estimated stability/calibration.
- `HOST_LIVE_REGRESSION_NOT_RUN` — intended host/runtime behavior has not been tested.

Never emit `VALIDATED`, `STABLE`, `INDEPENDENT_PASS`, or `HOST_LIVE_VERIFIED` from same-model evidence alone.

## Evaluation procedure

For each fixture:

1. Hide the fixture's `must_detect` / `fail_if` fields from the reasoning pass when practical.
2. Produce a compact auditable answer containing only observable claims/labels, not private chain-of-thought.
3. Compare that output to the fixture contract.
4. Record:
   - case id;
   - output summary;
   - detected concepts;
   - missed required concepts;
   - triggered fail conditions;
   - result: `PASS / PARTIAL / FAIL`;
   - evaluator identity class.
5. Aggregate results by suite, but retain per-case failures.
6. Any rule patch caused by the test must be followed by a re-run; do not erase the original failure receipt.

## Contamination tags

Every receipt must declare:

- `authoring_overlap`: whether the evaluated model/session authored or edited the fixtures/rules;
- `fixture_visibility`: whether expected labels were visible to the evaluator;
- `judge_independence`: same-model / fresh-context-same-model / different-model / human / deterministic-gold;
- `runtime_independence`: whether executions were actually separate;
- `host_live`: true/false.

If `authoring_overlap=true`, the highest evidence class available is `SMOKE_BASELINE` unless a separately generated unseen set is used with an independent judge.

## Current canonical suites

- S1–S12 — semantic/pragmatic reasoning.
- CQ1–CQ8 — argument schemes / critical questions.
- C1–C10 — causal / abductive reasoning.
- J1–J8 — judge bias / anti-sycophancy.
- E1–E12 — epistemic calibration / evidence sufficiency / VOI.

Total explicit fixtures: 50.

## Promotion path

`FIXTURE_SPECIFIED`
→ `SAME_MODEL_SMOKE`
→ `FRESH_CONTEXT_RUN`
→ `INDEPENDENT_JUDGED`
→ `UNSEEN_ADVERSARIAL`
→ `REPEATED_VARIANCE`
→ `HOST_LIVE_REGRESSION`

A later stage does not retroactively change the meaning of an earlier receipt.
