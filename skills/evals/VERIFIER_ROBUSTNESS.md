# Verifier Robustness & Metamorphic Evaluation

Status: `EXPERIMENTAL EVALUATION REFERENCE`

Purpose: prevent reasoning quality from being inferred from a single brittle judge, visible benchmark, or proxy reward. Use deterministic checks where semantics permit; otherwise test evaluator robustness under perturbation, judge replacement, hidden variants, and evidence-preserving transformations.

## Core invariants

- `VERIFIER_PASS != TASK_TRUTH`
- `ONE_JUDGE_AGREES != ROBUST_VALIDATION`
- `VISIBLE_TEST_PASS != GENERALIZATION`
- `REFERENCE_MATCH != REASONING_CORRECTNESS`
- `PROCESS_SCORE != FAITHFUL_REASONING`
- `STYLE_INVARIANCE_FAILURE = VERIFIER_WARNING`
- `SEMANTICALLY_EQUIVALENT_INPUTS SHOULD NOT CAUSE MATERIAL VERDICT FLIPS`
- `AGENT_WRITABLE_TESTS != TRUSTED_VERIFICATION`

## 1. Verification hierarchy

Prefer the strongest available check that directly corresponds to the claim:

1. deterministic exact rule / parser / type / schema check;
2. executable test or measurement bound to the target;
3. deterministic process constraint when domain rules are explicit;
4. reference/gold comparison with semantic normalization;
5. independent model judge with rubric and blind labels;
6. same-model/fresh-context judge only as a lower-grade signal;
7. self-rating by the generating model only as diagnostic metadata.

Never use a weaker verifier when a cheap stronger verifier is available.

## 2. Outcome vs process verification

Outcome verification asks whether the final result satisfies an external criterion.

Process verification asks whether intermediate observable decisions follow required rules or constraints.

Use process verification when:
- the final outcome can be accidentally correct despite invalid reasoning;
- intermediate domain rules are programmatically checkable;
- an invalid shortcut could pass the outcome test;
- provenance or evidence obligations must be preserved.

Do not require hidden chain-of-thought. Verify **observable intermediate artifacts**: claims, evidence links, state transitions, calculations, causal graph edges, tool receipts, or declared decision rules.

## 3. Deterministic-when-possible rule

If a claim can be checked by deterministic logic, do not outsource the final verdict entirely to an LLM judge.

Examples:
- JSON/schema validity;
- arithmetic/invariant checks;
- graph acyclicity under an acyclic contract;
- contradiction in mutually exclusive state labels;
- whether a claimed file/commit/receipt actually exists;
- whether a confidence update names a new evidence delta.

A neural judge may explain a failure, but the deterministic check owns the binary invariant when applicable.

## 4. Metamorphic testing

When a direct oracle is incomplete or expensive, generate transformed cases whose expected relationship to the original answer is known.

Useful metamorphic relations include:

### Semantic-preserving paraphrase
Change wording while preserving proposition/QUD.
Expected: same material verdict and evidence obligations.

### Candidate-order permutation
Swap A/B or evidence presentation order.
Expected: ranking should remain stable absent content changes.

### Prestige/identity masking
Remove model/source/role prestige metadata while preserving evidence.
Expected: epistemic ranking should not materially change.

### Verbosity normalization
Compress or expand style without changing claims/evidence.
Expected: evidence score should remain stable.

### Quantifier-preserving rewrite
Rewrite `not all` / `some not` or logically equivalent scope forms where valid.
Expected: normalized claim remains equivalent.

### Causal-graph isomorphism
Rename graph variables while preserving graph topology and stated mechanisms.
Expected: causal conclusion should depend on structure, not familiar labels.

### Counterfactual symmetry / controlled intervention variant
Change only the intervention specified by the model and propagate downstream according to the same structural rules.
Expected: changes follow the graph rather than lexical association.

### Evidence-provenance duplication
Duplicate the same upstream evidence through multiple derivative documents.
Expected: independent evidence weight should not increase.

Metamorphic testing detects brittleness even when no single gold answer can fully score the reasoning.

## 5. Evaluator-swap test

A material conclusion should not depend on one evaluator's quirks.

When consequence/cost justifies it:

1. evaluate with the primary judge;
2. hide presentation metadata and re-evaluate;
3. use a second rubric-compatible evaluator or deterministic subchecks;
4. compare decisive evidence/crux, not only scalar score;
5. flag material verdict changes without content/evidence changes.

`EVALUATOR_DEPENDENT_SUCCESS` is a reward/verifier-gaming warning.

## 6. Reference-based verifier limits

A reference answer is useful but incomplete when:
- multiple answers are valid;
- equivalent formulations differ lexically;
- the reference itself omits necessary reasoning;
- the task tests a process, not only a final string;
- an incorrect path can land on the correct final answer by chance.

Therefore compare normalized semantic claims and observable obligations, not raw string identity alone.

## 7. Reward / verifier hacking threat model

Watch for:

- verbosity optimized for judge preference;
- sycophantic wording optimized for evaluator agreement;
- hard-coding visible test cases;
- exploiting parser/format quirks;
- answer leakage from reference/gold fields;
- benchmark-specific shortcuts;
- changing or suppressing tests/logs/receipts;
- optimizing intermediate process scores without preserving final correctness;
- producing superficially valid reasoning that violates the intended rule under perturbed variants.

For agentic systems, tests, reward channels, evaluation rubrics, hidden cases, and audit logs should be treated as privileged verification assets when the runtime permits separation.

## 8. Unseen/adversarial split

Keep authored development fixtures separate from evaluation variants.

Recommended split:
- `DEV_VISIBLE` — explicit fixtures used to design rules;
- `PERTURBED_HIDDEN` — metamorphic variants not visible during rule authoring;
- `UNSEEN_ADVERSARIAL` — independently generated edge cases;
- `CROSS_DOMAIN` — same reasoning invariant in a different surface domain;
- `HOST_LIVE` — intended runtime behavior with real tools/receipts.

Do not promote a skill from visible-fixture success alone.

## 9. Verifier disagreement protocol

If deterministic checks, reference verifier, and model judge disagree:

1. preserve all verdicts;
2. identify which exact claim each verifier evaluates;
3. inspect scope/reference ambiguity;
4. prefer target-bound deterministic evidence for invariants it directly owns;
5. use an independent adjudicator for residual semantic disputes;
6. leave unresolved if no verifier has a decisive basis.

Do not average incompatible verifier scores into false certainty.

## 10. Research signal

2026 verifier research reports three recurring themes:

- deterministic/verifiable process checks can improve rule adherence when the domain exposes checkable intermediate constraints;
- reference-based and learned verifiers still have substantial errors, structure sensitivity, and cross-domain limitations;
- reward/verifier hacking is a system-level risk, so evaluation requires hidden variants, evaluator separation, and privileged verification assets rather than a single proxy score.

These findings justify layered verification, not the claim that deterministic or process verification solves general reasoning evaluation.