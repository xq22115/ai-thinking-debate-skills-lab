#!/usr/bin/env python3
"""Read-only liveness reconciliation for ordinary-chat agent runs.

The reconciler never retries or mutates a run. It compares persisted state with
worker PID liveness, process-start identity when observable, and record freshness
so ordinary chat does not confuse a reused PID or a long-silent worker with a
verified-live agent. Persisted record identity is validated before liveness data
is trusted so a record copied from another run cannot yield a false terminal or
LIVE result.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import time
from typing import Any

RUN_ID_RE = re.compile(r"^[0-9a-f]{32}$")
TERMINAL = {"PASS", "FAIL", "VETO", "BLOCKED", "CANCELLED", "STALE"}
ACTIVE = {"QUEUED", "RUNNING"}


def _state_dir() -> pathlib.Path:
    raw = os.environ.get("ORDINARY_CHAT_STATE_DIR", "~/.ordinary-chat-agent")
    return pathlib.Path(raw).expanduser().resolve()


def _bounded_int(name: str, default: int, low: int, high: int) -> int:
    try:
        value = int(os.environ.get(name, str(default)))
    except ValueError:
        value = default
    return min(high, max(low, value))


def _grace_seconds() -> int:
    return _bounded_int("ORDINARY_CHAT_STARTUP_GRACE_SECONDS", 30, 1, 600)


def _max_silence_seconds() -> int:
    return _bounded_int("ORDINARY_CHAT_LIVENESS_MAX_SILENCE_SECONDS", 300, 30, 86400)


def _identity_tolerance_seconds() -> int:
    return _bounded_int("ORDINARY_CHAT_PROCESS_START_TOLERANCE_SECONDS", 15, 2, 120)


def _record_path(run_id: str) -> pathlib.Path:
    return _state_dir() / "runs" / run_id / "record.json"


def _read_record(run_id: str) -> dict[str, Any]:
    value = json.loads(_record_path(run_id).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("record_root_not_object")
    # Older fixtures may omit these fields, but any present identity/version must
    # agree with the path-selected run. Production bridge records always include both.
    if value.get("run_id") not in {None, run_id}:
        raise ValueError("record_run_id_mismatch")
    if value.get("schemaVersion") not in {None, 1}:
        raise ValueError("record_schema_invalid")
    if not isinstance(value.get("status"), str) or not value.get("status"):
        raise ValueError("record_status_invalid")
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


def _process_start_unix(pid: int) -> int | None:
    """Best-effort process birth time without requiring third-party packages.

    `ps -o lstart=` is available on macOS and common Linux distributions. A
    failure is treated as unknown rather than as proof that the worker is dead.
    """
    if pid <= 0:
        return None
    try:
        cp = subprocess.run(
            ["ps", "-o", "lstart=", "-p", str(pid)],
            text=True,
            capture_output=True,
            check=False,
            timeout=2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = cp.stdout.strip() if cp.returncode == 0 else ""
    if not text:
        return None
    try:
        stamp = dt.datetime.strptime(text, "%a %b %d %H:%M:%S %Y")
    except ValueError:
        return None
    return int(stamp.timestamp())


def _process_identity(recorded_started: int | None, observed_started: int | None) -> str:
    if not recorded_started or observed_started is None:
        return "UNKNOWN"
    tolerance = _identity_tolerance_seconds()
    # The worker records worker_started_at_unix immediately after it starts, so
    # the OS-observed process birth should be at or just before that timestamp.
    if observed_started > recorded_started + 2:
        return "MISMATCH"
    if recorded_started - observed_started > tolerance:
        return "MISMATCH"
    return "MATCH"


def inspect(run_id: str) -> dict[str, Any]:
    if not RUN_ID_RE.fullmatch(run_id):
        return {"schemaVersion": 2, "result": "NOT_FOUND", "reason": "invalid_run_id"}
    path = _record_path(run_id)
    if not path.is_file():
        return {"schemaVersion": 2, "result": "NOT_FOUND", "run_id": run_id}
    try:
        record = _read_record(run_id)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {
            "schemaVersion": 2,
            "result": "FAIL",
            "run_id": run_id,
            "reason": "record_unreadable" if isinstance(exc, (OSError, json.JSONDecodeError)) else "record_integrity_invalid",
        }

    status = str(record.get("status") or "UNKNOWN")
    now = int(time.time())
    updated = int(record.get("updated_at_unix") or record.get("created_at_unix") or 0)
    age = max(0, now - updated) if updated > 0 else None

    if status in TERMINAL:
        return {
            "schemaVersion": 2,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": status,
            "liveness": "TERMINAL",
            "worker_pid": record.get("worker_pid"),
            "result": "PASS",
        }

    if status not in ACTIVE:
        return {
            "schemaVersion": 2,
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
                "schemaVersion": 2,
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
            "schemaVersion": 2,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": status,
            "liveness": "STARTING",
            "worker_pid": None,
            "age_seconds": age,
            "result": "PASS",
        }

    alive = _pid_alive(pid)
    if alive is False:
        return {
            "schemaVersion": 2,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": "STALE",
            "liveness": "STALE",
            "worker_pid": pid,
            "age_seconds": age,
            "result": "PASS",
            "reason": "worker_pid_not_alive",
        }
    if alive is None:
        return {
            "schemaVersion": 2,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": status,
            "liveness": "UNKNOWN",
            "worker_pid": pid,
            "age_seconds": age,
            "result": "CONDITIONAL",
            "reason": "worker_pid_liveness_unknown",
        }

    recorded_started_raw = record.get("worker_started_at_unix")
    recorded_started = recorded_started_raw if isinstance(recorded_started_raw, int) else None
    observed_started = _process_start_unix(pid)
    identity = _process_identity(recorded_started, observed_started)

    if identity == "MISMATCH":
        return {
            "schemaVersion": 2,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": "STALE",
            "liveness": "STALE",
            "worker_pid": pid,
            "age_seconds": age,
            "process_identity": identity,
            "observed_process_started_at_unix": observed_started,
            "recorded_worker_started_at_unix": recorded_started,
            "result": "PASS",
            "reason": "worker_pid_reused_or_identity_mismatch",
        }

    if age is not None and age > _max_silence_seconds():
        return {
            "schemaVersion": 2,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": status,
            "liveness": "SUSPECT",
            "worker_pid": pid,
            "age_seconds": age,
            "process_identity": identity,
            "result": "CONDITIONAL",
            "reason": "worker_alive_but_record_silent_past_threshold",
        }

    if identity != "MATCH":
        return {
            "schemaVersion": 2,
            "run_id": run_id,
            "persisted_status": status,
            "effective_status": status,
            "liveness": "LIVE_UNCONFIRMED",
            "worker_pid": pid,
            "age_seconds": age,
            "process_identity": identity,
            "result": "CONDITIONAL",
            "reason": "worker_alive_process_identity_unavailable",
        }

    return {
        "schemaVersion": 2,
        "run_id": run_id,
        "persisted_status": status,
        "effective_status": status,
        "liveness": "LIVE",
        "worker_pid": pid,
        "age_seconds": age,
        "process_identity": identity,
        "result": "PASS",
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
