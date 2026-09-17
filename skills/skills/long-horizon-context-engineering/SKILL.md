---
name: long-horizon-context-engineering
description: Use when an agent task spans many turns, context windows, sessions, handoffs, large tool outputs, or hours of work and context rot, compaction loss, stale state, or premature completion is plausible.
---

# Long-Horizon Context Engineering

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

Context is a finite working set, not an archive. Preserve task truth durably outside the model window and rehydrate only the smallest high-signal state needed for the next decision.

## State layers

Keep these separate:

- **Goal contract** — objective, hard constraints, acceptance tests, non-goals.
- **World/runtime state** — exact revisions, target identities, current processes/sessions, mutable dependencies.
- **Decision ledger** — decisions, rationale, superseded alternatives, unresolved cruxes.
- **Evidence index** — evidence IDs/locations and what claims they support; avoid re-injecting full raw logs by default.
- **Execution state** — completed steps, pending work, unsafe-to-repeat actions, rollback points.
- **Working context** — only what the current step needs.

## Compaction protocol

1. Compact before the context becomes unreliable, not only after failure.
2. Optimize recall before brevity: preserve hard constraints, architectural decisions, unresolved defects, exact identifiers, failed routes, verification status, and safety/rollback boundaries.
3. Drop duplicated prose, stale tool outputs, already-consumed search snippets, and narrative dead ends once their durable lesson/evidence pointer is retained.
4. Mark every summarized claim as verified, derived, hypothesis, or unknown.
5. Keep immutable references to source artifacts so a fresh context can re-open load-bearing evidence instead of trusting the summary.
6. After rehydration, revalidate mutable state such as branch head, process/session IDs, tool schemas, permissions, queues, or remote status.

## Session handoff contract

A fresh worker/session receives: goal revision, current exact target, acceptance ledger, completed verified work, open unknowns, failed mechanisms, protected capabilities, evidence pointers, pending actions, unsafe-to-repeat actions, and the next highest-value test.

Do not transfer private chain-of-thought. Transfer decisions, evidence, assumptions, tests, and state needed for execution.

## Anti-rot checks

- Does the summary preserve every hard constraint?
- Does a claimed fact still have an owning source/evidence pointer?
- Did a world-state fact silently become stale?
- Did an old blocker become the new goal?
- Did a failed method become a false impossibility claim?
- Did the new context inherit a completion claim whose acceptance test was never run?

## Release gate

A long-horizon task is resumable only when a fresh context can reconstruct the current goal and state without replaying unsafe effects or guessing missing decisions. If rehydration depends on memory alone, durability is `NOT RUN`.
