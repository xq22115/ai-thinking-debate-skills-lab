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

## Task Goal Intelligence v3

The goal gate is no longer only a first-turn interpretation step. Its v3 runtime projection adds an evidence-bearing state machine around the whole trajectory:

- event-sourced `GOAL_VERSION` / `GOAL_FINGERPRINT` semantics so corrections invalidate dependent work without silently rewriting history;
- historical completion/config/runtime claims are provisional until rebound to fresh owning-system evidence;
- anti-loophole / anti-minimization checks prevent imperfect wording, examples, named tools, or a route-local blocker from silently shrinking the desired end state;
- blocked-slice isolation continues every separable goal-advancing path instead of turning one unavailable route into task abandonment;
- Goal Capsule recitation re-anchors the current goal after corrections, context compaction/handoff, route changes, repeated failures, target/session changes and before final acceptance;
- Progress Ledger requires acceptance/evidence/uncertainty/state delta; activity volume by itself is not progress, and repeated no-delta steps force a causally different route;
- high-scale ecosystem evidence is combined with high-discrimination negative/rare evidence; opaque/anonymous/underground/onion threat-intelligence signals begin as provenance-bearing leads rather than facts;
- end-to-end user-goal success is judged before step-level polish, failure analysis identifies the first upstream failure, and completion claims are reverse-walked to current owning evidence;
- real corrections and false-completion traces are promoted into adversarial regression cases and optimizer feedback.

The dedicated `Task Goal Intelligence v3 Gate` reruns the canonical v2/v2.2 invariants before validating v3, so the package cannot pass by deleting prior protections or renaming away routing contracts.

## Default implicit skills

| Skill | Primary ownership |
|---|---|
| `task-goal-intelligence` | goal interpretation, semantic delta, historical-claim revalidation, anti-minimization, progress evidence and information-gain routing |
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

The architecture follows a synthesis rather than one framework copy: constrained candidate selection/hand-off patterns, conditional tool nodes, dynamic tool discovery, semantic routing after eligibility filtering, negative-routing tests, fallback graphs, held-out promotion gates and postcondition verification. Task Goal Intelligence v3 additionally records targeted mechanisms from RECAP/EACL intent-for-planning evaluation, Hamel Husain + Shreya Shankar's end-to-end/error-analysis methodology, DSPy/GEPA textual-feedback optimization, Manus context recitation, Magentic-One task/progress ledgers, and OpenCTI/MISP provenance patterns. External references and limitations are kept in machine-readable source ledgers rather than being treated as authority by name alone.

Default research is adaptive and MATERIAL-DELTA driven. Historic numeric/time/worker thresholds survive only under explicit `STRICT_DEEPLOCK`; they are not a universal definition of depth.

## Desktop / Codex distribution

The repository contains `.agents/plugins/marketplace.json`. The package is skill-only and does not itself grant filesystem, terminal, MCP server, background daemon, browser-control or other host primitives.

`PACKAGED != HOST_LIVE`. An owning ChatGPT/Codex surface must import/sync this exact revision and demonstrate fresh-session discovery, positive implicit routing, hard-negative routing, conditional specialist activation, fallback behavior and postcondition evidence before that surface is called `HOST_LIVE`.

## Tests and promotion

The package uses deterministic routing, behavior, specialist and composition/fallback regression corpora plus a dedicated task-goal v3 hard-negative corpus. Promotion requires:

- package/metadata/schema validation;
- primary routing corpus PASS;
- composition + fallback corpus PASS;
- Expert Labs known-outcome oracle PASS;
- simple-task and specialist-noun hard negatives PASS;
- Task Goal Intelligence v2/v2.2 invariant preservation PASS;
- Task Goal Intelligence v3 machine contract / adversarial corpus PASS;
- JSON/JSONL parse PASS;
- no protected capability or authorization-boundary regression.

A skill is a folder, not a prompt string. Repairs may change `SKILL.md`, references, policy metadata, scripts and evals together; promotion cannot rely on self-report.
