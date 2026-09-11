# AI Efficiency Operating System — 2026 Native Plugin

Status: **v1.4 package candidate / hosted ChatGPT-Codex HOST_LIVE not preclaimed**.

Version 1.4 keeps the Native Goal Harness and ordinary-ChatGPT Superpowers process bridge, and adds a systematic GitHub operation layer. Material GitHub work now has a first-class specialist, a machine-readable schema-v2 operation contract, deterministic routing/evals, failure-class recovery, exact read-back requirements and runtime probes spanning read, analysis, live tool schema, invocation, writing, workflow execution and final verification.

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

The native package includes:

- `skills/task-goal-intelligence/` — thin goal/phase router with progressive references and deterministic preamble;
- `skills/github-operation-orchestrator/` — demand-loaded GitHub multi-stage operation specialist;
- `adapters/chatgpt/github-pull-runtime.json` — machine-readable ordinary-ChatGPT GitHub operation contract;
- `adapters/chatgpt/GITHUB_OPERATION_LOOP.md` — human-readable operation loop and recovery matrix;
- `adapters/chatgpt/RUNTIME_PROBE.md` — owning-surface read/schema/write/workflow/fallback live probe;
- `skills/superpowers-conversation-runtime/` — isolated ordinary-ChatGPT implementation-process bridge;
- `scripts/route_oracle.py` and `scripts/composition_oracle.py` — deterministic routing/composition baselines;
- `scripts/github_operation_oracle.py` — known-outcome GitHub failure/recovery classifier;
- `evals/github-operation-cases.jsonl` — deterministic GitHub operation failure/recovery cases;
- `scripts/validate_plugin.py` and control-plane validators — fail-closed package/bridge checks.

## GitHub operation loop

The GitHub operation path is treated as one evidence-bound state machine:

`GOAL_LOCKED → TARGET_RESOLVED → AUTHORITY_RESOLVED → READ_PLAN_READY → SOURCE_READ → EVIDENCE_SUFFICIENT → TOOL_SCHEMA_READY → INVOCATION_PREFLIGHT → INVOKED → RESPONSE_CLASSIFIED → MUTATION/READBACK/EXECUTION → ACCEPTANCE_VERIFIED → REGRESSION_VERIFIED → COMPLETE`.

Not every state applies to read-only work, but a required state cannot be silently skipped and promoted to PASS.

The loop enforces these distinctions:

- exact repository/ref/path/blob identity vs ranked discovery;
- `OBSERVED` vs `DERIVED` vs `HYPOTHESIS` vs `UNKNOWN`;
- live tool schema vs remembered/guessed arguments;
- connector transport success vs task success;
- commit creation vs persisted read-back;
- workflow dispatch vs exact run/commit execution evidence;
- installation vs invocation vs observable effect;
- retry wording changes vs a causally different recovery route.

Two same-mechanism failures without a material evidence delta force a route change. Material writes require pre-read, current blob/base evidence, sequential dependent writes, exact-branch read-back, and regression checks. Plugin/skill pull claims cannot jump directly from source state to hosted effectiveness.

## Runtime behavior

When a host can execute the native preamble, it receives phase, path, goal version, goal fingerprint, missing core fields and hard gates before specialist routing. When execution is unavailable, the skill uses degraded inline state evaluation and continues the user's otherwise executable task without claiming the preamble ran.

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
| `github-operation-orchestrator` | multi-step GitHub read/search/analyze/action/write/PR/workflow/execute/read-back/verify work or repeated GitHub connector failures |
| `capability-forensics` | capability differs by model/harness/session/account/surface, or limiting layer is unclear |
| `mcp-surface-engineering` | many/changing/conflicting tools, schema drift, discovery/entitlement/context pressure |
| `agent-runtime-forensics` | tool/process reports success while file/process/network/artifact/postcondition state is missing or causally unclear |

Implicit composition remains bounded to three skills per phase: goal gate, one primary specialist, and `evidence-watchdog` when current state/completion proof is required. A topic noun by itself is not enough to trigger a heavy specialist.

## Explicit-only skills

`autonomy-contract`, `persistent-work-ledger`, and `authorized-reverse-engineering` remain explicit-only. The native goal upgrade does not silently broaden authority-bearing activation.

## Verification stack

Repository gates now cover both native-goal behavior and the GitHub operation loop:

- JSON/JSONL parse and Python compile;
- plugin/settings/skill inventory validation;
- deterministic routing plus hard-negative cases;
- bounded composition and fallback cases;
- GitHub operation known-outcome failure/recovery cases;
- ordinary-ChatGPT GitHub schema-v2 fail-closed validator and mutation tests;
- live-probe contract for exact read, schema discovery, write/read-back, workflow execution evidence, partial responses and no-progress route switching.

Repository-wide gates remain additional protections; package CI does not replace owning-surface verification.

## Truth boundary

`PACKAGED != HOST_LIVE`.

`CONNECTED != INVOKABLE != EFFECTIVE != VERIFIED`.

Repository CI can prove package structure, deterministic runtime behavior and regression contracts on an exact revision. It cannot by itself prove a hosted ChatGPT/Codex surface imported and behaviorally exercised that revision. HOST_LIVE still requires owning-surface discovery/load/invocation/effect/read-back evidence.
