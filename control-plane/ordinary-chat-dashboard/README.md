# Ordinary Chat Agent Dashboard

Read-only localhost visualization for the ordinary-chat bridge.

## Run

From the repository root:

```bash
python3 control-plane/ordinary-chat-dashboard/server.py
```

Open:

```text
http://127.0.0.1:8787/
```

## Shows
- local bridge preflight
- one run's queued/running/final state
- A01-A10 receipt summaries

## Does not do
- no run submission
- no file mutation
- no credential entry/storage
- no remote bind

The server intentionally binds only to `127.0.0.1`. It is a host-independent fallback UI even when ChatGPT MCP Apps UI is unavailable on the current account/client.
