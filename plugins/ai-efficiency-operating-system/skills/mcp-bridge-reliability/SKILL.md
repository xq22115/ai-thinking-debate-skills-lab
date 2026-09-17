---
name: mcp-bridge-reliability
description: Use when MCP servers, local or remote bridges, native hosts, connectors, or long-running tool sessions disconnect, become stale, route to the wrong session, lose authorization, or recover unreliably.
---

# MCP Bridge Reliability

Status: `EXPERIMENTAL / RUNTIME SPECIALIST`

## Core principle

A bridge is a lifecycle system, not a socket that either exists or does not. Track identity, transport, authorization, liveness, session affinity, state ownership, and recovery separately.

## Failure classes

Classify before restarting:

- discovery/registration;
- process lifecycle;
- transport/port/socket;
- protocol/version negotiation;
- authorization/credential scope;
- wrong device or session affinity;
- stale native host or extension state;
- request execution/tool error;
- backpressure/timeout;
- owning runtime unavailable;
- provider-side rejection.

## Reliability sequence

1. Record client, server, device, account, endpoint, protocol/spec version, process identity, and expected affinity.
2. Verify the path `configured → process alive → transport reachable → protocol handshake → authorized → tool listed → representative call → observable target effect`.
3. Keep liveness probes side-effect free. TCP-open does not prove protocol health; tool listing does not prove target action works.
4. Make reconnect idempotent. Recovery must not create duplicate daemons, duplicate native hosts, repeated tool execution, or conflicting ports.
5. Treat process/session IDs as stale after restart unless revalidated.
6. Use bounded retry/backoff only for transient classes. Authentication, wrong-device routing, version mismatch, and deterministic protocol errors require a changed route.
7. Persist resumable task state outside the volatile transport so reconnect does not replay unsafe side effects.
8. Test cold start, reconnect, client/server restart, auth expiry, port collision, stale session ID, wrong-device hint, rapid consecutive calls, and partial failure as applicable.

MCP `2026-07-28` moved toward a stateless request/response core with stronger authorization and extension semantics. Pin actual client/server spec and SDK versions rather than assuming older stateful behavior.

**REQUIRED SUB-SKILLS:** use `mcp-surface-engineering` for schema/discovery/entitlement problems, `identity-session-isolation` for cross-device/account routing, and `agent-concurrency-backpressure` when overload or retry pressure is involved.

## Output

Return lifecycle stage, exact endpoint/identity, failure class, stale-state risks, retry/reconnect contract, interruption test results, and the highest verified state from configuration through observable effect.
