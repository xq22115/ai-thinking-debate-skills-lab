# GitHub root control plane for ordinary ChatGPT

This document identifies the first real owner of each GitHub capability **and the activation boundary that decides whether a local skill package can affect ordinary ChatGPT at all**.

## Root finding

There are two independent questions that must never be collapsed:

1. **Which GitHub actions does ordinary ChatGPT actually expose?**
2. **Has this local AI Efficiency package actually been imported/installed/enabled on the current ChatGPT surface?**

The local repository does not implement the hosted GitHub action server. Its `.app.json` binds `github` to the existing hosted connector `connector_76869538009648d5b282a4bb21c3d157`.

The official public `openai/plugins` repository is explicitly a curated collection of Codex plugin examples. Its `plugins/github` manifests are useful provenance for the canonical GitHub plugin/connector relationship and for the separate MCP surface, but a commit to that repository or to this repository is **not** the ordinary-ChatGPT plugin deployment mechanism.

For ordinary ChatGPT, the controlling chain is:

`ChatGPT plugin installation / workspace marketplace import / current surface -> hosted GitHub connector namespace/schema -> GitHub remote state/permissions -> local orchestrator policy only if that local plugin is actually host-loaded`

Repair the first layer that actually owns the failed behavior. Do not repair a downstream prompt when the missing capability belongs to host activation or the connector.

## Activation truth — the missing root that previously caused false completion

`REPOSITORY PACKAGE != CHATGPT INSTALLED PLUGIN != CONNECTED APP != LIVE CONNECTOR ACTION != VERIFIED EFFECT`

A `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, green repository CI, or a merge to `main` proves repository/package state only.

To make a repository-hosted plugin affect ordinary ChatGPT, current OpenAI product behavior requires a **host-side activation path**, such as:

- installation from the Plugin Directory when the plugin is published and available to the account/workspace;
- an eligible workspace administrator importing the GitHub marketplace and assigning/allowing the plugin, followed by marketplace sync;
- a supported custom app/plugin rollout for the workspace.

A Git push is not a marketplace sync. A marketplace JSON file sitting in a repository is not evidence that ChatGPT imported it. After an imported marketplace changes, the host may need automatic daily sync or an explicit **Sync now/Refresh** operation before the current plugin release changes.

The current public/global lookup for `ai-efficiency-operating-system` does not resolve a public release. That does **not** prove a workspace-specific import is absent, but it blocks any claim that the local package is globally installed merely because the repository exists.

Until current host evidence proves import/install/enablement and a behavioral probe exercises the loaded revision, use:

`CUSTOM_PLUGIN_ACTIVATION_UNVERIFIED`

Do not claim ordinary ChatGPT is using this local skill package.

## What each layer controls

### ChatGPT host / workspace

Controls:

- plugin installation and enablement;
- workspace GitHub marketplace import and sync;
- whether local/custom skills are exposed on the current surface;
- connected-app availability;
- the user's action-approval policy;
- session/tool namespace visibility.

An **Allow all actions** setting only changes approval behavior for actions that already exist. It does not create connector actions, expand GitHub App scopes, import a local marketplace, or install this repository's skill package.

### Hosted OpenAI GitHub connector

Controls the live action inventory, each action schema, endpoint allowlist, response shape, connector-side search behavior, and the set of writes/Actions operations exposed to ordinary ChatGPT.

The live schema outranks remembered tool syntax, local docs, and Codex/MCP manifests.

### GitHub remote

Controls repository contents, refs, commits, PRs, issues, Actions state, and repository permissions enforced by GitHub.

### Local AI Efficiency plugin — only if host-loaded

May improve goal interpretation, search strategy, query fanout, live tool discovery, action selection, argument construction, fallback, read-back, verification, and completion logic **only after ordinary ChatGPT has actually loaded the plugin**.

It cannot add a hosted connector action, grant GitHub App/OAuth permissions, bypass an endpoint allowlist, turn the connector into arbitrary shell execution, or install itself into ChatGPT by committing files to GitHub.

## Root failure taxonomy

Use the first matching owner:

- `CUSTOM_PLUGIN_ACTIVATION_UNVERIFIED` — local package/repo exists, but current ordinary-ChatGPT import/install/enablement and loaded revision are not proven.
- `UPSTREAM_CAPABILITY_GAP` — the required action is absent after narrow live-tool discovery.
- `HOST_PERMISSION_POLICY` — the action exists but host/plugin approval or enablement blocks it.
- `GITHUB_REMOTE_PERMISSION` — the action exists but GitHub rejects repository authority.
- `CALLER_SEARCH_UNDERFETCH` — the caller used a shallow/default search plan, failed to preserve an explicit result-count target, or stopped before query fanout.
- `CALLER_SCHEMA_STALE` — the caller used remembered/stale parameters instead of the live action schema.
- `CALLER_RESPONSE_TRUNCATION` — a truncated tool response was treated as complete.
- `CALLER_CHAIN_BREAK` — a lower-layer success was promoted to completion without read-back/postcondition evidence.

Only caller/orchestrator failures are repairable by local skill code. Host activation, hosted connector capability, and GitHub provider permission failures must be fixed at their owning layer and must not be disguised as prompt failures.

## Search-depth repair

The symptom "GitHub search only returns one to three results" is not a valid conclusion from one call. The live search surface has been observed accepting a larger `topn`, while large responses can be truncated by transport/context limits. Therefore shallow caller strategy and truncation handling are separate from connector result capacity.

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

1. prove the required plugin/app/tool surface is current for this session;
2. discover the relevant live action if its schema is not already current;
3. verify required fields/enums/identifier semantics;
4. construct arguments only from current evidence;
5. classify read-only/idempotent/effectful behavior;
6. define the observable postcondition and rollback/recovery path;
7. invoke;
8. classify the response before chaining another material action.

If the live namespace does not contain the needed action, stop trying alternate parameter spellings and classify `UPSTREAM_CAPABILITY_GAP`.

## Execution repair

The ordinary-ChatGPT GitHub connector must not be treated as arbitrary code execution.

If a direct workflow-dispatch action is not present on the live surface, repository-controlled execution should use observable automatic triggers such as `pull_request` or isolated-branch `push` workflows where appropriate. Existing-workflow rerun is a different capability and must not be mislabeled as dispatch.

Every CI claim must bind the run to the exact commit. A green run proves only the checks declared by that workflow, not hosted ChatGPT activation.

## Completion

A root fix is complete only when:

- the first owning layer is identified;
- **ordinary-ChatGPT activation of any claimed local plugin is proven independently of repository state**;
- the failure is classified at its real layer;
- any local repair changes the local cause rather than masking an upstream gap;
- explicit search breadth is measured by unique results;
- material writes are independently read back;
- execution is observed at the claimed layer;
- no repository/package/connector success is promoted to a higher layer without evidence.

Machine-readable companion: `github-upstream-capability-contract.json`.
