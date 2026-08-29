# Skills Catalog

## Canonical orchestration plugin

### ai-efficiency-operating-system — `1.1.0-rc1`

Canonical path: `plugins/ai-efficiency-operating-system/`.

The core remains the validated eight-skill Executive Harness topology, strengthened by Deep Task Integrity, DeepLock V2.1, ARR v1.3 and current OpenAI/Agent Skills patterns. Version 1.1 adds four **explicit-only Expert Labs** without increasing the default implicit trigger pool.

### Executive skills

| Skill | Trigger owner |
|---|---|
| `chief-of-staff-core` | complex task contract and phase routing |
| `plan-arbiter` | plan/architecture/sequence choice |
| `evidence-watchdog` | state and completion verification |
| `executive-research` | current/deep/root-cause research, including AI Ecosystem Recon reference |
| `memory-policy` | durable memory and rehydration |
| `convergence-controller` | review loops and skill evolution |
| `autonomy-contract` | explicit effect-bearing delegation |
| `persistent-work-ledger` | explicit durable runtime state on capable hosts |

The first six are eligible for implicit phase routing; the last two remain explicit-only.

### Expert Labs — explicit-only / demand-loaded

| Skill | Specialist use |
|---|---|
| `capability-forensics` | model-vs-harness-vs-tool-vs-permission/session/entitlement/environment bottleneck diagnosis |
| `mcp-surface-engineering` | dynamic tool discovery, schema/version drift, namespace collision, entitlement and tool-poisoning controls |
| `authorized-reverse-engineering` | static/dynamic analysis of authorized binaries/software with artifact/toolchain identity and evidence lineage |
| `agent-runtime-forensics` | model/tool/process/file/network/artifact/postcondition causal evidence and replay/forensic manifests |

Expert Labs are not default-enabled. Their presence is not evidence that the current host has binary-analysis runtimes, MCP servers, eBPF/OS telemetry, filesystem/terminal access, or any other external capability. They maximize authorized capability and observability and do not bypass provider safety, access controls, licensing/DRM or authorization boundaries.

Default research is adaptive and MATERIAL-DELTA-driven. Historic DeepLock numeric/time/worker thresholds are preserved only under explicit `STRICT_DEEPLOCK` acceptance profile.

The repository includes `.agents/plugins/marketplace.json` for current OpenAI GitHub marketplace import. Package presence is not host activation; live ChatGPT Desktop/Codex status requires owning-surface probe evidence.

## Portable specialist library

The following older specialists remain useful as direct references or standalone skills when their narrow trigger applies. They do not compete with the canonical plugin for orchestration ownership:

- `evidence-gap-research`
- `competing-hypotheses`
- `root-cause-clustering`
- `completion-gate`
- `recoverable-state`
- `compatibility-audit`
- `multi-agent-deliberation`
- `capability-challenge`
- `durable-agent-control-plane`

## Skill authoring rule

Prefer one semantic owner, thin `SKILL.md`, progressive disclosure, hard-negative trigger tests and deterministic checks for machine-verifiable constraints. A skill change is not promoted because it reads well; preserve a failing baseline/case, test the repair, run protection/holdout regressions and keep rollback.

Specialized skills require a no-skill or lighter-baseline counterfactual before broad promotion because relevant-looking skills can still create negative transfer or excessive procedure.

## Completion truth

`PACKAGED != HOST_LIVE`.

A GitHub write, archive, marketplace manifest, CI pass or plugin listing cannot by itself prove the intended ChatGPT/Codex surface loaded and exercised the exact revision.
