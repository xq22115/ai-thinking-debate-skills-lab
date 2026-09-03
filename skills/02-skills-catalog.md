# Skills Catalog

## Canonical orchestration plugin

### ai-efficiency-operating-system — `1.2.0`

Canonical path: `plugins/ai-efficiency-operating-system/`.

Version 1.2 connects Goal Intelligence v2 to actual skill routing. The package now uses a lightweight goal gate, phase ownership, conditional specialist auto-invocation, bounded composition, fallback/self-repair and postcondition verification. It explicitly rejects the assumption that package presence or connector visibility proves effective use.

### Default implicit skills

| Skill | Trigger owner |
|---|---|
| `task-goal-intelligence` | latent task goal, target identity, semantic delta, information-gain routing |
| `chief-of-staff-core` | complex task contract and phase routing |
| `plan-arbiter` | plan/architecture/sequence choice |
| `evidence-watchdog` | state and completion verification |
| `executive-research` | current/deep/root-cause research and evidence archaeology |
| `memory-policy` | durable memory and rehydration |
| `convergence-controller` | repeated no-progress/review loops and route change |

### Conditional implicit specialists — demand-loaded

| Skill | Specialist use |
|---|---|
| `capability-forensics` | model-vs-harness-vs-tool-vs-permission/session/entitlement/environment bottleneck diagnosis |
| `mcp-surface-engineering` | dynamic tool discovery, schema/version drift, namespace collision, entitlement/context pressure and tool-poisoning controls |
| `agent-runtime-forensics` | model/tool/process/file/network/artifact/postcondition causal evidence and replay |

These specialists are eligible for implicit invocation only after the routing eligibility layer finds material diagnostic signals. A topic noun such as “MCP” or “runtime” is insufficient by itself.

### Explicit-only skills

| Skill | Why explicit |
|---|---|
| `autonomy-contract` | authority documentation cannot create authority |
| `persistent-work-ledger` | requires real durable runtime primitives |
| `authorized-reverse-engineering` | remains intentionally scoped to authorized artifact analysis |

## Canonical combination patterns

- research-heavy → `task-goal-intelligence` + `executive-research` + `evidence-watchdog`
- capability bottleneck → `task-goal-intelligence` + `capability-forensics` + `evidence-watchdog`
- MCP/tool-surface pressure → `task-goal-intelligence` + `mcp-surface-engineering` + `evidence-watchdog`
- runtime-effect mismatch → `task-goal-intelligence` + `agent-runtime-forensics` + `evidence-watchdog`
- architecture choice → `task-goal-intelligence` + `plan-arbiter`
- repeated route failure → `task-goal-intelligence` + `convergence-controller` + `evidence-watchdog`
- cross-session context → `task-goal-intelligence` + `memory-policy`
- complex multi-stage → `task-goal-intelligence` + `chief-of-staff-core` + `evidence-watchdog`

Implicit bundles are bounded to three skills per phase. Discover many, load few.

## Portable specialist library

The following specialists remain useful as direct references or standalone skills when their narrow trigger applies. They do not compete with the canonical plugin for orchestration ownership:

- `evidence-gap-research`
- `competing-hypotheses`
- `root-cause-clustering`
- `completion-gate`
- `recoverable-state`
- `compatibility-audit`
- `multi-agent-deliberation`
- `capability-challenge`
- `durable-agent-control-plane`
- canonical full-detail `task-goal-intelligence` under `skills/skills/`

## Skill authoring rule

Prefer one semantic owner, thin `SKILL.md`, progressive disclosure, hard-negative trigger tests and deterministic checks for machine-verifiable constraints. A skill change is not promoted because it reads well; preserve a failing baseline/case, test the repair, run protection/holdout regressions and keep rollback.

Specialized skills require a no-skill or lighter-baseline counterfactual before broad promotion because relevant-looking skills can still create negative transfer or excessive procedure. Learned/semantic reranking may refine ordering only after deterministic eligibility filtering; it may not silently make explicit-only skills implicit.

## Completion truth

`PACKAGED != HOST_LIVE`.

`CONNECTED != INVOKABLE != EFFECTIVE != VERIFIED`.

A GitHub write, archive, marketplace manifest, CI pass, plugin listing or available connector cannot by itself prove the intended ChatGPT/Codex surface loaded and exercised the exact revision. Host-live acceptance requires owning-surface probes for implicit routing, hard negatives, conditional specialist activation, fallback and postcondition evidence.
