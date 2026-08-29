# Capability Boundary Recon — ChatGPT / Codex / Desktop

Use after `capability-forensics` when the missing capability could be caused by product, workspace, plugin/app, role, session or surface boundaries rather than the model itself.

This is a **diagnostic** playbook. It reconstructs the effective capability chain; it does not bypass product, workspace, provider or authorization controls.

## 1. Boundary chain

For a desired capability, inspect the layers separately:

`PLAN/ROLLOUT → WORKSPACE POLICY → ROLE → PLUGIN AVAILABILITY → PLUGIN INSTALL → REQUIRED APP → APP ENABLEMENT → PROVIDER AUTH → ACTION CONTROLS → SURFACE SUPPORT → SESSION REGISTRATION → TOOL VISIBILITY → INVOCATION → POSTCONDITION`

A failure at any earlier layer can present to the user as “the AI cannot do it”.

## 2. Plugin vs app vs skill

Keep these concepts separate:

- **plugin** — packaged workflow capability/distribution unit;
- **skill** — reusable workflow instructions/process knowledge;
- **app** — connection to external data/actions with its own permissions/auth;
- **MCP/local runtime** — host-specific tool/server surface when present.

Installing or syncing a plugin does not automatically authorize an app. A skill-only plugin can be available without external app access. A plugin’s skills cannot create missing filesystem, terminal, browser-control or local MCP capability.

## 3. Current OpenAI surface checks

For current ChatGPT/Codex plugin investigations, verify rather than assume:

- plan and rollout for the target account;
- workspace `Use plugins` / skill permissions;
- role assignment;
- plugin installation policy;
- required app availability;
- app/provider connection and the intended account identity;
- read/write/action controls;
- supported surface (web / desktop / Codex / Work);
- region restrictions;
- current app/desktop build when material;
- whether the host requires refresh/restart/new task after catalog or capability changes.

GitHub marketplace sync proves content distribution only. It does **not** grant provider-account authorization or app permissions.

## 4. Desktop-only classification

Do not assume every imported plugin works identically on web and desktop.

When a plugin declares local/MCP server configuration, the host may classify it as Desktop-only. Therefore distinguish:

- skill-only portable plugin;
- plugin referencing supported remote apps;
- plugin declaring local/MCP runtime;
- desktop application that independently owns/registers an MCP server.

Do not add an MCP declaration merely to make a skill look more capable if doing so unnecessarily removes web portability.

## 5. Multi-account / multi-profile differential

When the same feature differs between accounts or devices, build a matrix rather than copying configuration blindly:

| Layer | Account/device A | Account/device B |
|---|---|---|
| plan/workspace | | |
| role/policy | | |
| plugin version/install | | |
| required app | | |
| provider identity | | |
| action controls | | |
| host build/surface | | |
| session/tool list | | |
| minimal invocation | | |
| postcondition | | |

Change one dimension at a time where practical. “Same ChatGPT login” does not prove identical workspace role, app connection, surface registration or local runtime.

## 6. Session registration / stale catalog probe

A plugin/tool can be correctly installed yet absent from the current task/session.

Probe in this order:

1. confirm current plugin/app state from the owning product UI/runtime;
2. enumerate the current task’s actual tools/skills if the host exposes them;
3. compare with a fresh supported task/session when catalog refresh may be session-bound;
4. restart/refresh the product only when current product guidance says that is relevant;
5. invoke a minimal safe tool action;
6. read back the actual target state.

Do not repeatedly reinstall a working plugin to solve a stale session unless installation itself is proven wrong.

## 7. Effective permission truth

Separate:

- workspace can install plugin;
- user can see/use plugin;
- underlying app is enabled;
- provider account is connected;
- app can read the needed source;
- app can perform the needed write/action;
- action requires approval;
- actual call is authorized for the selected account/resource.

“Full plugin access” is not a universal override over provider permissions, workspace policy or unsupported actions.

## 8. Capability differential experiments

High-information comparisons:

- same model + same prompt, plugin disabled vs installed;
- same model, web vs desktop;
- same plugin, current session vs fresh session;
- same plugin, account/profile A vs B;
- same tool, old cached schema vs live schema;
- same app, read-only action vs supported write action;
- configured state vs minimal real invocation vs postcondition read-back.

Record all uncontrolled differences before attributing the result to the model.

## 9. Classification

Prefer one of:

- `PLAN_OR_ROLLOUT`
- `WORKSPACE_OR_ROLE_POLICY`
- `PLUGIN_NOT_AVAILABLE`
- `PLUGIN_NOT_INSTALLED_OR_STALE`
- `APP_NOT_ENABLED`
- `PROVIDER_AUTH_OR_ACCOUNT`
- `ACTION_CONTROL_OR_PERMISSION`
- `SURFACE_NOT_SUPPORTED`
- `DESKTOP_LOCAL_RUNTIME_MISSING`
- `SESSION_REGISTRATION_STALE`
- `TOOL_SCHEMA_OR_VERSION`
- `INVOCATION_FAILURE`
- `POSTCONDITION_FAILURE`
- `MODEL_OR_REASONING_LIMIT`
- `UNKNOWN`

Only use `MODEL_OR_REASONING_LIMIT` after relevant external/harness/capability layers have been ruled out with evidence.

## 10. Repair order

Prefer fixing the earliest causal layer:

1. correct target/account/profile/workspace;
2. correct plugin/app availability and role policy;
3. correct provider authentication/account selection;
4. correct action permissions/controls;
5. correct host/surface/version/session registration;
6. correct tool schema/runtime integration;
7. correct invocation/effect implementation;
8. only then tune prompting/model/harness if the capability exists but reasoning remains the bottleneck.

## 11. Proof standard

A capability is not “unlocked” at `configured` or `installed`.

For a stateful capability, prefer:

`VISIBLE → AUTHORIZED → INVOKABLE → EFFECT_OBSERVED → POSTCONDITION_VERIFIED`

If the owning product/runtime cannot be inspected, report the result as a static diagnosis and list the live probes still required.
