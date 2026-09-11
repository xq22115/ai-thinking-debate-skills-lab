# Skills Catalog

## Canonical orchestration plugin

### ai-efficiency-operating-system — `1.4.1`

Canonical path: `plugins/ai-efficiency-operating-system/`.

The protected 1.4.1 package contract keeps **Task Goal Intelligence 4.0 Native**, the v2/v2.2/v3 semantic protections, and the isolated ordinary-ChatGPT Superpowers host adapter; it adds a first-class GitHub operation orchestrator and corrects the upstream activation boundary. Repository package state, ordinary-ChatGPT plugin activation, workspace effective policy, required-app/member access, hosted GitHub connector capability, GitHub remote state and verified behavioral effect are separate layers. GitHub work is modeled as an evidence-bound state machine spanning goal lock, host activation truth, exact target resolution, authoritative reads, analysis, live action/schema resolution, invocation preflight, response classification, mutation, execution observation, read-back, recovery, regression and completion.

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
- `host-adapters.json` — machine-readable host-specific adapters kept outside the canonical router inventory;
- `adapters/chatgpt/github-pull-runtime.json` — machine-readable ordinary-ChatGPT GitHub operation contract;
- `adapters/chatgpt/github-upstream-capability-contract.json` — root ownership and host-activation truth;
- `adapters/chatgpt/GITHUB_ROOT_CONTROL_PLANE.md` — human-readable ownership/activation model;
- `adapters/chatgpt/HOST_ACTIVATION_PROBE.md` — repository marketplace → ChatGPT host import/sync/effective-policy/app-access/load behavioral probe;
- `adapters/chatgpt/GITHUB_OPERATION_LOOP.md` — human-readable GitHub read/analyze/call/write/execute/verify loop;
- `skills/github-operation-orchestrator/` — demand-loaded GitHub specialist for multi-stage repository/plugin/PR/workflow work;
- `skills/superpowers-conversation-runtime/` — thin ordinary-ChatGPT Superpowers bridge with progressive disclosure;
- `scripts/goal_skill_start.py` — executable `GOAL_*`/`GATE_*` preamble;
- `scripts/quick_validate.py` — package-local conformance check;
- `scripts/superpowers_route_oracle.py` — isolated process-routing oracle for ordinary ChatGPT;
- `scripts/validate_superpowers_runtime.py` — adapter/upstream/process-coverage/size contract;
- `scripts/validate_github_upstream_contract.py` — fail-closed GitHub root ownership validator;
- `scripts/validate_chatgpt_host_activation_contract.py` — fail-closed repository-to-ChatGPT activation validator;
- `spec/task-goal-intelligence-spec.md` — host-neutral spec;
- `evals/task-goal-native-state-cases.jsonl` — executable state/gate cases;
- `evals/task-goal-native-pressure-holdout.jsonl` — hosted pressure cases; packaging is verified, HOST_LIVE pass is not preclaimed;
- `evals/superpowers-conversation-routing-cases.jsonl` — ordinary-chat positive and hard-negative process-routing pressure cases;
- `evals/github-operation-cases.jsonl` and `evals/github-root-control-cases.jsonl` — GitHub lifecycle/root-owner known-outcome cases.

### Ordinary ChatGPT Superpowers host adapter

`superpowers-conversation-runtime` is registered as a host adapter, not silently counted as a new canonical router member. It uses progressive ceremony:

- `DIRECT` — ordinary explanation/rewriting/simple work stays direct;
- `BOUNDED` — debugging, behavior/feature changes, review feedback and skill authoring load only the relevant Superpowers process;
- `ARCHITECTURAL` — only materially architectural work adds goal locking, design/planning and verification.

The bridge maps bugs/failing tests to `systematic-debugging`, new/changed behavior to `brainstorming`, settled implementation to `test-driven-development`, approved plans to `executing-plans`, review feedback to `receiving-code-review`, skill authoring to `writing-skills`, and completion claims to `verification-before-completion` while preserving local `evidence-watchdog` ownership. It stays quiet by default and never invents unavailable worktrees, subagents, background execution, filesystem access or test runs.

### Ordinary ChatGPT GitHub operation adapter

`github-operation-orchestrator` is a conditional canonical specialist for material GitHub work **only when the owning ChatGPT surface has actually loaded the local plugin**. It uses the bound GitHub app and `github-pull-runtime.json` schema v2 to preserve one operation envelope across the lifecycle:

`GOAL_LOCKED → TARGET_RESOLVED → AUTHORITY_RESOLVED → READ_PLAN_READY → SOURCE_READ → EVIDENCE_SUFFICIENT → TOOL_SCHEMA_READY → INVOCATION_PREFLIGHT → INVOKED → RESPONSE_CLASSIFIED → MUTATION/EXECUTION/READBACK → ACCEPTANCE_VERIFIED → REGRESSION_VERIFIED → COMPLETE`.

Before crediting the local specialist with ordinary-ChatGPT behavior, the host activation chain must remain explicit:

`GIT REPO → MARKETPLACE CATALOG → CHATGPT MARKETPLACE IMPORT/SYNC → WORKSPACE EFFECTIVE POLICY → PLUGIN INSTALL/ASSIGN → REQUIRED APP ACCESS/AUTH → CURRENT SURFACE LOAD → BEHAVIORAL EFFECT`.

A merge, green CI, marketplace file, repository `AVAILABLE / ON_INSTALL` metadata, separately installed `github@openai-curated` connector, or `Allow all actions` setting is not sufficient proof of the local plugin being host-live. Import/Sync itself also does not prove effective workspace policy, required-app role access or member/provider authentication. Missing evidence remains `CUSTOM_PLUGIN_ACTIVATION_UNVERIFIED`; inability to perform the required host import/install step remains `HOST_IMPORT_BLOCKED`.

Once activation is established, the GitHub loop keeps `OBSERVED`, `DERIVED`, `HYPOTHESIS`, and `UNKNOWN` separate; requires live schema resolution when material action shape is not already current; treats transport success, commit creation, workflow request/rerun, installation and invocation as lower-layer evidence rather than completion; preserves explicit search breadth targets with query fanout/dedup/truncation handling; and forces a causal route change after two same-mechanism attempts without a material evidence delta.

Evidence owner routing is host-aware: current library/framework/API facts prefer Context7 when available; repository/PR/Actions facts use GitHub; user files use Files; connected private data uses its owning connector; other current public facts use web; stateful completion uses owning-system readback.

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
| `github-operation-orchestrator` | host-loaded multi-step GitHub read/search/analyze/action/write/PR/workflow/execute/read-back/verify loops, plugin/skill pulls and repeated GitHub connector failures |
| `capability-forensics` | model-vs-harness-vs-tool-vs-permission/session/entitlement/environment bottleneck diagnosis, including uncertain plugin activation/effective policy/app access |
| `mcp-surface-engineering` | dynamic tool discovery, schema/version drift, namespace collision, entitlement/context pressure and tool-poisoning controls |
| `agent-runtime-forensics` | model/tool/process/file/network/artifact/postcondition causal evidence and replay |

These specialists are eligible for implicit invocation only after the routing eligibility layer finds material diagnostic signals. A topic noun such as “GitHub”, “MCP” or “runtime” is insufficient by itself.

### Explicit-only skills

| Skill | Why explicit |
|---|---|
| `autonomy-contract` | authority documentation cannot create authority |
| `persistent-work-ledger` | requires real durable runtime primitives |
| `authorized-reverse-engineering` | remains intentionally scoped to authorized artifact analysis |

## Canonical combination patterns

- research-heavy → `task-goal-intelligence` + `executive-research` + `evidence-watchdog`
- GitHub operation → `task-goal-intelligence` + `github-operation-orchestrator` + `evidence-watchdog` after host activation/effective policy is proven
- capability bottleneck → `task-goal-intelligence` + `capability-forensics` + `evidence-watchdog`
- MCP/tool-surface pressure → `task-goal-intelligence` + `mcp-surface-engineering` + `evidence-watchdog`
- runtime-effect mismatch → `task-goal-intelligence` + `agent-runtime-forensics` + `evidence-watchdog`
- architecture choice → `task-goal-intelligence` + `plan-arbiter`
- repeated route failure → `task-goal-intelligence` + `convergence-controller` + `evidence-watchdog`
- cross-session context → `task-goal-intelligence` + `memory-policy`
- complex multi-stage → `task-goal-intelligence` + `chief-of-staff-core` + `evidence-watchdog`

Implicit canonical bundles are bounded to three skills per phase. Host adapters are orthogonal process overlays and do not consume a canonical router slot merely by being packaged. Discover many, load few.

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

`PACKAGED != CHATGPT_IMPORTED != WORKSPACE_POLICY_EFFECTIVE != APP_ACCESSIBLE != CONNECTED != INVOKABLE != EFFECTIVE != VERIFIED`.

A GitHub write, marketplace manifest, CI pass, plugin listing or available connector cannot prove the intended ordinary-ChatGPT surface loaded and exercised the exact local revision. Host-live acceptance requires current marketplace import/sync or another supported installation path, effective workspace installation/auth policy, required-app/member access and authentication when applicable, current-surface visibility, a behavioral marker unique to the intended revision, fallback validation and owning-system postcondition evidence.
