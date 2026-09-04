# Skills Catalog

## Canonical orchestration plugin

### ai-efficiency-operating-system — `1.3.0`

Canonical path: `plugins/ai-efficiency-operating-system/`.

Version 1.3 routes through **Task Goal Intelligence 4.0 Native** while preserving the v2/v2.2/v3 semantic protections. The goal capability is now a native harness package rather than one large prompt: host-neutral spec, thin implicit router, runtime preamble, phase machine, progressive references, executable state oracle, fresh verification and recovery, plus a pressure holdout for hosted behavior.

### Native Task Goal configuration

Machine profile: `plugins/ai-efficiency-operating-system/native-goal-harness.json`.

State flow:

`ORIENT → DISCRIMINATE → COMMIT → EXECUTE → VERIFY → LEARN`

`RECOVER` can interrupt material work. Task-path complexity ratchets `DIRECT → INVESTIGATIVE → ARCHITECTURAL`; it cannot be downgraded merely to escape evidence, verification or blockers.

The runtime package is deliberately split:

- `SKILL.md` — thin routing surface;
- `references/phase-machine.md` — phase gates / recovery;
- `references/runtime-preamble.md` — machine status protocol / degraded mode;
- `references/evidence-and-optimization.md` — root cause, verification, rare evidence and failure-trace optimizer;
- `references/upstream-lock.json` — exact OpenAI Plugins, Superpowers, GStack, Anthropic Skills and DSPy/GEPA revisions;
- `scripts/goal_skill_start.py` — executable `GOAL_*`/`GATE_*` preamble;
- `scripts/quick_validate.py` — package-local conformance check;
- `spec/task-goal-intelligence-spec.md` — host-neutral spec;
- `evals/task-goal-native-state-cases.jsonl` — 30 executable state/gate cases;
- `evals/task-goal-native-pressure-holdout.jsonl` — 24 hosted pressure cases; packaging is verified, HOST_LIVE pass is not preclaimed.

### Core durability rules

- current owning evidence outranks stale historical completion prose;
- corrections invalidate dependent downstream work while preserving unaffected evidence;
- wording loopholes, examples, named tools and route-local blockers cannot silently shrink the end state;
- one blocked slice does not justify abandoning separable work;
- activity volume is not progress; progress requires acceptance/evidence/uncertainty/state delta;
- two no-delta material steps force a causal route pivot;
- three materially distinct failed repairs to one mechanism force architectural review;
- completion requires fresh reverse-walk evidence: `claim → acceptance test → owning evidence → current goal version → causal path`;
- anonymous/opaque/underground/onion signals begin as provenance-bearing leads, never facts from rarity alone;
- optimizer promotion requires target + protection + holdout + adversarial slices, and hard-slice regression vetoes aggregate gains.

### Default implicit skills

| Skill | Trigger owner |
|---|---|
| `task-goal-intelligence` | native goal preamble, phase routing, semantic delta, anti-minimization, recovery, progress and verification entry |
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

Prefer one semantic owner, thin runtime routers, progressive disclosure, executable machine checks, hard-negative/pressure holdouts and current owning evidence. A skill change is not promoted because it reads well; preserve failing behavior, test the repair, run target/protection/holdout/adversarial regressions and keep rollback.

## Completion truth

`PACKAGED != HOST_LIVE`.

`CONNECTED != INVOKABLE != EFFECTIVE != VERIFIED`.

A GitHub write, marketplace manifest, CI pass, plugin listing or available connector cannot prove the intended hosted surface loaded and exercised the exact revision. Host-live acceptance requires owning-surface discovery/load, implicit routing, pressure cases, fallback and postcondition evidence.
