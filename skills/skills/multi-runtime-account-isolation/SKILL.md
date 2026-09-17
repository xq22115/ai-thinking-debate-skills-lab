---
name: multi-runtime-account-isolation
description: Use when multiple devices, accounts, browser profiles, desktop apps, IDEs, bridges, or agent runtimes operate concurrently and wrong-target actions, state pollution, naming collisions, or cross-session interference are plausible.
---

# Multi Runtime Account Isolation

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

Names are hints; isolation requires independent runtime identity and separate state lanes.

## Isolation dimensions

For each lane, bind and keep separate when applicable:

- device fingerprint and hostname;
- OS/user/home root;
- account identity or non-secret local alias;
- browser profile/user-data directory;
- application root process/session;
- workspace/cwd/repository/worktree;
- ports, sockets, native-host channels, and local endpoints;
- caches, temp directories, logs, checkpoints, receipts;
- automation session/connection IDs;
- credentials and permission scope.

## Target gate

Before a material action, require enough independent signals to distinguish the target from every concurrently active alternative. Prefer process lineage, filesystem path, account/profile alias, session/window identity, and a read-only functional sentinel.

If two lanes can produce the same friendly name, the friendly name cannot authorize a write.

## Collision rules

1. Never reuse a stateful session ID across devices or accounts unless the protocol explicitly defines it as portable and the target is revalidated.
2. Give local services deterministic, lane-specific endpoint names/ports; fail on collision instead of silently attaching to an existing listener.
3. Store private account/profile mappings locally and untracked.
4. Keep evidence receipts lane-bound so proof from Account 1 cannot satisfy Account 2.
5. After any app restart, connector reconnect, browser relaunch, sleep/wake, or device route change, revalidate lane identity before continuing writes.
6. When shared resources are unavoidable, serialize mutations with ownership/leases and include the lane ID in every claim.

## Cross-pollution tests

- Run both accounts simultaneously and prove writes land only in the intended lane.
- Restart one runtime and confirm the other stays connected.
- Intentionally present duplicate window/app names and verify disambiguation.
- Create a port/session collision and verify fail-closed behavior.
- Confirm logs, caches, and checkpoints remain attributable to one lane.

## Release gate

`PASS` requires independent identity evidence for every active lane, no shared mutable state without explicit ownership, and an adversarial wrong-target test. If target identity is ambiguous, stop the write path rather than guessing.
