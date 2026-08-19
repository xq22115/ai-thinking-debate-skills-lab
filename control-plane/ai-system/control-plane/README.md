# GitHub Agent Control Plane v3

This directory is the canonical repository-level control plane for multi-chat, multi-agent GitHub work. It extends `AGENTS.md`; it does not replace GitHub permissions, product routing, or an orchestration runtime.

## Hard invariants

1. **GitHub Issue = task system of record.** One Issue anchors acceptance criteria and risk.
2. **One writer per branch.** Concurrent actors never share a mutable branch.
3. **Run identity is explicit.** Every run has a unique `run_id`, pinned base SHA, and per-run integration branch.
4. **Ownership claim precedes planning.** Every writer creates one create-only `claim.schema.json` claim on its actor branch. Automatic takeover and force-push ownership transfer are forbidden; recovery uses a new run ID.
5. **Plans live on actor branches.** There is no shared mutable plan ledger.
6. **A01 snapshots refs by commit SHA.** The collector resolves each moving branch name once, then reads plan and claim from that immutable SHA and records SHA-256 hashes plus claim/executor/execution identity.
7. **Declare intent before mutation.** Cross-ref write-set preflight must PASS before task work starts.
8. **Snapshot-bound execution.** Before fan-in, the verified final head must be the actor branch head, descend from the approved plan SHA, preserve the approved plan/claim hashes, and remain within the write set.
9. **Receipt identity is claim-bound.** PASS/VETO receipts use schema v2 and must repeat the immutable `claim_id`, `plan_head_sha`, branch, executor/execution identity, and `head_sha` = pre-receipt work head.
11. **Receipt-only evidence commit.** After the work head is frozen, the only allowed path change before final snapshot verification is the actor's own namespaced receipt; a foreign receipt or extra task change is VETO.
10. **Optimistic concurrency.** Existing-file updates use current blob SHA; stale SHA means re-read/replan, never force.
12. **Append-only evidence.** Claims, plans, receipts and run evidence are namespaced; no shared `latest.json`.
13. **Base freshness before fan-in.** If current target base differs from the pinned base, the stale run is VETO and must restart under a new `run_id`.
14. **Per-run fan-in.** Integration branch is `task/<issue>/<run_id>/integration`, never a per-Issue shared branch.
15. **All ten runtime gates.** A01-A10 must each produce authentic independent PASS receipts, with zero VETO and zero missing.
16. **Static CI is not an agent vote.** Ten deterministic lanes validate repository contracts but do not prove ten independent AI executions.
17. **Exact-revision evidence.** Completion cites the exact commit/PR/test/workflow evidence that verified the result.
18. **No secrets in Git.** Use platform/task-scoped runtime identity instead of committed credentials.

## Seven separate gates

### 1. Ownership-claim gate
`claim.schema.json` binds issue, run, actor, branch, base SHA, claim ID, executor ID and execution ID. Claims are create-only; contested ownership fails closed.

### 2. Immutable snapshot collection gate
`scripts/collect_write_plans_from_refs.py` resolves each actor ref to `plan_head_sha`, reads the plan and claim from that SHA, and emits SHA-256 hashes. Collection is read-only across refs and ephemeral.

### 3. Write-set conflict gate
`scripts/check_write_plan_conflicts.py` rejects unsafe paths, mismatched bases, duplicate branches/refs, dependency cycles, and unresolved write-set overlap.

### 4. Snapshot-bound execution + receipt-binding gate
`scripts/verify_snapshot_bound_execution.py` checks branch-head identity, plan/work/final ancestry, immutable plan/claim hashes, receipt v2 identity against the claim snapshot, task diff scope through the receipt-declared work head, replay resistance, and that the final evidence commit changes only the exact own-receipt path.

### 5. Ten-independent-代理 adjudication gate
`scripts/adjudicate_agent_receipts.py` requires all A01-A10 PASS, distinct executor/execution/evidence/branch identities, zero VETO/missing receipts, and no direct failing evidence. Repository receipts alone do not prove physical/model-process independence.

### 6. Base-freshness gate
`scripts/verify_run_freshness.py` rejects a run when the trusted current target base no longer equals its pinned base SHA. Old PASS evidence cannot cross that boundary.

### 7. Repository/static gate
`.github/workflows/agent-control-plane-10-gate.yml` runs ten deterministic lanes plus the contract/unit tests on an exact revision. It is repository verification, not independent-agent execution evidence.

## Bootstrap for any chat

Read in order: `AGENTS.md` → `ai-system/registry.yml` → `registry.json` → task Issue → pinned base SHA → active run claims/plans/refs. A writing chat that cannot establish a unique run/actor branch and create-only claim may read, but must not mutate.

## Why this layout

The design separates the control plane from task data. Mutable work stays isolated by branch, coordination uses immutable Git snapshots, integration is serialized per run, and every PASS claim remains attributable to an exact revision.

## Local independent executor gate

`scripts/local_agent_executor.py` is the local execution backend for turning the ten role contracts into externally observed independent model processes. It probes Claude Code authentication before launch and returns `BLOCKED` with zero model processes when authentication is unavailable.

A local executor PASS requires ten distinct wrapper-observed process instances, wrapper-minted execution IDs, backend session IDs, Git workspaces, and actor branches. Model text claiming independence is never accepted as independence evidence. Tool access uses a **positive allowlist**: A01–A06 and A08–A10 receive only `Read,Glob,Grep`; A07 receives only `Read,Glob,Grep,Edit,Write`. `Bash` is not granted by default to any role, so shell writes cannot bypass the write-set/snapshot gates. Raw executor output stays outside Git until a trusted receipt-materialization step binds it to claim-bound receipt v2 evidence.

## Trusted local execution finalizer

`scripts/finalize_local_agent_execution.py` is the only repository-approved bridge from ephemeral local-executor output to claim-bound receipt v2 evidence. It requires the execution row to match the immutable claim/plan snapshot. Read-only agents must have a clean workspace; any mutation is VETO. A07 may have task changes, but the trusted wrapper verifies those paths against the approved write set before creating the task commit. Pre-existing staged changes are VETO.

The finalizer never pushes a remote branch. It creates at most a trusted A07 task commit followed by the actor's receipt-only commit, then runs the snapshot-bound verifier. Finalized evidence is eligible for A01–A10 adjudication only when snapshot verification passes.

## Local ten-agent run preparer

`scripts/prepare_local_agent_run.py` prepares a run without launching any model and without pushing any remote branch. It requires a clean source worktree, an exact pinned base that still matches the selected base ref, a workspace root outside the source repository, and collision-free run/branch names.

The preparer creates exactly ten local actor worktrees/branches. Each actor receives a create-only ownership claim commit followed by a plan commit. Read-only roles A01–A06/A08–A10 use an empty task `write_set`; A07 is the only role that may receive an explicit task write scope. Empty write sets are valid and remain fail-closed because any later task diff is undeclared and therefore VETO.

The role dependency DAG is staged rather than blindly concurrent: A01 first; A02/A03/A04 after A01; A05; A06; A07; A08; A09; then A10. After all claim/plan commits, the preparer runs immutable cross-ref collection and committed write-plan preflight, emits claim-bound executor assignments/snapshots into an ephemeral coordination directory, and creates the per-run integration branch only after preflight PASS.

Numeric OS PIDs are recorded for audit, but PID reuse across sequential waves is valid; independence is keyed to distinct observed `Popen` process instances plus execution/session/workspace identity.

## Dependency-aware local ten-agent orchestrator

`scripts/run_local_agent_workflow.py` is the only local path eligible to claim a complete A01–A10 runtime cycle. `local_agent_executor.py` is a low-level subprocess primitive and is **not** completion evidence by itself.

The orchestrator runs the role dependency DAG in waves. A downstream actor launches only after every declared dependency finalized PASS; any VETO/FAIL/BLOCKED dependency blocks downstream launch. Read-only roles may mount finalized dependency workspaces with `--add-dir`; A07 is forbidden from mounting external workspaces because it has Edit/Write capability, so A07 receives trusted dependency receipt summaries in its prompt instead.

Every launched actor still gets a distinct wrapper-observed process instance, predeclared claim execution identity, backend session and isolated workspace. After each model result, the trusted finalizer materializes scope-checked receipt v2 evidence. Only when A01–A10 all finalize PASS does the orchestrator collect receipts ephemerally, run deterministic ten-receipt adjudication, and finally check the pinned target base for freshness. A local workflow PASS therefore means `A01-A10 PASS + adjudication PASS + base freshness PASS`; it still does not push or merge GitHub branches.

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
