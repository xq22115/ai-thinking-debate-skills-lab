# AI Efficiency Operating System — 2026 Native Plugin

Status: **RC / package candidate / host-live not yet proven**.

This is the canonical replacement for the former monolithic `skills/skills/ai-efficiency-operating-system` package. It does not discard the earlier work: it restructures it around the strongest previously validated artifacts and the current OpenAI plugin/Agent Skills model.

## Basis

The runtime-facing design is a synthesis, not a rewrite from scratch:

- **Executive Harness v1.0.0** supplies the validated eight-skill topology, phase ownership, negative routing, context budget and host-capability boundaries.
- **Deep Task Integrity** supplies the adaptive depth governor, temporal breadth, 12-route search map, evidence lineage and MATERIAL DELTA stop/pivot rule.
- **DeepLock V2.1** supplies authority separation, isolated-first-pass review, strict evidence-family accounting and the optional strict acceptance profile.
- **ARR v1.3** supplies durable runtime concepts such as goal CAS, first-class UNKNOWN effects, fencing, receiver read-back and semantic replay. These stay behind the persistent-runtime boundary rather than being pretended into ordinary ChatGPT.

External 2026 references are recorded in `references/2026-baseline.md`.

## Eight skills

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

The first six may be selected implicitly. The last two are explicit-only because an ordinary skill must never pretend it grants autonomous authority or persistent runtime primitives.

## Desktop / Codex distribution

The repository now contains `.agents/plugins/marketplace.json`, which follows OpenAI's current GitHub marketplace import path. The plugin itself is under `plugins/ai-efficiency-operating-system/` and is skill-only: it does not declare MCP servers, so the core is not intentionally Desktop-only.

A repository package is still not proof of activation. `HOST_LIVE` requires the actual ChatGPT/Codex surface to import/install this exact revision and pass the live probe in `adapters/chatgpt/RUNTIME_PROBE.md`.

## Research depth

Default research is **adaptive**, not quota theater. Another round is justified only by a MATERIAL DELTA: a gate advanced, hypothesis discriminated, new upstream mechanism, independent decision-changing evidence, resolved version/time conflict, counterexample/regression, or a changed feasible action set.

The historic 600-second / 50-family / 10-domain / 10-worker requirements survive as the explicit `STRICT_DEEPLOCK` profile. They are not used as a universal definition of intelligence or depth.

## Evolution

A skill is a folder, not a prompt string. Repairs may change `SKILL.md`, references, scripts and evals together, but promotion requires target + protection + holdout checks and cannot be self-approved.
