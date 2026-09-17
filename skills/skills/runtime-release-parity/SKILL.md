---
name: runtime-release-parity
description: Use when code, prompts, skills, models, tools, or configuration pass locally or in CI but behave differently after packaging, deployment, installation, marketplace sync, host loading, or production execution.
---

# Runtime Release Parity

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

Release truth is an identity chain. Source success is not runtime success unless the exact intended artifact, configuration, permissions, and dependency set are proven at the owning runtime.

## Parity ledger

Track independently when applicable:

- source repository + commit SHA;
- build inputs and generated artifact digest;
- package/plugin/model/tool version;
- deployment/install target and environment;
- host/runtime build and entrypoint;
- active configuration/feature flags/policy;
- dependency versions and tool/MCP schemas;
- account/entitlement/permission scope;
- loaded revision and observable behavior.

Do not collapse moving labels such as `latest`, branch names, marketplace versions, package versions, file blob SHAs, and installed runtime revisions into one value.

## Promotion sequence

`source test → build/package verification → artifact identity → staging/isolated load → representative runtime probe → canary/limited release → production read-back → user-path verification`

At every boundary, record what changed and what remained unverified.

## Drift detection

Check for:

- different CLI or executable entrypoints;
- generated files not derived from the reported source revision;
- stale cache or marketplace/plugin sync;
- environment-variable or feature-flag differences;
- permission/entitlement differences;
- dependency lock drift;
- tool schema/API version drift;
- architecture/OS differences;
- old processes still serving the previous revision.

## Deployment discipline

1. Pin immutable dependencies where reproducibility matters.
2. Serialize deployment to one production target when concurrent releases could race.
3. Gate sensitive environments with explicit protections/approvals where supported.
4. Keep an exact rollback artifact/revision before promotion.
5. Prefer a read-only or low-impact canary that identifies the loaded revision and exercises one representative path.
6. If runtime evidence contradicts CI/package evidence, runtime wins and the release remains unverified.

## Release gate

`PASS` means the exact reported revision/artifact is proven loaded in the intended host and the requested user path works there. If only source or CI is proven, report that layer rather than promoting it to production truth.
