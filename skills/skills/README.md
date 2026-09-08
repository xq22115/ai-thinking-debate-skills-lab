# Evidence-Gated Deliberation & Skills OS — RC1 Skills

Status: `EXPERIMENTAL / NOT HOST-LIVE VERIFIED`

The skill folder shape follows the current Agent Skills semantic pattern: each portable skill is self-contained and centered on `SKILL.md` with YAML frontmatter containing at least `name` and `description`. Host-specific packaging/adapters remain separate.

## RC1 Core Skills

1. `evidence-gap-research` — evidence sufficiency, counterevidence, source-dependence/provenance, contradiction handling, calibrated belief updates, highest-value next test, and stop conditions. (`0.2.0-rc1`; consult `EPISTEMIC_CALIBRATION.md` when confidence/evidence aggregation is decision-critical)
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

`capability-challenge → compatibility-audit → evidence-gap-research (consult EPISTEMIC_CALIBRATION.md when evidence sufficiency / belief update / source dependence / VOI matters) → semantic-argument-microscope (when claims/wording/context are contested; consult ARGUMENT_SCHEMES.md when inferential scheme matters; consult CAUSAL_ABDUCTIVE_REASONING.md when the crux is causal/explanatory/interventional/counterfactual) → competing-hypotheses → root-cause-clustering → multi-agent-deliberation (only if useful; judge bias checks when material) → durable-agent-control-plane (when execution spans actors/interruptions) → execution → completion-gate → recoverable-state checkpoint`

The orchestrator should omit skills when their trigger conditions are absent.

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
- `SELF_CRITIQUE_WITHOUT_INFORMATION_GAIN != VERIFICATION`
- `LOCAL_TEST_PASS != HOSTED_CI_PASS`
- `REPOSITORY_ARTIFACT != PROVIDER_LIVE_EXECUTION`
- `TOOL_SUCCESS != TASK_COMPLETE`
- `PRE_STEP_INFRA_FAILURE != TEST_FAILURE`

## Evaluation References

- `skills/evals/epistemic-calibration-fixtures.json` — E1–E12 source dependence, sequential belief updates, evidence sufficiency/conflict, VOI, stop-rule, semantic-answer clustering, and over-reasoning fixtures.
- `skills/evals/semantic-argument-microscope-fixtures.json` — S1–S12 semantic/pragmatic fixtures.
- `skills/evals/argument-scheme-critical-question-fixtures.json` — CQ1–CQ8 scheme recognition, critical-question ranking, burden and steelman fidelity.
- `skills/evals/causal-abductive-reasoning-fixtures.json` — C1–C10 association/intervention/counterfactual, confounding, reverse causation, collider, measurement-shift, graph-coherence and abductive discrimination fixtures.
- `skills/evals/multi-agent-judge-bias-fixtures.json` — J1–J8 position/order, verbosity, bandwagon, early-consensus, follow-up persuasion and self-judging bias fixtures.

Fixture presence is not model execution evidence. These suites remain `SPECIFIED_NOT_EXECUTED` until actual target-model/judge runs produce receipts/results.

## Promotion Rule

No skill moves from `EXPERIMENTAL` to `STABLE` until positive, negative, ambiguous-trigger, stale-version, unsupported-host, adversarial, permission, infrastructure-blocker, and regression cases appropriate to that skill are tested.

For `evidence-gap-research`, the minimum epistemic regression set additionally includes duplicate-source detection, sequential evidence revision, non-diagnostic evidence, conflict-aware unresolved states, bounded partial-support answers, fake-precision resistance, high-VOI action selection, stop-rule behavior, confidence-delta auditing, multi-answer semantic clustering, source reliability vs relevance, and over-reasoning termination.

For `semantic-argument-microscope`, the minimum semantic regression set additionally includes definition mismatch, hidden warrant, QUD substitution, pragmatic context flip, presupposition-vs-assertion, defeater update, stance freedom, claim-strength calibration, generation/inference asymmetry, scheme ambiguity, critical-question relevance, burden handling, steelman fidelity, causal-direction checks, intervention/counterfactual separation, and causal-graph coherence.

For `multi-agent-deliberation`, material judge validation additionally includes order swap, verbosity normalization, bandwagon resistance, minority-correct retention, early-consensus resistance, follow-up persuasion checks, blind-label invariance, and separation from debater self-evaluation.

## Portability Boundary

These files describe portable procedural logic. Host-specific plugin manifests, tool calls, sandbox APIs, filesystem paths, permissions, schedulers, MCP/SDK details, and deployment mechanisms belong in adapters rather than in the portable core.

Current product documentation may change faster than these portable contracts. Re-run `compatibility-audit` and use current primary product/spec sources before direct host installation.
