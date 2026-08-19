# 16 — Governance & Autonomy Convergence from Other Chats

Date: 2026-08-18

This note distills portable design principles from other GitHub-backed chat work without copying repository-specific automation into the RC1 portable skills layer.

## Internal inputs

### PR #28 — High-autonomy Copilot orchestration layer

Observed branch/head at review:
- branch: `feat/autonomy-orchestrator-v2`
- head: `1693b8856e4b6e4ddc8a612d3dbcc26f04479cf4`

Portable findings:
- expose a wide **available** capability surface, but activate the smallest sufficient toolset per task;
- delegate only when the runtime actually exposes delegation/subagents;
- keep routine reversible work autonomous;
- keep hard denials narrow and machine-checkable;
- tool visibility is not host authorization;
- backend/read-back evidence is required before claiming GitHub/MCP/admin state is active;
- file write, command exit, or model prose is not completion evidence.

### PR #25 — AI Master System control layer

Observed branch/head:
- branch: `setup/ai-master-system`
- head: `6fade9aec8bea092e7c9ef96a2d76d0bd4c09c32`
- state at review: merged

Portable findings:
- central capability discovery registry;
- separate agents, skills, prompts, configs and MCP assets;
- explicit verification states;
- no secrets in repository state;
- additive AI control layer should preserve existing repository governance.

### PR #19 — Proof-carrying governance / Agent Core V6

Observed branch/head:
- branch: `agent-core-v5-admin-drift-20260817`
- head: `f80992b4d2a2500f47d9475fb663700a78d9523b`

Portable findings:
- exact required-check identity includes workflow path, exact head and selected run;
- security-sensitive policy/evaluator material can require immutable base binding;
- proof ledgers should bind base/head, run IDs, hashes and evidence digests;
- execution infrastructure state must distinguish code/test failure from billing-blocked, runnerless, skipped, cancelled or queued states;
- structural health, read-only drift observation and mutation/convergence are separate responsibilities.

---

# Portable synthesis

## 1. Capability truth has three layers

Do not collapse these into one boolean:

```text
VISIBLE      = capability/tool is exposed to the runtime
AUTHORIZED   = backing credential/app is permitted to perform the action
VERIFIED     = a real consumer/read-back proves the requested capability works
```

A visible GitHub, MCP or admin tool is not proof of authorization or successful operation.

## 2. High autonomy should be permission-honest

Recommended default:

- read/search/inspect: autonomous;
- reversible feature-branch edits: autonomous;
- tests and repair loops: autonomous;
- PR creation/update: autonomous when connector permits it;
- external irreversible action: explicit gate;
- credentials/secrets: never infer, expose or fabricate;
- admin mutation: require an actually authorized surface plus read-back;
- destructive/default-branch/force operations: narrow deny/escalation.

This avoids both failure modes:

- **approval wall** — asks unnecessarily for every reversible action;
- **fake autonomy** — claims permissions or actions the host never granted/executed.

## 3. Wide available surface, small active surface

A capable runtime may expose many tools, but each task should activate only the smallest sufficient set.

Benefits:
- lower tool-selection ambiguity;
- smaller attack surface;
- clearer provenance;
- easier debugging;
- less accidental duplicate work.

This is the tool-routing analogue of the RC1 deliberation rule:

> scale by marginal value, not raw count.

## 4. Registry before invention

Before adding a new prompt, skill, agent, MCP integration or adapter:

1. query the capability registry;
2. inspect existing trigger/scope;
3. reuse if sufficient;
4. extend if the responsibility is the same but incomplete;
5. create a new capability only when it has a genuinely distinct trigger, contract or eval.

A future registry should record at least:

```yaml
name:
type: agent|skill|prompt|tool|adapter|workflow
status: active|experimental|blocked|deprecated
entrypoint:
compatibility:
permissions:
verification:
source_revision:
```

## 5. Proof-carrying status

Status words should carry receipts.

Base status vocabulary:

```text
PASS
FAIL
BLOCKED
NOT_RUN
```

For infrastructure failures, preserve the observed class when evidence supports it:

```text
BILLING_BLOCKED
PERMISSION_BLOCKED
AUTH_BLOCKED
RUNNER_UNAVAILABLE
DEPENDENCY_UNAVAILABLE
```

Never convert `steps=null` into a code-test failure when no test step ran.

## 6. Exact-revision evidence

For change-sensitive claims, record:
- base SHA;
- head SHA;
- workflow/path identity;
- run/job IDs;
- selected evidence timestamp;
- hashes of load-bearing policy/config when useful.

Newer evidence on the same revision supersedes stale evidence when they conflict.

## 7. Separate observation from mutation

For governance/admin/control-plane work:

```text
STRUCTURAL CONTRACT
      ↓
READ-ONLY DRIFT / CAPABILITY PROBE
      ↓
PLAN / PRECHECK
      ↓
EXPLICIT MUTATION SURFACE
      ↓
READ-BACK
      ↓
RECEIPT / ROLLBACK STATE
```

Do not make the same component both the only writer and the only judge of success when independent read-back is available.

## 8. Product guidance vs repository-state evidence

A new source-conflict class is required for fast-moving AI products:

```text
PRODUCT_GUIDANCE
REPOSITORY_CONTENT
REPOSITORY_METADATA
RUNTIME_OBSERVATION
```

These can disagree without one automatically invalidating the others.

### OpenAI Codex example, 2026-08-18

Current official OpenAI product guidance states that plugins are a primary packaging/discovery surface for ChatGPT and Codex workflows and can contain skills, apps and app templates. The official `openai/skills` README explicitly marks that repository deprecated and points users toward plugins/build-plugin guidance. The `openai/plugins` README documents a required `.codex-plugin/plugin.json` manifest for its plugin examples.

At the same time, GitHub repository metadata observed for `openai/plugins` reports the repository as archived.

Therefore the defensible conclusion is **not** “archived repo means plugins are deprecated.” Instead:

- current product behavior/guidance should be sourced from current OpenAI product/developer documentation;
- an archived example repository can remain useful as a format/example snapshot;
- repository metadata should be recorded separately from product-status claims;
- if official product docs and example repository text diverge, flag an upstream documentation inconsistency rather than silently choosing one.

### Google ADK example, 2026-08-18

The current `google/adk-python` README identifies ADK 2.0 and explicitly documents breaking changes to agent API, event model and session schema. It states ADK 2.0 sessions are readable by ADK 1.28+ with extra fields ignored, while older 1.x versions are incompatible.

This confirms why compatibility claims need exact version boundaries rather than a generic “ADK compatible” label.

---

# RC1 impact

These findings strengthen the existing portable core:

- `capability-challenge` should test **VISIBLE vs AUTHORIZED vs VERIFIED**;
- `completion-gate` should require exact-revision or direct read-back evidence for mutable host claims;
- `compatibility-audit` should include permission/runtime surface, not only OS/version;
- `durable-agent-control-plane` should model infrastructure blockers separately from task failures;
- `multi-agent-deliberation` should use a wide role pool but a small active set chosen by information gain;
- future capability registries should prevent duplicate prompts/skills/agents from accumulating invisibly;
- source governance should distinguish product docs, repository content, repository metadata and runtime observation.

## Non-import decision

PR #28, #25 and #19 contain repository-specific GitHub/Copilot/admin automation. RC1 should distill principles and tests, not blindly copy those implementation files into the portable skills layer.

Architecture boundary:

`portable reasoning contract != one repository's host automation`
