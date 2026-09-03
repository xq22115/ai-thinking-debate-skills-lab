---
name: task-goal-intelligence
description: Use when a substantive task could be misread because the real target, entity, constraints, hidden requirements, prior corrections, route ownership, completion condition, or easier neighboring task could distort execution.
---

# Task Goal Intelligence — Plugin Projection

Runtime projection revision: `3.0.0`.

This is the lightweight auto-invoked projection of the repository's canonical `skills/skills/task-goal-intelligence/SKILL.md` plus the v3 extension contract. It must remain useful when the plugin is installed without loading the portable library.

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

## 1. Event-sourced goal state

Maintain `GOAL_VERSION`, `GOAL_FINGERPRINT`, and a compact `GOAL_EVENT_LOG` rather than repeatedly rewriting one summary until its provenance disappears.

Material events include `USER_REQUEST`, `ADD`, `UPDATE`, `OVERRIDE`, `RETRACT`, `CORRECTION`, `EVIDENCE`, `BLOCKER`, `ROUTE_CHANGE`, and `ACCEPTANCE_RESULT`.

For every correction or material new fact:

1. identify which goal/assumption nodes changed;
2. invalidate downstream conclusions that depended on superseded nodes;
3. preserve unaffected evidence and constraints;
4. recompute the winning interpretation, acceptance debt, and next action;
5. increment the goal version only for semantic changes, not cosmetic restatements.

### Historical-claim invalidation

Treat old completion/configuration/runtime claims as `HISTORICAL_CLAIM` until the current task can bind them to fresh evidence. Current owning-system read-back outranks prior prose, prior summaries, stale screenshots, and old agent self-report. If fresh evidence contradicts history, invalidate the historical claim immediately instead of defending it.

## 2. Anti-loophole / anti-minimization gate

Do not exploit imperfect wording, examples, incidental nouns, method suggestions, or omitted implementation detail to reduce the user's requested end state.

Distinguish:

- end state from suggested route;
- hard constraint from example;
- protected capability from optional implementation detail;
- blocker from replacement mission;
- inability of one route from impossibility of the task.

Before accepting a simpler interpretation, construct the strongest **nearest easier task** and ask whether the proposed action silently turns the real task into that easier substitute. Reject the substitution when it lowers capability, scope, verification, target identity, or acceptance criteria merely because it is easier to complete.

A route boundary or unavailable slice does not rewrite `ROOT_GOAL`. Isolate that slice, preserve the remaining acceptance contract, and continue every separable goal-advancing action that is still executable. Do not replace allowed task progress with generic process, policy, safety, ethics, or tool-compliance discussion when those are not themselves the user's task.

## 3. Interpretation tournament for planning utility

When materially different interpretations would produce materially different plans, preserve 3–5 candidate interpretations long enough to discriminate them. Score them by downstream planning utility, not paraphrase similarity.

For each serious candidate record:

- supporting and disconfirming evidence;
- required assumptions;
- action if true;
- consequence if wrong;
- acceptance proof if true;
- predicted user correction if wrong.

If plausible candidates share the same reversible next action and acceptance boundary, keep working without needless interruption. Prefer a tool/read-back/test/history observation with high decision value before asking a broad question.

## 4. Goal Capsule recitation

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

## 5. Progress Ledger: effort is not progress

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

Two consecutive material steps with no acceptance/evidence/state/uncertainty delta force a causally different route, hypothesis, instrument, decomposition, or verifier. Do not lower the target to manufacture progress.

## 6. Active specialist routing

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

## 7. High-scale + rare-signal evidence mesh

For consequential research, deliberately combine two different discovery pressures:

1. **high-scale evidence** — mature projects, production adoption, repeated independent experience, benchmarks, stable ecosystems;
2. **high-discrimination evidence** — rejected/reverted PRs, bug archaeology, negative results, maintained forks, obscure implementation notes, benchmark fixtures, migration breakage, opposite-hypothesis evidence, underlinked expert work.

Popularity is a scale signal, not proof. Obscurity is a discovery signal, not proof.

For opaque, anonymous, underground, onion, closed-community, leak, or otherwise hard-to-attribute signals in threat-intelligence/OSINT tasks, start the item as `LEAD`, not fact. Preserve source class, stable identifier/hash when available, first/last-seen timing, actor/source history, independent corroboration, contradiction status, confidence, and decision impact. Promote only through `CORROBORATED` → `REPRODUCIBLE` → `OWNING_SOURCE_VERIFIED` when evidence supports those states.

Rare evidence earns extra value only when it changes a live interpretation, resolves a contradiction, exposes mechanism/failure mode, or materially changes acceptance.

## 8. End-to-end acceptance before process scoring

Evaluate the black-box question first: **did the result satisfy the user's actual goal and acceptance tests?** Only after that use step-level diagnostics.

On failure identify the **first upstream failure** that made later work invalid or irrelevant. Fixing downstream polish while the first upstream failure remains unresolved does not count as a successful repair.

Before `PASS`, reverse-walk every material completion claim:

`claim → acceptance test → owning evidence → current goal version → causal path`.

If a link is missing, stale, self-reported, or bound to the wrong target/version, the claim is partial/unverified.

## 9. Failure-driven optimization

Turn real user corrections, false-completion traces, stale-history contradictions, unnecessary clarifications, neighboring-task substitutions, blocked-route abandonments, and capability regressions into regression cases.

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
- false-completion rate;
- protected-capability regression rate.

## 10. Fallback and recovery

A failed route is evidence about the route, not permission to change the root goal.

- after one retry without new evidence, change method or specialist;
- after two no-delta material steps, force a causally different route;
- if a specialist is unavailable, fall back to the nearest capable base skill and continue gathering discriminating evidence;
- if a host capability is missing, record that local mismatch and continue all separable work;
- after repeated failure, route through `convergence-controller` with the failure fingerprint and acceptance debt;
- never declare success without the promised current evidence.

## Output

Expose useful state, not hidden chain-of-thought: active goal/version, material correction, chosen route, strongest evidence, actual state change, acceptance state, blocker, and any route change that materially affects the result.
