# 08 — Harness and ACP portability

## Verdict
Standardize portable skills/state around `AGENTS.md`, `.agents/skills`, MCP for tools, and ACP for editor↔agent sessions. Avoid binding the intelligence layer to Codex, Claude Code, Cursor, or one provider.

## Evidence
- Vercel AI SDK 7 HarnessAgent normalizes Codex, Claude Code, Pi and other harnesses behind one interface, separating harness from sandbox and runtime context.
- Open Interpreter's 2026 Rust rewrite explicitly emulates multiple harnesses and reuses `AGENTS.md`, shared `.agents/skills`, MCP, ACP, and Codex exec protocol.
- Agent Client Protocol is a dedicated standard for connecting editors to agents; its organization and SDKs remained actively updated through July 2026.

## Gap in current stack
Braintrust routes capabilities well, but there is no canonical `harness-adapter` contract covering session identity, capability discovery, permission mapping, compaction/checkpoint transfer, and exact-revision proof across harnesses.

## Recommendation
Create `harness-portability` skill/schema; treat the harness as replaceable infrastructure. Define adapters for Codex, Open Interpreter, ACP clients, and future harnesses; never encode provider-specific assumptions in acceptance criteria.

## Acceptance
The same task packet and acceptance contract can be consumed by two different harness adapters without changing the user goal or evidence schema.