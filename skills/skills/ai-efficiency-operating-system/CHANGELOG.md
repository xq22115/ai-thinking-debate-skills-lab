# Changelog — AI Efficiency Operating System

## 0.4.1-rc1 — 2026-08-29

Integrated the prior search-depth / reasoning-depth research into the existing canonical owner without creating a competing top-level alias.

### Added — canonical research/reasoning depth subsystem

New package file:

- `RESEARCH-REASONING-DEPTH.md`

It adds:

- decision-relevant information gain as the definition of real depth;
- a research contract bound to the active task contract;
- eight query lanes covering direct answer, mechanism, primary source, freshness, failure, counterevidence, alternative path and runtime proof;
- a four-pass research loop: broad map → blind-spot expansion → falsification/adversarial → cross-verification;
- freshness/name/path lifecycle labels (`CURRENT / CURRENT_WITH_COMPAT / STALE_REFERENCE_ONLY / SUPERSEDED / INVALID`);
- evidence-family clustering so reposts and shared reporting lineages do not inflate independent support;
- `INCOMPLETE_EVIDENCE` for unresolved material claims;
- source-class priority with owning-runtime/direct evidence above summaries;
- claim ledger, competing-hypothesis status, adaptive stop rules and P0–P3 depth budgeting;
- explicit retirement of fixed-time pseudo-depth, duplicate-source vote inflation, stale route retention, ornamental research and post-decisive over-searching.

### Integration policy

The subsystem is owned by `ai-efficiency-operating-system`. Existing specialist skills remain authoritative for their narrow responsibilities: `evidence-gap-research`, `competing-hypotheses`, `root-cause-clustering`, `compatibility-audit`, `multi-agent-deliberation`, `completion-gate`, and `recoverable-state`.

The catalog now registers this routing and adds shared invariants:

- `SOURCE_COUNT != EVIDENCE_INDEPENDENCE`
- `ELAPSED_TIME != REASONING_DEPTH`
- `NEWER != MORE_AUTHORITATIVE`
- `STALE_NAME_OR_PATH != CURRENT_ROUTE`

Host/runtime activation remains unverified until an owning runtime loads and exercises this exact package revision.

## 0.4.0-rc1 — 2026-08-29

Major evolution from v0.3's explicit hidden-state model into **authority-separated, calibrated-action orchestration**.

### Root-cause upgrade

v0.3: implicit context is hidden state.

v0.4: **authority co-location is hidden coupling**. A single fallible context must not simultaneously own proposal, authority, effect truth, evidence interpretation, completion verdict, receiver ACK and durable-memory promotion.

v0.4 also treats **action competence, abstention competence and tool adjudication as distinct capabilities**.

### Added — 10 new canonical modules

- `authority-plane-separation`
- `unknown-effect-reconciliation`
- `goal-version-cas-and-semantic-action-identity`
- `verifier-admission-canary-registry`
- `interaction-topology-preflight`
- `correlated-consensus-evidence-clustering`
- `agentic-abstention-and-timely-stop`
- `tool-invocation-adjudication-separation`
- `skill-lifecycle-model-aware-adaptation`
- `successor-conditioned-portable-handoff`

Total machine-readable modules: **57**.

### Strengthened existing owners

- delivery now requires receiver/independent-observer ACK; sender cannot self-ACK;
- memory authority now carries source/content lineage and authority ceilings;
- materialization adds source/package/install path+hash+size distribution parity;
- event-driven waiting distinguishes schedule metadata from execution/liveness receipts;
- resume/fencing includes no-parallel-resume and durable cancellation intent;
- completion vetoes ambiguous effects and unresolved hard obligations;
- multi-agent confidence is clustered by provenance/model/prompt/evidence route;
- skill admission is explicitly model/host-conditioned and lifecycle-managed.

### Runtime state

Schema expands to `v0.4` with:

- goal lineage/CAS;
- authority lineage;
- effect ledger with first-class `UNKNOWN`;
- interaction topology;
- evidence independence clusters;
- verifier admission registry;
- abstention ledger;
- tool adjudication;
- model-aware skill lifecycle;
- successor handoff envelopes;
- lifecycle receipts;
- distribution parity receipts.

### Evaluation

Behavioral/evolution contract expands from **T01–T50 → T01–T70**.

New tests cover authority co-location, UNKNOWN effects, stale goal versions, semantic action identity, receiver self-ACK, verifier drift, non-interactive approval deadlocks, delegation-framed authority, correlated consensus inflation, act/abstain pairs, post-hoc abstention, blind tool deference, tool/evidence conflicts, leave-one-out skill value, model-dependent skill harm, handoff debt, successor-view integrity, distribution parity and schedule/liveness false health.

### Cross-chat recovery

v0.4 incorporates previously underused account artifacts including ARR architectures, DeepLock V2.1, Executive Harness, R57 interaction-topology and research ledgers, ordinary-Chat convergence/performance verification and long-task recovery tests.

### Research calibration

Added 2026 research signals on agentic abstention, tool deference, dynamic skill lifecycle, model-aware skills, handoff debt and structured human-agent handoff. Research caveats remain explicit; preprints/local tests do not become production proof.

### Naming

No new efficiency alias was created. Canonical owner remains:

`ai-efficiency-operating-system`

## 0.3.0-rc1 — 2026-08-29

Evolved v0.2 into an explicit hidden-state operating system with 47 modules and T01–T50, adding instruction scope/provenance, per-agent context lineage, failed-turn quarantine, semantic-compaction rollback, observation caching, changed-strategy retry/circuit breaker, worker/verifier separation, event-driven waiting, branch-scoped degradation, delivery states, protocol contracts, skill-admission metrics, memory authority, input fidelity, temporal witness and physical materialization coverage.

## 0.2.0-rc1 — 2026-08-28

Evolved the original thin orchestration index into a layered contract with 29 modules, E0–E6 evidence levels, demand-loaded context/tools, adaptive multi-agent routing, recoverable execution, performance separation, completion state, runtime schema, source matrix and 31 evals.

## 0.1.0-rc1 — 2026-08-28

Initial orchestration package with 15 flat skill entries, A01–A10 responsibility topology, basic provenance classes, GitHub read-back gate and single canonical naming policy.
