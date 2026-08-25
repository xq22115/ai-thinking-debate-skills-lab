# Debate 01 — MCP Core

## Position
Use MCP 2026-07-28 v2 as the interoperability layer, but do not turn every capability into MCP.

## Evidence
- MCP 2026-07-28 is stateless and uses `server/discover`; TypeScript SDK v2 is the stable line.
- MCP Apps is the UI extension; Tasks moved out of core.
- ChatGPT custom MCP write/modify remains product-plan gated; the repository cannot force-enable host features.

## Adopt
1. `@modelcontextprotocol/server` v2 and explicit modern protocol negotiation.
2. A small tool surface: health, capabilities, submit-run, run-status, receipt-fetch.
3. Accurate read/write/destructive/idempotent annotations.
4. OAuth/issuer validation when external auth is added.
5. Cache hints for stable catalogs/status metadata.

## Reject
- Monolithic `do_everything` tools.
- Pretending MCP bypasses ChatGPT sandbox, plan gates, or product permissions.
- Legacy session-dependent architecture as the default.
- Exposing arbitrary shell execution directly as an MCP tool.

## Acceptance
PASS only if the MCP layer can be disabled without breaking the existing local A01-A10 workflow, tool schemas are narrow, and every mutation produces an auditable receipt.

## Sources
- https://blog.modelcontextprotocol.io/posts/2026-07-28/
- https://ts.sdk.modelcontextprotocol.io/v2/
- https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt
