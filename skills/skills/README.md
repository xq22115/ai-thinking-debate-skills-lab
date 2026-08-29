# Evidence-Gated Deliberation & Skills OS — RC1 Skills

Status: `EXPERIMENTAL / NOT HOST-LIVE VERIFIED`

The skill folder shape follows the current Agent Skills semantic pattern: each portable skill is self-contained and centered on `SKILL.md` with YAML frontmatter containing at least `name` and `description`. Host-specific packaging/adapters remain separate.

## RC1 Core Skills

1. `evidence-gap-research` — claim/evidence closure and counterevidence search.
2. `competing-hypotheses` — materially different explanations and discriminating tests.
3. `root-cause-clustering` — mechanism-level repair instead of symptom patching.
4. `completion-gate` — prevents false `done` / `verified` / `deployed` claims; exact-revision and infrastructure-state aware. (`0.1.1-rc1`)
5. `recoverable-state` — external checkpoints for long-horizon work.
6. `compatibility-audit` — host/OS/version/permission/product-surface checks with source-class separation. (`0.1.1-rc1`)
7. `multi-agent-deliberation` — dynamic 1–30 role coverage pool routed by marginal information gain; runtime independence is evidence-gated. (`0.1.1-rc1`)
8. `capability-challenge` — separates `VISIBLE`, `AUTHORIZED`, and `VERIFIED` before terminal `cannot`. (`0.1.1-rc1`)
9. `durable-agent-control-plane` — durable task identity, isolated writers, receipts, resume/recovery, and task-result vs infrastructure-state separation. (`0.1.1-rc1`)
10. `ai-efficiency-operating-system` — single canonical orchestration owner for goal protection, authority/effect/evidence separation, context/tool economy, deep reasoning/research, execution recoverability, completion truth and model-aware skill lifecycle. Its canonical research subsystem is `ai-efficiency-operating-system/RESEARCH-REASONING-DEPTH.md`; do not create competing `deep-thinking-*`, `research-os-*`, or `efficiency-*` aliases for the same responsibility.

## Composition Order

For complex engineering/research tasks, recommended default composition:

`ai-efficiency-operating-system (task contract + routing) → capability-challenge → compatibility-audit → research-reasoning-depth subsystem when research depth is material → evidence-gap-research → competing-hypotheses → root-cause-clustering → multi-agent-deliberation (only if useful) → durable-agent-control-plane (when execution spans actors/interruptions) → execution → completion-gate → recoverable-state checkpoint`

The orchestrator should omit skills when their trigger conditions are absent. The research-depth subsystem is not a new top-level skill: it is owned by `ai-efficiency-operating-system` and delegates specialist procedures to the existing evidence, hypothesis, root-cause, compatibility, deliberation and completion skills rather than duplicating them.

## Shared Hard Invariants

- `UNKNOWN != IMPOSSIBLE`
- `FAILED_PATH != FAILED_GOAL`
- `VISIBLE != AUTHORIZED != VERIFIED`
- `DOCUMENTATION != RUNTIME_PROOF`
- `CONFIGURED != VERIFIED_DIRECT`
- `CONFIDENCE != EVIDENCE`
- `CONSENSUS != CORRECTNESS`
- `LOCAL_TEST_PASS != HOSTED_CI_PASS`
- `REPOSITORY_ARTIFACT != PROVIDER_LIVE_EXECUTION`
- `TOOL_SUCCESS != TASK_COMPLETE`
- `PRE_STEP_INFRA_FAILURE != TEST_FAILURE`
- `SOURCE_COUNT != EVIDENCE_INDEPENDENCE`
- `ELAPSED_TIME != REASONING_DEPTH`
- `NEWER != MORE_AUTHORITATIVE`
- `STALE_NAME_OR_PATH != CURRENT_ROUTE`

## Promotion Rule

No skill moves from `EXPERIMENTAL` to `STABLE` until positive, negative, ambiguous-trigger, stale-version, unsupported-host, adversarial, permission, infrastructure-blocker, and regression cases appropriate to that skill are tested.

For research-depth behavior, promotion additionally requires evidence that query expansion improves decision-relevant accuracy, freshness checks catch obsolete names/paths, counterevidence search reduces false confidence, duplicate-source clustering prevents vote inflation, adaptive stopping avoids ornamental over-research, and simple tasks do not incur unnecessary browsing.

## Portability Boundary

These files describe portable procedural logic. Host-specific plugin manifests, tool calls, sandbox APIs, filesystem paths, permissions, schedulers, MCP/SDK details, and deployment mechanisms belong in adapters rather than in the portable core.

Current product documentation may change faster than these portable contracts. Re-run `compatibility-audit`, apply the research subsystem's freshness/name gate, and use current primary product/spec sources before direct host installation.
