---
name: evidence-gate
description: Use whenever fixed, configured, installed, tested, live, deployed, delivered or complete must be proven, or after a stateful mutation that requires postcondition/read-back evidence.
---

# Evidence Gate

## Purpose
Prevent successful commands, writes, tests or agent statements from being mistaken for the user's intended end state.

## Activate when
Use after effectful work, deployment/configuration, installation, runtime claims, delivery, CI, repairs or any material completion assertion.

## Do not activate
Do not demand runtime proof for purely conceptual writing that has no external state transition.

## Antigravity-native execution
Use the strongest actually observed state: `DRAFTED -> PACKAGED -> IMPLEMENTED -> TESTED -> VERIFIED -> HOST_LIVE -> DEPLOYED -> HEALTHY`. Prefer owning-runtime/user-path read-back over static files or prose.

## Workflow
1. Bind evidence to target, revision/version, requirement and time.
2. Read back the postcondition after mutation.
3. Use an independent observer when material independence is required.
4. Invalidate stale evidence after workspace/ref/permission/skill/runtime epoch changes.
5. Preserve `UNKNOWN` when confirmation is missing; reconcile before replay.

## Validation
A test must be capable of failing under the violated invariant. `file exists`, `tool returned success`, `PR exists`, `CI green` and `skill listed` each prove only their own state.

## Boundaries
Do not skip evidence levels by rhetoric. `PACKAGED != HOST_LIVE` and local test pass does not automatically prove another runtime, account or environment.