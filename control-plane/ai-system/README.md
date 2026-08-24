# AI Master System

This directory is the repository-level control center for reusable AI work.

## Purpose

Keep reusable prompts, agent roles, skills, MCP integration notes, configuration, and evidence-bound completion contracts in one versioned place without mixing them into application code.

## Layout

- `agents/` — agent/router contracts and role definitions
- `skills/` — reusable capability packages and invocation notes
- `prompts/` — reusable prompt templates
- `configs/` — tool/model/workflow configuration that is safe to commit; `continuous-thinking-global.json` is the default repository-wide quality profile
- `control-plane/` — run contracts, receipts, gates, and `acceptance-contract.schema.json`
- `mcp/` — MCP server integration manifests and setup notes
- `registry.yml` — single discovery index for the above assets and quality entrypoints

## Operating model

1. Discover capabilities and the active quality profile through `registry.yml` before adding a new tool or rule.
2. Read the repository root `AGENTS.md` and `configs/continuous-thinking-global.json` for non-trivial work.
3. Convert material/critical outcomes into default-fail acceptance criteria before declaring completion.
4. Reuse an existing skill or prompt before creating a duplicate.
5. Keep secrets out of the repository; commit only examples/placeholders.
6. Validate actual behavior before marking a capability as active: `configured → registered → loaded → executed → observable effect`.
7. Prefer small, composable assets over one giant prompt.

## Machine enforcement

The deep-reasoning CI gate executes `scripts/validate_continuous_thinking_global.py` and regression tests the evidence-bound acceptance validator. This protects repository policy from silent drift, but it does not by itself prove that an external ChatGPT/IDE/SaaS consumer loaded the repository profile. Product/runtime activation must be verified at the consumer.

## Status vocabulary

Use exactly one of: `active`, `experimental`, `disabled`, `blocked`.

This layer supplements the repository's root `AGENTS.md`; it does not replace repository governance or product-level permissions/policies.
