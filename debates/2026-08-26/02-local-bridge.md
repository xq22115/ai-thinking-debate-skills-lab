# Debate 02 — Local Bridge

## Position
The missing capability is not another reasoning prompt; it is a narrow, auditable bridge from ordinary chat to the already-existing local agent workflow.

## Adopt
1. Prefer the already-installed Remote Desktop Commander for direct local read/write when its device is online.
2. For long loops, route through an explicit launcher (`chat-work-agent` or the existing `run_local_agent_workflow.py`) rather than exposing raw shell as a generic chat tool.
3. Configure `CHAT_WORK_AGENT_PATH`, `ALLOWED_WORKSPACE_ROOTS`, timeout, and output/receipt directories through environment variables.
4. Add health/preflight tools that report device/runtime/backend availability before submission.
5. Require every launched run to return a run id, status, final head, receipts, and failure reason.

## Reject
- Direct arbitrary shell MCP tool.
- Global filesystem roots such as `/` or the entire home directory by default.
- Hidden background processes with no run id or receipt.
- Claiming an offline Remote Desktop device is a sandbox restriction.

## Current Gap
The repository contains a mature local executor, but no formal ordinary-chat bridge and no `chat-work-agent` integration. Remote Desktop Commander is authorized but its device is currently offline.

## Acceptance
PASS when ordinary chat can preflight the bridge, submit only within allowlisted roots, fetch status/receipts, and fail closed when the local device or backend is unavailable.
