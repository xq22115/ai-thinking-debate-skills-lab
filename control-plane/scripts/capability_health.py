#!/usr/bin/env python3
"""Local capability health snapshot for ordinary-chat routing.

This module intentionally probes only fixed, known execution surfaces. It does not
accept arbitrary commands and never emits credential values. External ChatGPT app
state is represented as requiring host-side preflight rather than guessed locally.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import tempfile
import time
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREPARE = ROOT / "scripts" / "prepare_local_agent_run.py"
RUN_WORKFLOW = ROOT / "scripts" / "run_local_agent_workflow.py"
MEMORY = ROOT / "scripts" / "project_memory.py"
DASHBOARD = ROOT / "ordinary-chat-dashboard" / "server.py"
MCP_PACKAGE = ROOT / "ai-system" / "mcp" / "package.json"


def _state_dir() -> pathlib.Path:
    raw = os.environ.get("ORDINARY_CHAT_STATE_DIR", "~/.ordinary-chat-agent")
    path = pathlib.Path(raw).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path


def _bounded_int(name: str, default: int, low: int, high: int) -> int:
    try:
        value = int(os.environ.get(name, str(default)))
    except ValueError:
        value = default
    return min(high, max(low, value))


def _configured_exec(env_name: str) -> tuple[bool, bool]:
    raw = os.environ.get(env_name, "").strip()
    if not raw:
        return False, False
    path = pathlib.Path(raw).expanduser().resolve()
    return True, bool(path.is_file() and os.access(path, os.X_OK))


def _command_ready(env_name: str, default_name: str) -> tuple[bool, str | None]:
    override = os.environ.get(env_name, "").strip()
    if override:
        path = pathlib.Path(override).expanduser().resolve()
        return bool(path.is_file() and os.access(path, os.X_OK)), path.name
    found = shutil.which(default_name)
    return found is not None, pathlib.Path(found).name if found else None


def _atomic_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.parent.chmod(0o700)
    except OSError:
        pass
    fd, temp_path = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        try:
            os.chmod(temp_path, 0o600)
        except OSError:
            pass
        os.replace(temp_path, path)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def snapshot(*, persist: bool = True, ttl_seconds: int | None = None) -> dict[str, Any]:
    ttl = ttl_seconds if ttl_seconds is not None else _bounded_int("ORDINARY_CHAT_HEALTH_TTL_SECONDS", 60, 5, 3600)
    ttl = min(3600, max(5, int(ttl)))
    now = int(time.time())

    chat_configured, chat_ready = _configured_exec("CHAT_WORK_AGENT_PATH")
    claude_configured, claude_ready = _configured_exec("CLAUDE_PATH")
    playwright_ready, playwright_bin = _command_ready("PLAYWRIGHT_CLI_BIN", "playwright-cli")
    browser_use_ready, browser_use_bin = _command_ready("BROWSER_USE_BIN", "browser-use")

    a01_scripts = PREPARE.is_file() and RUN_WORKFLOW.is_file()
    health: dict[str, dict[str, Any]] = {
        "github-native": {
            "state": "external_preflight_required",
            "ready": None,
            "reason": "ChatGPT plugin/app connectivity is host-side state",
        },
        "remote-desktop-commander": {
            "state": "external_preflight_required",
            "ready": None,
            "reason": "device connectivity is visible only through the connected app",
        },
        "chat-work-agent": {
            "state": "ready" if chat_ready else ("misconfigured" if chat_configured else "not_configured"),
            "ready": chat_ready,
            "configured": chat_configured,
        },
        "a01-a10-runtime": {
            "state": "ready" if claude_ready and a01_scripts else "not_ready",
            "ready": bool(claude_ready and a01_scripts),
            "claude_configured": claude_configured,
            "claude_executable": claude_ready,
            "runtime_scripts_present": a01_scripts,
        },
        "ordinary-chat-mcp": {
            "state": "code_ready_runtime_external",
            "ready": None,
            "code_ready": MCP_PACKAGE.is_file(),
            "reason": "deployment/listening state is checked by the MCP consumer or health endpoint",
        },
        "playwright-cli": {
            "state": "ready" if playwright_ready else "not_installed",
            "ready": playwright_ready,
            "binary": playwright_bin,
        },
        "browser-use-cli": {
            "state": "ready" if browser_use_ready else "not_installed",
            "ready": browser_use_ready,
            "binary": browser_use_bin,
        },
        "playwright-mcp": {
            "state": "runtime_external",
            "ready": None,
            "reason": "MCP process/extension attachment is checked at consumer connection time",
        },
        "project-memory": {
            "state": "ready" if MEMORY.is_file() else "missing",
            "ready": MEMORY.is_file(),
        },
        "ordinary-chat-dashboard": {
            "state": "code_ready_runtime_external" if DASHBOARD.is_file() else "missing",
            "ready": None if DASHBOARD.is_file() else False,
            "code_ready": DASHBOARD.is_file(),
        },
    }

    payload: dict[str, Any] = {
        "schemaVersion": 1,
        "generated_at_unix": now,
        "expires_at_unix": now + ttl,
        "ttl_seconds": ttl,
        "capabilities": health,
        "result": "PASS",
    }
    if persist:
        _atomic_json(_state_dir() / "health" / "capability-health.json", payload)
    return payload


def cached_or_snapshot() -> dict[str, Any]:
    path = _state_dir() / "health" / "capability-health.json"
    if path.is_file():
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value, dict) and int(value.get("expires_at_unix", 0)) > int(time.time()):
                value["cache"] = "HIT"
                return value
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            pass
    value = snapshot(persist=True)
    value["cache"] = "MISS"
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot")
    snap.add_argument("--no-persist", action="store_true")
    snap.add_argument("--ttl-seconds", type=int)
    sub.add_parser("cached")
    args = parser.parse_args(argv)

    if args.command == "snapshot":
        result = snapshot(persist=not args.no_persist, ttl_seconds=args.ttl_seconds)
    else:
        result = cached_or_snapshot()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("result") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
