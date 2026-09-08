# 07 — Deliberation Router Specification v1.3

## Objective

Select the smallest reasoning/deliberation topology that can materially change the decision, then choose an action that is robust to the remaining uncertainty. Route first by unresolved information need and decision consequence, not by task length, rhetoric, or requested agent count alone.

## 1. Inputs

- task risk: low / medium / high / critical
- uncertainty: low / medium / high
- reversibility: reversible / costly / irreversible
- evidence sufficiency: full / partial / irrelevant / absent / conflicting
- evidence dependence: independent / partially dependent / shared-upstream / unknown
- evidence conflict: none / moderate / severe
- wording/QUD ambiguity: none / material
- causal crux: no / yes
- distribution shift: none / suspected / material / unknown
- action loss asymmetry: low / moderate / high / catastrophic
- decision sensitivity: stable / threshold-sensitive / unknown
- domain breadth: narrow / cross-domain
- compatibility surface: single-host / multi-host
- security sensitivity: normal / elevated
- acceptance-test clarity: clear / ambiguous
- best available direct test: none / low-VOI / high-VOI
- best reversible probe/pilot: none / available

## 2. Pre-deliberation gates

### Gate A — direct evidence

If an authoritative, target-bound observation/test can directly settle the acceptance criterion, prefer it over debate.

### Gate B — epistemic sufficiency

Run `evidence-gap-research` when evidence is partial, absent, conflicting, dependent, stale, shifted, or target-unbound.

Before escalation, identify:
- current claim state;
- strongest support/contradiction;
- source dependence;
- unresolved crux;
- highest-value missing evidence;
- whether historical calibration is likely transferable.

### Gate C — semantic/argument normalization

Run `semantic-argument-microscope` when parties/models may be disagreeing about different definitions, scopes, QUDs, warrants, argument schemes, or pragmatic interpretations.

Do not spend multiple agents debating different questions unknowingly.

### Gate D — causal/abductive normalization

If the live crux is causal, explanatory, interventional, or counterfactual, use the causal/abductive reference before assigning debate roles.

Do not ask a council to vote on causation from raw correlation.

### Gate E — distribution-shift / action context

If the action is consequential, determine whether the evidence/calibration context differs materially from the target context.

When shift is suspected/material/unknown:
- downgrade claims of calibration transfer;
- seek target-bound evidence or a local validation probe;
- prefer reversible action when downside is large;
- do not treat historical performance as a deployment guarantee.

## 3. Default deliberation routing

### Tier 0 — deterministic / direct test
Use 1 execution or research path.

Use when:
- task is mechanical or directly measurable;
- acceptance test is explicit;
- authoritative evidence is unambiguous;
- another reasoning role has negligible expected information value.

### Tier 1 — independent alternatives
Use 2–4 genuinely different methods/review roles when a second path can change the decision.

Typical composition:
- primary hypothesis/method;
- independent alternative;
- evidence/test auditor;
- optional judge.

### Tier 2 — adversarial deliberation
Use 5–9 roles only when material uncertainty survives normalization.

Possible roles:
- 2–3 competing hypotheses;
- evidence/provenance auditor;
- red team;
- falsifier;
- domain specialist;
- causal/semantic specialist when relevant;
- shift/sensitivity auditor when action transfer is uncertain;
- integrator/judge.

### Tier 3 — extended council
Activate 10–18 specialists when the task is cross-domain, high-impact, or has multiple independent unknowns that can genuinely be investigated separately.

### Tier 4 — 30-role coverage pool
Use up to 30 roles only while each additional role has a distinct evidence/method/verification duty and positive marginal information gain.

Rule:
No role may exist solely to increase agent count.

## 4. Escalation triggers

Escalate one tier only if at least one material condition holds:

- two strong competing hypotheses remain after normalization;
- independent high-quality evidence conflicts;
- a red team exposes a live blocking flaw;
- causal graph alternatives remain observationally equivalent and require different tests;
- compatibility differs materially by OS/host/version;
- critical action lacks rollback or has high consequence;
- distribution shift is material and target-bound validation is missing;
- decision flips under plausible changes to key assumptions;
- acceptance criteria cannot yet be objectively tested;
- the strongest minority hypothesis predicts a different observable outcome;
- a new role has access to a genuinely distinct evidence channel or method.

## 5. De-escalation / stop triggers

Reduce or stop active deliberation when:

- a direct test/measurement now dominates discussion in expected information value;
- a reversible probe/pilot dominates another debate round;
- hypotheses converge on the same mechanism and remaining differences are non-material;
- new messages repeat evidence or arguments already represented;
- apparent source diversity resolves to one shared upstream source;
- authoritative target-bound evidence resolves the crux;
- residual uncertainty cannot change the action;
- the next available information action has lower expected value than its cost;
- the correct epistemic state is `UNRESOLVED` because decisive evidence is unavailable;
- a robust fallback is acceptable across all live hypotheses.

Do not continue merely to consume a reasoning budget.

## 6. Message policy

Always retain:
- new evidence with provenance;
- material contradiction;
- discriminating test;
- blocking risk;
- minority hypothesis with strong evidence;
- changed confidence **with evidence delta**;
- unresolved evidence obligation;
- causal graph or QUD change that materially alters the dispute;
- distribution-shift warning;
- threshold/sensitivity flip;
- reversibility or loss asymmetry that changes the action.

Drop/compress:
- repeated agreement;
- paraphrases;
- stylistic commentary;
- unsupported confidence;
- duplicated downstream citations from the same upstream source;
- critiques that add no new evidence, defeater, test, or action-relevant delta.

## 7. Judge policy

The judge ranks claims by:

1. reproducible direct evidence;
2. current primary/spec/vendor evidence where applicable;
3. independent corroboration after provenance de-duplication;
4. discriminating tests and falsifiability;
5. coherent inference with calibrated uncertainty;
6. popularity/majority only as a weak social signal.

For material judgments, apply relevant bias checks from `multi-agent-deliberation`: blind labels, independent first score, order swap, verbosity normalization, evidence-only pass, minority audit, fresh-context judge separation.

`VOTE_COUNT != EVIDENCE_WEIGHT`

## 8. Value-of-information routing

Before another debate/search round, ask:

- Could the new information change the verdict or action?
- Does it distinguish live hypotheses?
- Is it likely to be obtainable/reliable?
- What is the consequence of remaining wrong?
- What is the cost of obtaining it, including delay?

Prefer the action with the highest expected decision value, not the action that looks most intellectually elaborate.

## 9. Decision robustness routing

When an action is required, separate `belief ranking` from `action ranking`.

Evaluate:
- asymmetric losses / impact radius;
- reversibility / rollback;
- distribution-shift status;
- sensitivity / threshold flip point;
- expected vs worst-case regret where useful;
- whether an `OTHER / MODEL_MISSPECIFICATION` branch remains plausible;
- whether a cheap probe/pilot can lower uncertainty before commitment.

Allowed action classes:
- `COMMIT`
- `PROBE`
- `PILOT`
- `DEFER`
- `ABSTAIN_ESCALATE`
- `ROBUST_FALLBACK`

Rules:
- `MOST_LIKELY_STATE != BEST_ACTION`.
- An irreversible action generally requires stronger decision evidence than a reversible probe.
- Historical calibration does not transfer automatically under distribution shift.
- A threshold-sensitive recommendation must be reported as fragile rather than robust.
- `UNRESOLVED` does not imply no action; probe/pilot/fallback may be justified.

## 10. Termination

Deliberation stops when one of these holds:

- acceptance evidence is complete;
- remaining hypotheses are non-material to the decision;
- expected value of another round is lower than cost;
- a hard blocker is target-bound and documented;
- execution/eval/probe is now more informative than further discussion;
- evidence is genuinely insufficient/conflicting and the correct output is an explicit unresolved state;
- a robust action is acceptable across the live uncertainty set.

Consensus alone is not a termination condition if material evidence obligations remain open.

## 11. Anti-patterns

- 30 homogeneous clones.
- Majority vote without provenance.
- Endless critique with no discriminating test.
- One agent writes the answer and 29 agents merely approve it.
- Treating verbosity as depth.
- Treating hidden chain-of-thought length as a quality metric.
- Escalating before normalizing QUD/definitions.
- Debating causation before separating association/intervention/counterfactual.
- Counting repeated reports of one source as independent corroboration.
- Continuing research after information gain collapses.
- Forcing a definitive verdict when evidence remains genuinely unresolved.
- Choosing the most likely hypothesis as the action without a loss/reversibility check.
- Reusing in-domain calibration under material shift without target validation.
- Committing irreversibly when a cheap high-VOI probe is available.