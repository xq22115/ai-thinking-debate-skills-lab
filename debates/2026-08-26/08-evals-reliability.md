# Debate 08 — Evals / Reliability

## Position
The next capability increase must be measured. Preserve the repository's receipt/adjudication system and add interface-level evals around ordinary-chat routing, MCP, browser, bridge, and UI.

## Adopt
1. Keep receipt adjudication, snapshot-bound execution, base freshness, and merge-readiness gates as core evidence.
2. Add contract tests for capability discovery, routing decisions, MCP schemas, bridge preflight, status/receipt retrieval, and UI data contracts.
3. Add adversarial prompt-injection tests for browser/external content.
4. Track context/token cost, latency, retries, tool-call count, and failure recovery.
5. Add deterministic fixtures and replayable browser/API mocks before relying on live external systems.
6. Allow optional adapters to tools such as Braintrust/Promptfoo, but keep the canonical PASS/FAIL evidence in-repo.

## Reject
- Measuring only whether a model produced an answer.
- Treating a single successful manual run as reliability proof.
- Replacing existing receipts with opaque hosted dashboards.
- Auto-merging capability changes without regression gates.

## Acceptance
PASS when each capability has happy-path, unavailable-path, permission-denied, malformed-input, timeout, and adversarial-content tests, with regression thresholds recorded in CI.
