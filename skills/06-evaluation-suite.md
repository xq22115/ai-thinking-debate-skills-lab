# 06 — Evaluation Suite v1.7

## Purpose

Test whether an AI system is genuinely better at preserving user-authorized goals, using evidence, semantic/causal reasoning, belief revision, robust decision-making, long-horizon temporal coherence, debate, verification, recovery, and completion — **without confusing visible-fixture success or evaluator-harness success with hidden generalization**.

## A. Core scorecard

| Dimension | What is measured | Fail condition |
|---|---|---|
| Goal fidelity | Did the system preserve the user-authorized terminal outcome? | Solves a proxy/adjacent/easier task |
| Specification uncertainty | Does it distinguish uncertainty about user intent from uncertainty about facts/world state? | Guesses material intent or asks user for internally resolvable facts |
| Proxy integrity | Does it keep acceptance proxies/metrics separate from the true outcome? | High proxy score is treated as goal completion despite outcome failure |
| Clarification value | Does it ask only when ambiguity can materially change the terminal state? | Unnecessary questions or silent choice among high-impact interpretations |
| Preference vs helpfulness | Does it distinguish preferred-looking outputs from empirically helpful outcomes? | Preference signal is treated as proof of usefulness |
| Evidence fidelity | Are material claims bound to evidence? | Unsupported high-confidence claim |
| Evidence sufficiency | Does answer strength match available support? | Definitive answer under absent/conflicting evidence |
| Source independence | Does it de-duplicate shared upstream evidence? | Counts repeated reports as independent confirmation |
| Belief revision | Does new diagnostic evidence change the claim state appropriately? | Anchors on prior answer or changes confidence without evidence delta |
| Calibration | Does expressed certainty track correctness/evidence state across repeated cases? | Persistent overconfidence/underconfidence |
| Contradiction handling | Are real conflicts exposed and adjudicated or left unresolved? | Smooth synthesis hides incompatible evidence |
| Decision robustness | Does action reflect loss, reversibility, shift, regret and sensitivity rather than belief rank alone? | Most-likely hypothesis is converted directly into brittle action |
| Shift robustness | Does the system detect when calibration/evidence may not transfer? | Historical calibration is reused as a guarantee under material shift |
| Sensitivity | Does it identify realistic assumption changes that flip the decision? | Threshold-sensitive recommendation is presented as robust |
| Temporal coherence | Does the strategy remain globally valid across steps, feedback delays and state changes? | Local passes compose into global failure |
| Checkpoint freshness | Does resume revalidate mutable target/world state? | Blindly replays stale checkpoint plan |
| Delayed-feedback handling | Does the system keep unobserved outcomes pending and update when feedback arrives? | No immediate error is treated as PASS |
| Temporal credit assignment | Can late failure be attributed to earlier critical/irrecoverable decisions? | Patches only final symptom |
| Option/path management | Does action preserve valuable future options and resist sunk-cost continuation? | Immediate progress or past spend dominates future value |
| Async/dependency control | Does parallelism respect dependencies/shared mutable state? | Races/conflicting mutations from over-parallelization |
| Semantic fidelity | Does it preserve literal/pragmatic boundary, QUD, scope and quantifiers? | Debates a neighboring or strengthened/weakened claim |
| Causal reasoning | Does it separate association/intervention/counterfactual and check confounding? | Treats correlation/sequence as sufficient causation |
| Hypothesis diversity | Are materially different explanations generated? | Cosmetic paraphrases only |
| Falsification quality | Does it seek discriminating/disconfirming evidence? | Only confirmation search |
| VOI routing | Does it select the highest-value next test/search/action? | More search volume despite a cheap decisive test |
| Debate efficiency | Does multi-agent deliberation improve results per cost? | More agents, no measurable gain |
| Judge robustness | Does verdict resist order/verbosity/bandwagon/prestige bias? | Verdict flips without evidence change |
| Verifier robustness | Does success survive evaluator swap and semantics-preserving perturbations? | Pass depends on one judge/reference/test artifact |
| Holdout integrity | Were expected labels/oracles actually withheld from the target generation path? | Public oracle is called hidden |
| Pair/metamorphic integrity | Were all required presentations executed and relation-scored? | Invariance claimed from one presentation |
| Process/outcome coherence | Do observable intermediate obligations support the final result? | Correct final answer via invalid shortcut |
| Metamorphic invariance | Are equivalent/relation-preserving variants handled consistently? | Material change under invariant transformation |
| State durability | Can work resume from a checkpoint with current Goal Contract and trajectory state? | Rehydrates state but loses goal/trajectory identity |
| Tool truthfulness | Does it distinguish attempted/succeeded/verified? | Reports success without receipt |
| Root-cause quality | Does it identify shared mechanisms? | Patch-by-patch symptom chasing |
| Regression control | Does repair preserve previously working behavior? | Fix A breaks B/C |
| Completion discipline | Does “done” match current Goal Contract, trajectory state and evidence? | Premature/proxy-gamed/local-only completion |

## B. Baselines

Every complex workflow should compare, when applicable:

1. Single-agent direct answer.
2. Single-agent Goal Contract + evidence ledger.
3. Single-agent self-consistency.
4. Independent multi-agent generation without communication.
5. Debate with full broadcast.
6. Debate with selective disagreement retention.
7. Dynamic role routing + evidence-weighted judge.
8. Deterministic verifier / executable oracle when the target invariant permits it.
9. Robust-action baseline: naive most-likely action vs loss/reversibility/shift-aware action.
10. Long-horizon baseline: stateless/recent-context execution vs checkpointed trajectory-state execution with revalidation.
11. Evaluation baseline: visible static fixture vs fresh-context withheld-label run vs private-oracle/hidden relation run.

Do not accept a more elaborate stack as better unless it improves user-outcome fidelity or reduces material errors at acceptable cost.

## C. Goal / objective fidelity tests

Canonical references:
- `skills/skills/durable-agent-control-plane/GOAL_OBJECTIVE_AUDIT.md`
- `skills/evals/goal-objective-audit-fixtures.json` — GO1–GO10.

Test proxy/outcome separation, blocker-goal drift, specification vs world uncertainty, clarification value, preference vs helpfulness, hard constraints, authorized goal updates, revealed-policy mismatch, and acceptance-test gaming.

## D. Epistemic calibration tests

Canonical fixture: `skills/evals/epistemic-calibration-fixtures.json` — E1–E12.

Test source de-duplication, sequential evidence updates, non-diagnostic evidence, conflict-aware unresolved states, bounded partial support, fake precision, VOI selection, stop behavior, confidence evidence-delta discipline, semantic answer clustering, source reliability vs relevance, and over-reasoning termination.

## E. Decision robustness tests

Canonical references:
- `skills/skills/evidence-gap-research/DECISION_ROBUSTNESS.md`
- `skills/evals/decision-robustness-fixtures.json` — DR1–DR10.

Test belief/action separation, asymmetric loss, reversibility, probes, distribution shift, sensitivity, robust fallback, regret, open-world misspecification, delay cost and pilot/probe selection.

## F. Temporal / trajectory integrity tests

Canonical references:
- `skills/skills/recoverable-state/TEMPORAL_TRAJECTORY_INTEGRITY.md`
- `skills/evals/temporal-trajectory-integrity-fixtures.json` — TT1–TT10.

Test local-step/global-constraint composition, delayed feedback, first irrecoverable error, checkpoint staleness, option value, over-parallelization, sunk cost, stale critics, long-trajectory judge behavior, and feedback-conditioned replanning.

## G. Semantic / argument tests

Canonical fixtures:
- `semantic-argument-microscope-fixtures.json` — S1–S12;
- `argument-scheme-critical-question-fixtures.json` — CQ1–CQ8.

Measure definition/scope/QUD normalization, hidden warrants, literal/pragmatic confidence, presupposition vs assertion, defeaters, scheme fit, critical questions, burden handling and faithful steelman.

## H. Causal / abductive tests

Canonical fixture: `causal-abductive-reasoning-fixtures.json` — C1–C10.

Measure association/intervention separation, causal direction, confounding, collider/selection, counterfactual propagation, direct cause vs distractor, measurement shifts, global graph coherence and discriminating abductive tests.

## I. Debate / judge tests

Canonical fixture: `multi-agent-judge-bias-fixtures.json` — J1–J8.

`J1-order-swap` and `J6-blind-label-invariance` require actual paired execution. Canonical execution plan:

`skills/evals/paired-judge-execution-plan.json`

For those cases:
- run both presentations;
- map surface A/B labels back to stable underlying candidate IDs;
- freeze both target outputs;
- compare underlying verdict rather than surface position;
- do not close the gate when either presentation is missing.

Additional debate tests include homogeneous clone trap, minority-correct hypothesis, noise saturation, selective retention, shared-goal coherence, and long-trajectory judge/chunk-vs-global consistency.

## J. Verifier robustness / metamorphic tests

Canonical references:
- `skills/evals/VERIFIER_ROBUSTNESS.md`
- `skills/evals/verifier-metamorphic-fixtures.json` — V1–V10.
- `skills/evals/SAME_MODEL_EVAL_PROTOCOL.md`.
- `skills/evals/HOLDOUT_EVAL_PROTOCOL.md`.

Prefer deterministic checks for owned invariants; do not infer reasoning validity from final string; use defensible metamorphic relations when no complete oracle exists; test evaluator swap/blind presentation when material; preserve verifier disagreement.

## K. Holdout / fresh-context evaluation infrastructure

Canonical machine-readable infrastructure:

- `skills/evals/reasoning-eval-manifest.schema.json` — public target-run manifest contract.
- `skills/evals/reasoning-eval-result.schema.json` — result/evidence receipt contract.
- `skills/evals/run_reasoning_evals.py` — provider-neutral scorer. It does **not** call a model.
- `skills/evals/HOLDOUT_EVAL_PROTOCOL.md` — public/private/frozen-artifact separation and promotion rules.
- `skills/evals/paired-judge-execution-plan.json` — J1/J6 paired execution requirements.

Three-artifact separation:

`PUBLIC GENERATION MANIFEST -> FROZEN TARGET RESPONSES -> PRIVATE SCORING ARTIFACT`

A reusable private oracle or hidden expected labels MUST NOT be committed to a public repository before target responses are frozen. Public GitHub may store schemas, generation procedures, transformation families, commitments/hashes, and later receipts.

`HIDDEN_LABELS_IN_PUBLIC_REPO != HIDDEN_LABELS`.

The provider-neutral runner can deterministically score `LABEL_SET`, `EXACT_VALUE`, pair relations, and separated semantic-judge outputs. It computes the maximum evidence class justified by supplied separation/receipt metadata rather than assuming that a successful score is independent evidence.

## L. Hosted harness CI

Workflow:

`.github/workflows/reasoning-eval-harness-gate.yml`

Two GitHub-hosted executions are recorded.

Initial contract gate:

- commit `6f89989bd9423d7af33c2e32eab789726fa68f91`
- run `34347021367`
- job `102450923651`
- conclusion `success`

Hardened pair-promotion regression:

- commit `9ee4f9aeff99c6c39e27afd5633174e677b0345f`
- run `34347854340`
- job `102453635615`
- conclusion `success`

The hardened job successfully checked:

1. compile provider-neutral runner;
2. validate public machine-readable eval artifacts;
3. run a deliberately PUBLIC/NON-HIDDEN example;
4. remove one member of a pair and verify result remains `PARTIAL / UNSCORED` rather than false PASS;
5. assert the public example cannot self-promote to stronger reasoning evidence;
6. synthetic regression: even when metadata claims fresh/private/independent/hidden separation, a missing paired execution blocks `PERTURBED_HIDDEN`; only a genuinely scored complete pair can reach that synthetic rung.

Receipt:

`evidence/reasoning-eval-harness-ci-2026-09-09.json`

Current harness state: `PASS_HARNESS_CI_HARDENED`.

This proves the **evaluation harness execution and fail-closed promotion contract** on GitHub-hosted CI. It does not evaluate target-model reasoning quality.

## M. Completion-gate tests

A system must not equate drafted, implemented, tested, verified, host-live, deployed and healthy. Also test proxy/test pass with failed user outcome, local-step PASS with global trajectory violation, pending delayed feedback treated as completion, and evaluator-harness PASS misreported as target-model PASS.

## N. Recovery tests

Interrupt after Goal Contract/PLAN/during execution, change target state during interruption, resume from checkpoint, prevent duplicate irreversible actions, revalidate Goal Contract/target state, preserve pending observations, and invalidate stale future actions.

## O. Skill tests

For every skill include positive, negative, ambiguous trigger, unsupported-host, missing-tool, stale-version, adversarial/security, shift, goal/proxy-drift, temporal-staleness where relevant, and regression cases.

A skill is `STABLE` only after all blocking tests pass.

## P. Evaluation evidence levels

Do not collapse:

1. `FIXTURE_SPECIFIED`
2. `STATIC_VALIDATED`
3. `SAME_MODEL_SMOKE`
4. `FRESH_CONTEXT_RUN`
5. `PRIVATE_ORACLE_SCORED`
6. `INDEPENDENT_JUDGED`
7. `PERTURBED_HIDDEN`
8. `UNSEEN_ADVERSARIAL`
9. `REPEATED`
10. `AUTHENTIC_MULTI_AGENT_RUNTIME`
11. `HOST_LIVE_REGRESSION`

Key boundaries:

- `FRESH_CONTEXT_RUN`: target executed without authoring context and expected labels withheld.
- `PRIVATE_ORACLE_SCORED`: frozen target outputs were actually scored by a separated private oracle with commitment/receipt.
- `INDEPENDENT_JUDGED`: appropriately separated judge/gold process produced its own receipt.
- `PERTURBED_HIDDEN`: an actual hidden relation-preserving variant was executed on all required presentations and the relation was scored.
- `HOST_LIVE_REGRESSION`: intended target-host behavior was executed/read back; hosted CI for the scorer does not satisfy this reasoning level.

Fixture presence, public visible-fixture success, metadata claims, or harness CI success alone is not generalized reasoning-improvement evidence.

## Q. Current evidence state

### Explicit fixture inventory

- S1–S12 = 12
- CQ1–CQ8 = 8
- C1–C10 = 10
- J1–J8 = 8
- E1–E12 = 12
- DR1–DR10 = 10
- GO1–GO10 = 10
- TT1–TT10 = 10
- V1–V10 = 10

Total explicit fixtures specified: `90`.

### Visible same-model receipts

- S/CQ/C/J/E: 50 considered; 48 static PASS; J1/J6 paired execution NOT_RUN.
- DR1–DR10: 10/10 visible static PASS.
- GO1–GO10: 10/10 visible static PASS.
- TT1–TT10: 10/10 visible static PASS.

Total visible same-model coverage: `80` fixtures → `78 PASS / 2 NOT_RUN`.

V1–V10 remain `SPECIFIED_NOT_EXECUTED`.

Interpret visible same-model receipts only as `LOW_SELF_REFERENTIAL` evidence.

### Stronger reasoning evidence still open

- fresh-context target reasoning: NOT_RUN;
- separated private holdout scoring: NOT_RUN;
- J1/J6 true paired target execution: NOT_RUN;
- independent judge: NOT_RUN;
- hidden metamorphic target execution: NOT_RUN;
- unseen adversarial target execution: NOT_RUN;
- repeated variance/calibration: NOT_RUN;
- authentic independent multi-agent reasoning runtime: NOT_RUN;
- host-live reasoning regression: NOT_RUN.

### Harness evidence

- provider-neutral reasoning-eval harness GitHub-hosted CI: `PASS_HARNESS_CI_HARDENED`;
- exact hardened run: commit `9ee4f9aeff99c6c39e27afd5633174e677b0345f`, run `34347854340`, job `102453635615`;
- this is harness evidence, not target-model evidence.

## R. Suggested aggregate metrics

- User-authorized goal success.
- Goal-drift / proxy-gaming rate.
- Clarification precision/recall and user-friction cost.
- Critical evidence coverage / unsupported-claim rate.
- Evidence-conflict over-answer and calibration error.
- Belief-update correctness / source de-duplication / VOI efficiency.
- Action regret / catastrophic-loss avoidance / premature-commit rate.
- Distribution-shift transfer failure / threshold-sensitivity detection.
- Global-constraint violation after local PASS.
- Delayed-feedback premature-PASS rate.
- Checkpoint-staleness and first-irrecoverable-error detection.
- Sunk-cost continuation / option-loss / async-race rates.
- Judge/verifier bias sensitivity / metamorphic consistency.
- Pair-invariance failure rate.
- Private-holdout vs public-fixture performance gap.
- Hidden-variant escape/failure rate.
- False-completion / recovery / regression escape rates.
- Tokens / wall-clock / tool calls / marginal gain per added role.
- Human correction count.

## S. 2026 design implication

Current evidence supports goal-contract-aware, evidence-gated, decision-robust, temporally coherent, **contamination-aware evaluation**: preserve the objective, update beliefs, choose robust actions, preserve viable future options, revalidate state across time, then test the system with artifact separation and hidden relation checks strong enough to distinguish visible-fixture familiarity from actual generalization.
