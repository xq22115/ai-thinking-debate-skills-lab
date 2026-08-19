#!/usr/bin/env python3
"""Lifecycle manager for prepared/finalized local A01-A10 runs."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

try:
    from scripts.adjudicate_agent_receipts import adjudicate
    from scripts.run_local_agent_workflow import run_workflow
    from scripts.verify_run_freshness import verify_freshness
    from scripts.verify_snapshot_bound_execution import verify_execution
    from scripts.check_write_plan_conflicts import evaluate_plans
except ModuleNotFoundError:
    from adjudicate_agent_receipts import adjudicate
    from run_local_agent_workflow import run_workflow
    from verify_run_freshness import verify_freshness
    from verify_snapshot_bound_execution import verify_execution
    from check_write_plan_conflicts import evaluate_plans

EXPECTED_ACTORS = [f"A{i:02d}" for i in range(1, 11)]


def _git(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args], text=True,
        capture_output=True, check=False,
    )


def _git_text(repo: pathlib.Path, *args: str) -> str | None:
    cp = _git(repo, *args)
    return cp.stdout.strip() if cp.returncode == 0 else None


def _assignment_map(preparation: dict) -> dict[str, dict]:
    return {str(row.get("actor_id")): row for row in preparation.get("assignments", [])}

def _remote_head(repo: pathlib.Path, remote: str, branch: str) -> str | None:
    cp = _git(repo, "ls-remote", "--heads", remote, f"refs/heads/{branch}")
    if cp.returncode != 0:
        return None
    line = cp.stdout.strip()
    return line.split()[0] if line else None


def _current_base(preparation: dict) -> str:
    repo = pathlib.Path(str(preparation.get("source_repo", "")))
    base_ref = str(preparation.get("base_ref", ""))
    return _git_text(repo, "rev-parse", "--verify", f"{base_ref}^{{commit}}") or ""


def inspect_run(preparation: dict, workflow: dict | None = None, *, remote: str = "origin") -> dict[str, object]:
    failures: list[str] = []
    repo = pathlib.Path(str(preparation.get("source_repo", "")))
    assignments = _assignment_map(preparation)
    if preparation.get("result") != "PASS":
        failures.append("preparation_not_pass")
    if not repo.is_dir() or _git_text(repo, "rev-parse", "HEAD") is None:
        failures.append("source_repo_unavailable")
    if set(assignments) != set(EXPECTED_ACTORS):
        failures.append("assignment_actor_set_mismatch")
    actors: dict[str, dict] = {}
    receipt_payloads: dict[str, dict] = {}
    snapshots = preparation.get("snapshots") or {}
    finalizations = (workflow or {}).get("finalizations") or {}
    for actor in EXPECTED_ACTORS:
        row = assignments.get(actor, {})
        workspace = pathlib.Path(str(row.get("workspace", "")))
        branch = str(row.get("branch", ""))
        local_head = _git_text(repo, "rev-parse", "--verify", f"refs/heads/{branch}") if branch else None
        receipt_rel = f"ai-system/control-plane/runs/{preparation.get('issue_number')}/{preparation.get('run_id')}/receipts/{actor}.json"
        receipt_source = None
        receipt_result = None
        receipt_payload = None
        receipt_text = _git_text(repo, "show", f"{local_head}:{receipt_rel}") if local_head else None
        if receipt_text is not None:
            receipt_source = "git-head"
            try:
                receipt_payload = json.loads(receipt_text)
                receipt_result = receipt_payload.get("result")
            except json.JSONDecodeError:
                receipt_result = "INVALID"
        elif workspace.is_dir() and (workspace / receipt_rel).is_file():
            receipt_source = "worktree"
            try:
                receipt_payload = json.loads((workspace / receipt_rel).read_text(encoding="utf-8"))
                receipt_result = receipt_payload.get("result")
            except (OSError, json.JSONDecodeError):
                receipt_result = "INVALID"
        receipt_exists = receipt_source is not None
        if receipt_exists and isinstance(receipt_payload, dict):
            receipt_payloads[actor] = receipt_payload
        snapshot_result = {"result": "NOT_RUN"}
        if receipt_exists and local_head and isinstance(snapshots.get(actor), dict):
            snapshot_result = verify_execution(
                repo, int(preparation.get("issue_number") or 0),
                str(preparation.get("run_id") or ""), actor, snapshots[actor], local_head
            )
            if snapshot_result.get("result") != "PASS":
                failures.append(f"status_snapshot_verification_not_pass:{actor}")
        actors[actor] = {
            "branch": branch,
            "workspace": str(workspace),
            "workspace_exists": workspace.is_dir(),
            "local_head": local_head,
            "remote_head": _remote_head(repo, remote, branch) if branch and repo.is_dir() else None,
            "plan_head_sha": row.get("plan_head_sha"),
            "final_head_sha": (finalizations.get(actor) or {}).get("final_head_sha"),
            "receipt_exists": receipt_exists,
            "receipt_source": receipt_source,
            "receipt_result": receipt_result,
            "snapshot_verification": snapshot_result.get("result"),
            "status": ((workflow or {}).get("statuses") or {}).get(actor) or receipt_result,
        }
    if receipt_payloads:
        with tempfile.TemporaryDirectory() as td:
            receipt_dir = pathlib.Path(td)
            for actor, payload in receipt_payloads.items():
                (receipt_dir / f"{actor}.json").write_text(
                    json.dumps(payload, ensure_ascii=False), encoding="utf-8"
                )
            derived_adjudication = adjudicate(
                receipt_dir, int(preparation.get("issue_number") or 0),
                str(preparation.get("run_id") or "")
            )
    else:
        derived_adjudication = {"result": "NOT_RUN"}
    base_freshness = verify_freshness(
        str(preparation.get("base_sha", "")), _current_base(preparation)
    ) if not failures else {"result": "NOT_RUN"}
    workflow_result = (workflow or {}).get("result")
    effective_result = workflow_result or (derived_adjudication.get("result") if derived_adjudication.get("result") != "NOT_RUN" else None)
    remote_count = sum(1 for row in actors.values() if row["remote_head"])
    all_snapshots_verified = all(
        (not row["receipt_exists"]) or row["snapshot_verification"] == "PASS"
        for row in actors.values()
    )
    if effective_result == "PASS" and all(row["receipt_exists"] for row in actors.values()) and all_snapshots_verified and base_freshness.get("result") == "PASS":
        stage = "FINALIZED_PASS_PUBLISHED" if remote_count == 10 else "FINALIZED_PASS_UNPUBLISHED"
    elif effective_result in {"VETO", "FAIL", "BLOCKED"}:
        stage = f"FINALIZED_{effective_result}"
    else:
        stage = "PREPARED"
    return {
        "schemaVersion": 1,
        "issue_number": preparation.get("issue_number"),
        "run_id": preparation.get("run_id"),
        "stage": stage,
        "actors": actors,
        "remote_actor_count": remote_count,
        "integration_branch": preparation.get("integration_branch"),
        "integration_local_head": _git_text(repo, "rev-parse", "--verify", f"refs/heads/{preparation.get('integration_branch')}") if repo.is_dir() else None,
        "integration_remote_head": _remote_head(repo, remote, str(preparation.get("integration_branch", ""))) if repo.is_dir() else None,
        "base_freshness": base_freshness,
        "derived_adjudication": derived_adjudication,
        "failures": failures,
        "result": "PASS" if not failures else "VETO",
    }


def _is_ancestor(repo: pathlib.Path, older: str, newer: str) -> bool:
    return _git(repo, "merge-base", "--is-ancestor", older, newer).returncode == 0


def publish_run(preparation: dict, workflow: dict | None = None, *, remote: str = "origin") -> dict[str, object]:
    repo = pathlib.Path(str(preparation.get("source_repo", "")))
    assignments = _assignment_map(preparation)
    finalizations = (workflow or {}).get("finalizations") or {}
    failures: list[str] = []
    unchanged: list[str] = []
    to_push: list[tuple[str, str, str]] = []
    if preparation.get("result") != "PASS":
        failures.append("preparation_not_pass")
    if not repo.is_dir():
        failures.append("source_repo_unavailable")
    if set(assignments) != set(EXPECTED_ACTORS):
        failures.append("assignment_actor_set_mismatch")
    if failures:
        return {"schemaVersion": 2, "pushed": [], "unchanged": [], "failures": failures, "result": "VETO"}

    # Phase 1: validate every local head and every remote ancestry before any push.
    remote_heads: dict[str, str | None] = {}
    any_remote = False
    for actor in EXPECTED_ACTORS:
        assignment = assignments[actor]
        branch = str(assignment["branch"])
        local_head = _git_text(repo, "rev-parse", "--verify", f"refs/heads/{branch}") or ""
        expected_head = str((finalizations.get(actor) or {}).get("final_head_sha") or assignment.get("plan_head_sha") or "")
        if not expected_head or local_head != expected_head:
            failures.append(f"local_head_mismatch:{actor}")
            continue
        remote_head = _remote_head(repo, remote, branch)
        remote_heads[actor] = remote_head
        if remote_head == local_head:
            unchanged.append(actor)
        else:
            to_push.append((actor, branch, local_head))
            any_remote = any_remote or bool(remote_head)

    if any_remote:
        fetch = _git(repo, "fetch", "-q", remote, "+refs/heads/*:refs/remotes/%s/*" % remote)
        if fetch.returncode != 0:
            failures.append("remote_fetch_failed")
        else:
            for actor, branch, local_head in to_push:
                remote_head = remote_heads.get(actor)
                if not remote_head:
                    continue
                fetched = _git_text(repo, "rev-parse", f"refs/remotes/{remote}/{branch}") or ""
                if fetched != remote_head or not _is_ancestor(repo, remote_head, local_head):
                    failures.append(f"remote_not_fast_forward:{actor}")

    if failures:
        return {
            "schemaVersion": 2, "remote": remote, "pushed": [],
            "unchanged": sorted(unchanged), "atomic_push_attempted": False,
            "failures": sorted(set(failures)), "result": "VETO",
        }
    if not to_push:
        return {
            "schemaVersion": 2, "remote": remote, "pushed": [],
            "unchanged": sorted(unchanged), "atomic_push_attempted": False,
            "failures": [], "result": "PASS",
        }

    # Phase 2: all changed actor refs publish in one atomic transaction.
    refspecs = [f"refs/heads/{branch}:refs/heads/{branch}" for _, branch, _ in to_push]
    push = _git(repo, "push", "--atomic", remote, *refspecs)
    if push.returncode != 0:
        return {
            "schemaVersion": 2, "remote": remote, "pushed": [],
            "unchanged": sorted(unchanged), "atomic_push_attempted": True,
            "failures": [f"atomic_push_failed:{push.stderr.strip()}"], "result": "VETO",
        }

    readback_failures: list[str] = []
    pushed: list[str] = []
    for actor, branch, local_head in to_push:
        readback = _remote_head(repo, remote, branch)
        if readback != local_head:
            readback_failures.append(f"remote_readback_mismatch:{actor}")
        else:
            pushed.append(actor)
    return {
        "schemaVersion": 2, "remote": remote, "pushed": sorted(pushed),
        "unchanged": sorted(unchanged), "atomic_push_attempted": True,
        "failures": readback_failures,
        "result": "PASS" if not readback_failures else "FAIL",
    }


def publish_integration(preparation: dict, integration: dict, *, remote: str = "origin") -> dict[str, object]:
    failures: list[str] = []
    repo = pathlib.Path(str(preparation.get("source_repo", "")))
    if preparation.get("result") != "PASS":
        failures.append("preparation_not_pass")
    if integration.get("result") != "PASS":
        failures.append("integration_not_pass")
    if not repo.is_dir():
        failures.append("source_repo_unavailable")
    branch = str(preparation.get("integration_branch", ""))
    expected_head = str(integration.get("integration_head_sha", ""))
    local_head = _git_text(repo, "rev-parse", "--verify", f"refs/heads/{branch}") if repo.is_dir() and branch else None
    if not branch:
        failures.append("integration_branch_missing")
    if not expected_head or local_head != expected_head:
        failures.append("integration_local_head_mismatch")
    if failures:
        return {"schemaVersion": 1, "pushed": False, "unchanged": False, "failures": sorted(set(failures)), "result": "VETO"}
    remote_head = _remote_head(repo, remote, branch)
    if remote_head == local_head:
        return {"schemaVersion": 1, "remote": remote, "branch": branch, "head_sha": local_head, "pushed": False, "unchanged": True, "failures": [], "result": "PASS"}
    if remote_head:
        fetch = _git(repo, "fetch", "-q", remote, f"refs/heads/{branch}:refs/remotes/{remote}/{branch}")
        if fetch.returncode != 0:
            return {"schemaVersion": 1, "pushed": False, "unchanged": False, "failures": ["integration_remote_fetch_failed"], "result": "VETO"}
        fetched = _git_text(repo, "rev-parse", f"refs/remotes/{remote}/{branch}") or ""
        if fetched != remote_head or not _is_ancestor(repo, remote_head, local_head or ""):
            return {"schemaVersion": 1, "pushed": False, "unchanged": False, "remote_head": remote_head, "local_head": local_head, "failures": ["integration_remote_not_fast_forward"], "result": "VETO"}
    push = _git(repo, "push", remote, f"refs/heads/{branch}:refs/heads/{branch}")
    if push.returncode != 0:
        return {"schemaVersion": 1, "pushed": False, "unchanged": False, "failures": [f"integration_push_failed:{push.stderr.strip()}"], "result": "VETO"}
    readback = _remote_head(repo, remote, branch)
    if readback != local_head:
        return {"schemaVersion": 1, "pushed": False, "unchanged": False, "remote_head": readback, "local_head": local_head, "failures": ["integration_remote_readback_mismatch"], "result": "VETO"}
    return {"schemaVersion": 1, "remote": remote, "branch": branch, "head_sha": local_head, "pushed": True, "unchanged": False, "failures": [], "result": "PASS"}


def _write_json(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _commit_one(repo: pathlib.Path, relative: str, message: str) -> str | None:
    add = _git(repo, "add", "--", relative)
    if add.returncode != 0:
        return None
    commit = _git(repo, "-c", "user.name=Agent Control Plane", "-c", "user.email=agent-control-plane@local.invalid", "commit", "-m", message)
    return _git_text(repo, "rev-parse", "HEAD") if commit.returncode == 0 else None

def integrate_run(preparation: dict, workflow: dict) -> dict[str, object]:
    failures: list[str] = []
    if preparation.get("result") != "PASS":
        failures.append("preparation_not_pass")
    if workflow.get("result") != "PASS":
        failures.append("workflow_not_pass")
    if (workflow.get("adjudication") or {}).get("result") != "PASS":
        failures.append("workflow_adjudication_not_pass")
    if (workflow.get("base_freshness") or {}).get("result") != "PASS":
        failures.append("workflow_base_freshness_not_pass")
    repo = pathlib.Path(str(preparation.get("source_repo", "")))
    if not repo.is_dir():
        failures.append("source_repo_unavailable")
    current_freshness = verify_freshness(str(preparation.get("base_sha", "")), _current_base(preparation)) if repo.is_dir() else {"result": "NOT_RUN"}
    if current_freshness.get("result") != "PASS":
        failures.append("current_base_not_fresh")
    integration_branch = str(preparation.get("integration_branch", ""))
    integration_head = _git_text(repo, "rev-parse", "--verify", f"refs/heads/{integration_branch}") if repo.is_dir() else None
    if integration_head != preparation.get("base_sha"):
        failures.append("integration_branch_not_at_pinned_base")
    if failures:
        return {"schemaVersion": 1, "failures": sorted(set(failures)), "result": "VETO"}

    assignments = _assignment_map(preparation)
    finalizations = workflow.get("finalizations") or {}
    for actor in EXPECTED_ACTORS:
        assignment = assignments.get(actor) or {}
        finalization = finalizations.get(actor) or {}
        branch = str(assignment.get("branch", ""))
        local_head = _git_text(repo, "rev-parse", "--verify", f"refs/heads/{branch}") or ""
        if local_head != str(finalization.get("final_head_sha", "")):
            failures.append(f"actor_final_head_mismatch:{actor}")
    if failures:
        return {"schemaVersion": 1, "failures": sorted(set(failures)), "result": "VETO"}

    workspace_root = pathlib.Path(str(preparation.get("workspace_root", "")))
    integration_workspace = workspace_root / "_integration"
    if integration_workspace.exists():
        return {"schemaVersion": 1, "failures": ["integration_workspace_exists"], "result": "VETO"}
    add = _git(repo, "worktree", "add", "-q", str(integration_workspace), integration_branch)
    if add.returncode != 0:
        return {"schemaVersion": 1, "failures": [f"integration_worktree_create_failed:{add.stderr.strip()}"], "result": "FAIL"}
    merged_actor_heads: dict[str, str] = {}
    for actor in EXPECTED_ACTORS:
        branch = str(assignments[actor]["branch"])
        merge = _git(
            integration_workspace,
            "-c", "user.name=Agent Control Plane",
            "-c", "user.email=agent-control-plane@local.invalid",
            "merge", "--no-ff", "--no-edit", branch,
        )
        if merge.returncode != 0:
            _git(integration_workspace, "merge", "--abort")
            return {
                "schemaVersion": 1,
                "integration_workspace": str(integration_workspace),
                "merged_actor_heads": merged_actor_heads,
                "failures": [f"integration_merge_failed:{actor}:{merge.stderr.strip()}"],
                "result": "VETO",
            }
        merged_actor_heads[actor] = str(finalizations[actor]["final_head_sha"])

    issue = int(preparation["issue_number"])
    run_id = str(preparation["run_id"])
    receipt_dir = integration_workspace / f"ai-system/control-plane/runs/{issue}/{run_id}/receipts"
    integration_adjudication = adjudicate(receipt_dir, issue, run_id)
    if integration_adjudication.get("result") != "PASS":
        return {
            "schemaVersion": 1,
            "integration_workspace": str(integration_workspace),
            "merged_actor_heads": merged_actor_heads,
            "adjudication": integration_adjudication,
            "failures": ["integration_adjudication_not_pass"],
            "result": "VETO",
        }

    pre_evidence_head = _git_text(integration_workspace, "rev-parse", "HEAD") or ""
    changed = (_git_text(integration_workspace, "diff", "--name-only", str(preparation["base_sha"]), pre_evidence_head) or "").splitlines()
    run_prefix = f"ai-system/control-plane/runs/{issue}/{run_id}/"
    actual_task_paths = sorted(path for path in changed if not path.startswith(run_prefix))
    expected_task_paths = sorted(
        (finalizations.get("A07") or {}).get("snapshot_verification", {}).get("task_changed_paths", []) or []
    )
    if actual_task_paths != expected_task_paths:
        return {
            "schemaVersion": 1,
            "integration_workspace": str(integration_workspace),
            "merged_actor_heads": merged_actor_heads,
            "actual_task_paths": actual_task_paths,
            "expected_task_paths": expected_task_paths,
            "failures": ["integration_task_diff_mismatch"],
            "result": "VETO",
        }
    integration_rel = f"ai-system/control-plane/runs/{issue}/{run_id}/integration.json"
    integration_payload = {
        "schema_version": 1,
        "issue_number": issue,
        "run_id": run_id,
        "base_sha": preparation["base_sha"],
        "integration_branch": integration_branch,
        "head_sha": pre_evidence_head,
        "merged_actor_heads": merged_actor_heads,
        "task_changed_paths": actual_task_paths,
        "adjudication_result": integration_adjudication["result"],
        "base_freshness_result": current_freshness["result"],
        "remote_push_performed": False,
    }
    _write_json(integration_workspace / integration_rel, integration_payload)
    final_head = _commit_one(integration_workspace, integration_rel, "chore(run): record integration receipt")
    if not final_head:
        return {"schemaVersion": 1, "failures": ["integration_receipt_commit_failed"], "result": "FAIL"}
    final_diff = (_git_text(integration_workspace, "diff", "--name-only", pre_evidence_head, final_head) or "").splitlines()
    if final_diff != [integration_rel]:
        return {"schemaVersion": 1, "failures": ["integration_receipt_commit_not_isolated"], "result": "VETO"}
    final_freshness = verify_freshness(str(preparation.get("base_sha", "")), _current_base(preparation))
    if final_freshness.get("result") != "PASS":
        return {
            "schemaVersion": 1,
            "integration_workspace": str(integration_workspace),
            "integration_head_sha": final_head,
            "base_freshness": final_freshness,
            "failures": ["base_drift_during_integration"],
            "result": "VETO",
        }
    return {
        "schemaVersion": 1,
        "integration_workspace": str(integration_workspace),
        "integration_branch": integration_branch,
        "integration_head_sha": final_head,
        "integration_receipt_path": integration_rel,
        "merged_actor_heads": merged_actor_heads,
        "task_changed_paths": actual_task_paths,
        "adjudication": integration_adjudication,
        "base_freshness": final_freshness,
        "failures": [],
        "result": "PASS",
    }


def _show_text(repo: pathlib.Path, ref: str, relative: str) -> str | None:
    cp = _git(repo, "show", f"{ref}:{relative}")
    return cp.stdout if cp.returncode == 0 else None


def _path_history(repo: pathlib.Path, branch: str, relative: str) -> list[str]:
    cp = _git(repo, "log", "--format=%H", branch, "--", relative)
    if cp.returncode != 0:
        return []
    return [line.strip() for line in cp.stdout.splitlines() if line.strip()]


def _ensure_local_branch_from_remote(
    repo: pathlib.Path, branch: str, remote: str
) -> tuple[str | None, str | None]:
    local = _git_text(repo, "rev-parse", "--verify", f"refs/heads/{branch}")
    remote_head = _remote_head(repo, remote, branch)
    if local and remote_head and local != remote_head:
        return None, "local_remote_branch_mismatch"
    if local:
        return local, None
    if not remote_head:
        return None, "branch_missing_local_and_remote"
    fetch = _git(repo, "fetch", "-q", remote, f"refs/heads/{branch}:refs/remotes/{remote}/{branch}")
    if fetch.returncode != 0:
        return None, "remote_fetch_failed"
    fetched = _git_text(repo, "rev-parse", f"refs/remotes/{remote}/{branch}")
    if fetched != remote_head:
        return None, "remote_fetch_readback_mismatch"
    create = _git(repo, "branch", branch, fetched or "")
    if create.returncode != 0:
        return None, "local_branch_create_failed"
    return _git_text(repo, "rev-parse", f"refs/heads/{branch}"), None


def recover_run(
    source_repo: pathlib.Path | str,
    issue_number: int,
    run_id: str,
    base_ref: str,
    workspace_root: pathlib.Path | str,
    *,
    remote: str = "origin",
) -> dict[str, object]:
    repo = pathlib.Path(source_repo).resolve()
    workspace_root = pathlib.Path(workspace_root).resolve()
    failures: list[str] = []
    if issue_number < 1:
        failures.append("invalid_issue_number")
    if not run_id or "/" in run_id or ".." in run_id:
        failures.append("invalid_run_id")
    if not repo.is_dir() or _git_text(repo, "rev-parse", "HEAD") is None:
        failures.append("source_repo_unavailable")
    if repo.is_dir() and _git_text(repo, "status", "--porcelain"):
        failures.append("source_repo_dirty")
    try:
        workspace_root.relative_to(repo)
        failures.append("workspace_root_inside_source_repo")
    except ValueError:
        pass
    if workspace_root.exists() and any(workspace_root.iterdir()):
        failures.append("workspace_root_not_empty")
    registry_path = repo / "ai-system/control-plane/registry.json"
    if not registry_path.is_file():
        failures.append("registry_missing")
        registry = {}
    else:
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
        except Exception:
            registry = {}
            failures.append("registry_invalid_json")
    if failures:
        return {"schemaVersion": 1, "failures": sorted(set(failures)), "result": "VETO"}

    namespace = registry.get("namespace") or {}
    agent_template = str(namespace.get("agent_branch_template", ""))
    integration_template = str(namespace.get("integration_branch_template", ""))
    if not agent_template or not integration_template:
        return {"schemaVersion": 1, "failures": ["namespace_templates_missing"], "result": "VETO"}
    role_files = {str(row.get("id")): str(row.get("role_file", "")) for row in registry.get("agents", [])}
    plans: list[dict] = []
    snapshots: dict[str, dict] = {}
    recovered_rows: list[dict] = []
    actor_heads: dict[str, str] = {}
    base_shas: set[str] = set()

    for actor in EXPECTED_ACTORS:
        branch = agent_template.format(issue_number=issue_number, agent_id=actor, run_id=run_id)
        branch_head, error = _ensure_local_branch_from_remote(repo, branch, remote)
        if error or not branch_head:
            failures.append(f"actor_branch_recovery:{actor}:{error}")
            continue
        actor_heads[actor] = branch_head
        plan_path = f"ai-system/control-plane/runs/{issue_number}/{run_id}/plans/{actor}.json"
        claim_path = f"ai-system/control-plane/runs/{issue_number}/{run_id}/claims/{actor}.json"
        plan_history = _path_history(repo, branch, plan_path)
        claim_history = _path_history(repo, branch, claim_path)
        if not plan_history:
            failures.append(f"plan_commit_not_found:{actor}")
            continue
        if len(plan_history) != 1:
            failures.append(f"plan_history_not_immutable:{actor}")
            continue
        if not claim_history:
            failures.append(f"claim_commit_not_found:{actor}")
            continue
        if len(claim_history) != 1:
            failures.append(f"claim_history_not_immutable:{actor}")
            continue
        plan_head = plan_history[0]
        claim_head = claim_history[0]
        if not _is_ancestor(repo, claim_head, plan_head):
            failures.append(f"claim_commit_not_ancestor_of_plan:{actor}")
            continue
        plan_text = _show_text(repo, plan_head, plan_path)
        claim_text = _show_text(repo, plan_head, claim_path)
        if plan_text is None or claim_text is None:
            failures.append(f"plan_or_claim_missing_at_plan_head:{actor}")
            continue
        try:
            plan = json.loads(plan_text)
            claim = json.loads(claim_text)
        except Exception:
            failures.append(f"plan_or_claim_invalid_json:{actor}")
            continue
        checks = {
            "plan_actor": plan.get("actor_id") == actor,
            "claim_actor": claim.get("actor_id") == actor,
            "plan_issue": plan.get("issue_number") == issue_number,
            "claim_issue": claim.get("issue_number") == issue_number,
            "plan_run": plan.get("run_id") == run_id,
            "claim_run": claim.get("run_id") == run_id,
            "plan_branch": plan.get("branch") == branch,
            "claim_branch": claim.get("branch") == branch,
            "claim_status": claim.get("status") == "CLAIMED",
            "same_base": claim.get("base_sha") == plan.get("base_sha"),
        }
        for label, ok in checks.items():
            if not ok:
                failures.append(f"recovered_identity_mismatch:{actor}:{label}")
        for field in ["claim_id", "executor_id", "execution_id"]:
            if not str(claim.get(field, "")).strip():
                failures.append(f"recovered_claim_missing_{field}:{actor}")
        base_shas.add(str(plan.get("base_sha", "")))
        plans.append(plan)
        snapshots[actor] = {
            "branch": branch,
            "plan_head_sha": plan_head,
            "plan_sha256": hashlib.sha256(plan_text.encode("utf-8")).hexdigest(),
            "claim_sha256": hashlib.sha256(claim_text.encode("utf-8")).hexdigest(),
            "claim_id": claim.get("claim_id"),
            "executor_id": claim.get("executor_id"),
            "execution_id": claim.get("execution_id"),
        }
        recovered_rows.append({
            "issue_number": issue_number,
            "run_id": run_id,
            "actor_id": actor,
            "branch": branch,
            "workspace": str(workspace_root / actor),
            "claim_id": claim.get("claim_id"),
            "executor_id": claim.get("executor_id"),
            "execution_id": claim.get("execution_id"),
            "plan_head_sha": plan_head,
            "depends_on": list(plan.get("depends_on") or []),
            "role_file": role_files.get(actor, ""),
        })

    if set(actor_heads) != set(EXPECTED_ACTORS):
        failures.append("actor_branch_set_incomplete")
    if len(base_shas) != 1 or "" in base_shas:
        failures.append("recovered_base_sha_mismatch")
    preflight = evaluate_plans(plans) if len(plans) == 10 else {"result": "NOT_RUN"}
    if preflight.get("result") != "PASS":
        failures.append("recovered_plan_preflight_not_pass")
    base_sha = next(iter(base_shas), "")
    current_base = _git_text(repo, "rev-parse", "--verify", f"{base_ref}^{{commit}}") or ""
    freshness = verify_freshness(base_sha, current_base) if base_sha else {"result": "NOT_RUN"}
    if freshness.get("result") != "PASS":
        failures.append("recovered_base_not_fresh")
    if failures:
        return {
            "schemaVersion": 1, "issue_number": issue_number, "run_id": run_id,
            "snapshots": snapshots, "preflight": preflight,
            "base_freshness": freshness, "failures": sorted(set(failures)), "result": "VETO",
        }

    integration_branch = integration_template.format(issue_number=issue_number, run_id=run_id)
    integration_local = _git_text(repo, "rev-parse", "--verify", f"refs/heads/{integration_branch}")
    integration_remote = _remote_head(repo, remote, integration_branch)
    if integration_local and integration_remote and integration_local != integration_remote:
        return {"schemaVersion": 1, "failures": ["integration_local_remote_mismatch"], "result": "VETO"}
    if not integration_local and integration_remote:
        recovered, error = _ensure_local_branch_from_remote(repo, integration_branch, remote)
        if error or not recovered:
            return {"schemaVersion": 1, "failures": [f"integration_branch_recovery:{error}"], "result": "VETO"}
    elif not integration_local:
        create = _git(repo, "branch", integration_branch, base_sha)
        if create.returncode != 0:
            return {"schemaVersion": 1, "failures": ["integration_branch_create_failed"], "result": "FAIL"}

    workspace_root.mkdir(parents=True, exist_ok=True)
    coordination = workspace_root / "_coordination"
    coordination.mkdir(parents=True, exist_ok=True)
    for row in recovered_rows:
        workspace = pathlib.Path(str(row["workspace"]))
        add = _git(repo, "worktree", "add", "-q", str(workspace), str(row["branch"]))
        if add.returncode != 0:
            return {
                "schemaVersion": 1, "restored_actors": [x["actor_id"] for x in recovered_rows if pathlib.Path(str(x["workspace"])).is_dir()],
                "failures": [f"recovered_worktree_create_failed:{row['actor_id']}:{add.stderr.strip()}"],
                "result": "FAIL",
            }
    preparation = {
        "schemaVersion": 1,
        "source_repo": str(repo),
        "issue_number": issue_number,
        "run_id": run_id,
        "base_sha": base_sha,
        "base_ref": base_ref,
        "workspace_root": str(workspace_root),
        "coordination_dir": str(coordination),
        "integration_branch": integration_branch,
        "assignments": sorted(recovered_rows, key=lambda row: row["actor_id"]),
        "snapshots": snapshots,
        "collector": {"schemaVersion": 2, "collected": EXPECTED_ACTORS, "snapshots": snapshots, "errors": [], "result": "PASS"},
        "preflight": preflight,
        "base_freshness": freshness,
        "recovered_from_git": True,
        "remote": remote,
        "failures": [],
        "result": "PASS",
    }
    _write_json(coordination / "run-preparation.json", preparation)
    return preparation


def rehydrate_run(preparation: dict) -> dict[str, object]:
    repo = pathlib.Path(str(preparation.get("source_repo", "")))
    assignments = _assignment_map(preparation)
    failures: list[str] = []
    if preparation.get("result") != "PASS":
        failures.append("preparation_not_pass")
    if not repo.is_dir() or _git_text(repo, "rev-parse", "HEAD") is None:
        failures.append("source_repo_unavailable")
    if set(assignments) != set(EXPECTED_ACTORS):
        failures.append("assignment_actor_set_mismatch")
    existing: list[str] = []
    missing: list[str] = []
    for actor in EXPECTED_ACTORS:
        row = assignments.get(actor, {})
        branch = str(row.get("branch", ""))
        workspace = pathlib.Path(str(row.get("workspace", "")))
        if not branch or _git_text(repo, "rev-parse", "--verify", f"refs/heads/{branch}") is None:
            failures.append(f"local_branch_missing:{actor}")
            continue
        if workspace.exists():
            if not workspace.is_dir() or _git_text(workspace, "rev-parse", "HEAD") is None:
                failures.append(f"workspace_path_collision:{actor}")
                continue
            if _git_text(workspace, "branch", "--show-current") != branch:
                failures.append(f"workspace_branch_mismatch:{actor}")
                continue
            existing.append(actor)
        else:
            missing.append(actor)
    if failures:
        return {
            "schemaVersion": 1, "existing_actors": existing, "restored_actors": [],
            "failures": sorted(set(failures)), "result": "VETO",
        }
    restored: list[str] = []
    for actor in missing:
        row = assignments[actor]
        workspace = pathlib.Path(str(row["workspace"]))
        workspace.parent.mkdir(parents=True, exist_ok=True)
        add = _git(repo, "worktree", "add", "-q", str(workspace), str(row["branch"]))
        if add.returncode != 0:
            return {
                "schemaVersion": 1, "existing_actors": existing,
                "restored_actors": restored,
                "failures": [f"worktree_restore_failed:{actor}:{add.stderr.strip()}"],
                "partial_restore_preserved": bool(restored), "result": "FAIL",
            }
        if _git_text(workspace, "branch", "--show-current") != str(row["branch"]):
            return {
                "schemaVersion": 1, "existing_actors": existing,
                "restored_actors": restored,
                "failures": [f"restored_branch_mismatch:{actor}"],
                "partial_restore_preserved": True, "result": "FAIL",
            }
        restored.append(actor)
    return {
        "schemaVersion": 1, "existing_actors": existing,
        "restored_actors": restored, "branches_preserved": True,
        "remote_mutation_performed": False, "failures": [], "result": "PASS",
    }


def cleanup_run(preparation: dict, *, force: bool = False) -> dict[str, object]:
    repo = pathlib.Path(str(preparation.get("source_repo", "")))
    assignments = _assignment_map(preparation)
    dirty_actors: list[str] = []
    targets: list[tuple[str, pathlib.Path]] = []
    for actor in EXPECTED_ACTORS:
        workspace = pathlib.Path(str((assignments.get(actor) or {}).get("workspace", "")))
        if workspace.is_dir():
            targets.append((actor, workspace))
            status = _git_text(workspace, "status", "--porcelain")
            if status:
                dirty_actors.append(actor)
    integration_workspace = pathlib.Path(str(preparation.get("workspace_root", ""))) / "_integration"
    if integration_workspace.is_dir():
        targets.append(("integration", integration_workspace))
        status = _git_text(integration_workspace, "status", "--porcelain")
        if status:
            dirty_actors.append("integration")
    if dirty_actors and not force:
        return {
            "schemaVersion": 1,
            "dirty_actors": sorted(dirty_actors),
            "removed_worktrees": [],
            "failures": ["dirty_worktree_present"],
            "result": "VETO",
        }
    removed: list[str] = []
    failures: list[str] = []
    for label, workspace in targets:
        args = ["worktree", "remove"]
        if force:
            args.append("--force")
        args.append(str(workspace))
        cp = _git(repo, *args)
        if cp.returncode != 0:
            failures.append(f"worktree_remove_failed:{label}:{cp.stderr.strip()}")
        else:
            removed.append(label)
    _git(repo, "worktree", "prune")
    return {
        "schemaVersion": 1,
        "dirty_actors": sorted(dirty_actors),
        "removed_worktrees": removed,
        "branches_preserved": True,
        "remote_branches_deleted": False,
        "coordination_preserved": True,
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }


def _load(path: str) -> dict:
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    status_p = sub.add_parser("status")
    status_p.add_argument("--preparation-json", required=True)
    status_p.add_argument("--workflow-json")
    status_p.add_argument("--remote", default="origin")
    pub_p = sub.add_parser("publish")
    pub_p.add_argument("--preparation-json", required=True)
    pub_p.add_argument("--workflow-json")
    pub_p.add_argument("--remote", default="origin")
    int_p = sub.add_parser("integrate")
    int_p.add_argument("--preparation-json", required=True)
    int_p.add_argument("--workflow-json", required=True)
    pub_int_p = sub.add_parser("publish-integration")
    pub_int_p.add_argument("--preparation-json", required=True)
    pub_int_p.add_argument("--integration-json", required=True)
    pub_int_p.add_argument("--remote", default="origin")
    recover_p = sub.add_parser("recover")
    recover_p.add_argument("--source-repo", required=True)
    recover_p.add_argument("--issue", type=int, required=True)
    recover_p.add_argument("--run-id", required=True)
    recover_p.add_argument("--base-ref", default="main")
    recover_p.add_argument("--workspace-root", required=True)
    recover_p.add_argument("--remote", default="origin")
    rehydrate_p = sub.add_parser("rehydrate")
    rehydrate_p.add_argument("--preparation-json", required=True)
    resume_p = sub.add_parser("resume")
    resume_p.add_argument("--preparation-json", required=True)
    resume_p.add_argument("--claude-path", default="")
    resume_p.add_argument("--output-dir", required=True)
    resume_p.add_argument("--max-parallel", type=int, default=3)
    resume_p.add_argument("--timeout-seconds", type=float, default=180.0)
    resume_p.add_argument("--max-budget-usd", type=float, default=0.05)
    resume_p.add_argument("--model")
    clean_p = sub.add_parser("cleanup")
    clean_p.add_argument("--preparation-json", required=True)
    clean_p.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "recover":
        result = recover_run(args.source_repo, args.issue, args.run_id, args.base_ref, args.workspace_root, remote=args.remote)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["result"] == "PASS" else 1

    preparation = _load(args.preparation_json)
    if args.command == "resume":
        result = run_workflow(
            preparation,
            args.claude_path,
            args.output_dir,
            max_parallel=args.max_parallel,
            timeout_seconds=args.timeout_seconds,
            max_budget_usd=args.max_budget_usd,
            model=args.model,
            resume_existing=True,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["result"] == "PASS" else 1
    if args.command == "status":
        workflow = _load(args.workflow_json) if args.workflow_json else None
        result = inspect_run(preparation, workflow, remote=args.remote)
    elif args.command == "publish":
        workflow = _load(args.workflow_json) if args.workflow_json else None
        result = publish_run(preparation, workflow, remote=args.remote)
    elif args.command == "integrate":
        result = integrate_run(preparation, _load(args.workflow_json))
    elif args.command == "publish-integration":
        result = publish_integration(preparation, _load(args.integration_json), remote=args.remote)
    elif args.command == "rehydrate":
        result = rehydrate_run(preparation)
    else:
        result = cleanup_run(preparation, force=args.force)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
