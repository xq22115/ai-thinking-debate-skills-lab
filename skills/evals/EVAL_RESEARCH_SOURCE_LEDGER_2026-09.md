# Evaluation Research Source Ledger — 2026-09

Status: `SCREENED_100_UNIQUE_SOURCE_GROUPS`
Updated: 2026-09-10

## Scope

This ledger supports the reasoning-evaluation workstream. It prioritizes 2026-06 through 2026-09 evidence about evaluation validity, benchmark contamination, dynamic/live benchmarks, LLM-as-a-judge reliability, verifier robustness, calibration/abstention, agent evaluation, execution provenance, metamorphic testing, reproducibility, and reward/verifier hacking.

Counting rule: one source group per unique canonical URL below. Mirrors, publisher/arXiv duplicates, and repeated metadata records are not counted twice. Earlier work is retained only when it is foundational to a current acceptance test and is marked `FOUNDATIONAL`.

This is a **source-discovery and relevance ledger**, not a claim that every source has been full-text independently reproduced. Inclusion means the title/metadata and available abstract or official page were screened as materially relevant. High-impact architectural claims still require direct reading of the strongest primary sources.

## Evidence themes

1. contamination resistance / private or fresh evaluation
2. dynamic and current benchmark generation
3. judge and verifier validity
4. metamorphic / perturbation / invariance testing
5. calibration, abstention, and uncertainty
6. agent and multi-agent runtime evaluation
7. execution provenance, traceability, and reproducibility
8. process-vs-outcome verification and reward hacking
9. run-to-run variance and deployment transfer
10. falsifiability and evidence-grounded reasoning

## 100 unique source groups

| ID | Source | Window | Relevance | Canonical URL |
|---|---|---|---|---|
| S001 | Last Translation Benchmark | 2026-09 | dynamic/live benchmark | https://arxiv.org/abs/2609.04173 |
| S002 | CleanScore: Black-Box Benchmark Audits with Negative Controls and Sensitivity Bounds | 2026-09 | benchmark audit / negative controls | https://openalex.org/W7205014752 |
| S003 | Designing reproducible large-language-model-assisted scientific analyses | 2026-09 | reproducibility / provenance | https://openalex.org/W7208720693 |
| S004 | ScienceArena: Benchmarking LLMs on Latest Scientific Olympiad Competitions | 2026-08 | fresh benchmark / current tasks | https://arxiv.org/abs/2608.30517 |
| S005 | HEPToolBench 1.2: Testing How Reliably Language Models Can Drive Particle Physics Software | 2026-08 | tool-use reliability | https://arxiv.org/abs/2608.28232 |
| S006 | CultureConverse: A Multilingual Multi-turn Simulation Harness for Culturally Grounded Assistance in East and Southeast Asia | 2026-08 | simulation harness / cross-cultural evaluation | https://arxiv.org/abs/2608.28405 |
| S007 | LoopArena: Benchmarking Models as Runtime Controllers for Loop Engineering | 2026-08 | runtime controller benchmark | https://arxiv.org/abs/2608.28281 |
| S008 | Benchmarking large language model agent societies against human behavioural distributions | 2026-08 | multi-agent evaluation | https://arxiv.org/abs/2608.28182 |
| S009 | RATIO: A Benchmark for Retrieval Across Typed Ideation Operations in Scientific Literature | 2026-08 | retrieval / typed operation evaluation | https://arxiv.org/abs/2608.27394 |
| S010 | DuMateBench: Evaluating Autonomous Agents in Complex Real-World Workflows | 2026-08 | agent workflow benchmark | https://arxiv.org/abs/2608.26546 |
| S011 | AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling | 2026-08 | judge reliability / agentic tool-use | https://arxiv.org/abs/2608.26623 |
| S012 | From Atomic to Agentic: Towards Interpretable Evaluation of LLMs' Agentic Mathematical Capabilities | 2026-08 | interpretable agent evaluation | https://arxiv.org/abs/2608.26950 |
| S013 | Evaluating human and LLM screening workflows in a conceptually complex scoping review: Recall--workload trade-offs and run-to-run consistency | 2026-08 | repeatability / run variance | https://arxiv.org/abs/2608.26885 |
| S014 | Load-Bearing Context: The Question Damage Score for Evaluating Context Reliance in Linguistic Reasoning | 2026-08 | context sensitivity / reasoning | https://arxiv.org/abs/2608.27756 |
| S015 | Skill Issue: Are Skills Language-Invariant in LLMs? | 2026-08 | cross-language invariance | https://arxiv.org/abs/2608.25832 |
| S016 | MathAdv: What Theorem Provers Know, Reason, Formalize, and Generalize | 2026-08 | reasoning / formal verification | https://arxiv.org/abs/2608.25449 |
| S017 | AutoVerifier: Residual-Guided Non-Parametric Optimization for Reference-Based Answer Verification | 2026-08 | verifier robustness | https://arxiv.org/abs/2608.25637 |
| S018 | Reconstructing the Right Episode: Evaluating Interleaved Conversational Memory Beyond Long Context | 2026-08 | memory / evaluation validity | https://arxiv.org/abs/2608.25655 |
| S019 | How Do LLM Agents Actually Get the Flag? Trace-Level Provenance for Agentic Offensive Security Evaluation | 2026-08 | trace provenance / agent evaluation | https://arxiv.org/abs/2608.26237 |
| S020 | MemToC: Benchmarking Memory-Tool Conflict Resolution in Large Language Models | 2026-08 | memory/tool conflict benchmark | https://arxiv.org/abs/2608.26295 |
| S021 | Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence | 2026-08 | judge anchoring bias | https://arxiv.org/abs/2608.25869 |
| S022 | A Judge Should Know What Changed: Construct Validity for LLM-as-a-Judge Evaluation | 2026-08 | construct validity / judge | https://arxiv.org/abs/2608.24419 |
| S023 | The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents | 2026-08 | agent continuity / handoff | https://arxiv.org/abs/2608.24358 |
| S024 | Right Diagnoses, Decorative Reasoning: A Perturbation Audit of Medical Chain-of-Thought | 2026-08 | perturbation / process-vs-outcome | https://arxiv.org/abs/2608.24790 |
| S025 | When Do Supervised UQ Ensembles Improve LLM Hallucination Detection? A Robustness Study | 2026-08 | uncertainty / robustness | https://arxiv.org/abs/2608.24492 |
| S026 | Beyond Confidence: Test-Time Scaling for Multi-Turn Search Agents via Retrieval Grounding | 2026-08 | confidence / grounding | https://arxiv.org/abs/2608.24024 |
| S027 | SA-Bench: Evaluating Semantic Alignment in LLM-Based Paper Reproduction | 2026-08 | semantic alignment / reproduction | https://arxiv.org/abs/2608.24252 |
| S028 | BrowserForge: Scaling Web Episode via Parallel Browser Sandboxes | 2026-08 | browser-agent evaluation harness | https://arxiv.org/abs/2608.24848 |
| S029 | SimVerity: When Does Simulated Agent Success Survive Physical Deployment? | 2026-08 | sim-to-real validation | https://arxiv.org/abs/2608.25067 |
| S030 | Foundation models as oracles for refactoring correctness detection | 2026-08 | oracle reliability | https://openalex.org/W7204117659 |
| S031 | What Proves You Wrong: Benchmarking Language Models on Falsifiable Research Ideation | 2026-08 | falsifiability / research reasoning | https://arxiv.org/abs/2608.22948 |
| S032 | Execution-Anchored Hallucination Calibration Reranking for Verilog Code Generation | 2026-08 | execution-grounded calibration | https://arxiv.org/abs/2608.22938 |
| S033 | SWE Refactor Bench: Can Coding Agents Complete a Long-Horizon, Whole-Repository Stack Migration? | 2026-08 | long-horizon coding agent benchmark | https://arxiv.org/abs/2608.23564 |
| S034 | Beyond Verdicts: A Graph-Based Analysis of Human and LLM Reasoning in Scientific Fact-Checking | 2026-08 | reasoning graph / fact-checking | https://arxiv.org/abs/2608.23047 |
| S035 | Predicting the scale limits of social mechanisms in agent societies | 2026-08 | multi-agent scaling / social mechanisms | https://arxiv.org/abs/2608.22884 |
| S036 | The Compaction Cliff in Long-Running AI Agent Memory | 2026-08 | long-run agent memory reliability | https://arxiv.org/abs/2608.22752 |
| S037 | MARS: Multi-Specialist LLM Relay System for Competitive Programming | 2026-08 | multi-agent specialization | https://arxiv.org/abs/2608.23918 |
| S038 | Feedback That Backfires: Why Small Language Model Agents Repeat the Call They Just Watched Fail | 2026-08 | agent failure recurrence | https://arxiv.org/abs/2608.23651 |
| S039 | From Preferences to Principles: Rubric-Based Alignment for Grounded Knowledge Answers | 2026-08 | rubric / grounded evaluation | https://arxiv.org/abs/2608.23812 |
| S040 | LLM-Based Agents for Software and Systems Security: Approaches, Applications, and Assessment | 2026-08 | agent assessment survey | https://arxiv.org/abs/2608.28490 |
| S041 | Causal evidence that language models use confidence to drive behaviour | 2026-09 | confidence / causal behavior | https://openalex.org/W7211901703 |
| S042 | Check The Scoreboard: An Analysis of Scoring Schemes on Multiple-Choice Evaluation | 2026-08 | metric/scoring sensitivity | https://arxiv.org/abs/2608.29887 |
| S043 | Where Abstention Lives: A Pre-Registered Four-Way Comparison of Abstention Interfaces in a Small Language Model with Versioned Memory | 2026-08 | abstention / preregistration | https://openalex.org/W7204496982 |
| S044 | AERA: Adaptive Evidence Residual Allocation for Efficient Test-Time Reasoning | 2026-08 | evidence allocation / reasoning | https://arxiv.org/abs/2608.27964 |
| S045 | CURA: Certified Runtime Alarms for Computer-Use Agents | 2026-08 | runtime assurance | https://arxiv.org/abs/2608.27808 |
| S046 | When Linguistic and Internal Confidence Diverge in Large Language Models | 2026-08 | confidence calibration | https://arxiv.org/abs/2608.28382 |
| S047 | Twin Worlds: Equivariance-Based Abstention for Evidence-Grounded Reasoning | 2026-08 | equivariance / abstention | https://arxiv.org/abs/2608.28018 |
| S048 | Multi-Expert Conformal Risk Control for Pairwise LLM Judging in Open-Ended Dialogue | 2026-08 | judge calibration / conformal risk | https://arxiv.org/abs/2608.26529 |
| S049 | Localize-Then-Decide Guarantees for LLM Judgments | 2026-08 | judge reliability / guarantees | https://arxiv.org/abs/2608.25824 |
| S050 | Overview of SHROOM-Visions 2026: A Shared Task on Hallucination Detection in Large Vision-Language Models | 2026-08 | hallucination evaluation | https://arxiv.org/abs/2608.25662 |
| S051 | Knowing When to Ask for Help: Bayesian Self-Escalation in Hierarchical LLM Agents | 2026-08 | uncertainty / escalation | https://arxiv.org/abs/2608.24087 |
| S052 | Selective Risk Control for LLM Decision Agents under Uncertainty | 2026-08 | selective prediction / risk | https://openalex.org/W7204142177 |
| S053 | More Rejective, Not More Discriminative: The Unit of Verification in Pre-Execution LLM Oversight | 2026-08 | verification / oversight | https://arxiv.org/abs/2608.23941 |
| S054 | TrustDABench: Benchmarking Reliability and Robustness of LLMs for Structured Data Analysis | 2026-08 | reliability benchmark | https://arxiv.org/abs/2608.24145 |
| S055 | The RAT: A Unified Bayesian Model for RAG Evaluation | 2026-08 | Bayesian evaluation | https://arxiv.org/abs/2608.24753 |
| S056 | PCFBench: A Diagnostic Benchmark for Product Carbon Footprint Estimation | 2026-08 | diagnostic benchmark design | https://arxiv.org/abs/2608.27716 |
| S057 | FinExam-10K: When Retrieval Helps Financial Reasoning? | 2026-08 | retrieval / reasoning evaluation | https://arxiv.org/abs/2608.28155 |
| S058 | Knowing Before Answering: Decoding Language Models for Reliable RAG | 2026-08 | reliable RAG / confidence | https://arxiv.org/abs/2608.27661 |
| S059 | Evaluating Confidence-Gated Retrieval with Matched Trajectory Replay | 2026-08 | matched replay / confidence | https://arxiv.org/abs/2608.26846 |
| S060 | LAAF: A Layered Accountability Architecture Framework for LLM Applications | 2026-08 | accountability / evidence architecture | https://arxiv.org/abs/2608.27102 |
| S061 | Machine Learning Validation Pipelines: From Tabular Benchmarking to Conformal Calibration and Execution-Grounded Agentic Testing | 2026-08 | validation pipeline | https://openalex.org/W7204970000 |
| S062 | Can LLMs Judge Legal Accuracy? Reliability of LLM Evaluators for High-Stakes Insurance QA in a Low-Resource Language | 2026-09 | judge reliability | https://openalex.org/W7211886615 |
| S063 | Turning Domain Expertise into Multi-Dimensional Evaluation of Biomedical AI with Karenina | 2026-09 | multi-dimensional evaluation | https://openalex.org/W7208814027 |
| S064 | Responsible Artificial Intelligence in Courts: A Four-Test Framework | 2026-08 | high-stakes evaluation framework | https://openalex.org/W7207665633 |
| S065 | SA-GGCoT: social-aware graph-grounded chain-of-thought for multimodal claim verification under bounded evidence | 2026-08 | evidence-grounded verification | https://openalex.org/W7204846465 |
| S066 | RRR: Reflexive Role Routing | 2026-04 | FOUNDATIONAL: adaptive role routing | https://arxiv.org/abs/2604.18419 |
| S067 | ZenBrain measurement package: judged outputs, flag manifests, and analysis scripts | 2026-04 | FOUNDATIONAL: measurement artifacts | https://arxiv.org/abs/2604.23878 |
| S068 | Intent Drift in LLM-Assisted BCI Communication: An In-Silico Benchmark Under Simulated Decoder Corruption | 2026-08 | perturbation / intent robustness | https://openalex.org/W7204481334 |
| S069 | ClawProBench: trace-aware evaluation with frozen workplace holdouts | 2026-08 | frozen holdout / agent trace | https://arxiv.org/abs/2608.22510 |
| S070 | Gaming Without an Attacker: Benchmark Fingerprinting in LLM-Driven Search Under Selection Pressure | 2026-08 | benchmark gaming / contamination | https://arxiv.org/abs/2608.08722 |
| S071 | Auditing Data Leakage in Whole-Slide Image Multimodal Benchmarks | 2026-07 | data leakage audit | https://arxiv.org/abs/2607.12278 |
| S072 | CausalDS | 2026-07 | causal evaluation / diagnostic benchmark | https://arxiv.org/abs/2607.08093 |
| S073 | Cost-Effective Agent Harnesses for ARC-AGI-1 | 2026-07 | agent harness evaluation | https://arxiv.org/abs/2607.06764 |
| S074 | MacroLens | 2026-06 | macro evaluation / robustness | https://arxiv.org/abs/2606.24950 |
| S075 | AI Sandboxes: threat model and evaluation isolation | 2026-06 | sandbox / execution isolation | https://arxiv.org/abs/2606.18532 |
| S076 | Cross-View Correspondence Is a Measurement Intervention | 2026-08 | measurement intervention / evaluator validity | https://arxiv.org/abs/2608.17713 |
| S077 | Who Grades the Grader? | 2026-07 | meta-evaluation / judge auditing | https://arxiv.org/abs/2607.12790 |
| S078 | Code-MUE: uncertainty evaluation | 2026-07 | uncertainty / coding evaluation | https://arxiv.org/abs/2607.12273 |
| S079 | Workflow Graphs for Black-Box Boundary Testing | 2026-07 | boundary testing / workflow graphs | https://arxiv.org/abs/2607.06873 |
| S080 | LogicHunter | 2026-07 | logic reasoning benchmark / error detection | https://arxiv.org/abs/2607.06195 |
| S081 | LGMT: Logic-Grounded Metamorphic Testing for Evaluating the Reasoning Reliability of LLMs | 2026-05 | FOUNDATIONAL: metamorphic reasoning test | https://arxiv.org/abs/2605.23965 |
| S082 | BeyondBench: Contamination-Resistant Evaluation of Reasoning in Language Models | 2026 | dynamic contamination-resistant benchmark | https://proceedings.iclr.cc/paper_files/paper/2026/hash/22b4e30a7a660b17f1fb58ab49671e77-Abstract-Conference.html |
| S083 | Piloting the world's first double-blind AI evaluations | 2026-08 | double-blind / cryptographic isolation | https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/ |
| S084 | VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models | 2026 | reference verifier benchmark | https://proceedings.iclr.cc/paper_files/paper/2026/hash/e812af67a942c21dd0104bd929f99da1-Abstract-Conference.html |
| S085 | VerifyBench: A Systematic Benchmark for Evaluating Reasoning Verifiers Across Domains | 2026-03 | verifier cross-domain benchmark | https://ojs.aaai.org/index.php/AAAI/article/view/40448 |
| S086 | Beyond Outcome Verification: Verifiable Process Reward Models for Structured Reasoning | 2026-07 | deterministic process verification | https://aclanthology.org/2026.findings-acl.1611/ |
| S087 | A survey of reward hacking in agentic large language model systems | 2026-08 | reward/verifier hacking taxonomy | https://link.springer.com/article/10.1007/s44163-026-01980-z |
| S088 | Causal Reward Adjustment: Mitigating Reward Hacking in External Reasoning via Backdoor Correction | 2026-03 | reward hacking / causal correction | https://ojs.aaai.org/index.php/AAAI/article/view/40584 |
| S089 | Your Reasoning Model is Secretly a Reward Model - Optimization-Free Verification from Experience | 2026-07 | verification / calibration | https://aclanthology.org/2026.acl-long.788/ |
| S090 | Reward Under Attack: Analyzing the Robustness and Hackability of Process Reward Models | 2026-02 | FOUNDATIONAL: PRM adversarial robustness | https://arxiv.org/abs/2603.06621 |
| S091 | Smarter Not Harder: Generative Process Evaluation with Intrinsic-Signal Driving and Ability-Adaptive Reward Shaping | 2026 | process reward model / reward hacking | https://proceedings.iclr.cc/paper_files/paper/2026/hash/da842df0d1e35e15a521267acb62bbd0-Abstract-Conference.html |
| S092 | Suggestible Judges: Asymmetric Conformity in Large Language Model Adjudication | 2026-09 | judge conformity / sycophancy | https://openalex.org/W7207586483 |
| S093 | Benchmarking LLM Judges for Voice-Agent Evaluation: Reliability, Calibration, and Human Oversight | 2026-08 | judge calibration / human oversight | https://arxiv.org/abs/2608.24314 |
| S094 | Multi-Agent Debate for LLM Judges with Adaptive Stability Detection | 2025-10 | FOUNDATIONAL: multi-agent judge / stopping | https://arxiv.org/abs/2510.12697 |
| S095 | Dynamic Benchmarking of Reasoning Capabilities in Code Large Language Models Under Data Contamination | 2025-03 | FOUNDATIONAL: dynamic contamination benchmark | https://arxiv.org/abs/2503.04149 |
| S096 | On scalable oversight with weak LLMs judging strong LLMs | 2024-07 | FOUNDATIONAL: scalable oversight | https://arxiv.org/abs/2407.04622 |
| S097 | Towards A Unified View of Answer Calibration for Multi-Step Reasoning | 2023-11 | FOUNDATIONAL: reasoning calibration | https://arxiv.org/abs/2311.09101 |
| S098 | MIRAI: Evaluating LLM Agents for Event Forecasting | 2024-07 | FOUNDATIONAL: agent evaluation / temporal evidence | https://arxiv.org/abs/2407.01231 |
| S099 | ACTIONREASONINGBENCH: Reasoning about Actions | 2024-06 | FOUNDATIONAL: reasoning benchmark / obfuscation | https://arxiv.org/abs/2406.04046 |
| S100 | Safety Hacking in Constrained Best-of-N Inference-time Scaling | 2026-08 | proxy/reward hacking under inference scaling | https://arxiv.org/abs/2608.22915 |

## Screening notes

- `S001–S093` are primarily 2026 items, with June–September prioritized where available.
- Entries marked `FOUNDATIONAL` are deliberately outside the preferred window because they define a measurement technique or failure mode reused by the 2026 work.
- Search providers used in this research pass included OpenAlex via Sider Scholar and direct web/official proceedings retrieval. The raw candidate pool exceeded 200 records before relevance screening and URL-level deduplication.
- A failed Scholar query containing a `title=null` metadata record was excluded rather than counted.
- Same paper appearing via arXiv, OpenAlex, publisher, or conference pages counts once in this ledger.
- `SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`: source count is useful for coverage, but architectural decisions should weight directness, methodological quality, dependence, and whether a source actually discriminates the active crux.

## Current synthesis

The literature converges on a measurement bottleneck rather than a need for ever more reasoning procedure:

`EVALUATION_VALIDITY = TASK_VALIDITY + INFORMATION_SEPARATION + EXECUTION_PROVENANCE + VERIFIER_ROBUSTNESS + REPEATABILITY`

The expression is conceptual, not a numeric formula. The current repository gap is therefore not another visible fixture; it is an independently attributable target execution whose response artifact is bound to the manifest and whose freshness claim is owned by an external/owning runtime rather than by the manifest itself.

Hard invariants:

- `MANIFEST_CLAIM != EXECUTION_EVIDENCE`
- `FRESH_CONTEXT_FLAG != FRESH_CONTEXT_PROOF`
- `BOUND_RECEIPT != SEMANTIC_TRUTH_OF_RUNTIME_CLAIM`
- `SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`
- `VERIFIER_PASS != TASK_TRUTH`
- `ROBUSTNESS != NEVER_CHANGING`
- `CALIBRATED_ROBUSTNESS = INVARIANCE_WHEN_IRRELEVANT + SENSITIVITY_WHEN_DECISIVE`
