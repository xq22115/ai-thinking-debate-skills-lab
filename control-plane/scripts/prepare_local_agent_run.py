#!/usr/bin/env python3
"""Prepare ten claim-bound local agent worktrees without launching a model."""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import uuid

try:
    from scripts.check_write_plan_conflicts import evaluate_plans
    from scripts.collect_write_plans_from_refs import collect_plans
except ModuleNotFoundError:
    from check_write_plan_conflicts import evaluate_plans
    from collect_write_plans_from_refs import collect_plans

EXPECTED_ACTORS = [f"A{i:02d}" for i in range(1, 11)]
DEFAULT_DEPENDENCIES = {
    "A01": [],
    "A02": ["A01"],
    "A03": ["A01"],
    "A04": ["A01"],
    "A05": ["A01", "A02", "A04"],
    "A06": ["A01", "A05"],
    "A07": ["A01", "A02", "A03", "A04", "A05", "A06"],
    "A08": ["A01", "A07"],
    "A09": ["A01", "A07", "A08"],
    "A10": ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09"],
}


def _git(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def _git_text(repo: pathlib.Path, *args: str) -> str | None:
    cp = _git(repo, *args)
    return cp.stdout.strip() if cp.returncode == 0 else None


def _resolve_commit(repo: pathlib.Path, revision: str) -> str | None:
    return _git_text(repo, "rev-parse", "--verify", f"{revision}^{{commit}}")


def _branch_exists(repo: pathlib.Path, branch: str) -> bool:
    return _git(repo, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}").returncode == 0


def _show_json(repo: pathlib.Path, revision: str, path: str) -> dict | None:
    text = _git_text(repo, "show", f"{revision}:{path}")
    if text is None:
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _default_id(kind: str, actor: str) -> str:
    return f"{kind}-{actor}-{uuid.uuid4().hex}"


def _write_json(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _commit_file(workspace: pathlib.Path, relative: str, message: str) -> str | None:
    add = _git(workspace, "add", "--", relative)
    if add.returncode != 0:
        return None
    commit = _git(
        workspace,
        "-c", "user.name=Agent Control Plane",
        "-c", "user.email=agent-control-plane@local.invalid",
        "commit", "-m", message,
    )
    if commit.returncode != 0:
        return None
    return _git_text(workspace, "rev-parse", "HEAD")


def _inside_repo(repo: pathlib.Path, candidate: pathlib.Path) -> bool:
    try:
        candidate.resolve().relative_to(repo.resolve())
        return True
    except ValueError:
        return False


def _normalize_config(plan_config: dict | None) -> tuple[dict[str, dict], list[str]]:
    plan_config = plan_config or {}
    failures: list[str] = []
    if not isinstance(plan_config, dict):
        return {}, ["plan_config_not_object"]
    unknown_actors = sorted(set(plan_config) - set(EXPECTED_ACTORS))
    for actor in unknown_actors:
        failures.append(f"unknown_plan_actor:{actor}")
    normalized: dict[str, dict] = {}
    allowed_keys = {"read_set", "write_set", "prompt_suffix"}
    for actor in EXPECTED_ACTORS:
        raw = plan_config.get(actor) or {}
        if not isinstance(raw, dict):
            failures.append(f"plan_config_not_object:{actor}")
            raw = {}
        unknown_keys = sorted(set(raw) - allowed_keys)
        for key in unknown_keys:
            failures.append(f"unknown_plan_config_key:{actor}:{key}")
        read_set = raw.get("read_set", ["**"])
        write_set = raw.get("write_set", [])
        prompt_suffix = raw.get("prompt_suffix", "")
        if not isinstance(read_set, list) or not all(isinstance(x, str) and x for x in read_set):
            failures.append(f"invalid_read_set:{actor}")
            read_set = []
        if not isinstance(write_set, list) or not all(isinstance(x, str) and x for x in write_set):
            failures.append(f"invalid_write_set:{actor}")
            write_set = []
        if actor != "A07" and write_set:
            failures.append(f"readonly_write_set_nonempty:{actor}")
        if not isinstance(prompt_suffix, str):
            failures.append(f"invalid_prompt_suffix:{actor}")
            prompt_suffix = ""
        normalized[actor] = {
            "read_set": read_set,
            "write_set": write_set,
            "prompt_suffix": prompt_suffix,
        }
    return normalized, failures


def prepare_run(
    repo: pathlib.Path,
    issue_number: int,
    run_id: str,
    base_sha: str,
    base_ref: str,
    workspace_root: pathlib.Path,
    *,
    plan_config: dict | None = None,
    id_factory=None,
) -> dict[str, object]:
    repo = pathlib.Path(repo)
    workspace_root = pathlib.Path(workspace_root)
    id_factory = id_factory or _default_id
    failures: list[str] = []

    if not repo.is_dir() or _resolve_commit(repo, "HEAD") is None:
        failures.append("repository_not_git_worktree")
    if not isinstance(issue_number, int) or issue_number < 1:
        failures.append("invalid_issue_number")
    if not run_id or "/" in run_id or ".." in run_id:
        failures.append("invalid_run_id")
    if len(base_sha) != 40 or any(ch not in "0123456789abcdef" for ch in base_sha):
        failures.append("invalid_base_sha")
    if workspace_root.exists() and any(workspace_root.iterdir()):
        failures.append("workspace_root_not_empty")
    if _inside_repo(repo, workspace_root):
        failures.append("workspace_root_inside_source_repo")

    status = _git_text(repo, "status", "--porcelain")
    if status is None:
        failures.append("source_status_failed")
    elif status:
        failures.append("source_worktree_dirty")

    resolved_base = _resolve_commit(repo, base_ref)
    if resolved_base is None:
        failures.append("base_ref_unresolvable")
    elif resolved_base != base_sha:
        failures.append("base_ref_mismatch")
    if _resolve_commit(repo, base_sha) != base_sha:
        failures.append("base_sha_unresolvable")

    registry = _show_json(
        repo, base_sha, "ai-system/control-plane/registry.json"
    ) if len(base_sha) == 40 else None
    if not registry:
        failures.append("base_registry_missing_or_invalid")
        agents: list[dict] = []
    else:
        agents = registry.get("agents") or []
        ids = [str(row.get("id", "")) for row in agents]
        if ids != EXPECTED_ACTORS:
            failures.append("registry_actor_set_mismatch")
        for row in agents:
            role_file = str(row.get("role_file", ""))
            if not role_file or _git_text(repo, "cat-file", "-e", f"{base_sha}:{role_file}") is None:
                failures.append(f"role_file_missing:{row.get('id')}:{role_file}")

    config, config_failures = _normalize_config(plan_config)
    failures.extend(config_failures)
    branches = {
        actor: f"agent/{issue_number}/{actor}/{run_id}"
        for actor in EXPECTED_ACTORS
    }
    integration_branch = f"task/{issue_number}/{run_id}/integration"
    for branch in [*branches.values(), integration_branch]:
        if _branch_exists(repo, branch):
            failures.append(f"branch_already_exists:{branch}")

    identities: dict[str, dict[str, str]] = {}
    for actor in EXPECTED_ACTORS:
        identities[actor] = {
            "claim_id": str(id_factory("claim", actor)),
            "executor_id": str(id_factory("executor", actor)),
            "execution_id": str(id_factory("execution", actor)),
        }
        for field, value in identities[actor].items():
            if not value:
                failures.append(f"empty_identity:{actor}:{field}")
    for field in ["claim_id", "executor_id", "execution_id"]:
        values = [identities[a][field] for a in EXPECTED_ACTORS]
        if len(set(values)) != len(values):
            failures.append(f"duplicate_{field}")

    role_map = {str(row.get("id")): row for row in agents}
    prospective_plans: list[dict] = []
    for actor in EXPECTED_ACTORS:
        cfg = config.get(actor, {"read_set": [], "write_set": [], "prompt_suffix": ""})
        prospective_plans.append({
            "schema_version": 1,
            "issue_number": issue_number,
            "run_id": run_id,
            "actor_id": actor,
            "branch": branches[actor],
            "base_sha": base_sha,
            "read_set": cfg["read_set"],
            "write_set": cfg["write_set"],
            "depends_on": DEFAULT_DEPENDENCIES[actor],
            "status": "PROPOSED",
        })
    if not failures:
        prospective = evaluate_plans(prospective_plans)
        if prospective.get("result") != "PASS":
            failures.append("prospective_preflight_veto")
            failures.extend(str(x) for x in prospective.get("failures", []))
            if prospective.get("unresolved_conflicts"):
                failures.append("prospective_write_conflict")
    else:
        prospective = {"result": "NOT_RUN"}

    if failures:
        return {
            "schemaVersion": 1,
            "issue_number": issue_number,
            "run_id": run_id,
            "failures": sorted(set(failures)),
            "prospective_preflight": prospective,
            "result": "VETO",
        }

    workspace_root.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    plan_heads: dict[str, str] = {}
    workspaces: dict[str, pathlib.Path] = {}

    for actor in EXPECTED_ACTORS:
        workspace = workspace_root / actor
        branch = branches[actor]
        add = _git(
            repo, "worktree", "add", "-q", "-b", branch,
            str(workspace), base_sha,
        )
        if add.returncode != 0:
            return {
                "schemaVersion": 1,
                "issue_number": issue_number,
                "run_id": run_id,
                "created_actors": created,
                "failures": [f"worktree_create_failed:{actor}:{add.stderr.strip()}"],
                "partial_preparation_preserved": bool(created),
                "result": "FAIL",
            }
        workspaces[actor] = workspace
        created.append(actor)
        claim_rel = (
            f"ai-system/control-plane/runs/{issue_number}/{run_id}/claims/"
            f"{actor}.json"
        )
        identity = identities[actor]
        claim = {
            "schema_version": 1,
            "issue_number": issue_number,
            "run_id": run_id,
            "actor_id": actor,
            "branch": branch,
            "base_sha": base_sha,
            "claim_id": identity["claim_id"],
            "executor_id": identity["executor_id"],
            "execution_id": identity["execution_id"],
            "status": "CLAIMED",
        }
        _write_json(workspace / claim_rel, claim)
        claim_head = _commit_file(workspace, claim_rel, f"chore(run): claim {actor}")
        if not claim_head:
            return {
                "schemaVersion": 1,
                "created_actors": created,
                "failures": [f"claim_commit_failed:{actor}"],
                "partial_preparation_preserved": True,
                "result": "FAIL",
            }
        cfg = config[actor]
        plan_rel = (
            f"ai-system/control-plane/runs/{issue_number}/{run_id}/plans/"
            f"{actor}.json"
        )
        plan = {
            "schema_version": 1,
            "issue_number": issue_number,
            "run_id": run_id,
            "actor_id": actor,
            "branch": branch,
            "base_sha": base_sha,
            "read_set": cfg["read_set"],
            "write_set": cfg["write_set"],
            "depends_on": DEFAULT_DEPENDENCIES[actor],
            "status": "PROPOSED",
        }
        _write_json(workspace / plan_rel, plan)
        plan_head = _commit_file(workspace, plan_rel, f"chore(run): plan {actor}")
        if not plan_head:
            return {
                "schemaVersion": 1,
                "created_actors": created,
                "failures": [f"plan_commit_failed:{actor}"],
                "partial_preparation_preserved": True,
                "result": "FAIL",
            }
        plan_heads[actor] = plan_head

    coordination = workspace_root / "_coordination"
    collected_dir = coordination / "plans"
    refs = {actor: branches[actor] for actor in EXPECTED_ACTORS}
    collection = collect_plans(
        repo, refs, issue_number, run_id, collected_dir
    )
    _write_json(coordination / "collection.json", collection)
    if collection.get("result") != "PASS":
        result = {
            "schemaVersion": 1,
            "issue_number": issue_number,
            "run_id": run_id,
            "created_actors": created,
            "collection": collection,
            "failures": ["committed_plan_collection_veto"],
            "partial_preparation_preserved": True,
            "result": "VETO",
        }
        _write_json(coordination / "run-preparation.json", result)
        return result

    committed_plans = [
        json.loads((collected_dir / f"{actor}.json").read_text(encoding="utf-8"))
        for actor in EXPECTED_ACTORS
    ]
    preflight = evaluate_plans(committed_plans)
    _write_json(coordination / "preflight.json", preflight)
    if preflight.get("result") != "PASS":
        result = {
            "schemaVersion": 1,
            "issue_number": issue_number,
            "run_id": run_id,
            "created_actors": created,
            "collection": collection,
            "preflight": preflight,
            "failures": ["committed_preflight_veto"],
            "partial_preparation_preserved": True,
            "result": "VETO",
        }
        _write_json(coordination / "run-preparation.json", result)
        return result

    create_integration = _git(repo, "branch", integration_branch, base_sha)
    if create_integration.returncode != 0:
        result = {
            "schemaVersion": 1,
            "created_actors": created,
            "collection": collection,
            "preflight": preflight,
            "failures": [f"integration_branch_create_failed:{create_integration.stderr.strip()}"],
            "partial_preparation_preserved": True,
            "result": "FAIL",
        }
        _write_json(coordination / "run-preparation.json", result)
        return result

    snapshots = collection.get("snapshots") or {}
    assignments: list[dict] = []
    for actor in EXPECTED_ACTORS:
        agent = role_map[actor]
        snapshot = snapshots[actor]
        cfg = config[actor]
        role_file = str(agent["role_file"])
        role_name = str(agent.get("name_zh", actor))
        dependencies = DEFAULT_DEPENDENCIES[actor]
        prompt = (
            f"You are {actor} — {role_name}. Read {role_file} and AGENTS.md. "
            f"This run is issue #{issue_number}, run_id={run_id}. "
            f"Your declared dependencies are {dependencies}. "
            "Stay within your role and return only the required structured decision."
        )
        if cfg["prompt_suffix"]:
            prompt += " " + cfg["prompt_suffix"]
        assignments.append({
            "issue_number": issue_number,
            "run_id": run_id,
            "actor_id": actor,
            "branch": branches[actor],
            "workspace": str(workspaces[actor].resolve()),
            "role_file": role_file,
            "claim_id": snapshot["claim_id"],
            "executor_id": snapshot["executor_id"],
            "execution_id": snapshot["execution_id"],
            "plan_head_sha": snapshot["plan_head_sha"],
            "depends_on": dependencies,
            "prompt": prompt,
        })

    result = {
        "schemaVersion": 1,
        "issue_number": issue_number,
        "run_id": run_id,
        "base_sha": base_sha,
        "base_ref": base_ref,
        "source_repo": str(repo.resolve()),
        "workspace_root": str(workspace_root.resolve()),
        "integration_branch": integration_branch,
        "dependencies": DEFAULT_DEPENDENCIES,
        "assignments": assignments,
        "snapshots": snapshots,
        "collection": collection,
        "preflight": preflight,
        "prospective_preflight": prospective,
        "remote_push_performed": False,
        "failures": [],
        "result": "PASS",
    }
    _write_json(coordination / "assignments.json", {"assignments": assignments})
    _write_json(coordination / "snapshots.json", snapshots)
    _write_json(coordination / "run-preparation.json", result)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--issue", type=int, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--base-ref", default="main")
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--plan-config")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    config = {}
    if args.plan_config:
        config = json.loads(pathlib.Path(args.plan_config).read_text(encoding="utf-8"))
    result = prepare_run(
        pathlib.Path(args.repo),
        args.issue,
        args.run_id,
        args.base_sha,
        args.base_ref,
        pathlib.Path(args.workspace_root),
        plan_config=config,
    )
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
