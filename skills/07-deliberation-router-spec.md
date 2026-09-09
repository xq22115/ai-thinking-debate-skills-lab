# 07 — Deliberation Router Specification v1.5

## Objective

Select the smallest reasoning/deliberation topology that can materially change the decision **without losing the user-authorized goal or long-horizon coherence**, then choose an action robust to remaining uncertainty and temporal constraints. Route first by goal/specification uncertainty, unresolved information need, decision consequence, and trajectory state—not by task length, rhetoric, or requested agent count alone.

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
- temporal horizon: single-step / short / long
- delayed feedback: none / pending / material
- checkpoint state: none / fresh / stale-unknown / stale-confirmed
- dependency structure: independent / ordered / asynchronous / shared-mutable-state
- global constraint pressure: low / moderate / near-limit / violated
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

Ask only when specification uncertainty can materially change the terminal state or irreversible action. Do not block on low-value ambiguities when a reversible, clearly labeled default preserves the goal.

### Gate B — direct evidence

If an authoritative, target-bound observation/test can settle model/world uncertainty, prefer it over clarification or debate.

### Gate C — epistemic sufficiency

Run `evidence-gap-research` when evidence is partial, absent, conflicting, dependent, stale, shifted, or target-unbound.

Before escalation identify current claim state, strongest support/contradiction, source dependence, unresolved crux, highest-value missing evidence, and calibration-transfer limits.

### Gate D — semantic/argument normalization

Run `semantic-argument-microscope` when parties/models may be disagreeing about definitions, scopes, QUDs, warrants, argument schemes, or pragmatic interpretations.

### Gate E — causal/abductive normalization

If the live crux is causal, explanatory, interventional, or counterfactual, use the causal/abductive reference before assigning debate roles.

### Gate F — distribution-shift / action context

For consequential action under suspected/material/unknown shift:
- downgrade calibration-transfer claims;
- seek target-bound evidence/local validation;
- prefer reversible action when downside is large;
- do not treat historical performance as a deployment guarantee.

### Gate G — temporal / trajectory integrity

Run `recoverable-state` with `TEMPORAL_TRAJECTORY_INTEGRITY.md` when any of these is material:
- work spans many dependent steps or interruptions;
- important feedback arrives later;
- checkpoints may be stale;
- global budgets/constraints span multiple steps;
- parallel actors share mutable state;
- irreversible commitments remove future branches;
- a late failure may have an earlier cause.

Before continuing a long trajectory identify:
- current checkpoint freshness;
- pending delayed observations;
- global remaining constraints/budgets;
- irreversible commitments and remaining options;
- dependency/synchronization state;
- whether current strategy is still preferred from the current state.

`LOCAL_STEP_SUCCESS != TRAJECTORY_SUCCESS`.

## 3. Default deliberation routing

### Tier 0 — deterministic / direct test
Use one execution/research path when the task is mechanical, directly measurable, and another role has negligible information value.

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
- red team/falsifier;
- domain specialist;
- causal/semantic specialist when relevant;
- shift/sensitivity auditor when transfer is uncertain;
- objective/proxy auditor when specification gaming is material;
- trajectory/dependency auditor when long-horizon state is material;
- integrator/judge.

### Tier 3 — extended council
Activate 10–18 specialists only when cross-domain/high-impact work contains multiple genuinely independent unknowns.

### Tier 4 — 30-role coverage pool
Use up to 30 roles only while each additional role has a distinct evidence/method/verification duty and positive marginal information gain.

No role may exist solely to increase agent count.

## 4. Shared-goal and shared-state rule

All roles receive the same current root goal, hard constraints, acceptance tests, non-goals, target identity, Goal Contract revision, and—when relevant—trajectory checkpoint revision.

Agents may disagree about methods, evidence, causal models, risks, or tests. A role does not gain authority to silently change the terminal outcome or mutate shared state outside its write-set.

## 5. Escalation triggers

Escalate only if at least one material condition holds:

- root goal/acceptance contract remains materially ambiguous;
- two strong competing hypotheses remain after normalization;
- independent high-quality evidence conflicts;
- proxy gaming could make acceptance pass while true outcome fails;
- a red team exposes a live blocking flaw;
- causal alternatives require different tests;
- critical action lacks rollback or has high consequence;
- distribution shift is material and target-bound validation is missing;
- decision flips under plausible changes to key assumptions;
- a checkpoint is stale and different replans remain plausible;
- late feedback creates ambiguous temporal attribution;
- asynchronous dependencies create materially different completion-order outcomes;
- a new role has access to a genuinely distinct evidence channel or method.

## 6. De-escalation / stop triggers

Reduce or stop deliberation when:

- a high-value clarification resolves material specification uncertainty;
- a direct test/measurement dominates discussion in VOI;
- a reversible probe/pilot dominates another debate round;
- a pending delayed observation should be awaited before irreversible continuation;
- hypotheses converge and remaining differences are non-material;
- apparent source diversity resolves to one upstream source;
- authoritative target-bound evidence resolves the crux;
- residual uncertainty cannot change the action;
- next information action costs more than its expected value;
- a robust fallback is acceptable across live hypotheses;
- a fresh current-state comparison shows the existing branch is dominated, in which case replan/rollback rather than debate more.

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
- reversibility/loss change that alters action;
- checkpoint freshness change;
- pending delayed feedback;
- global budget/constraint delta;
- irreversible commitment / option loss;
- suspected first irrecoverable error.

Drop/compress repeated agreement, paraphrases, unsupported confidence, duplicated derivative citations, critiques with no evidence/test/action delta, and clarifications whose answer cannot materially affect the action.

## 8. Judge policy

Rank contributions first by compatibility with the current Goal Contract and valid trajectory state, then by:
1. reproducible direct evidence;
2. current primary/spec/product evidence where applicable;
3. independent corroboration after provenance de-duplication;
4. discriminating tests/falsifiability;
5. coherent inference with calibrated uncertainty;
6. popularity only as a weak social signal.

For long trajectories, do not infer success from final polish alone. Preserve early critical violations and use checkpoint/chunk plus global trajectory audit when needed.

## 9. Value-of-information / clarification / timing routing

Before another question, search, wait, probe, or debate round, ask:

- Is the uncertainty about specification, world/model, or pending temporal feedback?
- Could resolving it change the verdict/action/terminal state?
- Can existing context or direct read/test resolve it?
- Is useful feedback expected soon enough to justify waiting?
- What is the consequence of remaining wrong?
- What is the cost of obtaining information, including delay and lost option value?

Prefer the highest decision-value information action, not maximum questioning, search, or visible activity.

## 10. Decision robustness routing

When action is required, separate belief ranking from action ranking. Evaluate asymmetric losses, reversibility, shift, sensitivity, expected/worst-case regret, open-world branches, probe/pilot options, and future option loss.

Allowed action classes:
`COMMIT`, `PROBE`, `PILOT`, `DEFER`, `ABSTAIN_ESCALATE`, `ROBUST_FALLBACK`.

Rules:
- `MOST_LIKELY_STATE != BEST_ACTION`;
- irreversible actions need stronger decision evidence than cheap probes;
- historical calibration does not automatically transfer;
- threshold-sensitive recommendations must be reported as fragile;
- unresolved belief may still permit probe/pilot/fallback;
- no action may silently weaken the Goal Contract;
- immediate progress may be dominated by preserving future option value.

## 11. Temporal recovery / replan routing

When a long-horizon trajectory changes, choose one:

- `KEEP_STRATEGY`
- `LOCAL_REPAIR`
- `REPLAN_BRANCH`
- `ROLLBACK`
- `ABANDON_BRANCH`
- `WAIT_FOR_FEEDBACK`

Base the choice on current—not sunk—future value. If a late failure appears, distinguish `DOWNSTREAM_SYMPTOM` from `FIRST_IRRECOVERABLE_ERROR` before patching.

## 12. Termination

Stop when acceptance evidence is complete for the actual user-authorized outcome, remaining hypotheses are non-material, another round has lower expected value than cost, a blocker is target-bound/documented, execution/eval/probe is more informative, evidence is correctly unresolved, or a robust action is acceptable across live uncertainty.

For long-horizon work, do not terminate while required delayed feedback is pending or global constraints remain unaudited.

## 13. Anti-patterns

- solving a proxy task instead of the root goal;
- treating blocker elimination as the new mission;
- asking the user for facts the system can read directly;
- guessing a material target identity;
- optimizing visible tests instead of outcome;
- majority vote without provenance;
- endless critique without a discriminating test;
- verbosity as depth;
- debating causation before causal normalization;
- repeated-source count as corroboration;
- research after information gain collapses;
- definitive verdict under genuine evidence conflict;
- most-likely hypothesis converted directly into irreversible action;
- calibration transfer under material shift without validation;
- blind replay of stale checkpoint plans;
- local-step PASS used as trajectory PASS;
- over-parallelizing dependent shared-state mutations;
- continuing a dominated branch because of sunk cost.