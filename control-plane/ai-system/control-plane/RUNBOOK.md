# Multi-chat / 10-agent GitHub Runbook

## 0. Bootstrap from any chat

1. Resolve the canonical repository from `ai-system/control-plane/registry.json`.
2. Read `AGENTS.md`, `ai-system/registry.yml`, `registry.json`, and `MULTI-CHAT-PROTOCOL.md`.
3. Resume by GitHub Issue number, never from chat memory alone.
4. Read the Issue, open PRs, run IDs, branch refs, claims, plans, and receipts before any mutation.

Repository files standardize behavior after GitHub is routed; they cannot force product-level connector selection. Explicit GitHub intent remains the routing fallback.

## 1. Define the task and pin the trusted base

- Keep exactly one canonical GitHub Issue for the task.
- Record acceptance criteria and risk.
- Resolve the exact current target/base commit SHA.
- Mint a collision-resistant `run_id`: `YYYYMMDDTHHMMSSZ-<nonce>`.
- Evidence from another run ID or another base SHA is not reusable PASS evidence.

## 2. Claim actor ownership before planning

Create one unique actor branch, for example:

`agent/<issue>/<A01-A10>/<run_id>`

Before the plan, create a claim conforming to `claim.schema.json` at:

`ai-system/control-plane/runs/<issue>/<run_id>/claims/<actor_id>.json`

The claim binds actor, branch, base SHA, claim ID, executor ID, and execution ID. Claim creation is **create-only**. Automatic takeover and force-push ownership transfer are forbidden. If another execution already owns the claim/branch, return VETO/BLOCKED; recovery uses a new `run_id` rather than replacing the owner inside the old run.

## 3. Declare immutable write intent on the actor branch

After the claim, commit one plan conforming to `write-plan.schema.json` at:

`ai-system/control-plane/runs/<issue>/<run_id>/plans/<actor_id>.json`

Declare the actor branch, pinned base SHA, exact repository-relative `write_set`, optional `read_set`, and `depends_on` edges. The actor may commit the claim and plan, but task mutation must not start yet.

Once A01 snapshots the plan, **do not rewrite the plan or claim**. A legitimate scope expansion requires a new run ID and new preflight; widening an already-approved snapshot retroactively is VETO.

## 4. A01 resolves refs once and snapshots by commit SHA

A01 uses the read-only collector:

```bash
python3 scripts/collect_write_plans_from_refs.py \
  --repo . \
  --issue <issue> \
  --run-id <run_id> \
  --entry A01=agent/<issue>/A01/<run_id> \
  --entry A02=agent/<issue>/A02/<run_id> \
  --output-dir /tmp/write-plans-<run_id> \
  --receipt /tmp/write-plan-collection.json
```

For each actor, the collector resolves the moving branch name to one immutable `plan_head_sha`, then reads the plan and claim from that SHA. The receipt records `plan_head_sha`, SHA-256 hashes for both plan and claim, and the bound claim/executor/execution IDs. A branch moving after resolution does not change the approved snapshot.

The collected plan directory and collection receipt are ephemeral execution evidence, not a shared mutable Git ledger.

## 5. Preflight all snapshot write sets

Run:

```bash
python3 scripts/check_write_plan_conflicts.py \
  /tmp/write-plans-<run_id> \
  --output /tmp/write-plan-preflight.json
```

Disjoint sets may run in parallel. Overlap without a dependency is VETO. Overlap with an explicit dependency is serialized. Dependency cycles, duplicate refs/branches, mismatched base SHAs, unknown dependencies, invalid paths, and traversal are VETO.

Only a PASS preflight unlocks task mutation.

## 6. Execute only on the claimed actor branch

- Never share one mutable branch between concurrent writers.
- Never force-push to transfer ownership.
- Read before write and use current blob SHA for replacement writes.
- Treat a stale blob SHA as a re-read/replan signal.
- Stay inside the approved `write_set`.
- Keep credentials outside Git and evidence namespaces distinct.

## 7. Freeze the exact task work head

After the approved task mutations and direct tests are complete, record the exact actor work head before any receipt is written:

```bash
git rev-parse HEAD
```

This SHA is the receipt's `head_sha`. In this contract, **`head_sha` = work head**: the exact task state before the final receipt-only evidence commit. It is deliberately not the receipt commit SHA, which would be self-referential if embedded in its own contents.

## 8. Emit a claim-bound v2 receipt as a receipt-only evidence commit

PASS/VETO receipts use `receipt.schema.json` schema version 2 and must bind:

- the same Issue, `run_id`, `agent_id`, role, and actor branch;
- the immutable `claim_id`;
- the approved `plan_head_sha`;
- the same executor ID and execution ID from the ownership claim;
- `head_sha` = the pre-receipt work head;
- the independent-execution flag, evidence partition, and direct evidence.

Write the receipt at:

`ai-system/control-plane/runs/<issue>/<run_id>/receipts/<agent_id>.json`

Then commit **only that receipt path**. This is the actor's receipt-only evidence commit. Do not combine new task changes, plan/claim edits, or another actor's receipt with this commit.

Historical v1 `NOT_RUN` receipts may remain as archival blocker evidence. A v1 PASS/VETO receipt is invalid and cannot adjudicate to runtime PASS.

## 9. Verify snapshot-bound execution and receipt identity before fan-in

Materialize the actor's snapshot object from A01's collection receipt, then verify the final branch head (the receipt evidence commit):

```bash
python3 scripts/verify_snapshot_bound_execution.py \
  --repo . \
  --issue <issue> \
  --run-id <run_id> \
  --actor <actor_id> \
  --snapshot-json <actor-snapshot.json> \
  --final-head <exact-receipt-commit-sha> \
  --output /tmp/snapshot-verification-<actor_id>.json
```

PASS requires all of the following:

- the actor branch still resolves to the exact final receipt commit;
- the approved `plan_head_sha` is an ancestor of the receipt-declared work head;
- that work head is an ancestor of the final receipt commit;
- the plan and ownership claim still match their approved SHA-256 snapshots;
- the receipt is schema v2 and its Issue/run/actor/branch/`claim_id`/executor/execution/`plan_head_sha` all match the immutable snapshot;
- task paths changed from plan head through work head stay inside the approved `write_set`;
- paths changed from work head through final head are **exactly** that actor's own receipt path.

Any receipt identity mismatch, branch drift, invalid lineage, plan/claim rewrite, old-snapshot replay, foreign receipt path, undeclared task path, or extra post-work mutation is VETO.

## 10. Adjudicate the ten independent 代理

Run:

```bash
python3 scripts/adjudicate_agent_receipts.py \
  ai-system/control-plane/runs/<issue>/<run_id>/receipts \
  --issue <issue> \
  --run-id <run_id> \
  --output agent-adjudication.json
```

The adjudicator only accepts PASS/VETO receipt schema v2. Runtime PASS requires A01-A10 all PASS, distinct executor/execution/evidence partitions and branches, zero VETO/missing receipts, and no direct failing evidence. Majority vote cannot override VETO.

Snapshot-bound verification and adjudication are separate gates: the former proves each receipt belongs to the approved claim/work lineage; the latter proves the ten-agent aggregate contract.

## 11. Re-check base freshness

Immediately before integration, resolve the trusted current target/base SHA and run:

```bash
python3 scripts/verify_run_freshness.py \
  --pinned <run-base-sha> \
  --current <current-target-base-sha> \
  --output /tmp/base-freshness.json
```

If the target base moved, the result is VETO. Do not reuse the old run's PASS evidence after another run or human merge changes the base; start a new `run_id`, re-pin and replan.

## 12. Fan in on a per-run integration branch

The integration branch is run-scoped:

`task/<issue>/<run_id>/integration`

A10 is the single merge owner for that run. Only actors with PASS snapshot-bound receipt verification may enter fan-in. Never use the old shared `task/<issue>/integration` pattern and never force-write actor branches.

Open one final integration PR to `main`. A merge queue may add another latest-base revalidation layer when available, but it does not replace repository claim/snapshot/receipt gates.

## 13. Verify exact revision

Verify the final PR head SHA and all relevant evidence: ownership claims, immutable snapshot collection, write-set preflight, receipt-bound per-actor snapshot verification, ten independent receipts/adjudication, base freshness, tests/checks, and adversarial evidence. A prior-head success, unrelated workflow, or job that never acquired a runner is not PASS.

## 14. Close

Move to `MERGED` only after the final integration PR is actually merged and the merge SHA is recorded. If billing, permissions, runtime capability, or independent executors are unavailable, keep the task `BLOCKED` with the exact blocker. Never convert missing execution into PASS.

## Local executor preflight and launch

Before treating A01–A10 as independently executed, prepare ten distinct Git workspaces/branches and an assignments JSON, then probe the backend without launching a model:

```bash
python3 scripts/local_agent_executor.py --claude-path ~/.local/bin/claude --probe-only
```

If authentication is unavailable, the only valid result is `BLOCKED` and zero model processes. After authentication, launch with an explicit per-agent budget and output directory. Runtime independence requires ten distinct wrapper-observed process instances, execution IDs, Claude session IDs, workspaces, and branches. Tool permissions are a **positive allowlist**: read-only roles get `Read,Glob,Grep`; A07 gets `Read,Glob,Grep,Edit,Write`; `Bash` is denied by omission for every role unless a future separately reviewed contract explicitly adds a safe shell capability. Any child exit, missing/duplicate session, duplicate workspace/branch, or malformed structured decision fails closed. A runner PASS is executor evidence only; final task PASS still requires claim-bound receipt v2 materialization, snapshot verification, A01–A10 adjudication, and fresh-base verification.

## Finalize one local execution into receipt v2

After a local actor process finishes, do not copy its model JSON directly into Git. Use the trusted finalizer with the collector-produced actor snapshot and wrapper-produced execution row:

```bash
python3 scripts/finalize_local_agent_execution.py --repo <actor-workspace> --actor A07 --snapshot-json <actor-snapshot.json> --execution-json <executor-output/A07.json> --output <finalization.json>
```

The execution identity must match the predeclared claim. Read-only agents must have a clean workspace. A07 changes are committed only after write-set scope verification. Existing staged changes are VETO. The finalizer writes receipt schema v2, creates a receipt-only commit, runs snapshot verification, and never pushes the branch. Only then may the receipt enter ten-agent adjudication.

## Prepare ten local agent workspaces before backend launch

Use the preparer before `local_agent_executor.py`. It does not call Claude and does not push Git refs:

```bash
python3 scripts/prepare_local_agent_run.py   --repo .   --issue <issue>   --run-id <new-run-id>   --base-sha <exact-current-base-sha>   --base-ref <trusted-base-ref>   --workspace-root /tmp/agent-run-<run-id>   --plan-config <optional-plan-config.json>
```

By default all ten actors are task read-only (`write_set: []`). Only A07 may receive a non-empty `write_set` via plan config; any non-A07 task write scope is VETO before worktree creation. The preparer rejects dirty source worktrees, stale base refs, existing run branches, non-empty/colliding workspace roots, malformed configuration and invalid prospective plans before mutation. It then creates claim→plan commits, collects immutable plan snapshots, performs committed preflight, writes `assignments.json`/`snapshots.json` under the non-Git coordination directory, and creates `task/<issue>/<run_id>/integration` locally. A preparer PASS is readiness evidence only, not model execution evidence.

Record every OS PID, but do not reject a valid staged run solely because the OS reused a numeric PID after an earlier process exited. Use the wrapper-observed process-instance identity for uniqueness.

## Run the dependency-aware local workflow

After preparation PASS and backend authentication PASS, run the orchestration layer rather than invoking the low-level executor as a completion path:

```bash
python3 scripts/run_local_agent_workflow.py   --preparation-json <workspace-root>/_coordination/run-preparation.json   --claude-path ~/.local/bin/claude   --output-dir <workspace-root>/_runtime   --max-parallel 3   --max-budget-usd <per-agent-cap>
```

The orchestrator executes A01 first; A02/A03/A04 after A01; then A05, A06, A07, A08, A09 and A10 according to the prepared dependency DAG. A dependency non-PASS blocks downstream launch. Read-only dependent roles receive finalized dependency workspaces through `--add-dir`; A07 never receives external workspaces and instead receives trusted dependency receipt summaries. Each actor result is finalized before its dependents can run. Full local PASS additionally requires deterministic ten-receipt adjudication and fresh-base verification. The orchestrator does not push or merge remote refs.

## Durable runtime attestation

Every schema-v2 PASS/VETO receipt carries a **runtime attestation** produced by the trusted wrapper, not by model self-report. It persists the provider, wrapper-observed process-instance ID, OS PID, monotonic spawn timestamp, backend-session SHA-256, and stdout/stderr SHA-256 values. The raw backend session ID is never persisted in Git. Ten PASS receipts must have distinct process-instance IDs and distinct backend-session hashes.

## Run lifecycle manager

`scripts/manage_local_agent_run.py` owns **status / publish / integrate / publish-integration / recover / rehydrate / resume / cleanup** after local preparation and execution. `status` reconciles local heads, receipts, remote heads and base freshness. `publish` creates or fast-forwards actor branches only; divergence is VETO and force push is forbidden. `integrate` requires workflow PASS, adjudication PASS and fresh base, merges all ten finalized actor heads into the per-run integration branch, re-adjudicates receipts, and requires the integrated task diff to equal the already verified A07 task diff before writing an integration-only receipt. `cleanup` refuses dirty worktrees unless an explicit force flag is supplied and never deletes remote evidence branches.

### Resume, rehydrate, and integration publication

A BLOCKED or interrupted run may resume under the **same run_id** only when the pinned base is still fresh and every reused PASS receipt is re-read from Git, passes snapshot verification, and passes durable runtime-attestation validation. Only actors without a reusable receipt are launched again. An existing VETO receipt is terminal for that run and cannot be overwritten by a later model answer.

After safe cleanup, `python3 scripts/manage_local_agent_run.py rehydrate --preparation-json <...>` restores missing actor worktrees from their preserved local branches without reset, force, or remote mutation. After local integration PASS, `publish-integration` publishes the per-run integration branch using create-or-fast-forward semantics only; divergence is VETO.

### Git-only recovery after coordination loss

If the previous `_coordination` directory is gone, `python3 scripts/manage_local_agent_run.py recover --source-repo <repo> --issue <N> --run-id <run> --base-ref <main> --workspace-root <new-root>` reconstructs the preparation contract from the ten preserved actor branches. It finds each original plan commit from Git history, re-reads the claim/plan at that immutable commit, recomputes SHA-256 snapshot hashes, re-runs the ten-plan preflight and base-freshness gate, then restores worktrees. It does not require the old coordination JSON and performs no remote mutation. Durable receipts can then be reused only through `--resume-existing`, which revalidates snapshot and runtime attestation.


`resume` revalidates existing receipt snapshot + durable runtime attestation before reuse. If every actor receipt is reusable, resume requires no provider binary or login and performs zero model executions; a Claude path is needed only when one or more actors are actually missing and must be launched.


Recovery treats claim and plan history as immutable: each actor claim path and plan path may be touched by exactly one commit, and the sole claim commit must precede the sole plan commit. Any later edit is VETO rather than a new approved snapshot.


`status` treats committed actor-branch receipts as durable truth rather than worktree files: after cleanup, or when `workflow.json` is unavailable, it reads receipts from branch HEAD, re-runs snapshot verification and deterministic adjudication, and requires fresh base before reporting a finalized PASS stage.


Receipt evidence is graph-immutable: the final receipt-only commit must be the immediate single child of the declared work head. A second receipt-only rewrite commit is VETO even when the final file diff still contains only the receipt path.
