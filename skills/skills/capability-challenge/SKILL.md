---
name: capability-challenge
description: Distinguish a real platform limitation from a missing permission, unavailable connector action, temporary failure, unsupported host, or unverified assumption before concluding that a task cannot be done.
---

# Capability Challenge

Version: `0.1.1-rc1`

## Objective

Prevent false terminal `cannot` while preserving hard safety, authorization, and platform boundaries.

## Capability Truth Model

For every material capability, keep three states separate:

- `VISIBLE` — the tool/action appears in the current runtime or schema.
- `AUTHORIZED` — the backing credential/app/account is permitted to perform the required operation.
- `VERIFIED` — a direct consumer call or read-back proves the requested capability actually works in the target environment.

Never infer `AUTHORIZED` from `VISIBLE`, or `VERIFIED` from configuration alone.

## Workflow

1. Name the exact blocked operation and the user-level goal it serves.
2. Record `VISIBLE / AUTHORIZED / VERIFIED` separately; use `UNKNOWN` when not observed.
3. Classify the blocker: `NO_TOOL`, `NO_PERMISSION`, `AUTH_BLOCKED`, `UNSUPPORTED_API`, `HOST_MISMATCH`, `TEMPORARY_FAILURE`, `POLICY_BOUNDARY`, `INFRASTRUCTURE_BLOCKED`, or `UNKNOWN`.
4. Inspect the actual connected-tool schema / host capability rather than relying on remembered limitations.
5. Check whether a narrower, adjacent, or differently routed **supported** operation achieves the same goal.
6. Prefer reversible supported alternatives; never bypass safety, source-system permissions, or authorization.
7. When a probe is safe, execute the smallest direct probe and record its exact environment/revision/time.
8. If still blocked, state the exact missing capability and the evidence that would change the conclusion.

## Evidence Rules

- `UNKNOWN != IMPOSSIBLE`.
- `FAILED_PATH != FAILED_GOAL`.
- A visible connector action is evidence only for visibility.
- A successful read operation does not prove write/admin permission.
- A configuration file declaring permission does not prove the host granted it.
- Backend read-back or a successful direct consumer action is stronger than local configuration inspection.

## Output Contract

Return:
- requested goal;
- requested capability;
- `VISIBLE` state + evidence;
- `AUTHORIZED` state + evidence;
- `VERIFIED` state + evidence;
- blocker class;
- supported alternatives checked;
- final status: `PASS | FAIL | BLOCKED | UNKNOWN`;
- precise next enabling condition.

## Completion Gate

`CANNOT` is valid only when the actual required capability is unavailable or disallowed after supported alternatives and safe probes have been checked. If permission or runtime truth cannot be observed, report `BLOCKED` or `UNKNOWN`, not an invented terminal limitation.
