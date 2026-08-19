# AI Thinking, Debate & Skills Research Archive — 2026-08-18

Status: **Evidence-Gated Deliberation & Skills OS v1.3 RC1 — GitHub staged / CI blocked / host-live unverified**.

## Canonical synthesis

**TRUTH HARD / METHOD SOFT**

- Hard: evidence, state transitions, completion criteria, permissions, rollback, provenance, evals.
- Soft: strategy, branch count, agent topology, search depth, tool selection, debate shape.
- Debate is for generating and attacking competing hypotheses, not role-count theater.
- Durable state must live outside transient model context.
- Reusable procedures should be packaged as versioned, testable skills.
- Scale deliberation by **marginal information gain and consequence**, not by a fixed number of agents.
- Capability truth is three-stage: **VISIBLE → AUTHORIZED → VERIFIED**.
- Fast-moving product evidence must distinguish **PRODUCT_GUIDANCE / REPOSITORY_CONTENT / REPOSITORY_METADATA / RUNTIME_OBSERVATION**.

## Recovered cross-chat lineages

- Continuous Thinking: v1.x → v8.3.0 family; later evidence-gated research/debate lines.
- Multi-Agent Deliberation OS: v1.0.0 → v10.1.0.
- Global AI Operating Rules: v0.1.0 → v0.5.0.
- LIMIT-RELEASE Ω: v5.x → v6.2.x.
- Agent Skills Governance: v0.1.x → v0.6.x family; earlier named v0.3.0.
- Human Presence Dialogue OS: v1.0.0; later work references v2.0.0.
- Deep Thinking skillpack: v3.0.0-rc1.
- Adlerian Recursive Socratic Inquiry OS: v7.0.0.
- U.S. Counsel AI OS: v2.0.0 → v2.1.0.
- Animation Skillpack: v0.3.0 / 19 skills.
- Adaptive AI Control Plane and FLEX-TRUTH KERNEL lines.

These are archive facts about prior chat work, **not proof of live host installation**.

## Cross-chat convergence

The current source model is deliberately layered:

- **PR #46 = archive/vault layer** — broad historical recovery, status labels, registries.
- **PR #45 = portable reasoning/skills/evidence layer** — evidence, hypotheses, deliberation, compatibility, completion, recovery.
- **PR #29 = execution/control-plane layer** — durable task identity, isolated actor workspaces, receipts, resume/recovery, runtime truth boundaries.
- **PR #28/#25/#19 = governance/autonomy inputs** — distilled into portable permission/evidence principles rather than copied wholesale.

Pinned internal heads are recorded in `13-cross-chat-source-lock.json`; branch drift must be explicitly re-snapshotted before migration or exact-revision claims are inherited.

## 2026 evidence refresh

The archive now uses current product guidance, a 22-source evidence ledger, and exact upstream GitHub locks where applicable.

Current primary/upstream lines include:

- OpenAI Agents SDK — durable harness, sandboxes, resumable execution; 2026-08 workflow/skill boundary changes.
- OpenAI Codex current plugin/skill product guidance — plugins package workflow capabilities; `openai/skills` README is deprecated, while example-repository metadata is tracked separately from product status.
- Anthropic agent research and `anthropics/skills` — plan-level oversight, verifiable outcomes, prompt auditing, discernment-oriented skills.
- Microsoft Agent Framework — active Microsoft workflow/agent line; AutoGen retained as maintenance/history context.
- Google ADK 2.0 — workflow/multi-agent runtime plus explicit breaking agent API/event/session-schema boundary.
- LangGraph — active explicit graph/state orchestration and checkpointing line.
- Agent Skills / MCP — portable skill semantics and dynamically negotiated tool/protocol capabilities.
- OpenClaw — active session/context provenance and long-running state work.
- `obra/superpowers` — adaptive routing, SDD continuity, falsifiable tests, multi-harness compatibility.
- 2026 multi-agent/debate research — diversity, topology, selective communication and adjudication matter more than raw agent count.

Evidence ledger: `05-source-ledger.json` — **22 sources**.
Reproducible external snapshot: `12-upstream-source-lock.json`.
Latest delta synthesis: `13-aug18-upstream-delta.md`.

## RC1 portable skill set

Nine current core skills:

1. `evidence-gap-research`
2. `competing-hypotheses`
3. `root-cause-clustering`
4. `completion-gate` — `0.1.1-rc1`
5. `recoverable-state`
6. `compatibility-audit` — `0.1.1-rc1`
7. `multi-agent-deliberation` — `0.1.1-rc1`
8. `capability-challenge` — `0.1.1-rc1`
9. `durable-agent-control-plane` — `0.1.1-rc1`

The 30-role map is a **coverage topology**, not proof that 30 independent external model processes were run. Runtime fan-out remains adaptive and runtime independence is separately evidence-gated.

## Evaluation layer

`evals/rc1-fixtures.json` is now `0.1.1-rc1` with **15 adversarial/spec fixtures**, including:

- false completion;
- pre-step infrastructure blocker ≠ test failure;
- minority-correct hypothesis;
- clone diversity;
- role labels ≠ runtime independence;
- root-cause clustering;
- interruption/resume;
- Windows/macOS compatibility;
- product-guidance vs repository-metadata conflict;
- framework version boundary;
- missing repository-creation capability;
- visible ≠ authorized;
- read permission ≠ write permission;
- runner unavailable with durable receipts;
- stale remembered evidence.

These are eval specifications/fixtures; they are not evidence that hosted eval execution has passed.

## Research map

- `00-cross-chat-research-map.md` — normalized recovered research families.
- `01-30-role-deliberation.md` — 30-role coverage/debate topology.
- `02-skills-catalog.md` — nine RC1 skills plus candidate supporting responsibilities.
- `03-2026-current-evidence.md` — current evidence synthesis.
- `04-reference-architecture.md` — target architecture.
- `05-source-ledger.json` — 22-source ledger with source-class separation and unstable GitHub sources pinned where applicable.
- `06-evaluation-suite.md` — false-completion, recovery, root-cause, diversity and efficiency eval plan.
- `07-deliberation-router-spec.md` — adaptive 1–30 role routing.
- `08-portability-matrix.md` — portable logic vs host/OS/product-version specifics.
- `09-research-backlog.md` — remaining RC1 work.
- `10-ci-diagnosis.md` — hosted CI blocker evidence.
- `11-cross-chat-convergence.md` — PR #46/#45/#29 convergence.
- `12-upstream-source-lock.json` — reproducible external repository snapshot.
- `13-aug18-upstream-delta.md` — 2026-08-18 upstream change implications.
- `13-cross-chat-source-lock.json` — exact internal PR/branch/head locks.
- `14-rc1-release-gates.md` — ten release/status gates.
- `15-machine-readable-governance.md` — machine-readable role/claim governance layer.
- `16-governance-autonomy-convergence.md` — autonomy, capability truth, exact-revision evidence and source-class governance.
- `data/role_activation_policy.yaml` — machine-readable deliberation policy.
- `data/claim_obligation_graph.json` — machine-readable claims/obligations/invariants.
- `skills/` — nine portable RC1 skills.
- `evals/` — adversarial/control-plane fixtures.
- `adapters/` — host-specific boundary, intentionally separate from portable core.

## Release truth

The highest defensible current state is:

`RC1_PACKAGED_AND_GITHUB_STAGED / CI_BLOCKED / HOST_LIVE_UNVERIFIED`

Do **not** infer:

- GitHub committed → CI passed;
- eval specified → eval executed;
- repository artifacts → authentic multi-agent runtime executed;
- role names → runtime independence;
- local/deterministic test → provider live verified;
- visible tool → authorized mutation;
- configuration → live host state;
- branch/PR exists → dedicated repository exists;
- package exists → stable/deployed/healthy.

Release gates are authoritative in `14-rc1-release-gates.md`.

## Current blockers

- Issue #47 — GitHub Actions jobs fail before workflow steps execute; leading diagnosis is billing/spending-limit state and is kept distinct from code/test failure.
- Issue #48 — migrate to dedicated `ai-thinking-debate-skills-lab`; top-level repository creation is unavailable through the connected GitHub action set.

## Dedicated target repository

Recommended final repository: `ai-thinking-debate-skills-lab`.

Current staging location:

- repository: `xq22115/demo-repository`
- branch: `research/ai-thinking-debate-skills-20260818`
- PR: #45
- directory: `research/ai-thinking-debate-skills-2026-08-18/`

PR #45 should remain **Draft** until the blocking release gates are resolved.
