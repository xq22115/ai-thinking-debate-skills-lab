# Debate 06 — Skill / Tool Routing

## Position
Routing quality is now more valuable than indiscriminately increasing tool count. Use the narrowest, lowest-context interface that can reliably finish the task.

## Preferred Order
1. Installed first-party/native ChatGPT app when it already owns the provider/action.
2. CLI + Skill for deterministic, high-throughput local/coding operations.
3. MCP for discoverable stateful external capabilities and interactive sessions.
4. Existing A01–A10 local agent runtime for multi-step autonomous work.
5. Browser automation only when no better API/tool interface exists.

## Adopt
- A machine-readable capability registry with availability, mode, latency/cost class, read/write risk, and required credentials.
- Explicit escalation/de-escalation rules.
- Preflight checks before escalating to local agent or browser.
- Context budget as a routing signal.
- Provider de-duplication: do not wrap GitHub/Gmail/Drive twice unless the bridge adds a missing composition capability.

## Reject
- A universal tool called for every task.
- Loading every MCP tool description into every prompt when not needed.
- Duplicate provider credentials across native app and custom bridge without a concrete benefit.

## Acceptance
PASS when common tasks choose a deterministic single route, fallback order is testable, and unavailable capabilities fail with an actionable reason instead of silently substituting another tool.
