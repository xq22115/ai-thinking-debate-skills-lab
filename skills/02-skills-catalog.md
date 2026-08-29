# Skills Catalog

## Canonical orchestration plugin

### ai-efficiency-operating-system — `1.1.0-rc1`

Canonical path: `plugins/ai-efficiency-operating-system/`.

This replaces the former monolithic `skills/skills/ai-efficiency-operating-system/SKILL.md` runtime entry with the previously validated eight-skill Executive Harness topology, strengthened by Deep Task Integrity, DeepLock V2.1, ARR v1.3 and current 2026 OpenAI/Superpowers/agent-skills/SkillHone patterns.

The 1.1 control plane adds provider-free machine contracts for research integrity, evaluator governance, focused skill composition, capability-gated replay/checkpoints and validation/promotion truth. These extend the eight owners; they do not create another competing skill layer.

| Skill | Trigger owner |
|---|---|
| `chief-of-staff-core` | complex task contract and phase routing |
| `plan-arbiter` | plan/architecture/sequence choice |
| `evidence-watchdog` | state and completion verification |
| `executive-research` | current/deep/root-cause research |
| `memory-policy` | durable memory and rehydration |
| `convergence-controller` | review loops and skill evolution |
| `autonomy-contract` | explicit effect-bearing delegation |
| `persistent-work-ledger` | explicit durable runtime state on capable hosts |

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

When marginal contribution matters, compare the candidate with a no-skill or semantically matched reference. Aggregate benchmark gain does not justify universal activation, and excessive verification/pipeline ceremony may be negative transfer.

## Completion truth

`PACKAGED != HOST_LIVE`.

`STRUCTURAL != INSTALLED_TEMPLATE != EXECUTABLE != BEHAVIORAL_TARGET`.

A GitHub write, archive, marketplace manifest, CI pass or plugin listing cannot by itself prove the intended ChatGPT/Codex surface loaded and exercised the exact revision.
