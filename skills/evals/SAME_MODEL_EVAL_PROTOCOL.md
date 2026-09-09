# Same-Model Reasoning Evaluation Protocol

Status: `EXPERIMENTAL / EVALUATION GOVERNANCE`

## Purpose

Allow cheap reasoning smoke tests in the same model/session that helped author the rules, while preventing those tests from being misreported as fresh-context, private-oracle, independent, hidden, host-live, or generalized validation.

## Hard boundary

A same-model visible-fixture evaluation is **not independent evidence** of reasoning improvement.

`SAME_MODEL_PASS != INDEPENDENT_VALIDATION`

`AUTHORING_MODEL_GRADES_ITS_OWN_FIXTURES != UNBIASED_JUDGE`

`FIXTURE_FAMILIARITY != GENERALIZATION`

`PUBLIC_EXPECTED_LABELS != PRIVATE_ORACLE`

Same-model evaluation may detect obvious regressions, contradictions, missing fields, or inability to apply a declared procedure. It cannot establish robustness on unseen distributions, hidden perturbations, runtime independence, or host-live behavior.

## Allowed status vocabulary

- `SMOKE_BASELINE_PASS` — the current model can apply declared rules to explicit visible fixtures without an obvious contract contradiction.
- `SMOKE_BASELINE_FAIL` — one or more explicit fixtures expose a visible failure.
- `INDEPENDENT_JUDGE_NOT_RUN` — no appropriately separated evaluator has graded the outputs.
- `PRIVATE_ORACLE_NOT_RUN` — no separated private scoring artifact has graded frozen target outputs.
- `PERTURBED_HIDDEN_NOT_RUN` — no hidden metamorphic/paired relation has been executed.
- `UNSEEN_GENERALIZATION_NOT_RUN` — no independently/procedurally generated unseen adversarial set has been executed.
- `REPEATED_VARIANCE_NOT_RUN` — no repeated sampling has estimated stability/calibration.
- `HOST_LIVE_REGRESSION_NOT_RUN` — intended host/runtime behavior has not been tested.

Never emit `VALIDATED`, `STABLE`, `INDEPENDENT_PASS`, or `HOST_LIVE_VERIFIED` from visible same-model evidence alone.

## Same-model smoke procedure

For each public/visible fixture:

1. Hide `must_detect` / `fail_if` from the answering pass when practical, but still record if the same session authored or saw them.
2. Produce a compact auditable output containing observable conclusions/labels, not private chain-of-thought.
3. Compare that output to the visible fixture contract.
4. Record case ID, output summary, detected concepts, missed obligations, triggered fail conditions, result and evaluator identity class.
5. Aggregate results by suite while preserving every failure/NOT_RUN.
6. Any rule patch caused by the test must be followed by a re-run; never erase the original failure receipt.

A same-model smoke can be useful engineering evidence even when contaminated. Its value is regression detection, not proof of generalization.

## Contamination tags

Every receipt must declare, using `null/UNKNOWN` rather than optimistic guesses:

- `authoring_overlap`;
- whether the base fixture was visible to the generator;
- whether expected labels were visible to the generator;
- whether a hidden variant was visible;
- whether responses were frozen before scoring;
- judge independence;
- runtime independence;
- host-live state.

Visible authored-fixture success is capped at `SAME_MODEL_SMOKE`.

Authoring overlap does **not** magically invalidate a later genuinely fresh/private holdout, but promotion for that later run must be based on its own artifact separation: expected labels withheld, fresh context, frozen responses, private oracle/independent judge, hidden variants, and receipts as required.

## Current canonical suites

- S1–S12 — semantic/pragmatic reasoning.
- CQ1–CQ8 — argument schemes / critical questions.
- C1–C10 — causal / abductive reasoning.
- J1–J8 — judge bias / anti-sycophancy.
- E1–E12 — epistemic calibration / evidence sufficiency / VOI.
- DR1–DR10 — decision robustness / loss / shift / regret.
- GO1–GO10 — goal/objective fidelity / clarification / proxy integrity.
- TT1–TT10 — temporal/trajectory integrity.
- V1–V10 — verifier/metamorphic robustness.

Total explicit fixtures currently specified: `90`.

Current visible same-model execution receipts cover `80` fixtures: `78` static PASS and `2` paired-execution-dependent NOT_RUN (`J1`, `J6`). V1–V10 remain specified but not executed.

## Promotion path

Canonical evidence ladder:

`FIXTURE_SPECIFIED`
→ `STATIC_VALIDATED`
→ `SAME_MODEL_SMOKE`
→ `FRESH_CONTEXT_RUN`
→ `PRIVATE_ORACLE_SCORED`
→ `INDEPENDENT_JUDGED`
→ `PERTURBED_HIDDEN`
→ `UNSEEN_ADVERSARIAL`
→ `REPEATED`
→ `AUTHENTIC_MULTI_AGENT_RUNTIME`
→ `HOST_LIVE_REGRESSION`

A later stage does not retroactively change the meaning of an earlier receipt.

For exact requirements and separation rules, use `HOLDOUT_EVAL_PROTOCOL.md` and `reasoning-eval-result.schema.json`.
