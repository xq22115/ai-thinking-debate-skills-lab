---
name: github-operations
description: Use for GitHub repository discovery, source acquisition, branches, commits, pull requests, reviews, CI, continuity or durable Git-backed task artifacts.
---

# GitHub Operations

## Purpose
Make GitHub a versioned engineering/evidence surface while preserving repository identity, revision truth and runtime boundaries.

## Activate when
Use for repository reads/writes, source pinning, PR/CI work, cross-session Git continuity, importing reusable code or persisting task artifacts.

## Do not activate
Do not involve GitHub in unrelated prose or local-only work with no repository/evidence benefit.

## Antigravity-native execution
Resolve exact `owner/repo`, default/target branch and current commit before writes. Read the relevant file/state first, branch for non-trivial changes, keep commits causal, and prefer immutable SHAs for imported sources. Credentials and MCP authentication remain outside skill files.

## Workflow
1. Verify repository/ref and permission.
2. Inspect existing implementation/history/CI.
3. Make bounded changes on an isolated branch when appropriate.
4. Run relevant tests/checks.
5. Review diff and workflow state.
6. Open/update PR with acceptance mapping and remaining blockers.
7. Keep source receipts for external imports.

## Validation
A repository artifact proves repository state only. Bind claims to exact commit SHA; inspect CI jobs/logs rather than assuming a workflow trigger passed.

## Boundaries
Never expose secrets, force-push protected history without explicit authority, or equate repository presence with local Antigravity activation.