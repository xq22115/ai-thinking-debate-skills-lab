# 2026-06 to 2026-08 Agent Control Plane Design Basis

## Scope

This note records the engineering patterns used to design `ai-system/control-plane/`. It is a design-basis document, not evidence that the repository can force ChatGPT product-level routing or that ten independent agents executed.

## Cross-source patterns

### 1. Isolate work before increasing autonomy

Across current coding-agent systems, concurrency is increasingly handled with separate environments, VMs, branches, or worktrees rather than several agents sharing one mutable checkout. The control plane therefore forbids concurrent writers on one branch and gives each chat/run/agent its own namespace.

Representative 2026 sources reviewed include GitHub Desktop worktrees (2026-06-26), Cursor cloud-agent environments and dedicated machines (2026-06/07), AWS AgentCore isolated microVM patterns (2026-06/07), Docker agent isolation guidance (2026-06/07), and Google Antigravity/Agent Factory orchestration material (2026-06).

### 2. Make the task tracker the durable control record

GitHub Issues, Jira work items, Linear workspace objects, and GitLab lifecycle context are repeatedly used as stable task/context anchors around otherwise ephemeral agent sessions. For this repository a GitHub Issue is the task system of record, while chat text remains transient input.

Representative sources reviewed include GitHub issue automation controls (2026-07-23), Linear agent/coding-session material (2026-06/07), Atlassian Jira-to-agent handoff patterns (2026-06/07), and GitLab agentic lifecycle/orchestration material (2026-06/07).

### 3. Separate cognition from deterministic controls

Model reasoning can be flexible; identity, permissions, branch/ref selection, writes, tests, and merge decisions should be deterministic and auditable. This repository places those deterministic contracts in JSON/YAML, Git refs, CI, and PRs instead of relying on a giant prompt.

Representative sources reviewed include GitHub Agentic Workflows (2026-06-11), Vercel Agent/AI SDK workflow patterns (2026-06/07), Sourcegraph agentic batch/orchestrator patterns (2026-06/07), and AWS AgentCore identity/observability guidance (2026-06/07).

### 4. Keep credentials outside the agent's cognitive context

Modern agent platforms increasingly inject scoped credentials at tool/runtime boundaries and isolate execution rather than exposing broad, long-lived secrets to prompts or agent memory. This design therefore forbids secrets in Git, defaults tool access to read-only, and requires task-scoped explicit writes.

Representative sources reviewed include Vercel Agent Stack (2026-06-17), Docker secure-agent guidance (2026-06/07), GitHub Actions security changes (2026-06/07), and GitLab governance material (2026-06/07).

### 5. Treat observability and evaluation as part of the product

Traces, tool calls, intermediate state, eval datasets, and durable run records are becoming first-class engineering surfaces. The repository therefore uses namespaced receipts, exact SHAs, workflow logs, negative tests, and explicit PASS/VETO/BLOCKED semantics.

Representative sources reviewed include Braintrust agent evaluation/observability (2026-06), Honeycomb Agent Timeline/OpenTelemetry material (2026-06), Datadog coding-agent/agent-observability material (2026-06), and Arize self-improving agent workflows (2026-06).

### 6. Fan out freely; fan in through governed review

Parallel agents are useful only if integration is controlled. Current practices use draft PRs, CI gates, risk routing, policy checks, and staged integration. This repository implements ten independent lane contracts and a fail-closed aggregate gate, but does not equate those static lanes with ten independent model executions.

## Repository consequences

- `AGENTS.md` remains the root behavior contract.
- `ai-system/registry.yml` is the discovery index.
- `ai-system/control-plane/registry.json` defines machine-readable task/run/branch invariants.
- GitHub Issues are the durable task ledger.
- Unique refs/worktrees are the concurrency boundary.
- Per-agent receipts are append-only evidence.
- Pull requests are the fan-in mechanism.
- GitHub Actions validates deterministic contracts on an exact revision.
- Independent-agent execution must produce independent receipts; role files and CI matrix entries alone are not enough.
