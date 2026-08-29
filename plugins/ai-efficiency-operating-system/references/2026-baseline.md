# 2026 baseline and borrowed mechanisms

Verification date: 2026-08-29.

This package borrows mechanisms, not prose. Internal historical test receipts, current public sources, repository implementations and live-host evidence remain separate evidence classes.

## OpenAI current packaging and eval boundary

- **openai/plugins**: current curated packaging uses `.codex-plugin/plugin.json`, `skills/`, optional per-skill `agents/openai.yaml`, marketplace metadata and plugin-specific tests. Snapshot checked through commit `1e285826e604f66f7208f7ac4dba0fe8341d1f57` (2026-08-28).
- **plugin-eval**: the official local-first evaluator keeps a deterministic static engine and normalized result schema separate from host/runtime benchmarking. It explicitly distinguishes trigger, invoke, deferred and explicit-only budgets; observed usage/benchmarking is an additional mode rather than proof silently inferred from static analysis.
- **GitHub marketplace / ChatGPT**: package and marketplace presence do not prove installation, invocation, permission or behavioral target state. The live adapter therefore retains a separate owning-surface probe.

## Mature skill frameworks

- **obra/superpowers**: skill creation is treated like TDD; observe baseline failure, write the smallest effective skill, rerun pressure cases, refactor. Frequently loaded skills are kept thin; heavy material moves to references/scripts.
- **addyosmani/agent-skills**: skills are specific, verifiable and minimal; lifecycle ownership and trigger regression matter.
- **garrytan/gstack**: many narrow opinionated skills rather than one universal prompt; host/domain knowledge is scoped instead of becoming a universal self-modifying runtime.
- **OthmanAdi/planning-with-files**: durable working state can survive compaction/restart when the host actually provides lifecycle/persistence; writable reinjected state must not become an authority-escalation path.
- **Tencent/SkillHone**: optimize the whole skill folder, keep eval and skill data separated, preserve persistent decision history and gate promotion on held-out validation.
- **Microsoft SkillOpt**: use bounded add/delete/replace edits, strict held-out improvement, rejected-edit feedback and slower structural updates instead of unbounded self-rewriting.

## Current research that constrains this design

### Skill negative transfer

**Agent Skills Can Be Harmful** — arXiv:2608.11888, 2026-08-12. Differential comparison against no-skill or semantically matched reference runs found 307 skill-induced failures, including functional and efficiency regressions; excessive verification and heavy implementation pipelines were major excessive-procedure classes.

Transfer:
- no aggregate benchmark may justify universal activation;
- skill admission includes no-skill/matched-reference attribution;
- functional and efficiency regressions both matter;
- extra verification ceremony is not automatically rigor.

### Cross-skill switching

**Toward Skill-Native LLMs: Skill Entropy for Benchmarking and Training Long-Horizon Reasoning** — arXiv:2608.05139, 2026-08-05. Cross-skill accuracy falls as skill-switching entropy increases.

Transfer:
- keep one primary phase owner;
- retrieve a task-relevant skill subgraph rather than the whole bank;
- for durable long-horizon work, treat skill changes as explicit state transitions when that distinction matters.

### Citation truth under deep retrieval

**Cited but Not Verified** — arXiv:2605.06635, 2026-05-07. Citation evaluation separates link accessibility, relevance and factual support; increasing research depth from 2 to 150 tool calls reduced fact-check accuracy by about 42% on average across two frontier models in the reported ablation.

Transfer:
- retrieval depth and citation verification are separate controls;
- load-bearing citations need source accessibility/relevance/fact support checks;
- source/citation count cannot substitute for factual grounding.

### Progress mirage

**When Do Agent Loops Mistake Stagnation for Progress?** — arXiv:2607.25152, 2026-07-27. In 54 cycles the agent self-reported progress every time while 56% of measured deltas were zero or negative; a strong in-band judge remained unreliable for open-ended objectives whose success signal lived outside the transcript.

Transfer:
- executor/self-judge reports cannot certify external outcomes;
- open-ended target success requires out-of-band/owning-world postconditions where available;
- simulated/known-outcome controls remain SHADOW evidence until observed-target verification exists.

## Internal validated lineage retained from earlier releases

### Executive Harness v1.0.0 — baseline owner topology

Historical local receipts: repeated 54/54 deterministic tests, 8/8 skill lint, routing metrics at 1.000 on its recorded corpus, package parity and a compact context budget. Live ChatGPT trigger behavior was not proven.

Use: canonical eight-skill semantic ownership and negative routing baseline. New changes must preserve or improve this baseline rather than replacing it with a new mega-skill.

### Deep Task Integrity

Recovered original reference includes temporal breadth, 12 search operations, obligation/evidence graph, heterogeneous review lanes, lifecycle epoch and MATERIAL-DELTA depth progression.

Use: research depth and root-cause owner.

### DeepLock V2.1

Recovered design separates Control / Cognitive / Verification planes, uses isolated first-pass review and real worker identity receipts, and keeps strict thresholds as an explicit acceptance profile.

Use: optional `STRICT_DEEPLOCK`, not default intelligence scoring.

### ARR v1.3

Recovered durable-runtime release includes goal CAS, authority fencing, UNKNOWN effect reconciliation, receiver-side delivery truth and semantic replay.

Use: only behind the explicit persistent-runtime capability gate.

## Second-round recovered control systems

### Deep Control v5 — local known-outcome evidence

Recovered verification report showed a naive low-yield streak stopping before a later CRITICAL finding. The corrected local validator used `surface_epoch`, mandatory-lens coverage and exact artifact-hash regression before optional stop; the recorded corrected suite passed 30/30.

Use: coverage-aware stop. Historical local receipt is not host-live evidence.

### GPT Deep Research focused replay v5 — receipt-only donor

Recovered verification receipt reports 154/154 local tests and names controls for query novelty, freshness/unknown-date handling, provenance concentration, counterevidence, retrieved-content injection risk, session query cache, full-source verification, citation-chain coverage, conflict disclosure and answer release.

Boundary: production source for that archived candidate was not recovered in this integration. Therefore these are treated as tested historical invariants to re-implement and re-test here, not copied executable code.

### Persistent Parallel Research & Execution Kernel v10.3.0

Recovered release receipts report 162/162 primary and portable local tests, isolated integration stages and locally distinct worker PID/method traces. The package explicitly did not claim ten frontier-model agents, live provider/search or ChatGPT account E2E.

Use: fresh-release receipts, Task Dossier / requirement-hypothesis-evidence-change-test-outcome discipline, isolated eval stages, explicit open obligations and rollback.

### AIREP v1.0.0

Recovered architecture review records a reduction from 47 legacy concepts to 8 stable core stages, 31 volatile regression cases, 59 deterministic tests and T0/T1/T2 evidence separation. Its fatal audit identified false global PASS from structure-only validators and required separate structural / installed-template / executable / behavioral-target truth.

Use: minimal capability frontier, validation-layer separation, no-skill utility and runtime attestation honesty.

## World-Class Source OS v2 — original GitHub implementation donors

The following mechanisms were recovered from exact commits in `xq22115/braintrust`; they are donor implementations, not automatically active runtime truth:

- `81729a8a...` — adaptive L0–L5 source/research orchestration;
- `65247eef...` — evaluator lifecycle and independent-method tribunal;
- `11bcbd70...` — C0–C6 checkpoint/replay contract;
- `f97051bc...` — sparse risk-triggered critics with zero consensus-vote inflation;
- `470f3cf8...` — bounded scheduler, duplicate coalescing, mutation mutex, cost/lineage caps and failure-class retry;
- `1a6b079f...` — evidence cache/delta refresh keyed by source/revision/claim scope/fragment digest;
- `a3715737...` — adaptive compute governor whose budgets are ceilings rather than quality quotas;
- `7d496b78...` — claim/evidence/authority graphs with claim-scoped authority, `do_not_infer` and open obligations;
- `9ad8a8bf...` — performance telemetry and SHADOW_ONLY vs OBSERVED_TARGET promotion;
- `a6b73268...` — mechanism casebook with preconditions, failure modes, transfer and anti-transfer boundaries;
- `3f2e8298...` — route authority separated from prestige/world-class labeling;
- `df0d2d99...` — 100-repository ordinary-chat harness landscape scan with the explicit warning that 100 GitHub repos are neither 100 domains nor 100 independent corroborations.

Only mechanisms that survive the current plugin's deterministic contracts/evals are promoted into this package.

## Core design consequences

1. Eight model-facing semantic owners remain; do not create a ninth mega-skill for these controls.
2. Machine-verifiable invariants live in contracts/scripts/evals rather than being expanded into always-loaded prose.
3. Research integrity includes query novelty, provenance/freshness, retrieved-content authority separation, counterevidence and citation release; search volume is not truth.
4. Evaluators have lifecycle and method diversity; a semantic judge cannot self-mint high-impact completion authority.
5. Skill composition is sparse and task-relevant, with no-skill/matched-reference attribution where marginal contribution matters.
6. Long-horizon replay uses capability-gated checkpoints and safe effect reconciliation; ordinary ChatGPT is not treated as a database/daemon.
7. Static/package CI proves only its observed validation layer. ChatGPT Desktop `HOST_LIVE` remains unproven until the owning surface runs the current exact revision.
