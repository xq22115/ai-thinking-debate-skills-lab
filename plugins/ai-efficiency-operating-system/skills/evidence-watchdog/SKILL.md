---
name: evidence-watchdog
description: Use when a claim of fixed, configured, installed, tested, live, deployed, delivered or complete must be proven, or when a stateful mutation requires postcondition/read-back evidence.
---

# Evidence Watchdog

A successful command, tool call, write, PR, CI check or executor statement is not the intended state transition.

## Separate state levels

Use the strongest level actually observed:

`DRAFTED → PACKAGED → IMPLEMENTED → TESTED → VERIFIED → HOST_LIVE → DEPLOYED → HEALTHY`

Do not skip levels by rhetoric.

## Evidence hierarchy

Prefer, when applicable:

1. owning-runtime/user-path postcondition;
2. independent deterministic reproduction/read-back;
3. exact current implementation/configuration evidence;
4. authoritative static documentation;
5. indirect/reporting evidence;
6. unsupported hypothesis.

Bind evidence to target identity, revision/version, requirement, observed time and expiry when state can drift.

## Independence

The executor cannot self-certify material completion. When independent verification is required, evidence must come from a distinct observer/tool/runtime route, not a renamed role that shares the same unverified output.

If a state-sensitive epoch changes — resume, compaction, target/ref, cwd, tool/permission, instruction or skill revision — old evidence becomes history until refreshed.

`UNKNOWN` is first-class. If an effect may have happened but confirmation was lost, read back the postcondition before replay.

Read `references/evidence-completion.md` for the detailed gate and strict completion vocabulary.
