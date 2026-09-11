# Ordinary ChatGPT host activation probe

Purpose: prove that the repository package has crossed the product boundary into the **actual ChatGPT host** before any local skill is credited with changing ordinary ChatGPT behavior.

## Why this probe exists

Repository/package evidence and ChatGPT activation are different systems:

`GIT REPO -> MARKETPLACE CATALOG -> CHATGPT MARKETPLACE IMPORT/SYNC -> WORKSPACE EFFECTIVE POLICY -> PLUGIN INSTALL/ASSIGN -> REQUIRED APP ACCESS/AUTH -> CURRENT SURFACE LOAD -> BEHAVIORAL EFFECT`

A green CI run, a merge to `main`, `.agents/plugins/marketplace.json`, `.codex-plugin/plugin.json`, or `.app.json` proves only a lower layer. None of them independently proves that ordinary ChatGPT loaded this plugin revision.

The public `openai/plugins` repository documents Codex plugin examples. It may provide manifest/provenance examples, but it is not evidence that this repository's plugin is deployed to ordinary ChatGPT.

## Canonical repository import target

Repository:

`https://github.com/xq22115/ai-thinking-debate-skills-lab`

Marketplace file:

`.agents/plugins/marketplace.json`

The marketplace is at repository root, so a GitHub marketplace import should use the repository URL itself and leave Path empty unless the repository layout changes.

Expected repository marketplace entry:

- plugin name: `ai-efficiency-operating-system`;
- source: `local`;
- source path: `./plugins/ai-efficiency-operating-system`;
- repository policy metadata currently records installation `AVAILABLE` and authentication `ON_INSTALL`.

**Repository marketplace policy is not workspace effective policy.** Current OpenAI host behavior requires workspace settings to configure the effective Installation policy and authentication/access. Import or sync does not apply repository policy values as the workspace's effective policy, does not connect members' provider accounts, and does not grant required-app access.

Expected package version must be read from the current imported revision's `.codex-plugin/plugin.json`; do not hard-code a stale version in host validation.

## Host activation sequence

On an eligible ChatGPT workspace/account surface:

1. Open the host's Plugins/workspace plugin administration surface.
2. Import the GitHub marketplace using the repository URL above. This is a **host/admin operation**, not a Git push.
3. Confirm the marketplace import resolves `ai-efficiency-operating-system` from the expected local source path.
4. Read the **effective workspace Installation policy** on the imported plugin; do not infer it from repository `policy` values.
5. Confirm the plugin is Available/Installed for the intended role according to workspace settings.
6. Confirm each required app is enabled and accessible for the intended member role.
7. Complete member/provider authentication only when required by the live app capability; import/sync does not perform this authentication.
8. After repository changes, use the host's marketplace **Sync now** capability when available, or the documented automatic sync process. Git push is not sync evidence. Refreshing only the displayed plugin list is not GitHub marketplace sync.
9. Confirm the host-visible plugin revision/version corresponds to the intended repository revision when the surface exposes revision metadata.
10. Confirm the plugin/skill is visible on the current ordinary-ChatGPT surface.
11. Run a behavioral probe that requires a marker unique to the imported revision, not merely the separately installed canonical GitHub connector.
12. Only after that behavioral probe succeeds may the local plugin be marked `HOST_LIVE` for the tested surface/revision.

If the current account/workspace does not expose GitHub marketplace import, installation/assignment controls, required-app access, or the required authentication path, classify the missing step as `HOST_IMPORT_BLOCKED` or `CUSTOM_PLUGIN_ACTIVATION_UNVERIFIED`. Do not edit repository prompts to simulate product activation.

## Required evidence packet

A host-live activation claim should record:

- tested ChatGPT surface (Web/Desktop and relevant workspace/profile);
- marketplace identity/source repository;
- import/sync receipt or current host marketplace state;
- plugin name and host-visible install/enable/assignment state;
- effective workspace Installation policy independently of repository policy metadata;
- exact expected repository commit and package version;
- required GitHub app dependency availability and role access;
- member/provider authentication state when required;
- current plugin/skill visibility on the tested surface;
- a behavioral probe unique to the intended local plugin revision;
- final status: `PASS`, `FAIL`, `BLOCKED`, or `NOT_RUN`.

## Negative controls

These must **not** be accepted as host activation proof by themselves:

- GitHub commit/merge success;
- repository CI success;
- marketplace JSON exists;
- repository marketplace `AVAILABLE` or `ON_INSTALL` metadata exists;
- package manifest exists;
- marketplace import or sync completed, without effective workspace policy and required-app/member-access checks;
- canonical `github@openai-curated` is installed;
- GitHub connector is callable;
- GitHub action permission is `Allow all actions`;
- Codex can load the package;
- a previous assistant message says the plugin is live.

The canonical GitHub connector and this local orchestration plugin are separate activation dimensions.

## Terminal truth

Use `CHATGPT_LOCAL_PLUGIN_HOST_LIVE` only when the current ChatGPT surface has independently proven marketplace import/sync or another supported installation path, effective workspace policy, required-app access/authentication when applicable, current-surface load, and behavior for the exact intended revision.

Otherwise retain `CUSTOM_PLUGIN_ACTIVATION_UNVERIFIED` even when every repository and CI check is green.
