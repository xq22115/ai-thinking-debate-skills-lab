# AI Efficiency Operating System — 2026 Native Plugin

Status: **v1.3 package candidate / hosted ChatGPT-Codex HOST_LIVE not preclaimed**.

Version 1.3 changes Task Goal Intelligence from a monolithic semantic rule block into an upstream-native agent harness package: thin router, deterministic runtime preamble, explicit phase machine, progressive references/scripts, fresh-verification gate, recovery state, executable state evals and failure-trace holdouts.

## Native Goal Harness 4.0

Canonical machine profile: `native-goal-harness.json`.

Canonical states:

`ORIENT → DISCRIMINATE → COMMIT → EXECUTE → VERIFY → LEARN`

`RECOVER` can interrupt a material phase and returns to the nearest still-valid state. A semantic user correction interrupts back to `ORIENT`.

Task complexity uses a one-way ratchet:

`DIRECT → INVESTIGATIVE → ARCHITECTURAL`

Hidden complexity can upgrade the path. The harness cannot silently downgrade a live task to avoid evidence, verification, coordination, or a blocker.

## Upstream-native configuration model

The package adapts control structures from exact public upstream revisions recorded in `skills/task-goal-intelligence/references/upstream-lock.json`:

- **OpenAI `openai/plugins`** — skill-as-folder packaging: manifest, agents policy, references, scripts, quick validation;
- **obra/superpowers** — process-skill dispatch, hard phase gates, root-cause-before-fix, fresh-verification-before-completion, rationalization pressure tests;
- **garrytan/gstack** — runtime preamble/status protocol, degraded mode, session-bound runtime state, thin routing, completion-state protocol;
- **Anthropic `anthropics/skills`** — host-neutral spec separated from minimal runtime skill packages and progressive disclosure;
- **Stanford DSPy/GEPA** — execution-trace + textual-feedback optimization with target/protection/holdout/adversarial promotion slices.

The repo adopts mechanisms and package structure, not verbatim upstream prompt prose.

## Package shape

`task-goal-intelligence` now follows a native package layout:

- `SKILL.md` — thin implicit router only;
- `agents/openai.yaml` — invocation policy;
- `references/phase-machine.md` — state transitions and complexity ratchet;
- `references/runtime-preamble.md` — machine protocol, trust boundary and degraded mode;
- `references/evidence-and-optimization.md` — root cause, fresh verification, evidence mesh and optimizer loop;
- `references/upstream-lock.json` — exact source commits and adopted mechanisms;
- `scripts/goal_skill_start.py` — deterministic preamble producing `GOAL_*` / `GATE_*` status;
- `scripts/quick_validate.py` — package-local validator;
- `spec/task-goal-intelligence-spec.md` — host-neutral conformance spec;
- `evals/task-goal-native-state-cases.jsonl` — executable state/gate suite;
- `evals/task-goal-native-pressure-holdout.jsonl` — host behavioral pressure holdout, packaged but not falsely claimed as HOST_LIVE-passed.

## Runtime behavior

When a host can execute the preamble, it receives phase, path, goal version, goal fingerprint, missing core fields and hard gates before specialist routing. When execution is unavailable, the skill uses degraded inline state evaluation and continues the user's otherwise executable task without claiming the preamble ran.

Material progress requires at least one acceptance, evidence, decision-critical uncertainty or observable-state delta. Two no-delta material steps force causal recovery. Three materially distinct failed repairs to one mechanism force architectural review rather than a fourth symptom patch.

Before any completion/fixed/enabled/effective/verified claim, the harness reverse-walks:

`claim → acceptance test → owning evidence → current goal version → causal path`

Historical prose, command exit status and agent self-report cannot substitute for current owning evidence.

## Default implicit skills

| Skill | Primary ownership |
|---|---|
| `task-goal-intelligence` | native goal preamble, phase routing, semantic delta, anti-minimization, recovery and verification entry |
| `chief-of-staff-core` | complex task contract and phase ownership |
| `plan-arbiter` | plan/architecture/sequence choice |
| `evidence-watchdog` | completion claims, postconditions and read-back |
| `executive-research` | current/deep/root-cause research and evidence archaeology |
| `memory-policy` | durable context and rehydration |
| `convergence-controller` | repeated failure/review loops and materially different route selection |

## Conditional implicit specialists

| Skill | Auto-invoke trigger |
|---|---|
| `capability-forensics` | capability differs by model/harness/session/account/surface, or limiting layer is unclear |
| `mcp-surface-engineering` | many/changing/conflicting tools, schema drift, discovery/entitlement/context pressure |
| `agent-runtime-forensics` | tool/process reports success while file/process/network/artifact/postcondition state is missing or causally unclear |

Implicit composition remains bounded to three skills per phase: goal gate, one primary specialist, and `evidence-watchdog` when current state/completion proof is required.

## Explicit-only skills

`autonomy-contract`, `persistent-work-ledger`, and `authorized-reverse-engineering` remain explicit-only. The native goal upgrade does not silently broaden authority-bearing activation.

## Verification stack

`Task Goal Native v4 Gate` executes, rather than merely scans, the native package:

- JSON/JSONL parse and Python compile;
- skill-local quick validation including five exact upstream revision locks;
- 30-case deterministic state-machine oracle covering all seven phases;
- native harness structural/behavioral contract validation;
- 24-case pressure-holdout packaging and class coverage validation;
- existing plugin validation;
- existing Task Goal Intelligence v3 validator.

Repository-wide gates remain additional protections; v4 does not replace them.

## Truth boundary

`PACKAGED != HOST_LIVE`.

`CONNECTED != INVOKABLE != EFFECTIVE != VERIFIED`.

Repository CI can prove package structure, deterministic runtime behavior and regression contracts on an exact revision. It cannot by itself prove a hosted ChatGPT/Codex surface imported and behaviorally exercised that revision. HOST_LIVE still requires owning-surface discovery/load/invocation/effect/read-back evidence.
