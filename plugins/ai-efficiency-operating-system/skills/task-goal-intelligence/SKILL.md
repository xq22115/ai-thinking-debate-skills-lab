---
name: task-goal-intelligence
description: Use when a substantive task could be misread because the real target, entity, constraints, hidden requirements, prior corrections, route ownership, or completion condition are ambiguous or easy to drift away from.
---

# Task Goal Intelligence — Plugin Projection

This is the lightweight routing projection of the repository's canonical `skills/skills/task-goal-intelligence/SKILL.md`. It must be useful on its own when the plugin is installed without loading the portable library.

## Core contract

Before material action, recover enough of the active Goal Contract to keep routing faithful:

- root goal and desired end state;
- hard constraints, negations, and protected capabilities;
- target identity and causal owner;
- acceptance tests and completion evidence plan;
- decision-critical unknowns;
- recent corrections and superseded constraints.

Do not call a fluent paraphrase proof of understanding.

## Interpretation and information gain

When materially different interpretations would cause different actions, preserve competing candidates long enough to test them. Prefer the next observation with the highest decision value: a tool call, runtime probe, repository read, history lookup, test, or one discriminating clarification.

If plausible interpretations share the same safe reversible next step, keep working without needless interruption.

## Semantic delta

Treat each substantive user correction as a state update. Mark superseded requirements obsolete instead of silently carrying them forward. A new correction outranks a stale summary.

## Active routing handoffs

Select the smallest specialist set that can advance the Goal Contract. Do not activate specialists merely because a noun appears.

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

## Composition discipline

Use at most three implicit skills in one phase. Prefer:

1. this goal gate;
2. one primary specialist;
3. `evidence-watchdog` when the task contains a state/completion claim.

Do not load every skill or every tool schema. Discover many, load few.

## Fallback/self-repair

A failed route is evidence about the route, not permission to change the root goal.

- after one retry without new evidence, change method or specialist;
- if a specialist is unavailable, fall back to the nearest base skill and continue collecting discriminating evidence;
- if host capability is missing, report the mismatch rather than fabricating execution;
- after repeated failure, route through `convergence-controller` and choose a materially different path;
- never declare success without the promised acceptance evidence.

## Output

Keep visible output compact: active goal, selected route, strongest evidence, acceptance state, blocker, and any route change that materially affects the result. Do not expose hidden chain-of-thought.
