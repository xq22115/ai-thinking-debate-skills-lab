---
name: compatibility-audit
description: Use before installing, migrating or relying on skills, MCP servers, workflows, scripts or configurations whose behavior may differ by Antigravity version, OS, workspace, protocol or permission state.
---

# Compatibility Audit

## Purpose
Separate portable capability semantics from the exact host/runtime adapter required to execute them.

## Activate when
Use for migrations, version upgrades, cross-OS deployment, MCP changes, copied configurations, external skill packs or any volatile integration contract.

## Do not activate
Do not add ceremony to stable, self-contained text-only work with no host dependency.

## Antigravity-native execution
Fingerprint Antigravity version/build, OS/architecture, workspace scope, skill discovery path, project rules, MCP schema/config location, shell/runtime, permissions and credential surface. Verify current primary documentation/source when any contract may have changed.

## Workflow
1. Record source and target environment envelopes.
2. Separate portable semantics from host assumptions.
3. Identify breaking fields, paths, schemas, permissions and lifecycle differences.
4. Build the smallest adapter.
5. Test positive, unsupported-host, stale-version and permission cases.
6. Pin versions/revisions where drift matters.

## Validation
Static documentation proves a contract, not local activation. Mark `supported`, `experimental` or `unsupported` only with matching evidence; runtime compatibility requires target-runtime execution.

## Boundaries
Never silently copy an old session, path, API or permission assumption into a newer runtime. Unknown compatibility remains `UNKNOWN`.