# ChatGPT Web/Desktop live probe

Purpose: prove the exact imported plugin revision is actually discoverable, the bound GitHub app is available when GitHub work is requested, the GitHub operation loop performs real read/analyze/schema/invoke/write/execute/verify transitions, routing uses the selected specialist deeply, failed routes recover correctly, and postconditions are verified on the owning ChatGPT surface. Repository/package validation is insufficient.

## Install/import boundary

The repository provides `.agents/plugins/marketplace.json` for supported workspace/plugin import flows. The plugin manifest is `plugins/ai-efficiency-operating-system/.codex-plugin/plugin.json`; its `version` field is the single package-version source of truth. Do not duplicate a fixed expected package version in this probe.

The plugin includes `.app.json` with the `github` app binding used for repository/PR/issue/Actions work. Importing or syncing the repository does not itself prove that the owning workspace has connected or authorized that app. Actual availability depends on workspace permissions, plan, surface and import/install state. Do not convert a GitHub commit into a `HOST_LIVE` claim.

Repository marketplace `policy` values are catalog metadata, not proof of the workspace's effective installation/authentication policy. After import/sync, read the effective workspace Installation policy separately, verify each required app is enabled and accessible for the intended member role, and verify member/provider authentication when the live app requires it. Import/sync does not connect member accounts or grant required-app access.

The plugin does not manufacture local filesystem, process/network telemetry, terminal, browser-control, binary-analysis or other host capabilities. Those must be supplied and authorized by the owning host/runtime.

For ordinary ChatGPT GitHub work, read `github-upstream-capability-contract.json`, `HOST_ACTIVATION_PROBE.md`, `github-pull-runtime.json`, and `GITHUB_OPERATION_LOOP.md`. Machine profiles are authoritative for fail-closed validation; Markdown files are human-readable operational projections.

## Probe order

1. Import/sync the repository marketplace through the actual supported workspace/admin plugin control for the target account.
2. Confirm `AI Efficiency Operating System` is listed for the owning workspace/surface.
3. Read the effective workspace Installation policy; do not infer it from repository marketplace `AVAILABLE / ON_INSTALL` metadata.
4. Confirm the plugin is available/installed/assigned for the intended user or role according to workspace policy.
5. For each required app, confirm it is enabled and accessible for the intended role; complete member/provider authentication only if required by that app.
6. Read the expected plugin name/version from `.codex-plugin/plugin.json` at the exact imported/synced repository revision. Confirm the owning surface reports the same version when exposed; never compare against a hand-written stale version constant.
7. For GitHub-backed work, verify the plugin exposes or can use the bound `GitHub` app, then distinguish these states: `APP_DECLARED → APP_AVAILABLE → APP_ROLE_ACCESSIBLE → APP_AUTHENTICATED_IF_REQUIRED → TOOL_NAMESPACE_VISIBLE → TOOL_SCHEMA_READY → TOOL_INVOKABLE → EFFECT_VERIFIED`.
8. Verify the operation profile reports schema v2 and contains the state path `GOAL_LOCKED → TARGET_RESOLVED → AUTHORITY_RESOLVED → READ_PLAN_READY → SOURCE_READ → EVIDENCE_SUFFICIENT → TOOL_SCHEMA_READY → INVOCATION_PREFLIGHT → INVOKED → RESPONSE_CLASSIFIED`, plus the applicable mutation/execution/verification states.
9. Run a real GitHub **pull/read path** from ordinary ChatGPT:
   - lock the requested target and acceptance criterion;
   - resolve a known repository by exact identity;
   - record default branch, current head and effective permissions when exposed;
   - fetch a known file from an exact ref and preserve its blob SHA;
   - distinguish observed facts from derived conclusions and unresolved hypotheses;
   - if ranked/code search misses, pivot to a causally distinct exact lookup/direct fetch/tree-or-contents route before concluding absence;
   - if a response is empty/truncated, targeted-refetch the exact object instead of inferring missing state.
10. Run a real **live-schema invocation preflight**:
   - narrow-discover the relevant GitHub action when its schema is not already current in context;
   - verify required arguments, enums, identifier semantics and write behavior from the live tool description;
   - reject an invented/unknown argument rather than guessing;
   - after a simulated or observed schema mismatch, rediscover the action before retrying;
   - record the expected postcondition before an effectful call.
11. Run a real GitHub **write/read-back path** only on a safe test branch/repository when write verification is required:
   - record rollback/base revision;
   - read target file and current blob SHA;
   - create/use an isolated test branch for non-trivial probes;
   - write sequentially;
   - classify the connector response before chaining another material action;
   - read the same target branch back and compare intended content;
   - deliberately exercise one stale-SHA or equivalent detectable failure on the safe test path and verify it does not corrupt the accepted state;
   - restore/delete the probe state and read back the rollback result.
12. Run a real GitHub **execution path** when execution is part of the acceptance contract:
   - distinguish workflow dispatch/request acceptance from workflow execution success;
   - bind the observed workflow run to the exact commit/ref under test;
   - inspect its conclusion and any relevant evidence exposed by the GitHub surface;
   - verify the user-level postcondition separately when it is higher than CI status;
   - if owning-runtime behavior cannot be observed, report `BLOCKED` or `NOT_RUN`, not PASS.
13. Run a **partial/ambiguous response** probe:
   - simulate or encounter partial success, truncation, ambiguous status, or remote failure;
   - preserve exact target/action/status and evidence delta;
   - read current remote state before deciding the next material action;
   - prove the workflow does not blindly chain a mutation from an ambiguous result.
14. Run a **no-progress** probe:
   - cause two same-mechanism attempts to produce no material evidence delta;
   - verify the next attempt changes causal mechanism rather than wording;
   - ensure target identity, acceptance criteria and authority ceiling remain unchanged.
15. Run base positive/negative routing:
   - multi-step GitHub read/search/analyze/call/write/workflow/verify task → `github-operation-orchestrator` behavior after host activation truth is satisfied;
   - explanation-only `GitHub 是什麼` → no GitHub specialist ceremony;
   - material target ambiguity → `task-goal-intelligence` behavior;
   - plan comparison → `plan-arbiter` behavior;
   - completion claim → `evidence-watchdog` postcondition behavior;
   - current technical research → `executive-research` behavior;
   - simple arithmetic/translation and explanation-only specialist nouns → no heavy specialist ceremony.
16. **Without explicit skill names**, run conditional specialist probes:
   - same model/product behaves differently by session/account/surface → `capability-forensics` behavior;
   - many/changing MCP tools or schema/context pressure → `mcp-surface-engineering` behavior;
   - tool/process claims success but real state is missing → `agent-runtime-forensics` behavior.
17. Verify deep-use markers rather than mere name-dropping:
   - GitHub probe maintains host activation, workspace policy, app access/auth, target/revision/schema/result/evidence-delta/legal-next-action state and uses a failure-class-specific recovery route;
   - capability probe distinguishes declared/visible/authorized/loadable/invokable/effective/verified states and chooses a differential probe;
   - MCP probe inspects live namespace/schema/version/entitlement/session and proposes narrow/lazy discovery when relevant;
   - runtime probe correlates intent/tool/process/file/network/artifact/postcondition evidence and reports missing planes rather than inventing them.
18. Verify bounded composition: no more than three implicit skills in one phase; for material GitHub operations after host activation the default rich shape is `task-goal-intelligence + github-operation-orchestrator + evidence-watchdog`.
19. Verify fallback/self-repair: simulate or encounter one unavailable/failed specialist or GitHub retrieval route, preserve the Goal Contract, retry the same mechanism at most once without new evidence, then select a materially different goal-advancing route.
20. Verify explicit-only boundaries:
   - `autonomy-contract` does not appear implicitly;
   - `persistent-work-ledger` does not pretend ordinary Chat has durable primitives;
   - `authorized-reverse-engineering` remains intentionally explicit and authorization-scoped.
21. Test a real state claim with owning-runtime/read-back proof.

## GitHub response classification

A successful tool/transport response proves only that one invocation returned. It does not prove the requested pull, installation, write, workflow, execution or runtime activation succeeded.

Classify before retrying or chaining:

- `SUCCESS_WITH_EVIDENCE`;
- `PARTIAL_SUCCESS`;
- `EMPTY_OR_TRUNCATED`;
- `SCHEMA_MISMATCH`;
- `TARGET_NOT_RESOLVED`;
- `PERMISSION_BLOCKED`;
- `STALE_REVISION_OR_BLOB`;
- `DISCOVERY_FALSE_NEGATIVE`;
- `REMOTE_OR_RUNTIME_FAILURE`;
- `AMBIGUOUS_RESULT`.

Preserve the exact target, mechanism, error/status, evidence delta and legal next actions. After two materially similar failures without evidence delta, change mechanism rather than wording.

## Operation evidence packet

For a material probe retain enough evidence to reconstruct:

- goal and acceptance criterion;
- ChatGPT marketplace/import state and effective workspace policy;
- required-app/member access and authentication when applicable;
- owner/repository/ref/path/PR/workflow identity;
- base/head/blob/version dimensions;
- observed authority;
- live tool/action schema source;
- preconditions and exact arguments;
- response/result class;
- evidence delta;
- post-write read-back;
- execution/run identity when applicable;
- acceptance and regression result;
- rollback/cleanup proof.

This is an audit record, not a request to expose private chain-of-thought.

## Acceptance states

`CHATGPT_DESKTOP_HOST_LIVE` requires observed plugin availability, effective workspace policy, required-app/member access/authentication when applicable, plus successful behavior probes on the actual Desktop surface for the exact imported/synced plugin revision.

`CHATGPT_GITHUB_BRIDGE_VERIFIED` additionally requires:

- the plugin manifest references `./.app.json`;
- `.app.json` resolves the `github` app binding expected by the current package;
- the GitHub app is available/role-accessible and authenticated when required on the owning surface;
- `github-pull-runtime.json` schema v2 and `GITHUB_OPERATION_LOOP.md` agree on the core operation states;
- a real ordinary-ChatGPT GitHub read/pull path succeeds;
- live action/schema preflight is observed for a material call;
- one causally relevant failure/fallback path is observed;
- material write claims, when tested, finish with owning GitHub read-back;
- requested execution claims, when tested, bind exact execution evidence to the exact revision;
- no required state is silently skipped or promoted from `NOT_RUN/BLOCKED` to PASS.

`CHATGPT_ROUTING_VERIFIED` additionally requires:

- goal-gate routing;
- GitHub orchestrator positive and explanation-only negative routing;
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
