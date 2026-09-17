---
name: runtime-release-parity
description: Use when code, prompts, skills, models, tools, or configuration pass in source or CI but may behave differently after packaging, deployment, installation, marketplace sync, host loading, process restart, or production execution.
---

# Runtime and Release Parity

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

`SOURCE_PASS != LIVE_RUNTIME_PASS`. Release truth is an identity chain: source success is not runtime success unless the exact intended artifact, configuration, permissions, dependencies, and running process are proven at the owning runtime.

## Parity ledger

Track independently when applicable:

- source repository + exact commit SHA;
- build inputs and generated artifact digest;
- package/plugin/model/tool version;
- deployment/install target and environment;
- host/runtime build, executable/entrypoint and process start time;
- active configuration, feature flags and policy revision;
- dependency versions and tool/MCP schemas;
- account/entitlement/permission scope;
- loaded revision and observable user-path behavior.

Do not collapse moving labels such as `latest`, branch names, package/marketplace versions, blob SHAs, artifact digests, installed revisions, and process identity into one “version.”

## Promotion sequence

`source test → build/package verification → artifact identity → staging/isolated load → representative runtime probe → canary/limited release → production read-back → user-path verification`

At every boundary, record what changed and what remains unverified.

## Drift detection

Check for different CLI/executable entrypoints, generated files not derived from the reported source revision, stale cache or marketplace sync, environment/feature-flag differences, permission/entitlement differences, dependency lock drift, tool schema/API drift, architecture/OS differences, stale workers/daemons, and old processes still serving a previous revision.

## Workflow

1. Capture the pre-change live identity and exact rollback artifact/revision.
2. Prove which source/config generated the candidate artifact.
3. Verify the owning runtime actually loaded that artifact/config rather than a stale cache/process.
4. Test the user path on the exact live identity.
5. Run restart/cold-start validation when bootstrapping, persistence, workers, or caches are part of the failure model.
6. Re-read identity after restart and detect silent fallback to an older artifact/config.
7. Keep source tests, integration tests, package verification and live runtime evidence as separate layers.
8. Verify rollback restores the prior known-good identity when rollback is part of the release contract.

## Release discipline

Prefer immutable/pinned dependencies where reproducibility matters. Serialize deployment to one production target when concurrent releases could race. Gate sensitive environments with explicit protections when supported. Prefer a low-impact canary that reports loaded identity and exercises one representative path.

If runtime evidence contradicts CI/package evidence, runtime wins and the release remains unverified.

**REQUIRED SUB-SKILL:** use `agent-runtime-forensics` when process/artifact provenance is unclear, `identity-session-isolation` when multiple profiles/hosts coexist, and `evidence-watchdog` before release claims.

## Output

Return the source→artifact→deployment→runtime chain, exact identities, drift findings, cold-start/restart evidence, rollback target, user-path result, and highest verified layer.
