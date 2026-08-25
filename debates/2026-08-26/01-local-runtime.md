# 01 — Local runtime bridge

## Verdict
Prefer the host-native Remote Desktop Commander connector when it is online; use Open Interpreter as the local harness/runtime fallback, not as a second chat brain.

## Evidence
- Remote Desktop Commander exposes terminal, process, file read/write/search/edit operations directly to a connected chat client.
- Open Interpreter's August 2026 Rust releases support native sandboxing, MCP/ACP, shared `.agents/skills`, multiple harness emulations, and local execution on Windows/macOS/Linux.
- A repository config cannot remove ChatGPT's host sandbox. The practical route is an authorized local runtime bridge.

## Gap in current stack
The capability catalog has no first-class `local-runtime` capability/state, and ordinary-chat completion can be falsely inferred from repo configuration even when the local device is offline.

## Recommendation
Create `local-runtime-bridge` skill + health receipt with states `ONLINE/DEGRADED/OFFLINE/UNKNOWN`; route file/terminal work to the live host connector first, Open Interpreter second, and never claim local execution from config presence alone.

## Acceptance
A real ordinary chat must read a known local file, write a reversible temp file, read it back, run a harmless command, and delete/rollback the temp artifact through the same runtime.