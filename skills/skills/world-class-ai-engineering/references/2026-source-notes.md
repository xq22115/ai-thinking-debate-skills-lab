# 2026 Source Notes and Invalidation Triggers

Refreshed: `2026-09-18`

These notes are not a substitute for runtime verification. They capture upstream changes that materially alter AI-engineering assumptions. Re-check the source when the invalidation trigger fires.

## Model Context Protocol — 2026-07-28

Primary sources:
- https://blog.modelcontextprotocol.io/posts/2026-07-28/
- https://blog.modelcontextprotocol.io/posts/mcp-roadmap/

Material engineering changes:
- stateless protocol core;
- optional discovery and self-describing requests;
- `Mcp-Method` / `Mcp-Name` header routing;
- cache hints for list/read results;
- extensions framework, including Tasks and MCP Apps;
- authorization hardening, including issuer validation and movement toward client metadata documents;
- formal deprecation policy.

Portable lesson: transport/session assumptions are versioned architecture, not timeless truths. Keep application state, protocol state, authorization, routing, and task lifecycle separate.

Invalidate/re-check when: MCP publishes a newer stable spec, the target SDK changes tier/version, or the host advertises different transport/auth capabilities.

## OpenAI Agents SDK — tracing, sessions, guardrails, handoffs

Primary sources:
- https://openai.github.io/openai-agents-python/
- https://openai.github.io/openai-agents-python/tracing/
- https://openai.github.io/openai-agents-python/guardrails/

Material engineering practices:
- end-to-end traces can capture model generations, tool calls, handoffs, guardrails, and custom events;
- sessions provide persistent working context;
- tool guardrails sit around custom function-tool calls and local MCP tools when configured;
- agent-level input/output guardrails do not automatically cover every delegated/tool boundary;
- parallel guardrails may allow model/tool work to begin before a tripwire completes; blocking execution changes the side-effect/cost guarantee;
- hosted/built-in tools do not necessarily share the same tool-guardrail pipeline.

Portable lesson: security and observability controls must be mapped to the actual execution boundary. “A guardrail exists” is not proof that the effectful tool path is covered.

Invalidate/re-check when: SDK major/minor behavior changes, a new tool family is used, tracing policy changes, or the target runtime has Zero Data Retention constraints.

## OpenTelemetry GenAI observability

Primary sources:
- https://opentelemetry.io/blog/2026/genai-observability/
- https://opentelemetry.io/docs/specs/otel/semantic-conventions/

Material engineering practices:
- GenAI telemetry can standardize model/token/tool/runtime observations across vendors;
- tracing/metrics/events should expose enough structure to separate model latency from tool/retry/network costs;
- semantic conventions are still versioned and may remain in development.

Portable lesson: standardize correlation and attributes, but pin the semantic-convention version and treat full prompt/tool content as opt-in because observability can become a privacy leak.

Invalidate/re-check when: semantic convention stability/status changes or attributes used by the target collector are renamed.

## Durable agent execution

Primary sources:
- https://docs.langchain.com/oss/javascript/langgraph/thinking-in-langgraph
- https://docs.temporal.io/

Material engineering practices:
- LangGraph checkpoints state at graph/node boundaries and can pause/resume through interrupts;
- smaller durable boundaries improve recovery granularity but can increase persistence overhead;
- Temporal frames long-running workflows, including AI agents, around crash/retry resilience and resumable execution.

Portable lesson: “long-running agent” requires durable state semantics, not merely a long model context. Separate checkpoint identity, idempotency, retry policy, side-effect receipts, and resume-time revalidation.

Invalidate/re-check when: the chosen workflow engine changes checkpoint/replay semantics, namespace rules, retry defaults, or persistence backend.

## Evaluation and graders

Primary sources:
- https://platform.openai.com/docs/api-reference/evals
- https://platform.openai.com/docs/api-reference/graders

Material engineering practices:
- evals can be structured as reusable datasets plus graders;
- graders can include deterministic string checks, similarity metrics, model-based labels/scores, or compositions;
- evaluator design is itself part of the system and can be gamed or biased.

Portable lesson: preserve RED baselines, hard slices, holdouts, and exact-revision evaluation. Do not promote an aggregate score when protected/adversarial cases regress.

Invalidate/re-check when: grader schema/API changes or a new evaluator model/version materially changes judgments.

## Agent security and memory/context poisoning

Primary sources:
- https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/

Material engineering risks:
- direct/indirect prompt injection;
- tool abuse and privilege escalation;
- data exfiltration;
- memory/context poisoning that persists untrusted instructions across sessions.

Portable lesson: external content is evidence/data, not authority. Persistent memory needs provenance, scope, write policy, freshness/invalidation, and isolation.

Invalidate/re-check when: OWASP Agentic guidance is revised, the memory subsystem changes, or new external-data/tool surfaces are introduced.

## Agent Skills packaging

Primary source:
- https://agentskills.io/specification

Material engineering practices:
- self-contained skill folders centered on `SKILL.md`;
- YAML frontmatter with discoverable trigger descriptions;
- progressive disclosure through references/scripts/assets rather than a monolithic always-loaded prompt.

Portable lesson: skill discovery text should describe *when to load*, while operational detail remains in the body/references. Test skills against pressure cases rather than judging prose quality.

Invalidate/re-check when: the Agent Skills specification or the owning host’s installation/discovery mechanism changes.

## Evidence hierarchy used by this pack

For a material claim, prefer the highest available evidence layer:

`owning runtime/user path > stateful postcondition read-back > exact-revision integration test > focused automated test > static/source inspection > documentation > model assertion`

Documentation can establish support semantics. It cannot prove the target runtime actually loaded, executed, persisted, or produced the requested effect.
