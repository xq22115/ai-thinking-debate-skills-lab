---
name: web-session-recovery
description: Use when a web AI/app session cannot send, freezes, loses state, hits request-frequency symptoms or behaves inconsistently and remote limits must be separated from local browser/network/session amplification.
---

# Web Session Recovery

## Purpose
Recover safely from local session amplification while preserving drafts/state and never pretending to disable server-side limits.

## Activate when
Use for inconsistent tabs/sessions, freezes, send failures, stale browser state, VPN/proxy/extension interactions or suspected local request fan-out.

## Do not activate
Do not use to bypass rate limits, anti-abuse, account restrictions, geographic/billing controls or service policy.

## Antigravity-native execution
When authorized browser/OS primitives exist, inspect exact app/session identity, timestamp/error, active/background work, network route, extensions, cache/site state and provider status in that order. Prefer non-destructive DOM/accessibility/backend inspection over foreground mouse actions.

## Workflow
1. Record failing surface and reproducible symptom.
2. Compare same account/task across independent routes where available.
3. Inspect local amplification before destructive cleanup.
4. Back up metadata/drafts needed for recovery.
5. Apply the smallest reversible local fix.
6. Read back protected work and expected postcondition.

## Validation
A local cleanup proves only that local state changed safely. Re-test the original symptom and distinguish server, local, mixed or unknown cause.

## Boundaries
No retry storms, IP rotation, header/device spoofing, session theft or adversarial filter probing.