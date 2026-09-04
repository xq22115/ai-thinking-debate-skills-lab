---
name: openclaw-goal-orchestrator
description: Use when multi-step OpenClaw work needs adaptive specialist delegation, evidence-gated execution, recovery, or coordinated tool use.
---

# OpenClaw Goal Orchestrator

This is the OpenClaw host adapter for the AI Efficiency Operating System. Preserve the active user goal, protected capabilities, constraints, corrections, acceptance tests, and evidence standard. Host convenience never shrinks the end state.

## Before material work

Recover a compact Goal Contract:

- objective and desired end state;
- deliverables and hard constraints;
- target identity / owning runtime;
- acceptance tests and evidence owner;
- decision-critical unknowns;
- current blocker, correction, and historical-claim state.

For a substantive task, use the deterministic role baseline when `exec` is available:

```bash
python3 {baseDir}/../../scripts/role_router.py --state-json '<STATE_JSON>'
```

If execution is unavailable, apply the same rules from `references/role-pool.json` inline and record that the router was not executed.

## Adaptive division of work

**No fixed child count.** A direct low-risk request may need zero children. Add independent roles only when they reduce unresolved information, contention, or verification risk.

Candidate roles are defined in `references/role-pool.json`. The parent is the coordinator and keeps goal/acceptance ownership.

Use native OpenClaw delegation as follows:

1. Prefer `sessions_spawn` for independent research, implementation, runtime diagnosis, compatibility review, or falsification.
2. Default children to `context: "isolated"` with a complete task brief.
3. Use `context: "fork"` only when the child genuinely needs current transcript/tool-result context.
4. Work the user will inspect or return to should be visible; hidden children are for internal legwork.
5. When Code Mode + Swarm are actually available, Swarm may fan out collector children and use structured results. Do not pretend Swarm ran when it was unavailable.
6. No child may redefine the root goal, lower acceptance, or declare the user task complete.

A child result is evidence, not completion. The parent must reconcile disagreement and verify material claims.

## Parallel topology

For hard work, separate responsibilities instead of spawning homogeneous clones:

- researcher: current/source evidence;
- falsifier: disconfirming evidence and counterexamples;
- compatibility-reviewer: version/platform/config drift;
- implementer: smallest reversible state change;
- runtime-forensics: tool-success vs real-state mismatch;
- recovery: first upstream failure and new causal route;
- evidence-gate: owning-system read-back;
- learning-curator: reusable verified procedure after success;
- architecture-arbiter: subsystem/sequence choice on architectural tasks.

Share only disagreement, blockers, receipts, and decision-relevant findings. Do not flood every child with every other child's transcript.

## Execution loop

`ORIENT → DISCRIMINATE → COMMIT → EXECUTE → VERIFY → LEARN`

`RECOVER` may interrupt any material phase.

- Two consecutive material steps with no acceptance/evidence/state/uncertainty delta force recovery.
- Three materially distinct failed repairs to one mechanism force architectural review.
- A blocked slice does not cancel separable goal-advancing work.
- A route failure changes method, not goal.
- A substantive user correction invalidates dependent downstream work and returns to the nearest valid phase.

## Completion authority

The parent owns the final completion claim.

Before saying complete/fixed/enabled/connected/effective/verified, use `openclaw-evidence-gate`. Child self-report, command exit status, a written config file, or queue acceptance is insufficient by itself.

## Learning handoff

After a verified outcome, use `openclaw-learning-loop` only for a reusable procedure, recovery technique, durable correction, or ordering constraint. Do not train on transient provider failures, routine success, secrets, or one-off personal facts.
