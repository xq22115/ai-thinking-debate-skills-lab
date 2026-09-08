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

Synthesis: debate can help, but raw agent count or debate duration is not the objective. Diversity, topology, selective initiation, selective communication, cost, evidence-weighted adjudication, and resistance to persuasive-but-wrong arguments determine value.

## 2025–2026 semantic / argument reasoning evidence

- Can LLMs Judge Debates? Evaluating Non-Linear Reasoning via Argumentation Theory Semantics (Findings of EMNLP 2025): https://aclanthology.org/2025.findings-emnlp.1159/
  - Natural debates are better modeled as support/attack argument graphs than as a flat sequence alone; longer or disrupted discourse increases ranking errors, motivating explicit graph-aware reasoning.
- Dancing with Critiques: Enhancing LLM Reasoning with Stepwise Natural Language Self-Critique (2025): https://arxiv.org/abs/2503.17363
  - Rich step-level natural-language critique can guide inference better than reducing each step to a scalar score; implication: inspect hinge steps locally instead of only judging the final answer.
- SSR: Socratic Self-Refine for Large Language Model Reasoning (2025): https://arxiv.org/abs/2511.10621
  - Decompose reasoning into verifiable sub-question/sub-answer units, identify unreliable steps, and refine locally.
- Pragmatic Inference Chain (PIC), EMNLP 2025: https://aclanthology.org/2025.emnlp-main.296/
  - Structured pragmatic inference helps with inference-intensive implicit language; implication: distinguish explicit proposition, presupposition/implicature, and context-dependent interpretation.

Synthesis: “deep meaning” should not mean unconstrained mind-reading. A robust procedure separates explicit claim from presupposition, implicature, framing, scope, burden shifts, and strategic discourse function; then binds each inferred layer to text/context and marks uncertain readings as hypotheses.

## Public debate case-study provenance — Cambridge Union, 2025-05-19

- User-provided clip/reference: https://www.youtube.com/watch?v=cHTHYzQ8ErU
- Official full Cambridge Union Q&A/debate upload: https://www.youtube.com/watch?v=dkiM-z0Mzyg

Use: qualitative reasoning-pattern study only, not authority on the disputed political/social claims.

Observed reusable reasoning mechanics include definition locking, claim narrowing, consequence testing, category distinctions, internal-consistency challenges, source/translation challenges, and strategic reframing. The same footage also illustrates failure modes that a truth-seeking system should detect rather than imitate: question substitution, forced binaries, burden asymmetry, definitional capture, and rhetorical confidence being mistaken for evidence.

Consequence: the portable `deep-semantic-debate-reasoning` skill treats rhetoric and epistemic strength as separate axes and requires an update/falsification condition for material claims.
