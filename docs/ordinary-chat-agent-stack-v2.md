# Ordinary Chat Agent Stack v2

## Objective
Maximize useful capability from an ordinary chat by routing work to authorized execution layers rather than pretending the chat host itself has become an unrestricted local agent.

## Runtime Order

### 1. Connected provider app
Use an installed first-party/provider app first when it already supports the requested action.

### 2. Direct local tool
For bounded local inspection/editing/terminal work, use the authorized Remote Desktop Commander connection when online.

### 3. Browser
- deterministic/replayable: Playwright CLI + installed Skill
- persistent/exploratory: Playwright MCP
- visual session monitoring: `playwright-cli show`

### 4. Project memory
Use explicit project-memory search for scoped recall with provenance. Memory is never populated automatically from transcripts.

### 5. Long local agent task
Use `chat-work-agent` for a long inspect-act-verify loop, or the existing A01-A10 workflow when dependency-aware ten-role execution and receipt adjudication are needed.

A01-A10 submissions bind to the resolved base SHA at queue time. If the named base ref moves before the worker starts, the run is vetoed instead of silently executing against a different commit.

### 6. MCP gateway
When the ChatGPT account/workspace exposes custom MCP, connect the ordinary-chat MCP gateway for capability discovery, bridge preflight, run status, receipt summaries, project-memory search, and explicitly enabled submit tools.

### 7. Local dashboard
Use the read-only localhost dashboard for visual preflight, run status, and receipt inspection. It serves only the dashboard page and `/api/*`; source files in the dashboard directory are not exposed as static files.

## Local Bootstrap

The source repository must be clean before bootstrap because the governed A01-A10 preparation also requires a clean source worktree.

```bash
bash control-plane/scripts/bootstrap_ordinary_chat_stack.sh
```

The bootstrap:
1. validates Git/Python/Node/npm and requires Node.js 20+;
2. installs Playwright CLI;
3. installs the Playwright Skill at repository-local `.claude/skills/playwright-cli`;
4. primes the Playwright MCP package;
5. compiles and tests bridge, memory, dashboard, and MCP components;
6. verifies generated artifacts remain ignored and the repository is still clean;
7. writes a private `bootstrap-receipt.json` under `ORDINARY_CHAT_STATE_DIR` with installed tool versions and no credentials.

Generated Playwright/MCP runtime outputs are deliberately ignored: `.playwright-cli/`, generated Playwright Skill content, MCP `node_modules/`, MCP `dist/`, and MCP `.env`.

For reproducible installs, override the package specs:

```bash
export PLAYWRIGHT_CLI_SPEC='@playwright/cli@<version>'
export PLAYWRIGHT_MCP_SPEC='@playwright/mcp@<version>'
```

## Required Environment

```bash
export ORDINARY_CHAT_ALLOWED_ROOTS=/absolute/allowed/root
export CHAT_WORK_AGENT_PATH=/absolute/path/to/chat-work-agent
export CLAUDE_PATH=/absolute/path/to/claude
```

Multiple allowed roots use the operating system path separator.

Bridge preflight reports path validity separately from backend readiness through fields including `workspace_allowed`, `repo_root_allowed`, `chat_submit_ready`, and `a01_submit_ready`.

## Default Safety State
- MCP submit tools: OFF
- project memory writes: OFF
- local path access without allowlist: BLOCKED
- raw shell MCP tool: nonexistent
- A01-A10 dirty source worktree: BLOCKED/VETO
- A01-A10 base-ref drift after queueing: VETO
- remote MCP bind without host policy: refused
- remote MCP bind without auth/explicit override: refused
- dashboard: read-only, localhost only

To enable guarded submit tools after validation:

```bash
export ORDINARY_CHAT_MCP_ALLOW_SUBMIT=true
```

To separately allow explicit project-memory writes:

```bash
export ORDINARY_CHAT_MEMORY_ALLOW_WRITE=true
```

`ephemeral` memory has a real TTL (default 86400 seconds). Override within the bounded range used by the implementation:

```bash
export ORDINARY_CHAT_MEMORY_EPHEMERAL_TTL_SECONDS=3600
```

Memory database/state directories are hardened to private user permissions where the platform supports POSIX modes. Search treats `%` and `_` literally instead of as SQL wildcard input.

## MCP Gateway

For a manual local check without creating a package lock in the source tree:

```bash
cd control-plane/ai-system/mcp
npm install --package-lock=false --no-audit --no-fund
npm run check
npm run dev
```

Default endpoint: `http://127.0.0.1:3000/mcp`.

## Dashboard

```bash
python3 control-plane/ordinary-chat-dashboard/server.py
```

Open `http://127.0.0.1:8787/`.

The dashboard rejects POST/PUT/PATCH/DELETE, blocks direct serving of its Python source files, and sets no-store, frame, content-type, referrer, and CSP headers.

## Verification
A capability is considered active only after:
1. its path/capability preflight is PASS;
2. the relevant backend-specific readiness field is true;
3. its relevant automated tests are PASS;
4. the actual consumer can list/call it;
5. mutations produce the expected run/receipt evidence;
6. no broader capability was silently substituted.

A long-running worker also re-checks allowlists/backend availability. A01-A10 re-checks source cleanliness and queued base SHA before execution to reduce queue-time/worker-time drift.

## Platform Boundary
A repository, Skill, MCP server, plugin permission, or browser tool cannot force-enable a ChatGPT host feature, plan-gated feature, hidden model route, or server-side permission that the product has not exposed. The agent-like behavior here comes from routing ordinary chat to authorized external/local runtimes with verifiable state and receipts.
