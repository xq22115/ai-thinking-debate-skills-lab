# 10 — GitHub Actions Failure Diagnosis

Date: 2026-08-18
PR: #45

## Observed

At PR head `c0fc557be881349f246cea4c384dcda907db95d1`, four pull-request workflows concluded `failure`:

- Auto Assign
- Proof HTML
- Core CI
- PR Risk Router

Core CI jobs:
- `node-dependencies` → failure
- `validate-core` → failure

Proof HTML job:
- `proof` → failure

For the inspected failed jobs, the GitHub connector returned `steps: []` / `steps: null`. Attempting to retrieve the job log returned a GitHub/Azure blob `404 BlobNotFound`.

## What this proves

The PR is **not CI-healthy** and must not be labeled `VERIFIED`, `DEPLOYABLE`, or `HEALTHY`.

The available evidence indicates failure before observable workflow steps were recorded. That makes a normal script/test assertion failure less likely for the inspected runs.

## What this does NOT prove

Current evidence is insufficient to name the exact root cause. Plausible classes include:

- runner provisioning/startup failure;
- organization/repository Actions policy restriction;
- billing/quota/service-side failure;
- action-resolution/startup failure;
- another pre-step infrastructure condition.

These remain hypotheses, not facts.

## Next discriminating checks

1. Inspect Actions policy/settings for the organization/repository.
2. Inspect a newly triggered run after the current branch head changes.
3. Check whether jobs obtain non-empty step records.
4. If logs become available, bind the root-cause claim to the first failing initialization/step message.
5. Compare with a known-good workflow run in the same repository/account.

## Completion status

`CI_DIAGNOSED_PARTIAL / ROOT_CAUSE_UNKNOWN`

Do not merge RC1 solely because the Markdown/skill files exist.