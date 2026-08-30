---
name: multi-agent-deliberation
description: Use when a complex task has several genuinely independent information needs or adversarial viewpoints whose parallel investigation can materially improve the decision.
---

# Multi Agent Deliberation

## Purpose
Use multiple agents for independent information gain, not role-play theater or vote counting.

## Activate when
Use for separable research branches, independent verification, architecture alternatives, adversarial review or parallel diagnostics with clear merge criteria.

## Do not activate
Do not spawn multiple agents for a serial dependency, a trivial task or when they would all read/write the same state without isolation.

## Antigravity-native execution
Use only parallel/subagent primitives the active runtime actually exposes. Give each worker a bounded contract: question, target, allowed tools, evidence format, non-goals and handoff artifact. Isolate writers or assign one merge owner.

## Workflow
1. Decompose by independent uncertainty, not arbitrary role count.
2. Assign non-overlapping evidence obligations.
3. Preserve source/revision identity in each result.
4. Compare contradictions using discriminating evidence.
5. Merge under the root goal and acceptance tests.
6. Verify final state independently of worker claims.

## Validation
Consensus is not correctness. Count evidence families, not agents. A worker's `done` status does not close the parent task until the owning acceptance gate passes.

## Boundaries
Do not claim parallelism if the runtime executed serially. Avoid shared mutable-state races, duplicate external effects and authority expansion through delegation.