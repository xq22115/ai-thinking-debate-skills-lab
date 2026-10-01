---
name: identity-session-isolation
description: Use when multiple accounts, profiles, repositories, workspaces, machines, browser sessions, MCP servers, agents, or credentials coexist and a wrong-target mutation, state leak, namespace collision, or cross-session contamination is possible.
---

# Identity and Session Isolation

## Core principle

Every effectful action needs an explicit target identity. Human-readable labels are hints, not routing keys.

## Identity tuple

Bind the operation to the smallest stable tuple available, such as:

`user/account + host/device + app/profile + workspace/repo + runtime/session + connector/server + target object`

## Workflow

1. Enumerate concurrent identities and shared resources before mutation.
2. Resolve stable IDs/paths/refs for the intended target; avoid routing from window title or display name alone.
3. Partition caches, logs, temp state, sockets/ports, credentials and tool namespaces wherever cross-account mixing is unsafe.
4. Stamp telemetry and artifacts with target identity so later forensics can distinguish sessions.
5. Before a material write, assert the active identity tuple and target revision.
6. Run a negative test proving the same action does **not** affect the neighboring account/profile/workspace.
7. On restart/reconnect, re-resolve identity; do not assume PID, window handle, port or token remains bound to the same owner.
8. Clean up leases/sessions without tearing down unrelated identities.

## Hard rules

- `SAME APP NAME != SAME ACCOUNT`.
- `SAME TOOL NAME != SAME SERVER/ENTITLEMENT`.
- A PID/window handle is ephemeral identity.
- Shared bridges must carry explicit routing identity or be treated as contamination risks.
- A successful Account 1 test cannot verify Account 2.

## Output

Return identity graph, shared-state risks, routing keys, isolation boundaries, positive target test, negative cross-target test and cleanup result.
