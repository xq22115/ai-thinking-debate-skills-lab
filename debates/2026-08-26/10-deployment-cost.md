# Debate 10 — Deployment / Cost

## Position
Use a free-first local architecture, but do not trade away trust or reliability for a random free hosted service.

## Adopt
1. Local agent runtime remains local and uses the already-authorized Remote Desktop/bridge when the device is online.
2. Stateless MCP gateway can run on a small HTTPS-capable host only when ChatGPT/product support requires a remote endpoint.
3. Prefer low-cost/free tiers for stateless routing, health, and UI; keep credentials and local filesystem execution off the public gateway.
4. GitHub Actions remains the canonical CI gate for code/config changes.
5. Support Docker/Compose for portable self-hosting and easy rollback.
6. Keep browser profiles and durable memory local by default.
7. Use Secure MCP Tunnel only on accounts/workspaces where OpenAI exposes it; do not claim it is universally available.

## Reject
- Publicly exposing a local shell/agent executor to save setup effort.
- Permanent paid infrastructure for workloads that can sleep or run locally.
- Free hosted MCP servers with unknown code/data policies.
- Treating a GitHub repository as a mechanism to bypass ChatGPT plan gates.

## Acceptance
PASS when the ordinary-chat path works locally with zero additional recurring infrastructure cost where possible, the remote layer is stateless and replaceable, secrets remain outside Git, and the system has a documented rollback/offline mode.
