# Agent Core Contract

This repository supports AI-assisted work with a minimal, evidence-driven default capability profile.

## Operating rules

1. Identify the exact goal, repository scope, and acceptance checks before editing.
2. Inspect existing files and workflows before changing them.
3. Preserve working behavior unless the requested task explicitly changes it.
4. Prefer the smallest reliable route: host-native tools → existing skills → purpose-built CLI → existing MCP → shell/repository automation → install new tooling only when necessary.
5. Keep external tools deferred/on-demand; do not preload overlapping capabilities simply because they are available.
6. For browser work, prefer native browser tooling or Playwright CLI/Skills; use stateful MCP/browser agents only when the task genuinely requires persistent exploratory state.
7. For bugs or failed automation, find the root cause before stacking fixes. Test one falsifiable hypothesis at a time.
8. For non-trivial/multi-file changes, use a branch and pull request.
9. Never commit secrets, credentials, tokens, private keys, cookies, or sensitive user data.
10. Do not claim completion from a file write, command exit code, or agent success message alone. Verify the actual acceptance criterion on the exact revision.
11. Report verification as `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN` with evidence.
12. Repository files do not modify product-level AI policies, model weights, account permissions, or a user's local Cursor/ChatGPT configuration merely by existing in GitHub.

## Multi-chat GitHub control plane

For work involving multiple chats, multiple agents, or repeated GitHub-backed tasks, bootstrap through `ai-system/control-plane/README.md` and `ai-system/control-plane/registry.json` after reading `ai-system/registry.yml`.

- Use a GitHub Issue number as the canonical task identity; do not infer identity from remembered chat prose.
- Pin the base commit SHA and mint a unique `run_id` before planning.
- Give every writing actor a unique branch. Concurrent writers must never share one mutable branch.
- Before a plan exists, each writer establishes a **create-only ownership claim** on its own branch. Automatic takeover and force-push ownership transfer are forbidden. A stale/contested owner requires a new `run_id`.
- After the claim, commit the namespaced write plan on that same actor branch. No shared multi-writer plan ledger is allowed.
- The 編排代理 resolves each actor branch exactly once to a commit SHA, then reads the plan and ownership claim from that immutable commit. The approved plan/claim hashes are immutable snapshot evidence.
- Run `scripts/check_write_plan_conflicts.py` before task mutation. Unresolved write-set overlap is VETO; an explicit dependency serializes overlap.
- Before fan-in, run **snapshot-bound** execution verification with `scripts/verify_snapshot_bound_execution.py`. The final head must descend from the approved plan SHA, the branch must still point to the verified final head, and plan/claim hashes must not change.
- Actual task paths must remain inside the approved `write_set`; the only automatic control-plane exception is that actor's exact receipt path.
- After task work is complete, freeze the exact work head. A PASS/VETO receipt must be schema v2 and bind `claim_id`, `plan_head_sha`, executor/execution identity, branch, and `head_sha` = the pre-receipt work head.
- Commit the receipt as a **receipt-only evidence commit**. Snapshot-bound verification must prove the work head is in the approved lineage and the only path changed after it is that actor's own receipt.
- Before replacing an existing file, fetch its current blob SHA; a stale-SHA rejection is a conflict signal, never a reason to force the write.
- Keep plans, claims, receipts, and execution evidence namespaced by Issue/run/actor; never update a shared `latest` file.
- Immediately before integration, run `scripts/verify_run_freshness.py`. If the trusted target base moved, VETO the stale run and start a new `run_id`; do not reuse old PASS evidence.
- Fan-in uses the per-run branch `task/<issue>/<run_id>/integration`, then one final PR targets `main`.
- The ten-代理 contract is fail-closed: role definitions, branches, claims, snapshots, static CI lanes, or AI success messages are not proof of ten independent executions. Missing independent receipts remain `NOT_RUN`/`BLOCKED`.
- Persist wrapper-observed independence as receipt-v2 **runtime attestation**: process-instance identity, PID, spawn timestamp, backend-session hash, and stdout/stderr hashes. Never persist the raw backend session ID.
- After a local workflow, use `scripts/manage_local_agent_run.py` for `status / publish / integrate / publish-integration / recover / rehydrate / resume / cleanup`; actor publication is create-or-fast-forward only, integration re-adjudicates and re-checks the A07 task diff, and cleanup never silently discards dirty worktrees.
- For interrupted runs, `run_local_agent_workflow.py --resume-existing` may reuse only Git receipts that pass snapshot and runtime-attestation revalidation; an existing VETO receipt is terminal. After cleanup, `manage_local_agent_run.py rehydrate` restores worktrees from preserved branches. `publish-integration` is create-or-fast-forward only and never force-pushes divergence.
- If `_coordination` is lost, `manage_local_agent_run.py recover` must reconstruct the run from the ten preserved actor branches by locating the original plan commits, re-reading claims/plans, recomputing snapshot hashes, and re-running preflight/freshness before any receipt is reused.

- When a local Claude Code backend is used, run `scripts/local_agent_executor.py`; authentication must PASS before launch, otherwise the result is `BLOCKED` with zero model processes.
- Local executor independence is wrapper-observed: ten distinct wrapper-observed process instances, execution IDs, backend session IDs, workspaces, and branches are required. Model self-assertion is not independence evidence.
- Local executor tool access is a positive allowlist: read-only roles get `Read,Glob,Grep`, A07 gets `Read,Glob,Grep,Edit,Write`, and `Bash` is not granted by default.
- Convert local executor output to Git evidence only through `scripts/finalize_local_agent_execution.py`; model JSON is not itself a receipt. The finalizer requires claim identity, scope-checks A07 changes, rejects read-only mutations/staged changes, creates receipt v2, and does not push.
- Prepare local A01–A10 runs with `scripts/prepare_local_agent_run.py` before backend launch. Read-only roles must use `write_set: []`; only A07 may receive task write scope. Preparation is local-only, claim-before-plan, exact-base-bound, and does not push.
- Use `scripts/run_local_agent_workflow.py` for a complete local A01–A10 runtime. Direct `local_agent_executor.py` output is not completion evidence. Downstream agents run only after dependencies finalize PASS; A07 may not mount external dependency workspaces; full local PASS also requires deterministic receipt adjudication and fresh-base verification.

## Review expectations

For material changes, verify the exact diff, run the strongest relevant automated check, and perform a separate negative/adversarial check when practical. A green unrelated workflow is not proof of the requested behavior.


Recovery treats claim and plan history as immutable: each actor claim path and plan path may be touched by exactly one commit, and the sole claim commit must precede the sole plan commit. Any later edit is VETO rather than a new approved snapshot.


`status` treats committed actor-branch receipts as durable truth rather than worktree files: after cleanup, or when `workflow.json` is unavailable, it reads receipts from branch HEAD, re-runs snapshot verification and deterministic adjudication, and requires fresh base before reporting a finalized PASS stage.


Receipt evidence is graph-immutable: the final receipt-only commit must be the immediate single child of the declared work head. A second receipt-only rewrite commit is VETO even when the final file diff still contains only the receipt path.
