---
name: mcp-bridge-reliability
description: Use when MCP servers, local/remote bridges, connectors, native hosts, or long-running tool sessions disconnect, become stale, route to the wrong application/account context, lose authorization, or recover unreliably.
---

# MCP Bridge Reliability

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

A bridge is a lifecycle system, not a socket that either exists or does not. Track identity, transport, authorization, liveness, application-level affinity/state ownership, protocol revision, and recovery separately.

## Failure model

Classify failures before restarting anything: discovery/registration; process lifecycle; transport/port/socket; protocol/version metadata; authorization/credential scope; wrong device/account/application affinity; stale native-host/extension state; request/tool error; backpressure/timeout; owning runtime unavailable; provider-side rejection.

## Reliability sequence

1. Record client implementation metadata when available, server, device, account, endpoint, protocol/spec version, process identity, and any application-level state or affinity handle that must survive across calls. Do not treat self-reported MCP client metadata as an authorization or account-identity proof.
2. Verify `configured → process alive → transport reachable → protocol version/client capabilities valid → authorized → capability/tool discovery when needed → representative call → observable target effect`.
3. Keep liveness probes side-effect free. TCP-open does not prove protocol health; tool listing does not prove target action.
4. Make reconnect idempotent. Recovery must not create duplicate daemons/native hosts, duplicate tool execution, conflicting ports, or replay unsafe state-changing calls.
5. Persist only minimum resumable application/task state. Treat process IDs, cached tool catalogs, authorization state, and application-level handles as stale after restart until revalidated.
6. Use bounded retries with jitter/backoff only for transient classes. Authentication, version mismatch, wrong-device/account routing, and deterministic protocol errors require a changed route.
7. After two equivalent failures, pivot transport, endpoint, process owner, protocol path, or diagnostic instrument.
8. For long tasks, checkpoint task state outside the volatile bridge so reconnection does not replay unsafe side effects.

## Current MCP compatibility

Fingerprint the actual MCP protocol and SDK on the client/server pair before applying lifecycle assumptions. In MCP `2026-07-28`, the protocol core is stateless: the legacy `initialize`/`initialized` exchange and `Mcp-Session-Id` are retired. Every request requires the protocol version and client capabilities in `_meta`. `io.modelcontextprotocol/clientInfo` is optional, though clients normally SHOULD include it unless specifically configured otherwise; it is self-reported metadata for identification/logging/debugging and must not be treated as a security or account-affinity credential. On Streamable HTTP, every request POST must also carry `MCP-Protocol-Version`, and the header value must equal `_meta.io.modelcontextprotocol/protocolVersion`; a mismatch is rejected with HTTP 400 and the MCP `HeaderMismatch` JSON-RPC error. Servers implementing `2026-07-28` MUST implement `server/discover`, but clients are not required to call it before ordinary RPCs; when a client does call it, use the result to validate supported versions/capabilities and handle cache freshness explicitly. Tool/resource/prompt list responses may also be cacheable. Application state and security identity may still exist, but they should be explicit rather than confused with a hidden protocol transport session or self-reported client/server metadata.

Do not project these semantics onto older MCP revisions. Version-specific adapters may need the older handshake/session lifecycle.

## Verification matrix

Test applicable cases: cold start, normal call without pre-discovery, explicit `server/discover`, server restart, client restart, network interruption, auth expiration, port collision, duplicate launch, wrong-device/account affinity, stale application handle or cached capability catalog, omitted optional `clientInfo`, rapid consecutive calls, and recovery after partial failure.

**REQUIRED SUB-SKILL:** use `mcp-surface-engineering` for discovery/schema/namespace pressure, `identity-session-isolation` for wrong-account/application routing, and `tool-contract-testing` for call/effect semantics.

## Release gate

Do not call a bridge stable because it connected once. `PASS` requires repeated representative calls, recovery from at least one relevant interruption, no duplicate side effects, and target identity/affinity verification after reconnect.
