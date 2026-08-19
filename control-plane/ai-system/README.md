# AI Master System

This directory is the repository-level control center for reusable AI work.

## Purpose

Keep reusable prompts, agent roles, skills, MCP integration notes, and configuration in one versioned place without mixing them into application code.

## Layout

- `agents/` — agent/router contracts and role definitions
- `skills/` — reusable capability packages and invocation notes
- `prompts/` — reusable prompt templates
- `configs/` — tool/model/workflow configuration that is safe to commit
- `mcp/` — MCP server integration manifests and setup notes
- `registry.yml` — single discovery index for the above assets

## Operating model

1. Discover capabilities through `registry.yml` before adding a new tool.
2. Reuse an existing skill or prompt before creating a duplicate.
3. Keep secrets out of the repository; commit only examples/placeholders.
4. Validate actual behavior before marking a capability as active.
5. Prefer small, composable assets over one giant prompt.

## Status vocabulary

Use exactly one of: `active`, `experimental`, `disabled`, `blocked`.

This layer supplements the repository's root `AGENTS.md`; it does not replace repository governance or product-level permissions/policies.
