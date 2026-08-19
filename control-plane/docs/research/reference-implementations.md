# Verified reference implementations

This index contains repositories that were directly resolved through the GitHub connector during issue #27. Presence here means the repository exists and was readable; it does **not** mean its design is copied wholesale or that every capability is enabled in this repository.

| Repository | Why it matters to this control plane | Adoption note |
|---|---|---|
| `openai/symphony` | Issue-tracker-as-control-plane, isolated per-issue workspaces, repository-owned workflow policy, bounded concurrency, retries/reconciliation, structured observability, proof-of-work before landing. | Primary architecture reference; adapt concepts, not product-specific assumptions. |
| `github/gh-aw` | GitHub-native Agentic Workflows; useful reference for safe outputs, Actions integration, repository-level agent workflows, and governance around autonomous work. | Prefer GitHub-native primitives when they solve the problem cleanly. |
| `github/gh-aw-firewall` | Execution/network firewall component associated with GitHub Agentic Workflows. | Reference for enforcing runtime boundaries outside the prompt. |
| `github/github-mcp-server` | Official GitHub MCP server implementation. | Reference for tool-surface design and GitHub capability exposure; do not assume MCP is required for every chat. |
| `microsoft/agent-framework` | Microsoft agent framework for orchestration/runtime patterns. | Useful comparison for framework-agnostic runtime contracts and observability. |
| `aws/bedrock-agentcore-starter-toolkit` | AWS AgentCore starter toolkit. | Reference for runtime identity, isolated execution, deployment and operational controls. |
| `google/adk-python` | Google's Agent Development Kit for Python. | Reference for agent composition, workflow/agent abstractions, and lifecycle tooling. |

## Design rule

Use these repositories as falsifiable implementation references: read the exact file/commit needed for a concrete decision, record the revision, and test the adapted behavior locally or in CI. Do not treat stars, brand reputation, or a README claim as completion evidence.
