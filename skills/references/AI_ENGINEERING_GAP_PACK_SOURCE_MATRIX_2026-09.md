# AI Engineering Gap Pack — Current Source Matrix (2026-09)

Purpose: separate current product/framework facts from portable engineering mechanisms. Source freshness does not replace target-runtime verification.

| Domain | Current primary / high-authority anchor | Engineering lesson |
|---|---|---|
| OpenAI Agents SDK context | https://openai.github.io/openai-agents-python/context/ | Keep local application/runtime context separate from model-visible context; derived wrappers in a run share underlying app context unless explicitly isolated. |
| OpenAI Agents SDK sessions | https://openai.github.io/openai-agents-python/sessions/ | Session history is durable conversation state, not a substitute for explicit runtime identity or acceptance state; resumed runs need the same intended session/storage identity. |
| OpenAI Agents SDK usage | https://openai.github.io/openai-agents-python/usage/ | Track usage per run/stage; previous session history can increase later input token use even when usage is reported per run. |
| OpenAI Agents SDK tracing | https://openai.github.io/openai-agents-python/tracing/ | One workflow trace can correlate generations, tools, handoffs, guardrails, and custom events; concurrency needs trace/span identity rather than interleaved logs. |
| OpenAI API rate-limit guidance | https://help.openai.com/en/articles/5955604 | Honor `Retry-After` when available; otherwise use bounded exponential backoff with jitter. Failed requests can consume limits, so uncontrolled retries worsen overload. |
| OpenAI Responses service tier | https://developers.openai.com/api/reference/cli/resources/responses/methods/create | Processing tier is a serving/latency/cost control and must be tracked separately from model identity/capability. |
| Anthropic context engineering | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Treat context as a finite attention budget; use progressive disclosure, compaction, structured notes, and focused subagents rather than dumping all history/tools into every turn. |
| Anthropic long-running harness | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Long tasks need durable progress artifacts and clean incremental handoffs; compaction alone does not prevent premature completion or half-finished state. |
| Anthropic tool engineering | https://www.anthropic.com/engineering/writing-tools-for-agents | Tool quality needs agent-facing evals, clear namespacing, deliberate boundaries, and measured iteration rather than schema generation alone. |
| MCP 2026-07-28 | https://blog.modelcontextprotocol.io/posts/2026-07-28/ | Diagnose actual MCP revision and lifecycle semantics; modern MCP moves toward stateless request/response, stronger authorization, extensions, and task support. |
| Microsoft UI Automation scaling | https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-screenscaling | UIA coordinates are physical; DPI-virtualized/logical coordinate mixing can generate false geometric misses. |
| Electron process model | https://www.electronjs.org/docs/latest/tutorial/process-model | Multiple renderer/utility processes are architectural; process count alone cannot establish zombies, leaks, or crash loops. |
| Playwright locators | https://playwright.dev/docs/locators | Prefer semantic selectors plus condition/actionability checks over pixel geometry and fixed sleeps. |
| GitHub Actions deployment controls | https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments | Environment protection and deployment concurrency make release ordering/approval explicit; release serialization is a runtime correctness tool, not only CI configuration. |
| GitHub Actions secure use | https://docs.github.com/en/actions/reference/security/secure-use | Immutable full commit SHAs reduce dependency drift for third-party Actions where reproducibility/security matters. |
| OpenTelemetry semantic conventions | https://opentelemetry.io/docs/specs/semconv/ | Prefer shared trace/metric/log semantics so multi-runtime evidence can be correlated instead of becoming incompatible local logs. |

## Portable synthesis

1. **Bound concurrency at the bottleneck.** Worker count is not a universal throughput knob; queue age, retries, tail latency, and side effects reveal overload earlier than raw utilization alone.
2. **Externalize long-horizon truth.** Goal, evidence, exact identities, unsafe-to-repeat actions, and acceptance state belong in durable structured state; model context should contain only the current working set.
3. **Release identity must be end-to-end.** Source SHA, artifact digest/version, installed revision, host configuration, permission scope, and behavioral revision are different identities.
4. **Tool contracts include lifecycle and effects.** Schema validity is only one layer; retries, timeouts, pagination, auth, partial success, idempotency, and postconditions require tests.
5. **Routing is a constrained optimization problem.** Hard capability/quality constraints filter candidate routes before cost/latency optimization; model/service-tier/provider changes need protected evals.
6. **Observability is causal infrastructure.** Trace IDs, target identity, retry relations, and exact versions let operators distinguish model failure, tool failure, infrastructure failure, and stale-state failure.
7. **Progressive disclosure beats global prompt inflation.** Load only the skill, evidence, and tool surface needed for the current decision.

Status: `CURRENT-SOURCE RESEARCH / HOST-LIVE EFFECT NOT PRECLAIMED`.
