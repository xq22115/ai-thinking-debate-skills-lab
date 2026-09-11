#!/usr/bin/env python3
"""Read-only localhost dashboard for ordinary-chat agent runs."""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
BRIDGE = HERE.parent / "scripts" / "ordinary_chat_bridge.py"
HOST = "127.0.0.1"


def _port() -> int:
    try:
        value = int(os.environ.get("ORDINARY_CHAT_DASHBOARD_PORT", "8787"))
    except ValueError as exc:
        raise SystemExit("ORDINARY_CHAT_DASHBOARD_PORT must be an integer") from exc
    if not 1 <= value <= 65535:
        raise SystemExit("ORDINARY_CHAT_DASHBOARD_PORT must be between 1 and 65535")
    return value


def _bridge(args: list[str]) -> tuple[int, dict[str, Any]]:
    try:
        cp = subprocess.run(
            [sys.executable, str(BRIDGE), *args],
            text=True,
            capture_output=True,
            check=False,
            timeout=15,
            env=os.environ,
        )
    except subprocess.TimeoutExpired:
        return 1, {"schemaVersion": 1, "result": "FAIL", "reason": "dashboard_bridge_timeout"}
    except OSError as exc:
        return 1, {
            "schemaVersion": 1,
            "result": "FAIL",
            "reason": f"dashboard_bridge_spawn_error:{type(exc).__name__}",
        }
    try:
        payload = json.loads(cp.stdout or "{}")
    except json.JSONDecodeError:
        return 1, {"schemaVersion": 1, "result": "FAIL", "reason": "bridge_non_json_output"}
    if not isinstance(payload, dict):
        return 1, {"schemaVersion": 1, "result": "FAIL", "reason": "bridge_json_not_object"}
    return cp.returncode, payload


def _http_status(code: int, payload: dict[str, Any]) -> int:
    if payload.get("result") == "NOT_FOUND":
        return 404
    reason = str(payload.get("reason") or "")
    if reason.startswith("dashboard_bridge_"):
        return 503
    return 200 if code == 0 else 409


class Handler(SimpleHTTPRequestHandler):
    server_version = "OrdinaryChatDashboard/1.0"
    sys_version = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        super().end_headers()

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/api/preflight":
            args = ["preflight"]
            workspace = query.get("workspace", [""])[0]
            repo = query.get("repo", [""])[0]
            if workspace:
                args += ["--workspace", workspace]
            if repo:
                args += ["--repo", repo]
            code, payload = _bridge(args)
            return self._json(_http_status(code, payload), payload)

        match = re.fullmatch(r"/api/run/([0-9a-f]{32})", parsed.path)
        if match:
            code, payload = _bridge(["status", "--run-id", match.group(1)])
            return self._json(_http_status(code, payload), payload)

        receipt = re.fullmatch(r"/api/receipt/([0-9a-f]{32})/(A0[1-9]|A10)", parsed.path)
        if receipt:
            code, payload = _bridge([
                "receipt-summary", "--run-id", receipt.group(1), "--actor", receipt.group(2)
            ])
            return self._json(_http_status(code, payload), payload)

        if parsed.path == "/api/healthz":
            return self._json(200, {"ok": True, "read_only": True})

        if parsed.path in {"/", "/index.html"}:
            self.path = "/index.html"
            return super().do_GET()

        return self._json(404, {"error": "not_found"})

    def _read_only(self) -> None:
        self._json(405, {"error": "read_only_dashboard"})

    do_POST = _read_only
    do_PUT = _read_only
    do_PATCH = _read_only
    do_DELETE = _read_only

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("dashboard: " + (fmt % args) + "\n")


class DashboardServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    port = _port()
    print(f"ordinary-chat dashboard: http://{HOST}:{port}/")
    DashboardServer((HOST, port), Handler).serve_forever()
