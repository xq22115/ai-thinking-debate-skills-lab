---
name: github-operation-orchestrator
description: Use when GitHub work requires a reliable multi-step read/search/analyze/tool-call/write/PR/workflow/verification loop, especially for plugin or skill pulls, repeated connector failures, partial results, branch mutations, or claims that source changes are actually live.
---

# GitHub Operation Orchestrator

## Core principle

Treat GitHub work as one **evidence-bound state machine**, not a bag of repository tools. The unit of success is the user's requested postcondition on the exact target/revision, not a successful connector response.

For ordinary ChatGPT GitHub work, the canonical machine contract is `../../adapters/chatgpt/github-pull-runtime.json` and the human operational projection is `../../adapters/chatgpt/GITHUB_OPERATION_LOOP.md`.

## When to activate

Activate when at least one is true:

- the task spans multiple GitHub stages such as discover -> read -> analyze -> mutate -> verify;
- a plugin/skill/repository pull must be proven installed, registered, executed, or effective;
- search, fetch, write, PR, workflow, schema, permission, or response-shape failures are recurring;
- a GitHub write must preserve rollback, blob SHA, branch identity, and read-back integrity;
- a workflow/CI result must be bound to the exact commit and user acceptance criterion;
- a prior GitHub tool call returned success but the requested state/effect remains uncertain.

Do not activate merely because the word GitHub appears in a simple explanation-only question.

## Workflow

1. **Lock the goal.** Preserve objective, exact effect/deliverable, acceptance criteria, authority ceiling, target identity, critical unknowns, evidence plan, and stop conditions.
2. **Resolve identity.** Determine exact owner/repository, default branch, target ref/path/PR/workflow, current revision, and observed permissions. Once identity is known, prefer exact lookup over ranked search.
3. **Build the read plan.** Read the smallest authoritative set that can resolve the decision. Broad search/tree results locate candidates; exact object fetches establish material facts.
4. **Classify evidence.** Keep `OBSERVED`, `DERIVED`, `HYPOTHESIS`, and `UNKNOWN` distinct. Do not mutate on a decision-critical hypothesis when a discriminating test is practical.
5. **Resolve the live tool schema.** Narrowly discover the exact GitHub action when its schema is not already current. Validate required fields, enums, IDs, SHA/ref semantics, and write behavior. Never invent parameters from memory.
6. **Run invocation preflight.** Confirm the action advances the current subgoal, identifiers are current, effect class is understood, rollback exists for material writes, and the expected postcondition is explicit.
7. **Invoke and classify.** Separate transport success from task success. Preserve target, mechanism, status/error, evidence delta, and legal next actions before chaining another material call.
8. **Mutate safely.** Pre-read, record base and blob SHA, prefer a branch for non-trivial work, serialize dependent same-path writes, and keep rollback available.
9. **Read back.** Independently fetch the exact target branch/object and compare intended versus observed content/state. A commit SHA or PR URL alone is never completion proof.
10. **Observe execution.** If the user asked to run/test/install/activate, distinguish repository state, workflow request, workflow result, installation, invocation, and observable effect. Verify at the highest claimed layer.
11. **Recover by failure class.** Search miss -> exact lookup; truncation -> targeted refetch; schema mismatch -> rediscover schema; stale SHA -> re-read/reconcile; partial success -> continue from observed remote state; permission failure -> verify actual authority; repeated no-delta failure -> change causal mechanism.
12. **Verify and close.** Test acceptance criteria, applicable invariants, exact revision, at least one causally relevant fallback/failure path when practical, and adjacent regression. Only then return PASS.

## Per-call operation envelope

For material calls maintain enough state to answer:

- What exact subgoal is this call advancing?
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

After each failed/inconclusive attempt compare the evidence fingerprint. If two same-mechanism attempts produce no material change in target identity, revision/version, live schema/permission, failure class, discriminating evidence, observable state, or legal next action, switch mechanisms.

## Completion statuses

- `PASS`: requested effect is verified on the exact target/revision and applicable invariants/regressions pass.
- `FAIL`: a required behavior or invariant failed and remains unsatisfied.
- `BLOCKED`: a concrete missing permission/capability/external dependency prevents the next valid transition.
- `NOT_RUN`: required execution or verification has not occurred.

Never promote partial success, a green unrelated workflow, repository configuration, plugin installation, or connector transport success to a higher layer.

## Composition

Typical rich bundle: `task-goal-intelligence` -> `github-operation-orchestrator` -> `evidence-watchdog`.

Escalate narrowly when the blocker is specialized:

- live tool namespace/schema/context pressure -> `mcp-surface-engineering`;
- apparent success with missing runtime effect -> `agent-runtime-forensics`;
- capability/permission/session/surface uncertainty -> `capability-forensics`;
- current external/maintainer evidence required -> `executive-research`.

Keep implicit composition bounded; do not load specialists merely because their nouns appear.

## Boundary

Do not broaden repository/app permissions, bypass authorization, force-push over divergence, or mutate an ambiguous target just to keep the loop moving. A verified BLOCKED state is better than fabricated completion.