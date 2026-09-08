# 07 — Deliberation Router Specification v1.4

## Objective

Select the smallest reasoning/deliberation topology that can materially change the decision **without losing the user-authorized goal**, then choose an action robust to remaining uncertainty. Route first by goal/specification uncertainty, unresolved information need, and decision consequence—not by task length, rhetoric, or requested agent count alone.

## 1. Inputs

- goal-contract state: clear / materially ambiguous / mixed-goal / drift-suspected
- specification uncertainty: none / low / material
- latest authorized goal revision: known / uncertain
- proxy/metric gaming risk: low / material / unknown
- task risk: low / medium / high / critical
- model/world uncertainty: low / medium / high
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

### Gate 0 — Goal Contract / objective audit

Before spending reasoning or agent budget, determine whether the intended terminal state is sufficiently specified for the proposed action.

When material, normalize:
- `ROOT_GOAL`;
- `HARD_CONSTRAINTS`;
- `ACCEPTANCE_TESTS`;
- `PROXIES / METRICS`;
- `NON_GOALS`;
- target identity/environment;
- latest authorized goal revision.

Use `durable-agent-control-plane/GOAL_OBJECTIVE_AUDIT.md` when ambiguity, intent drift, mixed goals, proxy optimization, or specification gaming is plausible.

Do not ask the user questions merely because the model is uncertain about a fact that can be read/tested internally.

### Gate A — clarification value

If the uncertainty is about what the user wants, estimate the decision value of clarification.

Ask when:
- alternative interpretations lead to materially different or irreversible terminal states;
- the wrong interpretation has meaningful cost;
- user-authoritative context does not already resolve it.

Do not block on low-value ambiguities when a reversible, clearly labeled default preserves the goal.

### Gate B — direct evidence

If an authoritative, target-bound observation/test can settle a model/world-state uncertainty, prefer it over clarification or debate.

### Gate C — epistemic sufficiency

Run `evidence-gap-research` when evidence is partial, absent, conflicting, dependent, stale, shifted, or target-unbound.

Before escalation, identify:
- current claim state;
- strongest support/contradiction;
- source dependence;
- unresolved crux;
- highest-value missing evidence;
- whether historical calibration is transferable.

### Gate D — semantic/argument normalization

Run `semantic-argument-microscope` when parties/models may be disagreeing about definitions, scopes, QUDs, warrants, argument schemes, or pragmatic interpretations.

### Gate E — causal/abductive normalization

If the live crux is causal, explanatory, interventional, or counterfactual, use the causal/abductive reference before assigning debate roles.

Do not ask a council to vote on causation from raw correlation.

### Gate F — distribution-shift / action context

If the action is consequential, determine whether evidence/calibration context differs materially from the target context.

When shift is suspected/material/unknown:
- downgrade calibration-transfer claims;
- seek target-bound evidence/local validation;
- prefer reversible action when downside is large;
- do not treat historical performance as a deployment guarantee.

## 3. Default deliberation routing

### Tier 0 — deterministic / direct test
Use 1 execution or research path when the task is mechanical, directly measurable, and another reasoning role has negligible information value.

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
- shift/sensitivity auditor when transfer is uncertain;
- objective/proxy auditor when specification gaming is material;
- integrator/judge.

### Tier 3 — extended council
Activate 10–18 specialists only when cross-domain/high-impact work contains multiple genuinely independent unknowns.

### Tier 4 — 30-role coverage pool
Use up to 30 roles only while each additional role has a distinct evidence/method/verification duty and positive marginal information gain.

No role may exist solely to increase agent count.

## 4. Shared-goal rule for multi-agent work

All roles receive the same current:
- root goal;
- hard constraints;
- acceptance tests;
- non-goals;
- target identity;
- goal-contract revision.

Agents may disagree about methods, evidence, causal models, risks, or tests. A role does not gain authority to silently change the terminal outcome.

Any proposed goal change is classified and returned to the coordinator/user-authoritative layer.

## 5. Escalation triggers

Escalate only if at least one material condition holds:

- root goal/acceptance contract remains materially ambiguous and no cheap clarification/default resolves it;
- two strong competing hypotheses remain after normalization;
- independent high-quality evidence conflicts;
- proxy gaming could make acceptance pass while true outcome fails;
- a red team exposes a live blocking flaw;
- causal alternatives require different tests;
- compatibility differs materially by OS/host/version;
- critical action lacks rollback or has high consequence;
- distribution shift is material and target-bound validation is missing;
- decision flips under plausible changes to key assumptions;
- a new role has access to a genuinely distinct evidence channel or method.

## 6. De-escalation / stop triggers

Reduce or stop deliberation when:

- a high-value clarification resolves material specification uncertainty;
- a direct test/measurement dominates discussion in VOI;
- a reversible probe/pilot dominates another debate round;
- hypotheses converge and remaining differences are non-material;
- apparent source diversity resolves to one upstream source;
- authoritative target-bound evidence resolves the crux;
- residual uncertainty cannot change the action;
- next information action costs more than its expected value;
- correct state is explicitly unresolved;
- a robust fallback is acceptable across live hypotheses.

Do not continue merely to consume a reasoning budget.

## 7. Message policy

Always retain:
- root-goal/hard-constraint/acceptance changes;
- specification uncertainty that can change terminal state;
- proxy-vs-outcome mismatch;
- new evidence with provenance;
- material contradiction;
- discriminating test;
- blocking risk;
- minority hypothesis with strong evidence;
- confidence change with evidence delta;
- distribution-shift warning;
- sensitivity flip;
- reversibility/loss change that alters action.

Drop/compress:
- repeated agreement;
- paraphrases;
- stylistic commentary;
- unsupported confidence;
- duplicated derivative citations;
- critiques with no evidence/test/action delta;
- clarifying questions whose answer cannot materially affect the action.

## 8. Judge policy

Rank contributions first by compatibility with the current Goal Contract, then by:
1. reproducible direct evidence;
2. current primary/spec/product evidence where applicable;
3. independent corroboration after provenance de-duplication;
4. discriminating tests/falsifiability;
5. coherent inference with calibrated uncertainty;
6. popularity only as a weak social signal.

A contribution that optimizes a different terminal goal cannot win merely by having better evidence for that different task.

Use bias checks from `multi-agent-deliberation` for material judgments.

## 9. Value-of-information / clarification routing

Before another question, search, or debate round, ask:

- Is the uncertainty about the specification or about the world/model?
- Could resolving it change the verdict/action/terminal state?
- Can existing user-authoritative context or a direct read/test resolve it?
- What is the consequence of remaining wrong?
- What is the cost of obtaining the information, including user friction/delay?

Prefer the highest decision-value information action, not maximum questioning or maximum search.

## 10. Decision robustness routing

When action is required, separate `belief ranking` from `action ranking`.

Evaluate:
- asymmetric losses/impact radius;
- reversibility/rollback;
- distribution-shift status;
- sensitivity/threshold flip;
- expected vs worst-case regret where useful;
- `OTHER / MODEL_MISSPECIFICATION` branch;
- reversible probe/pilot options.

Allowed action classes:
`COMMIT`, `PROBE`, `PILOT`, `DEFER`, `ABSTAIN_ESCALATE`, `ROBUST_FALLBACK`.

Rules:
- `MOST_LIKELY_STATE != BEST_ACTION`;
- irreversible actions need stronger decision evidence than cheap probes;
- historical calibration does not automatically transfer;
- threshold-sensitive recommendations must be reported as fragile;
- unresolved belief may still permit probe/pilot/fallback;
- no action may silently weaken the Goal Contract.

## 11. Termination

Stop when:
- acceptance evidence is complete **for the actual user-authorized outcome**;
- remaining hypotheses are non-material;
- another round has lower expected value than cost;
- a hard blocker is target-bound/documented;
- execution/eval/probe is more informative;
- evidence is genuinely insufficient/conflicting and unresolved is correct;
- a robust action is acceptable across live uncertainty.

Consensus or proxy score alone is not a termination condition if goal/acceptance obligations remain open.

## 12. Anti-patterns

- solving a proxy task instead of the root goal;
- treating blocker elimination as the new mission;
- asking the user for facts the system can read directly;
- guessing a material target identity;
- optimizing visible tests instead of outcome;
- 30 homogeneous clones;
- majority vote without provenance;
- endless critique without a discriminating test;
- verbosity as depth;
- debating causation before causal normalization;
- repeated-source count as corroboration;
- research after information gain collapses;
- definitive verdict under genuine evidence conflict;
- most-likely hypothesis converted directly into irreversible action;
- calibration transfer under material shift without validation.