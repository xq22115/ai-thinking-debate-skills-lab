# Ordinary ChatGPT host activation probe

Purpose: prove that the repository package has crossed the product boundary into the **actual ChatGPT host** before any local skill is credited with changing ordinary ChatGPT behavior.

## Why this probe exists

Repository/package evidence and ChatGPT activation are different systems:

`GIT REPO -> MARKETPLACE CATALOG -> CHATGPT MARKETPLACE IMPORT/SYNC -> PLUGIN INSTALL/ASSIGN -> APP DEPENDENCY -> CURRENT SURFACE LOAD -> BEHAVIORAL EFFECT`

A green CI run, a merge to `main`, `.agents/plugins/marketplace.json`, `.codex-plugin/plugin.json`, or `.app.json` proves only a lower layer. None of them independently proves that ordinary ChatGPT loaded this plugin revision.

The public `openai/plugins` repository documents Codex plugin examples. It may provide manifest/provenance examples, but it is not evidence that this repository's plugin is deployed to ordinary ChatGPT.

## Canonical repository import target

Repository:

`https://github.com/xq22115/ai-thinking-debate-skills-lab`

Marketplace file:

`.agents/plugins/marketplace.json`

The marketplace is at repository root, so a GitHub marketplace import should use the repository URL itself and no subdirectory path unless the host UI requires one for a future layout change.

Expected marketplace entry:

- plugin name: `ai-efficiency-operating-system`;
- source: `local`;
- source path: `./plugins/ai-efficiency-operating-system`;
- installation policy: `AVAILABLE`;
- authentication: `ON_INSTALL`.

Expected package version must be read from the current imported revision's `.codex-plugin/plugin.json`; do not hard-code a stale version in host validation.

## Host activation sequence

On an eligible ChatGPT workspace/account surface:

1. Open the host's Plugins/workspace plugin administration surface.
2. Import the GitHub marketplace using the repository URL above. This is a **host/admin operation**, not a Git push.
3. Confirm the marketplace import resolves `ai-efficiency-operating-system` from the expected local source path.
4. Confirm the plugin becomes available/assigned for the intended user or role.
5. Install/enable the plugin on the owning ChatGPT surface when the host exposes that action.
6. Resolve its required `github` app dependency and confirm the canonical GitHub app is available/connected for the intended account.
7. After repository changes, use the host's marketplace **Sync now/Refresh** capability when available, or wait for the host's documented sync process; repository push alone is not sync evidence.
8. Confirm the host-visible plugin revision/version corresponds to the intended repository revision when the surface exposes revision metadata.
9. Run a behavioral probe in ordinary ChatGPT that requires a marker unique to the imported revision, not merely the already-installed canonical GitHub connector.
10. Only after that behavioral probe succeeds may the local plugin be marked `HOST_LIVE` for the tested surface/revision.

If the current account/workspace does not expose GitHub marketplace import, installation, assignment, or the required app connection, classify the missing step as `HOST_IMPORT_BLOCKED` or `CUSTOM_PLUGIN_ACTIVATION_UNVERIFIED`. Do not edit repository prompts to simulate product activation.

## Required evidence packet

A host-live activation claim should record:

- tested ChatGPT surface (Web/Desktop and relevant workspace/profile);
- marketplace identity/source repository;
- import/sync receipt or current host marketplace state;
- plugin name and host-visible install/enable/assignment state;
- exact expected repository commit and package version;
- GitHub app dependency availability/connection state;
- current tool/plugin visibility on the tested surface;
- a behavioral probe unique to the intended local plugin revision;
- final status: `PASS`, `FAIL`, `BLOCKED`, or `NOT_RUN`.

## Negative controls

These must **not** be accepted as host activation proof by themselves:

- GitHub commit/merge success;
- repository CI success;
- marketplace JSON exists;
- package manifest exists;
- canonical `github@openai-curated` is installed;
- GitHub connector is callable;
- GitHub action permission is `Allow all actions`;
- Codex can load the package;
- a previous assistant message says the plugin is live.

The canonical GitHub connector and this local orchestration plugin are separate activation dimensions.

## Terminal truth

Use `CHATGPT_LOCAL_PLUGIN_HOST_LIVE` only when the current ChatGPT surface has independently proven import/install/enablement and behavior for the exact intended revision.

Otherwise retain `CUSTOM_PLUGIN_ACTIVATION_UNVERIFIED` even when every repository and CI check is green.
