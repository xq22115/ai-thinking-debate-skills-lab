# Hidden Holdout / Fresh-Context Evaluation Protocol

Status: `EXPERIMENTAL EVAL INFRASTRUCTURE / NOT A MODEL RESULT`

Purpose: move reasoning evaluation beyond visible same-model smoke while preventing the evaluation harness itself from creating leakage, false independence, unverifiable promotion, or post-hoc oracle/response mutation.

## Hard invariants

- `PUBLIC_FIXTURE_PASS != HIDDEN_GENERALIZATION`
- `FRESH_CONTEXT != PRIVATE_ORACLE`
- `PRIVATE_ORACLE != INDEPENDENT_MODEL_JUDGE`
- `PAIR_TEST_REQUIRES BOTH_EXECUTIONS`
- `METAMORPHIC_CLAIM_REQUIRES_RELATION_CHECK`
- `HIDDEN_LABELS_IN_PUBLIC_REPO != HIDDEN_LABELS`
- `PLAIN_ORACLE_HASH != STRONG_LOW_ENTROPY_COMMITMENT`
- `ORACLE_PRESENT != COMMITMENT_REVEALED_AND_VERIFIED`
- `JUDGMENT_ARTIFACT_PRESENT != CASE_ACTUALLY_INDEPENDENTLY_JUDGED`
- `HASHED_ORACLE != VERIFIED_ORACLE_QUALITY`
- `CONTAMINATION_DETECTION_PASS != PROOF_OF_NO_CONTAMINATION`
- `MODEL_OUTPUT_MUST_BE_FROZEN_BEFORE_PRIVATE_SCORING`
- `RESPONSE_SET_AFTER_FREEZE != AUTHORIZED_FROZEN_RESPONSE_SET`

## 1. Canonical commit-reveal pipeline

For a real private holdout, use this ordering:

`PRIVATE BLUEPRINT -> PUBLIC MANIFEST + SALTED ORACLE COMMITMENT -> TARGET RUN -> RESPONSE FREEZE RECEIPT -> REVEAL SALT + ORACLE -> VERIFY COMMITMENT / MANIFEST / RESPONSE BINDING -> PRIVATE SCORE / INDEPENDENT JUDGE`

Do not reorder the reveal before target response freeze.

### Phase A — private blueprint

The blueprint may contain prompts plus private scoring rules, expected values, pair relations, hidden transformations, and judge-designated cases. For a reusable real holdout it remains outside the public target-generation path.

Canonical schema:

`skills/evals/holdout-blueprint.schema.json`

### Phase B — public manifest + salted commitment

`prepare_holdout_commitment.py` strips scoring material from the public generation manifest and creates a salted commitment over the canonical private oracle.

Commitment algorithm:

`SHA256-SALTED-CANONICAL-JSON-v1`

Conceptually:

`SHA256(domain || private_random_salt || canonical_private_oracle)`

The pre-run public artifact contains the commitment, not the salt or oracle.

A plain unsalted hash of a small/low-entropy label set is not a strong secrecy mechanism because plausible oracle contents may be enumerable offline. The unrevealed random salt prevents direct pre-run dictionary matching while preserving later verification.

Canonical tools/contracts:

- `skills/evals/prepare_holdout_commitment.py`
- `skills/evals/holdout-commitment.schema.json`
- `skills/evals/reasoning-eval-manifest.schema.json`

### Phase C — target execution

The target sees only the public generation manifest plus whatever normal task context the experiment explicitly permits. It must not see the private blueprint, private oracle, salt, expected labels, hidden relation answer, or independent judge verdict.

`FRESH_CONTEXT_RUN` additionally requires that the target execution itself is genuinely separated from the fixture-authoring context and that expected labels were withheld.

### Phase D — response freeze

Before reveal/scoring, freeze the exact target response set.

`freeze_eval_responses.py` binds:

- suite/run ID;
- public-manifest canonical hash;
- canonical response-set hash;
- response count;
- exact case IDs.

Canonical contract:

`skills/evals/response-freeze-receipt.schema.json`

A later response mutation invalidates the reveal binding and must fail closed at scoring time.

### Phase E — reveal and verify

Only after response freeze may the private salt and oracle be revealed to the scoring path.

`verify_holdout_reveal.py` verifies:

- commitment algorithm/domain;
- suite/run identity;
- public manifest hash;
- revealed salted oracle against the pre-run commitment;
- response-freeze receipt binding.

Canonical contract:

`skills/evals/holdout-reveal-receipt.schema.json`

A successful reveal receipt proves commitment consistency and response binding. It does **not** prove oracle correctness, model freshness, judge independence, or reasoning quality.

### Phase F — scoring / independent judging

`run_reasoning_evals.py` consumes frozen target responses, optional private oracle, verified reveal receipt, and optional independent judgments.

It does not call a model.

`PRIVATE_ORACLE_SCORED` requires all of:

- target already executed;
- fresh-context prerequisites satisfied;
- responses frozen before scoring;
- private oracle separated;
- at least one deterministic private case/pair actually scored;
- verified salted commit-reveal receipt binding the same manifest, response set, and oracle.

An oracle file merely being present is insufficient.

`INDEPENDENT_JUDGED` additionally requires an independent judge with its own receipt to have actually scored at least one designated `SEMANTIC_JUDGE` case. An unrelated judgment artifact cannot promote the run.

## 2. Public/private artifact boundary

### Public before target execution

Allowed:

- schemas;
- runner/tool code;
- generation procedures;
- transformation families;
- blank templates;
- public seed fixtures explicitly marked non-hidden;
- public generation manifest;
- salted oracle commitment with salt/oracle unrevealed.

### Private until responses freeze

Keep private:

- reusable holdout expected labels;
- exact private oracle;
- commitment salt;
- hidden variants intended to remain unseen;
- judge gold/rubric content that reveals answers;
- private blueprint when it reveals scoring structure.

### Public after scoring when safe

May publish:

- hashes/commitments;
- non-reusable reveal receipts;
- aggregate results;
- execution receipts;
- disclosed holdout artifacts only when future reuse/secrecy is no longer required.

Do not publish reusable hidden answers and continue calling them hidden.

## 3. Evidence ladder

Do not collapse:

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

### Promotion requirements

`FRESH_CONTEXT_RUN` requires target execution without authoring conversation/context and without expected labels visible to the generator.

`PRIVATE_ORACLE_SCORED` requires verified commit-reveal plus actual deterministic private scoring on frozen responses.

`INDEPENDENT_JUDGED` requires an appropriately separated judge/gold process that actually adjudicated a designated semantic case with its own identity/receipt.

`PERTURBED_HIDDEN` requires at least one relation-preserving variant hidden from the generator before execution, all required paired presentations present, and an actual cross-run relation score.

`UNSEEN_ADVERSARIAL` requires independently or procedurally generated adversarial cases unavailable to the target path before execution.

`REPEATED` requires enough repeated executions for the claimed variance/calibration statement.

`AUTHENTIC_MULTI_AGENT_RUNTIME` requires observable runtime/session separation for claims of independent agents.

`HOST_LIVE_REGRESSION` requires target-host execution/read-back appropriate to the claimed host behavior.

## 4. Pair-only and metamorphic scoring

A presentation that exists only to participate in a cross-run relation should use `PAIR_ONLY` in the private blueprint rather than inventing an unnecessary single-case oracle.

Recommended relation families when defensible:

- semantic paraphrase preserving proposition/QUD;
- A/B candidate order swap;
- identity/prestige masking;
- verbosity normalization without evidence change;
- variable/symbol renaming;
- causal-graph isomorphism;
- independent-source vs duplicate-upstream provenance substitution;
- formally equivalent quantifier/logical normalization;
- presentation-format normalization;
- temporal-state renaming when transition semantics are preserved.

Do not call a transformation semantics-preserving merely because one LLM says so. Prefer formal rules, deterministic construction, reviewed templates, or independent validation.

## 5. Paired judge tests

For order/prestige/identity sensitivity, one execution is insufficient.

Minimum pair contract:

- execute all required presentations;
- map A/B surface labels back to stable underlying candidate IDs;
- freeze the complete response set;
- compare underlying verdicts rather than surface positions;
- record ties/abstentions;
- fail the invariance claim if underlying winner flips without evidence/content change.

This remains the required path for `J1-order-swap` and `J6-blind-label-invariance`.

## 6. Contamination metadata

Every receipt should report, even if unknown:

- authoring overlap;
- fixture visibility to generator;
- expected-label visibility;
- hidden-variant visibility;
- response freeze state;
- commit-reveal verification state;
- judge independence;
- runtime independence;
- host-live state.

Use `null/UNKNOWN`, not optimistic defaults, when provenance is not established.

## 7. Tamper / false-promotion regressions

Canonical GitHub-hosted workflow:

`.github/workflows/reasoning-eval-harness-gate.yml`

It must keep regression coverage for at least:

- private scoring keys absent from public manifest;
- salted reveal succeeds for matching oracle/salt;
- oracle mutation after commitment fails;
- response mutation after freeze fails at scoring;
- no verified reveal receipt -> no `PRIVATE_ORACLE_SCORED`;
- unrelated judgment artifact -> no `INDEPENDENT_JUDGED`;
- missing paired presentation -> pair `UNSCORED` and no `PERTURBED_HIDDEN`;
- public non-hidden fixture remains capped at `SAME_MODEL_SMOKE`.

These synthetic/contract tests validate the harness, not target-model reasoning.

## 8. Holdout quality

A hidden set can still be poor. Audit:

- construct validity;
- label correctness;
- relation validity;
- difficulty diversity;
- domain/style diversity;
- duplicate templates;
- proxy gaming opportunities;
- hidden-variant meaningfulness after normalization.

`HIDDEN != HIGH_QUALITY`.

A salted commitment proves precommitment consistency, not oracle quality.

## 9. Research signal

2026 evaluation work increasingly emphasizes stronger separation and dynamic generation rather than trusting a fixed public benchmark or contamination detector alone. BeyondBench uses procedural/on-the-fly generation; logic-grounded metamorphic testing uses relation-preserving cross-input checks; contamination-detection research shows detectors can be fragile; and Google DeepMind's 2026 double-blind AI-evaluation pilot strengthens evaluator/model-development separation.

Design implication: treat evaluation information itself as privileged state, bind it cryptographically when useful, freeze target outputs before reveal, and distinguish harness integrity from model capability.

Relevant public references:

- Google DeepMind, 2026-08-27 — double-blind AI evaluation pilot.
- ICLR 2026 BeyondBench — contamination-resistant algorithmic problem generation.
- 2026 LGMT — logic-grounded metamorphic reasoning evaluation.
- ICLR 2026 Fragility of Benchmark Contamination Detection.
- 2026 reward-hacking survey — hidden/dynamic/adversarial/metamorphic evaluator defenses.
