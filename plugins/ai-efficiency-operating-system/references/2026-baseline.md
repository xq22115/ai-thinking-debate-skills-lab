# 2026 baseline and borrowed mechanisms

Verification date: 2026-08-29.

This package borrows mechanisms, not prose, and keeps internal/user-specific acceptance rules separate from external framework claims. External projects are discovery/evidence sources for the scopes they actually test; popularity is never treated as proof.

## OpenAI

- **Plugins in ChatGPT and Codex**: current OpenAI Help Center guidance (updated 2026-08-29) describes the Plugin Directory as the cross-product workflow capability model. Plugins may contain skills, apps and app templates; skill-only plugins are possible. Installing/using a plugin still depends on plan, workspace, role, region, supported surface and included capabilities.
- **Plugin/app permission separation**: plugin availability/installation and the underlying app’s provider authentication, workspace access, supported read/write actions and approval controls are separate layers. Installing a plugin cannot bypass those controls.
- **GitHub marketplace import/sync**: current OpenAI guidance says marketplace sync imports plugin content and keeps it updated, but does **not** connect workspace members’ provider accounts or grant app permissions. An existing plugin ID can be preserved through marketplace migration using the documented `pluginId` mapping.
- **Desktop-only classification**: current OpenAI marketplace guidance notes that imported plugins declaring MCP servers can receive a Desktop-only label. Therefore a portable skill-only plugin should not declare MCP merely to appear more capable.
- **Skills in ChatGPT**: workspace role permissions separately govern skill creation/use, uploading, sharing, publishing and installing. Skill availability is not equivalent to tool/app authorization.
- **openai/plugins**: current official packaging uses `.codex-plugin/plugin.json`, `skills/`, optional per-skill `agents/openai.yaml`, references/scripts, and plugin-eval tooling.
- **plugin-eval**: static/package analysis, token/context accounting and benchmark comparison remain distinct from live host activation.

## Mature skill frameworks

- **obra/superpowers**: skill creation is treated like TDD; observe baseline failure, write the smallest effective skill, rerun pressure cases, refactor. Frequently loaded skills are kept thin; heavy material moves to references/scripts.
- **addyosmani/agent-skills**: skills are specific, verifiable and minimal; lifecycle ownership and trigger regression matter.
- **garrytan/gstack**: narrow opinionated skills rather than one universal prompt; domain knowledge is scoped rather than turned into a self-modifying global runtime.
- **OthmanAdi/planning-with-files**: persistent working state survives compaction/restart only when the host supplies the mechanism; writable reinjected state must not silently become authority.
- **Tencent/SkillHone**: optimize the whole skill folder, not only `SKILL.md`; separate eval data and skill data; record changes as reviewable Git artifacts and gate promotion on held-out validation.
- **Microsoft SkillOpt**: use bounded skill edits, held-out strict improvement, rejected-edit feedback and rollback instead of unbounded self-rewriting.
- **SkillsBench (arXiv:2602.12670)**: 7,308 trajectories show curated skills help on average but 16/84 tasks have negative deltas; focused 2–3-module skills outperform comprehensive documentation and self-generated skills provide no reliable average gain.
- **Agent Skills Can Be Harmful (arXiv:2608.11888, 2026-08-12)**: differential attribution found 307 skill-induced failures/regressions; seemingly relevant skills can cause excessive procedure, excessive verification and heavy implementation pipelines. This supports hard-negative routing and no-skill/semantically-matched counterfactuals.
- **Demystifying Agent Skills (arXiv:2608.14036, 2026-08-14)**: controlled experiments show procedural anchoring is a major benefit mechanism while skill retrieval precision falls sharply as pools grow. This supports keeping Expert Labs explicit-only rather than enlarging the default trigger pool.
- **Auto-Policy, not Auto-Skill (arXiv:2608.25091, 2026-08-25)**: argues that procedural skill text should not be allowed to carry machine authority implicitly. This independently supports DeepLock-style separation of workflow knowledge from typed permission/policy controls.

## Harness / capability engineering

- **Model × harness is a first-class variable**: current harness benchmarks and public paired evaluations show that the same model can materially change outcome under different orchestration/tool/context environments. A model limitation is not inferred before harness/tool/session differentials are tested.
- **Long-horizon harnesses** increasingly use durable state and fresh-context controller/executor/auditor patterns rather than trusting ever-growing chat history.
- **Short/simple tasks are a hard negative**: heavier harnessing can add no value or regress efficiency, so capability modules are demand-loaded.
- **Capability truth is layered**: product docs, installed packages, visible tools, permissions, loadability, invocation, real effects and verified postconditions are separate states.
- **Capability Boundary Recon** therefore tests plan/rollout, workspace policy, role, plugin state, required apps, provider account/auth, action controls, supported surface, session registration, runtime tool visibility, invocation and postcondition before labeling a limitation as model-level.

## MCP / tool-surface engineering

- **MCP-Zero (arXiv:2506.01056 / xfey/MCP-Zero)**: active tool discovery is motivated by large tool catalogs; its published dataset contains 308 servers / 2,797 tools. This is a source for retrieval-style tool discovery, not a universal production prescription.
- **dynamic-discovery-mcp**: demonstrates a proxy/meta-tool pattern that exposes discovery/invocation tools while deferring upstream schemas and even whole MCP connections; useful for progressive disclosure when fidelity is preserved.
- **Microsoft 365 Copilot dynamic MCP tool discovery (2026-07-14 docs)**: resolves MCP tool definitions at runtime rather than freezing publish-time catalogs, reinforcing runtime schema freshness and entitlement/user-specific surfaces.
- **MCP Security: Threat Modeling and Tool Poisoning Attacks (JCP 2026)**: reproducible threat-model/tool-poisoning artifacts show that MCP tool metadata and returned content must remain in an untrusted external-data domain.
- **Risk-Aware Reranking for Agentic Tool Retrieval (arXiv:2608.22751, 2026-08-24)**: treats retrieval as a pre-execution boundary and separates task relevance from risk exposure. This supports risk-aware candidate selection before tool invocation.
- **Tools Are Not Islands (arXiv:2607.25718)**: motivates set-level tool retrieval where the utility/compatibility of the chosen tool set matters, not only each tool’s isolated similarity score.
- **ToolSense (arXiv:2606.12451)**: shows that tool retrieval evaluated on overly explicit tool-naming queries can substantially overestimate performance on realistic ambiguous requests. Hard-negative/vague-query retrieval tests are therefore required.

## AI-assisted authorized reverse engineering

- **SumTuusDeus/ghidra-mcp**: headless PyGhidra MCP implementation exposing binary load/decompile/call-graph/byte-pattern/annotation operations. It demonstrates reproducible headless analysis but does not define our authorization policy.
- **bethington/ghidra-mcp / GhidraPluginProject** and other 2026 Ghidra MCP implementations demonstrate larger tool surfaces, batching/transactions and version-aware annotation transfer patterns.
- **NSA Ghidra issues #9352/#9354/#9355 (2026-07)** document community proposals for native MCP integration; these are proposals/issue history, not proof that official Ghidra ships a supported native MCP server.
- **evilsocket/ghidra-re** demonstrates an agent wrapper around a Ghidra MCP workflow.
- **Rev·Deck (`biniamf/ai-reverse-engineering`)** demonstrates an evidence-first local static-analysis workstation where findings are grounded in inspectable Ghidra artifacts instead of unconstrained model claims.
- **auto-re-agent (`Dryxio/auto-re-agent`)** demonstrates reverser/checker separation and conservative evidence bundles around build/test/runtime parity.
- Dynamic analysis may use authorized instrumentation such as Frida only when it discriminates a material hypothesis. Reverse engineering never becomes a license/DRM, authentication/access-control, credential, persistence or unauthorized-target bypass mechanism.

## Runtime provenance / agent forensics

- **ByteYellow/AgentProvenance (2026)** correlates model intent, application context and runtime telemetry into a content-addressed evidence DAG spanning tool calls, processes, file/network events, artifacts, taint, diff/blame/replay and audit manifests. The project explicitly treats itself as an evidence layer rather than a generic sandbox or final reward/verdict engine.
- This package borrows the separation of evidence planes and causal lineage, not claims of kernel-level observability on hosts where such telemetry is unavailable.

## Deep-research verification

- **DeepTRACE (ICLR 2026)** and 2026 citation-audit research reinforce that fluent deep research can still have incomplete/incorrect citation support.
- **Cited but Not Verified (arXiv:2605.06635)** separates link validity, relevance and fact verification; increasing tool-call volume does not monotonically improve factual citation quality.
- **From Fluent to Verifiable (arXiv:2602.13855)** motivates claim-level auditability/provenance rather than citation-count proxies.
- Therefore AI Ecosystem Recon uses citation-chain checks, provenance-family concentration, conflict disclosure and a MATERIAL-DELTA stop rule rather than “search more” as a universal answer.

## 2026 research constraints

- Multi-agent debate can converge on shared error; diversity and isolated first-pass evidence are more important than raw seat count.
- Tool availability is not monotonic utility; irrelevant/distracting tools can reduce performance, so tools are demand-loaded.
- Tool retrieval is not semantic search alone; relevance, risk, authority, host compatibility and set-level utility are independent axes.
- Skill usefulness is task/model/harness dependent; a positive aggregate benchmark cannot justify enabling every skill on every task.
- Self-evolving skill pools can accumulate contamination; promotion needs pre-commit evaluation, bounded edits, independent/held-out validation, rejected-change history and rollback.
- Persistent working memory improves recovery only when the actual host supplies the persistence/reinjection mechanism; reinjected writable state must not become an authority-escalation channel.
- Agent/runtime telemetry is capability-gated. Missing telemetry creates an evidence gap; skill prose cannot fabricate processes, eBPF events, files, workers or network traces.
- Procedure and authority remain separate: a skill can recommend a workflow, but it cannot mint permissions that the host/product/provider does not grant.

## Internal validated lineage

The package also incorporates prior user artifacts at the strongest actually observed evidence level:

- **Executive Harness v1.0.0** — 54/54 local tests, 8/8 lint, deterministic routing corpus, distribution parity; live ChatGPT trigger remained unproven.
- **Deep Task Integrity** — adaptive depth, temporal breadth, 12 search operations, evidence graph and two-no-delta pivot.
- **DeepLock V2.1** — authority separation, real-worker identity, evidence-family accounting, optional strict external completion gate.
- **ARR v1.3** — logical/control/effect-delivery/temporal-witness separation and durable effect semantics.
- **Deep Control v5** — durable event/state ledger, surface-epoch-aware convergence, semantic compaction, content-addressed observations, changed-strategy retry/circuit-breaker principles.
- **World-Class Source OS v2** — adaptive compute/source qualification, sparse critics, evaluator lifecycle/tribunal, evidence cache and checkpoint/replay mechanisms recovered from original `xq22115/braintrust` commits.
- **GPT Deep Research focused replay v5** — receipt-only donor: query novelty, provenance concentration, citation/release gates were recovered from verification artifacts; production source was not recovered, so its reported test count is not treated as directly replayable proof.
- **Persistent Parallel Research Kernel v10.3** — release receipts preserve task-dossier/evidence/change/test lineage and explicitly distinguish local package/runtime assurance from unexecuted live-provider/account/browser tests.
- **AIREP v1.0.0** — 47 concepts reduced to 8 stable core skills; paired/no-skill utility, hard-negative activation, Minimal Capability Frontier, and structural/installed/executable/behavioral validation separation.

None of those historical local results are upgraded into current ChatGPT Desktop `HOST_LIVE` evidence without a fresh owning-surface probe.
