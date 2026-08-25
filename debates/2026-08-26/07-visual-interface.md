# 07 — Visual interface

## Verdict
Use two visual layers instead of inventing another dashboard: an in-chat MCP/App widget for compact run state, plus Interpreter Workstation (or an existing desktop shell) for local multi-file/computer workflows. Use Canvs/Figma only for artifacts, not as the agent control plane.

## Evidence
- AI SDK 7 adds MCP Apps and a terminal UI; Interpreter Workstation is an open-source desktop agent shell over Open Interpreter that works across files, documents, spreadsheets, PDFs, browser, and computer.
- Workstation deliberately keeps the runtime in Open Interpreter and the desktop UI as a separate shell, avoiding duplicated provider/harness implementations.

## Gap in current stack
The current control plane has receipts and GitHub state but no ordinary-chat visualization contract for current goal, running tool, approval, evidence, blocked reason, and resumable next action.

## Recommendation
Create a tiny `agent-status-card` MCP Apps resource/widget schema backed by the durable run receipt. Keep the UI read-only except explicit approval controls. For full desktop work, prefer an existing open-source shell rather than rebuilding Electron from scratch.

## Acceptance
The chat UI must render the same run ID/status/evidence that the backend receipt reports, and stale UI state must be detectable by revision/timestamp mismatch.