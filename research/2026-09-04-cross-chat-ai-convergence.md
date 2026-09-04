# 2026-09-04 Cross-Chat AI Research Convergence

Status: **research / deliberation lane**. This document does not become the runtime owner for ordinary ChatGPT. `xq22115/braintrust` remains the external control-plane source of truth for ordinary ChatGPT routing/runtime contracts.

## Goal

Converge the user's latest AI research, cross-chat findings, Notion runtime skills, GitHub agent-control work, OpenClaw automation work, and deliberation/evaluation patterns into one non-duplicating architecture.

## Current exact refs

- `xq22115/braintrust@bddde59832739d650f88d344210df6dd8a7b691e`
- `xq22115/ai-thinking-debate-skills-lab@0393886b46f23f820e24de8e9197905c093ee701` as the base used for this research branch
- Notion: `AI Control Center｜Notion MCP × GitHub × ChatGPT`
- Notion runtime: `AI Skills Runtime Library｜Auto-Invoke` (14 runtime skills observed on 2026-09-04)

## Recovered cross-chat implementation state

Observed previously completed/verified package versions include:

- OpenHands / Agent Canvas 1.16.0
- OpenCode 1.18.27
- Goose 1.48.0
- Codex CLI 0.153.0
- Claude Code 2.1.259
- Gemini CLI 0.58.0
- claude-agent-acp 0.73.0
- codex-acp 1.8.0

A prior Goose → Codex ACP → ChatGPT path returned `GOOSE_ACP_OK`. Historical runtime blockers must still be re-probed before reuse; old success/failure is not current host-live evidence.

## Architecture convergence

The strongest common pattern across the current estate is:

1. **Goal fidelity first** — compile root task, desired end state, negations, hard constraints and acceptance tests; corrections override stale summaries.
2. **Demand-loaded capability routing** — keep a wide known capability inventory but activate only the smallest causally useful Skills/MCP/connectors.
3. **CLI/API/DOM first** — use deterministic execution surfaces when available; GUI/CUA is a fallback when the target effect actually requires it.
4. **Durable external state** — keep long-horizon state in GitHub/Notion/task ledgers/checkpoints rather than prompt prose alone.
5. **Session isolation** — separate chats/agents/write-sets; same architecture owner + same write-set means one writer.
6. **Independent verification** — `CONNECTED -> INVOKED -> DEEP_USED -> CHALLENGED -> TASK_EFFECT_VERIFIED`; existence or self-report cannot promote completion.
7. **Causal recovery** — two materially no-delta attempts freeze the route and force a causally distinct fallback rather than prompt churn.

## OpenClaw / high-autonomy lane

The current preferred design is not “fine-tune first.” It is a stateful harness with:

- session isolation;
- completion judge;
- auto-continue controller;
- deterministic DOM/ARIA browser actions with computer-use fallback;
- watchdog;
- checkpoint/resume;
- context hygiene;
- bounded approvals where the owning runtime requires them.

PR #44 in this repository contains the current OpenClaw-native adaptive adapter line. `PACKAGE/CI != HOST_LIVE`; an actual OpenClaw Gateway/profile/agent must still produce runtime receipts.

## Task Goal Intelligence / reasoning lane

PR #43 contains the current upstream-native Task Goal Intelligence v4 harness line. The important convergence is structural, not prompt-volume based:

- thin router;
- deterministic runtime preamble/state;
- progressive disclosure;
- explicit phase/state transitions;
- competing hypotheses and disconfirming evidence;
- fresh completion reverse-walk;
- held-out regression protection.

## Notion + GitHub runtime lane

Notion remains decision/context/research memory. GitHub remains executable truth for code/config/PR/Issue/Actions/exact refs. The Notion `Notion × GitHub Autopilot｜Auto-Invoke` skill now also includes cross-chat research recovery and deliberation routing.

Do not duplicate the runtime owner here. This repository is the **deliberation/evaluation/research lane**; ordinary ChatGPT external control-plane ownership remains in `xq22115/braintrust`.

## Deliberation / debate router

Debate is activated only when competing interpretations can change architecture, write-set, tool route, acceptance, or a high-impact decision.

Minimum independent perspectives:

1. Goal Architect — protects the actual requested end state.
2. Evidence Auditor — checks source independence, freshness and read-back strength.
3. Runtime Engineer — tests whether a proposal can actually run on the owning host.
4. Red Team — seeks counterexamples, false completion and neighboring-task substitution.
5. Integration Maintainer — checks duplicate owners, migration risk, compatibility and rollback.

Optional roles when material: cost/latency, security/boundary, user-workflow/non-interference, eval/regression specialist.

### Debate quality rules

- preserve material disagreement instead of forcing superficial consensus;
- do not count labels/personas as independent model executions;
- do not count agent headcount without runtime/session receipts;
- terminate when acceptance evidence is complete or remaining disagreement cannot change the decision;
- output only decision-relevant deltas back to the canonical owner.

Without independent runtime receipts, this is **multi-perspective deliberation**, not a claim of truly independent multi-model sessions.

## Web / “internal settings” projection boundary

What can be durably strengthened:

- ChatGPT Memory / persistent user context;
- Notion AI Skills and Research/Decision memory;
- GitHub external control-plane contracts, skills, tests and evidence;
- connected-tool routing and read-back discipline when those surfaces are actually available.

What these external artifacts cannot rewrite:

- hidden OpenAI system prompts;
- model weights;
- server-side safety/policy enforcement;
- native account/plan permissions;
- hidden native tool selection.

Therefore the correct measurable interpretation of “strengthen the internal settings” is **stronger persistent routing/context/skill/evidence contracts on surfaces that can actually be loaded**, not a claim that the model’s hidden substrate was modified.

## Acceptance for this convergence lane

`RECOVERED_CONTEXT -> CANONICAL_OWNER_RESOLVED -> LIVE_READBACK -> SYNTHESIZED -> RESEARCH/SKILL_UPDATED -> DEBATE_DELTA_RECORDED -> TASK_EFFECT_VERIFIED`

Any missing state must remain explicit and cannot be relabeled as complete.
