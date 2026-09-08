# Argument Schemes & Decision-Critical Questions

Status: `EXPERIMENTAL REFERENCE / USE ON DEMAND`

Purpose: identify the *kind* of inferential bridge an argument uses, then ask the smallest number of critical questions most likely to change the conclusion. Do not generate a ritual checklist.

## General rule

1. Normalize the claim and current QUD.
2. Identify the best-fitting argument scheme(s). Multiple schemes may coexist.
3. Instantiate the scheme using the actual text/evidence.
4. Generate candidate critical questions.
5. Rank questions by **decision value**: likelihood of exposing a false premise, weak warrant, missing defeater, or unsupported claim-strength escalation.
6. Ask/test the top 1–3; stop when additional questions are unlikely to change the verdict.

A fluent question is not automatically a critical question. A valid critical question must target a live premise, warrant, evidence obligation, defeater, or inference dependency.

## Core scheme library

### 1. Expert / authority opinion

Pattern:
`E is a credible expert in domain D; E asserts A; therefore A is supported.`

High-value critical questions:
- Is E actually expert in the domain relevant to A?
- Is the cited statement represented accurately and in context?
- Is E independent/reliable for this claim?
- Do relevant peer experts materially disagree?
- What primary evidence supports E's conclusion?

Failure mode: attacking the person when the underlying evidence independently supports the claim, or accepting prestige without domain fit.

### 2. Causal inference

Pattern:
`X occurred/varied; Y followed/varied; therefore X caused or materially contributed to Y.`

High-value critical questions:
- Is temporal order correct?
- What plausible confounders or common causes exist?
- Is there a mechanism connecting X to Y?
- Does changing X predictably change Y under comparable conditions?
- Are selection effects, regression to the mean, or measurement changes plausible?

Failure mode: treating correlation, sequence, or one anecdote as sufficient causation.

### 3. Analogy

Pattern:
`A and B share relevant properties; a conclusion/rule holds for A; therefore it may hold for B.`

High-value critical questions:
- Which similarities are causally/relevantly connected to the conclusion?
- Which dissimilarities could break the transfer?
- Is there a closer comparison class?
- Does the analogy illuminate a mechanism or merely evoke emotion?

Failure mode: surface resemblance or emotional similarity without structural relevance.

### 4. Consequences / practical reasoning

Pattern:
`Action P is expected to cause outcomes O; O is desirable/undesirable; therefore P should/should not be done.`

High-value critical questions:
- How likely and how large are the predicted consequences?
- What alternatives achieve the same benefit with lower cost?
- What second-order effects or distributional impacts matter?
- What values/tradeoffs convert the forecast into the normative conclusion?
- What evidence would make the recommendation reverse?

Failure mode: hiding a value judgment inside an empirical forecast or ignoring alternatives.

### 5. Sign / indicator

Pattern:
`Observation S is normally associated with state A; S is observed; therefore A is more likely.`

High-value critical questions:
- What is the base rate of A?
- How specific/sensitive is S for A?
- What alternative states also produce S?
- Is the measurement reliable in this context?

Failure mode: treating an indicator as proof rather than evidence with false positives/negatives.

### 6. Example / precedent

Pattern:
`Case C illustrates a rule/pattern; therefore the broader claim is supported.`

High-value critical questions:
- Is C representative or cherry-picked?
- What is the relevant comparison class?
- Are there counterexamples of similar evidentiary weight?
- Is the inference universal, typical, or merely existential?

Failure mode: using one vivid case to justify a population-level claim.

### 7. Popular opinion / consensus

Pattern:
`Many relevant people believe A; therefore A receives some support.`

High-value critical questions:
- Is this group epistemically relevant and independently informed?
- Could shared incentives, copied sources, or social conformity explain agreement?
- Is there direct evidence stronger than the consensus signal?
- Does the claim concern facts, norms, or preferences?

Failure mode: consensus counted as independent evidence when participants share one source or incentive.

### 8. Definition / classification

Pattern:
`Object X satisfies criteria C for category K; therefore X is K and inherits consequences/rules attached to K.`

High-value critical questions:
- Are the criteria explicit and applied consistently?
- Is the category boundary contested or context-sensitive?
- Does the conclusion depend on the label or on underlying properties?
- Has the definition changed during the debate?

Failure mode: definition laundering—winning by silently redefining the category.

### 9. Rule / principle application

Pattern:
`General principle R applies to conditions C; C holds here; therefore conclusion A follows.`

High-value critical questions:
- What is the exact scope and qualifier of R?
- Are there exceptions/defeaters?
- Does the current case actually satisfy C?
- Is R applied consistently to structurally similar cases?

Failure mode: treating a defeasible rule as exceptionless or using a counterexample outside its scope.

### 10. Burden-based / absence-of-evidence move

Pattern:
`A has not been established/refuted under the relevant burden; therefore the decision state remains/not-A is adopted for this procedure.`

High-value critical questions:
- Who actually bears which burden under this decision context?
- What standard is required: plausibility, preponderance, high confidence, proof beyond reasonable doubt, etc.?
- Is absence of evidence expected if A were true?
- Is the speaker converting 'not proven' into 'proven false'?

Failure mode: illicit burden shifting or confusing procedural non-establishment with factual falsity.

## Critical-question ranking

Score candidate questions qualitatively on:

- **crux proximity** — does answering it change the main conclusion?
- **discrimination** — does it separate competing hypotheses?
- **evidence accessibility** — can it be answered with available/obtainable evidence?
- **scope** — does it test the actual claim rather than a neighboring issue?
- **non-redundancy** — is it materially new?

Prefer one decisive question over ten decorative objections.

## Steelman before attack

Before evaluating a consequential argument:

1. state the strongest interpretation that remains faithful to the speaker's words/context;
2. distinguish charitable reconstruction from adding premises the speaker never licensed;
3. attack the strongest faithful version;
4. if the conclusion survives, increase confidence; if only a weak straw version fails, do not claim the original is defeated.

`STEELMAN != INVENT_A_BETTER_ARGUMENT_FOR_THE_SPEAKER`.

## Research signal

Argument-scheme classification and Critical Questions Generation remain active research problems. 2025 ArgMining work reports that scheme-guided methods are useful, while the shared task's best accuracy still left substantial room for improvement. Therefore scheme detection and critical-question usefulness must remain evaluation-gated rather than assumed correct.
