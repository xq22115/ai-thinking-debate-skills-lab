#!/usr/bin/env bash
set -euo pipefail
umask 077

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE_DIR="${ORDINARY_CHAT_STATE_DIR:-$HOME/.ordinary-chat-agent}"
PLAYWRIGHT_CLI_SPEC="${PLAYWRIGHT_CLI_SPEC:-@playwright/cli@0.1.18}"
PLAYWRIGHT_MCP_SPEC="${PLAYWRIGHT_MCP_SPEC:-@playwright/mcp@0.0.79}"
STEP="initialization"

fail_step() {
  printf 'BOOTSTRAP_FAILED step=%s\n' "$STEP" >&2
}
trap fail_step ERR

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "BLOCKED: required command not found: $1" >&2
    exit 2
  }
}

need git
need python3
need node
need npm

NODE_MAJOR="$(node -p 'Number(process.versions.node.split(".")[0])')"
if [[ ! "$NODE_MAJOR" =~ ^[0-9]+$ ]] || (( NODE_MAJOR < 20 )); then
  echo "BLOCKED: Node.js 20+ is required by the MCP gateway" >&2
  exit 2
fi

STATE_DIR="$(python3 -c 'import os,sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$STATE_DIR")"
mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true

cd "$ROOT"
if [[ -n "$(git status --porcelain)" ]]; then
  echo "BLOCKED: repository must be clean before bootstrap; A01-A10 also requires a clean source worktree" >&2
  exit 3
fi

STEP="install-playwright-cli"
printf '%s\n' '[1/6] Installing pinned Playwright CLI...'
npm install -g "$PLAYWRIGHT_CLI_SPEC"

STEP="install-playwright-skills"
printf '%s\n' '[2/6] Installing Playwright skill into repository-local .claude/skills...'
playwright-cli install --skills

STEP="prime-playwright-mcp"
printf '%s\n' '[3/6] Priming pinned Playwright MCP package cache...'
npx --yes "$PLAYWRIGHT_MCP_SPEC" --help >/dev/null

STEP="check-python"
printf '%s\n' '[4/6] Checking ordinary-chat Python components...'
python3 -m py_compile "$ROOT/control-plane/scripts/ordinary_chat_bridge.py"
python3 -m py_compile "$ROOT/control-plane/scripts/project_memory.py"
python3 -m py_compile "$ROOT/control-plane/ordinary-chat-dashboard/server.py"
python3 "$ROOT/control-plane/tests/test_ordinary_chat_bridge.py"
python3 "$ROOT/control-plane/tests/test_project_memory.py"
python3 "$ROOT/control-plane/tests/test_ordinary_chat_dashboard.py"

STEP="check-mcp"
printf '%s\n' '[5/6] Checking MCP gateway from the committed package lock...'
MCP_LOCK="$ROOT/control-plane/ai-system/mcp/package-lock.json"
if [[ ! -s "$MCP_LOCK" ]]; then
  echo "BLOCKED: committed MCP package-lock.json is required" >&2
  exit 2
fi
LOCK_SHA_BEFORE="$(python3 - "$MCP_LOCK" <<'PY'
import hashlib, pathlib, sys
print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())
PY
)"
(
  cd "$ROOT/control-plane/ai-system/mcp"
  npm ci --no-audit --no-fund
  npm run check
)
LOCK_SHA_AFTER="$(python3 - "$MCP_LOCK" <<'PY'
import hashlib, pathlib, sys
print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())
PY
)"
if [[ "$LOCK_SHA_BEFORE" != "$LOCK_SHA_AFTER" ]]; then
  echo "FAIL: npm ci changed the committed MCP package lock" >&2
  exit 4
fi

STEP="verify-clean-tree"
printf '%s\n' '[6/6] Verifying bootstrap did not dirty the repository...'
if [[ -n "$(git status --porcelain)" ]]; then
  echo "FAIL: bootstrap generated unignored repository changes" >&2
  git status --short >&2
  exit 4
fi

STEP="write-receipt"
RECEIPT="$STATE_DIR/bootstrap-receipt.json"
python3 - "$RECEIPT" "$ROOT" "$PLAYWRIGHT_CLI_SPEC" "$PLAYWRIGHT_MCP_SPEC" "$LOCK_SHA_BEFORE" <<'PY'
import json
import pathlib
import subprocess
import sys
import time

receipt_path = pathlib.Path(sys.argv[1])
root = pathlib.Path(sys.argv[2])

def command(*args):
    cp = subprocess.run(args, text=True, capture_output=True, check=False)
    return {"exit_code": cp.returncode, "stdout": cp.stdout.strip()[:4000]}

payload = {
    "schemaVersion": 2,
    "created_at_unix": int(time.time()),
    "repository": str(root),
    "requested": {
        "playwright_cli": sys.argv[3],
        "playwright_mcp": sys.argv[4],
    },
    "mcp_package_lock_sha256": sys.argv[5],
    "versions": {
        "git": command("git", "--version"),
        "python": command("python3", "--version"),
        "node": command("node", "--version"),
        "npm": command("npm", "--version"),
        "playwright_cli": command("playwright-cli", "--version"),
    },
    "repository_clean_after_bootstrap": True,
    "result": "PASS",
}
receipt_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
receipt_path.chmod(0o600)
PY
trap - ERR

cat <<EOF

BOOTSTRAP_CODE_READY
Receipt: $RECEIPT

Required runtime configuration before local mutation/agent launch:
  ORDINARY_CHAT_ALLOWED_ROOTS=<path-separated allowlisted project roots>
  CHAT_WORK_AGENT_PATH=<absolute chat-work-agent executable path>
  CLAUDE_PATH=<absolute authenticated Claude CLI path, if using A01-A10>

Optional guarded capabilities:
  ORDINARY_CHAT_MCP_ALLOW_SUBMIT=true
  ORDINARY_CHAT_MEMORY_ALLOW_WRITE=true

Pinned defaults may be deliberately overridden when validating an upgrade:
  PLAYWRIGHT_CLI_SPEC=<npm package@version>
  PLAYWRIGHT_MCP_SPEC=<npm package@version>

This script does not write credentials, does not enable unrestricted filesystem access,
uses the committed MCP dependency lock, and verifies that generated runtime artifacts remain
ignored so A01-A10 clean-tree gates still work.
EOF
