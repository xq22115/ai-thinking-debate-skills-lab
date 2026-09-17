---
name: runtime-release-parity
description: Use when source, tests, packages, daemons, desktop apps, containers, workers, bridges, or deployed agents may be running different revisions and a fix appears correct in one layer but not in the live runtime.
---

# Runtime and Release Parity

## Core principle

`SOURCE_PASS != LIVE_RUNTIME_PASS`. Treat every build/deploy/run layer as a separately identifiable artifact.

## Identity tuple

Record when applicable:

`repo + source commit + build artifact digest + package version + config revision + runtime/process/container identity + host/profile + start time`

Never collapse these into one “version.”

## Workflow

1. Capture the pre-change live identity and rollback target.
2. Prove which source/config produced the artifact intended for deployment.
3. Verify the owning runtime actually loaded that artifact/config.
4. Distinguish stale process, stale cache, stale worker and stale search/index from source defects.
5. Test the user path on the exact live identity.
6. Restart/cold-start when persistence or bootstrapping is part of the failure model.
7. Re-read identity after restart; detect silent fallback to an older artifact/config.
8. Compare source test, integration test and live result without promoting evidence across layers.
9. Preserve rollback and verify rollback restores the prior known-good identity.

## Red flags

- “102/102 tests pass” while the live daemon predates the patch;
- a package version is used as a substitute for commit/digest identity;
- a branch is updated but workers were never restarted/reloaded;
- a restart fixes the symptom but no persistence test follows;
- one account/profile is tested while another owns the failing runtime.

**REQUIRED SUB-SKILL:** use `agent-runtime-forensics` when process/artifact provenance is unclear and `completion-gate` before release claims.

## Output

Return the source→artifact→runtime chain, exact identities, drift findings, restart/cold-start evidence, rollback target, and highest verified layer.
