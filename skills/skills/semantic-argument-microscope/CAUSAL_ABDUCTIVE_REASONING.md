# Causal & Abductive Reasoning Reference

Status: `EXPERIMENTAL REFERENCE / USE ON DEMAND`

Purpose: distinguish association, intervention, counterfactual reasoning, and abductive explanation before accepting a causal story. Use when the live crux is `why did this happen?`, `what caused it?`, `what would happen if we changed X?`, or `what would have happened otherwise?`.

## Causal ladder

Keep three levels distinct:

1. **Association / observation** — what variables/events co-occur or predict each other?
2. **Intervention** — what would happen to Y if we actively set/change X while breaking X's ordinary causes?
3. **Counterfactual** — for this same case/unit, what would Y have been if X had been different while relevant background facts were held according to the causal model?

Do not infer a higher level from a lower one without a causal bridge.

`P(Y|X) != P(Y|do(X))`

## Causal graph first

For material causal questions, build the smallest useful directed graph before telling a story.

Represent candidate edges as hypotheses, not facts, until supported:

`A -> B`

Track at least:

- candidate direct causes;
- shared causes/confounders;
- mediators;
- possible reverse-causation paths;
- selection variables;
- alternative mechanisms;
- outcome measurement changes.

Prefer global graph coherence over exhaustively judging isolated pairwise relations. Local plausibility can create a globally inconsistent causal story.

## Core causal checks

### 1. Temporal order
A cause generally must be able to precede its effect in the relevant mechanism.

But `earlier -> later` alone does not prove causation.

### 2. Confounding
Ask whether C plausibly causes both X and Y:

`C -> X`
`C -> Y`

If yes, X-Y association may not represent the causal effect of X.

### 3. Reverse causation
Check whether the outcome or an upstream precursor could influence the alleged cause:

`Y -> X`

### 4. Mediation
If X affects Y through M:

`X -> M -> Y`

do not casually treat M as an independent competing cause or control it away without considering the estimand.

### 5. Collider / selection warning
If X and Y both influence S:

`X -> S <- Y`

conditioning/selecting on S can create a misleading association. Do not mechanically `control for everything`.

### 6. Measurement shift
An apparent causal change can be produced by changed definitions, reporting, instrumentation, thresholds, or data collection.

## Abductive reasoning: best explanation, not first explanation

Abduction asks which hypothesis best explains observed evidence.

For each plausible causal explanation H, record:

- mechanism;
- evidence H predicts;
- evidence that would be surprising under H;
- alternative hypotheses that predict the same observation;
- direct vs background cause distinction;
- discriminating evidence/test;
- current confidence state.

Generate multiple **causally different** explanations, not paraphrases.

Do not select H merely because it is vivid, familiar, morally satisfying, or narratively coherent.

## Direct cause vs background condition

When explaining an event, distinguish:

- **direct/proximate cause** — a near mechanism producing the target event;
- **enabling/background condition** — necessary or influential context that does not itself identify the direct mechanism;
- **trigger** — an event that initiates a mechanism;
- **common cause** — explains both alleged cause and outcome;
- **correlated distractor** — semantically related but causally irrelevant.

This distinction is critical for real-world event reasoning where many facts are true but only some explain the target transition.

## Intervention test

Ask:

`If we actively changed X while holding the causal structure otherwise appropriate, should Y change?`

A useful intervention proposal must specify:

- intervention target;
- what downstream variables may change;
- what upstream causes are cut/held outside the intervention;
- relevant time horizon;
- possible spillovers/side effects.

Do not treat observational adjustment as equivalent to a real intervention without justification.

## Counterfactual protocol

For a counterfactual question:

1. **Abduction:** infer relevant latent/background state from what actually happened.
2. **Action/intervention:** replace the structural assignment for the counterfactual variable.
3. **Prediction:** propagate consequences through the causal graph.
4. Keep unrelated facts fixed only when the causal model licenses them to remain fixed.
5. Backtrack if the hypothetical creates structural inconsistency.

Do not answer counterfactuals by simply swapping one sentence token while leaving all causally downstream facts unchanged.

## Causal evidence ladder

Evidence strength is context dependent, but useful distinctions include:

- raw co-occurrence / anecdote;
- temporal sequence;
- repeated observational association with measured confounder handling;
- natural experiment / quasi-experimental variation;
- randomized intervention where feasible and applicable;
- mechanism evidence;
- converging evidence from causally distinct methods.

Never mechanically equate one method label with truth. Examine design, assumptions, measurement, applicability, and threats to identification.

## Causal crux questions

High-value questions often include:

- What alternative cause would generate the same observation?
- What evidence distinguishes X-causes-Y from Y-causes-X?
- What shared cause could explain both?
- What intervention on X would change Y if the story were true?
- What counterfactual prediction does this mechanism uniquely make?
- What measurement/selection change could mimic the effect?
- Which node/edge, if removed, collapses the causal explanation?

## Anti-storytelling gate

A causal explanation counts as progress only if it changes at least one of:

- graph structure;
- predicted observation;
- discriminating test;
- intervention expectation;
- counterfactual expectation;
- confidence based on new evidence.

A longer narrative with the same unsupported edge is not deeper reasoning.

## Interaction with argument analysis

When a causal claim appears in debate:

`literal claim -> causal scheme -> candidate graph -> confounder/reverse/selection checks -> competing causal hypotheses -> intervention/counterfactual test -> evidence update`

The rhetorical force of a causal story is scored separately from causal identification.

## Research signal

Recent benchmark work continues to find counterfactual and complex causal reasoning difficult for LLMs, especially under unfamiliar rules, multi-path graphs, and fresh contexts. Causal-graph structure and explicit intervention/counterfactual procedures can improve reasoning, but they do not guarantee correct causal discovery. Use this reference as an evaluation scaffold, not proof that the model has learned causal inference.
