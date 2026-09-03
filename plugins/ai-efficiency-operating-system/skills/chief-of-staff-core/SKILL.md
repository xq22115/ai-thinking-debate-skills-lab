---
name: chief-of-staff-core
description: Use when a task is complex, multi-stage, multi-tool, long-horizon, or constraint-heavy and needs one primary phase owner to preserve the user's objective, acceptance criteria, authority and routing.
---

# Chief of Staff Core

Keep one task contract and one primary owner for the current phase. Do not turn every request into the full harness.

## Contract

For non-trivial work compile:

- objective;
- deliverables;
- acceptance criteria;
- hard constraints and forbidden substitutions;
- authority ceiling;
- decision-critical unknowns;
- completion evidence plan;
- stop conditions;
- current blocker and next causal action.

A later user correction supersedes contradicted assumptions. Retrieval, memory, tools and reviewers may update evidence but cannot silently rewrite the objective.

## Route by authority, goal and phase

Choose the primary specialist in this order:

1. explicit user correction or explicit skill request;
2. actual host capability and authorization;
3. active Goal Contract / target identity;
4. current task phase and diagnostic signal;
5. semantic similarity.

For substantive work, `task-goal-intelligence` owns the lightweight goal gate. Use at most three implicit skills in one phase. More skill activations are not automatically better.

Base phase owners:

- selecting a route/architecture → `plan-arbiter`;
- current evidence/root cause/research → `executive-research`;
- proving a state or completion → `evidence-watchdog`;
- durable context/memory → `memory-policy`;
- repeated review/no-progress route → `convergence-controller`.

Conditional specialist escalation:

- capability differs by model/harness/account/session/surface or limiting layer is unclear → `capability-forensics`;
- large/changing/conflicting MCP/tool surface, schema drift or context/namespace pressure → `mcp-surface-engineering`;
- tool/process reports success but file/process/network/artifact/postcondition state disagrees → `agent-runtime-forensics`.

These three specialists are demand-loaded implicit candidates, not globally always-on skills. Topic nouns alone do not trigger them. `autonomy-contract`, `persistent-work-ledger`, and `authorized-reverse-engineering` remain explicit-only.

## Combination rule

Prefer one of these bounded shapes:

- goal gate + primary owner;
- goal gate + primary specialist + `evidence-watchdog` when state/completion matters.

Do not load every skill or every tool schema. Discover many, load few.

## Fallback/self-repair

A failed specialist route is evidence about the route, not a new mission.

1. Preserve root goal, constraints and acceptance tests.
2. Retry the same route at most once without new evidence.
3. If still blocked, choose a materially different specialist/method/layer.
4. If a conditional specialist is unavailable, fall back to the nearest base skill and continue collecting discriminating evidence.
5. Report host-capability mismatch rather than fabricating execution.
6. Require postcondition/read-back proof before completion.

## Goal firewall

Reject work that lacks an acceptance, dependency-unlock, or information-gain edge to the active goal. A workaround that removes a capability the user requires is a diagnostic/tradeoff, not a full fix.

Do not duplicate the repository's broad Continuous Quality + Durability Kernel here. This skill owns task compilation and routing, not global policy redefinition.

Read `references/control-contract.md` when authority, host capability, phase ownership or scope-loss is ambiguous.
