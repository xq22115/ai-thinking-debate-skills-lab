# AI Efficiency Operating System — 2026 Native Plugin

Version: **1.1.0-rc1**  
Status: **RC / package candidate / host-live not yet proven**.

This is the canonical replacement for the former monolithic `skills/skills/ai-efficiency-operating-system` package. It does not discard the earlier work: it restructures it around the strongest previously validated artifacts and the current OpenAI plugin/Agent Skills model.

## Basis

The runtime-facing design is a synthesis, not a rewrite from scratch:

- **Executive Harness v1.0.0** supplies the validated eight-skill topology, phase ownership, negative routing, context budget and host-capability boundaries.
- **Deep Task Integrity** supplies the adaptive depth governor, temporal breadth, 12-route search map, evidence lineage and MATERIAL DELTA stop/pivot rule.
- **DeepLock V2.1** supplies authority separation, isolated-first-pass review, strict evidence-family accounting and the optional strict acceptance profile.
- **ARR v1.3** supplies durable runtime concepts such as goal CAS, first-class UNKNOWN effects, fencing, receiver read-back and semantic replay. These stay behind the persistent-runtime boundary rather than being pretended into ordinary ChatGPT.
- **Recovered second-round control systems** supply coverage-aware stop, citation/source release gates, evaluator lifecycle/tribunal, no-skill differential attribution, C0–C6 replay and shadow-vs-observed promotion. These are machine contracts rather than new always-on skills.

External 2026 references and evidence boundaries are recorded in `references/2026-baseline.md`.

## Eight skills remain the semantic owners

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

## 1.1 machine control plane

The plugin now has five provider-free machine-readable contracts:

- `contracts/research-integrity.json` — query novelty, provenance/freshness, retrieved-content authority firewall, citation/counterevidence/conflict release and coverage-aware stop;
- `contracts/evaluator-governance.json` — evaluator admission, quarantine/deprecation and independent-method tribunal;
- `contracts/skill-composition.json` — task-relevant skill subgraph, explicit long-horizon transitions and no-skill/matched-reference attribution;
- `contracts/replay-checkpoints.json` — capability-gated C0–C6 replay, typed task graph and unsafe-effect reconciliation;
- `contracts/validation-policy.json` — STRUCTURAL/INSTALLED_TEMPLATE/EXECUTABLE/BEHAVIORAL_TARGET separation and SHADOW_ONLY vs OBSERVED_TARGET promotion.

`control_plane_oracle.py` exercises planted known-outcome cases without a provider. This is deliberate: deterministic control logic should not depend on the same model it is supposed to govern.

## Desktop / Codex distribution

The repository contains `.agents/plugins/marketplace.json`, following OpenAI's current GitHub marketplace import model. The plugin is skill-only: it does not declare an MCP server, so the portable core is not intentionally Desktop-only.

A repository package is still not proof of activation. `HOST_LIVE` requires the actual ChatGPT/Codex surface to import/install this exact revision and pass `adapters/chatgpt/RUNTIME_PROBE.md`.

## Research depth

Default research is **adaptive**, not quota theater. Another round is justified only by a MATERIAL DELTA: a gate advanced, hypothesis discriminated, new upstream mechanism, independent decision-changing evidence, resolved version/time conflict, counterexample/regression, or a changed feasible action set.

Research depth and research integrity are separate. More retrieval can worsen citation truth, so load-bearing claims are governed by source accessibility, relevance, factual support, provenance concentration, counterevidence and conflict disclosure rather than citation count alone.

The historic 600-second / 50-family / 10-domain / 10-worker requirements survive as the explicit `STRICT_DEEPLOCK` profile. They are acceptance thresholds, not a universal definition of intelligence or depth.

## Evolution

A skill is a folder, not a prompt string. Repairs may change `SKILL.md`, references, scripts and evals together, but promotion requires target + protection + holdout checks and cannot be self-approved.

A candidate skill/control is compared with a no-skill or semantically matched reference where attribution matters. Simulated known-outcome controls may reach `SHADOW_ONLY`; promotion to target use requires current observed-target evidence plus protected-quality non-regression and measurable utility/cost gain.
