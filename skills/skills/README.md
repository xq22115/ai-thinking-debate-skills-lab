# Evidence-Gated Deliberation & Skills OS — RC1 Skills

Status: `EXPERIMENTAL / NOT HOST-LIVE VERIFIED`

The skill folder shape follows the current Agent Skills semantic pattern: each portable skill is self-contained and centered on `SKILL.md` with YAML frontmatter containing at least `name` and `description`. Host-specific packaging/adapters remain separate.

## RC1 Core Skills

1. `evidence-gap-research` — evidence sufficiency, counterevidence, source-dependence/provenance, contradiction handling, calibrated belief updates, VOI, distribution-shift checks, loss/reversibility/sensitivity analysis, robust action selection, and stop conditions. (`0.3.0-rc1`; consult `EPISTEMIC_CALIBRATION.md` and `DECISION_ROBUSTNESS.md` on demand)
2. `semantic-argument-microscope` — literal/pragmatic boundary, implicit warrants, presuppositions, QUD/crux control, defeaters, burden/frame shifts, rhetorical-vs-epistemic separation, plus on-demand argument-scheme / critical-question and causal / abductive analysis before debate. (`0.2.0-rc1`; reasoning references added 2026-09-08)
3. `competing-hypotheses` — materially different explanations and discriminating tests.
4. `root-cause-clustering` — mechanism-level repair instead of symptom patching.
5. `completion-gate` — prevents false `done` / `verified` / `deployed` claims; exact-revision and infrastructure-state aware. (`0.1.1-rc1`)
6. `recoverable-state` — external checkpoints for long-horizon work.
7. `compatibility-audit` — host/OS/version/permission/product-surface checks with source-class separation. (`0.1.1-rc1`)
8. `multi-agent-deliberation` — dynamic 1–30 role coverage plus anti-sycophancy, minority retention, bias-resistant judge checks, and evidence-graph adjudication; runtime independence remains evidence-gated. (`0.2.0-rc1`)
9. `capability-challenge` — separates `VISIBLE`, `AUTHORIZED`, and `VERIFIED` before terminal `cannot`. (`0.1.1-rc1`)
10. `durable-agent-control-plane` — durable task identity, isolated writers, receipts, resume/recovery, and task-result vs infrastructure-state separation. (`0.1.1-rc1`)

## Composition Order

For complex engineering/research/argument tasks, recommended default composition:

`capability-challenge → compatibility-audit → evidence-gap-research (EPISTEMIC_CALIBRATION.md for evidence/belief/VOI; DECISION_ROBUSTNESS.md when action loss, reversibility, shift or sensitivity matter) → semantic-argument-microscope (when claims/wording/context are contested; ARGUMENT_SCHEMES.md when inferential scheme matters; CAUSAL_ABDUCTIVE_REASONING.md when the crux is causal/explanatory/interventional/counterfactual) → competing-hypotheses → root-cause-clustering → multi-agent-deliberation (only if useful; judge bias checks when material) → verifier/metamorphic checks when consequential → robust action / execution → completion-gate → recoverable-state checkpoint`

The orchestrator should omit skills and references when their trigger conditions are absent.

## Shared Hard Invariants

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
- `SELF_CRITIQUE_WITHOUT_INFORMATION_GAIN != VERIFICATION`
- `LOCAL_TEST_PASS != HOSTED_CI_PASS`
- `REPOSITORY_ARTIFACT != PROVIDER_LIVE_EXECUTION`
- `TOOL_SUCCESS != TASK_COMPLETE`
- `PRE_STEP_INFRA_FAILURE != TEST_FAILURE`

## Evaluation References

- `skills/evals/epistemic-calibration-fixtures.json` — E1–E12 source dependence, sequential belief updates, evidence sufficiency/conflict, VOI, stop-rule, semantic-answer clustering, and over-reasoning fixtures.
- `skills/evals/decision-robustness-fixtures.json` — DR1–DR10 belief/action separation, asymmetric loss, reversibility, probes, distribution shift, sensitivity, robust fallback, regret and open-world fixtures.
- `skills/evals/semantic-argument-microscope-fixtures.json` — S1–S12 semantic/pragmatic fixtures.
- `skills/evals/argument-scheme-critical-question-fixtures.json` — CQ1–CQ8 scheme recognition, critical-question ranking, burden and steelman fidelity.
- `skills/evals/causal-abductive-reasoning-fixtures.json` — C1–C10 association/intervention/counterfactual, confounding, reverse causation, collider, measurement-shift, graph-coherence and abductive discrimination fixtures.
- `skills/evals/multi-agent-judge-bias-fixtures.json` — J1–J8 position/order, verbosity, bandwagon, early-consensus, follow-up persuasion and self-judging bias fixtures.
- `skills/evals/verifier-metamorphic-fixtures.json` — V1–V10 evaluator robustness and metamorphic invariance fixtures.

Fixture presence is not generalized model-execution evidence. Visible same-model smoke, hidden variants, independent judging, repeated variance and host-live regression remain separate evidence classes.

## Promotion Rule

No skill moves from `EXPERIMENTAL` to `STABLE` until positive, negative, ambiguous-trigger, stale-version, unsupported-host, adversarial, permission, infrastructure-blocker, shift, and regression cases appropriate to that skill are tested.

For `evidence-gap-research`, minimum regression additionally includes duplicate-source detection, sequential revision, non-diagnostic evidence, conflict-aware unresolved states, bounded partial support, fake-precision resistance, high-VOI test selection, stop-rule behavior, confidence-delta auditing, multi-answer clustering, source reliability vs relevance, over-reasoning termination, belief/action separation, loss asymmetry, reversibility, distribution shift, sensitivity, regret, robust fallback, and open-world misspecification.

For `semantic-argument-microscope`, minimum semantic regression additionally includes definition mismatch, hidden warrant, QUD substitution, pragmatic context flip, presupposition-vs-assertion, defeater update, stance freedom, claim-strength calibration, generation/inference asymmetry, scheme ambiguity, critical-question relevance, burden handling, steelman fidelity, causal-direction checks, intervention/counterfactual separation, and causal-graph coherence.

For `multi-agent-deliberation`, material judge validation additionally includes order swap, verbosity normalization, bandwagon resistance, minority-correct retention, early-consensus resistance, follow-up persuasion checks, blind-label invariance, and separation from debater self-evaluation.

## Portability Boundary

These files describe portable procedural logic. Host-specific plugin manifests, tool calls, sandbox APIs, filesystem paths, permissions, schedulers, MCP/SDK details, and deployment mechanisms belong in adapters rather than in the portable core.

Current product documentation may change faster than these portable contracts. Re-run `compatibility-audit` and use current primary product/spec sources before direct host installation.