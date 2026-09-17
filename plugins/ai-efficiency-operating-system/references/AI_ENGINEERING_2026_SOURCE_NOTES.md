# AI Engineering 2026 Source Notes

Status: current-source learning notes, not runtime proof.
Verified: 2026-09-18 against primary sources.

The pack records reusable mechanisms separately from product-specific claims so skills remain portable when APIs and protocol versions change.

## OpenAI

### Agents API — 2026-09-10

Source: https://openai.com/index/introducing-the-agents-api/

OpenAI describes a managed agent harness for long-running cloud agents that manages context, tool use and subagents, with infrastructure for work that can run for days, manipulate files/code, and preserve intermediate results.

Portable lesson: long-horizon reliability is a harness + state + execution-environment problem, not only a model/prompt problem.

### Agents SDK evolution — 2026-04-15

Source: https://openai.com/index/the-next-evolution-of-the-agents-sdk/

The Agents SDK added a model-native harness, controlled workspaces, native sandbox execution, snapshot/rehydration for durable execution, isolated environments and parallel work across sandboxes/containers.

Portable lessons: separate harness from compute; externalize resumable state; keep credentials out of model-generated-code environments; parallelize only across isolated, compatible work units.

### Agents SDK tracing and guardrails

Sources:
- https://openai.github.io/openai-agents-python/tracing/
- https://openai.github.io/openai-agents-python/guardrails/
- https://openai.github.io/openai-agents-python/tools/
- https://openai.github.io/openai-agents-python/mcp/

Current SDK tracing records end-to-end workflows through spans for model generations, tool calls, handoffs, guardrails and custom events. Tool guardrails can validate or block custom `FunctionTool` calls and tools converted from local MCP server objects before and after execution; blocking guardrails are materially different from parallel guardrails when side effects or cost must be prevented.

Guardrail coverage is boundary-specific. Agent-level input/output guardrails do not automatically wrap every delegated call. Handoffs use their own path, while hosted tools such as `WebSearchTool`, `FileSearchTool`, `HostedMCPTool`, `CodeInterpreterTool` and `ImageGenerationTool`, plus built-in execution tools such as `ComputerTool`, `ShellTool`, `ApplyPatchTool` and `LocalShellTool`, do not use the same local function-tool guardrail pipeline. A hosted MCP tool therefore cannot be credited with local MCP tool-guardrail coverage merely because both are called “MCP”.

Portable lessons: correlate the full trajectory rather than only final output; map every guardrail/approval to the exact execution boundary it actually controls; use blocking execution when prohibited side effects must not start before validation; never infer full-path protection from the existence of one agent-level guardrail.

## Anthropic

### Effective context engineering for AI agents — 2025-09-29

Source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

Anthropic frames context as a finite attention budget and recommends curating the smallest high-signal token set across instructions, tools, MCP, external data and history.

Portable lessons: just-in-time retrieval, compact durable notes, bounded tool context and deliberate compaction/rehydration are core long-horizon engineering mechanisms.

### Demystifying evals for AI agents — 2026-01-09

Source: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

Agent behavior spans many turns, tool calls and state changes, so one-shot output grading is insufficient.

Portable lesson: evaluate trajectories, state transitions, tool behavior and recovery in addition to final output quality.

### How we contain Claude across products — 2026-05-25

Source: https://www.anthropic.com/engineering/how-we-contain-claude

Anthropic separates failure likelihood from blast radius and describes containment through enforced environment/access boundaries rather than relying only on repeated human approval prompts.

Portable lesson: capability growth should be paired with least privilege, isolation, egress/credential boundaries and rollback/disable mechanisms.

## OWASP Agentic Security

### Memory & Context Poisoning — 2026-05-13

Source: https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/

OWASP highlights that an agent can carry untrusted content forward through persistent memory/context, turning an ordinary retrieved artifact, repository workflow or prior interaction into a cross-session prompt-injection or control-state risk.

Portable lessons: persistent memory is an authority boundary and attack surface, not merely storage. Keep provenance and trust class on durable entries; scope writes; quarantine unverified external instructions; support supersede/invalidate/expiry; and pressure-test whether poisoned or stale memory can become control state after compaction, restart or rehydration.

## Model Context Protocol

### MCP specification `2026-07-28`

Sources:
- https://modelcontextprotocol.io/specification/2026-07-28/basic/index
- https://modelcontextprotocol.io/specification/2026-07-28/server/discover
- https://blog.modelcontextprotocol.io/posts/2026-07-28/

The release introduced a stateless protocol core, Multi Round-Trip Requests, header-based routing, cacheable list results, authorization hardening, formal extensions and updated Tier-1 SDKs. The legacy `initialize`/`initialized` exchange and `Mcp-Session-Id` transport session were retired. Each request requires protocol version and client capabilities in `_meta`; `clientInfo` is optional but normally SHOULD be included unless configured otherwise, and is self-reported metadata rather than an authorization identity. Servers implementing `2026-07-28` MUST implement `server/discover`; calling it is optional for clients, which may instead issue another RPC inline and handle version errors. Streamable HTTP routing exposes `Mcp-Method` and `Mcp-Name` headers so routing/authorization assumptions can be tested explicitly rather than inferred from request bodies or sticky transport state.

### Release-candidate migration context — 2026-05-21

Source: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/

The release candidate describes the stateless core, Extensions framework, Tasks, MCP Apps, authorization changes and formal deprecation policy.

Portable lessons: fingerprint the actual protocol/SDK pair; do not assume an older handshake or hidden transport session; distinguish server conformance from optional client discovery, and validate per-request capabilities, optional client metadata, cache freshness, auth, extensions/tasks and live schema composition on the actual client/server pair. Keep application-level state and security identity explicit and separate from MCP transport or self-reported client metadata.

## OpenTelemetry

### GenAI observability — 2026-05-14

Source: https://opentelemetry.io/blog/2026/genai-observability/

OpenTelemetry demonstrates tracing model calls, tool invocations, token usage, latency and errors; detailed prompt/completion/tool content is opt-in and can contain sensitive data.

### Semantic conventions

Sources:
- https://opentelemetry.io/docs/specs/semconv/
- https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/

Semantic conventions standardize operation names and attributes for cross-stack correlation. Current documentation notes that GenAI attributes/conventions are evolving and some definitions have moved to the dedicated GenAI semantic-conventions repository.

Portable lessons: trace identity, model/tool operations, token/cost and error/latency metadata by default; treat raw content as sensitive opt-in telemetry; track semantic-convention version/stability instead of assuming names never change.

## Microsoft Agent Framework

### Workflow observability

Source: https://learn.microsoft.com/en-us/agent-framework/workflows/observability

Agent Framework emits workflow/session/invocation/executor/message spans, logs and metrics and can expose delivery/buffering/error state across workflow edges. Sensitive message/input/output telemetry is explicitly configurable.

Portable lesson: agent observability should cover message/executor/workflow flow, not only individual LLM calls.

## Windows desktop automation

### UI Automation screen scaling

Source: https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-screenscaling

Microsoft documents that UI Automation point/bounding-rectangle APIs operate in physical coordinates, while non-DPI-aware clients can receive or supply incompatible logical coordinates. Correct clients must account for DPI awareness and physical cursor coordinates when geometry is unavoidable.

Portable lessons: prefer semantic UIAutomation/Accessibility element identity over screen geometry; when coordinates are required, fingerprint DPI/coordinate space explicitly and never mix logical and physical coordinates silently. Verify the target window/control before and after an input action.

## Electron / Chromium desktop runtime

### Electron process model

Source: https://www.electronjs.org/docs/latest/tutorial/process-model

Electron inherits Chromium's multi-process architecture. A single main process manages application lifecycle and windows; each BrowserWindow/web embed can have its own renderer, and applications may also create utility processes.

### Runtime process evidence

Sources:
- https://www.electronjs.org/docs/latest/api/process
- https://www.electronjs.org/docs/latest/api/structures/render-process-gone-details

Electron exposes process type, creation time, uptime, CPU and memory information, while renderer termination reasons distinguish clean exit, abnormal exit, killed, crash, OOM, launch failure, integrity failure and memory eviction.

Portable lessons: process count alone is not leak evidence. Diagnose role, parentage/ownership, creation/restart timeline, resource trajectory and explicit crash/exit reasons before classifying renderer churn, orphaning or crash loops.

## Cross-source synthesis

The primary sources converge on a production-agent architecture with these independent engineering concerns:

1. durable harness and externalized resumable state;
2. finite context/attention budgeting;
3. trajectory-level evaluation;
4. end-to-end observability across model/tool/workflow/runtime/UI layers;
5. explicit concurrency/backpressure and isolation;
6. live tool/protocol contract testing with boundary-specific guardrail coverage;
7. containment and blast-radius control;
8. exact source→artifact→runtime identity and release verification;
9. semantic-first desktop automation with explicit coordinate-space handling;
10. lifecycle-aware Electron/Chromium process forensics;
11. protocol-version-aware MCP bridge recovery with explicit application state;
12. provenance-aware durable memory that resists stale or poisoned context becoming control authority.

## Invalidation rule

Before relying on a product-specific API, lifecycle, semantic-convention name, SDK feature, guardrail pipeline, tool family or protocol behavior, re-check the current primary source whenever the provider, protocol, SDK, host, model or runtime version materially changes. The portable engineering mechanism may survive while the named interface does not.
