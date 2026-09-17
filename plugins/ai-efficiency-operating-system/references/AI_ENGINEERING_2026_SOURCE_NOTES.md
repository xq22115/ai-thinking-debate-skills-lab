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

## Model Context Protocol

### MCP specification `2026-07-28`
Source: https://blog.modelcontextprotocol.io/posts/2026-07-28/

The release introduced a stateless protocol core, Multi Round-Trip Requests, header-based routing, cacheable list results, authorization hardening, formal extensions and updated Tier-1 SDKs.

### Release-candidate migration context — 2026-05-21
Source: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/

The release candidate describes the stateless core, Extensions framework, Tasks, MCP Apps, authorization changes and formal deprecation policy.

Portable lessons: fingerprint negotiated spec/SDK/capabilities; do not assume an older stateful lifecycle; test caching, auth, extension/task semantics and live schema composition on the actual client/server pair.

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

## Cross-source synthesis

The primary sources converge on a production-agent architecture with these independent engineering concerns:

1. durable harness and externalized resumable state;
2. finite context/attention budgeting;
3. trajectory-level evaluation;
4. end-to-end observability across model/tool/workflow/runtime layers;
5. explicit concurrency/backpressure and isolation;
6. live tool/protocol contract testing;
7. containment and blast-radius control;
8. exact source→artifact→runtime identity and release verification.

## Invalidation rule

Before relying on a product-specific API, lifecycle, semantic-convention name, SDK feature or protocol behavior, re-check the current primary source whenever the provider, protocol, SDK, host, model or runtime version materially changes. The portable engineering mechanism may survive while the named interface does not.
