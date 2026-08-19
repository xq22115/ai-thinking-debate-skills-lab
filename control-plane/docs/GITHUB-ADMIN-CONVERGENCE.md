# Agent Core V4 — GitHub Admin Convergence

The repository-local V4 runtime is already able to prove `Merge Readiness` on live pull requests. The remaining GitHub admin surface is converged by `scripts/apply_agent_core_admin.py` using an already-authenticated GitHub CLI credential with repository **Administration: write**.

The tool is **dry-run by default**. A repository commit, policy file, or local backup is never treated as proof that GitHub settings changed; success requires API read-back after mutation.

## Dry run

```bash
python scripts/apply_agent_core_admin.py --repo xq22115/demo-repository
```

The dry run inspects and reports differences for:

- `allow_auto_merge = true`
- `allow_merge_commit = false`
- `allow_squash_merge = true`
- `allow_rebase_merge = true`
- `allow_update_branch = true`
- repository Ruleset `protect-main`
- default-branch PR requirement with review-thread resolution
- required status check `Merge Readiness` bound to GitHub Actions integration `15368`

If `protect-main` does not exist, dry run reports that it would be created. If it exists, unrelated rules and bypass actors are preserved while the `required_status_checks` rule is normalized to the single V4 gate.

## Apply

Only after reviewing dry-run output:

```bash
python scripts/apply_agent_core_admin.py --repo xq22115/demo-repository --apply
```

Before writing, the current repository metadata and existing Ruleset (if any) are saved under:

```text
~/.github-agent-core/backups/xq22115__demo-repository/
```

The write sequence is Ruleset first, repository settings second. The Ruleset is read back before repository settings are changed. If the later repository PATCH/read-back fails, the tool attempts to restore the old Ruleset or delete a newly-created Ruleset and restore previous repository setting values.

## Credential requirement

GitHub's repository-settings PATCH and repository Ruleset create/update APIs require a credential with **Administration: write** for the repository. If the authenticated `gh` account lacks that permission, the command must report `BLOCKED`; do not work around the failure by weakening the desired policy.

## Verification after apply

Run the dry-run command again. It should report both repository settings and Ruleset as compliant with `would_change: false`. Then independently read back GitHub repository metadata and the `protect-main` Ruleset before calling the admin layer complete.

## Live routing proof

A pull request that changes this runbook is intentionally routed through `Validate Agent Admin Convergence`. The trusted `main` manifest must therefore make `Merge Readiness` wait for that validator on the same PR head SHA before returning PASS.
