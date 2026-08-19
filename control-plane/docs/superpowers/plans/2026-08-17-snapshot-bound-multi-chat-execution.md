# Snapshot-Bound Multi-Chat Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Bind every multi-chat execution to an immutable ownership claim and approved plan snapshot, isolate integration per run, and fail closed on branch/base drift or replayed evidence.

**Architecture:** Each actor creates a one-shot claim and plan on its isolated branch. A01 resolves moving refs to exact commit SHAs, hashes the approved plan/claim, and verification later proves the final branch descends from that snapshot without rewriting either contract. Integration branches are per-run, not per-issue.

**Tech Stack:** Python 3 stdlib, Git CLI, JSON Schema documents, GitHub branch/PR conventions, unittest.

## Global Constraints

- No time-based automatic claim takeover; recovery uses a new `run_id`.
- No force-push ownership transfer.
- Plan/claim snapshots are immutable after preflight.
- Actual task diff must remain inside the approved `write_set`; only the actor's exact receipt path is an evidence exception.
- Stale base SHA at final integration is VETO/replan.
- Repository/static PASS does not satisfy the ten truly independent 代理 runtime gate.

---

### Task 1: Actor ownership claim contract

**Files:**
- Create: `ai-system/control-plane/claim.schema.json`
- Create: `tests/test_actor_claims.py`
- Modify: `ai-system/control-plane/registry.json`
- Modify: `scripts/validate_agent_control_plane.py`

**Interfaces:**
- Produces claim fields: `issue_number`, `run_id`, `actor_id`, `branch`, `base_sha`, `claim_id`, `executor_id`, `execution_id`, `status=CLAIMED`.

- [x] Write failing tests for missing claim contract, foreign executor, actor/branch mismatch and forbidden overwrite semantics.
- [x] Run `python3 -m unittest -v tests.test_actor_claims` and verify RED.
- [x] Add schema/registry/static-validator rules with create-only, no takeover, no force-push semantics.
- [x] Re-run claim tests and verify GREEN.

### Task 2: Immutable ref snapshot collection

**Files:**
- Modify: `scripts/collect_write_plans_from_refs.py`
- Modify: `tests/test_collect_write_plans_from_refs.py`

**Interfaces:**
- Collector output adds `snapshots[actor_id] = {branch, plan_head_sha, plan_sha256, claim_sha256, claim_id, executor_id, execution_id}`.
- Plan and claim are read using the resolved commit SHA, not the moving ref name.

- [x] Add failing tests where a ref moves after resolution, plan/claim hashes are asserted, and missing/mismatched claims VETO.
- [x] Run collector tests and verify RED.
- [x] Implement `git rev-parse <ref>^{commit}`, SHA-bound `git show`, SHA-256 hashing, and snapshot receipt output.
- [x] Re-run collector tests and verify GREEN.

### Task 3: Snapshot-bound execution verifier

**Files:**
- Create: `scripts/verify_snapshot_bound_execution.py`
- Create: `tests/test_snapshot_bound_execution.py`
- Modify: `scripts/verify_write_plan_scope.py` only if needed for the exact receipt-path exception.

**Interfaces:**
- `verify_execution(repo, plan, snapshot, final_head_sha) -> dict`.
- PASS requires current branch head equals `final_head_sha`, plan snapshot ancestor of final head, plan/claim hashes unchanged, and changed paths are scope-safe.

- [x] Add failing tests for non-descendant final head, moving branch, plan rewrite, claim rewrite, undeclared file, foreign receipt path and replayed old snapshot.
- [x] Run snapshot verifier tests and verify RED.
- [x] Implement minimal Git ancestry/hash/diff verification and exact own-receipt exception.
- [x] Re-run tests and verify GREEN.

### Task 4: Run-isolated fan-in and stale-base gate

**Files:**
- Modify: `ai-system/control-plane/registry.json`
- Modify: `ai-system/control-plane/run-contract.schema.json`
- Modify: `ai-system/control-plane/state-machine.json`
- Create: `scripts/verify_run_freshness.py`
- Create: `tests/test_run_freshness.py`

**Interfaces:**
- Integration branch template becomes `task/{issue_number}/{run_id}/integration`.
- `verify_freshness(pinned_base_sha, current_base_sha) -> PASS|VETO`.

- [x] Add failing tests rejecting the old shared integration template and stale base SHA.
- [x] Run freshness tests and verify RED.
- [x] Implement per-run integration namespace, run schema fields and stale-base verifier.
- [x] Re-run tests and verify GREEN.

### Task 5: Wire governance and exact-head verification

**Files:**
- Modify: `ai-system/control-plane/RUNBOOK.md`
- Modify: `ai-system/control-plane/README.md`
- Modify: `AGENTS.md`
- Modify: `.github/agent-core-policy.yml`
- Modify: `.github/required-checks.yml`
- Modify: `.github/CODEOWNERS`
- Modify: `.github/workflows/agent-control-plane-10-gate.yml`
- Modify: `tests/test_agent_control_plane.py`

**Interfaces:**
- Static validator exposes checks for claim ownership, SHA-bound plan collection, snapshot-bound execution, per-run integration namespace and base freshness.

- [x] Add registration tests before production wiring and verify RED.
- [x] Wire all new scripts/schemas/tests into policy, manifest, CODEOWNERS and workflow.
- [x] Run all repository `tests/test_*.py` modules explicitly, `scripts/validate_control_contracts.py`, YAML parsing and clean-worktree check.
- [x] Re-clone/reset the exact PR head SHA on the connected Mac and repeat the full verification before updating the PR evidence.

### Task 6: Bind final receipt contents to the immutable ownership claim

**Files:** `receipt.schema.json`, receipt adjudicator, snapshot verifier, governance/docs/tests.

- [x] Reproduce that a correct receipt path with a foreign executor currently passes snapshot verification.
- [x] Require PASS/VETO receipt schema v2 with `claim_id` and `plan_head_sha`; preserve historical v1 `NOT_RUN` compatibility.
- [x] Define receipt `head_sha` as pre-receipt work head and enforce `plan -> work -> receipt commit` ancestry.
- [x] Require the final post-work diff to contain exactly the actor's own receipt path.
- [x] Bind receipt actor/branch/claim/executor/execution/plan identity to the immutable claim snapshot.
- [x] Add fail-closed governance registration and run full regression / contract / YAML verification.
