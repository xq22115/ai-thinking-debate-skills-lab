# Evidence-Gated Deliberation & Skills OS — RC1 Skills

Status: `EXPERIMENTAL / NOT HOST-LIVE VERIFIED`

The skill folder shape follows the current Agent Skills semantic pattern: each portable skill is self-contained and centered on `SKILL.md` with YAML frontmatter containing at least `name` and `description`. Host-specific packaging/adapters remain separate.

## RC1 Core Skills

1. `evidence-gap-research` — evidence sufficiency, counterevidence, source-dependence/provenance, contradiction handling, calibrated belief updates, VOI, distribution-shift checks, loss/reversibility/sensitivity analysis, robust action selection, and stop conditions. (`0.3.0-rc1`; consult `EPISTEMIC_CALIBRATION.md` and `DECISION_ROBUSTNESS.md` on demand)
2. `semantic-argument-microscope` — literal/pragmatic boundary, implicit warrants, presuppositions, QUD/crux control, defeaters, burden/frame shifts, rhetorical-vs-epistemic separation, plus on-demand argument-scheme / critical-question and causal / abductive analysis before debate. (`0.2.0-rc1`)
3. `competing-hypotheses` — materially different explanations and discriminating tests.
4. `root-cause-clustering` — mechanism-level repair instead of symptom patching.
5. `completion-gate` — prevents false `done` / `verified` / `deployed` claims; exact-revision and infrastructure-state aware. (`0.1.1-rc1`)
6. `recoverable-state` — durable checkpoint/trajectory state, target revalidation, delayed-feedback tracking, global-constraint auditing, option-value/sunk-cost checks, async dependency control, and first-irrecoverable-error recovery. (`0.2.0-rc1`; consult `TEMPORAL_TRAJECTORY_INTEGRITY.md` for long-horizon work)
7. `compatibility-audit` — host/OS/version/permission/product-surface checks with source-class separation. (`0.1.1-rc1`)
8. `multi-agent-deliberation` — dynamic 1–30 role coverage plus anti-sycophancy, minority retention, bias-resistant judge checks, and evidence-graph adjudication; runtime independence remains evidence-gated. (`0.2.0-rc1`)
9. `capability-challenge` — separates `VISIBLE`, `AUTHORIZED`, and `VERIFIED` before terminal `cannot`. (`0.1.1-rc1`)
10. `durable-agent-control-plane` — durable Goal Contract + task identity, isolated writers, goal-contract-bound receipts, goal-drift detection, proxy/acceptance integrity, resume/recovery, and task-result vs infrastructure-state separation. (`0.2.0-rc1`; consult `GOAL_OBJECTIVE_AUDIT.md` when objective ambiguity/proxy gaming matters)

## Composition Order

For complex engineering/research/argument tasks, recommended default composition:

`Goal Contract / objective audit → capability-challenge → compatibility-audit → evidence-gap-research (EPISTEMIC_CALIBRATION.md for evidence/belief/VOI; DECISION_ROBUSTNESS.md when loss/reversibility/shift/sensitivity matter) → semantic-argument-microscope (ARGUMENT_SCHEMES.md / CAUSAL_ABDUCTIVE_REASONING.md on demand) → competing-hypotheses → root-cause-clustering → multi-agent-deliberation (only if useful) → verifier/metamorphic checks when consequential → robust action → recoverable-state/TEMPORAL_TRAJECTORY_INTEGRITY.md when execution is long-horizon/stateful/delayed/asynchronous → execution bound to Goal Contract + trajectory state → completion-gate → fresh recoverable-state checkpoint`

The orchestrator should omit skills and references when their trigger conditions are absent.

## Shared Hard Invariants

- `USER_WORDING != FULL_INTENT`
- `STATED_PREFERENCE != VERIFIED_HELPFULNESS`
- `PROXY_SCORE != TRUE_GOAL`
- `TASK_COMPLETION != USER_SUCCESS`
- `SPECIFICATION_UNCERTAINTY != MODEL_UNCERTAINTY`
- `GOAL_DRIFT != PROGRESS`
- `ACCEPTANCE_TEST != LICENSE_TO_GAME_THE_TEST`
- `MODEL_STATED_OBJECTIVE != REVEALED_DECISION_POLICY`
- `UNKNOWN != IMPOSSIBLE`
- `FAILED_PATH != FAILED_GOAL`
- `VISIBLE != AUTHORIZED != VERIFIED`
- `DOCUMENTATION != RUNTIME_PROOF`
- `CONFIGURED != VERIFIED_DIRECT`
- `CONFIDENCE != EVIDENCE`
- `SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`
- `REPETITION != CORROBORATION`
- `RELEVANCE != RELIABILITY`
- `PLAUSIBILITY != PROBABILITY`
- `CONFLICTING_EVIDENCE != LICENSE_TO_PICK_ONE_SIDE`
- `STRING_DISAGREEMENT != EPISTEMIC_DISAGREEMENT`
- `MORE_REASONING != BETTER_CALIBRATION`
- `LOW_INFORMATION_GAIN != KEEP_SEARCHING`
- `MOST_LIKELY_STATE != BEST_ACTION`
- `CONFIDENCE != UTILITY`
- `CALIBRATED_IN_DOMAIN != CALIBRATED_UNDER_SHIFT`
- `AVERAGE_CASE_SUCCESS != WORST_CASE_ACCEPTABILITY`
- `IRREVERSIBLE_ACTION REQUIRES STRONGER_DECISION_EVIDENCE`
- `UNRESOLVED_STATE != NO_ACTION_POSSIBLE`
- `LOCAL_STEP_SUCCESS != TRAJECTORY_SUCCESS`
- `CHECKPOINT_EXISTS != CHECKPOINT_IS_FRESH`
- `CURRENT_STATE != CHECKPOINT_STATE`
- `DELAYED_FEEDBACK != NO_FEEDBACK`
- `LATE_FAILURE MAY HAVE EARLY_CAUSE`
- `OPTION_VALUE != IMMEDIATE_REWARD`
- `PAST_COST != FUTURE_BENEFIT`
- `PARALLELISM != FREE_SPEEDUP`
- `RECOVERABLE_NOW != RECOVERABLE_LATER`
- `CONSENSUS != CORRECTNESS`
- `VOTE_COUNT != EVIDENCE_WEIGHT`
- `VERBOSITY != ARGUMENT_STRENGTH`
- `RHETORICAL_WIN != EPISTEMIC_WIN`
- `PLAUSIBLE_IMPLICATURE != ASSERTED_FACT`
- `GENERATIVE_PLAUSIBILITY != CASE_EVIDENCE`
- `ASSIGNED_STANCE != BELIEF`
- `NOT_PROVEN != PROVEN_FALSE`
- `FLUENT_QUESTION != CRITICAL_QUESTION`
- `ASSOCIATION != INTERVENTION`
- `P_Y_GIVEN_X != P_Y_GIVEN_DO_X`
- `TEMPORAL_ORDER != CAUSATION`
- `LOCAL_CAUSAL_PLAUSIBILITY != GLOBAL_GRAPH_COHERENCE`
- `NARRATIVE_FIT != BEST_CAUSAL_EXPLANATION`
- `VERIFIER_PASS != TASK_TRUTH`
- `VISIBLE_TEST_PASS != GENERALIZATION`
- `PUBLIC_FIXTURE_PASS != HIDDEN_GENERALIZATION`
- `FRESH_CONTEXT != PRIVATE_ORACLE`
- `PRIVATE_ORACLE != INDEPENDENT_MODEL_JUDGE`
- `PAIR_TEST_REQUIRES_BOTH_EXECUTIONS`
- `METAMORPHIC_CLAIM_REQUIRES_RELATION_CHECK`
- `HIDDEN_LABELS_IN_PUBLIC_REPO != HIDDEN_LABELS`
- `CONTAMINATION_DETECTION_PASS != PROOF_OF_NO_CONTAMINATION`
- `SELF_CRITIQUE_WITHOUT_INFORMATION_GAIN != VERIFICATION`
- `LOCAL_TEST_PASS != HOSTED_CI_PASS`
- `HOSTED_EVAL_HARNESS_CI != TARGET_MODEL_PASS`
- `REPOSITORY_ARTIFACT != PROVIDER_LIVE_EXECUTION`
- `TOOL_SUCCESS != TASK_COMPLETE`
- `PRE_STEP_INFRA_FAILURE != TEST_FAILURE`

## Evaluation References

### Fixture families

- `skills/evals/goal-objective-audit-fixtures.json` — GO1–GO10 goal/specification/proxy fixtures.
- `skills/evals/epistemic-calibration-fixtures.json` — E1–E12 evidence/calibration/VOI fixtures.
- `skills/evals/decision-robustness-fixtures.json` — DR1–DR10 robust-action/shift/regret fixtures.
- `skills/evals/temporal-trajectory-integrity-fixtures.json` — TT1–TT10 long-horizon/trajectory fixtures.
- `skills/evals/semantic-argument-microscope-fixtures.json` — S1–S12 semantic/pragmatic fixtures.
- `skills/evals/argument-scheme-critical-question-fixtures.json` — CQ1–CQ8 scheme/CQ fixtures.
- `skills/evals/causal-abductive-reasoning-fixtures.json` — C1–C10 causal/abductive fixtures.
- `skills/evals/multi-agent-judge-bias-fixtures.json` — J1–J8 judge bias / anti-sycophancy fixtures.
- `skills/evals/verifier-metamorphic-fixtures.json` — V1–V10 evaluator robustness/metamorphic fixtures.

Total explicit fixtures specified: `90`.

Visible same-model receipts currently cover 80 fixtures: `78 PASS / 2 paired NOT_RUN`; V1–V10 remain `SPECIFIED_NOT_EXECUTED`.

### Evaluation infrastructure

- `skills/evals/SAME_MODEL_EVAL_PROTOCOL.md` — visible-fixture contamination boundary.
- `skills/evals/HOLDOUT_EVAL_PROTOCOL.md` — public manifest / frozen responses / private oracle separation.
- `skills/evals/reasoning-eval-manifest.schema.json` — public run metadata contract.
- `skills/evals/reasoning-eval-result.schema.json` — machine-readable evidence/result contract.
- `skills/evals/run_reasoning_evals.py` — provider-neutral artifact scorer; does not call a model.
- `skills/evals/paired-judge-execution-plan.json` — true paired execution requirements for J1/J6.

Canonical evidence ladder:

`FIXTURE_SPECIFIED → STATIC_VALIDATED → SAME_MODEL_SMOKE → FRESH_CONTEXT_RUN → PRIVATE_ORACLE_SCORED → INDEPENDENT_JUDGED → PERTURBED_HIDDEN → UNSEEN_ADVERSARIAL → REPEATED → AUTHENTIC_MULTI_AGENT_RUNTIME → HOST_LIVE_REGRESSION`

GitHub-hosted `Reasoning Eval Harness Gate` has passed for the evaluator harness at the recorded receipt `evidence/reasoning-eval-harness-ci-2026-09-09.json`. This is infrastructure evidence only; fresh-context/private-holdout/independent/hidden target-model evaluation remains NOT_RUN.

## Promotion Rule

No skill moves from `EXPERIMENTAL` to `STABLE` until positive, negative, ambiguous-trigger, stale-version, unsupported-host, adversarial, permission, infrastructure-blocker, shift, goal/proxy-drift, temporal-staleness and regression cases appropriate to that skill are tested.

For `durable-agent-control-plane`, objective-fidelity regression includes proxy-vs-outcome, blocker-goal drift, specification-vs-model uncertainty, high/low-value clarification, preference-vs-helpfulness, hard constraints, authorized-vs-unauthorized goal update, revealed-policy mismatch, and acceptance-test gaming.

For `evidence-gap-research`, minimum regression includes duplicate-source detection, sequential revision, conflict-aware unresolved states, high-VOI selection, belief/action separation, loss asymmetry, reversibility, distribution shift, sensitivity, regret, robust fallback and open-world misspecification.

For `recoverable-state`, temporal regression includes local-pass/global-fail, delayed-feedback pending state, first-irrecoverable-error localization, checkpoint staleness, option value, over-parallelization, sunk-cost continuation, stale-feedback/critic handling, long-trajectory judge robustness and feedback-conditioned replanning.

For `semantic-argument-microscope`, minimum regression includes definition mismatch, hidden warrant, QUD substitution, pragmatic context flip, defeaters, stance freedom, claim-strength calibration, scheme/CQ fidelity, causal-direction/intervention/counterfactual checks and graph coherence.

For `multi-agent-deliberation`, material judge validation includes true paired order swap, verbosity normalization, bandwagon resistance, minority-correct retention, early-consensus resistance, follow-up persuasion, true paired blind-label invariance, separation from debater self-evaluation, and long-trajectory early-failure retention when relevant.

A visible/public fixture cannot satisfy a hidden-generalization promotion gate merely by being scored correctly.

## Portability Boundary

These files describe portable procedural logic. Host-specific plugin manifests, tool calls, sandbox APIs, filesystem paths, permissions, schedulers, MCP/SDK details, and deployment mechanisms belong in adapters rather than in the portable core.

Current product documentation may change faster than these portable contracts. Re-run `compatibility-audit` and use current primary product/spec sources before direct host installation.
