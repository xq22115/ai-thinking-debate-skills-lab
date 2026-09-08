# 2026 Current Evidence

Access date: 2026-09-09

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

Current 2026-08-18 commit activity included changes touching memory bounds/reload, state/session claims, skills GitHub identity, write-scoped worktrees, terminal delivery outcomes, and Claude subagent event isolation.

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

Synthesis: debate can help, but raw agent count or debate duration is not the objective. Diversity, topology, selective initiation/communication, calibrated confidence, cost, anti-sycophancy, evidence-weighted adjudication, minority preservation, and resistance to persuasive-but-wrong arguments determine value.

## BayesBench — sequential evidence accumulation, 2026-06-29
https://arxiv.org/abs/2606.30850

Evidence: evaluates multi-turn Bayesian estimation/prediction and latent-framed prediction across multiple LLMs. Scaling improves latent inference and evidence accumulation, but the improvement does not reliably transfer to downstream prediction.

Consequence: do not score only the final answer. Track belief trajectory, evidence delta, and whether updated latent beliefs actually change the downstream forecast coherently.

## Evidence Sufficiency Benchmark — answer/abstention calibration, 2026
https://doi.org/10.32604/cmc.2026.086343

Evidence: controlled evidence conditions from full support through partial, irrelevant, absent, and conflicting evidence. Evaluated models frequently over-answer under conflicting evidence; recognizing conflict is harder than recognizing no context.

Consequence: add an evidence-sufficiency gate before definitive answering. `CONFLICT_AWARE_ANSWERING` is insufficient when the decisive contradiction remains unresolved.

## AbstentionBench — reasoning models and unanswerable questions, 2025
https://arxiv.org/abs/2506.09038
https://github.com/facebookresearch/AbstentionBench

Evidence: broad abstention benchmark across multiple unanswerable/underspecified scenarios; reports that reasoning-oriented tuning/behavior does not automatically improve abstention and can worsen over-answering.

Consequence: treat abstention/selective answering as a separate capability from raw reasoning accuracy.

## RMCB — confidence estimation for reasoning models, EACL 2026
https://aclanthology.org/2026.eacl-long.78/

Evidence: large benchmark across high-stakes and reasoning datasets. Reports a persistent trade-off between discrimination and calibration; no single confidence-estimation method dominates both.

Consequence: `confidence estimator` must not be treated as a universal scalar oracle. Evaluate calibration and discrimination separately on the target task class.

## Human's Last Exam / expert-level academic benchmark, Nature 2025/2026
https://www.nature.com/articles/s41586-025-09962-4

Evidence: frontier models remain poorly calibrated on difficult expert-level questions and can answer incorrectly with high confidence. The paper also reports diminishing and eventually reversing returns at very large reasoning-token budgets in its analyzed setup.

Consequence: `MORE_REASONING != BETTER_CALIBRATION`. Use information-gain/VOI stop rules rather than unconditional reasoning-token escalation.

## Calibrating LLMs with sample consistency, AAAI 2025
https://ojs.aaai.org/index.php/AAAI/article/view/34120

Evidence: confidence can be estimated from distributions of multiple sampled generations, but sample consistency must be interpreted carefully.

Consequence: cluster semantically equivalent answers and account for tasks with multiple valid answers; `STRING_DISAGREEMENT != EPISTEMIC_DISAGREEMENT`.

## Multiple-correct-answer calibration, 2026
https://arxiv.org/abs/2602.07842

Evidence: common training-free confidence methods can become miscalibrated when multiple answers are valid; semantic aggregation improves this setting in the reported experiments.

Consequence: answer diversity is not automatically uncertainty. Confidence aggregation should operate over semantic hypotheses, not raw strings.

## Conflicting evidence in RAG — COLM 2025
https://openreview.net/pdf?id=z1MHB2m3V9

Evidence: RAMDocs studies ambiguity, misinformation, noise, and conflicting retrieved evidence jointly; multi-agent reconciliation can help in the studied setup.

Consequence: retrieved documents need conflict/noise classification before aggregation. Multi-agent debate is useful only when evidence roles are distinct and adjudication remains evidence-weighted.

## Source reliability under conflicting evidence — IJCAI/EMNLP 2025
https://www.ijcai.org/proceedings/2025/1073
https://aclanthology.org/2025.emnlp-main.1738/

Evidence: RAG reliability drops when conflicting sources differ in credibility; source-reliability-aware methods improve conflict handling in reported experiments.

Consequence: relevance alone is insufficient. Track source reliability, provenance, and independence before evidence aggregation.

## Multi-document RAG load — Findings of EMNLP 2025
https://aclanthology.org/2025.findings-emnlp.1064/

Evidence: increasing the number of documents can degrade performance even when total context length and relevant-information position are controlled.

Consequence: more retrieved documents are not automatically better. De-duplicate and select by decision value rather than maximizing document count.

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

## Behavioral evaluation / judge reliability evidence

### Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge — IJCNLP-AACL 2025
https://aclanthology.org/2025.ijcnlp-long.18/

Evidence: across many judges/tasks, answer position can systematically influence LLM-as-a-Judge decisions; the effect is not explainable as random noise alone.

Consequence: pairwise preference claims should use blinded labels and order swaps, and disagreement should be reported rather than silently averaged away.

### Judging with Many Minds: Do More Perspectives Mean Less Prejudice? — Findings of EMNLP 2025
https://aclanthology.org/2025.findings-emnlp.941/

Evidence: multi-agent judge/debate frameworks can amplify position, verbosity, chain-of-thought and bandwagon biases after interaction instead of automatically canceling them.

Consequence: `more judges` or `judge debate` is not itself a reliability guarantee. Preserve raw judge outputs, independent scores, bias checks, and dissent where material.

### LRBench and Judge-R1: Principled Evaluation and Training of LLM-Based Judges for Long-Context Reasoning — Findings of ACL 2026
https://aclanthology.org/2026.findings-acl.2029/

Evidence: long-context reasoning evaluation benefits from fine-grained principle-violation labels rather than final-answer preference alone.

Consequence: the dialogue-state harness records dimension-level scores and explicit blocking errors instead of collapsing evaluation immediately to one scalar.

### Don't Judge Code by Its Cover: Exploring Biases in LLM Judges for Code Evaluation — Findings of EACL 2026
https://aclanthology.org/2026.findings-eacl.70/

Evidence: judges can remain vulnerable to systematic presentation biases even when asked to generate tests before scoring.

Consequence: a judge-generated rationale or test is not sufficient proof of judge reliability. Protect evaluation with structured criteria, independent evidence when available, and explicit judge metadata.

## 2026 synthesis

The current evidence supports a layered reasoning design:

`evidence sufficiency/provenance -> semantic/QUD normalization -> dialogue-state/common-ground repair when multi-turn commitments matter -> causal/abductive model when needed -> competing hypotheses -> discriminating test -> selective multi-agent deliberation -> bias-resistant judge -> VOI stop rule -> calibrated conclusion`

The canonical semantic owner remains `semantic-argument-microscope`. Progressive references extend it only when needed:

- `ARGUMENT_SCHEMES.md` — inferential scheme + decision-critical question selection;
- `CAUSAL_ABDUCTIVE_REASONING.md` — causal/explanatory/interventional/counterfactual reasoning;
- `DIALOGUE_STATE.md` — multi-turn shared commitments, temporary grants, answer-space/criterion shifts, common-ground repair, provenance laundering, and structural-transfer checks.

Behavioral evaluation is also evidence-gated. `semantic-dialogue-state-eval-protocol.md` plus `run_semantic_dialogue_state_eval.py` freeze four comparable arms, prompt/instruction hashes, response identities, blind judge tasks, dimension-level scoring, blocking errors, same-model-judge metadata, and treatment regressions. The harness intentionally does not make provider calls by itself.

The repeated research signal is negative as well as positive: more tokens, more sources, more agents, more rounds, and more judges do **not** monotonically improve reliability. Optimize for independent evidence, discrimination, calibration, structural comprehension, decision value, and auditable state changes rather than visible reasoning volume.

Static fixtures, CI asset validation, and harness self-tests remain packaging/execution-harness evidence only; target-model behavior, independent judge validity, and host-live routing require separate execution evidence.
