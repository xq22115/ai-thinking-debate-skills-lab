# Multi-chat GitHub Invocation Protocol

## Start of every GitHub-backed task

1. Resolve the canonical repository from `registry.json`, not chat memory.
2. Read `AGENTS.md`, `ai-system/registry.yml`, `README.md`, `RUNBOOK.md`, and the current task Issue.
3. Resolve the exact target/base SHA and mint a unique `run_id`.
4. Create a unique actor branch. Never share a mutable branch with another chat/execution.
5. Create the actor's **create-only ownership claim** before its plan. No automatic takeover and no force-push ownership transfer; contested ownership means new `run_id`.
6. Commit the actor write plan on that branch. Task mutation is still locked.
7. A01 resolves all actor branch names to exact commit SHAs and collects plan/claim snapshots by SHA, including SHA-256 hashes. The collection is ephemeral.
8. Run write-set conflict preflight. Only PASS unlocks task mutation.
9. Execute on the claimed branch, using current blob SHA for existing-file replacements.
10. Freeze the exact task work head before writing evidence.
11. Emit a schema-v2 PASS/VETO receipt as a **receipt-only evidence commit**. It binds `claim_id`, `plan_head_sha`, branch, executor/execution identity, and `head_sha` = the pre-receipt work head.
12. Run snapshot-bound execution verification against the final receipt commit. Plan/claim rewrite, receipt identity mismatch, branch drift, invalid work-head lineage, replayed snapshot, undeclared task path, foreign receipt, or extra post-work change is VETO.
13. Adjudicate A01-A10 fail-closed using authentic independent 代理 receipts.
14. Immediately before integration, compare the pinned base with the trusted current base. Drift is VETO and requires a new `run_id`.
15. Fan-in only on `task/<issue>/<run_id>/integration`; then open one final PR to `main`.
16. Verify the exact final revision and report `PASS`, `VETO`, `FAIL`, `BLOCKED`, or `NOT_RUN`. Missing execution never becomes PASS.

## Re-entry from another chat

Resume by Issue number and explicit run IDs. Read claims, plans, branch SHAs, PRs and receipts before deciding whether to join an existing run read-only or create a new run. Never infer ownership from similar prompts.

## Collision and replay policy

- Same actor/run claim already owned by another execution: VETO/BLOCKED; new run required.
- Same mutable branch, two writers: forbidden.
- Same file, disjoint branches: allowed only if write-set preflight permits it.
- Branch name moved after snapshot: approved snapshot remains bound to its resolved commit SHA.
- Plan/claim modified after snapshot: VETO.
- Final head not descended from approved plan SHA: VETO.
- Actual task diff outside write set: VETO.
- PASS/VETO receipt v1 or receipt identity not matching the immutable claim: VETO/FAIL.
- Any post-work path other than the actor's exact receipt: VETO.
- Stale base SHA before integration: VETO; new run required.
- Old snapshot/receipt replay into a newer run: forbidden.

## Product limitation

Repository files govern behavior after this repository is loaded. They cannot force every ChatGPT conversation to select GitHub, change model policy, or create ten independent executors. Explicit GitHub intent remains the product-routing fallback.
