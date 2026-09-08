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

Synthesis: debate can help, but raw agent count is not the objective. Diversity, topology, selective communication, cost, anti-sycophancy, and evidence-based adjudication determine value.

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

## Verifiable Process Reward Models — Findings of ACL 2026
https://aclanthology.org/2026.findings-acl.1611/

Evidence: VPRMs replace purely neural step scoring with deterministic rule-based verification for checkable intermediate decisions in a structured medical evidence-synthesis task. The reported experiments improve coherence between intermediate decisions and final labels, with gains over outcome-only verifiable rewards in that domain.

Consequence: when intermediate obligations are genuinely programmatically checkable, deterministic process verification should be preferred over asking a neural judge to infer rule adherence from prose. Do not generalize this to domains lacking a valid executable process oracle.

## VerifyBench — ICLR/AAAI 2026 verifier benchmarks
https://proceedings.iclr.cc/paper_files/paper/2026/hash/e812af67a942c21dd0104bd929f99da1-Abstract-Conference.html
https://ojs.aaai.org/index.php/AAAI/article/view/40448

Evidence: current reference-based/specialized/general verifiers retain substantial error on difficult cases. The AAAI benchmark reports sensitivity to response structure and cross-domain tradeoffs; no single verifier is uniformly reliable across all conditions.

Consequence: `ONE_VERIFIER != GROUND_TRUTH`. Evaluate verifier robustness by task family, structure, and cross-domain transfer; preserve disagreement between verifiers rather than collapsing it into one scalar.

## Reward hacking in agentic LLM systems — 2026 survey
https://link.springer.com/article/10.1007/s44163-026-01980-z

Evidence: review synthesizes feature-level, representation-level, evaluator-level, and environment-level reward-hacking surfaces, including verbosity/sycophancy shortcuts, judge/verifier gaming, benchmark overfitting, test exploitation, and reward-channel manipulation.

Consequence: treat tests, hidden variants, reference fields, reward channels, and audit logs as privileged verification assets when runtime separation is possible. A visible evaluator is itself an attack/optimization surface.

## Causal Reward Adjustment — AAAI 2026
https://ojs.aaai.org/index.php/AAAI/article/view/40584

Evidence: studies reward hacking in process-reward-model-guided reasoning and attributes failures partly to confounding semantic features; reports improvements from causal adjustment in the studied math-reasoning setup.

Consequence: high PRM score is not equivalent to logical correctness. Treat reward-model features as potentially confounded proxies and test with alternative/deterministic verification where possible.

## Logic-Grounded Metamorphic Testing — 2026
https://www.sciencedirect.com/science/article/pii/S0950705126010506

Evidence: proposes logic-grounded metamorphic relations derived from formal equivalences to test reasoning consistency under semantics-preserving transformations, addressing limitations of static benchmarks.

Consequence: add metamorphic invariance tests for paraphrase, candidate order, prestige masking, verbosity normalization, quantifier equivalence, causal graph isomorphism, and evidence-provenance duplication.

## 2026 synthesis

The current evidence supports a layered reasoning-and-verification design:

`evidence sufficiency/provenance -> semantic/QUD normalization -> causal/abductive model when needed -> competing hypotheses -> discriminating test -> selective multi-agent deliberation -> bias-resistant judge -> verifier robustness/metamorphic checks -> VOI stop rule -> calibrated conclusion`

The repeated research signal is negative as well as positive: more tokens, more sources, more agents, more confidence machinery, more learned-verifier scores, and more rounds do **not** monotonically improve reliability. The system should optimize for independent evidence, discrimination, calibration, target-bound deterministic checks where available, evaluator robustness, and decision value rather than visible reasoning/evaluation volume.
