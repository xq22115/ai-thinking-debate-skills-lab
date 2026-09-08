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

Synthesis: debate can help, but raw agent count or debate duration is not the objective. Diversity, topology, selective initiation, selective communication, calibrated confidence, cost, evidence-weighted adjudication, and resistance to persuasive-but-wrong arguments determine value. Consensus itself is not a reliable target; preserving a better-supported minority hypothesis can be more valuable than forcing convergence.

## 2025–2026 semantic / argument reasoning evidence

- Can LLMs Judge Debates? Evaluating Non-Linear Reasoning via Argumentation Theory Semantics (Findings of EMNLP 2025): https://aclanthology.org/2025.findings-emnlp.1159/
  - Natural debates are better modeled as support/attack argument graphs than as a flat sequence alone; longer or disrupted discourse increases ranking errors, motivating explicit graph-aware reasoning.
- Can LLMs Really Judge? A Progressive Argumentation-Mining Framework for Distinguishing Understanding from Aggregation (Findings of ACL 2026): https://aclanthology.org/2026.findings-acl.1473/
  - Generative correctness does not imply discriminative judgment. Progressive argument mining and selective retention can expose whether a model can distinguish a well-supported rationale from plausible noise instead of merely aggregating context.
- The Thin Line Between Comprehension and Persuasion in LLMs (Findings of ACL 2026): https://aclanthology.org/2026.findings-acl.329/
  - LLMs can maintain coherent persuasive debates while still failing on deeper dialogical comprehension, including argument quality and supporting-premise structure. Consequence: persuasion and structural comprehension need separate evaluation axes.
- Truth or Sophistry? LoFa: A Benchmark for LLM Robustness Against Logical Fallacies (ACL 2026): https://aclanthology.org/2026.acl-long.1112/
  - Fallacy recognition alone is insufficient; models must resist sustained persuasive pressure from fallacious arguments. Consequence: evaluate robustness under multi-round manipulation, while avoiding the fallacy fallacy (a bad argument does not by itself make its conclusion false).
- This House Debates AI: Evaluating a Language Model in Oxford-Style Debates against Human Experts (LREC 2026): https://aclanthology.org/2026.lrec-1.215/
  - Large models can be competitive with experienced human debaters across multi-turn Oxford-style debate, increasing the need to distinguish rhetorical competence from epistemic reliability.
- Dialogue is the Plan: From Interface to Joint Action in Agentic AI (ACL 2026): https://aclanthology.org/2026.acl-short.63/
  - Treating language only as an interface misses common ground, grounding, repair, and shared commitments. Consequence: dialogue state should participate in the planning loop, with explicit commitment tracking and repair rather than relying on an implicit transcript summary.
- Multi-Agent LLM Debate Unveils the Premise Left Unsaid (ArgMining 2025): https://aclanthology.org/2025.argmining-1.6/
  - Structured debate can improve implicit-premise recovery when agents refine predictions in response to opposing views. Forcing assigned stances degrades performance, motivating evidence-responsive stance freedom instead of role rigidity.
- Overview of the Critical Questions Generation Shared Task (ArgMining 2025): https://aclanthology.org/2025.argmining-1.23/
  - Critical-question generation remains difficult; top systems benefited from argumentation-scheme information. Consequence: do not equate question volume with question quality.
- ELLIS Alicante at CQs-Gen 2025 (ArgMining 2025): https://aclanthology.org/2025.argmining-1.31/
  - Generate multiple candidate critical questions and use a separate selector/judge to choose the most relevant ones. Consequence: cross-examination should rank candidate questions by usefulness/discriminative value before asking them.
- ARG2ST at CQs-Gen 2025 (ArgMining 2025): https://aclanthology.org/2025.argmining-1.29/
  - Usefulness-based selection consistently improves over unfiltered LLM question generation. Consequence: the reasoning system should explicitly score hinge relevance, answerability, evidence targeting, and frame neutrality.
- Toward Reasonable Parrots: Why Large Language Models Should Argue with Us by Design (ArgMining 2025): https://aclanthology.org/2025.argmining-1.3/
  - Position paper argues for argumentative dialogue grounded in relevance, responsibility, and freedom rather than treating the model as an answer oracle. Consequence: reasoning quality includes responsible dialogical moves and freedom to revise a stance when evidence changes.
- Limited Generalizability in Argument Mining: State-Of-The-Art Models Learn Datasets, Not Arguments (ACL 2025): https://aclanthology.org/2025.acl-long.1164/
  - Strong benchmark performance can rely on lexical shortcuts and degrade sharply on unseen datasets. Consequence: structural reasoning tests should paraphrase wording, swap domains, and remove familiar lexical cues before claiming generalization.
- Argument Mining with Fine-Tuned Large Language Models (COLING 2025): https://aclanthology.org/2025.coling-main.442/
  - End-to-end argument mining can jointly identify argumentative units and relations. Consequence: evaluation should score both node identification and relation recovery rather than only final labels.
- Can Large Language Models perform Relation-based Argument Mining? (COLING 2025): https://aclanthology.org/2025.coling-main.569/
  - Support/attack/neither relation classification is a distinct capability. Consequence: a rebuttal should be credited only when it attacks a proposition that materially supports the target conclusion.
- Dancing with Critiques: Enhancing LLM Reasoning with Stepwise Natural Language Self-Critique (2025): https://arxiv.org/abs/2503.17363
  - Rich step-level natural-language critique can guide inference better than reducing each step to a scalar score; implication: inspect hinge steps locally instead of only judging the final answer.
- SSR: Socratic Self-Refine for Large Language Model Reasoning (2025): https://arxiv.org/abs/2511.10621
  - Decompose reasoning into verifiable sub-question/sub-answer units, identify unreliable steps, and refine locally.
- Pragmatic Inference Chain (PIC), EMNLP 2025: https://aclanthology.org/2025.emnlp-main.296/
  - Structured pragmatic inference helps with inference-intensive implicit language; implication: distinguish explicit proposition, presupposition/implicature, and context-dependent interpretation.

Synthesis: “deep meaning” should not mean unconstrained mind-reading. A robust procedure separates explicit claim from presupposition, implicature, framing, scope, burden shifts, speech act, strategic setup, and update condition; then binds each inferred layer to text/context and marks uncertain readings as hypotheses. For debate quality, add structural diagnostics: recover support/attack/dependency relations, distinguish common ground from temporary assumptions, identify missing premises, rank critical questions by discriminative value, preserve evidence-responsive stance revision, and test structural generalization under paraphrase/domain shift. If these fail while eloquence improves, the result is rhetorical gain rather than reasoning gain.

## Public debate case-study provenance — Cambridge Union, 2025-05-19

- User-provided clip/reference: https://www.youtube.com/watch?v=cHTHYzQ8ErU
- Official full Cambridge Union Q&A/debate upload: https://www.youtube.com/watch?v=dkiM-z0Mzyg

Use: qualitative reasoning-pattern study only, not authority on the disputed political/social claims.

Observed reusable reasoning mechanics include definition locking, claim narrowing, consequence testing, category distinctions, internal-consistency challenges, source/translation challenges, strategic reframing, and questions that alter the opponent's commitment set or answer space. The same footage also illustrates failure modes that a truth-seeking system should detect rather than imitate: question substitution, forced binaries, burden asymmetry, definitional capture, rhetorical confidence being mistaken for evidence, and temporary/pressured commitments being treated as genuine agreement.

Consequence: the portable `deep-semantic-debate-reasoning` skill treats rhetoric and epistemic strength as separate axes, tracks dialogue-state delta plus common-ground status, recovers implicit premises cautiously, ranks critical questions by information value, and requires an update/falsification condition for material claims.
