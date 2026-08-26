#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE_DIR="${ORDINARY_CHAT_STATE_DIR:-$HOME/.ordinary-chat-agent}"
BROWSER_USE_SPEC="${BROWSER_USE_SPEC:-browser-use}"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "BLOCKED: required command not found: $1" >&2
    exit 2
  }
}

need git
need uv
need python3

case "$BROWSER_USE_SPEC" in
  browser-use|browser-use==*|browser-use@*) ;;
  *)
    echo "BLOCKED: BROWSER_USE_SPEC must target the browser-use package" >&2
    exit 2
    ;;
esac

if [ -n "$(git -C "$ROOT" status --porcelain)" ]; then
  echo "BLOCKED: source repository must be clean before browser-use bootstrap" >&2
  exit 2
fi

mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true

printf '%s\n' '[1/4] Installing Browser Use CLI with Python 3.12 via uv...'
uv tool install --python 3.12 --upgrade --force "$BROWSER_USE_SPEC"

need browser-use

printf '%s\n' '[2/4] Installing Browser Use agent skill into supported user skill locations...'
browser-use skill install

printf '%s\n' '[3/4] Verifying Browser Use CLI...'
browser-use --help >/dev/null

if [ -n "$(git -C "$ROOT" status --porcelain)" ]; then
  echo "FAIL: browser-use bootstrap modified the governed source repository" >&2
  git -C "$ROOT" status --short >&2
  exit 1
fi

printf '%s\n' '[4/4] Writing private bootstrap receipt...'
BROWSER_USE_VERSION="$(browser-use --version 2>/dev/null || printf '%s' unknown)"
python3 - "$STATE_DIR/browser-use-bootstrap-receipt.json" "$BROWSER_USE_VERSION" "$BROWSER_USE_SPEC" <<'PY'
import json, os, pathlib, sys, tempfile, time
path = pathlib.Path(sys.argv[1]).expanduser().resolve()
payload = {
    "schemaVersion": 1,
    "installed_at_unix": int(time.time()),
    "browser_use_version": sys.argv[2],
    "requested_spec": sys.argv[3],
    "result": "PASS",
}
path.parent.mkdir(parents=True, exist_ok=True)
fd, tmp = tempfile.mkstemp(prefix=path.name + '.', dir=path.parent)
with os.fdopen(fd, 'w', encoding='utf-8') as handle:
    json.dump(payload, handle, indent=2, sort_keys=True)
    handle.write('\n')
try:
    os.chmod(tmp, 0o600)
except OSError:
    pass
os.replace(tmp, path)
PY

echo "BROWSER_USE_BOOTSTRAP_READY"
