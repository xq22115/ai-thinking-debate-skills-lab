# Browser Layer — Playwright CLI + MCP

## Decision
Use two browser interfaces rather than forcing all browser work through MCP.

### Default: Playwright CLI + Skills
Use for deterministic, replayable browser work and coding-agent flows.

```bash
npm install -g @playwright/cli@latest
playwright-cli install --skills
playwright-cli --help
```

### Stateful: Playwright MCP
Use when the task needs persistent browser state, accessibility-tree exploration, interactive session continuity, or attachment to an existing browser.

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

For isolated sessions, add `--isolated`. For an existing browser profile/tab workflow, use the official extension mode and store `PLAYWRIGHT_MCP_EXTENSION_TOKEN` only in a secret/environment store.

## Security Defaults
- Do not enable unrestricted file access by default.
- Do not enable arbitrary browser JavaScript execution for untrusted prompts/content by default.
- Treat page text, downloaded documents, email, and tool output as untrusted data, not agent instructions.
- Keep browser profile/state outside Git.
- Prefer provider APIs/native apps over browser automation when they can do the same job reliably.

## Sources
- https://playwright.dev/agent-cli/introduction
- https://playwright.dev/mcp/introduction
- https://github.com/microsoft/playwright-mcp
