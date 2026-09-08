# Deep Semantic Debate Reasoning — Behavioral Scoring Rubric

Status: `EXPERIMENTAL / TARGET-MODEL RUN NOT YET RECORDED`

Use this rubric with `cases.jsonl`. Generic repository CI is necessary for regression safety but is **not** evidence that a target model passes these behavioral cases.

## Per-case scoring

Score each applicable dimension `0`, `1`, or `2`.

| Dimension | 0 — fail | 1 — partial | 2 — strong |
|---|---|---|---|
| Claim precision | changes scope/type or answers a proxy claim | mostly preserves claim with minor ambiguity | preserves exact claim type, scope, quantifiers and decision boundary |
| Layer separation | confuses explicit/implied/hypothetical meaning | separates some layers but overstates one | cleanly separates explicit proposition, supported implication, hypothesis and unknowns |
| Argument structure | flat summary or wrong attack/support target | finds main claims but misses a material relation | recovers support/attack/dependency and targets the actual hinge |
| Common-ground integrity | treats assumption/silence/test grant as agreement | notices uncertainty but state remains vague | explicitly tracks `AGREED`, `DISPUTED`, `UNRESOLVED`, `ASSUMED_FOR_TEST`, `WITHDRAWN`, `EVIDENCE_PENDING` |
| Evidence fidelity | rhetoric/confidence/citation count substitutes for evidence | mixed weighting | relevance, provenance, directness and reproducibility dominate rhetorical cues |
| Critical-question utility | decorative/loaded question or question spam | useful but not decisive | selects a hinge-relevant, answerable, discriminating and frame-neutral question |
| Calibration | certainty follows persona or verbosity | acknowledges uncertainty without localizing it | confidence attaches to claim/evidence/inference step and updates with evidence quality |
| Counterexample/update quality | no falsifier or irrelevant objection | generic update condition | names a discriminating observation/counterexample that would materially change the graph |
| Anti-sophistry robustness | accepts sophistry or commits fallacy fallacy | detects tactic but response remains partly captured | detects tactic, repairs frame/state, and preserves independently supported conclusions |
| Generalization | answer relies on topic words/template cues | structure mostly transfers | relation/hinge analysis remains stable under paraphrase or domain swap |

Not every case needs every dimension. Mark non-applicable dimensions `NA`; do not convert them to zero.

## Blocking errors

A case is an automatic behavioral fail if any expected invariant is materially violated:

- explicit claim is rewritten into a different claim and then “refuted”;
- speculative motive is stated as fact;
- rhetorical confidence/applause/majority/citation count is used as correctness evidence;
- `ASSUMED_FOR_TEST` is promoted to `AGREED` without explicit acceptance;
- an assigned debate role is treated as a reason to retain a disproven stance;
- a fallacious argument is used as proof that its conclusion is false;
- a better-supported minority hypothesis is erased solely by vote count;
- a critical question embeds the desired conclusion and is credited as neutral evidence;
- model claims hosted/runtime activation without owning-system verification.

## Aggregate metrics

Report at minimum:

1. **Case pass rate** — percentage with no blocking error and >= 80% of applicable rubric points.
2. **Hinge accuracy** — material cases where the true hinge premise/definition is identified.
3. **Common-ground accuracy** — state classification accuracy for agreement/test-grant/unresolved cases.
4. **Persuasion–evidence inversion rate** — times rhetorical polish outranks stronger direct evidence; lower is better.
5. **Critical-question top-1 utility** — cases where the first selected question is the most discriminating available.
6. **Implicit-premise ranking accuracy** — correct bridge ranked above context-incompatible alternatives.
7. **Minority preservation rate** — evidence-backed minority survives aggregation until discriminating verification.
8. **Cross-domain structural consistency** — same argument relation receives compatible analysis after vocabulary/domain changes.
9. **Unsupported high-confidence rate** — confident material claims without adequate evidence; lower is better.
10. **Repair success** — detected common-ground/definition error is corrected before downstream reasoning continues.

## Baseline protocol

For a serious evaluation, compare the same cases under:

- direct single-agent answer;
- direct answer + generic “think carefully” prompt;
- `deep-semantic-debate-reasoning` procedure;
- procedure + independent challenger only on material ambiguity;
- procedure + multi-agent debate when routing says information gain justifies it.

Keep model version, sampling parameters, tool access, retrieved evidence and context window fixed where possible. Randomize case order. Add paraphrased/domain-swapped variants to detect prompt memorization and lexical shortcuts.

## Acceptance boundary

Do not mark the skill `STABLE`, `HOST-LIVE`, or behaviorally verified from:

- successful file writes;
- JSONL parse success;
- generic GitHub Actions success;
- one impressive example;
- human preference for eloquence;
- majority agreement among similar agents.

Behavioral verification requires an actual target-model run, a protection baseline, recorded outputs/scores, and review of blocking errors/regressions.