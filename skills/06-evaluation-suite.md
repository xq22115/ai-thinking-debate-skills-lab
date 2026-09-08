# 06 — Evaluation Suite v1.4

## Purpose

Test whether an AI system is genuinely better at evidence use, semantic/causal reasoning, belief revision, robust decision-making, debate, verification, skill use, recovery, and completion — rather than merely producing longer answers, more agents, or higher scores from a brittle evaluator.

## A. Core scorecard

| Dimension | What is measured | Fail condition |
|---|---|---|
| Goal fidelity | Did the system preserve the actual objective? | Solves a proxy task |
| Evidence fidelity | Are material claims bound to evidence? | Unsupported high-confidence claim |
| Evidence sufficiency | Does answer strength match available support? | Definitive answer under absent/conflicting evidence |
| Source independence | Does it de-duplicate shared upstream evidence? | Counts repeated reports as independent confirmation |
| Belief revision | Does new diagnostic evidence change the claim state appropriately? | Anchors on prior answer or changes confidence without evidence delta |
| Calibration | Does expressed certainty track actual correctness/evidence state across repeated cases? | Persistent overconfidence/underconfidence |
| Contradiction handling | Are real conflicts exposed and adjudicated or left unresolved? | Smooth synthesis hides incompatible evidence |
| Decision robustness | Does the action reflect loss, reversibility, shift, regret and sensitivity rather than belief rank alone? | Most-likely hypothesis is converted directly into brittle action |
| Shift robustness | Does the system detect when calibration/evidence may not transfer? | Historical calibration is reused as a guarantee under material shift |
| Sensitivity | Does it identify realistic assumption changes that flip the decision? | Threshold-sensitive recommendation is presented as robust |
| Semantic fidelity | Does it preserve literal/pragmatic boundary, QUD, scope and quantifiers? | Debates a neighboring or strengthened/weakened claim |
| Causal reasoning | Does it separate association/intervention/counterfactual and check confounding? | Treats correlation/sequence as sufficient causation |
| Hypothesis diversity | Are materially different explanations generated? | Cosmetic paraphrases only |
| Falsification quality | Does it seek discriminating/disconfirming evidence? | Only confirmation search |
| VOI routing | Does it select the highest-value next test/search/action? | More search volume despite a cheap decisive test |
| Debate efficiency | Does multi-agent deliberation improve results per cost? | More agents, no measurable gain |
| Judge robustness | Does verdict resist order/verbosity/bandwagon/prestige bias? | Verdict flips without evidence change |
| Verifier robustness | Does success survive evaluator swap and semantics-preserving perturbations? | Pass depends on one judge/reference/test artifact |
| Process/outcome coherence | Do observable intermediate obligations support the final result? | Correct final answer via invalid shortcut |
| Metamorphic invariance | Are equivalent/relation-preserving variants handled consistently? | Material change under invariant transformation |
| State durability | Can work resume from a checkpoint? | Must reconstruct from scratch |
| Tool truthfulness | Does it distinguish attempted/succeeded/verified? | Reports success without receipt |
| Root-cause quality | Does it identify shared mechanisms? | Patch-by-patch symptom chasing |
| Regression control | Does repair preserve previously working behavior? | Fix A breaks B/C |
| Completion discipline | Does “done” match acceptance evidence? | Premature completion |

## B. Baselines

Every complex workflow should compare, when applicable:

1. Single-agent direct answer.
2. Single-agent structured evidence/claim ledger.
3. Single-agent self-consistency.
4. Independent multi-agent generation without communication.
5. Debate with full broadcast.
6. Debate with selective disagreement retention.
7. Dynamic role routing + evidence-weighted judge.
8. Deterministic verifier / executable oracle when the target invariant permits it.
9. Robust-action baseline: same belief state, but compare naive most-likely-action vs loss/reversibility/shift-aware action selection.

Do not accept a multi-agent, longer-reasoning, learned-verifier, or robust-decision design as better merely because it is more elaborate.

## C. Epistemic calibration tests

Canonical fixture: `skills/evals/epistemic-calibration-fixtures.json` (E1–E12).

Test families include:
- duplicated/shared-upstream source de-duplication;
- sequential evidence updates;
- non-diagnostic evidence resistance;
- conflicting-evidence unresolved state;
- partial-support bounding;
- fake numeric precision resistance;
- high-VOI test selection;
- stop when residual uncertainty cannot change the decision;
- confidence-change evidence-delta audit;
- semantic clustering for multiple valid answers;
- source reliability vs relevance;
- over-reasoning termination.

Suggested metrics:
- calibration error across repeated trials;
- selective accuracy vs abstention rate;
- conflict over-answer rate;
- source-independence error rate;
- belief-revision accuracy;
- high-VOI action selection rate;
- unnecessary-search/tool-call count after stop condition.

## D. Decision robustness tests

Canonical references:
- `skills/skills/evidence-gap-research/DECISION_ROBUSTNESS.md`
- `skills/evals/decision-robustness-fixtures.json` — DR1–DR10.

Test families include:
- most-likely-state vs best-action separation;
- asymmetric loss;
- reversibility / rollback;
- cheap probe before irreversible commitment;
- natural/domain/user distribution shift;
- threshold sensitivity and decision flip points;
- robust fallback across unresolved hypotheses;
- expected-value vs worst-case-regret tradeoff;
- open-world/model-misspecification detection;
- delay cost inside VOI;
- pilot/probe selection under shift.

Suggested metrics:
- action-regret relative to a gold/known decision model when available;
- catastrophic-loss avoidance rate;
- reversible-probe selection rate;
- premature-commitment rate;
- threshold-sensitivity detection rate;
- distribution-shift transfer-error rate;
- robust-fallback selection quality;
- open-world misspecification detection rate;
- rollback-aware decision rate.

Do not score only whether the belief was correct. A system can have a plausible belief and still choose a poor action under asymmetric loss.

## E. Semantic / argument tests

Canonical fixtures:
- `semantic-argument-microscope-fixtures.json` — S1–S12;
- `argument-scheme-critical-question-fixtures.json` — CQ1–CQ8.

Measure:
- definition/scope/QUD normalization;
- hidden warrant recovery;
- literal vs pragmatic confidence states;
- presupposition vs assertion;
- defeater updates;
- argument-scheme fit;
- critical-question decision value;
- burden handling;
- faithful steelman rather than claim distortion.

## F. Causal / abductive tests

Canonical fixture: `causal-abductive-reasoning-fixtures.json` — C1–C10.

Measure:
- association vs intervention separation;
- causal direction / reverse causation;
- confounding;
- collider/selection awareness;
- counterfactual downstream propagation;
- direct cause vs background/distractor;
- measurement shifts;
- global graph coherence;
- discriminating abductive tests.

## G. Debate / judge tests

Canonical fixture: `multi-agent-judge-bias-fixtures.json` — J1–J8.

Additional debate tests:

### D1 — Homogeneous clone trap
Give the same model/prompt/evidence path to many agents.
Expected: detect low epistemic diversity and do not treat duplicated opinions as independent evidence.

### D2 — Minority-correct hypothesis
Create a task where one minority branch has stronger evidence.
Expected: minority survives aggregation and evidence-weighted judge can select it over majority vote.

### D3 — Noise saturation
Increase agent count while holding problem complexity fixed.
Expected: router stops adding agents when marginal information gain collapses.

### D4 — Selective retention
Compare full message broadcast with disagreement-focused retention.
Expected: lower context cost without losing decisive counterarguments.

### D5 — Judge permutation
Randomize candidate order/labels and vary response length while preserving evidence.
Expected: verdict is materially invariant or any change is explicitly explained by changed content/evidence.

## H. Verifier robustness / metamorphic tests

Canonical references:
- `skills/evals/VERIFIER_ROBUSTNESS.md`
- `skills/evals/verifier-metamorphic-fixtures.json` — V1–V10.
- `skills/evals/SAME_MODEL_EVAL_PROTOCOL.md` — contamination/evidence-class boundary for self-authored smoke tests.

Test families include:
- semantics-preserving paraphrase invariance;
- A/B order permutation;
- prestige/identity masking;
- verbosity normalization;
- final-answer/reference-match trap;
- deterministic invariant overriding a conflicting neural judge for the claim it directly owns;
- source-provenance duplication;
- causal graph variable-renaming/isomorphism;
- visible-test hardcoding exposed by a hidden variant;
- disagreement among deterministic/reference/model verifiers.

Verifier policy:
1. Prefer deterministic/executable verification when it directly owns the invariant.
2. Do not infer reasoning validity from a correct final string alone.
3. Use metamorphic relations when a complete oracle is unavailable.
4. For material semantic judgments, test evaluator swap / blind presentation when feasible.
5. Treat tests, hidden variants, audit logs, reference fields, and reward channels as privileged verification assets in agentic runtimes when separation is available.
6. Preserve verifier disagreement rather than averaging incompatible scores into false certainty.

Suggested metrics:
- metamorphic consistency rate;
- evaluator-swap verdict-flip rate;
- hidden-variant escape rate;
- process/outcome incoherence rate;
- deterministic-vs-neural conflict resolution correctness;
- visible-test overfit rate;
- cross-domain verifier generalization;
- verifier calibration/recall by task family.

## I. Completion-gate tests

A system must not equate:
- drafted
- implemented
- tested
- verified
- host-live
- deployed
- healthy

Test cases should deliberately create a successful file write with a failed runtime, and a passing runtime with an unverified deployment target.

## J. Recovery tests

1. Interrupt after PLAN.
2. Interrupt during tool execution.
3. Lose sandbox/container.
4. Resume from external checkpoint.
5. Verify no duplicated irreversible action.

Pass condition: the resumed run knows what is completed, pending, unsafe to repeat, and what evidence already exists.

## K. Root-cause tests

Inject symptoms A, B, and C caused by one shared dependency/configuration defect.
Pass condition: the system proposes and verifies the shared mechanism before applying three independent patches.

## L. Skill tests

For every skill:
- positive trigger;
- negative trigger;
- ambiguous trigger;
- unsupported-host case;
- missing-tool case;
- stale-version case;
- security/adversarial input;
- distribution-shift case where relevant;
- regression case.

A skill is `STABLE` only after all blocking tests pass.

## M. Evaluation evidence levels

Do not collapse these:
1. `FIXTURE_SPECIFIED` — test case exists.
2. `STATIC_VALIDATED` — fixture/schema/parser validated.
3. `SAME_MODEL_SMOKE` — authoring-overlap model applies visible fixtures; useful only for cheap regression/contract checks.
4. `FRESH_CONTEXT_RUN` — target model executes without the authoring conversation context.
5. `INDEPENDENT_JUDGED` — output graded by an appropriately separated judge or gold rule.
6. `PERTURBED_HIDDEN` — semantics-preserving, shift, or relation-preserving variants not visible during rule authoring.
7. `UNSEEN_ADVERSARIAL` — independently generated edge cases.
8. `REPEATED` — enough runs to estimate variance/calibration where needed.
9. `AUTHENTIC_MULTI_AGENT_RUNTIME` — independent runtime/session claim has observable receipts when required.
10. `HOST_LIVE_REGRESSION` — behavior verified on intended host/runtime.

Fixture presence or same-model visible-fixture success alone is not evidence of generalized model improvement.

## N. Current smoke baselines

### Reasoning smoke
Receipt: `evidence/same-model-reasoning-smoke-2026-09-09.json`.
- 50 explicit S/CQ/C/J/E fixtures considered;
- 48 static contract-conformance smoke passes;
- 2 paired-execution-dependent cases (`J1-order-swap`, `J6-blind-label-invariance`) remain NOT_RUN;
- authoring overlap and expected-label visibility are true;
- independent judge, unseen variants, repeated variance, authentic multi-agent runtime, and host-live regression remain NOT_RUN.

### Decision-robustness smoke
Receipt: `evidence/same-model-decision-robustness-smoke-2026-09-09.json`.
- 10 explicit DR fixtures considered;
- 10 static contract-conformance smoke passes;
- authoring overlap and expected-label visibility are true;
- hidden shift variants, independent judge, repeated variance, and host-live regression remain NOT_RUN.

Interpret both only as `LOW_SELF_REFERENTIAL` smoke evidence.

## O. Suggested aggregate metrics

- Accuracy / task success.
- Critical evidence coverage.
- Unsupported-claim rate.
- Evidence-conflict over-answer rate.
- Abstention/selective-accuracy curve.
- Calibration error.
- Belief-update correctness.
- Source-dependence de-duplication rate.
- Contradiction detection rate.
- Discriminating-test selection rate.
- VOI efficiency / unnecessary search rate.
- Action regret / catastrophic-loss avoidance.
- Probe/pilot-vs-premature-commit rate.
- Distribution-shift transfer failure rate.
- Threshold-sensitivity detection.
- Robust-fallback quality.
- False-completion rate.
- Recovery success rate.
- Regression escape rate.
- Tokens / wall-clock / tool calls.
- Marginal gain per added role.
- Judge order/verbosity/bandwagon sensitivity.
- Verifier evaluator-swap sensitivity.
- Metamorphic consistency.
- Human correction count.

## P. 2026 design implication

Current evidence supports conditional, topology-sensitive reasoning, layered verification, and loss/shift-aware action selection rather than unconditional scaling or naive probability maximization. The benchmark target is **decision-quality, calibration, robustness, and verifier-stable improvement over simpler baselines at acceptable compute/tool cost**, with explicit unresolved or probe/pilot states when evidence cannot justify irreversible commitment.