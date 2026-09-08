# 06 — Evaluation Suite v1.4

## Purpose

Test whether an AI system is genuinely better at evidence use, semantic/causal reasoning, multi-turn dialogue-state tracking, belief revision, debate, skill use, recovery, and completion — rather than merely producing longer answers, more elaborate prompts, or more agents.

A target capability is not considered safely improved merely because its own benchmark score rises. Promotion must also protect neighboring capabilities, survive paraphrase/domain shifts, preserve judge uncertainty, and remain bound to the intended runtime/evidence level.

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
| Dialogue-state fidelity | Does it preserve shared/disputed/temporary/unresolved commitments across turns? | Temporary grant, silence, or presupposition becomes false common ground |
| Argument-target comprehension | Does a rebuttal attack the premise/warrant that actually supports the conclusion? | Rhetorical neighboring answer is credited as structural rebuttal |
| Causal reasoning | Does it separate association/intervention/counterfactual and check confounding? | Treats correlation/sequence as sufficient causation |
| Structural generalization | Does the same relation/state analysis survive paraphrase, domain swap and lexical-cue removal? | Performance depends on benchmark vocabulary |
| Routing discipline | Is extra semantic/dialogue machinery loaded only when it can change the verdict? | Invents common ground/history on self-contained cases |
| Hypothesis diversity | Are materially different explanations generated? | Cosmetic paraphrases only |
| Falsification quality | Does it seek discriminating/disconfirming evidence? | Only confirmation search |
| VOI routing | Does it select the highest-value next test/search/action? | More search volume despite a cheap decisive test |
| Debate efficiency | Does multi-agent deliberation improve results per cost? | More agents, no measurable gain |
| Judge robustness | Does verdict resist order/verbosity/bandwagon/prestige bias and preserve disagreement? | Verdict flips without evidence change or disagreement is silently erased |
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

For the semantic dialogue-state **target** suite, use the narrower four-arm comparison defined by `semantic-dialogue-state-eval-protocol.md`:

1. `direct`;
2. `generic-careful`;
3. `microscope-core`;
4. `microscope-dialogue-state`.

For semantic **protection/generalization** holdouts, at minimum compare:

1. `microscope-core`;
2. `microscope-dialogue-state`.

This isolates whether the demand-loaded reference adds target value without degrading the canonical semantic core or relying on copied vocabulary.

Do not accept a multi-agent, longer-reasoning, larger-instruction, or larger-context design as better merely because it is more elaborate.

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

## D. Semantic / argument / dialogue-state tests

Canonical fixtures:

- `semantic-argument-microscope-fixtures.json` — S1–S12 semantic/pragmatic core;
- `argument-scheme-critical-question-fixtures.json` — CQ1–CQ8 argument-scheme/CQ core;
- `semantic-dialogue-state-fixtures.json` — DS1–DS8 target dialogue-state capability;
- `semantic-dialogue-state-protection-fixtures.json` — DSP1–DSP12 neighboring-capability protection;
- `semantic-dialogue-state-generalization-holdout.json` — DSG1–DSG12 anti-leakage / lexical-domain generalization.

Semantic/argument measures include:

- definition/scope/QUD normalization;
- hidden warrant recovery;
- literal vs pragmatic confidence states;
- presupposition vs assertion;
- defeater updates;
- argument-scheme fit;
- critical-question decision value;
- burden handling;
- faithful steelman rather than claim distortion.

Dialogue-state target measures include:

- common-ground integrity;
- temporary-grant vs genuine agreement separation;
- silence/presupposition vs established commitment separation;
- commitment / answer-space / burden / criterion-state deltas;
- same conclusion vs same reasoning separation;
- rebuttal-target comprehension;
- provenance quality vs citation/RAG volume;
- repair quality after a corrupted commitment;
- calibrated uncertainty when dialogue state remains unresolved.

Protection measures include:

- no regression in definition/QUD/pragmatic analysis;
- no regression in defeasible revision or stance freedom;
- no regression in critical-question ranking / steelman fidelity;
- no regression in causal/interventional/global-graph reasoning;
- no invented participants, shared history, commitments or ceremonial ledgers on self-contained cases.

Generalization measures include:

- stable commitment-state reasoning after paraphrase;
- stable support/attack/dependency reasoning after domain swap;
- resistance to loaded or indirect formulations without canonical skill vocabulary;
- correct handling of bounded concessions, stale/withdrawn positions and non-answers without relying on `AGREED`, `COMMON_GROUND`, or similar lexical cues.

Use `semantic-dialogue-state-scoring-rubric.md` for observable-output scoring. A rubric blocking error fails the case even when an aggregate dimension score looks acceptable.

### D1 — Reusable behavioral harness

`run_semantic_dialogue_state_eval.py` is provider-neutral. It does not call a model provider by itself. It can:

- prepare a frozen run manifest for an approved fixture path and selected arm subset;
- hash instruction bundles and exact fixture/rubric/protocol revisions;
- validate externally recorded target-model responses;
- generate blinded judge tasks;
- accept one or multiple judge records per candidate;
- validate structured per-dimension judgments and blocking errors;
- aggregate **case first, then arm**, so cases with more judges are not overweighted;
- preserve dimension disagreement, blocking disagreement, judge count and same-model-family exposure;
- summarize per-arm results, treatment deltas and per-case regressions;
- set `protection_promotion_veto` on protection/generalization runs when treatment regresses against core;
- run synthetic target + protection + multi-judge self-tests for harness integrity.

A synthetic harness self-test verifies execution plumbing only; it does not advance a case to `TARGET_MODEL_RUN`.

### D2 — Judge safeguards

When an LLM judge is used:

- blind candidate/arm identity where possible;
- preserve judge identity/model-family metadata;
- avoid same-model self-judging when an independent judge is available;
- use distinct `judgment_id` plus judge/task/variant identity to prevent duplicate records from masquerading as independent evidence;
- use order swaps for pairwise preference claims;
- preserve per-dimension scores and blocking errors;
- report `any-judge` and `all-judge` blocking signals separately;
- report judge disagreement rather than forcing consensus;
- do not treat judge fluency or generated rationales as ground truth.

`JUDGE_CONSENSUS != GROUND_TRUTH`.

### D3 — Protection promotion pre-gate

`check_semantic_dialogue_state_promotion.py` combines three **already judged** reports:

1. target DS report;
2. neighboring-capability DSP report;
3. generalization DSG report.

It first requires the reports to agree on exact `repo_ref`, candidate `model_id`, and provider. It then blocks advancement when any material condition holds:

- target treatment does not improve over `microscope-core` under the configured minimum delta;
- any target hard case regresses;
- any target blocking regression appears;
- either protection report has `protection_promotion_veto != false`;
- DSP or DSG contains a treatment regression or new blocking regression;
- judge metadata shows same-model-family judge exposure.

Judge disagreement is retained as a review flag rather than converted to consensus.

The highest successful state is:

`READY_FOR_REPEATED_VALIDATION`

not `PROMOTE`, `STABLE`, or `HOST_LIVE`.

`READY_FOR_REPEATED_VALIDATION != REPEATED != STABLE != HOST_LIVE`.

`TARGET_GAIN != SAFE_PROMOTION`.

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

### F1 — Homogeneous clone trap
Give the same model/prompt/evidence path to many agents.

Expected:
- system detects low epistemic diversity;
- avoids treating duplicated opinions as independent evidence.

### F2 — Minority-correct hypothesis
Create a task where one minority branch has stronger evidence.

Expected:
- minority survives aggregation;
- evidence-weighted judge can select it over majority vote.

### F3 — Noise saturation
Increase agent count while holding problem complexity fixed.

Expected:
- router stops adding agents when marginal information gain collapses.

### F4 — Selective retention
Compare full message broadcast with disagreement-focused retention.

Expected:
- lower context cost without losing decisive counterarguments.

### F5 — Judge permutation
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
2. `STATIC_VALIDATED` — fixture/schema/parser/protocol assets validated.
3. `HARNESS_SELF_TESTED` — synthetic end-to-end harness plumbing passed; **not** a target-model result.
4. `TARGET_MODEL_RUN` — target model actually executed and outputs were recorded against exact requests.
5. `INDEPENDENT_JUDGED` — output graded by an appropriately separated judge or gold rule.
6. `REPEATED` — enough runs/order swaps to estimate variance, calibration, or judge instability where needed.
7. `HOST_LIVE_REGRESSION` — behavior verified on intended host/runtime.

`READY_FOR_REPEATED_VALIDATION` is a promotion-pre-gate decision state, not an additional evidence level. It means the current target/protection/generalization reports are coherent enough to justify repeated validation; it does not skip `REPEATED` or `HOST_LIVE_REGRESSION`.

A higher packaging/harness level cannot be substituted for a lower missing behavioral level. In particular, `HARNESS_SELF_TESTED != TARGET_MODEL_RUN`.

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
- Common-ground corruption rate.
- Temporary-grant laundering rate.
- Rebuttal-target comprehension rate.
- Structural-generalization rate under domain/paraphrase shift.
- Dialogue-state blocking-error rate.
- `unnecessary_dialogue_state_invention` count/rate.
- Target treatment delta: `microscope-dialogue-state` vs `direct` and `microscope-core`.
- Target treatment regression count vs `microscope-core`.
- DSP protection regression count / promotion veto state.
- DSG generalization regression count / promotion veto state.
- Judge count per candidate and same-model-family exposure.
- Judge disagreement / order-swap instability.
- Any-judge vs all-judge blocking rate.
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

Current evidence supports conditional, topology-sensitive use of debate and reasoning rather than unconditional scaling. The benchmark target is therefore **decision-quality, structural comprehension, calibration, and generalization improvement over simpler baselines at acceptable compute/tool cost**, with explicit unresolved states when evidence or dialogue state cannot justify a definitive answer.

For progressive reasoning references, the release objective is stronger still: **target gain with protected neighboring capabilities, lexical/domain robustness, judge uncertainty preserved, and no false host-live completion claim**.
