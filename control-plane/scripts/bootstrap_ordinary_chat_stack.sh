#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE_DIR="${ORDINARY_CHAT_STATE_DIR:-$HOME/.ordinary-chat-agent}"

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

mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true

printf '%s\n' '[1/5] Installing current official Playwright CLI...'
npm install -g @playwright/cli@latest

printf '%s\n' '[2/5] Installing Playwright agent skills...'
playwright-cli install --skills

printf '%s\n' '[3/5] Priming Playwright MCP package cache...'
npx --yes @playwright/mcp@latest --help >/dev/null

printf '%s\n' '[4/5] Checking ordinary-chat bridge Python...'
python3 -m py_compile "$ROOT/control-plane/scripts/ordinary_chat_bridge.py"
python3 -m py_compile "$ROOT/control-plane/scripts/project_memory.py"

printf '%s\n' '[5/5] Checking MCP gateway dependencies/build...'
(
  cd "$ROOT/control-plane/ai-system/mcp"
  npm install
  npm run check
)

cat <<'EOF'

BOOTSTRAP_CODE_READY

Required runtime configuration before local mutation/agent launch:
  ORDINARY_CHAT_ALLOWED_ROOTS=<path-separated allowlisted project roots>
  CHAT_WORK_AGENT_PATH=<absolute chat-work-agent executable path>
  CLAUDE_PATH=<absolute authenticated Claude CLI path, if using A01-A10>

Optional guarded capabilities:
  ORDINARY_CHAT_MCP_ALLOW_SUBMIT=true
  ORDINARY_CHAT_MEMORY_ALLOW_WRITE=true

Playwright MCP safe default example:
  control-plane/ai-system/browser/playwright.mcp.example.json

This script does not write credentials and does not enable unrestricted filesystem access.
EOF
