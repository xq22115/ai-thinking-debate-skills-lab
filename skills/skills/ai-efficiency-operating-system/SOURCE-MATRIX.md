# Source Matrix — AI Efficiency Operating System v0.3

Date: 2026-08-29  
Version: `0.3.0-rc1`  
Canonical package: `ai-efficiency-operating-system`

This matrix records the provenance used to evolve v0.3. It deliberately separates explicit user directives, recovered account artifacts/chats, current repository truth, current official external sources and assistant synthesis.

## Provenance classes

- `USER_DIRECTIVE` — explicit requirement from the user.
- `ACCOUNT_CHAT_RECOVERY` — prior-account chats or durable Library artifacts recovered in this run; substantial but not provably exhaustive.
- `REPOSITORY_CANONICAL` — current canonical repository artifacts.
- `EXTERNAL_RESEARCH` — current official/vendor/academic evidence.
- `ASSISTANT_SYNTHESIS` — formal integration created here; never misrepresented as a direct user instruction.
- `REQUIRES_CONFIRMATION` — insufficient evidence for promotion.

## Cross-chat / durable-account recovery

| Date / artifact or chat cluster | Recovered mechanism | v0.3 destination |
|---|---|---|
| 2026-08-20 — ordinary Chat / runtime bridging chats | Ordinary Chat can remain the natural-language control plane, but conversation relay is not capability execution. Real action needs an authorized runtime and receipts. | capability bridge + completion truth |
| 2026-08-21 — quality/evolution chats | Quality is a closed loop, not prompt length. Preserve global-model delta, coverage frontier, failure attribution and regression protection. | reasoning + evolution |
| 2026-08-21–23 — deep-thinking controls | Genuine depth requires analysis/evidence/falsification; waiting, polling and token drip are not reasoning. | model-delta depth + research contract |
| 2026-08-23 — background agent operation | Automation should avoid focus theft; prefer API/CLI/MCP/DOM/Accessibility and reversible/background paths. | background nondisruptive execution |
| 2026-08-24–25 — output stutter vs reasoning | “Do not answer instantly” means do real work, not make output stutter. Reasoning time and UI/output cadence are different. | performance budgets |
| 2026-08-25–28 — multi-chat / 429 / stream / history repair | Preserve many chats, tools, quality and depth; remove hot-path/history/retry/lock amplification instead of shrinking workload. | performance + no-goal-shrink |
| 2026-08-26 — primary-task control | Later tools/agents/retrieval/memory cannot silently overwrite the root task; explicit correction wins. | task contract + goal firewall |
| 2026-08-26–28 — queue/continuation/cross-PR work | Long work needs durable state, current owner/ref, idempotency/fencing and resume without duplicate effects. | execution + continuity |
| 2026-08-27 — context/tool efficiency | Discover many/load few; keep heavy context/evidence off always-hot paths. | progressive disclosure + observation cache |
| 2026-08-28 — owner/supersession/read-back convergence | Live main/runtime evidence outranks stale PR/chat prose; same-owner writes serialize; repo PASS is not product PASS. | identity lock + verification |
| 2026-08-28 — exact-10 runtime probe | Branches/personas/audit lanes cannot count as real agents; auth/runtime blockers must produce 0 verified rather than fake completion. | agent independence proof |
| 2026-08-28 — `ordinary-chat-global-agent-convergence-2026-08-28.md` | Ten independent target/route identity checks; protected baseline; capability/deployment state separation; diagnosis parallel/finalization single-writer. | identity lock + execution topology |
| 2026-08-28 — `ordinary-chat-github-repair-2026-08-28-v2.md` | Five-chat scale regression, lock only admission critical section, network settlement outside global lock, stale CI-generation coalescing. | performance + concurrency |
| 2026-08-09 — `DeepControl-v5-Research-Basis.txt` | Failed-turn quarantine; semantic compaction rollback; path/hash observation cache; changed-strategy bounded retry + circuit breaker; worker/verifier split; event-driven wait; branch-scoped degradation. | 8 new v0.3 mechanisms |
| 2026-08-09 — `AI_Agent_Engineering_Research_2026-08-09_Run2.md` | Instruction scope/precedence is host-specific; bounded continuity checkpoints; alternate-path invariants; protocol version awareness; activation precision/recall. Shared root cause: implicit context. | instruction/protocol/skill-admission modules |
| 2026-08-09 — `AI_Repair_Evolution_Pack_2026_v0.3.0_DELTA.md` | Track sent/delivered/acknowledged/incorporated/verified separately; no universal instruction precedence; no “more skills is always better”; no generated-skill self-approval. | delivery state + admission gate |
| 2026-08-10 — `00-LATEST-GITHUB-SNAPSHOT.md` | Per-agent context-window lineage/checkpoints; instruction provenance across sessions; skills as discovery/config/runtime harness components, not giant prompts. | context lineage + provenance |
| 2026-08-10 — `validation_report(20260810-113744).md` | Temporal witness detects whole-store rollback; physical-file contract and reverse coverage prevent staged/described artifacts from passing. | temporal witness + materialization |
| 2026 — Windows AI dictation deep research artifact | Distinguish raw text accuracy, correction intent and generated writing; track proper nouns/code-switch/hallucination/deletion. | input-fidelity module |
| 2026 — memory/agent research artifact (`Deep Research report(1)`) | Recurrence-triggered memory consolidation, intent-aware context folding and failure-aware minimal specialist routing. | memory authority + adaptive routing |
| 2026-08-29 — current continuation | Continue cross-chat recovery, deepen the same canonical skill package and use A01–A10 without creating name collisions. | v0.3 package-wide |

## Root-cause synthesis

The strongest cross-source common cause is **implicit context**.

Efficiency and correctness collapse when the system silently assumes:

1. active task/goal;
2. active instruction precedence;
3. surviving memory/state after compaction or resume;
4. target owner/ref/version;
5. permission/runtime availability;
6. protocol semantics;
7. agent independence;
8. handoff incorporation;
9. skill activation;
10. completion.

v0.3 turns these into explicit state, evidence and tests.

## Canonical repository sources

### `skills/06-evaluation-suite.md`
Provides goal/evidence fidelity, falsification, marginal-agent gain, durability, tool truthfulness, regression and completion-state discipline.

### `skills/07-deliberation-router-spec.md`
Provides smallest useful topology, escalation/de-escalation, evidence-weighted judging and selective retention.

### `skills/11-cross-chat-convergence.md`
Provides cross-chat convergence ordering and the rule that exact current repository/runtime evidence outranks remembered summaries for mutable state.

### Portable core dependencies
`evidence-gap-research`, `competing-hypotheses`, `root-cause-clustering`, `compatibility-audit`, `capability-challenge`, `multi-agent-deliberation`, `durable-agent-control-plane`, `recoverable-state`, `completion-gate`.

## Current official external calibration

External sources calibrate mechanisms; they do not override the active user contract.

1. **Model Context Protocol — 2026-07-28 Specification**  
   https://blog.modelcontextprotocol.io/posts/2026-07-28/  
   Current final release: stateless protocol core, request self-description, header routing, cacheable ordered list results, MRTR, extensions including Tasks, authorization hardening and deprecation policy. Design consequence: protocol behavior must be version-aware, and tool-list caching can reduce repeated discovery work.

2. **OpenAI Release Notes — Codex, 2026-08-24**  
   https://openai.com/products/release-notes/  
   `codex mcp-server` is deprecated; use Codex app server. Design consequence: historical architecture must not freeze a deprecated execution bridge as canonical.

3. **Model Context Protocol — 2026-07-28 Release Candidate / migration framing**  
   https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/  
   Documents breaking changes and version migration. Design consequence: old and new MCP behavior require explicit compatibility branches.

4. **OpenAI current agent/model guidance**  
   Used for lean instructions, relevant-tool exposure and deterministic execution where autonomy is unnecessary.

5. **Anthropic context engineering / multi-agent research engineering**  
   Used for context scarcity, compaction, specialized subagents and coordination cost of over-spawning.

6. **2026 context/memory/agent research recovered in account Library**  
   Used only as research signal for recurrence-based memory consolidation, intent-aware context folding, failure-aware specialist routing and skill evolution. No single paper is treated as universal production proof.

## Current repository truth at start of v0.3 write

Immediately before core object creation, live `main` was re-read at:

`e240855c5026856ff104d8b080b09187a9e32ad6`

Base tree:

`0c3398175f9c05e273c57992730ec4c8037feed9`

That head already contains concurrent repository work after the previous efficiency-package update. v0.3 therefore builds from live main and must use a non-force fast-forward update; it must not overwrite concurrent work using the older `5fe0e072...` head.

The final verification file must refresh this after writes and record the actual v0.3 commit/read-back.

## Input-fidelity sub-contract

Cross-chat speech/dictation work adds a general efficiency lesson: preprocessing errors can masquerade as reasoning errors.

Keep separate:

- raw input fidelity;
- correction intent;
- generated rewrite quality.

Do not let cleanup change technical terms, proper nouns, dates/numbers or final corrections and then blame the reasoning layer.

## Memory policy

Durable memory should store validated mechanisms, not every conversational event.

Promote only with:

- recurrence or high materiality;
- evidence;
- correct scope/version;
- provenance;
- retest trigger.

Transient outages and failed turns remain quarantined/ephemeral.

## Conflict-resolution order

1. current explicit user correction;
2. exact owning-runtime evidence for mutable runtime state;
3. current exact repository/object state for repository facts;
4. current official primary source for product/protocol behavior;
5. deterministic/independent corroboration;
6. validated durable account artifact;
7. coherent assistant synthesis;
8. popularity/majority as weak evidence only.

## Coverage boundary

This continuation materially expands recovery beyond v0.2, including previously missed durable artifacts and cross-chat clusters.

`ACCOUNT_CHAT_RECOVERY = EXPANDED_SUBSTANTIAL`  
`ACCOUNT_WIDE_EXHAUSTIVE = UNVERIFIED`

The retrieval surface still does not expose a provably complete account message inventory/cardinality, so exhaustive-account coverage must not be claimed.
