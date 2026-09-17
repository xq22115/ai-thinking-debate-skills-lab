---
name: tool-contract-testing
description: Use when an agent depends on function tools, MCP servers, plugins, connectors, browser/computer tools, or external APIs and correctness depends on schemas, capability negotiation, retries, side effects, or postconditions.
---

# Tool Contract Testing

## Core principle

A tool contract is `schema + capability + identity + failure semantics + effect semantics`. A successful RPC is only one field.

## Workflow

1. Fingerprint live tool/server/client/protocol versions and authorization scope.
2. Validate input and output against the **live** schema, including unions, references and conditional JSON Schema where supported.
3. Test required/optional/null/empty/boundary inputs and unknown fields.
4. Define effect contract: what external state must change, remain unchanged, or be idempotent.
5. Exercise timeout, cancellation, retry, duplicate delivery and partial-failure semantics.
6. Read back the target state after material effects.
7. Test version/capability mismatch explicitly; fail closed when a required capability is absent.
8. Keep discovery cache invalidation rules for schema, entitlement, session and protocol changes.

## MCP 2026 rule

For MCP, do not assume pre-`2026-07-28` lifecycle semantics. Current investigations must check the negotiated spec/SDK behavior, including the stateless core and relevant extensions/capabilities. Roots, Sampling and Logging deprecation status must be treated as version-sensitive evidence, not timeless protocol truth.

## Hard rules

- `HTTP/RPC SUCCESS != EFFECT SUCCESS`.
- Generated schema examples do not prove the connected server implements them.
- Retrying an effectful tool without idempotency analysis can duplicate side effects.
- Display-name equality does not prove server/tool identity.
- Cached list results need invalidation when entitlement or server revision changes.

**REQUIRED SUB-SKILL:** use `mcp-surface-engineering` for large/changing MCP surfaces.

## Output

Return live contract fingerprint, positive/negative cases, effect read-back, retry/idempotency result, compatibility gaps and exact protocol/runtime identity.
