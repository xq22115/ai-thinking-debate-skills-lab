---
name: evidence-gap-research
description: Identify the minimum evidence needed to accept, reject, bound, or leave unresolved important claims; track evidence sufficiency, source dependence, contradictions, belief updates, and the highest-value next test. Use for research, diagnosis, verification, high-stakes decisions, and any task where unsupported confidence would be costly.
---

# Evidence Gap Research

Version: `0.2.0-rc1`

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Objective

Convert a vague research task into a claim-evidence program that updates beliefs proportionally to evidence and stops when additional search/reasoning no longer has decision value.

Do not treat search volume, citation count, confidence, or repeated restatement as proof.

## Core Workflow

1. Restate the decision or deliverable in testable terms.
2. Enumerate the material claims that must be true for success.
3. Classify each claim as `FACT`, `INFERENCE`, `ASSUMPTION`, or `UNKNOWN`.
4. Normalize scope, time, quantifiers, definitions, and target environment before comparing evidence.
5. For each non-trivial claim, record the strongest available support and strongest plausible contradiction.
6. Classify evidence sufficiency as `FULL_SUPPORT`, `PARTIAL_SUPPORT`, `IRRELEVANT_OR_NON_DIAGNOSTIC`, `ABSENT`, or `CONFLICTING`.
7. Trace source provenance/dependence when multiple sources may share one upstream origin.
8. Update the claim state only when new evidence creates a material evidence delta.
9. If unresolved, identify the highest-value discriminating test/search by expected decision value.
10. Stop when critical claims are supported/rejected/bounded/explicitly unresolved and further information has low expected decision value.

## Claim Ledger

For each decision-critical claim maintain, when useful:

- normalized claim;
- type: fact / inference / assumption / unknown;
- current state: `SUPPORTED / LEAN_SUPPORTED / UNRESOLVED / LEAN_REJECTED / REJECTED`;
- evidence sufficiency state;
- strongest support;
- strongest contradiction;
- source provenance / independence;
- freshness/version/target applicability;
- evidence delta since the previous state;
- current crux;
- decisive missing evidence or test;
- whether the remaining uncertainty can change the decision.

## Evidence Quality and Independence

Prefer evidence that is:

- direct or reproducible;
- bound to the actual target/version/environment when relevant;
- primary or close to the underlying observation;
- independently corroborated;
- discriminating between live hypotheses;
- current enough for the claim's stability class.

Do not count repeated downstream reports of one upstream source as independent corroboration.

`SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`

When source dependence is material, consult `EPISTEMIC_CALIBRATION.md` and construct a compact provenance graph.

## Evidence Sufficiency / Abstention Gate

Before presenting a claim as settled:

- `FULL_SUPPORT`: answer the supported conclusion with normal qualifications.
- `PARTIAL_SUPPORT`: answer only the bounded/weaker conclusion and name the unresolved gap.
- `IRRELEVANT_OR_NON_DIAGNOSTIC`: do not treat topical relevance as support.
- `ABSENT`: do not convert model memory or plausibility into external verification.
- `CONFLICTING`: expose the conflict and adjudicate source quality/dependence if possible; otherwise remain unresolved.

A model that notices conflict but still picks a side without a discriminating basis has not closed the evidence gap.

## Belief Update Rule

A material confidence/state change must identify its evidence delta.

Use Bayesian-style comparative discipline when helpful:

- what was plausible before the new evidence?;
- how expected is the evidence under each serious hypothesis?;
- is the evidence genuinely independent?;
- does it discriminate between the hypotheses?;
- what contradiction or defeater does it add/remove?;

Use numeric probabilities only when defensible inputs exist. Otherwise use ordered qualitative states and directional updates.

`MORE_REASONING != MORE_EVIDENCE`

## Contradiction Handling

When sources disagree:

1. normalize whether the claims actually conflict after accounting for scope/time/definition;
2. compare source reliability and distance from primary evidence;
3. trace shared upstream sources;
4. identify whether the disagreement is factual, inferential, normative, or measurement-based;
5. find the smallest discriminating fact/test that could resolve the conflict;
6. remain unresolved when no justified adjudication is available.

Do not hide contradictions in a prose synthesis.

## Expected Value of Information

When a critical uncertainty remains, rank candidate next actions by:

- decision sensitivity;
- hypothesis discrimination;
- probability of obtaining usable evidence;
- consequence of a wrong decision;
- time/compute/money/risk cost.

Prefer a single high-value test over many redundant searches.

Use precise expected-value numbers only when inputs justify them; otherwise use a qualitative ranking.

## Stop Rule

Stop research/deliberation when:

- acceptance criteria are directly verified;
- residual uncertainty cannot change the decision;
- the best available next tests have low expected information value;
- new searches repeatedly return dependent/redundant evidence;
- decisive evidence is unavailable and the correct state is explicitly `UNRESOLVED`;
- execution or measurement now has higher information value than further discussion.

Do not equate a larger reasoning budget with better calibration.

## Interaction with Other Skills

Use:

- `semantic-argument-microscope` when wording, warrants, QUD, argument scheme, or causal interpretation is contested;
- `competing-hypotheses` when multiple explanations remain live;
- `multi-agent-deliberation` only when genuinely different evidence/method roles add value;
- `completion-gate` before claiming verified/deployed/healthy status.

For detailed evidence calibration, source dependence, Bayesian-style updates, evidence sufficiency, VOI, and stop rules, consult `EPISTEMIC_CALIBRATION.md`.

## Output Contract

Return a compact, auditable result containing:

- claim ledger;
- evidence sufficiency per critical claim;
- strongest support and contradiction;
- source provenance/dependence notes where material;
- unresolved contradictions;
- belief updates with evidence deltas;
- highest-value missing test/search;
- stop/continue rationale;
- calibrated conclusion, including an explicit unresolved state when appropriate.

## Failure Modes

- search-volume-as-proof;
- citation-count-as-independence;
- selecting one side of conflicting evidence without adjudication;
- converting partial support into a stronger claim;
- confidence inflation after restating the same evidence;
- inventing numeric priors/likelihoods;
- continuing research after marginal information gain collapses;
- treating model memory as external verification;
- hiding contradictory evidence in a smooth synthesis;
- confusing relevance with reliability or diagnosticity.

## Evaluation

Primary regression spec:

`skills/evals/epistemic-calibration-fixtures.json` — E1–E12.

Fixture presence is not target-model execution evidence. Sequential belief-update evaluation, evidence-sufficiency/abstention evaluation, VOI action selection, independent judging, and host-live regression remain separate gates.

## Research Signal

Recent 2025–2026 research reports persistent failures in LLM confidence calibration, abstention under insufficient/conflicting evidence, sequential Bayesian belief updating, and multi-source evidence reconciliation. It also shows that additional reasoning or more elaborate confidence estimation does not uniformly improve calibration. These findings motivate explicit evidence-state and information-value tracking rather than decorative confidence scores.

## Completion Gate

Never say `verified` when a critical claim lacks evidence bound to the actual target environment, and never turn an unresolved evidence conflict into a definitive conclusion merely because the system is expected to answer.
