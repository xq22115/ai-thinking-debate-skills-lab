# Decision Robustness Under Uncertainty

Status: `EXPERIMENTAL REFERENCE / USE ON DEMAND`

Purpose: translate an uncertain belief state into an action without pretending that the most likely hypothesis is automatically the best decision. Use when action costs are asymmetric, evidence may be out-of-distribution, choices differ in reversibility, or residual uncertainty remains after reasonable research.

## Core invariants

- `MOST_LIKELY_STATE != BEST_ACTION`
- `CONFIDENCE != UTILITY`
- `LOWER_EXPECTED_ERROR != LOWER_DECISION_LOSS`
- `CALIBRATED_IN_DOMAIN != CALIBRATED_UNDER_SHIFT`
- `IRREVERSIBLE_ACTION REQUIRES STRONGER_DECISION_EVIDENCE`
- `ROBUST_ACTION != MOST_OPTIMISTIC_ACTION`
- `AVERAGE_CASE_SUCCESS != WORST_CASE_ACCEPTABILITY`
- `UNRESOLVED_STATE != NO_ACTION_POSSIBLE`
- `REVERSIBLE_PROBE CAN DOMINATE PREMATURE_COMMITMENT`

## 1. Separate belief from action

Maintain two ledgers when consequence is material:

### Belief ledger
- live hypotheses / state estimates;
- evidence sufficiency;
- uncertainty / confidence state;
- source and shift notes;
- unresolved contradictions.

### Decision ledger
- available actions;
- possible outcomes under each live hypothesis;
- benefit / loss direction;
- reversibility;
- delay / information cost;
- safety or failure boundary;
- regret if the chosen action is wrong;
- whether a low-cost probe can reduce uncertainty before commitment.

Do not choose an action solely because one hypothesis has the highest probability.

## 2. Loss asymmetry

Two mistakes with equal probability can have radically different consequences.

Before recommending a consequential action, identify at least qualitatively:

- false-positive loss;
- false-negative loss;
- cost of delay;
- cost of abstention / deferral;
- reversibility / rollback cost;
- impact radius if wrong.

If losses are highly asymmetric, the decision threshold should reflect that asymmetry rather than defaulting to a 50% or majority threshold.

Use numeric expected utility only when probabilities and utilities are defensible. Otherwise use an ordinal loss matrix.

## 3. Expected utility vs robust decision

Expected utility is useful when the probability model is credible.

When model probabilities are fragile, misspecified, or shifted, also test robustness:

- does the recommended action remain acceptable across plausible probability ranges?;
- does a small change in one uncertain parameter flip the decision?;
- is there an action with slightly lower best-case value but much lower worst-case regret?;
- can the choice be staged, piloted, or made reversible?

A decision that wins only under one precise probability estimate is brittle.

## 4. Regret analysis

For each action A and plausible state H, ask:

`regret(A,H) = loss(A,H) - loss(best action if H were known)`

Use exact numbers only when meaningful; otherwise label regret as `LOW / MODERATE / HIGH / CATASTROPHIC`.

When probabilities are unreliable, compare:

- expected regret under the current belief model;
- worst-case regret over a plausible uncertainty set;
- whether a reversible probe lowers both uncertainty and regret.

Do not mechanically minimize worst-case regret when it creates obviously unacceptable routine cost; treat it as a robustness diagnostic, not a universal objective.

## 5. Sensitivity analysis

A decision is more trustworthy when its recommendation survives reasonable perturbations.

Perturb material assumptions such as:

- hypothesis probability / confidence band;
- source reliability;
- effect size;
- cost or benefit estimate;
- time horizon;
- base rate;
- availability of rollback;
- distribution-shift severity.

Record:

- `STABLE` — recommendation survives plausible perturbations;
- `THRESHOLD_SENSITIVE` — one or more realistic changes flip the recommendation;
- `MODEL_DEPENDENT` — recommendation depends strongly on one uncertain modeling choice;
- `SHIFT_UNSAFE` — calibration/assumptions are not transportable enough for the proposed action.

When threshold-sensitive, identify the smallest assumption change that flips the decision.

## 6. Distribution-shift gate

Before transferring an in-domain confidence estimate to a new case, ask whether the current input/context may differ materially from the calibration/evidence distribution.

Shift indicators can include:

- new user/task population;
- novel domain or vocabulary;
- changed operating environment;
- changed time period / policy / software version;
- unusual prompt or evidence pattern;
- model/tool/version drift;
- retrieval source mix outside prior calibration coverage.

If shift is material or unknown:

1. downgrade claims about calibration transfer;
2. prefer target-bound evidence or a small local validation sample;
3. widen uncertainty / prediction sets when applicable;
4. prefer reversible or conservative actions when downside is large;
5. avoid citing historical calibration as a guarantee.

`EXCHANGEABILITY_ASSUMPTION_FAILED -> COVERAGE_GUARANTEE_MAY_NOT_TRANSFER`

## 7. Unknown-unknown / model inadequacy warning

The hypothesis set itself can be incomplete.

Trigger an `OPEN_WORLD_CHECK` when:

- all current hypotheses fit poorly;
- observations remain surprising under every live model;
- the decision is high-impact and the model was built from narrow prior cases;
- distribution shift is detected;
- repeated patches are required to preserve one explanation.

Response options:

- add an `OTHER / MODEL_MISSPECIFICATION` branch;
- seek a new evidence channel or domain specialist;
- run a reversible probe;
- defer irreversible commitment;
- bound the decision rather than force a complete explanation.

## 8. Action classes under uncertainty

A useful action taxonomy:

- `COMMIT` — evidence/robustness sufficient for the intended consequence;
- `PROBE` — reversible measurement/action that can change the decision;
- `PILOT` — bounded deployment with explicit rollback and observation;
- `DEFER` — wait because information value exceeds delay cost;
- `ABSTAIN / ESCALATE` — current model/evidence is outside a justified decision boundary;
- `ROBUST_FALLBACK` — conservative action acceptable across multiple live hypotheses.

`UNRESOLVED` does not always imply `DEFER`; sometimes `PROBE` or `ROBUST_FALLBACK` is the highest-value action.

## 9. Decision threshold policy

Do not use one fixed threshold for every task.

A threshold should become stricter when:

- action is irreversible;
- downside is asymmetric / high;
- evidence is dependent or conflicting;
- distribution shift is material;
- verification is weak;
- rollback is unavailable.

A threshold may be lower when:

- action is cheap and reversible;
- observation from action is highly informative;
- failure impact is contained;
- rollback is reliable.

This is a decision rule, not permission to weaken factual standards: the belief state must remain honestly reported.

## 10. Interaction with VOI

VOI chooses whether more information is worth obtaining; decision robustness chooses what to do with the current uncertainty.

Recommended sequence:

`belief state -> action/loss matrix -> shift check -> sensitivity -> robust/expected-regret comparison -> VOI of probe/search -> COMMIT / PROBE / PILOT / DEFER / ABSTAIN / FALLBACK`

If a cheap reversible probe can materially reduce high-stakes uncertainty, prefer it over a brittle immediate commitment.

## 11. Output contract

When this reference is triggered, report only what is decision-relevant:

- current belief state and unresolved uncertainty;
- candidate actions;
- asymmetric losses / reversibility;
- distribution-shift status;
- sensitivity / threshold-flip point;
- robust fallback or regret comparison where material;
- highest-value probe / extra information;
- recommended action class with rationale;
- what evidence would justify escalation from probe/defer to commit.

Do not expose private chain-of-thought; provide auditable summaries and explicit assumptions.

## 12. Research signal

Recent work supports three design cautions:

1. LLM uncertainty/calibration can degrade under natural prompt or domain shift, so in-domain calibration should not be treated as portable by default.
2. Selective/conformal methods can provide useful risk-control mechanisms, but their guarantees depend on assumptions such as exchangeability and therefore require shift detection or abstention when those assumptions fail.
3. Decision-focused robustness and regret minimization can produce more stable downstream actions under uncertain coefficients/distributions, but they depend on the chosen uncertainty set and loss model.

Use this reference as a decision scaffold, not as proof that the model knows true utilities or probability distributions.