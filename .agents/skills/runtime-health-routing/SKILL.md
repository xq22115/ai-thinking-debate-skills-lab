---
name: runtime-health-routing
description: Use when capability choice depends on runtime health, latency, errors, rate/quota state, freshness, service availability or local amplification such as retries, network routes or competing processes.
---

# Runtime Health Routing

## Purpose
Route around transient unhealthy paths without confusing local amplification with provider/server limitations or hiding a persistent defect.

## Activate when
Use for unstable tools/providers, intermittent failures, excessive retries, degraded latency, quota/health changes or competing execution paths.

## Do not activate
Do not route merely to avoid debugging a stable reproducible bug, and do not use routing to evade service limits or anti-abuse controls.

## Antigravity-native execution
Measure current health of candidate routes: reachability, error class, latency, quota/entitlement visibility, version freshness and task-relevant postcondition. Distinguish remote service state from local VPN/proxy, extension, tab/process, cache or retry amplification.

## Workflow
1. Establish baseline failure and time.
2. Classify local, remote, mixed or unknown.
3. Probe independent routes without retry storms.
4. Prefer the healthiest authorized route that preserves acceptance criteria.
5. Keep fallback/circuit-breaker semantics bounded.
6. Re-check the original route after material state change.

## Validation
A faster response is not necessarily a correct one. Health requires both transport success and task-relevant behavior.

## Boundaries
Never rotate identities/IPs, spoof clients or flood retries to bypass limits. Preserve provider/account controls.