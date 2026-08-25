# Debate 04 — Browser Control

## Position
Use a dual browser strategy: Playwright CLI + Skills for high-throughput deterministic work, Playwright MCP only when persistent browser state and interactive introspection justify the context cost.

## Adopt
1. Playwright CLI/Skill for scripted navigation, tests, screenshots, extraction, and coding-agent workflows.
2. Playwright MCP for persistent sessions, accessibility-tree exploration, interactive state, or browser-extension attachment.
3. Separate browser credentials/profile state from repository configuration.
4. Add browser health, allowed-origin/domain policy, and artifact paths.
5. Keep Browser Use optional/experimental until its current reconnect, long-running, and security behavior is validated against our acceptance gates.

## Reject
- Enabling unrestricted filesystem access by default.
- Arbitrary page JavaScript execution for untrusted prompts/clients.
- Treating browser automation as a substitute for provider APIs when a first-party app/API is available.
- Always-on browser MCP for simple deterministic tasks.

## Acceptance
PASS when the router selects CLI versus MCP based on task statefulness, secrets are isolated, browsing has domain/workspace boundaries, and browser runs produce auditable artifacts.

## Sources
- https://github.com/microsoft/playwright-mcp
- https://github.com/browser-use/browser-use
