# ChatGPT Desktop → Real Agent Runtime Bridge Research

## Research objective
Make a desktop ChatGPT surface invoke a **real long-running agent loop** rather than merely expose filesystem or shell tools.

## Main architectural conclusion

```text
ChatGPT Desktop
    ↓ MCP
Agent Commander MCP
    ↓
Job Manager + Acceptance / Reviewer Loop
    ↓
Claude Agent SDK and/or Codex app-server
    ↓
Filesystem / shell / browser / other tools
```

## Required Commander operations
A bridge should expose durable job semantics rather than one blocking tool call:

- `run`
- `status`
- `steer`
- `result`
- `cancel`
- `list`

A background `jobId` is important because desktop/MCP request lifetimes can be much shorter than a serious coding or repair task.

## Critical distinction
**Desktop Commander / Filesystem Server are tool layers, not autonomous agent runtimes.**

They can expose files, commands and local actions to a model, but the following capabilities require an agent/controller layer:
- decide the next action after observing a result,
- retry or choose an alternate route,
- preserve a long-running task state,
- accept steering while a job is active,
- enforce acceptance criteria,
- distinguish stalled/idle from complete,
- recover after crash/timeouts,
- produce a final evidence-backed result.

## Candidate runtimes researched — 2026-08-17
- Claude Agent SDK
- Codex app-server
- MCP bridge/backends including historical candidates such as `xihuai18/claude-code-mcp`, `steipete/claude-code-mcp` (archived reference) and `ai-cli-mcp`

Candidate repositories are **research leads, not automatically approved dependencies**. Their current maintenance, security, protocol compatibility and license must be verified before installation.

## Acceptance / reviewer loop
A durable job should not stop because the underlying model returned one message. Recommended loop:

```text
PLAN
 → ACT
 → OBSERVE
 → TEST
 → REVIEW
 → if accepted: COMPLETE
 → if repairable: REPLAN / STEER / RETRY
 → if blocked: BLOCKED_WITH_EVIDENCE
```

The worker can propose `DONE`; a separate acceptance layer determines whether the requirements are actually satisfied.

## Job record
Minimum durable state should include:
- job ID
- user request / task contract
- runtime selected
- workspace/repository identity
- current phase
- last action/result
- acceptance criteria
- unresolved blockers
- retry count / route history
- evidence receipts
- final result or cancellation reason

## Tool / runtime topology
Keep the layers distinct:

1. **UI / conversation surface** — ChatGPT Desktop.
2. **Transport** — MCP or another connector.
3. **Commander** — job lifecycle and steering.
4. **Agent runtime** — Claude Agent SDK, Codex app-server or another genuine loop runtime.
5. **Tool layer** — filesystem, shell, browser, Git, local services.
6. **Verifier** — acceptance tests/evidence.

Transport does not imply authority, and tool access does not imply autonomy.

## Windows / macOS compatibility rule
Never hard-code a shared path or launcher assumption. Runtime discovery should record:
- OS/version/architecture
- shell
- executable path
- workspace path
- MCP transport
- environment variables
- credential mechanism
- service/process lifecycle
- restart/recovery behavior

## Status
`ARCHITECTURE_RECOMMENDATION / CANDIDATES_RESEARCHED / LIVE_DESKTOP_END_TO_END_NOT_PROVEN`

The architecture is a stronger match for “Work/Codex-like continuous execution” than simply attaching Filesystem Server/Desktop Commander, but an actual ChatGPT Desktop → Commander → runtime → acceptance-loop deployment still requires host-level implementation and verification.
