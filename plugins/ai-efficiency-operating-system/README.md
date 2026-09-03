# AI Efficiency Operating System — 2026 Native Plugin

Status: **v1.2 package candidate / host-live auto-invocation not yet proven on every owning surface**.

This is the canonical orchestration plugin for goal-aware routing, deep research, capability diagnosis and verified execution. It does not treat `installed`, `connected`, `invokable`, `effective`, and `verified` as the same state.

## v1.2 routing architecture

The runtime-facing design combines a deterministic eligibility baseline with demand-loaded specialist routing:

1. **Task Goal Intelligence gate** — recover the active goal, target identity, hard constraints, acceptance tests and decision-critical unknowns before material work.
2. **Phase owner** — choose the smallest executive skill that owns the current phase.
3. **Conditional specialist escalation** — capability, MCP/tool-surface and runtime-effect specialists may be invoked implicitly only when their diagnostic signals are materially present.
4. **Bounded composition** — at most three implicit skills per phase; discover many, load few.
5. **Fallback/self-repair** — a failed route does not change the root goal; retry once without new evidence, then change method/specialist and preserve acceptance criteria.
6. **Postcondition proof** — a returned tool success or written config is not completion without the intended state/read-back.

A host may add semantic/learned reranking after the deterministic eligibility filter. The deterministic layer stays canonical for regression tests, hard negatives and rollback.

## Default implicit skills

| Skill | Primary ownership |
|---|---|
| `task-goal-intelligence` | goal interpretation, semantic delta, information-gain routing |
| `chief-of-staff-core` | complex task contract and phase ownership |
| `plan-arbiter` | plan/architecture/sequence choice |
| `evidence-watchdog` | completion claims, postconditions and read-back |
| `executive-research` | current/deep/root-cause research and evidence archaeology |
| `memory-policy` | durable context and rehydration |
| `convergence-controller` | repeated failure/review loops and materially different route selection |

## Conditional implicit specialists

These are **not globally always-on**. They are demand-loaded when multiple task signals pass the eligibility gate.

| Skill | Auto-invoke trigger |
|---|---|
| `capability-forensics` | capability differs by model/harness/session/account/surface, or the limiting layer is unclear |
| `mcp-surface-engineering` | many/changing/conflicting tools, MCP schema drift, dynamic discovery, entitlement/context/namespace pressure |
| `agent-runtime-forensics` | a tool/process claims success while file/process/network/artifact/postcondition state is missing or causally unclear |

This directly implements the rule **connected ≠ invokable ≠ effective ≠ verified**.

## Explicit-only skills

| Skill | Why explicit |
|---|---|
| `autonomy-contract` | records authority for effect-bearing delegation; skill text cannot create authority |
| `persistent-work-ledger` | requires actual filesystem/durable-state primitives |
| `authorized-reverse-engineering` | specialist analysis must remain intentionally scoped to authorized artifacts |

## High-value combinations

- complex research → `task-goal-intelligence` + `executive-research` + `evidence-watchdog`
- capability bottleneck → `task-goal-intelligence` + `capability-forensics` + `evidence-watchdog`
- large MCP/tool surface → `task-goal-intelligence` + `mcp-surface-engineering` + `evidence-watchdog`
- runtime effect mismatch → `task-goal-intelligence` + `agent-runtime-forensics` + `evidence-watchdog`
- architecture choice → `task-goal-intelligence` + `plan-arbiter`
- repeated no-progress route → `task-goal-intelligence` + `convergence-controller` + `evidence-watchdog`
- cross-session context → `task-goal-intelligence` + `memory-policy`
- complex multi-stage task → `task-goal-intelligence` + `chief-of-staff-core` + `evidence-watchdog`

## Deep-use rule

A skill activation is not success. For material investigations, the specialist must read its required references and use its mechanism-specific workflow:

- capability-forensics uses the `DECLARED → VISIBLE → AUTHORIZED → LOADABLE → INVOKABLE → EFFECTIVE → VERIFIED` truth ladder and differential probes;
- MCP surface engineering fingerprints live namespace/schema/entitlement/session state and prefers lazy/dynamic discovery when eager schemas create cost or collisions;
- runtime forensics reconstructs causal evidence from intent/tool/process/file/network/artifact/postcondition planes;
- executive research must produce material decision delta, not merely more links.

## Research and world-class patterns

The architecture follows a synthesis rather than one framework copy: constrained candidate selection/hand-off patterns, conditional tool nodes, dynamic tool discovery, semantic routing after eligibility filtering, negative-routing tests, fallback graphs, held-out promotion gates and postcondition verification. External 2026 references remain in `references/2026-baseline.md`.

Default research is adaptive and MATERIAL-DELTA driven. Historic numeric/time/worker thresholds survive only under explicit `STRICT_DEEPLOCK`; they are not a universal definition of depth.

## Desktop / Codex distribution

The repository contains `.agents/plugins/marketplace.json`. The package is skill-only and does not itself grant filesystem, terminal, MCP server, background daemon, browser-control or other host primitives.

`PACKAGED != HOST_LIVE`. An owning ChatGPT/Codex surface must import/sync this exact revision and demonstrate fresh-session discovery, positive implicit routing, hard-negative routing, conditional specialist activation, fallback behavior and postcondition evidence before that surface is called `HOST_LIVE`.

## Tests and promotion

The package uses deterministic routing, behavior, specialist and composition/fallback regression corpora. A v1.2 promotion requires:

- package/metadata/schema validation;
- primary routing corpus PASS;
- composition + fallback corpus PASS;
- Expert Labs known-outcome oracle PASS;
- simple-task and specialist-noun hard negatives PASS;
- JSON/JSONL parse PASS;
- no protected capability or authorization-boundary regression.

A skill is a folder, not a prompt string. Repairs may change `SKILL.md`, references, policy metadata, scripts and evals together; promotion cannot rely on self-report.
