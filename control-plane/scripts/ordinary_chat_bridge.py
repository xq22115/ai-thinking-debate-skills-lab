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
    for item in raw.split(os.pathsep):
        if item.strip():
            roots.append(pathlib.Path(item).expanduser().resolve())
    return roots


def _inside_allowed(path: pathlib.Path) -> bool:
    resolved = path.expanduser().resolve()
    for root in _allowed_roots():
        try:
            resolved.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def _json_write(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    return json.loads(path.read_text(encoding="utf-8"))


def _record_path(run_id: str) -> pathlib.Path:
    return _state_dir() / "runs" / run_id / "record.json"


def _update_record(run_id: str, **updates: Any) -> dict[str, Any]:
    path = _record_path(run_id)
    current: dict[str, Any] = _json_read(path) if path.is_file() else {"run_id": run_id}
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


def preflight(workspace: str | None = None, repo: str | None = None) -> dict[str, Any]:
    chat_agent = _command_path("CHAT_WORK_AGENT_PATH")
    claude = _command_path("CLAUDE_PATH")
    workspace_path = pathlib.Path(workspace).expanduser().resolve() if workspace else None
    repo_path = pathlib.Path(repo).expanduser().resolve() if repo else None
    return {
        "schemaVersion": 1,
        "allowed_roots_configured": bool(_allowed_roots()),
        "allowed_root_count": len(_allowed_roots()),
        "workspace_allowed": _inside_allowed(workspace_path) if workspace_path else None,
        "repo_allowed": _inside_allowed(repo_path) if repo_path else None,
        "chat_work_agent_configured": chat_agent is not None,
        "chat_work_agent_executable": _executable(chat_agent),
        "claude_configured": claude is not None,
        "claude_executable": _executable(claude),
        "a01_a10_scripts_present": PREPARE.is_file() and RUN_WORKFLOW.is_file(),
        "state_dir": str(_state_dir()),
        "result": "PASS" if _allowed_roots() else "BLOCKED",
        "reason": None if _allowed_roots() else "ORDINARY_CHAT_ALLOWED_ROOTS_not_configured",
    }


def _validate_write_set(items: list[str]) -> list[str]:
    failures: list[str] = []
    for item in items:
        if not item or item.startswith("/") or ".." in pathlib.PurePosixPath(item).parts:
            failures.append(f"invalid_write_set:{item}")
    return failures


def _queue(kind: str, spec: dict[str, Any]) -> dict[str, Any]:
    run_id = uuid.uuid4().hex
    run_dir = _state_dir() / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    spec_path = run_dir / "spec.json"
    spec["run_id"] = run_id
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
    with open(os.devnull, "wb") as sink:
        proc = subprocess.Popen(
            [sys.executable, str(pathlib.Path(__file__).resolve()), "_worker", "--spec", str(spec_path)],
            stdin=subprocess.DEVNULL,
            stdout=sink,
            stderr=sink,
            start_new_session=True,
        )
    return _update_record(run_id, worker_pid=proc.pid)


def submit_chat(workspace: str, goal: str) -> dict[str, Any]:
    workspace_path = pathlib.Path(workspace).expanduser().resolve()
    agent = _command_path("CHAT_WORK_AGENT_PATH")
    failures: list[str] = []
    if not goal.strip():
        failures.append("goal_empty")
    if not workspace_path.is_dir():
        failures.append("workspace_missing")
    if not _inside_allowed(workspace_path):
        failures.append("workspace_not_allowlisted")
    if not _executable(agent):
        failures.append("chat_work_agent_unavailable")
    if failures:
        return {"schemaVersion": 1, "failures": failures, "result": "BLOCKED"}
    return _queue("chat-work-agent", {"workspace": str(workspace_path), "goal": goal})


def submit_a01(
    repo: str,
    issue: int,
    base_ref: str,
    goal: str,
    write_set: list[str],
    max_parallel: int,
    timeout_seconds: float,
    max_budget_usd: float,
    model: str | None,
) -> dict[str, Any]:
    repo_path = pathlib.Path(repo).expanduser().resolve()
    claude = _command_path("CLAUDE_PATH")
    failures = _validate_write_set(write_set)
    if not goal.strip():
        failures.append("goal_empty")
    if issue < 1:
        failures.append("issue_invalid")
    if not repo_path.is_dir():
        failures.append("repo_missing")
    if not _inside_allowed(repo_path):
        failures.append("repo_not_allowlisted")
    if not _executable(claude):
        failures.append("claude_unavailable")
    if not (1 <= max_parallel <= 10):
        failures.append("max_parallel_out_of_range")
    if not (10 <= timeout_seconds <= 3600):
        failures.append("timeout_out_of_range")
    if not (0 <= max_budget_usd <= 100):
        failures.append("budget_out_of_range")
    if failures:
        return {"schemaVersion": 1, "failures": sorted(set(failures)), "result": "BLOCKED"}
    return _queue(
        "a01-a10",
        {
            "repo": str(repo_path),
            "issue": issue,
            "base_ref": base_ref,
            "goal": goal,
            "write_set": write_set,
            "max_parallel": max_parallel,
            "timeout_seconds": timeout_seconds,
            "max_budget_usd": max_budget_usd,
            "model": model,
        },
    )


def status(run_id: str) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9a-f]{32}", run_id):
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "invalid_run_id"}
    path = _record_path(run_id)
    if not path.is_file():
        return {"schemaVersion": 1, "result": "NOT_FOUND", "run_id": run_id}
    return _json_read(path)


def receipt_summary(run_id: str, actor: str) -> dict[str, Any]:
    if actor not in {f"A{i:02d}" for i in range(1, 11)}:
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "invalid_actor"}
    record = status(run_id)
    receipt_dir = record.get("receipt_dir")
    if not receipt_dir:
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "receipt_dir_unavailable"}
    path = pathlib.Path(str(receipt_dir)) / f"{actor}.json"
    if not path.is_file():
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "receipt_missing"}
    payload = _json_read(path)
    safe_keys = ["schemaVersion", "issue_number", "run_id", "actor_id", "result", "head_sha", "failures"]
    return {"schemaVersion": 1, "receipt": {key: payload.get(key) for key in safe_keys if key in payload}, "result": "PASS"}


def _run_logged(command: list[str], log_path: pathlib.Path, *, timeout: float | None = None) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(command, text=True, capture_output=True, check=False, timeout=timeout)
    log_path.write_text(cp.stdout + "\n--- STDERR ---\n" + cp.stderr, encoding="utf-8")
    try:
        log_path.chmod(0o600)
    except OSError:
        pass
    return cp


def _worker_chat(spec: dict[str, Any], run_dir: pathlib.Path) -> None:
    run_id = str(spec["run_id"])
    agent = _command_path("CHAT_WORK_AGENT_PATH")
    _update_record(run_id, status="RUNNING", started_at_unix=int(time.time()))
    log_path = run_dir / "chat-work-agent.log"
    try:
        cp = _run_logged(
            [str(agent), "--cwd", str(spec["workspace"]), str(spec["goal"])],
            log_path,
            timeout=float(os.environ.get("CHAT_WORK_AGENT_TIMEOUT_SECONDS", "7200")),
        )
        match = re.search(r"(?:^|\n)RUN_DIR\s*[:=]\s*(.+)", cp.stdout)
        _update_record(
            run_id,
            status="PASS" if cp.returncode == 0 else "FAIL",
            exit_code=cp.returncode,
            log_path=str(log_path),
            external_run_dir=match.group(1).strip() if match else None,
            finished_at_unix=int(time.time()),
        )
    except subprocess.TimeoutExpired:
        _update_record(run_id, status="FAIL", failures=["chat_work_agent_timeout"], log_path=str(log_path), finished_at_unix=int(time.time()))


def _worker_a01(spec: dict[str, Any], run_dir: pathlib.Path) -> None:
    run_id = str(spec["run_id"])
    repo = pathlib.Path(str(spec["repo"]))
    claude = _command_path("CLAUDE_PATH")
    _update_record(run_id, status="RUNNING", started_at_unix=int(time.time()))
    base = subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", f"{spec['base_ref']}^{{commit}}"], text=True, capture_output=True, check=False)
    if base.returncode != 0:
        _update_record(run_id, status="FAIL", failures=["base_ref_unresolvable"], finished_at_unix=int(time.time()))
        return
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
    prepare = _run_logged(
        [
            sys.executable, str(PREPARE), "--repo", str(repo), "--issue", str(spec["issue"]),
            "--run-id", run_id, "--base-sha", base.stdout.strip(), "--base-ref", str(spec["base_ref"]),
            "--workspace-root", str(workspace_root), "--plan-config", str(plan_path), "--output", str(preparation_path),
        ],
        prepare_log,
    )
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
        data = _json_read(workflow_path)
        aggregate = data.get("result")
        failures = list(data.get("failures") or [])
    _update_record(
        run_id,
        status=str(aggregate or ("PASS" if workflow.returncode == 0 else "FAIL")),
        stage="workflow",
        exit_code=workflow.returncode,
        preparation_path=str(preparation_path),
        workflow_path=str(workflow_path),
        receipt_dir=str(output_dir / "receipts"),
        log_path=str(run_log),
        failures=failures,
        finished_at_unix=int(time.time()),
    )


def worker(spec_path: str) -> None:
    path = pathlib.Path(spec_path).resolve()
    spec = _json_read(path)
    run_id = str(spec["run_id"])
    run_dir = path.parent
    try:
        if spec.get("kind") == "unused":
            raise RuntimeError("invalid_kind")
        kind = status(run_id).get("kind")
        if kind == "chat-work-agent":
            _worker_chat(spec, run_dir)
        elif kind == "a01-a10":
            _worker_a01(spec, run_dir)
        else:
            _update_record(run_id, status="FAIL", failures=["unknown_kind"])
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
