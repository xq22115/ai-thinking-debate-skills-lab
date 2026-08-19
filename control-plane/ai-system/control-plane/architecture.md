# Architecture: Multi-chat GitHub Control Plane

## Layer model

| Layer | Purpose | Mutable? | Canonical evidence |
|---|---|---:|---|
| L0 Product routing | Whether a chat chooses the GitHub connector | outside repo | tool invocation only |
| L1 Discovery | Find repository rules and capabilities | rarely | `AGENTS.md`, registries |
| L2 Task ledger | Goal, acceptance, dependencies, state | server-managed | GitHub Issue |
| L3 Run namespace | Isolate each chat/attempt | immutable identity | `issue_number + run_id + base_sha` |
| L4 Agent workspaces | Independent work per role | yes, isolated | 10 unique branches/worktrees |
| L5 Evidence | Role-specific receipts and logs | append-only | receipt path + commit/workflow log |
| L6 Verification | Deterministic and adversarial gates | regenerated | 10-lane Actions workflow |
| L7 Integration | Fan-in reviewed changes | PR-mediated | PR diff, checks, reviews |
| L8 Promotion | Merge to main | single-writer | merge SHA + required checks |

## Branch topology

```text
main
└─ task/<issue>/integration
   ├─ agent/<issue>/A01/<run>
   ├─ agent/<issue>/A02/<run>
   ├─ agent/<issue>/A03/<run>
   ├─ agent/<issue>/A04/<run>
   ├─ agent/<issue>/A05/<run>
   ├─ agent/<issue>/A06/<run>
   ├─ agent/<issue>/A07/<run>
   ├─ agent/<issue>/A08/<run>
   ├─ agent/<issue>/A09/<run>
   └─ agent/<issue>/A10/<run>
```

A chat that is not participating in the full ten-agent fan-out uses `chat/<issue>/<run>` instead. It still gets a unique branch and still integrates by PR.

## Conflict prevention

The primary defense is **structural** rather than conversational. Two writers never share a branch. If two chats touch the same logical file, they do so on different refs; Git/PR comparison exposes the conflict at fan-in. Existing-file mutations additionally require the current blob SHA, so stale writes fail instead of silently overwriting newer state.

Run evidence is sharded by task/run/agent. A single shared JSON ledger would become a write hotspot, so the GitHub Issue is the mutable task record and receipts are append-only files or workflow logs.

## Advanced operating pattern

Use a two-speed system: agents get broad freedom inside disposable/isolated workspaces, while the control plane stays narrow and hard-gated. Keep cognition nondeterministic but make identity, permissions, branch creation, file mutation, tests, and merge deterministic. Feed observed failures back into skills/evals through PRs rather than letting an agent mutate its own governing policy mid-run.
