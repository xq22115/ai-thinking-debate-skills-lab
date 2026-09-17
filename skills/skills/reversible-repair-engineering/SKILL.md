---
name: reversible-repair-engineering
description: Use when repairing a live system where the requested capability must be preserved, the root cause is uncertain or high-impact, and changes need safe rollback, exact-state verification, and regression protection.
---

# Reversible Repair Engineering

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

A repair is an experiment on a real system. Preserve a known-good rollback point, change one causal mechanism at a time, and require evidence that the original user path improved without degrading protected capabilities.

## Repair contract

Before mutation record:

- exact target identity and revision/state;
- original symptom and reproducible trigger;
- protected capabilities/non-goals;
- leading causal hypothesis and falsifier;
- rollback target;
- acceptance and regression tests.

## Change discipline

1. Prefer the smallest mechanism-level change that can alter the suspected cause.
2. Do not start with destructive cleanup, broad resets, disabling features, killing unrelated sessions, or deleting state merely because they may reduce symptoms.
3. Separate diagnostic toggles from permanent fixes. Every temporary change gets an expiry/rollback step.
4. Make writes idempotent where possible and read them back immediately.
5. Preserve exact pre-change bytes/settings for anything replaced.
6. If multiple independent changes are necessary, checkpoint between them so causal attribution is retained.
7. Stop escalating a route that fails twice without new information; revert or pivot before adding more entropy.

## Verification ladder

`write/read-back → focused mechanism test → original user-path reproduction → adjacent capability regression → adversarial/negative case → stability observation`

A restart that temporarily clears state does not prove the underlying defect is repaired. A benchmark or unrelated green CI does not prove the user's path works.

## Rollback triggers

Rollback or pause escalation when:

- protected capability regresses;
- target identity becomes ambiguous;
- error class changes unexpectedly;
- new background churn or resource growth appears;
- verification cannot distinguish the repair from restart/cache effects;
- the change cannot be read back exactly.

## Release gate

`PASS` requires the exact final state to be readable, the original failure to be reproduced before or otherwise bounded, the repaired user path to pass, relevant adjacent behavior to remain intact, and rollback to remain known. Otherwise report `FAIL`, `BLOCKED`, or `NOT_RUN`.
