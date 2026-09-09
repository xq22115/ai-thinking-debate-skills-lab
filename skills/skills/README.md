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

For complex engineering/research/argument tasks:

`Goal Contract / objective audit → capability-challenge → compatibility-audit → evidence-gap-research → semantic-argument-microscope → competing-hypotheses → root-cause-clustering → multi-agent-deliberation only if useful → verifier/metamorphic checks when consequential → robust action → recoverable-state for long-horizon/stateful/delayed work → execution bound to Goal Contract + trajectory state → completion-gate → fresh recoverable-state checkpoint`

Omit layers whose trigger conditions are absent.

## Shared Hard Invariants

### Goal / execution truth

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
- `REPOSITORY_ARTIFACT != PROVIDER_LIVE_EXECUTION`
- `TOOL_SUCCESS != TASK_COMPLETE`

### Evidence / decision truth

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
- `IRREVERSIBLE_ACTION_REQUIRES_STRONGER_DECISION_EVIDENCE`

### Temporal / multi-agent truth

- `LOCAL_STEP_SUCCESS != TRAJECTORY_SUCCESS`
- `CHECKPOINT_EXISTS != CHECKPOINT_IS_FRESH`
- `CURRENT_STATE != CHECKPOINT_STATE`
- `DELAYED_FEEDBACK != NO_FEEDBACK`
- `LATE_FAILURE_MAY_HAVE_EARLY_CAUSE`
- `OPTION_VALUE != IMMEDIATE_REWARD`
- `PAST_COST != FUTURE_BENEFIT`
- `PARALLELISM != FREE_SPEEDUP`
- `CONSENSUS != CORRECTNESS`
- `VOTE_COUNT != EVIDENCE_WEIGHT`
- `VERBOSITY != ARGUMENT_STRENGTH`

### Semantic / causal truth

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

### Evaluation / holdout truth

- `VERIFIER_PASS != TASK_TRUTH`
- `VISIBLE_TEST_PASS != GENERALIZATION`
- `PUBLIC_FIXTURE_PASS != HIDDEN_GENERALIZATION`
- `FRESH_CONTEXT != PRIVATE_ORACLE`
- `PRIVATE_ORACLE != INDEPENDENT_MODEL_JUDGE`
- `PAIR_TEST_REQUIRES_BOTH_EXECUTIONS`
- `METAMORPHIC_CLAIM_REQUIRES_RELATION_CHECK`
- `HIDDEN_LABELS_IN_PUBLIC_REPO != HIDDEN_LABELS`
- `PLAIN_ORACLE_HASH != STRONG_LOW_ENTROPY_COMMITMENT`
- `ORACLE_PRESENT != COMMITMENT_REVEALED_AND_VERIFIED`
- `RESPONSE_SET_AFTER_FREEZE != AUTHORIZED_FROZEN_RESPONSE_SET`
- `JUDGMENT_ARTIFACT_PRESENT != CASE_ACTUALLY_INDEPENDENTLY_JUDGED`
- `CONTAMINATION_DETECTION_PASS != PROOF_OF_NO_CONTAMINATION`
- `SELF_CRITIQUE_WITHOUT_INFORMATION_GAIN != VERIFICATION`
- `LOCAL_TEST_PASS != HOSTED_CI_PASS`
- `HOSTED_EVAL_HARNESS_CI != TARGET_MODEL_PASS`
- `PRE_STEP_INFRA_FAILURE != TEST_FAILURE`

## Evaluation References

### Fixture families

- GO1–GO10 — goal/objective audit.
- E1–E12 — epistemic calibration/VOI.
- DR1–DR10 — decision robustness.
- TT1–TT10 — temporal/trajectory integrity.
- S1–S12 — semantic/pragmatic reasoning.
- CQ1–CQ8 — argument schemes/critical questions.
- C1–C10 — causal/abductive reasoning.
- J1–J8 — judge bias/anti-sycophancy.
- V1–V10 — verifier robustness/metamorphic tests.

Total explicit fixtures: `90`.

Visible same-model receipts cover 80 fixtures: `78 PASS / 2 paired NOT_RUN`; V1–V10 remain `SPECIFIED_NOT_EXECUTED`.

### Evaluation infrastructure

Visible smoke:

- `skills/evals/SAME_MODEL_EVAL_PROTOCOL.md`

Private/fresh-context protocol:

- `skills/evals/HOLDOUT_EVAL_PROTOCOL.md`

Commit-reveal/freeze toolchain:

- `skills/evals/holdout-blueprint.schema.json`
- `skills/evals/prepare_holdout_commitment.py`
- `skills/evals/holdout-commitment.schema.json`
- `skills/evals/reasoning-eval-manifest.schema.json`
- `skills/evals/freeze_eval_responses.py`
- `skills/evals/response-freeze-receipt.schema.json`
- `skills/evals/verify_holdout_reveal.py`
- `skills/evals/holdout-reveal-receipt.schema.json`
- `skills/evals/run_reasoning_evals.py`
- `skills/evals/reasoning-eval-result.schema.json`
- `skills/evals/paired-judge-execution-plan.json`

Canonical pipeline:

`PRIVATE BLUEPRINT → PUBLIC MANIFEST + SALTED ORACLE COMMITMENT → TARGET RUN → RESPONSE FREEZE → REVEAL SALT + ORACLE → VERIFY BINDING → SCORE / INDEPENDENT JUDGE`

Canonical evidence ladder:

`FIXTURE_SPECIFIED → STATIC_VALIDATED → SAME_MODEL_SMOKE → FRESH_CONTEXT_RUN → PRIVATE_ORACLE_SCORED → INDEPENDENT_JUDGED → PERTURBED_HIDDEN → UNSEEN_ADVERSARIAL → REPEATED → AUTHENTIC_MULTI_AGENT_RUNTIME → HOST_LIVE_REGRESSION`

GitHub-hosted `Reasoning Eval Harness Gate` is currently `PASS_HARNESS_CI_COMMIT_REVEAL_HARDENED` per `evidence/reasoning-eval-harness-ci-2026-09-09.json`.

That proves only harness execution/tamper/promotion behavior. Fresh-context/private-holdout/independent/hidden target-model evaluation remains `NOT_RUN`.

## Promotion Rule

No skill moves from `EXPERIMENTAL` to `STABLE` until appropriate positive, negative, ambiguous-trigger, stale-version, unsupported-host, adversarial, permission, infrastructure-blocker, shift, goal/proxy-drift, temporal-staleness and regression cases are tested.

For `multi-agent-deliberation`, judge validation includes true paired order swap, verbosity normalization, bandwagon resistance, minority-correct retention, early-consensus resistance, follow-up persuasion, true paired blind-label invariance, separation from debater self-evaluation, and long-trajectory early-failure retention when relevant.

A visible/public fixture, metadata claim, oracle-file presence, unrelated judge receipt, or hosted harness PASS cannot satisfy a stronger hidden-generalization promotion gate.

## Portability Boundary

These files describe portable procedural logic. Host-specific plugin manifests, tool calls, sandbox APIs, filesystem paths, permissions, schedulers, MCP/SDK details, and deployment mechanisms belong in adapters rather than in the portable core.

Current product documentation can change faster than portable contracts. Re-run `compatibility-audit` and use current primary product/spec sources before direct host installation.
