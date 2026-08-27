# Ordinary Chat Agent MCP Gateway

Tool-first MCP gateway for ordinary chat. It wraps the repository's existing local agent runtime through a narrow Python bridge instead of exposing arbitrary shell access.

## Baseline
- MCP core target: `2026-07-28`
- TypeScript SDK: `@modelcontextprotocol/server` `2.0.0`
- Node.js: 20+
- Default bind: `127.0.0.1:3000`
- Default mutations: disabled
- Dependency policy: exact direct versions + committed npm lockfile + `npm ci`

## Default read-only tools
- `capabilities`
- `bridge_preflight`
- `agent_run_status`
- `agent_receipt_summary`
- `project_memory_search`

## Guarded mutation tools
These are not registered unless `ORDINARY_CHAT_MCP_ALLOW_SUBMIT=true`:
- `agent_submit_chat_work`
- `agent_submit_a01_a10`

Project-memory mutation tools additionally require `ORDINARY_CHAT_MEMORY_ALLOW_WRITE=true`:
- `project_memory_add`
- `project_memory_delete`

## Reproducible local development

```bash
cd control-plane/ai-system/mcp
npm ci --no-audit --no-fund
npm run check
npm run dev
```

The committed `package-lock.json` is part of the runtime contract. CI/bootstrap must not silently regenerate it. A deliberate dependency refresh uses the trusted `mcp-lockfile-refresh` recipe on a dedicated task branch, with the resulting lockfile promoted only after task-specific acceptance, changed-path adjudication, and zero-reexecution resume evidence pass.

Health:

```bash
curl http://127.0.0.1:3000/healthz
```

## Required local bridge configuration
Before local mutation or agent launch, configure allowlisted roots and the relevant runtime path:

```bash
export ORDINARY_CHAT_ALLOWED_ROOTS=/absolute/project/root
export CHAT_WORK_AGENT_PATH=/absolute/path/to/chat-work-agent
export CLAUDE_PATH=/absolute/path/to/claude
```

Use `.env.example` as a template; do not commit real credentials.

## Remote exposure
The gateway refuses a non-loopback bind unless `MCP_ALLOWED_HOSTS` is configured. It also requires bearer auth by default for a remote bind unless an explicit override is set.

For ChatGPT, use only the remote/custom-MCP connectivity mechanism actually exposed by the current account/workspace (for example an approved HTTPS endpoint or supported secure tunnel). This repository does not bypass ChatGPT plan, workspace, or host-tool restrictions.

## UI
The v2 MCP gateway is intentionally tool-only. `@modelcontextprotocol/ext-apps` follows its own extension SDK/version line, so UI is decoupled rather than forcing incompatible SDK generations into one server.

A host-independent read-only UI is available at:

```bash
python3 control-plane/ordinary-chat-dashboard/server.py
```

Then open `http://127.0.0.1:8787/`.

## Browser
Use `../browser/README.md` for the Playwright CLI + MCP dual-routing design.

## Validation
`ordinary-chat-agent-stack.yml` checks:
- Python compile/tests
- project-memory isolation/write gates
- routing, liveness, chaos/recovery, and task-runtime regressions
- source/evidence separation and demo-template residue
- JSON policies and bootstrap syntax
- common secret prefixes
- package/lock agreement
- `npm ci` from the committed lockfile
- MCP v2 typecheck and client integration tests
- production TypeScript build
- lockfile immutability after install

Treat the gateway as active only after the actual consumer can list/call the expected tools and the relevant CI checks pass.
