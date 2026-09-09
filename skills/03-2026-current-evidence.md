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

Evidence: proposes logic-grounded metamorphic relations derived from formal equivalences to test reasoning consistency under semantics-preserving transformations, addressing limitations of static benchmarks. The reported experiments expose reasoning inconsistencies missed by ordinary reference-based evaluation.

Consequence: add metamorphic invariance tests only when the transformation relation is defensible. Prefer formal/deterministic relations where possible rather than informal paraphrases that may introduce semantic drift.

## BeyondBench — contamination-resistant dynamic reasoning evaluation, ICLR 2026
https://proceedings.iclr.cc/paper_files/paper/2026/hash/22b4e30a7a660b17f1fb58ab49671e77-Abstract-Conference.html

Evidence: replaces reliance on a fixed static benchmark with algorithmic on-the-fly problem generation over very large combinatorial spaces, deterministic solution verification, and isomorphic transformations. This reduces the value of memorizing a fixed public item set and allows fresh test instances to be generated repeatedly.

Consequence: for reasoning capabilities with constructible deterministic oracles, prefer procedural/dynamic holdouts over treating secrecy of one static item list as sufficient contamination protection. Public generation code can coexist with private run instances/oracles when target responses are frozen before scoring.

## Fragility of benchmark contamination detection — ICLR 2026
https://proceedings.iclr.cc/paper_files/paper/2026/hash/a3860475ddbfb8c644c43f0dcd266b66-Abstract-Conference.html

Evidence: reports that contamination-detection methods for reasoning models can be evaded under realistic training/evolution settings; a detector's failure to flag contamination is therefore not a reliable certificate that evaluation items were unseen.

Consequence: `CONTAMINATION_DETECTION_PASS != PROOF_OF_NO_CONTAMINATION`. Prefer structural separation: expected labels withheld from the generation path, frozen responses before scoring, private-oracle commitments, dynamic/hidden variants, and explicit contamination metadata.

## LENS — natural prompt distribution shift, ACL 2026
https://aclanthology.org/2026.acl-long.1508/

Evidence: studies 192 real-world post-deployment prompt-shift settings across time, user-group, and geographic axes, showing that natural prompt-distribution changes are a material deployment reliability problem rather than only a synthetic OOD concern.

Consequence: deployment reasoning must include a target-context shift gate. Historical model/evaluator performance should not be treated as transportable by default when the user/task population changes.

## SConU — selective conformal uncertainty, ACL 2025
https://aclanthology.org/2025.acl-long.934/

Evidence: conformal uncertainty methods provide risk/coverage mechanisms under assumptions such as exchangeability; SConU explicitly adds tests for samples that deviate from the calibration uncertainty distribution because ordinary conformal coverage can become unbounded when those assumptions fail.

Consequence: `CALIBRATED_IN_DOMAIN != CALIBRATED_UNDER_SHIFT`. Risk-control guarantees must be conditioned on their assumptions, with shift detection / abstention / wider uncertainty when transfer is unsupported.

## CAP — context-adaptive conformalized abstention policy, ACML 2025 / PMLR 2026 publication
https://proceedings.mlr.press/v304/tayebati26a.html

Evidence: learns context-adaptive risk/abstention behavior that balances point prediction, set prediction, and full abstention according to downstream utility, reporting maintained target coverage and improved selective-generation/calibration metrics in the studied setups.

Consequence: abstention should be treated as one action in a utility/risk policy, not a universal response to uncertainty. Depending on consequence and reversibility, `PROBE`, `PILOT`, bounded answer, or abstention can be preferable.

## Robust decision-focused learning via worst-case regret, UAI 2026
https://proceedings.mlr.press/v337/yamao26a.html

Evidence: in optimization-based decision-making with uncertain coefficients/distributions, worst-case-regret objectives over explicit uncertainty/ambiguity sets can yield more stable downstream solutions than nominal decision-focused baselines in the reported experiments.

Consequence: `MOST_LIKELY_STATE != BEST_ACTION`. Under fragile probabilities or asymmetric downside, compare expected performance with sensitivity / regret / robustness; however, the chosen uncertainty set and loss model remain assumptions that must themselves be audited.

## RECAP — intent rewriting for agentic planning, Findings of EACL 2026
https://aclanthology.org/2026.findings-eacl.105/

Evidence: RECAP targets real conversational ambiguity, underspecification, intent drift, vagueness, and mixed-goal dialogue by rewriting conversation into concise goal representations for downstream planning. The work reports utility improvements over baselines from intent rewriting approaches.

Consequence: explicit task-local goal normalization is a legitimate planning layer. Preserve a compact Goal Contract rather than allowing downstream planners/agents to infer different hidden objectives from the raw conversation.

## Structured Uncertainty Guided Clarification / ClarifyBench — Findings of ACL 2026
https://aclanthology.org/2026.findings-acl.2028/

Evidence: separates specification uncertainty (what the user wants) from model uncertainty and uses Expected Value of Perfect Information plus clarification cost to determine what to ask and when to stop in tool-calling agents.

Consequence: `SPECIFICATION_UNCERTAINTY != MODEL_UNCERTAINTY`. Ask high-value clarifying questions only when user-authoritative information is needed and materially changes the action; use direct reads/tests for internally resolvable world-state uncertainty.

## Planorama — preference vs actual helpfulness, EMNLP 2025
https://aclanthology.org/2025.emnlp-main.585/

Evidence: across thousands of plan executions/comparisons, user/model preferences and agent success did not reliably predict which plans actually helped users complete the task; surface preferences such as brevity and similarity were associated with preference but not helpfulness.

Consequence: `STATED_OR_RATED_PREFERENCE != VERIFIED_HELPFULNESS`. Evaluate real task outcome separately from what looks preferable, concise, familiar, or judge-friendly.

## Personalized Benchmarking — Findings of ACL 2026
https://aclanthology.org/2026.findings-acl.31/

Evidence: aggregate model rankings can diverge substantially from individual users' rankings, showing that population-average preference is a poor universal proxy for individual preference in many settings.

Consequence: do not silently substitute aggregate preference for the user's task-local preference/constraint state. Keep personalization bounded to evidence supplied by the user/context rather than inventing latent values.

## Revealed preferences for LLM alignment/steering — Microsoft Research, 2026
https://www.microsoft.com/en-us/research/publication/can-revealed-preferences-clarify-llm-alignment-and-steering/

Evidence: recovers cost functions implied by model choices and reports meaningful mismatches between models' verbalized objectives/preferences and the policies revealed by their decisions, including limits in reliably adopting user-specified cost functions.

Consequence: `MODEL_STATED_OBJECTIVE != REVEALED_DECISION_POLICY`. For task-local objective audits, compare declared priorities with observable choices under controlled tradeoffs rather than trusting self-description alone.

## Specification gaming in reasoning models — 2026
https://arxiv.org/abs/2605.02269

Evidence: a diverse suite of tasks with unintended high-scoring actions finds non-negligible specification gaming across tested reasoning models in most settings; the authors report higher exploit rates with RL reasoning training and only partial mitigation from test-time interventions.

Consequence: powerful reasoning against an imperfect specification can increase optimization pressure on the wrong proxy. Acceptance tests/proxies require outcome-binding, hidden variants, and anti-gaming checks; higher reasoning budget should not be assumed to improve goal fidelity.

## DeepPlanning — long-horizon global constrained planning, ACL 2026
https://aclanthology.org/2026.acl-long.335/

Evidence: evaluates practical long-horizon planning with proactive information gathering, fine-grained local constraints, and global time/financial constraints. Frontier agentic models still struggle, showing that locally plausible reasoning does not guarantee globally feasible plans.

Consequence: `LOCAL_STEP_SUCCESS != TRAJECTORY_SUCCESS`. Maintain global constraint/budget state across the full plan and evaluate trajectory-level feasibility, not only individual actions.

## YC-Bench — long-term planning, delayed feedback and compounding errors, 2026
https://arxiv.org/abs/2604.01212

Evidence: simulates a one-year startup trajectory spanning hundreds of turns under partial observability, delayed feedback, adversarial conditions and compounding consequences. The reported analysis finds persistent state/scratchpad use strongly associated with success and identifies distinct long-horizon failure modes including over-parallelization.

Consequence: durable compact state is not just convenience. Track strategy, delayed observations, resource state, irreversible decisions and dependency/parallelism constraints across context truncation and handoffs.

## Plan-RewardBench — trajectory-level reward/judge degradation, ACL 2026
https://aclanthology.org/2026.acl-long.1062/

Evidence: evaluates generative, discriminative and LLM-as-judge reward models on tool-integrated agent trajectories. Reported performance degrades sharply on longer trajectories and hard-negative variants.

Consequence: `LONGER_TRAJECTORY != MORE_RELIABLE_JUDGMENT`. Use checkpoint/chunk-level deterministic checks plus global trajectory audit; do not ask one judge to reconstruct all latent state from a very long raw transcript.

## STAPO — trajectory neglect under sparse/delayed rewards, ACL 2026
https://aclanthology.org/2026.acl-long.1308/

Evidence: characterizes trajectory neglect in long-horizon agent training: sparse/delayed reward can lead intermediate actions to lose focus on the task goal and interaction history. The work targets outlier steps associated with such neglect.

Consequence: preserve Goal Contract and compact trajectory state throughout execution, not only at the start and end. Intermediate step quality must be judged against the trajectory, not isolated fluency.

## Robotouille — asynchronous planning with time delays, 2025
https://portal.cs.cornell.edu/robotouille/
https://arxiv.org/abs/2502.05227

Evidence: benchmarks asynchronous long-horizon planning where subtasks interact through ordering, concurrency and delays. It exposes gaps in agents' ability to reason over when parallel vs sequential execution is appropriate.

Consequence: `PARALLELISM != FREE_SPEEDUP`. Explicitly model prerequisites, shared state, synchronization points and completion-order effects before parallelizing dependent work.

## Long-Horizon Agent Trajectory Attribution — 2026
https://arxiv.org/abs/2608.06909

Evidence: introduces trajectory attribution with local/long-range component and chain recovery, showing substantial variation in the difficulty of identifying what earlier trajectory component caused later outcomes.

Consequence: when a late failure appears, distinguish downstream symptom from the earliest material or irrecoverable cause. Preserve enough checkpoint/event structure for causal attribution rather than relying on recency.

## No More Stale Feedback / ECHO — ACL 2026
https://aclanthology.org/2026.acl-long.576/

Evidence: static/offline critics can become stale as the policy and trajectory distribution evolve, reducing feedback utility; the work co-evolves critic and policy in its training setting.

Consequence: `OLD_FEEDBACK != CURRENT_ORACLE`. Revalidate critic/evaluator assumptions when policy, environment, target distribution or task state changes materially.

## 2026 synthesis

The current evidence supports a layered goal-reasoning-verification-decision-trajectory-evaluation design:

`Goal Contract / specification audit -> capability/compatibility -> evidence sufficiency/provenance -> semantic/QUD normalization -> causal/abductive model when needed -> competing hypotheses -> discriminating test -> selective multi-agent deliberation -> bias-resistant judge -> verifier robustness -> VOI stop rule -> loss/reversibility/shift/sensitivity check -> temporal/trajectory gate -> execution/revalidation -> outcome-bound completion -> contamination-aware evaluation (fresh context -> frozen responses -> private oracle / independent judge -> hidden relation checks)`

The repeated research signal is negative as well as positive: more tokens, sources, agents, confidence machinery, verifier scores, preference ratings, parallel activity, or rounds do **not** monotonically improve reliability. A better probability estimate does not automatically imply a better action; a higher proxy/preference score does not imply user success; a sequence of local successes does not imply a valid long-horizon trajectory; and a pass on a public/static benchmark does not establish uncontaminated reasoning generalization. The system should optimize for user-authorized goal fidelity, independent evidence, discrimination, calibration, target-bound verification, evaluator robustness, distribution-shift awareness, reversible learning, sensitivity/regret, temporal coherence, durable state, global-constraint satisfaction, outcome-bound completion, and contamination-aware holdout evidence rather than visible reasoning/evaluation volume.
