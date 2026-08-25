# Debate 05 — MCP Apps / Visual UI

## Position
Add UI only where it improves run visibility and control. The best first UI is an agent-run dashboard, not a decorative chat widget.

## Adopt
1. Use MCP Apps / Apps SDK UI for run status, dependency graph, actor states, receipt links, failures, and final result when the ChatGPT host supports it.
2. Keep a standalone local/web control-plane dashboard as a host-independent fallback.
3. Separate data tools from render tools so status data can be reused without forcing widget rendering.
4. Display PASS / FAIL / VETO / BLOCKED, budget, elapsed time, base freshness, and receipt provenance.
5. Keep CSP and external domains minimal and explicit.

## Reject
- UI that hides the actual execution state.
- Widget-only functionality that makes the underlying tools unusable from non-UI MCP clients.
- Assuming a widget grants permissions that the MCP tool or ChatGPT product does not have.
- Loading arbitrary remote scripts/domains.

## Acceptance
PASS when all critical run state remains available as structured tool output and the UI is an optional visualization layer with explicit CSP/domain metadata.

## Sources
- OpenAI Apps SDK documentation
- MCP Apps extension documentation
