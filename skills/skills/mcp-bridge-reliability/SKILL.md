---
name: mcp-bridge-reliability
description: Use when MCP servers, local/remote bridges, connectors, native hosts, or long-running tool sessions disconnect, become stale, route to the wrong session, lose authorization, or recover unreliably.
---

# MCP Bridge Reliability

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

A bridge is a lifecycle system, not a socket that either exists or does not. Track identity, transport, authorization, liveness, session affinity, state ownership, and recovery separately.

## Failure model

Classify failures before restarting anything:

- discovery/registration;
- process lifecycle;
- transport/port/socket;
- protocol/version negotiation;
- authorization/credential scope;
- wrong device or wrong session affinity;
- stale native host or extension state;
- request execution/tool error;
- backpressure/timeout;
- owning runtime unavailable;
- provider-side rejection.

## Reliability sequence

1. Record client, server, device, account, endpoint, protocol/spec version, process identity, and expected session affinity.
2. Verify the full path: `configured → process alive → transport reachable → protocol handshake → authorized → tool listed → representative call → observable target effect`.
3. Keep liveness probes side-effect free. A TCP-open check does not prove protocol health; tool listing does not prove the target action works.
4. Make reconnect idempotent. Recovery must not create duplicate daemons, duplicate native hosts, repeated tool execution, or conflicting ports.
5. Persist only the minimum resumable state. Treat process/session IDs as stale after restart unless revalidated.
6. Use bounded retries with jitter/backoff only for transient classes. Authentication, version mismatch, wrong-device routing, and deterministic protocol errors require a changed route.
7. After two equivalent failures, pivot transport, endpoint, process owner, protocol path, or diagnostic instrument.
8. For long tasks, checkpoint the task state outside the volatile bridge so reconnection does not require replaying unsafe side effects.

## 2026 compatibility note

MCP `2026-07-28` moved toward a stateless request/response core and strengthened authorization/extension semantics. Do not assume older stateful-session behavior when diagnosing a current implementation; pin the actual client/server spec and SDK versions.

## Verification matrix

Test at least the applicable cases: cold start, normal call, server restart, client restart, network interruption, auth expiration, port collision, duplicate launch, wrong-device hint, stale session ID, rapid consecutive calls, and recovery after partial failure.

## Release gate

Do not call a bridge stable because it connected once. `PASS` requires repeated representative calls, recovery from at least one relevant interruption, no duplicate side effects, and target identity/affinity verification after reconnect.
