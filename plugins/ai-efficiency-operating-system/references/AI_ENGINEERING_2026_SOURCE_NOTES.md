# AI Engineering 2026 Source Notes

Status: source-learning notes, not runtime proof.

The pack records mechanisms separately from product-specific claims so skills remain portable when APIs change.

## OpenAI

- **Agents API — 2026-09-10**  
  https://openai.com/index/introducing-the-agents-api/  
  Durable sessions, long-running cloud agents, harness-managed context/tools/subagents, persistent intermediate work, and separation between harness and compute environment.
- **Agents SDK evolution — 2026-04-15**  
  https://openai.com/index/the-next-evolution-of-the-agents-sdk/  
  Model-native harness, sandbox execution, files/commands, controlled workspaces, approvals, tracing, handoffs, resume bookkeeping, memory/compaction/skills.
- **Agents/tool orchestration bootcamp — 2026**  
  https://academy.openai.com/  
  Production primitives: tools, routing, handoffs, guardrails, tracing and evals.

Portable lessons: separate harness from execution environment; make resume state explicit; trace agent/tool loops; verify tool effects; evaluate workflows rather than only final prose.

## Anthropic

- **Effective context engineering for AI agents — 2025-09-29**  
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents  
  Context is a finite attention budget; use high-signal context, just-in-time retrieval, compaction, structured notes/memory and subagents for long horizons.
- **Demystifying evals for AI agents — 2026-01-09**  
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents  
  Agent evals must cover trajectories/tool use/state, not only one-shot outputs.
- **How we contain Claude across products — 2026-05-25**  
  https://www.anthropic.com/engineering/how-we-contain-claude  
  Agent risk depends on both failure probability and blast radius; containment boundaries must be engineered as capability grows.
- **Scaling Managed Agents — 2026-04-08**  
  https://www.anthropic.com/engineering/managed-agents  
  Harness assumptions age as models change; keep stable interfaces and periodically revalidate scaffolding.

## Model Context Protocol

- **MCP specification release `2026-07-28`**  
  https://blog.modelcontextprotocol.io/posts/2026-07-28/  
  Major changes include a stateless protocol core, multi-round-trip requests, header-based routing, cacheable list results, authorization hardening, formal extensions and updated Tier-1 SDKs.
- **Release-candidate migration notes**  
  https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/  
  Roots, Sampling and Logging are deprecated under the new lifecycle; structured observability should use OpenTelemetry where applicable; tool schemas support full JSON Schema 2020-12 features.

Portable lessons: never assume an older stateful lifecycle; fingerprint spec/SDK/schema version; test capability negotiation, task/extension semantics, auth scope, caching and schema composition on the live client/server pair.

## Observability

- **OpenTelemetry GenAI observability — 2026-05-14**  
  https://opentelemetry.io/blog/2026/genai-observability/  
  Trace model calls, tool invocations, tokens, latency and errors; content capture is opt-in because it can be sensitive.
- **OpenTelemetry semantic conventions**  
  https://opentelemetry.io/docs/specs/semconv/  
  Standardized span/metric/log naming improves cross-stack correlation; convention versions and stability status must be tracked.
- **Microsoft Agent Framework workflow observability**  
  https://learn.microsoft.com/en-us/agent-framework/workflows/observability  
  Workflow spans, message/executor flow and delivery status provide operational visibility beyond one model call.

## Invalidation rule

Before relying on a product-specific claim, re-check the current primary source if the protocol, SDK, host, model, or runtime version materially changed. The reusable skill mechanism may survive while a named API or lifecycle does not.
