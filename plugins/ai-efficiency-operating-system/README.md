# AI Efficiency Operating System — 2026 Native Plugin

Status: **RC / package candidate / host-live not yet proven**.

This is the canonical replacement for the former monolithic `skills/skills/ai-efficiency-operating-system` package. It preserves the validated core while keeping high-cost/specialized capabilities out of the default route.

## Basis

The runtime-facing design is a synthesis, not a rewrite from scratch:

- **Executive Harness v1.0.0** supplies the validated eight-skill topology, phase ownership, negative routing, context budget and host-capability boundaries.
- **Deep Task Integrity** supplies the adaptive depth governor, temporal breadth, 12-route search map, evidence lineage and MATERIAL DELTA stop/pivot rule.
- **DeepLock V2.1** supplies authority separation, isolated-first-pass review, strict evidence-family accounting and the optional strict acceptance profile.
- **ARR v1.3** supplies durable runtime concepts such as goal CAS, first-class UNKNOWN effects, fencing, receiver read-back and semantic replay. These stay behind the persistent-runtime boundary rather than being pretended into ordinary ChatGPT.

External 2026 references are recorded in `references/2026-baseline.md`.

## Eight executive skills

| Skill | Primary ownership |
|---|---|
| `chief-of-staff-core` | task contract, phase routing, capability truth |
| `plan-arbiter` | plan choice, architecture tradeoffs, sequencing |
| `evidence-watchdog` | completion claims, postconditions, read-back |
| `executive-research` | current research, root cause, temporal/version analysis |
| `memory-policy` | durable memory, provenance, rehydration |
| `convergence-controller` | review loops, no-progress pivots, skill evolution |
| `autonomy-contract` | explicit effect-bearing delegation and authority |
| `persistent-work-ledger` | explicit durable state on filesystem/state-capable hosts |

The first six may be selected implicitly. `autonomy-contract` and `persistent-work-ledger` are explicit-only because an ordinary skill must never pretend it grants authority or persistent runtime primitives.

## Expert Labs — explicit-only

Version `1.1.0-rc2` retains the four **opt-in** expert skills from 1.1 and adds the stricter dual-surface 10-agent HOST_LIVE validation contract. Expert Labs do not increase the default implicit skill pool.

| Expert Lab | Use |
|---|---|
| `capability-forensics` | distinguish model vs harness vs tool vs permission vs session vs entitlement vs environment/runtime limitations |
| `mcp-surface-engineering` | dynamic/lazy tool discovery, schema drift, namespace collision, entitlement-specific surfaces and tool-poisoning controls |
| `authorized-reverse-engineering` | static/dynamic analysis of software/binaries the user is authorized to inspect, with exact artifact/toolchain identity |
| `agent-runtime-forensics` | correlate model intent, tool calls, process/file/network events, artifacts and postconditions into a scoped causal evidence graph |

Expert Labs are demand-loaded, default-disabled and require a no-skill/lighter-baseline counterfactual before promotion. They maximize **authorized capability and observability**; they do not bypass provider safety controls, access controls, licensing/DRM or authorization boundaries.

## AI-specific deep search

`executive-research/references/ai-ecosystem-recon.md` adds a dedicated AI research playbook without adding another implicit skill. It covers canonical-name/version reconstruction, repository/change archaeology, plugin/MCP schema and capability surfaces, model×harness differential research, hard-negative skill/eval evidence, security/tool-poisoning research, authorized reverse-engineering escalation and runtime provenance.

The rule remains: deeper search must produce a MATERIAL DELTA, not merely more links.

## Desktop / Codex distribution

The repository contains `.agents/plugins/marketplace.json`, following OpenAI's current GitHub marketplace import shape. The plugin itself is skill-only and declares no MCP server; local tools/runtimes remain owned by the actual host/app.

A repository package is not proof of activation. `HOST_LIVE` requires the actual ChatGPT/Codex surface to import/install this exact package content and pass the live probe in `adapters/chatgpt/RUNTIME_PROBE.md`. When strict ten-agent unanimity is explicitly requested, also use `adapters/chatgpt/HOST_LIVE_10WAY.md`.

## Research depth

Default research is **adaptive**, not quota theater. Another round is justified only by a MATERIAL DELTA: a gate advanced, hypothesis discriminated, new upstream mechanism, independent decision-changing evidence, resolved version/time conflict, counterexample/regression, or a changed feasible action set while preserving constraints.

The historic 600-second / 50-family / 10-domain / 10-worker requirements survive as the explicit `STRICT_DEEPLOCK` profile. They are not used as a universal definition of intelligence or depth.

## Tests and promotion

The package uses RED/GREEN skill TDD plus deterministic routing and behavior gates. Expert Labs add a known-outcome oracle that tests capability-layer diagnosis, MCP drift/poisoning, reverse-engineering authorization boundaries and runtime-effect provenance.

A skill is a folder, not a prompt string. Repairs may change `SKILL.md`, references, scripts and evals together, but promotion requires target + protection + holdout checks and cannot be self-approved.
