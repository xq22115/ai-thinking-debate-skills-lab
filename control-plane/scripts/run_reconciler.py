#!/usr/bin/env python3
"""Read-only liveness reconciliation for ordinary-chat agent runs.

The reconciler never retries or mutates a run. It compares the persisted state
with worker PID liveness so ordinary chat can distinguish a genuinely running
worker from a stale record after a crash or host restart.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import time
from typing import Any

RUN_ID_RE = re.compile(r"^[0-9a-f]{32}$")
TERMINAL = {"PASS", "FAIL", "VETO", "BLOCKED", "CANCELLED", "STALE"}
ACTIVE = {"QUEUED", "RUNNING"}


def _state_dir() -> pathlib.Path:
    raw = os.environ.get("ORDINARY_CHAT_STATE_DIR", "~/.ordinary-chat-agent")
    return pathlib.Path(raw).expanduser().resolve()


def _grace_seconds() -> int:
    try:
        value = int(os.environ.get("ORDINARY_CHAT_STARTUP_GRACE_SECONDS", "30"))
    except ValueError:
        value = 30
    return min(600, max(1, value))


def _record_path(run_id: str) -> pathlib.Path:
    return _state_dir() / "runs" / run_id / "record.json"


def _read_record(run_id: str) -> dict[str, Any]:
    value = json.loads(_record_path(run_id).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("record_root_not_object")
    return value


def _pid_alive(pid: int) -> bool | None:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return None
    return True


def inspect(run_id: str) -> dict[str, Any]:
    if not RUN_ID_RE.fullmatch(run_id):
        return {"schemaVersion": 1, "result": "NOT_FOUND", "reason": "invalid_run_id"}
    path = _record_path(run_id)
    if not path.is_file():
        return {"schemaVersion": 1, "result": "NOT_FOUND", "run_id": run_id}
    try:
        record = _read_record(run_id)
    except (OSError, ValueError, json.JSONDecodeError):
        return {"schemaVersion": 1, "result": "FAIL", "run_id": run_id, "reason": "record_unreadable"}

    status = str(record.get("status") or "UNKNOWN")
    now = int(time.time())
    updated = int(record.get("updated_at_unix") or record.get("created_at_unix") or 0)
    age = max(0, now - updated) if updated > 0 else None

    if status in TERMINAL:
        return {
            "schemaVersion": 1,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": status,
            "liveness": "TERMINAL",
            "worker_pid": record.get("worker_pid"),
            "result": "PASS",
        }

    if status not in ACTIVE:
        return {
            "schemaVersion": 1,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": status,
            "liveness": "UNKNOWN_STATE",
            "worker_pid": record.get("worker_pid"),
            "result": "CONDITIONAL",
            "reason": "unrecognized_nonterminal_status",
        }

    raw_pid = record.get("worker_pid")
    pid = raw_pid if isinstance(raw_pid, int) else None
    if pid is None:
        if age is not None and age > _grace_seconds():
            return {
                "schemaVersion": 1,
                "run_id": run_id,
                "persisted_status": status,
                "effective_status": "STALE",
                "liveness": "STALE",
                "worker_pid": None,
                "age_seconds": age,
                "result": "PASS",
                "reason": "active_record_without_worker_pid_past_grace",
            }
        return {
            "schemaVersion": 1,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": status,
            "liveness": "STARTING",
            "worker_pid": None,
            "age_seconds": age,
            "result": "PASS",
        }

    alive = _pid_alive(pid)
    if alive is True:
        return {
            "schemaVersion": 1,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": status,
            "liveness": "LIVE",
            "worker_pid": pid,
            "age_seconds": age,
            "result": "PASS",
        }
    if alive is False:
        return {
            "schemaVersion": 1,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": "STALE",
            "liveness": "STALE",
            "worker_pid": pid,
            "age_seconds": age,
            "result": "PASS",
            "reason": "worker_pid_not_alive",
        }
    return {
        "schemaVersion": 1,
        "run_id": run_id,
        "persisted_status": status,
        "effective_status": status,
        "liveness": "UNKNOWN",
        "worker_pid": pid,
        "age_seconds": age,
        "result": "CONDITIONAL",
        "reason": "worker_pid_liveness_unknown",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)
    result = inspect(args.run_id)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("result") in {"PASS", "CONDITIONAL"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
