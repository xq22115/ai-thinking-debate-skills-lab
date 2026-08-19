# Reference Architecture — Evidence-Gated Deliberation & Skills OS

```text
USER INTENT
  ↓
INTAKE / ACCEPTANCE CONTRACT
  ↓
EVIDENCE GAP ENGINE
  ↓
DELIBERATION ROUTER
  ├─ independent hypotheses
  ├─ specialist roles
  ├─ red team / falsifier
  └─ selective disagreement exchange
  ↓
PLAN / PRECHECK
  ├─ compatibility
  ├─ permissions
  ├─ security
  └─ rollback
  ↓
EXECUTION HARNESS
  ├─ sandbox/tool boundary
  ├─ skill loader
  ├─ deterministic action layer
  └─ durable task state
  ↓
OBSERVE / EVAL
  ├─ tests
  ├─ traces
  ├─ receipts
  └─ counterexample checks
  ↓
COMPLETION GATE
  ↓
CHECKPOINT / ARCHIVE / DEPLOY
```

## State machine

`INTAKE → DISCOVER → REPRODUCE → DIAGNOSE → PLAN → PRECHECK → SANDBOX_APPLY → OBSERVE → VERIFY → RED_TEAM → SELECT → COMMIT`

Failure transitions: `ROLLBACK`, `REPLAN`, `HALT_WITH_EVIDENCE`.

## Status vocabulary

Never collapse these states:
`DRAFTED`, `PACKAGED`, `STATIC_VALIDATED`, `TESTED`, `REVIEWED`, `VERIFIED`, `HOST_LIVE_UNVERIFIED`, `HOST_LIVE_VERIFIED`, `DEPLOYED`, `HEALTHY`.

## Debate routing

Use more roles when uncertainty, conflicting evidence, impact, irreversibility, cross-platform compatibility, or security risk is high. Use fewer roles for deterministic low-risk work with obvious acceptance tests.

## Anti-fake-completion gate
A task may declare `VERIFIED` only when all critical acceptance conditions have target-bound evidence, no blocking red-team finding remains, no critical unknown was closed without evidence, regression scope was checked, and the status label exactly matches what was tested.

## Compatibility adapter layer
Do not assume one skill format is natively portable everywhere. Keep a portable procedural core and host adapters for OpenAI/ChatGPT/Agents SDK, Claude/Claude Code/Agent Skills, MCP, OpenClaw, IDE agents, Windows, and macOS.
