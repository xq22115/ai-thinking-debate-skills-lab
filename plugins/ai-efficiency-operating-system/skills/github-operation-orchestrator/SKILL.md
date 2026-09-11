---
name: github-operation-orchestrator
description: Use when GitHub work requires a reliable multi-step read/search/analyze/tool-call/write/PR/workflow/verification loop, especially for plugin or skill pulls, search underfetch, repeated connector failures, partial results, branch mutations, or claims that source changes are actually live.
---

# GitHub Operation Orchestrator

## Core principle

Treat GitHub work as one **evidence-bound state machine**, not a bag of repository tools. The unit of success is the user's requested postcondition on the exact target/revision, not a successful connector response.

For ordinary ChatGPT GitHub work, use all three contracts:

- machine operation loop: `../../adapters/chatgpt/github-pull-runtime.json`;
- human operation loop: `../../adapters/chatgpt/GITHUB_OPERATION_LOOP.md`;
- upstream ownership/capability boundary: `../../adapters/chatgpt/github-upstream-capability-contract.json` and `../../adapters/chatgpt/GITHUB_ROOT_CONTROL_PLANE.md`.

## Root-owner gate

Before repairing a recurring GitHub failure, identify the **first layer that actually owns the failed behavior**:

`ChatGPT host/plugin state -> canonical OpenAI GitHub plugin dependency -> live GitHub connector action schema -> GitHub remote state -> local orchestrator policy`

Do not assume this skill owns the GitHub connector. The local plugin can improve planning, search fanout, live-schema discovery, action selection, argument construction, fallback, read-back, and verification. It cannot add connector actions, expand the connector endpoint allowlist, grant GitHub App/OAuth scopes, or create arbitrary remote execution.

Classify the root before changing anything:

- missing action after live discovery -> `UPSTREAM_CAPABILITY_GAP`;
- action exists but host/plugin approval or enablement blocks it -> `HOST_PERMISSION_POLICY`;
- action exists but GitHub rejects repository authority -> `GITHUB_REMOTE_PERMISSION`;
- shallow search plan / explicit breadth target not preserved -> `CALLER_SEARCH_UNDERFETCH`;
- remembered/stale parameters -> `CALLER_SCHEMA_STALE`;
- truncated response treated as complete -> `CALLER_RESPONSE_TRUNCATION`;
- lower-layer success promoted to completion -> `CALLER_CHAIN_BREAK`.

Only repair the layer that owns the failure. Never paper over an upstream capability gap with a longer prompt.

## When to activate

Activate when at least one is true:

- the task spans multiple GitHub stages such as discover -> read -> analyze -> mutate -> verify;
- a plugin/skill/repository pull must be proven installed, registered, executed, or effective;
- search, fetch, write, PR, workflow, schema, permission, or response-shape failures are recurring;
- the user sets an explicit GitHub search breadth target that must be measured and closed;
- a GitHub write must preserve rollback, blob SHA, branch identity, and read-back integrity;
- a workflow/CI result must be bound to the exact commit and user acceptance criterion;
- a prior GitHub tool call returned success but the requested state/effect remains uncertain.

Do not activate merely because the word GitHub appears in a simple explanation-only question.

## Workflow

1. **Lock the goal.** Preserve objective, exact effect/deliverable, acceptance criteria, authority ceiling, target identity, critical unknowns, evidence plan, numeric breadth targets, and stop conditions.
2. **Resolve root owner.** Determine whether the current blocker belongs to host/plugin state, live connector capability/schema, GitHub remote permission/state, or the local caller/orchestrator.
3. **Resolve identity.** Determine exact owner/repository, default branch, target ref/path/PR/workflow, current revision, and observed permissions. Once identity is known, prefer exact lookup over ranked search.
4. **Build the read/search plan.** Read the smallest authoritative set that can resolve the decision. Broad search/tree results locate candidates; exact object fetches establish material facts. If the user requested a numeric result count, preserve it as a hard acceptance target and fan out until it is met or exhaustion/blockage is proven.
5. **Classify evidence.** Keep `OBSERVED`, `DERIVED`, `HYPOTHESIS`, and `UNKNOWN` distinct. Do not mutate on a decision-critical hypothesis when a discriminating test is practical.
6. **Resolve the live tool schema.** Narrowly discover the exact GitHub action when its schema is not already current. Validate required fields, enums, IDs, SHA/ref semantics, and write behavior. Never invent parameters from memory.
7. **Run invocation preflight.** Confirm the action advances the current subgoal, identifiers are current, effect class is understood, rollback exists for material writes, and the expected postcondition is explicit.
8. **Invoke and classify.** Separate transport success from task success. Preserve target, mechanism, status/error, evidence delta, and legal next actions before chaining another material call.
9. **Mutate safely.** Pre-read, record base and blob SHA, prefer a branch for non-trivial work, serialize dependent same-path writes, and keep rollback available.
10. **Read back.** Independently fetch the exact target branch/object and compare intended versus observed content/state. A commit SHA or PR URL alone is never completion proof.
11. **Observe execution.** If the user asked to run/test/install/activate, distinguish repository state, workflow request, workflow result, installation, invocation, and observable effect. Verify at the highest claimed layer.
12. **Recover by failure class.** Search miss -> exact lookup or query fanout; truncation -> continuation/targeted refetch; schema mismatch -> rediscover schema; stale SHA -> re-read/reconcile; partial success -> continue from observed remote state; permission failure -> verify actual owner/authority; repeated no-delta failure -> change causal mechanism.
13. **Verify and close.** Test acceptance criteria, applicable invariants, exact revision, at least one causally relevant fallback/failure path when practical, and adjacent regression. Only then return PASS.

## Search breadth protocol

When the user requests a minimum such as 100 GitHub results/sources, do not silently collapse that to the connector's default page or a single query.

- preserve the requested count as a hard acceptance criterion;
- use the largest currently supported `topn` appropriate to the live schema;
- fan out across exact names/symbols, synonyms, error/behavior phrases, repository/org scopes, issue/PR/commit/workflow surfaces, and version/date terms;
- deduplicate by canonical repository object identity;
- count **unique** results, not tool-call volume;
- treat tool-response truncation as partial transport, not search exhaustion;
- continue with a materially different query until the target is met, connector exhaustion is observed, no new unique results appear across materially different queries, or a hard capability/permission blocker is proven;
- fetch exact objects for load-bearing conclusions; snippets remain discovery evidence.

A single shallow query is never evidence that only one to three relevant GitHub objects exist.

## Per-call operation envelope

For material calls maintain enough state to answer:

- What exact subgoal is this call advancing?
- Which layer owns this capability or blocker?
- What exact GitHub object and revision is targeted?
- What authority and preconditions were observed?
- Which live action/schema is being used?
- What identifiers/arguments came from current evidence?
- What observable postcondition would justify continuing?
- What result class and evidence delta occurred?
- What next transitions are now legal?
- What rollback or recovery path exists?

Do not expose private chain-of-thought; produce concise evidence-backed decision records when the user needs an audit trail.

## No-progress rule

Retrying with different wording is not a different route.

After each failed/inconclusive attempt compare the evidence fingerprint. If two same-mechanism attempts produce no material change in target identity, revision/version, live schema/permission, failure class, discriminating evidence, observable state, unique search result set, or legal next action, switch mechanisms.

## Execution boundary

The ordinary-ChatGPT GitHub connector is not an arbitrary shell executor. Existing workflow rerun and new workflow dispatch are different capabilities. If no dispatch action exists on the live tool surface, prefer repository-controlled automatic triggers such as PR/push workflows when that advances the user's goal, and bind any run to the exact commit.

Never claim a missing connector action was "implemented" by adding a local instruction. Report `UPSTREAM_CAPABILITY_GAP` and use a genuinely different capable path only when one is available and authorized.

## Completion statuses

- `PASS`: requested effect is verified on the exact target/revision and applicable invariants/regressions pass.
- `FAIL`: a required behavior or invariant failed and remains unsatisfied.
- `BLOCKED`: a concrete missing permission/capability/external dependency prevents the next valid transition.
- `NOT_RUN`: required execution or verification has not occurred.

Never promote partial success, a green unrelated workflow, repository configuration, plugin installation, connector transport success, or host permission setting to a higher layer.

## Composition

Typical rich bundle: `task-goal-intelligence` -> `github-operation-orchestrator` -> `evidence-watchdog`.

Escalate narrowly when the blocker is specialized:

- live tool namespace/schema/context pressure -> `mcp-surface-engineering`;
- apparent success with missing runtime effect -> `agent-runtime-forensics`;
- capability/permission/session/surface uncertainty -> `capability-forensics`;
- current external/maintainer evidence required -> `executive-research`.

Keep implicit composition bounded; do not load specialists merely because their nouns appear.

## Boundary

Do not broaden repository/app permissions, bypass authorization, force-push over divergence, mutate an ambiguous target, or claim control over the upstream connector just to keep the loop moving. A verified `UPSTREAM_CAPABILITY_GAP` or `BLOCKED` state is better than fabricated completion.
