# Epistemic Calibration & Evidence Sufficiency

Status: `EXPERIMENTAL REFERENCE / USE ON DEMAND`

Purpose: update beliefs in proportion to evidence quality, source independence, and diagnostic value; recognize when evidence is insufficient or conflicting; choose the next information-gathering action by expected decision value; stop when further reasoning/search is unlikely to change the decision.

## Core invariants

- `CONFIDENCE != EVIDENCE`
- `SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`
- `REPETITION != CORROBORATION`
- `PLAUSIBILITY != PROBABILITY`
- `PREDICTION_CONFIDENCE != LATENT_STATE_CONFIDENCE`
- `CONFLICTING_EVIDENCE != LICENSE_TO_PICK_ONE_SIDE`
- `MORE_REASONING != BETTER_CALIBRATION`
- `LOW_INFORMATION_GAIN != KEEP_SEARCHING`

## 1. Belief state, not confidence decoration

For each decision-critical claim H, maintain an auditable belief state:

- current claim state: `SUPPORTED / LEAN_SUPPORTED / UNRESOLVED / LEAN_REJECTED / REJECTED`;
- prior basis: what was known before the newest evidence;
- evidence delta: what new observation/source/test arrived;
- direction of update: raises, lowers, or leaves H materially unchanged;
- diagnosticity: how differently would this evidence be expected under H versus serious alternatives?;
- source dependence: is this genuinely new evidence or a restatement/derivative of an existing source?;
- unresolved contradictions;
- next discriminating test if the decision still turns on H.

Use numeric probabilities only when the underlying inputs justify them. Otherwise use ordered qualitative states. Do not fabricate priors or likelihood ratios merely to appear Bayesian.

## 2. Bayesian discipline without fake precision

The key update idea is comparative:

`posterior odds = prior odds × likelihood ratio`

For evidence E and hypotheses H1/H2, ask:

- How expected is E if H1 is true?
- How expected is E if H2 is true?
- Does E actually distinguish them?

Evidence that is equally likely under both hypotheses has low discriminating value even if it is vivid or relevant.

When numerical likelihoods are unavailable, use qualitative likelihood-ratio labels such as:

- `STRONGLY_FAVORS_H1`
- `MODERATELY_FAVORS_H1`
- `WEAKLY_FAVORS_H1`
- `NON_DIAGNOSTIC`
- symmetric H2 states.

A confidence change must point to the evidence delta that caused it.

## 3. Sequential evidence accumulation

When evidence arrives over multiple turns, update the same claim ledger instead of restarting from scratch.

For each new item:

1. identify the claim/hypothesis it bears on;
2. test whether it is independent of earlier evidence;
3. assess diagnosticity relative to live alternatives;
4. check whether it creates or resolves a contradiction;
5. revise the belief state;
6. record the reason for revision;
7. recompute the best next test only if the decision remains unresolved.

Do not let earlier confident wording anchor later updates.

## 4. Source-dependence and provenance graph

Multiple documents are not independent merely because they have different URLs, authors, or outlets.

Track provenance when material:

`upstream source -> derivative reports -> retrieved passages -> claim`

Possible relationships:

- `INDEPENDENT_OBSERVATION`
- `DERIVED_FROM`
- `QUOTES_SAME_PRIMARY_SOURCE`
- `SHARES_DATASET`
- `SHARES_MODEL_OR_PIPELINE`
- `UNKNOWN_DEPENDENCE`

Rules:

1. Ten summaries of one press release do not equal ten independent confirmations.
2. Independent replication, measurement, or primary-source confirmation deserves more weight than repetition.
3. When dependence is unknown and decision-critical, lower the corroboration claim rather than assuming independence.
4. Source prestige does not replace claim-level evidence quality.

## 5. Evidence sufficiency states

Before answering a claim as settled, classify available evidence:

- `FULL_SUPPORT` — evidence directly and adequately supports the requested conclusion under the relevant scope.
- `PARTIAL_SUPPORT` — evidence supports a bounded/weaker conclusion but leaves material gaps.
- `IRRELEVANT_OR_NON_DIAGNOSTIC` — information is related but does not resolve the claim.
- `ABSENT` — required evidence is missing.
- `CONFLICTING` — credible evidence supports incompatible live conclusions or key premises.

Response policy:

- Full support: answer with normal qualification.
- Partial support: answer only the supported bounded claim and name the gap.
- Irrelevant/absent: do not convert general plausibility or memory into external verification.
- Conflicting: expose the conflict, compare source quality/dependence, identify the crux, and remain unresolved when the conflict cannot be adjudicated.

`CONFLICT_AWARE_ANSWERING` is not enough if the decisive conflict remains unresolved.

## 6. Contradiction ledger

Maintain a compact contradiction graph for material disputes:

- claim A;
- claim B;
- whether they are truly incompatible after normalizing definitions/scope/time;
- evidence for each;
- source dependence and freshness;
- whether one is a stronger/weaker quantifier rather than a direct contradiction;
- resolving test or missing fact.

Do not force reconciliation by silently changing definitions, time ranges, populations, or modalities.

## 7. Expected Value of Information (VOI)

When uncertainty remains, do not automatically search more. Choose the next action by expected decision value.

A qualitative VOI estimate asks:

- **decision sensitivity:** could the result change the decision/verdict?
- **discrimination:** does it separate live hypotheses?
- **success probability:** is the test/search likely to produce usable evidence?
- **consequence:** how costly is choosing wrongly without the information?
- **cost:** time, compute, money, delay, complexity, or risk of the information action.

A practical qualitative rule:

`VOI ≈ probability information changes decision × value of improved decision − information cost`

Use precise numbers only when supported.

Prefer one high-VOI discriminating test over many low-value searches.

## 8. Stop rule / reasoning budget

Stop additional research or deliberation when one of these holds:

- acceptance criteria are directly verified;
- remaining uncertainty would not change the decision;
- available next tests have low expected information value;
- new searches repeatedly return dependent/redundant evidence;
- the claim should remain unresolved because decisive evidence is unavailable;
- execution/measurement now dominates further discussion in information value.

Do not continue merely because a larger reasoning budget exists. More tokens, more agents, or more sources can worsen calibration or create false confidence when they add no independent evidence.

## 9. Calibration checks

When confidence matters across repeated tasks, distinguish:

- **accuracy/discrimination:** can the system separate likely-correct from likely-wrong cases?;
- **calibration:** among claims expressed at a confidence level, how often are they actually correct?;
- **evidence sufficiency calibration:** does the system answer more definitively only as evidence becomes sufficient?;
- **selective accuracy / abstention quality:** does withholding a definitive answer improve correctness on answered cases without excessive useless abstention?

No single confidence estimator should be assumed best across all task classes.

## 10. Multi-answer and semantic-equivalence warning

Surface disagreement among sampled answers can overstate uncertainty when multiple formulations or multiple answers are genuinely valid.

Before using sample consistency as confidence:

- cluster semantically equivalent answers;
- determine whether the task allows multiple valid answers;
- separate answer diversity from substantive hypothesis diversity.

`STRING_DISAGREEMENT != EPISTEMIC_DISAGREEMENT`.

## 11. Interaction with the reasoning stack

Recommended flow when evidence confidence is decision-critical:

`claim normalization -> evidence sufficiency -> provenance/dependence graph -> competing hypotheses -> likelihood/diagnosticity update -> contradiction ledger -> discriminating test -> VOI decision -> calibrated answer or unresolved state`

For causal questions, combine with `CAUSAL_ABDUCTIVE_REASONING.md` before interpreting observational evidence as a likelihood update about causal effects.

For multi-agent disputes, combine with the bias-resistant judge and minority audit in `multi-agent-deliberation`.

## Research signal

Recent 2025–2026 work reports persistent gaps in LLM calibration, abstention, sequential Bayesian belief updating, and evidence conflict handling. Results also indicate that more reasoning or more elaborate confidence estimators do not uniformly improve calibration, and that multi-source evidence requires explicit handling of reliability and conflicts. Treat this reference as an evaluation scaffold, not proof that a model is Bayesian or calibrated.
