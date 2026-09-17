---
name: openclaw-evidence-gate
description: Use when OpenClaw work is about to claim complete, fixed, enabled, connected, effective, verified, delivered, installed, or host-live.
---

# OpenClaw Evidence Gate

This skill owns completion truth for the OpenClaw adapter.

## Reverse-walk every consequential claim

`claim → acceptance → owning evidence → current goal version → causal path`

A claim passes only if the evidence is current, target-bound, and produced by the system that actually owns the state.

Do not collapse:

`PACKAGED != LOADED != INVOKABLE != EFFECTIVE != VERIFIED != HOST_LIVE`

`QUEUED != DELIVERED`

`COMMAND_OK != POSTCONDITION_OK`

## Evidence hierarchy

Prefer, in order:

1. owning-runtime state/read-back;
2. deterministic test or observable postcondition on the intended target;
3. independent trace/receipt tied to the same run/revision;
4. configuration/package existence as supporting evidence only;
5. agent or child self-report as a lead, never sole proof.

For stateful changes, perform a read-back after the mutation. For a file, read the target file/revision. For config, use OpenClaw config/status/skills diagnostics. For a tool effect, inspect the intended process/network/artifact/delivery state.

A sub-agent or Swarm child result is evidence for parent review; it does not own the user's final status.

## Counterexample pass

Before success:

- search for a stale session, wrong agent/workspace, wrong profile, wrong branch, version skew, tool-policy exclusion, or unrefreshed skills snapshot;
- test the strongest plausible failure mode;
- preserve contradictory evidence instead of averaging it away.

If one hard acceptance condition lacks current owning evidence, do not label the task `DONE`.

## Status

Use the narrowest truthful status:

- `VERIFIED` — all hard acceptance conditions have fresh owning evidence;
- `VERIFIED_WITH_CONCERNS` — hard gates pass; non-veto concerns remain;
- `PARTIAL` — separable work succeeded but one or more acceptance conditions remain;
- `BLOCKED` — a concrete required condition cannot currently advance;
- `HOST_LIVE_UNVERIFIED` — package/config may exist, but the running OpenClaw surface was not behaviorally exercised.

Repository CI can validate this adapter package and deterministic router. It cannot prove a user's Gateway loaded and exercised it.
