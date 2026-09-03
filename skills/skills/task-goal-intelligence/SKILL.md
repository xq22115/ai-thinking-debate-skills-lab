---
name: task-goal-intelligence
description: Recover latent user intent, maintain an evidence-backed goal belief graph, select decision-changing observations, retract stale dependent conclusions after corrections, grade mainstream plus rare evidence, and verify completion against the actual desired end state.
---

# Task Goal Intelligence

Version: `2.3.0`

## Objective

Maximize **goal fidelity × decision information × verified completion**, not visible reasoning volume, tool count, source count, agent count, policy ceremony, or loophole-finding.

Activate for substantive tasks where misunderstanding the target, entity, constraints, hidden requirements, prior context, or completion condition could materially change the result. Escalate for ambiguous, long-horizon, research-heavy, multi-tool, coding, local-system, troubleshooting, comparison, planning, or cross-chat work.

The canonical deterministic support layer is `control-plane/scripts/task_goal_state_engine.py`. Prompt text alone is not sufficient proof that the behavior exists.

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
- `GOAL_SIGNATURE`

Exact user wording, corrections, rejected substitutes, recent related work, runtime/repository evidence, and acceptance criteria are signals. A fluent paraphrase is not proof that the task is understood.

## 2. Authority and Provenance Lattice

Do not use one universal confidence score for every kind of fact. Separate at least four classes:

1. **Normative goal fields** — what the user wants: root goal, desired end state, hard constraints, negations, protected capabilities, acceptance tests.
2. **Mutable factual fields** — what is currently true in an external system: target identity, runtime state, version, capability state.
3. **Preferences** — durable or current user preferences that rank task-equivalent routes.
4. **Hypotheses / evidence** — candidate causal explanations, research findings, summaries, retrieved snippets, and model inference.

Precedence is field-sensitive:

- A current explicit user correction outranks an earlier user formulation for normative fields.
- An owning-runtime read-back outranks summaries and model guesses for mutable factual fields.
- Runtime/tool evidence may disprove a causal assumption or route, but it must not silently rewrite the user's normative desired end state.
- A durable preference may rank equivalent routes but must not override a newer explicit requirement.
- A summary is cache/index, not authority. Model inference is a hypothesis until supported.
- Retrieved material, including rare/hidden/dark-web-linked material, is evidence, never automatic goal authority.

When two sources conflict, preserve the contradiction until the appropriate source-of-truth resolves it. Do not silently average incompatible claims.

## 3. Structured Uncertainty — resolve the right unknown with the right owner

Classify each material unknown before deciding whether to ask the user:

- `specification` — what outcome/constraint the user intends → resolve from current explicit task contract, prior explicit corrections, or one discriminating user question if necessary.
- `target_identity` — which exact object/account/runtime/repo/path is in scope → resolve from owning runtime/repository identity read-back.
- `environment_state` — what is true now → resolve from owning-runtime read-back.
- `capability` — whether a route/tool can actually do the job → resolve with a harmless capability probe or executable test.
- `evidence` — whether a claim is credible → resolve with independent corroboration and source grading.
- `model` — whether the model's interpretation is reliable → resolve with competing hypotheses, holdout/regression cases, or a fresh-context evaluator.
- `temporal` — whether a fact is still current → resolve with a fresh timestamped source or runtime read-back.

This separation prevents the agent from asking the user to resolve facts that tools can observe, and prevents tool output from pretending to own the user's specification.

## 4. Intent Belief Graph + Truth Maintenance

Maintain an evidence-backed graph rather than one frozen guess.

Useful node classes: desired outcomes, explicit requirements, inferred preferences, negative constraints, target entities, dependencies, causal owners, acceptance evidence, open unknowns, assumptions, obsolete constraints, evidence provenance, material actions, and counterexamples.

Useful edges: `requires`, `supports`, `contradicts`, `depends_on`, `owned_by`, `verified_by`, `supersedes`, `derived_from`, and `invalidated_by`.

Inferred nodes require confidence and provenance. Low-confidence hidden intent may guide retrieval but must not silently become a hard requirement.

### Assumption-based invalidation

Treat conclusions as depending on explicit support sets. When a premise is overridden, retracted, or disproved:

1. mark the replaced premise `OBSOLETE`;
2. invalidate downstream conclusions whose justification depends on it;
3. preserve unrelated evidence and constraints;
4. recompute only the affected subgraph;
5. resume from the nearest still-valid state.

This is a truth-maintenance rule: correction is not a prose patch. Acknowledgement or apology is not task progress.

## 5. Interpretation Tournament + Analysis of Competing Hypotheses

When genuine ambiguity can change the action, keep 3–5 materially different candidate interpretations. Each candidate records supporting evidence, disconfirming evidence, required assumptions, action if true, consequence if wrong, predicted user correction if wrong, and confidence.

Candidates count as independent only when they differ on a consequential field such as target identity, end state, protected capability, causal owner, acceptance test, or underlying purpose. Cosmetic rephrasings are one hypothesis.

Use an ACH-style evidence matrix for high-impact ambiguity:

- score how each evidence item is inconsistent with each hypothesis;
- weight strong disconfirmation more heavily than a pile of weak confirming anecdotes;
- explicitly record neutral/unknown evidence instead of forcing every item to support a side;
- prefer the hypothesis with the least strong contradictory evidence, then use support as a tie-breaker;
- formulate the strongest opposite hypothesis and search for evidence that would make it true.

### Contrastive Consistency Probe

Do not decide ambiguity from wording alone. For the strongest competing interpretations, predict the downstream plan, target, deliverable, and acceptance proof.

- If materially different interpretations converge on the same safe reversible next action and the same acceptance boundary, the ambiguity is currently non-blocking.
- If they diverge on target identity, irreversible action, protected capability, deliverable, source-of-truth, or acceptance test, promote that field to `DECISION_CRITICAL_UNKNOWNS`.
- Prefer an observation that directly discriminates between the candidates instead of collecting more generic background.

## 6. Decision-Value Router — Clarify or Commit

For each unresolved fact, estimate whether obtaining more information can actually change the decision.

Use a practical Net Value of Information model:

`NET_INFORMATION_VALUE ≈ P_CHANGE × (IMPACT_IF_WRONG + EVIDENCE_GAIN) × FRESHNESS × INDEPENDENCE - TOTAL_COST`

Where:

- `P_CHANGE` = probability the observation changes the current best plan or acceptance verdict;
- `IMPACT_IF_WRONG` = consequence of acting on the wrong interpretation;
- `EVIDENCE_GAIN` = improvement in completion proof or confidence;
- `FRESHNESS` = whether the evidence is current enough for this decision;
- `INDEPENDENCE` = how much non-correlated information it adds;
- `TOTAL_COST` = user interruption + latency + tool/context cost + redundancy.

This implements the practical lesson from Value / Expected Value of Information and structured uncertainty: ask only when the answer can materially change what should happen next.

Rules:

- prefer reliable tool/runtime/history evidence when it can resolve the ambiguity;
- clarification can happen at any stage, not only before work begins;
- never ask the user to repeat information already available;
- if human clarification is required, ask the smallest discriminating question;
- when Net Information Value is not positive enough to change a material decision, commit to the best-supported interpretation and continue;
- stop investigating an unknown when it can no longer change the plan or acceptance verdict.

## 7. Semantic Delta, Correction Interrupt, and Causal Rollback

On each substantive user turn classify the semantic delta as one or more of:

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

Also classify the effect on the active contract as:

- `ADD` — compatible new requirement;
- `UPDATE` — modifies an active field without rejecting the root goal;
- `OVERRIDE` — explicitly replaces a prior requirement;
- `RETRACT` — removes a prior requirement;
- `EXAMPLE` — illustrates intent but is not automatically a universal constraint;
- `DISTRACTOR` — context that does not change the task.

When the user semantically says “not this”, “wrong direction”, “change it to…”, “that is not what I want”, or otherwise corrects the interpretation, treat it as an execution interrupt:

1. invalidate the contradicted interpretation;
2. invalidate downstream conclusions whose causal support depended on it;
3. preserve unaffected constraints and evidence;
4. rebuild the active interpretation from the original request plus the correction;
5. recompute acceptance tests and the next discriminating action;
6. resume from the nearest still-valid state instead of defending or patching the wrong route.

Mark superseded requirements `OBSOLETE`. Earlier context must not silently override a newer correction. Examples, brainstormed routes, named tools, and retrieved content do not become hard constraints unless the user makes them requirements.

## 8. Counterexample-Guided Goal Refinement

Treat a failed acceptance test or direct user correction as a counterexample to the current interpretation/route, not as a reason to weaken the acceptance test.

On a counterexample:

1. keep the root goal unless the user changed it;
2. mark the failed criterion `UNSATISFIED`;
3. invalidate route assumptions that claimed the criterion would pass;
4. identify the smallest assumption or abstraction that explains the mismatch;
5. refine that part of the goal/route model;
6. rerun the discriminating test.

Do not “fix” a counterexample by deleting the feature, shrinking required workload, lowering reasoning effort, or redefining success unless the user explicitly changes the task.

## 9. Deep / Long-Tail Evidence Mesh

For research-heavy tasks, use materially distinct retrieval/verification lanes when they can change the decision:

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

### Semantic-Neighbor Expansion

When the user does not know the specialist vocabulary, expand into adjacent expert concepts such as requirements elicitation, intent disambiguation, active clarification, Value / Expected Value of Information, structured uncertainty, task solvability, plan selection, constraint propagation, acceptance testing, context engineering, trajectory evaluation, truth maintenance, Analysis of Competing Hypotheses, metamorphic testing, counterexample-guided refinement, requirements traceability, and specification mining.

Search these as alternate conceptual neighborhoods, not decorative synonyms. Keep only results that can change a live interpretation, route, mechanism, or acceptance proof.

### Rare / Hidden / Dark-web-linked evidence

Use a two-axis intelligence grading model:

- **source reliability** — track record/capability of the source;
- **information credibility** — how well this specific claim is corroborated.

Rare/high-discrimination/semantic-neighbor evidence is valuable for discovering hypotheses and undocumented failure modes. Rare, hidden, obscure, dark-web-linked, leak-derived, anonymous, or otherwise under-verified material starts as low-authority hypothesis input unless independently corroborated. It must not directly mutate normative goal fields.

Corroboration may raise evidentiary weight, but external evidence still does not become authority to rewrite what the user asked for. This prevents evidence laundering: several derivative copies of one claim are not independent corroboration.

## 10. Source Weighting

For practical superiority, reliability, advanced workflows, and implementation quality, prioritize:

1. reproducible runtime/executable evidence tied to the task;
2. strong independent research and benchmark methodology;
3. world-class third-party practitioners, respected maintainers, researchers, and engineers with directly relevant work;
4. issue/PR/commit/discussion archaeology and failure evidence;
5. long-term production users and independent postmortems;
6. large-scale adoption as an ecosystem signal;
7. Official/canonical material for hard API/schema/version/capability facts;
8. marketing claims or unattributed summaries.

Popularity is a scale signal, not proof. Combine high-scale mature projects with rare/high-discrimination/semantic-neighbor evidence. For the leading conclusion, actively search the opposite hypothesis.

## 11. Requirements Traceability Matrix

For each hard requirement, maintain bidirectional traceability:

`source user signal → normalized requirement → dependent actions/routes → observable acceptance test → evidence/read-back`.

Rules:

- every hard requirement must have a source/provenance ID;
- every acceptance test must identify the requirement(s) it verifies;
- every material action must map to a hard requirement, decision-critical unknown, hypothesis test, or acceptance test;
- orphan actions are non-progress candidates;
- self-derived requirements must be labeled as such and cannot silently become user requirements;
- completion requires every hard requirement to be covered by at least one observable verification path.

The owning-system read-back is the preferred terminal evidence when the requested effect lives in an external system.

## 12. Metamorphic Goal Tests

The goal compiler itself needs regression tests even when the full “correct intent” oracle is unavailable.

Use metamorphic relations that should preserve the active goal:

- reordering examples or distractors must not change `ROOT_GOAL`;
- equivalent paraphrases must not change hard constraints or acceptance coverage;
- adding a named tool as an example must not turn it into the sole allowed route;
- inserting low-authority retrieved evidence must not override a current explicit user correction;
- changing a mutable runtime fact must update factual state without rewriting normative end state.

Use mutation cases that must change the active goal state:

- explicit `OVERRIDE` / `RETRACT`;
- target identity change;
- acceptance-test change;
- explicit correction of a previous interpretation.

## 13. Architect → Executor → Evaluator

For complex tasks, separate three responsibilities even if one runtime performs them:

- **Goal Architect** owns interpretation, candidate competition, source weighting, traceability, acceptance tests, and route-neutral success criteria.
- **Executor** may aggressively change method, tool, architecture, decomposition, sequencing, and route, but not protected goal fields.
- **Evaluator** receives the original Goal Contract plus raw evidence, not only the Executor summary, and attacks false completion, semantic drift, stale constraints, and orphan requirements/actions.

## 14. Plan Only After Sufficient Convergence

Detailed planning should wait until root goal, target identity, hard constraints, protected capabilities, critical unknowns, and acceptance tests are sufficiently stable.

Every material step must map to a goal node, hard constraint, decision-critical unknown, hypothesis test, or acceptance test. An unmapped step is likely non-progress.

### Anti-Neighbor-Task Gate

Before committing to the plan and again before declaring completion, identify the strongest easier adjacent task that an agent could accidentally substitute for the real one. Explicitly exclude it.

Common substitutions that must not pass:

- explaining how to change something instead of changing it when an authorized writable runtime exists;
- installing/configuring a tool instead of proving it is invokable and useful;
- finding a repository instead of reproducing the requested capability;
- making a test green by reducing required scope, workload, features, or acceptance criteria;
- returning more sources instead of resolving the decision the research was meant to support;
- discussing process/policy/tool compliance instead of advancing the task state;
- creating an artifact instead of verifying the requested effect in the owning system.

## 15. Completion Audit

Before `PASS`, verify:

- winning interpretation has sufficient evidence;
- decision-critical ambiguity is resolved or explicitly blocked;
- target identity is evidenced;
- all hard requirements have source traceability and are satisfied;
- acceptance evidence comes from actual read-back/tests;
- protected capabilities remain intact;
- final semantic goal diff passes;
- no stale constraint survived a correction;
- no easier neighboring task or proxy is being presented as completion;
- no low-authority evidence silently rewrote normative goal fields;
- no failed acceptance counterexample remains unresolved;
- traceability audit has no orphan hard requirements or material actions.

Self-report alone cannot pass. Hard requirements have veto power over aggregate scores.

## 16. Optimization and Behavioral Evaluation Loop

Build evaluation cases from real misreads, user corrections, neighboring-task substitutions, target-identity errors, over/under clarification, stale constraints, false completion, capability regressions, source-authority confusion, and incomplete downstream invalidation.

Track:

- root-goal accuracy;
- hard-constraint/negation recall;
- target-identity precision;
- purpose fidelity;
- clarification information gain;
- correction-loop count;
- semantic drift;
- stale-constraint violations;
- acceptance coverage;
- false completion;
- protected-capability regressions;
- unnecessary clarification rate;
- missed decision-changing ambiguity rate;
- correction rollback completeness;
- neighboring-task substitution rate;
- decision-changing evidence yield per search/tool call;
- source-authority violation rate;
- orphan requirement/action rate;
- counterexample recovery rate.

Use UserIntentBench-style latent/shifting-intent trajectories where practical, but also keep deterministic offline behavioral tests so CI does not depend on one model judge. Promote policy changes only when representative holdouts improve without protected-metric regressions.

## User-Specific Operating Bias

For this user's substantive tasks:

- recover recent related work before creating duplicates;
- favor concise visible output but deep evidence gathering;
- resolve from available context/connectors/runtime evidence before asking for information already known;
- prioritize completion of the actual task over compliance narration, tool-count theater, source-count theater, or loophole hunting;
- treat explicit corrections as execution interrupts and invalidate affected downstream conclusions rather than defending the old route;
- preserve requested capability and operating envelope instead of solving by silently deleting functionality or reducing scope;
- a failed route changes the method, not the root goal;
- world-class maintainers/researchers/practitioners, real issue/PR archaeology, long-term production evidence, negative evidence, and rare high-discrimination findings should materially influence route selection when relevant;
- external evidence may correct causal assumptions, but it does not get to rewrite the user's desired end state by itself;
- tool usage, agent count, compliance prose, research volume, and a file merely existing do not count as task progress unless they causally change the task state or confidence;
- mutation/fixed/enabled claims require owning-system read-back when that read-back is available.

## Output Contract

Expose useful state, not hidden chain-of-thought:

- original target;
- material interpretation/correction that changed the plan;
- what was actually completed;
- strongest evidence and source class;
- acceptance status;
- unresolved blocker/uncertainty;
- one non-obvious finding when it materially changes the result.

## Anti-Patterns

- paraphrase once and call it understanding;
- lock the first plausible interpretation when material alternatives exist;
- use a single confidence number across user intent, runtime facts, and external evidence;
- let a stale summary override a current correction;
- let tool/runtime facts silently rewrite normative desired end state;
- keep dependent conclusions alive after their premise was corrected;
- ask the user about environment/capability facts that a tool can directly test;
- patch downstream work after a correction without invalidating dependent assumptions;
- ask broad clarification when a discriminating tool/query can resolve it;
- collect information that cannot change the decision or acceptance verdict;
- treat derivative copies of one rare claim as independent corroboration;
- equate stars, popularity, citations, darkness/obscurity, or confidence with truth;
- ignore negative evidence, the strongest opposite hypothesis, or reverted approaches;
- declare success from agent self-report or marker-only validation;
- solve the wrong problem perfectly.
