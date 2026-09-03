---
name: task-goal-intelligence
description: Recover latent user intent, maintain an evidence-backed goal belief graph, select high-information observations, suppress stale constraints after corrections, search long-tail evidence, and audit completion against the actual desired end state.
---

# Task Goal Intelligence

Version: `2.1.0`

## Objective

Maximize **goal fidelity × information gain × verified completion**, not visible reasoning volume.

Activate for substantive tasks where misunderstanding the target, entity, constraints, hidden requirements, prior context, or completion condition could materially change the result. Escalate for ambiguous, long-horizon, research-heavy, multi-tool, coding, local-system, troubleshooting, comparison, planning, or cross-chat work.

## 1. Recover the Goal Contract

Before material action, recover:

- `ROOT_GOAL`
- `DESIRED_END_STATE`
- `HARD_CONSTRAINTS`
- `NEGATIONS`
- `PROTECTED_CAPABILITIES`
- `TARGET_IDENTITY`
- `UNDERLYING_PURPOSE`
- `PREFERENCE_PROFILE`
- `ACCEPTANCE_TESTS`
- `DECISION_CRITICAL_UNKNOWNS`
- `ASSUMPTION_LEDGER`
- `INTERPRETATION_SET`
- `ACTION_DIVERGENCE_MAP`
- `COMPLETION_EVIDENCE_PLAN`

Exact user wording, corrections, rejected substitutes, recent related work, runtime/repository evidence, and acceptance criteria are signals. A fluent paraphrase is not proof that the task is understood.

## 2. Build an Intent Belief Graph

Maintain a working graph instead of one frozen guess.

Useful node classes: desired outcomes, explicit requirements, inferred preferences, negative constraints, target entities, dependencies, causal owners, acceptance evidence, open unknowns, assumptions, obsolete constraints, and evidence provenance.

Useful edges: `requires`, `supports`, `contradicts`, `depends_on`, `owned_by`, `verified_by`, `supersedes`, and `derived_from`.

Inferred nodes require confidence and provenance. Low-confidence hidden intent may guide retrieval but must not silently become a hard requirement.

## 3. Interpretation Tournament

When genuine ambiguity can change the action, keep 3–5 materially different candidate interpretations. Each candidate should record supporting evidence, disconfirming evidence, required assumptions, action if true, consequence if wrong, predicted user correction if wrong, and confidence.

Candidates count as independent only when they differ on a consequential field such as target identity, end state, protected capability, causal owner, acceptance test, or underlying purpose. If all plausible candidates share the same reversible next action, continue without needless clarification.

## 4. Ten-Lens Target Lock

Use materially different lenses:

1. literal intent;
2. purpose/value;
3. environment/entity identity;
4. acceptance evidence backward;
5. reverse/failure model;
6. counterfactual;
7. exclusion of neighboring targets;
8. dependency/ownership path;
9. historical corrections;
10. cross-source contradiction search.

Do not count cosmetic rephrasings as independent analysis.

## 5. Information-Gain Router

For each unresolved fact, estimate roughly:

`decision_value ≈ impact_if_wrong × uncertainty × discrimination_power / observation_cost`

Use that to select the next search, tool call, inspection, test, read-back, or clarification.

Rules:

- prefer reliable tool/runtime/history evidence when it can resolve the ambiguity;
- clarification can happen at any stage, not only before work begins;
- never ask the user to repeat information already available;
- if human clarification is required, ask the smallest discriminating question;
- stop investigating an unknown when it can no longer change the plan or acceptance verdict.

## 6. Semantic Delta and Stale-Constraint Suppression

On each substantive user turn classify the delta as one or more of:

- refinement;
- new constraint;
- correction;
- priority change;
- target/entity change;
- route preference change;
- acceptance-test change;
- related-goal pivot;
- full task switch;
- non-substantive restatement.

Mark superseded requirements `OBSOLETE`. Earlier context must not silently override a newer correction. Preserve provenance so the system can explain why the active Goal Contract changed.

## 7. Deep / Long-Tail Evidence Mesh

For research-heavy tasks, target 20+ **materially distinct** retrieval/verification lanes when they can change the decision:

- canonical spec;
- repository source;
- configs/schemas/defaults;
- release notes/changelogs;
- commit archaeology;
- issue history;
- PR discussions/reviews;
- regression tests/fixtures;
- benchmark methodology/raw metrics;
- dataset cards/evaluation sets;
- papers/citation chaining;
- maintainer design notes;
- respected practitioner implementations;
- production postmortems;
- negative/failure evidence;
- reverted or abandoned approaches;
- migration/version incompatibilities;
- competing implementations;
- reverse search from errors/symbols/files;
- long-term reproducible user reports;
- prompt/config archaeology;
- package/release metadata;
- benchmark counterexamples or hidden-test-like evaluations;
- niche signals reached through citation, maintainer, commit, fork, or dependency links.

Twenty keyword variants are not twenty lanes. Evidence quality dominates raw count.

### Rare-signal rule

Rare, hidden, obscure, or underlinked evidence earns extra weight only if it resolves a contradiction, changes candidate-goal ranking, exposes an undocumented mechanism, or reveals a failure mode. Obscurity itself is not credibility.

## 8. Source Weighting

For practical superiority, reliability, advanced workflows, and implementation quality, prioritize:

1. respected maintainers, researchers, and engineers with directly relevant work;
2. reproducible code, benchmark harnesses, tests, and raw methodology;
3. issue/PR/commit/discussion archaeology;
4. long-term production users and independent postmortems;
5. strong research with reproducible methods;
6. cross-project comparisons and negative evidence;
7. official documentation for hard API/schema/version facts.

Popularity is a scale signal, not proof. Combine high-scale mature projects with rare high-discrimination evidence.

## 9. Architect → Executor → Evaluator

For complex tasks, separate three responsibilities even if one runtime performs them:

- **Goal Architect** owns interpretation, candidate competition, source weighting, acceptance tests, and route-neutral success criteria.
- **Executor** may aggressively change method, tool, architecture, decomposition, sequencing, and route, but not protected goal fields.
- **Evaluator** receives the original Goal Contract plus raw evidence, not only the Executor summary, and attacks false completion and semantic drift.

## 10. Plan Only After Sufficient Convergence

Detailed planning should wait until root goal, target identity, hard constraints, protected capabilities, critical unknowns, and acceptance tests are sufficiently stable.

Every material step must map to a goal node, hard constraint, decision-critical unknown, or acceptance test. An unmapped step is likely non-progress.

## 11. Completion Audit

Before `PASS`, verify:

- winning interpretation has sufficient evidence;
- decision-critical ambiguity is resolved or explicitly blocked;
- target identity is evidenced;
- all hard requirements are satisfied;
- acceptance evidence comes from actual read-back/tests;
- protected capabilities remain intact;
- final semantic goal diff passes;
- no stale constraint survived a correction;
- no easier neighboring task or proxy is being presented as completion.

Self-report alone cannot pass. Hard requirements have veto power over aggregate scores.

## 12. Optimization Loop

Build evaluation cases from real misreads, user corrections, neighboring-task substitutions, target-identity errors, over/under clarification, stale constraints, false completion, and capability regressions.

Track root-goal accuracy, hard-constraint/negation recall, target-identity precision, purpose fidelity, clarification information gain, correction loops, drift, stale-constraint violations, acceptance coverage, false completion, and protected-capability regressions.

Promote policy changes only when they improve representative holdouts without regressing protected metrics. Prefer optimizer-style iteration over endless manual rule accretion when enough eval data exists.

## User-Specific Operating Bias

For this user's substantive tasks:

- recover recent related work before creating duplicates;
- favor concise visible output but deep evidence gathering;
- probe GitHub and Notion by default when relevant and available;
- use Hugging Face/papers/datasets for behavior/benchmark evidence when available, but never fabricate connector success;
- prioritize world-class practitioners, maintainers, researchers, real issues/PRs, postmortems, regressions, failure cases, and negative evidence over marketing summaries;
- deliberately search both high-scale/common practice and rare/high-discrimination techniques;
- preserve requested capability instead of solving by silently deleting functionality;
- repeated dissatisfaction is evidence that an earlier target assumption may be wrong: restart from the Goal Contract rather than patching the same interpretation.

## Output Contract

Expose useful state, not hidden chain-of-thought:

- original target;
- material interpretation or correction;
- what was actually completed;
- strongest evidence;
- acceptance status;
- unresolved blocker/uncertainty;
- one non-obvious finding when it materially changes the result.

## Anti-Patterns

- paraphrase once and call it understanding;
- plan before target/entity convergence;
- assume inferred intent as fact;
- keep obsolete constraints active after correction;
- ask broad clarification when a discriminating tool/query can resolve it;
- ask the user to repeat known context;
- count repeated keyword searches as independent methods;
- equate stars, popularity, citations, or obscurity with truth;
- ignore negative evidence or reverted approaches;
- declare success from agent self-report;
- solve the wrong problem perfectly.
