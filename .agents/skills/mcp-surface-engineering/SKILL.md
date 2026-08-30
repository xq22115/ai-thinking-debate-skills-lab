---
name: mcp-surface-engineering
description: Use for MCP server discovery, registration, authentication, schema/version drift, namespace collisions, tool visibility, entitlement or invocation failures in Antigravity.
---

# MCP Surface Engineering

## Purpose
Treat MCP as an external capability surface with explicit identity, schema, authorization and runtime state—not as text embedded inside a skill.

## Activate when
Use for MCP setup, migration, missing tools, schema incompatibility, duplicate namespaces, stale registrations, authentication or tool-surface poisoning concerns.

## Do not activate
Do not use for a purely procedural skill that needs no external MCP capability.

## Antigravity-native execution
Resolve the exact Antigravity build and current MCP configuration contract before editing. Keep credentials out of repository skill files. Separate server registration, auth, transport, tool schema, namespace and task-level permission.

## Workflow
1. Fingerprint server identity/version and configuration scope.
2. Inspect current registration before mutation.
3. Validate schema/tool names and collisions.
4. Authenticate through the supported host path.
5. Probe a harmless real invocation.
6. Verify a task-relevant postcondition and record version/config evidence.

## Validation
Use `DECLARED -> REGISTERED -> AUTHORIZED -> LOADABLE -> INVOKABLE -> VERIFIED`. A config entry or tool listing proves only its own state.

## Boundaries
Do not place secrets in skills, bypass auth, weaken tool safety, or assume an older MCP/session contract remains current.