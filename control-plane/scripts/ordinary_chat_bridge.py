#!/usr/bin/env python3
"""Narrow ordinary-chat bridge for existing local agent runtimes.

This bridge deliberately does not expose a generic shell. It provides preflight,
queued launch, status, and receipt-summary operations for allowlisted workspaces.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import uuid
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREPARE = ROOT / "scripts" / "prepare_local_agent_run.py"
RUN_WORKFLOW = ROOT / "scripts" / "run_local_agent_workflow.py"
RUN_ID_RE = re.compile(r"^[0-9a-f]{32}$")


def _state_dir() -> pathlib.Path:
    raw = os.environ.get("ORDINARY_CHAT_STATE_DIR", "~/.ordinary-chat-agent")
    path = pathlib.Path(raw).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path


def _allowed_roots() -> list[pathlib.Path]:
    raw = os.environ.get("ORDINARY_CHAT_ALLOWED_ROOTS", "")
    roots: list[pathlib.Path] = []
    seen: set[pathlib.Path] = set()
    for item in raw.split(os.pathsep):
        if not item.strip():
            continue
        root = pathlib.Path(item).expanduser().resolve()
        if root not in seen:
            roots.append(root)
            seen.add(root)
    return roots


def _inside(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _inside_allowed(path: pathlib.Path, roots: list[pathlib.Path] | None = None) -> bool:
    resolved = path.expanduser().resolve()
    return any(_inside(resolved, root) for root in (roots if roots is not None else _allowed_roots()))


def _json_write(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.parent.chmod(0o700)
    except OSError:
        pass
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _json_read(path: pathlib.Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("json_root_not_object")
    return value


def _record_path(run_id: str) -> pathlib.Path:
    return _state_dir() / "runs" / run_id / "record.json"


def _update_record(run_id: str, **updates: Any) -> dict[str, Any]:
    path = _record_path(run_id)
    try:
        current: dict[str, Any] = _json_read(path) if path.is_file() else {"run_id": run_id}
    except (OSError, ValueError, json.JSONDecodeError):
        current = {"run_id": run_id, "failures": ["record_recovered_from_corruption"]}
    current.update(updates)
    current["updated_at_unix"] = int(time.time())
    _json_write(path, current)
    return current


def _command_path(env_name: str) -> pathlib.Path | None:
    raw = os.environ.get(env_name, "").strip()
    if not raw:
        return None
    return pathlib.Path(raw).expanduser().resolve()


def _executable(path: pathlib.Path | None) -> bool:
    return bool(path and path.is_file() and os.access(path, os.X_OK))


def _git_text(repo: pathlib.Path, *args: str) -> str | None:
    cp = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, check=False)
    return cp.stdout.strip() if cp.returncode == 0 else None


def _git_root(repo: pathlib.Path) -> pathlib.Path | None:
    text = _git_text(repo, "rev-parse", "--show-toplevel")
    if not text:
        return None
    path = pathlib.Path(text).expanduser().resolve()
    return path if path.is_dir() else None


def _valid_base_ref(value: str) -> bool:
    if not value or value.startswith("-") or value.endswith("/") or value.endswith("."):
        return False
    if ".." in value or "@{" in value or "//" in value:
        return False
    forbidden = set(" ~^:?*[\\\x00")
    return not any(ch in forbidden or ord(ch) < 32 or ord(ch) == 127 for ch in value)


def _resolve_commit(repo: pathlib.Path, revision: str) -> str | None:
    if not _valid_base_ref(revision):
        return None
    return _git_text(repo, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")


def _worktree_dirty(repo: pathlib.Path) -> bool | None:
    status = _git_text(repo, "status", "--porcelain")
    return None if status is None else bool(status)


def preflight(workspace: str | None = None, repo: str | None = None) -> dict[str, Any]:
    roots = _allowed_roots()
    chat_agent = _command_path("CHAT_WORK_AGENT_PATH")
    claude = _command_path("CLAUDE_PATH")
    workspace_path = pathlib.Path(workspace).expanduser().resolve() if workspace else None
    repo_path = pathlib.Path(repo).expanduser().resolve() if repo else None
    workspace_exists = workspace_path.is_dir() if workspace_path else None
    workspace_allowed = _inside_allowed(workspace_path, roots) if workspace_path else None
    repo_exists = repo_path.is_dir() if repo_path else None
    repo_allowed = _inside_allowed(repo_path, roots) if repo_path else None
    repo_root = _git_root(repo_path) if repo_path and repo_exists else None
    repo_root_allowed = _inside_allowed(repo_root, roots) if repo_root else None
    repo_dirty = _worktree_dirty(repo_root) if repo_root else None
    scripts_present = PREPARE.is_file() and RUN_WORKFLOW.is_file()

    failures: list[str] = []
    if not roots:
        failures.append("ORDINARY_CHAT_ALLOWED_ROOTS_not_configured")
    if workspace_path is not None:
        if not workspace_exists:
            failures.append("workspace_missing")
        elif not workspace_allowed:
            failures.append("workspace_not_allowlisted")
    if repo_path is not None:
        if not repo_exists:
            failures.append("repo_missing")
        elif not repo_allowed:
            failures.append("repo_not_allowlisted")
        elif repo_root is None:
            failures.append("repo_not_git")
        elif not repo_root_allowed:
            failures.append("repo_root_not_allowlisted")

    return {
        "schemaVersion": 1,
        "allowed_roots_configured": bool(roots),
        "allowed_root_count": len(roots),
        "workspace_exists": workspace_exists,
        "workspace_allowed": workspace_allowed,
        "repo_exists": repo_exists,
        "repo_allowed": repo_allowed,
        "repo_git_root": str(repo_root) if repo_root else None,
        "repo_root_allowed": repo_root_allowed,
        "repo_dirty": repo_dirty,
        "chat_work_agent_configured": chat_agent is not None,
        "chat_work_agent_executable": _executable(chat_agent),
        "claude_configured": claude is not None,
        "claude_executable": _executable(claude),
        "a01_a10_scripts_present": scripts_present,
        "chat_submit_ready": bool(roots and workspace_exists and workspace_allowed and _executable(chat_agent)),
        "a01_submit_ready": bool(roots and repo_root and repo_root_allowed and repo_dirty is False and _executable(claude) and scripts_present),
        "state_dir": str(_state_dir()),
        "failures": sorted(set(failures)),
        "result": "PASS" if not failures else "BLOCKED",
        "reason": failures[0] if failures else None,
    }


def _validate_write_set(items: list[str]) -> list[str]:
    failures: list[str] = []
    for raw in items:
        item = raw.strip()
        normalized = item.replace("\\", "/")
        parts = pathlib.PurePosixPath(normalized).parts if normalized else ()
        invalid = (
            not item
            or "\x00" in item
            or normalized.startswith("/")
            or normalized.startswith("//")
            or bool(re.match(r"^[A-Za-z]:", normalized))
            or ".." in parts
            or ".git" in parts
        )
        if invalid:
            failures.append(f"invalid_write_set:{raw}")
    return failures


def _queue(kind: str, spec: dict[str, Any]) -> dict[str, Any]:
    run_id = uuid.uuid4().hex
    run_dir = _state_dir() / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    try:
        run_dir.chmod(0o700)
    except OSError:
        pass
    spec = dict(spec)
    spec["run_id"] = run_id
    spec["kind"] = kind
    spec_path = run_dir / "spec.json"
    _json_write(spec_path, spec)
    record = {
        "schemaVersion": 1,
        "run_id": run_id,
        "kind": kind,
        "status": "QUEUED",
        "goal_sha256": hashlib.sha256(str(spec.get("goal", "")).encode("utf-8")).hexdigest(),
        "created_at_unix": int(time.time()),
        "updated_at_unix": int(time.time()),
    }
    _json_write(_record_path(run_id), record)
    try:
        with open(os.devnull, "wb") as sink:
            proc = subprocess.Popen(
                [sys.executable, str(pathlib.Path(__file__).resolve()), "_worker", "--spec", str(spec_path)],
                stdin=subprocess.DEVNULL,
                stdout=sink,
                stderr=sink,
                start_new_session=True,
            )
    except OSError as exc:
        try:
            spec_path.unlink()
        except OSError:
            pass
        return _update_record(run_id, status="FAIL", failures=[f"worker_spawn_failed:{type(exc).__name__}"], finished_at_unix=int(time.time()))
    return _update_record(run_id, worker_pid=proc.pid, spawned_at_unix=int(time.time()))


def submit_chat(workspace: str, goal: str) -> dict[str, Any]:
    workspace_path = pathlib.Path(workspace).expanduser().resolve()
    agent = _command_path("CHAT_WORK_AGENT_PATH")
    failures: list[str] = []
    if not goal.strip():
        failures.append("goal_empty")
    if len(goal) > 20000:
        failures.append("goal_too_large")
    if not workspace_path.is_dir():
        failures.append("workspace_missing")
    if not _inside_allowed(workspace_path):
        failures.append("workspace_not_allowlisted")
    if not _executable(agent):
        failures.append("chat_work_agent_unavailable")
    if failures:
        return {"schemaVersion": 1, "failures": sorted(set(failures)), "result": "BLOCKED"}
    return _queue("chat-work-agent", {"workspace": str(workspace_path), "goal": goal})


def submit_a01(repo: str, issue: int, base_ref: str, goal: str, write_set: list[str], max_parallel: int, timeout_seconds: float, max_budget_usd: float, model: str | None) -> dict[str, Any]:
    candidate = pathlib.Path(repo).expanduser().resolve()
    claude = _command_path("CLAUDE_PATH")
    failures = _validate_write_set(write_set)
    if not goal.strip():
        failures.append("goal_empty")
    if len(goal) > 20000:
        failures.append("goal_too_large")
    if issue < 1:
        failures.append("issue_invalid")
    if not _valid_base_ref(base_ref):
        failures.append("base_ref_invalid")
    if not candidate.is_dir():
        failures.append("repo_missing")
    if candidate.is_dir() and not _inside_allowed(candidate):
        failures.append("repo_not_allowlisted")
    repo_path = _git_root(candidate) if candidate.is_dir() else None
    if candidate.is_dir() and repo_path is None:
        failures.append("repo_not_git")
    if repo_path is not None and not _inside_allowed(repo_path):
        failures.append("repo_root_not_allowlisted")
    dirty = _worktree_dirty(repo_path) if repo_path else None
    if dirty is None and repo_path is not None:
        failures.append("repo_status_failed")
    elif dirty:
        failures.append("repo_dirty")
    base_sha = _resolve_commit(repo_path, base_ref) if repo_path and _valid_base_ref(base_ref) else None
    if repo_path and _valid_base_ref(base_ref) and base_sha is None:
        failures.append("base_ref_unresolvable")
    if repo_path is not None and _inside(_state_dir(), repo_path):
        failures.append("state_dir_inside_repo")
    if not _executable(claude):
        failures.append("claude_unavailable")
    if not (PREPARE.is_file() and RUN_WORKFLOW.is_file()):
        failures.append("a01_a10_scripts_unavailable")
    if not (1 <= max_parallel <= 10):
        failures.append("max_parallel_out_of_range")
    if not (10 <= timeout_seconds <= 3600):
        failures.append("timeout_out_of_range")
    if not (0 <= max_budget_usd <= 100):
        failures.append("budget_out_of_range")
    if model is not None and (not model.strip() or len(model) > 200):
        failures.append("model_invalid")
    if failures:
        return {"schemaVersion": 1, "failures": sorted(set(failures)), "result": "BLOCKED"}
    assert repo_path is not None and base_sha is not None
    return _queue(
        "a01-a10",
        {
            "repo": str(repo_path), "issue": issue, "base_ref": base_ref, "base_sha": base_sha,
            "goal": goal, "write_set": write_set, "max_parallel": max_parallel,
            "timeout_seconds": timeout_seconds, "max_budget_usd": max_budget_usd,
            "model": model.strip() if model else None,
        },
    )


def status(run_id: str) -> dict[str, Any]:
    if not RUN_ID_RE.fullmatch(run_id):
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "invalid_run_id"}
    path = _record_path(run_id)
    if not path.is_file():
        return {"schemaVersion": 1, "result": "NOT_FOUND", "run_id": run_id}
    try:
        return _json_read(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return {"schemaVersion": 1, "result": "FAIL", "run_id": run_id, "failures": ["record_unreadable"]}


def receipt_summary(run_id: str, actor: str) -> dict[str, Any]:
    if not RUN_ID_RE.fullmatch(run_id):
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "invalid_run_id"}
    if actor not in {f"A{i:02d}" for i in range(1, 11)}:
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "invalid_actor"}
    record = status(run_id)
    if record.get("result") == "NOT_FOUND":
        return record
    receipt_dir_raw = record.get("receipt_dir")
    if not receipt_dir_raw:
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "receipt_dir_unavailable"}
    run_dir = _record_path(run_id).parent.resolve()
    receipt_dir = pathlib.Path(str(receipt_dir_raw)).expanduser().resolve()
    if not _inside(receipt_dir, run_dir):
        return {"schemaVersion": 1, "result": "FAIL", "reason": "receipt_dir_outside_run"}
    path = receipt_dir / f"{actor}.json"
    if not path.is_file():
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "receipt_missing"}
    try:
        payload = _json_read(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return {"schemaVersion": 1, "result": "FAIL", "reason": "receipt_unreadable"}
    if payload.get("run_id") != run_id or payload.get("actor_id") != actor:
        return {"schemaVersion": 1, "result": "FAIL", "reason": "receipt_identity_mismatch"}
    safe_keys = ["schemaVersion", "issue_number", "run_id", "actor_id", "result", "head_sha", "failures"]
    return {"schemaVersion": 1, "receipt": {key: payload.get(key) for key in safe_keys if key in payload}, "result": "PASS"}


def _run_logged(command: list[str], log_path: pathlib.Path, *, timeout: float | None = None) -> subprocess.CompletedProcess[str]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        cp = subprocess.run(command, text=True, capture_output=True, check=False, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        log_path.write_text(stdout + "\n--- STDERR ---\n" + stderr + "\n--- TIMEOUT ---\n", encoding="utf-8")
        try:
            log_path.chmod(0o600)
        except OSError:
            pass
        raise
    log_path.write_text(cp.stdout + "\n--- STDERR ---\n" + cp.stderr, encoding="utf-8")
    try:
        log_path.chmod(0o600)
    except OSError:
        pass
    return cp


def _worker_chat(spec: dict[str, Any], run_dir: pathlib.Path) -> None:
    run_id = str(spec["run_id"])
    workspace = pathlib.Path(str(spec["workspace"])).expanduser().resolve()
    agent = _command_path("CHAT_WORK_AGENT_PATH")
    if not workspace.is_dir() or not _inside_allowed(workspace):
        _update_record(run_id, status="BLOCKED", failures=["workspace_unavailable_at_worker"], finished_at_unix=int(time.time()))
        return
    if not _executable(agent):
        _update_record(run_id, status="BLOCKED", failures=["chat_work_agent_unavailable_at_worker"], finished_at_unix=int(time.time()))
        return
    _update_record(run_id, status="RUNNING", started_at_unix=int(time.time()))
    log_path = run_dir / "chat-work-agent.log"
    try:
        timeout = float(os.environ.get("CHAT_WORK_AGENT_TIMEOUT_SECONDS", "7200"))
        if not 10 <= timeout <= 86400:
            timeout = 7200.0
        cp = _run_logged([str(agent), "--cwd", str(workspace), str(spec["goal"])], log_path, timeout=timeout)
        match = re.search(r"(?:^|\n)RUN_DIR\s*[:=]\s*(.+)", cp.stdout)
        _update_record(run_id, status="PASS" if cp.returncode == 0 else "FAIL", exit_code=cp.returncode, log_path=str(log_path), external_run_dir=match.group(1).strip() if match else None, finished_at_unix=int(time.time()))
    except subprocess.TimeoutExpired:
        _update_record(run_id, status="FAIL", failures=["chat_work_agent_timeout"], log_path=str(log_path), finished_at_unix=int(time.time()))


def _worker_a01(spec: dict[str, Any], run_dir: pathlib.Path) -> None:
    run_id = str(spec["run_id"])
    repo = pathlib.Path(str(spec["repo"])).expanduser().resolve()
    claude = _command_path("CLAUDE_PATH")
    if not repo.is_dir() or not _inside_allowed(repo):
        _update_record(run_id, status="BLOCKED", failures=["repo_unavailable_at_worker"], finished_at_unix=int(time.time()))
        return
    if not _executable(claude):
        _update_record(run_id, status="BLOCKED", failures=["claude_unavailable_at_worker"], finished_at_unix=int(time.time()))
        return
    current_base = _resolve_commit(repo, str(spec["base_ref"]))
    if current_base != str(spec.get("base_sha") or ""):
        _update_record(run_id, status="VETO", stage="preflight", failures=["base_ref_drift"], queued_base_sha=spec.get("base_sha"), current_base_sha=current_base, finished_at_unix=int(time.time()))
        return
    dirty = _worktree_dirty(repo)
    if dirty is None:
        _update_record(run_id, status="FAIL", stage="preflight", failures=["repo_status_failed_at_worker"], finished_at_unix=int(time.time()))
        return
    if dirty:
        _update_record(run_id, status="VETO", stage="preflight", failures=["source_worktree_dirty_at_worker"], finished_at_unix=int(time.time()))
        return
    _update_record(run_id, status="RUNNING", started_at_unix=int(time.time()))
    workspace_root = run_dir / "worktrees"
    plan: dict[str, Any] = {}
    for index in range(1, 11):
        actor = f"A{index:02d}"
        plan[actor] = {"prompt_suffix": f"User goal: {spec['goal']}"}
    plan["A07"]["write_set"] = list(spec.get("write_set") or [])
    plan_path = run_dir / "plan-config.json"
    _json_write(plan_path, plan)
    preparation_path = run_dir / "run-preparation.json"
    prepare_log = run_dir / "prepare.log"
    prepare = _run_logged([
        sys.executable, str(PREPARE), "--repo", str(repo), "--issue", str(spec["issue"]),
        "--run-id", run_id, "--base-sha", str(spec["base_sha"]), "--base-ref", str(spec["base_ref"]),
        "--workspace-root", str(workspace_root), "--plan-config", str(plan_path), "--output", str(preparation_path),
    ], prepare_log)
    if prepare.returncode != 0 or not preparation_path.is_file():
        _update_record(run_id, status="FAIL", stage="prepare", exit_code=prepare.returncode, log_path=str(prepare_log), finished_at_unix=int(time.time()))
        return
    output_dir = run_dir / "workflow"
    run_log = run_dir / "workflow.log"
    command = [
        sys.executable, str(RUN_WORKFLOW), "--preparation-json", str(preparation_path),
        "--claude-path", str(claude), "--output-dir", str(output_dir),
        "--max-parallel", str(spec["max_parallel"]), "--timeout-seconds", str(spec["timeout_seconds"]),
        "--max-budget-usd", str(spec["max_budget_usd"]),
    ]
    if spec.get("model"):
        command.extend(["--model", str(spec["model"])])
    workflow = _run_logged(command, run_log)
    workflow_path = output_dir / "workflow.json"
    aggregate = None
    failures: list[str] = []
    if workflow_path.is_file():
        try:
            data = _json_read(workflow_path)
            aggregate = data.get("result")
            failures = list(data.get("failures") or [])
        except (OSError, ValueError, json.JSONDecodeError):
            failures.append("workflow_json_unreadable")
    _update_record(run_id, status=str(aggregate or ("PASS" if workflow.returncode == 0 else "FAIL")), stage="workflow", exit_code=workflow.returncode, preparation_path=str(preparation_path), workflow_path=str(workflow_path), receipt_dir=str(output_dir / "receipts"), log_path=str(run_log), failures=sorted(set(failures)), finished_at_unix=int(time.time()))


def worker(spec_path: str) -> None:
    path = pathlib.Path(spec_path).expanduser().resolve()
    try:
        spec = _json_read(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return
    run_id = str(spec.get("run_id") or "")
    if not RUN_ID_RE.fullmatch(run_id):
        return
    expected_spec = (_record_path(run_id).parent / "spec.json").resolve()
    if path != expected_spec:
        _update_record(run_id, status="FAIL", failures=["worker_spec_path_mismatch"], finished_at_unix=int(time.time()))
        return
    record = status(run_id)
    kind = record.get("kind")
    if spec.get("kind") != kind:
        _update_record(run_id, status="FAIL", failures=["worker_kind_mismatch"], finished_at_unix=int(time.time()))
        return
    expected_goal_hash = str(record.get("goal_sha256") or "")
    actual_goal_hash = hashlib.sha256(str(spec.get("goal", "")).encode("utf-8")).hexdigest()
    if expected_goal_hash != actual_goal_hash:
        _update_record(run_id, status="FAIL", failures=["worker_goal_hash_mismatch"], finished_at_unix=int(time.time()))
        return
    run_dir = path.parent
    try:
        if kind == "chat-work-agent":
            _worker_chat(spec, run_dir)
        elif kind == "a01-a10":
            _worker_a01(spec, run_dir)
        else:
            _update_record(run_id, status="FAIL", failures=["unknown_kind"], finished_at_unix=int(time.time()))
    except Exception as exc:
        _update_record(run_id, status="FAIL", failures=[f"worker_exception:{type(exc).__name__}"], finished_at_unix=int(time.time()))
    finally:
        try:
            path.unlink()
        except OSError:
            pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    pre = sub.add_parser("preflight")
    pre.add_argument("--workspace")
    pre.add_argument("--repo")
    chat = sub.add_parser("submit-chat")
    chat.add_argument("--workspace", required=True)
    a01 = sub.add_parser("submit-a01")
    a01.add_argument("--repo", required=True)
    a01.add_argument("--issue", type=int, required=True)
    a01.add_argument("--base-ref", default="main")
    a01.add_argument("--write-set", action="append", default=[])
    a01.add_argument("--max-parallel", type=int, default=3)
    a01.add_argument("--timeout-seconds", type=float, default=180.0)
    a01.add_argument("--max-budget-usd", type=float, default=0.05)
    a01.add_argument("--model")
    stat = sub.add_parser("status")
    stat.add_argument("--run-id", required=True)
    receipt = sub.add_parser("receipt-summary")
    receipt.add_argument("--run-id", required=True)
    receipt.add_argument("--actor", required=True)
    hidden = sub.add_parser("_worker")
    hidden.add_argument("--spec", required=True)
    args = parser.parse_args(argv)
    if args.command == "preflight":
        result = preflight(args.workspace, args.repo)
    elif args.command == "submit-chat":
        result = submit_chat(args.workspace, sys.stdin.read())
    elif args.command == "submit-a01":
        result = submit_a01(args.repo, args.issue, args.base_ref, sys.stdin.read(), args.write_set, args.max_parallel, args.timeout_seconds, args.max_budget_usd, args.model)
    elif args.command == "status":
        result = status(args.run_id)
    elif args.command == "receipt-summary":
        result = receipt_summary(args.run_id, args.actor)
    else:
        worker(args.spec)
        return 0
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("result") in {"PASS", "QUEUED", "RUNNING"} or result.get("status") in {"QUEUED", "RUNNING", "PASS"} else 1


if __name__ == "__main__":
    sys.exit(main())