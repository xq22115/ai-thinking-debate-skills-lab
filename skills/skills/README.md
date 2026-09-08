# Evidence-Gated Deliberation & Skills OS — RC1 Skills

Status: `EXPERIMENTAL / NOT HOST-LIVE VERIFIED`

The skill folder shape follows the current Agent Skills semantic pattern: each portable skill is self-contained and centered on `SKILL.md` with YAML frontmatter containing at least `name` and `description`. Host-specific packaging/adapters remain separate.

## RC1 Core Skills

1. `evidence-gap-research` — evidence sufficiency, counterevidence, source-dependence/provenance, contradiction handling, calibrated belief updates, VOI, distribution-shift checks, loss/reversibility/sensitivity analysis, robust action selection, and stop conditions. (`0.3.0-rc1`; consult `EPISTEMIC_CALIBRATION.md` and `DECISION_ROBUSTNESS.md` on demand)
2. `semantic-argument-microscope` — literal/pragmatic boundary, implicit warrants, presuppositions, QUD/crux control, defeaters, burden/frame shifts, rhetorical-vs-epistemic separation, plus on-demand argument-scheme / critical-question, causal / abductive, and multi-turn dialogue-state/common-ground analysis before debate. (`0.3.0-rc1`; consult `ARGUMENT_SCHEMES.md`, `CAUSAL_ABDUCTIVE_REASONING.md`, and `DIALOGUE_STATE.md` only when their trigger conditions are material)
3. `competing-hypotheses` — materially different explanations and discriminating tests.
4. `root-cause-clustering` — mechanism-level repair instead of symptom patching.
5. `completion-gate` — prevents false `done` / `verified` / `deployed` claims; exact-revision and infrastructure-state aware. (`0.1.1-rc1`)
6. `recoverable-state` — external checkpoints for long-horizon work.
7. `compatibility-audit` — host/OS/version/permission/product-surface checks with source-class separation. (`0.1.1-rc1`)
8. `multi-agent-deliberation` — dynamic 1–30 role coverage plus anti-sycophancy, minority retention, bias-resistant judge checks, and evidence-graph adjudication; runtime independence remains evidence-gated. (`0.2.0-rc1`)
9. `capability-challenge` — separates `VISIBLE`, `AUTHORIZED`, and `VERIFIED` before terminal `cannot`. (`0.1.1-rc1`)
10. `durable-agent-control-plane` — durable Goal Contract + task identity, isolated writers, goal-contract-bound receipts, goal-drift detection, proxy/acceptance integrity, resume/recovery, and task-result vs infrastructure-state separation. (`0.2.0-rc1`; consult `GOAL_OBJECTIVE_AUDIT.md` when objective ambiguity/proxy gaming matters)

## Composition Order

For complex engineering/research/argument tasks, recommended default composition:

`Goal Contract / objective audit → capability-challenge → compatibility-audit → evidence-gap-research (EPISTEMIC_CALIBRATION.md for evidence/belief/VOI; DECISION_ROBUSTNESS.md when loss/reversibility/shift/sensitivity matter) → semantic-argument-microscope (ARGUMENT_SCHEMES.md / CAUSAL_ABDUCTIVE_REASONING.md on demand; DIALOGUE_STATE.md only when multi-turn shared commitments/common-ground changes can alter the verdict) → competing-hypotheses → root-cause-clustering → multi-agent-deliberation (only if useful) → verifier/metamorphic checks when consequential → robust action / execution bound to Goal Contract revision → completion-gate → recoverable-state checkpoint`

The orchestrator should omit skills and references when their trigger conditions are absent. Do not load dialogue-state machinery for a short self-contained claim if QUD/crux/warrant analysis already resolves it.

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
- `CONSENSUS != CORRECTNESS`
- `VOTE_COUNT != EVIDENCE_WEIGHT`
- `VERBOSITY != ARGUMENT_STRENGTH`
- `RHETORICAL_WIN != EPISTEMIC_WIN`
- `PERSUASION != COMPREHENSION`
- `PLAUSIBLE_IMPLICATURE != ASSERTED_FACT`
- `GENERATIVE_PLAUSIBILITY != CASE_EVIDENCE`
- `ASSIGNED_STANCE != BELIEF`
- `NOT_PROVEN != PROVEN_FALSE`
- `FLUENT_QUESTION != CRITICAL_QUESTION`
- `TEMPORARY_GRANT != AGREEMENT`
- `UNANSWERED_PRESUPPOSITION != COMMON_GROUND`
- `SHARED_CONCLUSION != SHARED_REASONING`
- `STATE_CHANGE != EVIDENCE`
- `CITATIONS_OR_RAG != PROVENANCE_QUALITY`
- `LEXICAL_MATCH != ARGUMENT_UNDERSTANDING`
- `JUDGE_CONSENSUS != GROUND_TRUTH`
- `TARGET_GAIN != SAFE_PROMOTION`
- `PARAPHRASE_SUCCESS != STRUCTURAL_GENERALIZATION` unless relation/state behavior survives lexical/domain shifts
- `ASSOCIATION != INTERVENTION`
- `P_Y_GIVEN_X != P_Y_GIVEN_DO_X`
- `TEMPORAL_ORDER != CAUSATION`
- `LOCAL_CAUSAL_PLAUSIBILITY != GLOBAL_GRAPH_COHERENCE`
- `NARRATIVE_FIT != BEST_CAUSAL_EXPLANATION`
- `VERIFIER_PASS != TASK_TRUTH`
- `VISIBLE_TEST_PASS != GENERALIZATION`
- `SELF_CRITIQUE_WITHOUT_INFORMATION_GAIN != VERIFICATION`
- `LOCAL_TEST_PASS != HOSTED_CI_PASS`
- `REPOSITORY_ARTIFACT != PROVIDER_LIVE_EXECUTION`
- `TOOL_SUCCESS != TASK_COMPLETE`
- `PRE_STEP_INFRA_FAILURE != TEST_FAILURE`

## Evaluation References

- `skills/evals/goal-objective-audit-fixtures.json` — GO1–GO10 root-goal preservation, specification/model uncertainty separation, clarification value, proxy gaming, preference-vs-helpfulness, hard constraints and authorized goal-update fixtures.
- `skills/evals/epistemic-calibration-fixtures.json` — E1–E12 source dependence, sequential belief updates, evidence sufficiency/conflict, VOI, stop-rule, semantic-answer clustering, and over-reasoning fixtures.
- `skills/evals/decision-robustness-fixtures.json` — DR1–DR10 belief/action separation, asymmetric loss, reversibility, probes, distribution shift, sensitivity, robust fallback, regret and open-world fixtures.
- `skills/evals/semantic-argument-microscope-fixtures.json` — S1–S12 semantic/pragmatic fixtures.
- `skills/evals/argument-scheme-critical-question-fixtures.json` — CQ1–CQ8 scheme recognition, critical-question ranking, burden and steelman fidelity.
- `skills/evals/causal-abductive-reasoning-fixtures.json` — C1–C10 causal/abductive fixtures.
- `skills/evals/semantic-dialogue-state-fixtures.json` — DS1–DS8 target cases for common-ground integrity, temporary-grant laundering, answer-space/criterion lock, reasoning alignment, provenance, comprehension-vs-persuasion and structural transfer.
- `skills/evals/semantic-dialogue-state-protection-fixtures.json` — DSP1–DSP12 neighboring-capability protection across definition/QUD/pragmatics, defeasible revision/stance freedom, critical-question/steelman, causal/intervention/global graph, and simple no-dialogue-state cases.
- `skills/evals/semantic-dialogue-state-generalization-holdout.json` — DSG1–DSG12 anti-leakage/generalization using paraphrase, lexical-cue removal, domain changes and indirect formulations.
- `skills/evals/semantic-dialogue-state-scoring-rubric.md` — observable-output dimensions, explicit blocking errors, protection metrics and promotion veto.
- `skills/evals/semantic-dialogue-state-eval-protocol.md` — exact run/campaign identity, isolated execution, multi-judge case-first aggregation, blinded judging and judge-bias safeguards.
- `skills/evals/run_semantic_dialogue_state_eval.py` — provider-neutral run preparation, response validation, blinded judge tasks, disagreement-preserving summaries and protection vetoes.
- `skills/evals/prepare_semantic_dialogue_state_campaign.py` — freezes one repo/model/provider/seed identity across DS/DSP/DSG and creates linked manifests/requests/receipt templates plus `campaign_manifest.json`; preparation only, no provider/judge calls.
- `skills/evals/validate_semantic_dialogue_state_execution.py` — execution receipt/isolation validation and receipt-template preparation.
- `skills/evals/check_semantic_dialogue_state_promotion.py` — combined already-judged DS/DSP/DSG promotion pre-gate.
- `skills/evals/multi-agent-judge-bias-fixtures.json` — J1–J8 judge bias / anti-sycophancy fixtures.
- `skills/evals/verifier-metamorphic-fixtures.json` — V1–V10 evaluator robustness and metamorphic invariance fixtures.

Fixture presence, static validation, campaign preparation, or a synthetic harness self-test is not generalized model-execution evidence. Visible same-model smoke, fresh isolated target-model execution, independent judging, hidden/unseen variants, repeated variance, authentic runtime, and host-live regression remain separate evidence classes.

## Promotion Rule

No skill moves from `EXPERIMENTAL` to `STABLE` until positive, negative, ambiguous-trigger, stale-version, unsupported-host, adversarial, permission, infrastructure-blocker, shift, goal/proxy-drift, and regression cases appropriate to that skill are tested.

For `durable-agent-control-plane`, objective-fidelity regression additionally includes proxy-vs-outcome, blocker-goal drift, specification-vs-model uncertainty, high/low-value clarification, preference-vs-helpfulness, lexicographic hard constraints, authorized-vs-unauthorized goal update, revealed-policy mismatch, and acceptance-test gaming.

For `evidence-gap-research`, minimum regression additionally includes duplicate-source detection, sequential revision, conflict-aware unresolved states, high-VOI test selection, stop behavior, belief/action separation, loss asymmetry, reversibility, distribution shift, sensitivity, regret, robust fallback, and open-world misspecification.

For `semantic-argument-microscope`, minimum regression includes definition mismatch, hidden warrant, QUD substitution, pragmatic context flip, presupposition-vs-assertion, defeaters, stance freedom, claim-strength calibration, scheme/CQ fidelity, causal-direction/intervention/counterfactual checks, graph coherence, temporary-grant/common-ground integrity, answer-space/criterion changes, reasoning-alignment preservation, provenance relevance, rebuttal-target comprehension, DSP1–DSP12 neighboring protection, and DSG1–DSG12 lexical/domain structural generalization.

For the dialogue-state extension specifically, target-suite gain cannot authorize promotion if `microscope-dialogue-state` regresses against `microscope-core` on either protection holdout, introduces a new blocking error, or loses the intended relation/state behavior after lexical/domain cues change. `READY_FOR_REPEATED_VALIDATION` remains a pre-gate decision state, not `STABLE` or `HOST_LIVE`.

For `multi-agent-deliberation`, material judge validation includes order swap, verbosity normalization, bandwagon resistance, minority-correct retention, early-consensus resistance, follow-up persuasion checks, blind-label invariance, separation from debater self-evaluation, and preservation of material judge disagreement.

## Portability Boundary

These files describe portable procedural logic. Host-specific plugin manifests, tool calls, sandbox APIs, filesystem paths, permissions, schedulers, MCP/SDK details, and deployment mechanisms belong in adapters rather than in the portable core.

Current product documentation may change faster than these portable contracts. Re-run `compatibility-audit` and use current primary product/spec sources before direct host installation.