# GitHub root control plane for ordinary ChatGPT

This document identifies the first real owner of each GitHub capability before any local repair is attempted.

## Root finding

The local AI Efficiency plugin is **not** the implementation of GitHub actions. Its `.app.json` binds the `github` alias to the existing ChatGPT GitHub connector. OpenAI's canonical `github@openai-curated` plugin resolves to the same connector. The public `openai/plugins/plugins/github` package is primarily manifests/assets plus a separate MCP configuration for compatible coding-agent hosts; it does not contain an editable implementation of the ordinary-ChatGPT connector action server.

Therefore the control chain is:

`ChatGPT host/plugin state -> canonical OpenAI GitHub plugin dependency -> live GitHub connector tool namespace/schema -> GitHub remote state -> local orchestration policy`

Repair the first layer that actually owns the failed behavior. Do not repair a downstream prompt when the missing capability belongs to the connector.

## What each layer controls

### ChatGPT host

Controls whether the GitHub plugin is installed/enabled for the user/session, whether its namespace is visible, and the user's action-approval policy.

An "Allow all actions" setting means available actions can run without another approval prompt. It does **not** create connector actions, expand GitHub App scopes, or add endpoint families.

### Canonical OpenAI GitHub plugin / connector

Controls the live action inventory, each action schema, endpoint allowlist, response shape, connector-side search behavior, and the set of writes/Actions operations exposed to ordinary ChatGPT.

The live schema outranks remembered tool syntax and local documentation.

### GitHub remote

Controls repository contents, refs, commits, PRs, issues, Actions state, and repository permissions enforced by GitHub.

### Local AI Efficiency plugin

May improve goal interpretation, search strategy, query fanout, live tool discovery, action selection, argument construction, fallback, read-back, verification, and completion logic.

It cannot add a connector action, grant GitHub App/OAuth permissions, bypass an endpoint allowlist, or turn the connector into an arbitrary shell executor.

## Root failure taxonomy

Use the first matching owner:

- `UPSTREAM_CAPABILITY_GAP` — the required action is absent after narrow live-tool discovery.
- `HOST_PERMISSION_POLICY` — the action exists but host/plugin approval or enablement blocks it.
- `GITHUB_REMOTE_PERMISSION` — the action exists but GitHub rejects repository authority.
- `CALLER_SEARCH_UNDERFETCH` — the caller used a shallow/default search plan, failed to preserve an explicit result-count target, or stopped before query fanout.
- `CALLER_SCHEMA_STALE` — the caller used remembered/stale parameters instead of the live action schema.
- `CALLER_RESPONSE_TRUNCATION` — a truncated tool response was treated as complete.
- `CALLER_CHAIN_BREAK` — a lower-layer success was promoted to completion without read-back/postcondition evidence.

Only the last four are directly repairable by this local orchestrator. The first three must be reported at their real owning layer and must not be disguised as prompt failures.

## Search-depth repair

The earlier symptom "GitHub search only returns one to three results" is not a valid conclusion from one call.

When the user gives an explicit breadth target such as 100 results/sources:

1. preserve that number as an acceptance criterion;
2. use the largest currently supported `topn` appropriate to the live schema;
3. fan out across distinct query dimensions rather than repeating wording;
4. deduplicate by canonical repository object identity;
5. treat response truncation as partial transport, not result exhaustion;
6. continue until the numeric target is met, connector exhaustion is observed, materially different queries stop adding unique results, or a hard capability/permission blocker is proven;
7. fetch exact files/issues/PRs/commits for load-bearing conclusions because search snippets remain discovery evidence.

A single search call is never evidence that only a few matching objects exist.

## Invocation repair

Before a material call:

1. discover the relevant live action if its schema is not already current;
2. verify required fields/enums/identifier semantics;
3. construct arguments only from current evidence;
4. classify read-only/idempotent/effectful behavior;
5. define the observable postcondition and rollback/recovery path;
6. invoke;
7. classify the response before chaining another material action.

If the live namespace does not contain the needed action, stop trying alternate parameter spellings and classify `UPSTREAM_CAPABILITY_GAP`.

## Execution repair

The ordinary-ChatGPT connector must not be treated as arbitrary code execution.

If a direct workflow-dispatch action is not present on the live surface, repository-controlled execution should use observable automatic triggers such as `pull_request` or isolated-branch `push` workflows where appropriate. Existing-workflow rerun is a different capability and must not be mislabeled as dispatch.

Every CI claim must bind the run to the exact commit. A green run proves only the checks declared by that workflow, not hosted ChatGPT activation.

## Completion

A root fix is complete only when:

- the first owning layer is identified;
- the failure is classified at that layer;
- any local repair changes the local cause rather than masking an upstream gap;
- explicit search breadth is measured by unique results;
- material writes are independently read back;
- execution is observed at the claimed layer;
- no lower-layer success is promoted to a higher layer without evidence.

Machine-readable companion: `github-upstream-capability-contract.json`.
