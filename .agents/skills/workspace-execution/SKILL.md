---
name: workspace-execution
description: Use for effectful work inside the user's Antigravity project/workspace where exact repository/app/OS identity, local files, terminal, MCP tools, reversible edits and non-disruptive execution matter.
---

# Workspace Execution

## Purpose
Execute against the correct local/project target with minimal disruption and strong rollback/read-back discipline.

## Activate when
Use for file edits, terminal work, local app/config repair, repository changes, workspace automation or target-specific environment operations.

## Do not activate
Do not use when no local/project mutation is requested, and do not guess target instance/profile/device when multiple are plausible.

## Antigravity-native execution
Resolve workspace path, repo/ref, target app/instance, OS/architecture and permissions before mutation. Prefer native file/terminal/MCP/backend interfaces. For GUI work, prefer background/non-focus DOM/accessibility/native control and target-region evidence.

## Workflow
1. Snapshot current relevant state/Git diff.
2. Confirm exact target identity and protected user work.
3. Choose the least-invasive reversible mechanism.
4. Apply bounded change with rollback path.
5. Read back file/config/runtime state.
6. Test user-visible behavior and regression.
7. Persist only durable settings that survive restart when required.

## Validation
File write success is not runtime success. Verify the owning application/workspace behavior and exact revision whenever possible.

## Boundaries
Do not restart, close apps, steal focus, delete user data or alter unrelated profiles/accounts unless explicitly required and authorized.