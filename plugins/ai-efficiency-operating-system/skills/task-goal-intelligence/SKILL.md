---
name: task-goal-intelligence
description: Use when a substantive task could be misread because the real target, constraints, corrections, route ownership, hidden requirements, or completion condition can materially change execution.
---

# Task Goal Intelligence — Native Router

Runtime projection: `4.0.0-native`.

This file is intentionally thin. It routes the task and loads the minimum reference needed for the current phase. Do not reconstruct the old monolithic prompt from memory.

## Runtime preamble

If the host can execute local plugin scripts, run the deterministic preamble before material work:

```bash
python3 skills/task-goal-intelligence/scripts/goal_skill_start.py --state-json '<CURRENT_GOAL_STATE_JSON>'
```

Trust only output from the just-executed script for the current state. If command execution is unavailable, use `references/runtime-preamble.md` degraded mode and continue the user's task; do not pretend the script ran.

The state machine source of truth is `references/phase-machine.md`.

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

- `ORIENT` — reconstruct current goal/target/acceptance and invalidate stale historical claims;
- `DISCRIMINATE` — resolve only ambiguity that changes downstream action or acceptance;
- `COMMIT` — freeze route-neutral Goal Contract and reject the nearest easier substitute;
- `EXECUTE` — run the smallest useful specialist bundle and require material state/evidence delta;
- `VERIFY` — load `references/evidence-and-optimization.md` and obtain fresh owning evidence before any success claim;
- `RECOVER` — identify first upstream failure, isolate blocked slice, and change causal route rather than goal;
- `LEARN` — convert durable real failures/corrections into candidate evals, then require holdout protection before promotion.

Complexity uses a one-way ratchet: `DIRECT -> INVESTIGATIVE -> ARCHITECTURAL`. Hidden complexity may upgrade the path. Do not downgrade a live task merely to escape evidence, verification, coordination, or a blocker.

## Interpretation

Preserve competing interpretations only when they produce materially different plans, targets, irreversible actions, protected-capability outcomes, or acceptance proofs. Prefer a discriminating observation over generic research or broad clarification.

When all plausible interpretations share the same reversible next action and acceptance boundary, continue without needless interruption.

## Semantic delta

Treat a substantive correction as an execution interrupt, not a comment on the old plan:

1. classify the update (`ADD`, `UPDATE`, `OVERRIDE`, `RETRACT`, `EXAMPLE`, or `DISTRACTOR`);
2. invalidate conclusions that depended on contradicted goal/assumption nodes;
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

Two consecutive no-delta material steps force `RECOVER` and a causally different route. Never reduce scope/capability/verification merely to manufacture a green status.

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

Opaque/anonymous/underground/onion/closed-community signals begin as leads, not facts. Load `references/evidence-and-optimization.md` for provenance and promotion rules.

## Fresh verification gate

Before any statement equivalent to complete, fixed, enabled, installed, connected, invokable, effective, or verified, load `references/evidence-and-optimization.md` and reverse-walk:

`claim -> acceptance test -> owning evidence -> current goal version -> causal path`

Missing, stale, self-reported, or wrong-target evidence blocks `DONE`.

## Fallback/self-repair

A failed route changes the method, not the root goal.

- one retry without new evidence is the maximum for the same route;
- two no-delta steps force a causal pivot;
- three materially distinct failed repairs to one mechanism force architectural review;
- localize a blocked slice and continue all separable goal-advancing work;
- if a specialist/runtime feature is unavailable, fall back to the nearest capable route and record the mismatch;
- optional preamble/telemetry failure must not replace the user's task.

## v3 compatibility index

The native router preserves the prior semantic protections through progressive disclosure. These are compatibility anchors, not duplicated implementations:

- Runtime projection revision: `3.0.0` — superseded by `4.0.0-native`, retained so v3 protection tests remain meaningful.
- Event-sourced goal state → `references/phase-machine.md` and the current goal fingerprint protocol.
- Historical-claim invalidation → `ORIENT` plus fresh owning evidence.
- Anti-loophole / anti-minimization gate → `COMMIT` nearest easier task probe.
- Goal Capsule recitation → `references/runtime-preamble.md` host handoff capsule.
- Progress Ledger: effort is not progress → material-delta protocol above.
- Two consecutive material steps with no delta → `RECOVER` and causal pivot.
- High-scale + rare-signal evidence mesh → `references/evidence-and-optimization.md`.
- Opaque evidence begins at `LEAD` before corroboration/promotion.
- Failure-driven optimization → target/protection/holdout/adversarial promotion slices.
- Completion chain: claim → acceptance test → owning evidence → current goal version → causal path.
- The nearest easier task cannot replace the user's actual desired end state.

## Terminal status

Use one:

- `DONE` — all hard acceptance tests have fresh current evidence;
- `DONE_WITH_CONCERNS` — hard acceptance passes; non-veto concerns remain;
- `BLOCKED` — a concrete required acceptance condition cannot currently advance;
- `NEEDS_CONTEXT` — only when a decision-critical fact cannot be recovered from available context/tools.

Expose concise useful state: active goal/version, route, strongest evidence, actual state delta, acceptance status, blocker, and material route change. Do not expose hidden chain-of-thought.

## Package sources

- workflow/state machine: `references/phase-machine.md`
- runtime protocol/degraded mode: `references/runtime-preamble.md`
- verification/root-cause/evidence/optimizer: `references/evidence-and-optimization.md`
- exact upstream provenance: `references/upstream-lock.json`

After editing this skill package, run:

```bash
python3 skills/task-goal-intelligence/scripts/quick_validate.py
```
