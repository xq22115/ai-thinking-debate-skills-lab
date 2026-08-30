---
name: tool-acquisition-resilience
description: Use when Antigravity needs an additional tool, MCP capability, skill, CLI or adapter and discovery/installation may fail, drift or falsely appear complete.
---

# Tool Acquisition Resilience

## Purpose
Acquire the minimum verified executable capability needed for acceptance, not the largest catalog of installed tools.

## Activate when
Use for missing capabilities, stalled tool discovery, unreliable installs, MCP/tool substitution, source acquisition or first-route failure.

## Do not activate
Do not install tools when existing authorized capabilities already close the acceptance criteria.

## Antigravity-native execution
Track candidates as `DISCOVERED -> FETCHED -> CONFIGURED -> INSTALLED -> LOADABLE -> INVOKABLE -> VERIFIED`; also allow `DEGRADED`, `SIMULATED`, `FAILED`. Search current workspace first, then registries/upstreams/equivalent mechanisms/minimal adapters. Keep source identity and credentials separate.

## Workflow
1. Translate acceptance tests into capability intents.
2. Inventory existing tools/skills/MCP.
3. Discover candidates by capability, not product name alone.
4. Inspect license, scripts, secret/network behavior and rollback.
5. Pin source to immutable revision when drift matters.
6. Install/configure narrowly, invoke, then run task-relevant smoke test.
7. On failure, freeze the failed route and choose a causally independent candidate.

## Validation
Configured/install success is not usability. Every promoted capability must reach `VERIFIED` or be labeled with its true state.

## Boundaries
Never execute unreviewed third-party code solely because it ranked highly. Do not use acquisition to bypass host/provider access controls.