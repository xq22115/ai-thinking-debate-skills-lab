# Host Adapter Boundary — RC1

Portable skills must not hard-code host-specific execution details.

## Adapter Contract

Every host adapter should declare:

```yaml
host: <product/runtime>
verified_version: <exact version/date>
os: [windows, macos, linux, web]
capabilities: []
permissions_required: []
unsupported: []
last_verified: YYYY-MM-DD
```

## Required Adapter Families

### OpenAI / Agents SDK
Map portable workflow concepts to current agent, tool, sandbox, tracing, handoff/subagent, and durable-state primitives. Verify exact SDK/API version before installation.

### Anthropic / Agent Skills
Keep `SKILL.md` portable; map installation, plugin/marketplace/API behavior, permissions, and host-specific resources separately.

### MCP
Target the current MCP specification explicitly. Application state must not silently depend on obsolete protocol-session assumptions.

### OpenClaw
Pin an exact release/commit because interfaces change rapidly. Verify skills/plugins, memory/state, runners, gateway, worktrees, and subagent behavior against the installed version.

### Windows
Probe PowerShell/cmd/WSL, quoting, paths, services/tasks, permissions, filesystem behavior, and desktop-app constraints.

### macOS
Probe shell, TCC, app sandbox, launchd, Keychain, filesystem behavior, and desktop-app constraints.

## Rule

A portable skill may describe **what must happen**. The adapter owns **how this host performs it**.

Never label an adapter `verified` from documentation alone; host-live execution evidence is required.