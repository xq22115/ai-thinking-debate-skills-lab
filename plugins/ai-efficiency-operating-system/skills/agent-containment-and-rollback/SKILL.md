---
name: agent-containment-and-rollback
description: Use when an agent or automation can mutate files, repositories, cloud resources, desktop UI, external services, credentials, or user-visible state and a mistake could have a larger blast radius than the intended task.
---

# Agent Containment and Rollback

## Core principle

Reduce both failure probability **and blast radius**. Powerful agents should gain narrowly scoped capabilities, not ambient authority.

## Containment contract

For each effectful capability define:

- exact target scope and owner;
- allowed operation classes;
- credential/permission boundary;
- reversible vs irreversible effects;
- rate/concurrency limit;
- confirmation boundary required by the host/user;
- rollback/disable mechanism;
- telemetry needed to reconstruct the effect.

## Workflow

1. Start from least privilege and add only capabilities required by the goal.
2. Separate orchestration credentials from model-generated-code execution when practical.
3. Prefer isolated branch/worktree/sandbox/profile for risky changes.
4. Add dry-run/read-back/precondition checks before destructive or broad operations.
5. Make recovery automation conservative: ownership check, positive failure evidence, debounce/cooldown and idempotency before actions like reload/restart.
6. Cap retries, fan-out and write scope so one bad hypothesis cannot amplify indefinitely.
7. Record the exact rollback target before mutation.
8. Test both the intended effect and rollback/disable path.

## Red flags

- a UI heuristic can inject reload during normal layout transitions;
- one credential can mutate unrelated projects/accounts;
- a retry loop repeats an effect without idempotency;
- rollback means “reinstall and hope” rather than a known prior state;
- the monitor and repair actor share no independent safety gate.

## Output

Return capability map, blast-radius estimate, privilege boundary, preconditions, rollback target, recovery test and residual risks.
