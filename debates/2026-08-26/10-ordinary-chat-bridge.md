# 10 — Ordinary Chat agent bridge

## Verdict
The highest-capability ordinary-chat architecture is a capability bus, not a jailbreak: host-native/installed connectors for local actions when available, plus a trusted local agent runtime and secure remote bridge for capabilities the chat host cannot expose directly.

## Current OpenAI boundary (August 2026)
- ChatGPT custom MCP apps can be invoked in ordinary chats.
- Full MCP write/modify support is currently limited to Business/Enterprise/Edu; Pro can connect custom MCPs with read/fetch permissions in developer mode.
- ChatGPT cannot directly connect to a localhost MCP server; OpenAI documents Secure MCP Tunnel for private/developer-machine servers.
- Agent mode does not use custom apps; deep research uses custom apps only for read/fetch.

## Gap in current stack
The architecture still sometimes treats 'ordinary ChatGPT', 'Agent mode', 'custom MCP app', 'installed connector', and 'local harness' as interchangeable. They are separate capability surfaces.

## Recommendation
Create `ordinary-chat-agent-bridge` as the canonical front door. It discovers capabilities actually exposed in the current chat, routes local file/terminal work to an online authorized connector first, routes read-only custom-MCP work through the secure bridge when supported, and hands long-running local work to a resumable harness. Never claim host sandbox removal; prove each side effect by connector/runtime read-back.

## Acceptance
From an ordinary chat, capability discovery must report what is truly callable now. If a local connector is offline, local execution is `BLOCKED` rather than simulated. When online, a reversible local file/command test must complete and produce a runtime receipt.