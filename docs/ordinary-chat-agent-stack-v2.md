# Ordinary Chat Agent Stack v2

## Objective
Maximize useful capability from an ordinary chat by routing work to authorized execution layers rather than pretending the chat host itself has become an unrestricted local agent.

## Runtime Order

### 1. Connected provider app
Use an installed first-party/provider app first when it already supports the requested action.

### 2. Direct local tool
For bounded local inspection/editing/terminal work, use the authorized Remote Desktop Commander connection when online.

### 3. Browser
- deterministic/replayable: Playwright CLI + installed Skills
- persistent/exploratory: Playwright MCP

### 4. Long local agent task
Use `chat-work-agent` for a long inspect-act-verify loop, or the existing A01-A10 workflow when dependency-aware ten-role execution and receipt adjudication are needed.

### 5. MCP gateway
When the ChatGPT account/workspace exposes custom MCP, connect the ordinary-chat MCP gateway for capability discovery, bridge preflight, run status, receipt summaries, project-memory search, and explicitly enabled submit tools.

## Local Bootstrap

```bash
bash control-plane/scripts/bootstrap_ordinary_chat_stack.sh
```

The bootstrap installs current Playwright CLI, installs its agent skills, primes the Playwright MCP package, compiles the bridge/memory scripts, installs MCP dependencies, and runs the MCP check suite.

## Required Environment

```bash
export ORDINARY_CHAT_ALLOWED_ROOTS=/absolute/allowed/root
export CHAT_WORK_AGENT_PATH=/absolute/path/to/chat-work-agent
export CLAUDE_PATH=/absolute/path/to/claude
```

Multiple allowed roots use the operating system path separator.

## Default Safety State
- MCP submit tools: OFF
- project memory writes: OFF
- local path access without allowlist: BLOCKED
- raw shell MCP tool: nonexistent
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

## MCP Gateway

```bash
cd control-plane/ai-system/mcp
npm install
npm run check
npm run dev
```

Default endpoint: `http://127.0.0.1:3000/mcp`.

## Dashboard

```bash
python3 control-plane/ordinary-chat-dashboard/server.py
```

Open `http://127.0.0.1:8787/`.

## Verification
A capability is considered active only after:
1. its preflight is PASS;
2. its relevant automated tests are PASS;
3. the actual consumer can list/call it;
4. mutations produce the expected run/receipt evidence;
5. no broader capability was silently substituted.

## Platform Boundary
A repository, Skill, MCP server, plugin permission, or browser tool cannot force-enable a ChatGPT host feature, plan-gated feature, hidden model route, or server-side permission that the product has not exposed. The agent-like behavior here comes from routing ordinary chat to authorized external/local runtimes with verifiable state and receipts.
