---
name: capability-forensics
description: Use when an AI/agent/tool appears unable to perform a task and the real bottleneck could be model, harness, skill discovery, tool surface, permission, account, context, entitlement, environment or runtime state.
---

# Capability Forensics

## Purpose
Diagnose the actual limiting layer before changing prompts, models or permissions.

## Activate when
Use for missing tools, disabled actions, unexpected capability differences, installed-but-unusable integrations, surface mismatch or unexplained inability.

## Do not activate
Do not use when a known hard product boundary is already proven and no decision-relevant uncertainty remains.

## Antigravity-native execution
Track the capability ladder: `DECLARED -> VISIBLE -> AUTHORIZED -> LOADABLE -> INVOKABLE -> EFFECTIVE -> VERIFIED`. Inspect project skill discovery, rules, workspace identity, MCP/tool registration, account/permission state and OS constraints separately.

## Workflow
1. Freeze required outcome and protected capabilities.
2. Fingerprint model/runtime/workspace/OS/version/context/tools/permissions/account.
3. Change one layer at a time with a differential probe.
4. Prefer same task/different surface or same surface/different permission comparisons.
5. Read back the intended effect.
6. Classify the earliest failed ladder state and choose the least-invasive repair.

## Validation
`installed != invokable`; `listed != effective`; tool success != postcondition. Report each observed state plus unknowns.

## Boundaries
Maximize authorized capability and observability only. Never bypass safety, access, licensing, billing or entitlement controls.