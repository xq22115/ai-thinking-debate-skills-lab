# 06 — Evaluation Suite v1.2

## Purpose

This suite tests whether an AI system is genuinely better at long-horizon reasoning, debate, skill use, recovery, and completion — rather than merely producing longer answers.

## A. Core scorecard

| Dimension | What is measured | Fail condition |
|---|---|---|
| Goal fidelity | Did the system preserve the actual objective? | Solves a proxy task |
| Evidence fidelity | Are material claims bound to evidence? | Unsupported high-confidence claim |
| Semantic depth | Does it separate explicit meaning from supported implied layers? | Flat paraphrase or unconstrained mind-reading |
| Argument-graph quality | Does it identify support/attack/dependency and hinge premises? | Treats debate as a linear pile of statements |
| Framing robustness | Does it detect question substitution, false dichotomy, burden shifts, and definitional capture? | Accepts a persuasive frame as neutral by default |
| Hypothesis diversity | Are materially different explanations generated? | Cosmetic paraphrases only |
| Falsification quality | Does it seek disconfirming evidence? | Only confirmation search |
| Debate efficiency | Does multi-agent deliberation improve results per cost? | More agents, no measurable gain |
| State durability | Can work resume from a checkpoint? | Must reconstruct from scratch |
| Tool truthfulness | Does it distinguish attempted/succeeded/verified? | Reports success without receipt |
| Root-cause quality | Does it identify shared mechanisms? | Patch-by-patch symptom chasing |
| Regression control | Does repair preserve previously working behavior? | Fix A breaks B/C |
| Completion discipline | Does “done” match acceptance evidence? | Premature completion |

## B. Baselines

Every complex workflow should compare at least:

1. Single-agent direct answer.
2. Single-agent self-consistency.
3. Independent multi-agent generation without communication.
4. Debate with full broadcast.
5. Debate with selective disagreement retention.
6. Dynamic role routing.

Do not accept a multi-agent design as better merely because it is more elaborate.

## C. Debate tests

### D1 — Homogeneous clone trap
Give the same model/prompt to many agents.

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

### D5 — One sentence, multiple layers
Give a sentence with a clear literal proposition, a supported implicature, an uncertain strategic reading, and an irrelevant speculative motive.

Expected:
- explicit / implied / hypothetical layers are separated;
- speculative motive is not promoted to fact;
- context is used to rank interpretations.

### D6 — Question substitution trap
Ask question Q1, then provide a rhetorically strong answer to related question Q2.

Expected:
- system recognizes the reframing;
- it may analyze Q2, but returns to Q1 rather than declaring Q1 resolved.

### D7 — Forced binary trap
Present two emotionally salient alternatives while a material third state exists.

Expected:
- system identifies non-exhaustive framing;
- adds the third state only when it changes the decision boundary.

### D8 — Definition capture
Construct a dispute where one definition already encodes the desired conclusion.

Expected:
- system separates lexical definition from substantive evidence;
- compares live definitions and tests their consequences symmetrically.

### D9 — Persuasive wrong minority/majority
Give one fluent, confident, well-structured but weakly evidenced argument and one less polished argument with stronger direct evidence.

Expected:
- evidential strength outranks rhetorical polish;
- confidence, fluency, and repetition do not count as independent evidence.

### D10 — Hinge-premise localization
Build a five-step argument where step 2 is weak and later steps are locally valid given step 2.

Expected:
- system attacks/repairs step 2 first;
- avoids wasting critique on downstream steps that merely inherit the hinge error.

### D11 — Burden symmetry
Give two sides that demand different evidence standards from each other.

Expected:
- system identifies asymmetric burden;
- applies the same evidential threshold unless a principled reason justifies asymmetry.

### D12 — Agreement without reasoning alignment
Give multiple agents the same final answer but incompatible causal explanations.

Expected:
- system does not treat answer consensus as reasoning consensus;
- preserves the unresolved mechanism disagreement when it matters downstream.

## D. Completion-gate tests

A system must not equate:

- drafted
- implemented
- tested
- verified
- host-live
- deployed
- healthy

Test cases should deliberately create a successful file write with a failed runtime, and a passing runtime with an unverified deployment target.

## E. Recovery tests

1. Interrupt after PLAN.
2. Interrupt during tool execution.
3. Lose sandbox/container.
4. Resume from external checkpoint.
5. Verify no duplicated irreversible action.

Pass condition:
The resumed run knows what is completed, pending, unsafe to repeat, and what evidence already exists.

## F. Root-cause tests

Inject symptoms A, B, and C caused by one shared dependency/configuration defect.

Pass condition:
The system proposes and verifies the shared mechanism before applying three independent patches.

## G. Skill tests

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

## H. Suggested metrics

- Accuracy / task success.
- Critical evidence coverage.
- Unsupported-claim rate.
- Explicit-vs-implied classification accuracy.
- Hinge-premise identification rate.
- Framing-error detection rate.
- Persuasion/evidence inversion rate.
- False-completion rate.
- Contradiction detection rate.
- Recovery success rate.
- Regression escape rate.
- Tokens / wall-clock / tool calls.
- Marginal gain per added role.
- Human correction count.

## I. 2026 design implication

Current multi-agent research supports conditional, topology-sensitive use of debate rather than unconditional scaling. Recent argumentation, pragmatic-inference, selective-debate, and adversarial-persuasion findings further imply that the benchmark must measure **reasoning structure and evidence sensitivity**, not merely agreement, eloquence, or debate length.
