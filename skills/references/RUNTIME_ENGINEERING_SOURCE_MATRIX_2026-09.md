# Runtime Engineering Source Matrix — 2026-09

Purpose: current primary/near-primary anchors for the Runtime Engineering Pack. These are research inputs, not substitutes for target-runtime verification.

| Domain | Current anchor | Portable engineering lesson | Re-evaluate when |
|---|---|---|---|
| OpenAI agent tracing | https://openai.github.io/openai-agents-python/tracing/ | Trace the whole workflow; model generations, tools, handoffs, guardrails, and custom events are distinct spans/events. | SDK tracing model or retention behavior changes. |
| OpenAI guardrails | https://openai.github.io/openai-agents-python/guardrails/ | Input/output/tool boundaries differ; a guardrail attached at one boundary does not automatically protect every downstream tool or agent. | SDK guardrail execution semantics change. |
| MCP | https://blog.modelcontextprotocol.io/posts/2026-07-28/ | MCP 2026-07-28 introduces a stateless core, stronger authorization, routing/extensions, and long-running task capabilities; diagnose actual client/server version instead of assuming old stateful semantics. | A newer MCP spec is released. |
| A2A | https://a2a-protocol.org/v1.0.0/ | Treat agent-to-agent interoperability separately from agent-to-tool MCP; capability discovery, task management, and secure exchange do not imply shared internal state. | A2A release changes wire/task semantics. |
| OpenTelemetry | https://opentelemetry.io/docs/specs/semconv/ | Use shared span/metric/log semantics and stable operation naming; telemetry schemas should remain correlatable across languages and runtimes. | Semantic convention stability/version changes. |
| OpenTelemetry GenAI attributes | https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/ | Prompt/output content can contain sensitive data; content capture should be filtered, bounded, or opt-in rather than default telemetry. | GenAI conventions change. |
| Electron process model | https://www.electronjs.org/docs/latest/tutorial/process-model | Main, renderer, GPU/utility and other child processes are architectural; process count alone is not evidence of zombies or leaks. | Electron/Chromium process architecture materially changes. |
| Microsoft UI Automation scaling | https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-screenscaling | UI Automation coordinate APIs use physical coordinates; non-DPI-aware clients can miscompare physical and logical coordinates. | Windows UIA/DPI APIs change. |
| Playwright locators | https://playwright.dev/docs/locators | Prefer semantic locators and auto-waiting/retryable conditions over brittle geometry and fixed sleeps. | Locator/actionability semantics change. |
| GitHub Actions secure use | https://docs.github.com/en/actions/reference/security/secure-use | Pin third-party Actions to full commit SHAs when immutability matters; do not treat moving tags as reproducible dependencies. | GitHub immutable-action or policy model changes. |
| GitHub OIDC | https://docs.github.com/en/actions/reference/security/oidc | Prefer short-lived federated identity over long-lived deployment secrets; bind trust to predictable repository/workflow claims. | OIDC claim formats/trust guidance change. |
| Anthropic agent evals | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Multi-step agents require trajectory-aware evals combining deterministic checks, graders, task outcomes, and real failure cases. | New empirical guidance supersedes this. |
| LangGraph durability | https://reference.langchain.com/python/langgraph/types/Durability | Durable execution requires explicit persistence tradeoffs; side effects and nondeterminism need replay-safe/idempotent handling. | LangGraph persistence/replay semantics change. |

## Cross-source synthesis

1. **Runtime truth dominates configuration truth.** Every framework exposes layers where a component can be configured yet not executed or observable.
2. **State has ownership and lifetime.** Agent task state, protocol session state, process state, UI element handles, and browser/profile state should not be conflated.
3. **Recovery must be replay-safe.** Long-running agents and bridges need idempotent side effects, checkpoints, and target revalidation after reconnect/restart.
4. **Observability must preserve causality.** A useful trace ties retries, handoffs, tool calls, target identity, versions, and verification to one run rather than collecting unrelated logs.
5. **Selectors and identities should be semantic before geometric/nominative.** UI roles, process lineage, account/profile aliases, immutable revisions, and stable IDs outperform friendly names and pixel positions.
6. **Security and reliability share a boundary discipline.** Authorization, target identity, immutable dependencies, and least-privilege credentials prevent both security failures and wrong-target operational failures.
7. **Evaluation must contain real failure distributions.** Synthetic happy paths cannot catch session pollution, stale state, renderer churn, wrong endpoint probes, focus races, or recovery loops.

Status: `SOURCE_MATRIX_ONLY`. Every version-sensitive claim must be checked against the target implementation before a host-live `PASS`.
