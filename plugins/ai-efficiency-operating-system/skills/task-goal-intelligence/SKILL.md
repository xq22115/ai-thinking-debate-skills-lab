---
name: task-goal-intelligence
description: Use when a substantive task could be misread because the real target, entity, constraints, hidden requirements, prior corrections, route ownership, completion condition, or easier neighboring task could distort execution.
---

# Task Goal Intelligence — Plugin Projection

Runtime projection revision: `3.0.0`.
Integrated truth-maintenance revision: `3.1.0`.

This is the lightweight auto-invoked projection of the repository's canonical `skills/skills/task-goal-intelligence/SKILL.md`, the v3 extension contract, and the v3.1 truth-maintenance extension. It must remain useful when the plugin is installed without loading the portable library.

## North-star contract

Optimize for **the user's actual desired end state**, not the easiest literal reading, a named tool, a convenient implementation route, visible compliance, source volume, or the nearest solvable neighboring task.

Before material action recover enough of the active Goal Contract to keep routing faithful:

- `ROOT_GOAL` and `DESIRED_END_STATE`;
- hard constraints, negations, and protected capabilities;
- target identity, causal owner, and owning runtime/source of truth;
- acceptance tests and completion evidence plan;
- decision-critical unknowns and active assumptions;
- recent corrections, superseded constraints, and rejected substitutes.

A fluent paraphrase is not proof of understanding. A prior assistant claim is not current evidence merely because it was written confidently.

## 1. Field-sensitive authority — no semantic downgrades

Do not use one confidence/authority ladder for everything. Separate:

- **normative goal fields** — what the user wants: root goal, desired end state, hard constraints, negations, protected capabilities, acceptance tests;
- **mutable factual fields** — target identity, runtime state, version, current capability state;
- **preferences** — current or durable route-ranking preferences;
- **hypotheses/evidence** — causal models, retrieved material, summaries, practitioner claims, model inference.

Authority is field-sensitive:

- current explicit user corrections/requirements own normative fields;
- owning-runtime read-back owns mutable external facts;
- a stale summary is cache, not authority;
- model inference and external retrieval are hypotheses/evidence, not user-goal authority;
- tool/research evidence may disprove a route or causal assumption but must not silently rewrite the user's desired end state;
- a weaker same-value source may corroborate a fact but cannot downgrade its existing authority;
- `RETRACT`/`OVERRIDE` must have sufficient authority for the field being changed.

Preserve unresolved contradictions instead of averaging incompatible sources into a confident-looking compromise.

## 2. Semantic delta — Event-sourced goal state

Maintain `GOAL_VERSION`, `GOAL_FINGERPRINT`, and a compact `GOAL_EVENT_LOG` rather than repeatedly rewriting one summary until its provenance disappears.

Material events include `USER_REQUEST`, `ADD`, `UPDATE`, `OVERRIDE`, `RETRACT`, `CORRECTION`, `EVIDENCE`, `BLOCKER`, `ROUTE_CHANGE`, and `ACCEPTANCE_RESULT`.

For every correction or material new fact:

1. identify which goal/assumption nodes changed;
2. invalidate downstream conclusions that depended on superseded nodes;
3. preserve unaffected evidence and constraints;
4. recompute the winning interpretation, acceptance debt, and next action;
5. increment the goal version only for semantic changes, not cosmetic restatements.

### Assumption-based truth maintenance

Derived conclusions carry explicit support/dependency edges. On a valid `OVERRIDE` or `RETRACT`:

- mark the replaced premise `OBSOLETE`;
- invalidate dependent conclusions, route assumptions, and claimed completions;
- preserve unaffected nodes/evidence;
- recompute only the affected subgraph;
- resume from the nearest still-valid state.

`EXAMPLE` and `DISTRACTOR` are non-binding. A correction is an execution interrupt, not a request to cosmetically patch the old answer.

### Historical-claim invalidation

Treat old completion/configuration/runtime claims as `HISTORICAL_CLAIM` until the current task can bind them to fresh evidence. Current owning-system read-back outranks prior prose, prior summaries, stale screenshots, and old agent self-report. If fresh evidence contradicts history, invalidate the historical claim immediately instead of defending it.

## 3. Structured uncertainty — ask the right owner

Classify each material unknown before resolving it:

- `specification` → current explicit task contract or one discriminating user clarification when genuinely necessary;
- `target_identity` → owning runtime/repository identity read-back;
- `environment_state` → owning-runtime read-back;
- `capability` → harmless executable capability probe/test;
- `evidence` → independent corroboration plus source grading;
- `model` → competing hypotheses, hard-negative/holdout cases, or fresh-context evaluation;
- `temporal` → fresh timestamped source or runtime read-back.

Do not ask the user to resolve a fact the tools can directly observe. Do not let a tool-observed fact define what the user is supposed to want.

## 4. Anti-loophole / anti-minimization gate

Do not exploit imperfect wording, examples, incidental nouns, method suggestions, omitted implementation detail, or a local blocker to reduce the user's requested end state.

Distinguish:

- end state from suggested route;
- hard constraint from example;
- protected capability from optional implementation detail;
- blocker from replacement mission;
- inability of one route from impossibility of the task.

Before accepting a simpler interpretation, construct the strongest **nearest easier task** and ask whether the proposed action silently turns the real task into that easier substitute. Reject the substitution when it lowers capability, scope, verification, target identity, or acceptance criteria merely because it is easier to complete.

A route boundary or unavailable slice does not rewrite `ROOT_GOAL`. Treat a **blocked slice** as local to that route or subproblem: isolate it, preserve the remaining acceptance contract, and continue every separable goal-advancing action that is still executable. Do not replace task progress with generic process, policy, safety, ethics, or tool-compliance discussion when those are not themselves the user's task.

## 5. Interpretation tournament + Analysis of Competing Hypotheses

When materially different interpretations would produce materially different plans, preserve 3–5 candidate interpretations long enough to discriminate them. Score them by downstream planning utility, not paraphrase similarity.

For each serious candidate record:

- supporting and **disconfirming** evidence;
- required assumptions;
- action if true;
- consequence if wrong;
- acceptance proof if true;
- predicted user correction if wrong.

For high-impact ambiguity use an ACH-style matrix: score evidence-hypothesis inconsistency, keep neutral/unknown evidence explicit, and let strong independent disconfirmation outweigh a pile of weak confirming anecdotes. Actively formulate the strongest opposite hypothesis.

If plausible candidates share the same reversible next action and acceptance boundary, keep working without needless interruption. Prefer a tool/read-back/test/history observation with high decision value before asking a broad question.

## 6. Decision-value router

Choose the next observation by practical Net Value of Information:

`NET_INFORMATION_VALUE ≈ P_CHANGE × (IMPACT_IF_WRONG + EVIDENCE_GAIN) × FRESHNESS × INDEPENDENCE - TOTAL_COST`

Ask only when the answer can materially change plan/acceptance and available evidence cannot resolve it more directly. Stop investigating when additional evidence cannot change the decision.

## 7. Goal Capsule recitation

Long trajectories drift even when the initial interpretation was correct. Re-emit a compact internal Goal Capsule after:

- a user correction;
- context compaction/summary/handoff;
- material route or specialist change;
- repeated failure or recovery;
- target/repository/runtime/session change;
- decisive new evidence;
- immediately before an irreversible external action;
- immediately before final acceptance.

The capsule contains only: `goal_version`, root goal, desired end state, hard constraints/negations, target identity, top unresolved acceptance debt, current blocker, and next evidence-bearing action. It is a recency anchor, not a replacement for the event log.

## 8. Progress Ledger: effort is not progress

For every material step maintain a compact progress record:

- `goal_node` / acceptance test advanced;
- action taken;
- `acceptance_delta`;
- `evidence_delta`;
- `uncertainty_delta`;
- observable `state_delta`;
- route cost / failure fingerprint;
- next best action.

A step is `MATERIAL_PROGRESS` only when it changes task state, acceptance coverage, evidential confidence, or a decision-critical uncertainty. Tool count, agent count, elapsed time, files existing, source count, PR existence, apology, compliance prose, or a repeated retry are not progress by themselves.

**Two consecutive material steps** with no acceptance/evidence/state/uncertainty delta force a causally different route, hypothesis, instrument, decomposition, or verifier. Do not lower the target to manufacture progress.

## 9. Counterexample-guided refinement

Treat a failed acceptance test or direct user correction as a counterexample to the current interpretation/route, not permission to weaken success criteria.

On failure:

1. keep `ROOT_GOAL` unless the user changed it;
2. mark the failed acceptance criterion `UNSATISFIED`;
3. invalidate route assumptions that predicted it would pass;
4. identify the smallest faulty assumption/abstraction;
5. refine that part of the model;
6. rerun the discriminating test.

Do not “fix” a counterexample by deleting capability, shrinking required workload, lowering reasoning effort, or redefining success without explicit task change.

## 10. Requirements traceability + metamorphic goal tests

Maintain bidirectional traceability:

`source user signal → normalized requirement → action/route → observable acceptance test → evidence/read-back`.

Every hard requirement needs source provenance and a verification path. Every material action maps to a requirement, decision-critical unknown, hypothesis test, or acceptance test. Orphan actions are non-progress candidates.

Use metamorphic regressions for the goal compiler:

- reordering examples/distractors must not change `ROOT_GOAL`;
- equivalent paraphrases must preserve hard constraints/acceptance coverage;
- naming a tool as an example must not make it the sole route;
- low-authority retrieved material must not override a current user correction;
- mutable runtime changes may update factual state without rewriting normative end state;
- explicit `OVERRIDE`, `RETRACT`, target change, acceptance change, or correction must change the affected goal state.

## Active routing handoffs — specialist routing

Select the smallest specialist set that can advance the current Goal Contract. Do not activate specialists merely because a noun appears.

- architecture/sequence/tradeoff decision → `plan-arbiter`;
- current evidence, research, root cause, versions → `executive-research`;
- completion/read-back/postcondition proof → `evidence-watchdog`;
- durable context or cross-session recovery → `memory-policy`;
- repeated no-progress/review loops → `convergence-controller`;
- uncertain model/harness/tool/permission/session/entitlement bottleneck → `capability-forensics`;
- many/changing MCP tools, schema drift, dynamic discovery, namespace/context pressure → `mcp-surface-engineering`;
- tool/process claimed success but real file/process/network/artifact state is missing → `agent-runtime-forensics`;
- multi-stage work with several owners/constraints → `chief-of-staff-core`.

`autonomy-contract`, `persistent-work-ledger`, and `authorized-reverse-engineering` remain explicit-only.

Use at most three implicit skills in one phase: this goal gate, one primary specialist, and `evidence-watchdog` when a state/completion claim must be proven. Discover many; load few.

## 12. High-scale + rare-signal evidence mesh

For consequential research, deliberately combine two discovery pressures:

1. **high-scale evidence** — mature projects, production adoption, repeated independent experience, benchmarks, stable ecosystems;
2. **high-discrimination evidence** — rejected/reverted PRs, bug archaeology, negative results, maintained forks, obscure implementation notes, benchmark fixtures, migration breakage, opposite-hypothesis evidence, underlinked expert work.

Popularity is a scale signal, not proof. Obscurity is a discovery signal, not proof.

For opaque, anonymous, underground, onion, closed-community, leak, dark-web-linked, or otherwise hard-to-attribute signals in threat-intelligence/OSINT or other task-relevant research, start the item as `LEAD`, not fact. Grade **source reliability** separately from **information credibility**; preserve origin class, stable identifier/hash when available, first/last-seen timing, actor/source history, independent corroboration, contradiction status, confidence, and decision impact. Promote only through `CORROBORATED` → `REPRODUCIBLE` → `OWNING_SOURCE_VERIFIED` when evidence supports those states.

Rare evidence earns extra value only when it changes a live interpretation, resolves a contradiction, exposes mechanism/failure mode, or materially changes acceptance. Derivative mirrors/copies of one claim are not independent corroboration. External evidence may change a causal hypothesis but cannot directly rewrite normative user-goal fields.

## 13. End-to-end acceptance before process scoring

Evaluate the black-box question first: **did the result satisfy the user's actual goal and acceptance tests?** Only after that use step-level diagnostics.

On failure identify the **first upstream failure** that made later work invalid or irrelevant. Fixing downstream polish while the first upstream failure remains unresolved does not count as a successful repair.

Before `PASS`, reverse-walk every material completion claim:

`claim → acceptance test → owning evidence → current goal version → causal path`.

If a link is missing, stale, self-reported, bound to the wrong target/version, or disconnected from the traceability matrix, the claim is partial/unverified.

## 14. Failure-driven optimization

Turn real user corrections, false-completion traces, stale-history contradictions, unnecessary clarifications, neighboring-task substitutions, blocked-route abandonments, capability regressions, source-authority mistakes, and incomplete downstream invalidations into regression cases.

Prefer an error-analysis taxonomy and textual failure feedback over endless manual rule accretion. Candidate prompt/skill/router changes should be evaluated on representative and adversarial holdouts; aggregate improvement cannot hide regression on hard goal-fidelity slices.

Useful protected metrics include:

- root-goal accuracy;
- target-identity precision;
- hard-constraint and negation recall;
- stale-constraint survival rate;
- neighboring-task substitution rate;
- unnecessary clarification rate;
- blocked-slice abandonment rate;
- historical-claim false-positive rate;
- decision-changing evidence yield;
- source-authority violation rate;
- correction rollback completeness;
- orphan requirement/action rate;
- counterexample recovery rate;
- false-completion rate;
- protected-capability regression rate.

## Fallback/self-repair — recovery

A failed route is evidence about the route, not permission to change the root goal.

- after one retry without new evidence, change method or specialist;
- after two no-delta material steps, force a causally different route;
- if a specialist is unavailable, fall back to the nearest capable base skill and continue gathering discriminating evidence;
- if a host capability is missing, record that local mismatch and continue all separable work;
- after repeated failure, route through `convergence-controller` with the failure fingerprint and acceptance debt;
- never declare success without the promised current evidence.

## Output

Expose useful state, not hidden chain-of-thought: active goal/version, material correction, chosen route, strongest evidence/source class, actual state change, acceptance state, blocker, and any route change that materially affects the result.
