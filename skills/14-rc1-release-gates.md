# 14 — RC1 Release Gates

Date: 2026-08-18

Target candidate: `Evidence-Gated Deliberation & Skills OS v0.1.0-rc1`

## Gate 1 — Provenance

PASS only if:
- cross-chat inputs are pinned by exact PR/branch/head SHA;
- current external sources are version/date locked where unstable;
- historical claims are labeled as archive/history rather than current host truth.

Current: `PASS_FOR_RC1_ARCHIVE`

## Gate 2 — Scope isolation

PASS only if the staging diff does not modify unrelated repository production/control-plane files.

Current evidence: PR #45 compare against `main` shows all changed files under `research/ai-thinking-debate-skills-2026-08-18/`.

Current: `PASS`

## Gate 3 — Portable skills package

PASS only if core skills have explicit trigger/goal/workflow/output/completion boundaries.

Current core set: 9 skills.

Current: `PASS_FOR_EXPERIMENTAL_RC1`

## Gate 4 — Eval specification

PASS only if adversarial fixtures cover false completion, clone diversity, minority-correct hypotheses, root cause, recovery, compatibility, capability challenge, and control-plane publication/runtime boundaries.

Current: `PASS_SPEC_ONLY`

This does **not** mean executable hosted evals have run.

## Gate 5 — Cross-chat architecture convergence

PASS only if archive, portable reasoning, and execution/control-plane layers remain distinct and source-locked.

Current mapping:
- PR #46 = archive/vault
- PR #45 = portable reasoning/skills
- PR #29 = execution/control-plane

Current: `PASS`

## Gate 6 — Hosted CI

PASS only if required GitHub Actions jobs actually start workflow steps and pass.

Current: `BLOCKED_BY_BILLING_OR_SPENDING_LIMIT`

Issue: #47.

This gate is blocking.

## Gate 7 — Authentic runtime agent evidence

PASS only if runtime claims that require independent agents are supported by wrapper-observed/process/session/workspace/receipt evidence rather than role labels or model prose.

Current: `NOT_VERIFIED`

PR #29 explicitly preserves this boundary and reports authentic Claude execution as blocked/unverified.

## Gate 8 — Host adapters

PASS only if at least one target host adapter is tested against an exact current version and OS, with permissions/tools recorded.

Current: `SPECIFIED_NOT_HOST_VERIFIED`

## Gate 9 — Dedicated repository migration

PASS only when `ai-thinking-debate-skills-lab` exists and the pinned source material has migrated with provenance/hashes.

Current: `BLOCKED_BY_CONNECTOR_CAPABILITY`

Issue: #48.

## Gate 10 — Stable/merge declaration

`STABLE`, `MERGE_READY`, `HOST_LIVE_VERIFIED`, `DEPLOYED`, or `HEALTHY` may be claimed only after their corresponding evidence gates pass.

Current highest defensible status:

`RC1_PACKAGED_AND_GITHUB_STAGED / CI_BLOCKED / HOST_LIVE_UNVERIFIED`

PR #45 should remain Draft.
