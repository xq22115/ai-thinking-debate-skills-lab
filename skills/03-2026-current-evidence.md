# 2026 Current Evidence

Access date: 2026-09-08

## OpenAI — Agents SDK, 2026-04-15
https://openai.com/index/the-next-evolution-of-the-agents-sdk/

Evidence: model-native harness, sandbox execution, harness/compute separation, snapshot/rehydration, isolated subagent/container routing.

Consequence: durable execution should be implemented as external state + resumable harness, not only longer prompting.

## Anthropic — Trustworthy agents in practice, 2026-04-09
https://www.anthropic.com/research/trustworthy-agents

Evidence: plan-level oversight, autonomy/prompt-injection risks, subagent steering/visibility concerns.

Consequence: oversight at strategy/checkpoint boundaries with subagent observability.

## Anthropic — Claude Code expertise study, 2026-06-16
https://www.anthropic.com/research/claude-code-expertise

Evidence: large real-world session study; human planning vs agent execution split; verifiable outcomes such as tests/commits matter.

## Agent Skills
https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
https://github.com/anthropics/skills

Evidence: dynamic, folder-based procedural capabilities centered on `SKILL.md`.

## MCP 2026-07-28
https://blog.modelcontextprotocol.io/posts/2026-07-28/
https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/index.mdx

Evidence: stateless core, per-request capability negotiation, MRTR, extensions, auth hardening, task/deprecation changes.

Consequence: audit any 2025-era session/task assumptions before reuse.

## OpenAI Agents Python
https://github.com/openai/openai-agents-python

Use current SDK primitives rather than old Swarm-era assumptions.

## OpenClaw
https://github.com/openclaw/openclaw

Current 2026-08-18 commit activity includes changes touching memory bounds/reload, state/session claims, skills GitHub identity, write-scoped worktrees, terminal delivery outcomes, and Claude subagent event isolation.

Consequence: pin exact version/commit before applying configs.

## 2026 multi-agent/debate research

- SDRL: https://arxiv.org/abs/2601.22297
- Diversity-aware message retention: https://arxiv.org/abs/2603.20640
- Pareto-optimal multi-agent test-time scaling: https://arxiv.org/abs/2605.01566
- Social reasoning / collective truth-seeking: https://arxiv.org/abs/2605.30391
- SELENE — Selective and Evidence-Weighted LLM Debating (EACL 2026): https://aclanthology.org/2026.eacl-industry.7/
- Persuasion-driven adversarial influence in multi-agent LLM debate (Scientific Reports 2026): https://www.nature.com/articles/s41598-026-42705-7
- Demystifying Multi-Agent Debate: The Role of Confidence and Diversity (Findings of ACL 2026): https://aclanthology.org/2026.findings-acl.1694/
- Free-MAD: Consensus-Free Multi-Agent Debate (Findings of ACL 2026): https://aclanthology.org/2026.findings-acl.1600/

Synthesis: debate can help, but raw agent count or debate duration is not the objective. Diversity, topology, selective initiation/communication, calibrated confidence, cost, evidence-weighted adjudication, minority preservation, and resistance to persuasive-but-wrong arguments determine value.

## Semantic argument / dialogue-state evidence

### Dialogue is the Plan: From Interface to Joint Action in Agentic AI — ACL 2026
https://aclanthology.org/2026.acl-short.63/

Evidence: treating language only as an interface misses common ground, grounding, repair, and shared commitments involved in joint action.

Consequence: long multi-turn argument should not rely only on a flat transcript summary. When shared commitments materially affect later reasoning, preserve explicit common-ground state and repair corrupted assumptions before continuing.

### Multi-Agent LLM Debate Unveils the Premise Left Unsaid — ArgMining 2025
https://aclanthology.org/2025.argmining-1.6/

Evidence: structured debate can improve implicit-premise recovery by exposing alternative warrants, while forced assigned stances can degrade performance.

Consequence: use debate as a challenger for ambiguous bridges, not as a command to defend a role after its evidence collapses.

### Critical Questions Generation Shared Task — ArgMining 2025
https://aclanthology.org/2025.argmining-1.23/
https://aclanthology.org/2025.argmining-1.31/
https://aclanthology.org/2025.argmining-1.29/

Evidence: critical-question generation remains difficult; scheme information and usefulness-based candidate selection improve the quality of questions.

Consequence: `ARGUMENT_SCHEMES.md` should generate candidate questions and rank a small number by decision value rather than rewarding question volume.

### The Thin Line Between Comprehension and Persuasion in LLMs — Findings of ACL 2026
https://aclanthology.org/2026.findings-acl.329/

Evidence: models can sustain coherent persuasive dialogue while still failing on deeper dialogical/argument comprehension such as supporting-premise structure and argument quality.

Consequence: rhetorical success and structural comprehension require separate evaluation. Audience reaction, fluency, confidence, or verbal dominance cannot substitute for correct support/attack targeting or common-ground tracking.

### Can LLMs Judge Debates? Evaluating Non-Linear Reasoning via Argumentation Theory Semantics — Findings of EMNLP 2025
https://aclanthology.org/2025.findings-emnlp.1159/

Evidence: natural debate is non-linear and is better represented through support/attack relations than flat turn ordering alone; longer/disrupted discourse raises reasoning errors.

Consequence: use argument graphs/QUD/crux plus dialogue-state repair when turn history changes available premises.

### Limited Generalizability in Argument Mining: State-Of-The-Art Models Learn Datasets, Not Arguments — ACL 2025
https://aclanthology.org/2025.acl-long.1164/

Evidence: strong benchmark scores can rely on lexical/data-set shortcuts and degrade on unseen domains.

Consequence: semantic/argument reasoning must survive paraphrase, domain swaps, style changes, and removal of familiar lexical cues before being treated as structurally general.

### Relation-based and end-to-end Argument Mining — COLING 2025
https://aclanthology.org/2025.coling-main.569/
https://aclanthology.org/2025.coling-main.442/

Evidence: identifying argumentative units and classifying support/attack/neither relations are distinct capabilities.

Consequence: a rebuttal is structurally successful only if it attacks a proposition/warrant that materially supports the target conclusion; a polished neighboring response is not enough.

### Pragmatic Inference Chain — EMNLP 2025
https://aclanthology.org/2025.emnlp-main.296/

Evidence: structured pragmatic inference improves reasoning over inference-intensive implicit language.

Consequence: preserve the literal/pragmatic boundary and do not promote a plausible implicature or presupposition into established world evidence.

## Semantic dialogue-state synthesis

The canonical semantic owner remains `semantic-argument-microscope`. Its core handles literal/pragmatic boundaries, warrants, QUD/crux, defeaters, argument relations, stance freedom, and epistemic-vs-rhetorical separation. Progressive references extend it only when needed:

- `ARGUMENT_SCHEMES.md` — inferential scheme + decision-critical question selection;
- `CAUSAL_ABDUCTIVE_REASONING.md` — causal/explanatory/interventional/counterfactual reasoning;
- `DIALOGUE_STATE.md` — multi-turn shared commitments, temporary grants, answer-space/criterion shifts, common-ground repair, provenance laundering, and structural-transfer checks.

The important boundary is architectural as well as epistemic: prefer one semantic owner and demand-loaded references rather than multiple overlapping skills. Static fixtures and CI asset validation remain packaging evidence only; target-model behavior and host-live routing require separate execution evidence.
