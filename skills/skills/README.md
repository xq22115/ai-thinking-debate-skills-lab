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
7. `multi-agent-deliberation` — evidence-gated Expert Debate Council with canonical five-lane core, dynamic 1–30 role coverage, cross-chat single-writer coordination, Web logical-role projection, minority preservation, and owning-runtime verification; runtime independence is never inferred from role labels. (`0.1.3-rc1`)
8. `capability-challenge` — separates `VISIBLE`, `AUTHORIZED`, and `VERIFIED` before terminal `cannot`. (`0.1.1-rc1`)
9. `durable-agent-control-plane` — durable task identity, isolated writers, receipts, resume/recovery, and task-result vs infrastructure-state separation. (`0.1.1-rc1`)

## Composition Order

For complex engineering/research tasks, recommended default composition:

`capability-challenge → compatibility-audit → evidence-gap-research → competing-hypotheses → root-cause-clustering → multi-agent-deliberation (only if useful) → durable-agent-control-plane (when execution spans actors/interruptions) → execution → completion-gate → recoverable-state checkpoint`

The orchestrator should omit skills when their trigger conditions are absent. For multi-agent deliberation, bind the council to the current Goal Contract/goal version before material debate and stop debating when execution, measurement, or owning-runtime read-back has higher expected information value.

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
- `ROLE_DIVERSITY != RUNTIME_INDEPENDENCE`
- `REPOSITORY_SKILL_PERSISTED != CHATGPT_WEB_NATIVE_ALL_CHAT_DEPLOYED`

## Promotion Rule

No skill moves from `EXPERIMENTAL` to `STABLE` until positive, negative, ambiguous-trigger, stale-version, unsupported-host, adversarial, permission, infrastructure-blocker, and regression cases appropriate to that skill are tested.

## Portability Boundary

These files describe portable procedural logic. Host-specific plugin manifests, tool calls, sandbox APIs, filesystem paths, permissions, schedulers, MCP/SDK details, and deployment mechanisms belong in adapters rather than in the portable core.

Current product documentation may change faster than these portable contracts. Re-run `compatibility-audit` and use current primary product/spec sources before direct host installation.
