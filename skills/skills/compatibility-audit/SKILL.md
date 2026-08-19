---
name: compatibility-audit
description: Verify that instructions, skills, tools, and configurations actually match the target host, OS, version, permissions, runtime, and product surface before applying them. Use for Windows/macOS, desktop/web/CLI/API, MCP, IDE agents, and fast-moving agent frameworks.
---

# Compatibility Audit

Version: `0.1.1-rc1`

## Objective

Block copy-paste deployment of stale, host-incompatible, permission-incompatible, or product-surface-mismatched configuration.

## Environment Fingerprint

Record at least:

- product/host and surface: desktop, web, CLI, API, IDE, plugin, MCP, etc.;
- exact version / release / observation date;
- OS, shell, architecture;
- runtime/language version;
- installed tools and relevant feature flags;
- capability `VISIBLE / AUTHORIZED / VERIFIED` states;
- workspace/account/role restrictions when material.

## Source Classes

For fast-moving products, do not collapse these sources:

- `PRODUCT_GUIDANCE` — current official product/developer documentation;
- `REPOSITORY_CONTENT` — code/docs/examples at a pinned commit/blob;
- `REPOSITORY_METADATA` — archived/deprecated flags, releases, repository settings;
- `RUNTIME_OBSERVATION` — what the actual target environment exposes/does.

If these disagree, record the contradiction. For current product behavior, current official product/developer guidance normally outranks the lifecycle metadata of an example repository; direct runtime observation outranks assumptions about the user's actual environment.

## Workflow

1. Fingerprint the exact target environment.
2. Identify every environment and permission assumption in the proposed configuration.
3. Check current primary documentation/specification for unstable components.
4. Pin repository-backed evidence to a commit/blob/release when reproducibility matters.
5. Classify each assumption as `MATCH`, `ADAPTER_REQUIRED`, `UNSUPPORTED`, `UNKNOWN`, or `CONTRADICTED`.
6. Separate a product-level support claim from a target-account availability claim.
7. Prefer a current native mechanism over compatibility shims when both exist.
8. For Windows, verify PowerShell/cmd/Git Bash/WSL boundaries, quoting, path semantics, services/scheduler, process spawning, filesystem permissions and line endings.
9. For macOS, verify shell, TCC/sandbox permissions, launchd, Keychain and filesystem assumptions.
10. For framework upgrades, check explicit breaking-change and state/session-schema boundaries; do not infer cross-version compatibility from the project name.
11. Test the smallest reversible probe before full activation.
12. Re-run a target-specific functional check before claiming compatibility.

## Output Contract

Return a compatibility matrix with:
- requirement;
- source product/version;
- target product/version/surface;
- OS/runtime;
- permission/capability state;
- observed capability;
- status;
- adapter/fallback;
- evidence class;
- evidence date/source/revision;
- contradiction, if any;
- last verified date.

## Completion Gate

Never claim `cross-platform`, `compatible`, `supported`, or `installed-and-working` without target-specific evidence at the appropriate level.

`DOCUMENTATION_SUPPORT != TARGET_RUNTIME_VERIFICATION`.
