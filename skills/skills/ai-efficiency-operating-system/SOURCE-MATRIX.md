# Source Matrix — AI Efficiency Operating System v0.4

Date: 2026-08-29  
Version: `0.4.0-rc1`  
Canonical package: `ai-efficiency-operating-system`

This matrix records the sources used to evolve v0.4. It separates explicit user directives, recovered account artifacts/chats, current repository truth, current external research and new synthesis. Recovery is substantial, not provably exhaustive.

## Provenance classes

- `USER_DIRECTIVE` — explicit user requirement.
- `ACCOUNT_CHAT_RECOVERY` — prior-account chats or durable Library artifacts recovered in this run.
- `REPOSITORY_CANONICAL` — current canonical repository truth.
- `EXTERNAL_RESEARCH` — current official/vendor/academic evidence.
- `ASSISTANT_SYNTHESIS` — integration created here; not represented as a direct user instruction.
- `REQUIRES_CONFIRMATION` — insufficient evidence for promotion.

## v0.4 cross-chat / durable-account recovery

| Recovered artifact / cluster | Distinct recovered mechanism | v0.4 destination |
|---|---|---|
| `ARCHITECTURE(7).md` — ARR v1.3 | Logical, control, effect/evidence, delivery and external temporal-witness planes are distinct; `logical rewind != authority rewind != effect rewind != delivery rewind`. | `authority-plane-separation` |
| `ARCHITECTURE(7).md` / `ARCHITECTURE(3).md` | External effect ambiguity is a first-class `UNKNOWN`; read-back before replay; UNKNOWN is not FAILED/not-run. | `unknown-effect-reconciliation` |
| `ARCHITECTURE(3).md` | Semantic action identity binds run, goal version, tool, canonical args and semantic scope; goal changes use CAS and stale actions are rejected. | `goal-version-cas-and-semantic-action-identity` |
| `ARCHITECTURE(7).md` | Receiver-side truth: sender cannot self-ACK; receiver/independent observer read-back is authoritative for delivery. | strengthen `continuity-delivery-state-machine` |
| `ARCHITECTURE(7).md` | Memory authority includes content hash/source/authority ceiling/derived lineage; transform/echo/repetition cannot increase authority. | strengthen `memory-authority-and-recurrence-consolidation` |
| `ARCHITECTURE(3).md` | Verifier `(name, version)` requires canaries plus false-accept/false-reject budgets before admission. | `verifier-admission-canary-registry` |
| `ARCHITECTURE(5).md` | Evidence/reviewer independence is clustered by provenance/model/prompt/evidence route; SUPPORT and REFUTE are not averaged. | `correlated-consensus-evidence-clustering` |
| `SKILL_PATCH_R57.md` | Delegated/headless work must preflight interaction mode, responder/channel reachability and authority; approval required with no responder cannot wait forever; delegation prose creates no approval. | `interaction-topology-preflight` |
| `DeepLock V2.1 / ARCHITECTURE(2).md` | Shared root cause: authority co-location. Cognitive plane can propose but cannot grant completion. Real agents are external runtime/thread identities; isolation-before-debate reduces conformity. | v0.4 root thesis + A01–A10 truth boundary |
| `TEST_REPORT_V5.md` | Thread lease, no parallel resume, durable cancellation intent, bounded overload recovery and crash recovery were locally tested; tests used fake peers and do not prove live Codex account E2E. | strengthen resume/liveness gates; retain host-live boundary |
| `ordinary_chat_global_convergence_matrix_2026-08-28.json` | Ten audit branches were not real agents; mutable source/runtime/behavioral identities can remain BLOCKED even when GitHub convergence succeeds. | agent proof + target identity |
| `ordinary_chat_accelerator_verification_20260828.md` | Browser candidate passed queue/dedupe/rate-limit/render/stream/cross-tab tests while owning Mac runtime remained blocked; 9/10 is not complete. | performance + owning-runtime completion truth |
| `ARCHITECTURE(4).md` — Executive Harness | Raw web/tool output is ephemeral evidence; instruction-like external content is quarantined; distribution integrity requires path+SHA-256+size parity. | memory authority + distribution parity |
| `EXPLORED_LEDGER_R57.md` | New research themes: agentic abstention, blind tool deference, dynamic skill lifecycle, handoff debt, model-aware skill adaptation. | four new judgment/evolution/handoff owners |
| 2026-08-20–28 ordinary-Chat / performance / cross-PR clusters | Preserve many chats, tools, depth and native controls; optimize hot paths, backpressure, ownership and exact-head read-back rather than shrinking workload. | preserved v0.3 performance/control modules |
| 2026-08-29 continuation | Continue same canonical package; use A01–A10 workstreams without fake runtime-agent claims; evolve only materially distinct mechanisms. | package-wide v0.4 |

## v0.4 root-cause synthesis

v0.3 identified **implicit context = hidden state**.

v0.4 adds the deeper failure:

> **authority co-location = hidden coupling.**

When one context can propose, authorize, execute, interpret evidence, certify completion, self-ACK delivery and rewrite memory, plausible text can bypass real state transitions.

Canonical separation:

`INTENT → PROPOSAL → AUTHORITY → EFFECT → OBSERVATION → EVIDENCE → VERDICT → DELIVERY`

Independent temporal witness is added where rollback can repeat irreversible work.

Second synthesis:

> **Capability is incomplete without calibrated non-action and adjudication.**

A good agent must know when to act, gather, abstain, distrust a tool, or stop/delegate.

## Current external research calibration

These sources calibrate mechanisms; none overrides the active user task or substitutes for owning-runtime verification.

1. **AgentAbstain: Do LLM Agents Know When Not to Act?** — arXiv:2607.10059  
   Paired should-act/should-abstain evaluation; abstention is substantially distinct from general task solving. Post-hoc abstention after an irreversible action is explicitly a failure class.  
   Consequence: add paired act/abstain and timely-stop gates.

2. **Agentic Abstention: Do Agents Know When to Stop Instead of Act?** — arXiv:2606.28733  
   Evaluates sequential abstention on >28,000 tasks and emphasizes timeliness.  
   Consequence: stopping is a sequence-level decision, not a final-answer checkbox.

3. **When the Tool Decides: LLM Agents Defer Blindly to Graph Neural Network Tools, and Stronger Backbones Defer More** — arXiv:2606.14476  
   Narrow-domain evidence shows very high agreement with raw tool output and warns that stronger backbones may defer more. This does not prove universal tool deference.  
   Consequence: separate tool invocation from tool adjudication and preserve domain caveat.

4. **Dynamic Skill Lifecycle Management for Agentic Reinforcement Learning (SLIM)** — arXiv:2605.10923  
   Uses marginal contribution / leave-one-skill-out ideas to retain, retire or expand skills.  
   Consequence: skill portfolios need reversible lifecycle management rather than monotonic accumulation.

5. **Skill is Not One-Size-Fits-All: Model-Aware Skill Alignment for LLM Agents (MASA)** — arXiv:2605.30723  
   Reports that identical skills can help one model and harm another.  
   Consequence: skill admission/promotion is model/host-conditioned.

6. **Handoff Debt: The Rediscovery Cost When Coding Agents Take Over Interrupted Tasks** — arXiv:2606.02875  
   Structured context-bearing handoffs substantially reduce event/token rediscovery cost; outcome gains are model-dependent.  
   Consequence: preserve a canonical evidence core and generate successor-conditioned views.

7. **Collaborative Human-Agent Protocol (CHAP)** — arXiv:2606.09751  
   Working-draft protocol research for structured overrides/handoffs/evidence logs. It is not treated as a finalized standard.  
   Consequence: portable handoff envelopes are evidence-backed design input, not a universal host contract.

8. **OpenAI Agents SDK documentation (current 2026 guidance)**  
   Handoffs, agents-as-tools/manager orchestration, sessions and tracing expose distinct ownership/history/tracing choices.  
   Consequence: do not assume every delegation is a handoff; manager ownership and handoff ownership differ, and session/conversation ownership must be explicit.

9. **Model Context Protocol 2026-07-28**  
   Protocol behavior is versioned; current final core differs from older stateful initialization assumptions.  
   Consequence: protocol behavior remains version-conditioned.

10. **OpenAI 2026-08-24 Codex release notes**  
    `codex mcp-server` is deprecated in favor of Codex app server.  
    Consequence: historical runtime routes require deprecation/retest triggers.

## Evidence-quality cautions

- A research paper/preprint is evidence for a mechanism, not automatic production proof.
- Blind-tool-deference evidence is narrow to the evaluated tool/domain and must not be universalized.
- CHAP is a working draft, not a final standard.
- Model-aware skill and handoff results are explicitly model-dependent.
- Local/fake-peer tests do not prove the user's live host/account.
- Reviewer/source count is not evidence independence; provenance and lineage matter.

## Current repository truth before v0.4 write

At the start of this continuation, `main` was read at:

`14aae76ce9ae3a1be81075890cd947baa9eb3076`

Tree:

`afa632fb7aa80cc07ef1ef838b70a267c4d4fbb9`

The v0.4 write must re-read live `main` immediately before ref movement and use a non-force fast-forward. If another chat advances `main`, rebuild on that new base rather than overwriting it.

## Coverage boundary

This continuation materially expands cross-chat/account-artifact recovery beyond v0.3.

`ACCOUNT_CHAT_RECOVERY = EXPANDED_SUBSTANTIAL`  
`ACCOUNT_WIDE_EXHAUSTIVE = UNVERIFIED`

The available retrieval surface does not expose a provably complete account message inventory/cardinality. Exhaustive-account coverage must not be claimed.
