# 2026-08-26 Ten-Branch Synthesis — Ordinary Chat Agent Stack

## Decision
Do not replace the existing A01–A10 local agent workflow. Build a thin ordinary-chat access stack around it.

## Winning Architecture
1. **Native ChatGPT apps/plugins first** for providers they already support.
2. **Skill/CLI layer** for deterministic, high-throughput operations with low context overhead.
3. **Remote Desktop / local bridge** for authorized local read/write and launching long agent work.
4. **Existing A01–A10 runtime** for autonomous multi-step execution, preserving receipts, attestation, adjudication, freshness, and veto gates.
5. **MCP v2 gateway** for capability discovery, status, receipts, and guarded submission when the ChatGPT account/workspace exposes custom MCP.
6. **Playwright dual browser layer**: CLI/Skill by default; MCP only for persistent/interactive browser state.
7. **MCP Apps / control-plane UI** for run visualization, never as a permission bypass.
8. **Local-first scoped memory** with provenance and retention boundaries.
9. **Contract/eval gates** for routing, bridge, MCP, browser, security, and cost.

## Confirmed Existing Strengths
- Real dependency-aware A01–A10 executor and workflow.
- Separate process/session attestation.
- Receipt adjudication and finalization.
- Base freshness verification.
- PASS / FAIL / VETO / BLOCKED states.
- Existing quality-oriented GitHub Actions.
- Rich deliberation/research/evaluation skill specifications.

## Confirmed Gaps
- `control-plane/ai-system/mcp/` has no executable MCP server.
- Ordinary chat has no formal bridge to the local A01–A10 workflow.
- `chat-work-agent` is not represented in this repository.
- Remote Desktop Commander is not formally modeled as a runtime capability.
- No Playwright browser implementation/configuration in the repo.
- No MCP Apps run-status widget.
- No durable local-first project memory implementation.
- No contract tests covering the ordinary-chat capability router.

## Non-Goals
- Do not claim to disable ChatGPT sandbox/product restrictions.
- Do not expose unrestricted shell/filesystem/browser-JS as generic tools.
- Do not auto-install unvetted MCP Registry servers.
- Do not replace working local-agent governance with a popular framework for fashion alone.

## Merge Standard
The integration branch remains reviewable until static checks, policy/schema tests, MCP typecheck/tests, and secret-scan checks are green. Local runtime installation/health remains BLOCKED if the authorized remote device is offline.
