# AI Runtime Specialist Sources — 2026-09

Status: `CURRENT RESEARCH INPUT / NOT HOST-LIVE PROOF`

| Domain | Current anchor | Specialist lesson |
|---|---|---|
| Electron process model | https://www.electronjs.org/docs/latest/tutorial/process-model | Main, renderer, GPU/utility and other child processes are expected architectural roles; count alone does not prove zombie/leak/crash loop. |
| Microsoft UI Automation screen scaling | https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-screenscaling | UI Automation coordinate APIs use physical coordinates; DPI virtualization can create physical/logical coordinate mismatches in non-aware clients. |
| Playwright locators/actionability | https://playwright.dev/docs/locators | Semantic targeting and condition/actionability checks are more robust than pixel geometry and fixed sleeps; the principle transfers to desktop accessibility automation. |
| MCP 2026-07-28 | https://blog.modelcontextprotocol.io/posts/2026-07-28/ | Current MCP evolves toward stateless request/response semantics, stronger authorization, extensions and task support; diagnose the actual client/server revision and lifecycle instead of assuming old session behavior. |
| OpenAI Agents SDK tracing | https://openai.github.io/openai-agents-python/tracing/ | Correlate model, tool, handoff and custom runtime events in one trace; interleaved process/tool logs without run identity are weak causal evidence. |
| OpenTelemetry semantic conventions | https://opentelemetry.io/docs/specs/semconv/ | Stable operation/span/metric semantics make cross-process and cross-runtime evidence comparable. |

## Synthesis

### Electron / Chromium

A correct investigation distinguishes architecture from pathology. Strong evidence for pathology is longitudinal: orphaning, repeated same-role recreation, monotonic resource growth under comparable workload, crash/termination evidence, or a causal correlation between renderer lifecycle and the user-visible symptom.

### Desktop UI automation

Treat target identity, accessibility semantics, coordinate space, focus/input ownership and transition timing as independent dimensions. A healthy recovery guard needs hysteresis, cooldown, transition suppression and action receipts because the repair mechanism itself can become a source of renderer churn or user-input loss.

### MCP / bridges

Separate `configured`, `process alive`, `transport reachable`, `protocol handshake`, `authorized`, `tool discovered`, `representative invocation`, and `observable effect`. Recovery must be idempotent and must revalidate identity/affinity after restart or reconnect.

Re-check source versions before using version-specific claims in a host-live incident.
