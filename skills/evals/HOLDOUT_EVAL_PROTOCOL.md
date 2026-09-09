# Hidden Holdout / Fresh-Context Evaluation Protocol

Status: `EXPERIMENTAL EVAL INFRASTRUCTURE / NOT A MODEL RESULT`

Purpose: move reasoning evaluation beyond visible same-model smoke while preventing the evaluation harness itself from creating new leakage, false independence, or unverifiable promotion claims.

## Hard invariants

- `PUBLIC_FIXTURE_PASS != HIDDEN_GENERALIZATION`
- `FRESH_CONTEXT != PRIVATE_ORACLE`
- `PRIVATE_ORACLE != INDEPENDENT_MODEL_JUDGE`
- `PAIR_TEST_REQUIRES BOTH EXECUTIONS`
- `METAMORPHIC_CLAIM_REQUIRES RELATION_CHECK`
- `HIDDEN_LABELS IN PUBLIC REPO != HIDDEN_LABELS`
- `HASHED_ORACLE != VERIFIED_ORACLE_QUALITY`
- `CONTAMINATION_DETECTION_PASS != PROOF_OF_NO_CONTAMINATION`
- `MODEL_OUTPUT MUST BE FROZEN BEFORE PRIVATE SCORING`

## 1. Three-artifact separation

A holdout run should use three logically separate artifacts.

### A. Public generation manifest
Visible to the target generator. Contains only what is needed to run the case:

- run / suite ID;
- case ID;
- prompt/input;
- requested output schema;
- presentation metadata needed by the generator;
- no expected answer, `must_detect`, `fail_if`, gold label, pair winner, hidden relation outcome, or judge rubric that reveals the answer.

### B. Frozen target responses
Produced before any private oracle or judge output is exposed to the target path.

Each response should bind:

- run ID;
- case ID;
- target/model/runtime identity;
- output payload;
- response hash;
- execution receipt/reference when available.

Freeze this artifact before scoring.

### C. Private scoring artifact
Not visible to the target-generation path. May contain:

- expected exact values;
- required/forbidden labels;
- pair/metamorphic relations;
- deterministic gold rules;
- independent-judge rubric/results;
- hidden/adversarial variant metadata.

For a truly hidden holdout, this artifact MUST NOT be committed to the public repository before target responses are frozen. The public repository may store a SHA-256 commitment and later evaluation receipt.

## 2. What belongs in the public repo

Allowed:

- schemas;
- runner code;
- holdout-generation procedures;
- transformation families;
- blank templates;
- public seed fixtures explicitly marked non-hidden;
- oracle/manifest hashes after artifacts exist;
- final receipts after scoring, provided they do not leak future holdout answers intended for reuse.

Do not commit reusable private holdout expected labels or hidden variants to a public path and then call them hidden.

## 3. Evidence ladder

Do not collapse these levels:

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

`FRESH_CONTEXT_RUN` requires target execution without the authoring conversation/context and without expected labels visible to the generator.

`PRIVATE_ORACLE_SCORED` additionally requires target outputs frozen before scoring, a separated private oracle, an oracle hash/receipt, and deterministic private scoring for the claimed cases.

`INDEPENDENT_JUDGED` additionally requires an appropriately separated judge or gold process with its own identity/receipt. A target model grading itself in the same context does not satisfy this level.

`PERTURBED_HIDDEN` requires at least one relation-preserving variant hidden from the generator before execution and an actual cross-run relation check.

`UNSEEN_ADVERSARIAL` requires independently generated or procedurally generated adversarial cases not available to the target path before the run.

`REPEATED` requires repeated runs sufficient for the claimed variance/calibration statement; a single duplicate execution is not enough.

`AUTHENTIC_MULTI_AGENT_RUNTIME` requires observable runtime/session separation for claims of independent agents.

`HOST_LIVE_REGRESSION` requires target-host execution/read-back appropriate to the claimed host behavior.

## 4. Metamorphic holdout families

Use only transformations whose expected relation is defensible for the task.

Recommended families:

- semantic paraphrase preserving the proposition/QUD;
- A/B candidate order swap;
- identity/prestige masking;
- verbosity normalization without evidence change;
- variable/symbol renaming;
- causal-graph isomorphism;
- independent-source vs duplicate-upstream provenance substitution;
- equivalent quantifier/logical normalization where formally justified;
- presentation-format normalization;
- temporal state renaming when state-transition semantics are preserved.

Do not label a transformation semantics-preserving merely because an LLM says it is. Prefer formal rules, deterministic construction, human-reviewed templates, or independent validation where possible.

## 5. Paired judge tests

For order/prestige/identity sensitivity, one execution is insufficient.

Minimum pair contract:

- run both presentations;
- map A/B labels back to stable underlying candidate IDs before comparison;
- freeze both target outputs;
- compare the underlying verdict, not surface label;
- record ties/abstentions explicitly;
- fail the invariance claim if the underlying winner flips without evidence/content change.

This is the required execution path for the existing `J1-order-swap` and `J6-blind-label-invariance` gates.

## 6. Contamination metadata

Every receipt must report, even if unknown:

- authoring overlap;
- whether the base fixture was visible to the generator;
- whether expected labels were visible;
- whether the hidden variant was visible;
- whether the response artifact was frozen before scoring;
- judge independence;
- runtime independence;
- host-live state.

Use `null/UNKNOWN`, not optimistic defaults, when provenance is not established.

## 7. Result contract

Canonical result schema:

`skills/evals/reasoning-eval-result.schema.json`

Provider-neutral runner:

`skills/evals/run_reasoning_evals.py`

The runner does not call a model. It consumes already-produced response/judgment artifacts, applies deterministic private-oracle checks where possible, verifies paired relations, and computes the highest evidence class justified by supplied receipts/metadata.

This separation prevents the scoring harness from pretending it created fresh-context or independent runtime evidence.

## 8. Holdout quality

A hidden set can still be bad. Audit:

- construct validity;
- label correctness;
- relation validity;
- difficulty diversity;
- domain/style diversity;
- duplicated templates;
- proxy gaming opportunities;
- whether hidden variants remain meaningfully different after normalization.

`HIDDEN != HIGH_QUALITY`.

## 9. Research signal

2026 contamination-resistant reasoning work increasingly uses procedural/dynamic generation rather than relying only on static benchmark secrecy. Metamorphic testing likewise evaluates relation-preserving consistency and can reveal defects missed by isolated correctness tests. Research also shows contamination detection itself can be fragile, so this protocol treats separation and dynamic/hidden generation as evidence-producing design choices rather than assuming a detector can certify uncontaminated evaluation.

Relevant public research references:

- ICLR 2026 BeyondBench — contamination-resistant algorithmic problem generation.
- 2026 LGMT — logic-grounded metamorphic reasoning evaluation.
- ICLR 2026 Fragility of Benchmark Contamination Detection — contamination detection can be evaded/fragile.
- 2026 reward-hacking survey — hidden/dynamic/adversarial/metamorphic evaluations as defenses against visible evaluator optimization.
