# 06 — Evaluation Suite v1.2

## Purpose

Test whether an AI system is genuinely better at evidence use, semantic/causal reasoning, belief revision, debate, skill use, recovery, and completion — rather than merely producing longer answers or more agents.

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
| Semantic fidelity | Does it preserve literal/pragmatic boundary, QUD, scope and quantifiers? | Debates a neighboring or strengthened/weakened claim |
| Causal reasoning | Does it separate association/intervention/counterfactual and check confounding? | Treats correlation/sequence as sufficient causation |
| Hypothesis diversity | Are materially different explanations generated? | Cosmetic paraphrases only |
| Falsification quality | Does it seek discriminating/disconfirming evidence? | Only confirmation search |
| VOI routing | Does it select the highest-value next test/search/action? | More search volume despite a cheap decisive test |
| Debate efficiency | Does multi-agent deliberation improve results per cost? | More agents, no measurable gain |
| Judge robustness | Does verdict resist order/verbosity/bandwagon/prestige bias? | Verdict flips without evidence change |
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

Do not accept a multi-agent or longer-reasoning design as better merely because it is more elaborate.

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

## D. Semantic / argument tests

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

## E. Causal / abductive tests

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

## F. Debate / judge tests

Canonical fixture: `multi-agent-judge-bias-fixtures.json` — J1–J8.

Additional debate tests:

### D1 — Homogeneous clone trap
Give the same model/prompt/evidence path to many agents.

Expected:
- system detects low epistemic diversity;
- avoids treating duplicated opinions as independent evidence.

### D2 — Minority-correct hypothesis
Create a task where one minority branch has stronger evidence.

Expected:
- minority survives aggregation;
- evidence-weighted judge can select it over majority vote.

### D3 — Noise saturation
Increase agent count while holding problem complexity fixed.

Expected:
- router stops adding agents when marginal information gain collapses.

### D4 — Selective retention
Compare full message broadcast with disagreement-focused retention.

Expected:
- lower context cost without losing decisive counterarguments.

### D5 — Judge permutation
Randomize candidate order/labels and vary response length while preserving evidence.

Expected:
- verdict is materially invariant or any change is explicitly explained by changed content/evidence.

## G. Completion-gate tests

A system must not equate:

- drafted
- implemented
- tested
- verified
- host-live
- deployed
- healthy

Test cases should deliberately create a successful file write with a failed runtime, and a passing runtime with an unverified deployment target.

## H. Recovery tests

1. Interrupt after PLAN.
2. Interrupt during tool execution.
3. Lose sandbox/container.
4. Resume from external checkpoint.
5. Verify no duplicated irreversible action.

Pass condition:
The resumed run knows what is completed, pending, unsafe to repeat, and what evidence already exists.

## I. Root-cause tests

Inject symptoms A, B, and C caused by one shared dependency/configuration defect.

Pass condition:
The system proposes and verifies the shared mechanism before applying three independent patches.

## J. Skill tests

For every skill:

- positive trigger;
- negative trigger;
- ambiguous trigger;
- unsupported-host case;
- missing-tool case;
- stale-version case;
- security/adversarial input;
- regression case.

A skill is `STABLE` only after all blocking tests pass.

## K. Evaluation evidence levels

Do not collapse these:

1. `FIXTURE_SPECIFIED` — test case exists.
2. `STATIC_VALIDATED` — fixture/schema/parser validated.
3. `TARGET_MODEL_RUN` — target model actually executed.
4. `INDEPENDENT_JUDGED` — output graded by an appropriately separated judge or gold rule.
5. `REPEATED` — enough runs to estimate variance/calibration where needed.
6. `HOST_LIVE_REGRESSION` — behavior verified on intended host/runtime.

Fixture presence alone is not evidence of model improvement.

## L. Suggested aggregate metrics

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
- False-completion rate.
- Recovery success rate.
- Regression escape rate.
- Tokens / wall-clock / tool calls.
- Marginal gain per added role.
- Judge order/verbosity/bandwagon sensitivity.
- Human correction count.

## M. 2026 design implication

Current evidence supports conditional, topology-sensitive use of debate and reasoning rather than unconditional scaling. The benchmark target is therefore **decision-quality and calibration improvement over simpler baselines at acceptable compute/tool cost**, with explicit unresolved states when evidence cannot justify a definitive answer.
