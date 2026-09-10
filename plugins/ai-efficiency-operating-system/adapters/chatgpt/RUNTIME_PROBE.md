# ChatGPT Web/Desktop live probe

Purpose: prove the exact imported plugin revision is actually discoverable, the bound GitHub app is available when GitHub work is requested, routing uses the selected specialist deeply, failed retrieval routes recover correctly, and postconditions are verified on the owning ChatGPT surface. Repository/package validation is insufficient.

## Install/import boundary

The repository provides `.agents/plugins/marketplace.json` for supported workspace/plugin import flows. The plugin manifest is `plugins/ai-efficiency-operating-system/.codex-plugin/plugin.json`; its `version` field is the single package-version source of truth. Do not duplicate a fixed expected package version in this probe.

The plugin includes `.app.json` with the `github` app binding used for repository/PR/issue/Actions work. Importing or syncing the repository does not itself prove that the owning workspace has connected or authorized that app. Actual availability depends on workspace permissions, plan, surface and import/install state. Do not convert a GitHub commit into a `HOST_LIVE` claim.

The plugin does not manufacture local filesystem, process/network telemetry, terminal, browser-control, binary-analysis or other host capabilities. Those must be supplied and authorized by the owning host/runtime.

## Probe order

1. Import/sync the repository marketplace through the actual supported workspace/admin plugin control for the target account.
2. Confirm `AI Efficiency Operating System` is listed and installable/installed on the owning surface.
3. Read the expected plugin name/version from `.codex-plugin/plugin.json` at the exact imported/synced repository revision. Confirm the owning surface reports the same version when exposed; never compare against a hand-written stale version constant.
4. For GitHub-backed work, verify the plugin exposes or can use the bound `GitHub` app, then distinguish these states: `APP_DECLARED → APP_AVAILABLE → APP_CONNECTED → TOOL_NAMESPACE_VISIBLE → TOOL_INVOKABLE → EFFECT_VERIFIED`.
5. Run a real GitHub **pull/read path** from ordinary ChatGPT:
   - resolve a known repository by exact identity;
   - fetch a known file from an exact ref;
   - if ranked/code search misses, pivot to a causally distinct exact lookup/direct fetch/tree-or-contents route before concluding absence;
   - if a response is empty/truncated, targeted-refetch the exact object instead of inferring missing state.
6. Run a real GitHub **write/read-back path** only on a safe test branch/repository when write verification is required:
   - record rollback/base revision;
   - read target file and current blob SHA;
   - write sequentially;
   - read the same target branch back and compare intended content;
   - deliberately exercise one stale-SHA or equivalent detectable failure on the safe test path and verify it does not corrupt the accepted state;
   - restore/delete the probe state and read back the rollback result.
7. Run base positive/negative routing:
   - material target ambiguity → `task-goal-intelligence` behavior;
   - plan comparison → `plan-arbiter` behavior;
   - completion claim → `evidence-watchdog` postcondition behavior;
   - current technical research → `executive-research` behavior;
   - simple arithmetic/translation and explanation-only specialist nouns → no heavy specialist ceremony.
8. **Without explicit skill names**, run conditional specialist probes:
   - same model/product behaves differently by session/account/surface → `capability-forensics` behavior;
   - many/changing MCP tools or schema/context pressure → `mcp-surface-engineering` behavior;
   - tool/process claims success but real state is missing → `agent-runtime-forensics` behavior.
9. Verify deep-use markers rather than mere name-dropping:
   - capability probe distinguishes declared/visible/authorized/loadable/invokable/effective/verified states and chooses a differential probe;
   - MCP probe inspects live namespace/schema/version/entitlement/session and proposes narrow/lazy discovery when relevant;
   - runtime probe correlates intent/tool/process/file/network/artifact/postcondition evidence and reports missing planes rather than inventing them.
10. Verify bounded composition: no more than three implicit skills in one phase; goal gate + primary owner + verifier is the default rich shape.
11. Verify fallback/self-repair: simulate or encounter one unavailable/failed specialist or GitHub retrieval route, preserve the Goal Contract, retry the same mechanism at most once without new evidence, then select a materially different goal-advancing route.
12. Verify explicit-only boundaries:
   - `autonomy-contract` does not appear implicitly;
   - `persistent-work-ledger` does not pretend ordinary Chat has durable primitives;
   - `authorized-reverse-engineering` remains intentionally explicit and authorization-scoped.
13. Test a real state claim with owning-runtime/read-back proof.

## GitHub response classification

A successful tool/transport response proves only that one invocation returned. It does not prove the requested pull, installation, write or runtime activation succeeded.

Classify failures before retrying:

- plugin manifest/import problem;
- GitHub app binding/connection problem;
- tool namespace/schema problem;
- target identity or permission problem;
- discovery false negative;
- stale version/ref/blob problem;
- truncated/empty response;
- partial success followed by failure;
- owning-host state not read back.

Preserve the exact target, mechanism, error/status and evidence delta. After two materially similar failures, change mechanism rather than wording.

## Acceptance states

`CHATGPT_DESKTOP_HOST_LIVE` requires observed plugin availability plus successful behavior probes on the actual Desktop surface for the exact imported/synced plugin revision.

`CHATGPT_GITHUB_BRIDGE_VERIFIED` additionally requires:

- the plugin manifest references `./.app.json`;
- `.app.json` resolves the `github` app binding expected by the current package;
- the GitHub app is available/connected on the owning surface;
- a real ordinary-ChatGPT GitHub read/pull path succeeds;
- one causally relevant failure/fallback path is observed;
- material write claims, when tested, finish with owning GitHub read-back.

`CHATGPT_ROUTING_VERIFIED` additionally requires:

- goal-gate routing;
- positive base routing;
- conditional specialist implicit activation;
- simple/explanation hard negatives;
- bounded composition;
- no explicit-only leakage.

`CHATGPT_DEEP_USE_VERIFIED` additionally requires mechanism-specific specialist behavior, not just a mention of the selected skill.

`CHATGPT_FALLBACK_VERIFIED` additionally requires an observed failed/unavailable route to preserve the root goal and move to a materially different valid fallback.

If the UI/workspace does not expose import/install for this repository, report `HOST_IMPORT_BLOCKED`; do not rewrite the skill package to pretend product capability exists.

## Explicit 10-agent unanimity mode

When the user explicitly requires ten independent agents and 10/10 unanimous approval across both ChatGPT Web and ChatGPT Desktop, use `HOST_LIVE_10WAY.md` together with `control-plane/ai-system/configs/ten-way-unanimity-mode.json`.

That strict profile is not the default. It additionally requires independently attributable receipts, any requested concurrency proof, 10/10 required-lane PASS, current owning-surface evidence, and the same exact observed plugin revision on both tested surfaces.
