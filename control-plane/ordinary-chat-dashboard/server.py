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

HERE = pathlib.Path(__file__).resolve().parent
BRIDGE = HERE.parent / "scripts" / "ordinary_chat_bridge.py"
HOST = "127.0.0.1"
PORT = int(os.environ.get("ORDINARY_CHAT_DASHBOARD_PORT", "8787"))


def _bridge(args: list[str]) -> tuple[int, dict]:
    cp = subprocess.run(
        [sys.executable, str(BRIDGE), *args],
        text=True,
        capture_output=True,
        check=False,
        timeout=15,
        env=os.environ,
    )
    try:
        return cp.returncode, json.loads(cp.stdout or "{}")
    except json.JSONDecodeError:
        return 1, {"result": "FAIL", "reason": "bridge_non_json_output"}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlsplit(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/api/preflight":
            args = ["preflight"]
            if query.get("workspace", [""])[0]:
                args += ["--workspace", query["workspace"][0]]
            if query.get("repo", [""])[0]:
                args += ["--repo", query["repo"][0]]
            code, payload = _bridge(args)
            return self._json(200 if code == 0 else 409, payload)

        match = re.fullmatch(r"/api/run/([0-9a-f]{32})", parsed.path)
        if match:
            code, payload = _bridge(["status", "--run-id", match.group(1)])
            return self._json(200 if payload.get("result") != "NOT_FOUND" else 404, payload)

        receipt = re.fullmatch(r"/api/receipt/([0-9a-f]{32})/(A0[1-9]|A10)", parsed.path)
        if receipt:
            code, payload = _bridge([
                "receipt-summary", "--run-id", receipt.group(1), "--actor", receipt.group(2)
            ])
            return self._json(200 if code == 0 else 404, payload)

        if parsed.path == "/api/healthz":
            return self._json(200, {"ok": True, "read_only": True})

        return super().do_GET()

    def do_POST(self):
        self._json(405, {"error": "read_only_dashboard"})

    def log_message(self, fmt, *args):
        sys.stderr.write("dashboard: " + (fmt % args) + "\n")


if __name__ == "__main__":
    print(f"ordinary-chat dashboard: http://{HOST}:{PORT}/")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
