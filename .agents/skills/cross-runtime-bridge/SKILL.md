---
name: cross-runtime-bridge
description: Use when task state, artifacts or capability contracts must move between Antigravity and another authorized AI/agent runtime without assuming equivalent tools, memory, permissions or execution locality.
---

# Cross Runtime Bridge

## Purpose
Transfer task meaning and verifiable state across heterogeneous runtimes while preventing capability or authority assumptions from leaking across the boundary.

## Activate when
Use for handoff between Antigravity and other authorized coding/chat/agent environments, or when one runtime produces artifacts consumed by another.

## Do not activate
Do not use when the whole task is owned by one runtime and no cross-runtime transfer exists.

## Antigravity-native execution
Use explicit handoff artifacts containing goal revision, acceptance tests, target identity, artifact hashes, unresolved gates, evidence, required capabilities and permissions. Re-resolve skills/tools/MCP surfaces on the receiving runtime rather than copying tool names.

## Workflow
1. Serialize semantic task state, not hidden conversation assumptions.
2. Bind artifacts to immutable revisions/hashes where material.
3. Declare sender capabilities and receiver requirements separately.
4. Re-authorize and re-discover on receive.
5. Require receiver read-back for consequential delivery.

## Validation
Sender success != receiver acknowledgement. Cross-runtime parity must be reverified for the exact environment and revision.

## Boundaries
A bridge does not bypass provider policy, sandboxing, account boundaries or local permissions. Treat incompatible capability as a routing problem, not a reason to falsify completion.