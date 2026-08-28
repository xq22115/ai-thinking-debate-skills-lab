# Source Matrix — AI Efficiency Operating System v0.2

Date: 2026-08-28  
Canonical package: `ai-efficiency-operating-system`

This file records where v0.2 mechanisms came from. It deliberately distinguishes explicit user rules, recovered account history, current repository truth, external research and new synthesis.

## Provenance classes

- `USER_DIRECTIVE` — explicit user instruction.
- `ACCOUNT_CHAT_RECOVERY` — prior-account conversations/files recovered in this run; substantial but not provably exhaustive.
- `REPOSITORY_CANONICAL` — current canonical repository artifacts.
- `EXTERNAL_RESEARCH` — current official/vendor/academic evidence.
- `ASSISTANT_SYNTHESIS` — formalization created in this evolution pass.
- `REQUIRES_CONFIRMATION` — insufficient evidence for promotion.

## Prior-conversation clusters recovered

| Date / chat cluster | High-value rule recovered | v0.2 destination |
|---|---|---|
| 2026-08-20 — `驗證能力橋接 Runtime`, `代理模式解析` | Ordinary Chat remains the control center; copying chat is not capability bridging; real execution requires an authorized runtime and owning-runtime read-back. A genuine agent needs runtime/session receipts, not a persona/read-only relay. | capability bridge, real-agent proof, completion |
| 2026-08-21 — `全面提升內容品質` | Quality needs a closed loop rather than prompt length. Recovered failure classes include specification–behavior gap, proxy depth/breadth, premature narrative lock-in, context crowding, evaluator Goodhart/bias and local-revision regression. Depth should change the global model; breadth uses a coverage frontier. | coverage frontier, model-delta depth, skill evolution |
| 2026-08-21–23 — `全域深度思考設定`, `全域強制深度思考設定` | Genuine depth = more analysis/evidence/falsification/verification. Fixed waits, polling, tool/network wait, streaming throttling and token-drip are not reasoning. Explicit source/agent/duration floors must be evidenced, never simulated. | depth test, research contract, stop policy |
| 2026-08-23 — `設定背景代理操作` | Do not steal focus or surface windows. Prefer API/CLI/MCP/DOM/Accessibility; use screenshots only as needed evidence; reversible exploration first. | background-nondisruptive execution |
| 2026-08-24–25 — `修復輸出限制與卡頓`, `深度思考與卡頓比較` | “不要秒回答” means do actual research/thinking, not make output stutter. Reasoning depth and token/render/UI latency are separate. | performance contract, hot-path control |
| 2026-08-25–27 — multi-chat lag / 429 / performance chats | Do not fix speed by closing required chats, disabling tools/features, reducing concurrency, lowering depth/quality or shrinking workload. Prefer common-root routing/context/cache/retry/serialization/resource fixes. | no-goal-shrink, retry/cache/backpressure, lock scope |
| 2026-08-26 — `修復主任務控制問題` | Later context/tool/agent/memory/retrieval cannot overwrite the primary task. Explicit correction has priority. Search/found repo/tool success is not task completion. | task contract, correction reconciler, drift firewall |
| 2026-08-26–27 — queue/continuation/tool-acquisition work | Long work requires checkpoints, event-sourced state, idempotency/fencing, one owner per mutable target and resume without duplicated side effects. | durable journal, idempotent resume, target lock |
| 2026-08-27 — `提升GPT對話效能`, `全面提升輸出效能`, `全面優化GPT對話模式` | Lean front door; demand-load context/tools; preserve all capabilities. Keep heavy evidence/history transforms off the hot path and avoid repeated full accumulated-state work. | progressive disclosure, lean dedup, demand loader, hot-path control |
| 2026-08-28 — `鎖定主任務` and convergence work | Current owning `main`/runtime beats stale PR/chat summaries. Recheck source revision, owner/supersession and target before mutation. Repository PASS cannot replace owning-product PASS. | target identity lock, completion/read-back |
| 2026-08-28 — current request | Continue collecting other chats, use ten-agent division, fully evolve the efficiency package, avoid naming confusion and retain one best solution. | package-wide A01–A10 review; single canonical package |

## Durable account artifacts surfaced during recovery

Account retrieval also surfaced material including:

- `SKILL.md` — versioned user-intent contract and verifier/runtime proof.
- `Deep Agent Orchestration` — durable task graph and verified graph-state completion.
- `ARCHITECTURE(8).md`, `ARCHITECTURE(9).md` — invariants, anti-goal-shrink and runtime truth.
- `AGENTS.md` — context as scarce working memory, progressive disclosure and durable external state.
- `V6_DECISION_MATRIX.md` — artificial wait/stream throttling rejected as depth evidence.
- `ordinary_chat_global_convergence_matrix_2026-08-28.json` and related reports — `不卡頓 != 秒回`, current-owner/runtime acceptance and hot-path findings.
- `AI_Repair_Evolution_Pack_2026_v0.3.0_DELTA.md` — bounded state packet, live reconciliation, resume/cross-session controls.
- `00_GLOBAL_CUSTOM_INSTRUCTIONS.txt` — Goal/Success/Constraints/Blocker/Unknown control and observable completion.
- `Deep Research report` — execute→evaluate→attribute→modify→holdout→promote/rollback.
- `tool-call-data.json` — transport success separated from task success; exact task/thread identity matters.

These are recovery anchors, not proof that every account message was enumerated.

## Canonical repository sources

### `skills/06-evaluation-suite.md`
Adopted: goal/evidence fidelity, falsification, marginal agent gain, state durability, tool truthfulness, regression control, completion discipline, clone/minority/noise/selective-retention evals, and completion-state separation.

### `skills/07-deliberation-router-spec.md`
Adopted: smallest useful topology, escalation/de-escalation, evidence-weighted judge, selective retention, and stopping when execution/eval is more informative.

### `skills/11-cross-chat-convergence.md`
Adopted: archive→evidence gap→hypotheses→deliberation→root cause→compatibility→control plane→execution→receipts/evals→completion→recovery; exact repository/runtime evidence outranks remembered summaries for mutable state.

### Portable core dependencies
`evidence-gap-research`, `competing-hypotheses`, `root-cause-clustering`, `compatibility-audit`, `capability-challenge`, `multi-agent-deliberation`, `durable-agent-control-plane`, `recoverable-state`, `completion-gate`.

## 2026 external research calibration

External evidence strengthens mechanisms; it does not override the active user contract.

1. OpenAI — **Model guidance**  
   https://developers.openai.com/api/docs/guides/latest-model  
   Lean prompts, single-owner instructions and relevant-tool exposure support context/token efficiency.

2. OpenAI — **A practical guide to building AI agents**  
   https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/  
   Model + tools + instructions; use deterministic solutions where autonomy is unnecessary.

3. OpenAI — **The next evolution of the Agents SDK** (2026-04-15)  
   https://openai.com/index/the-next-evolution-of-the-agents-sdk/  
   Controlled computer/sandbox environments support long-horizon execution.

4. OpenAI — **Designing AI agents to resist prompt injection** (2026-03-11)  
   https://openai.com/index/designing-agents-to-resist-prompt-injection/  
   Constrain the impact/blast radius of misleading external context, not only strings.

5. Anthropic — **Effective context engineering for AI agents**  
   https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents  
   Context is finite; compaction, structured notes and specialized subagents are complementary.

6. Anthropic — **How we built our multi-agent research system**  
   https://www.anthropic.com/engineering/multi-agent-research-system  
   Parallel exploration helps some complex research, but coordination/over-spawning costs require routing and distillation.

7. Anthropic — **How we contain Claude across products** (2026-05-25)  
   https://www.anthropic.com/engineering/how-we-contain-claude  
   More capable agents require deliberate blast-radius containment.

8. Eslami (2026) — **Dynamic Coalition Formation and Communication Pricing in Skill-Based Agentic AI Systems**  
   https://arxiv.org/abs/2608.07532  
   Research signal for marginal-value agent activation and communication-edge cost; not treated as a universal production guarantee.

9. Ye et al. (2026) — **Meta Context Engineering via Agentic Skill Evolution**  
   https://arxiv.org/abs/2601.21557  
   Research signal for co-evolving context-engineering skills through execution/evaluation feedback.

10. Zhang et al. — **Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models**  
    https://arxiv.org/abs/2510.04618  
    Research signal for structured incremental context evolution that avoids context collapse/brevity loss.

## Conflict-resolution order

1. current explicit user correction for the user's task;
2. exact owning-runtime evidence for mutable runtime state;
3. current exact repository revision for repository state;
4. current primary/official source for product/API behavior;
5. independent deterministic/runtime corroboration;
6. coherent inference;
7. popularity/majority only as weak evidence.

External research cannot override hard user constraints. Assistant synthesis must remain labeled.

## Coverage boundary

v0.2 substantially expands cross-chat recovery versus v0.1, but the retrieval interface did not expose a complete account export/list whose cardinality could be independently verified.

`ACCOUNT_CHAT_RECOVERY = SUBSTANTIAL`  
`ACCOUNT_WIDE_EXHAUSTIVE = UNVERIFIED`
