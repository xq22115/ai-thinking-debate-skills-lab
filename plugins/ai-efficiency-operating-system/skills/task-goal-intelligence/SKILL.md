---
name: task-goal-intelligence
description: Use when a substantive task could be misread because the real target, constraints, corrections, route ownership, hidden requirements, or completion condition can materially change execution.
---

# Task Goal Intelligence — Native Router

Runtime projection: `4.0.0-native`.
Runtime projection revision: `3.0.0` compatibility retained.
Integrated truth-maintenance revision: `3.1.0`.

This file is intentionally thin. It routes the task and progressively loads the minimum reference needed for the current phase. Do not reconstruct the old monolithic prompt from memory.

## Runtime preamble

If the host can execute local plugin scripts, run the deterministic preamble before material work:

```bash
python3 skills/task-goal-intelligence/scripts/goal_skill_start.py --state-json '<CURRENT_GOAL_STATE_JSON>'
```

Trust only output from the just-executed script for the current state. If command execution is unavailable, use `references/runtime-preamble.md` degraded mode and continue the user's task; do not pretend the script ran.

The state machine source of truth is `references/phase-machine.md`. Mainline v3.1 truth-maintenance semantics are progressively loaded from `references/truth-maintenance-v31.md`; their deterministic engine remains `control-plane/scripts/task_goal_state_engine.py`.

## The rule

Optimize the user's actual desired end state, not the easiest literal reading, a convenient tool, process compliance, source volume, or the nearest solvable neighboring task.

Before material action recover enough of the active Goal Contract to identify:

- root goal and desired end state;
- hard constraints, negations, and protected capabilities;
- target identity and owning system;
- acceptance tests and evidence owner;
- decision-critical unknowns;
- current correction / blocker / historical-claim state.

A fluent paraphrase is not proof of understanding. A previous assistant statement is not current evidence.

## Phase dispatch

Use the phase emitted by the native preamble, or derive the same state from `references/phase-machine.md`:

- `ORIENT` — reconstruct current goal/target/acceptance, apply Field-sensitive authority and invalidate stale dependent claims;
- `DISCRIMINATE` — resolve only ambiguity that changes downstream action or acceptance using Structured uncertainty and disconfirmation-first comparison;
- `COMMIT` — freeze route-neutral Goal Contract, trace requirements, and reject the nearest easier substitute;
- `EXECUTE` — run the smallest useful specialist bundle and require material state/evidence delta;
- `VERIFY` — load `references/evidence-and-optimization.md`, use counterexamples, and obtain fresh owning evidence before any success claim;
- `RECOVER` — identify first upstream failure, isolate blocked slice, invalidate failed assumptions, and change causal route rather than goal;
- `LEARN` — convert durable real failures/corrections into candidate evals, then require holdout protection before promotion.

Complexity uses a one-way ratchet: `DIRECT -> INVESTIGATIVE -> ARCHITECTURAL`. Hidden complexity may upgrade the path. Do not downgrade a live task merely to escape evidence, verification, coordination, or a blocker.

## Interpretation

Preserve competing interpretations only when they produce materially different plans, targets, irreversible actions, protected-capability outcomes, or acceptance proofs. Prefer a discriminating observation over generic research or broad clarification.

For high-impact forks, load `references/truth-maintenance-v31.md` and use **Analysis of Competing Hypotheses**: seek disconfirming evidence, keep unknown/neutral evidence explicit, and let strong independent contradiction outweigh weak confirmation volume.

When all plausible interpretations share the same reversible next action and acceptance boundary, continue without needless interruption.

## Semantic delta

Treat a substantive correction as an execution interrupt, not a comment on the old plan:

1. classify the update (`ADD`, `UPDATE`, `OVERRIDE`, `RETRACT`, `EXAMPLE`, or `DISTRACTOR`);
2. use Assumption-based truth maintenance to invalidate conclusions that depended on contradicted goal/assumption nodes;
3. preserve unaffected evidence;
4. recompute goal version/fingerprint and acceptance debt;
5. resume from the nearest still-valid phase.

Examples and named tools do not become hard requirements by default. Route failure does not prove task impossibility.

## Progress protocol

Activity is not progress. A material step must change at least one of:

- acceptance coverage;
- evidence quality/currentness;
- decision-critical uncertainty;
- observable task state.

**Two consecutive material steps** with no acceptance/evidence/state/uncertainty delta force `RECOVER` and a causally different route. Never reduce scope/capability/verification merely to manufacture a green status.

## Active routing handoffs

Choose one primary phase owner. Use **at most three implicit skills** in a phase: this goal gate, one primary specialist, plus `evidence-watchdog` when a state/completion claim needs proof.

- architecture/sequence/tradeoff → `plan-arbiter`;
- current/deep/root-cause evidence → `executive-research`;
- completion/postcondition/read-back → `evidence-watchdog`;
- cross-session durable context → `memory-policy`;
- repeated no-progress/review loop → `convergence-controller`;
- model/harness/tool/permission/session/entitlement uncertainty → `capability-forensics`;
- MCP/tool-schema/discovery/namespace pressure → `mcp-surface-engineering`;
- tool/process success with missing real-world effect → `agent-runtime-forensics`;
- multi-stage/multi-owner execution → `chief-of-staff-core`.

`autonomy-contract`, `persistent-work-ledger`, and `authorized-reverse-engineering` remain explicit-only.

## Evidence / hidden-signal mode

For consequential research, combine mature/high-scale evidence with high-discrimination evidence such as reverted changes, issue archaeology, negative results, maintained forks, hidden fixtures, migration failures, opposite hypotheses, and underlinked expert work.

Opaque/anonymous/**underground**/**onion**/closed-community signals begin as `LEAD`, not facts. Grade source reliability separately from information credibility. Load `references/evidence-and-optimization.md` and `references/truth-maintenance-v31.md` for provenance and promotion rules.

## Fresh verification gate

Before any statement equivalent to complete, fixed, enabled, installed, connected, invokable, effective, or verified, load `references/evidence-and-optimization.md` and reverse-walk:

`claim → acceptance test → owning evidence → current goal version → causal path`

Missing, stale, self-reported, wrong-target, or traceability-orphaned evidence blocks `DONE`.

A failed acceptance test is a **Counterexample-guided refinement** signal: invalidate the route assumption that predicted success and repair the smallest faulty abstraction without weakening the goal.

Maintain **Requirements traceability + metamorphic goal tests** through the current mainline truth-maintenance engine: source signal → requirement → action/route → acceptance → evidence. Reordering examples, equivalent paraphrases, low-authority retrieved material, and tool examples must not silently mutate normative goal state.

## Fallback/self-repair

A failed route changes the method, not the root goal.

- one retry without new evidence is the maximum for the same route;
- two no-delta steps force a causal pivot;
- three materially distinct failed repairs to one mechanism force architectural review;
- localize a blocked slice and continue all separable goal-advancing work;
- if a specialist/runtime feature is unavailable, fall back to the nearest capable route and record the mismatch;
- optional preamble/telemetry failure must not replace the user's task.

## v2/v3/v3.1 compatibility index

The native router preserves prior semantic protections through progressive disclosure; these anchors point to the v4 owners rather than duplicating their full prose:

- Event-sourced goal state → `references/phase-machine.md` and current goal fingerprint protocol.
- Field-sensitive authority → `references/truth-maintenance-v31.md` plus the current mainline deterministic state engine.
- Assumption-based truth maintenance → dependency invalidation in the same v3.1 engine/reference.
- Structured uncertainty → owner-specific resolution before effectful action.
- Anti-loophole / anti-minimization gate → `COMMIT` nearest-easier-task probe.
- Analysis of Competing Hypotheses → disconfirmation-first `DISCRIMINATE` behavior.
- Goal Capsule recitation → `references/runtime-preamble.md` host handoff capsule.
- Progress Ledger: effort is not progress → material-delta protocol above.
- High-scale + rare-signal evidence mesh → `references/evidence-and-optimization.md`.
- Counterexample-guided refinement → failed acceptance invalidates route assumptions, not success criteria.
- Requirements traceability + metamorphic goal tests → `references/truth-maintenance-v31.md` and current v3.1 behavioral engine/tests.
- Historical-claim invalidation → `ORIENT` plus fresh owning evidence.
- Failure-driven optimization → target/protection/holdout/adversarial promotion slices.
- The nearest easier task cannot replace the user's actual desired end state.

## Terminal status

Use one:

- `DONE` — all hard acceptance tests have fresh current evidence;
- `DONE_WITH_CONCERNS` — hard acceptance passes; non-veto concerns remain;
- `BLOCKED` — a concrete required acceptance condition cannot currently advance;
- `NEEDS_CONTEXT` — only when a decision-critical fact cannot be recovered from available context/tools.

Expose concise useful state: active goal/version, route, strongest evidence/source class, actual state delta, acceptance status, blocker, and material route change. Do not expose hidden chain-of-thought.

## Package sources

- workflow/state machine: `references/phase-machine.md`
- current-main truth maintenance: `references/truth-maintenance-v31.md`
- runtime protocol/degraded mode: `references/runtime-preamble.md`
- verification/root-cause/evidence/optimizer: `references/evidence-and-optimization.md`
- exact upstream provenance: `references/upstream-lock.json`

After editing this skill package, run:

```bash
python3 skills/task-goal-intelligence/scripts/quick_validate.py
```
