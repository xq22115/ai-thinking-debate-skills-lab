# Capability Fingerprinting & Differential Probes

Use this reference only after `capability-forensics` is explicitly selected for a material investigation.

## 1. Required-capability frontier

Start from the desired end state, not the currently visible tools. List only capabilities that are causally required, for example:

- current public information retrieval;
- repository read/write;
- local filesystem or terminal execution;
- browser DOM/computer use;
- persistent state;
- background/event-driven work;
- multi-agent runtime;
- binary/static-analysis runtime;
- runtime telemetry/provenance;
- user/account entitlement.

Do not add a capability because it is interesting. Extra surfaces create context, permission, reliability, and security cost.

## 2. Fingerprint dimensions

Record exact observed values where possible:

| Dimension | Examples |
|---|---|
| model | model/preset, reasoning effort, allowlist |
| harness | ChatGPT, Codex, desktop app, CLI, IDE, agent framework |
| host | OS, app build, architecture, profile/account |
| session | current task/thread vs fresh task; reload requirements |
| instructions | account/project/repo/skill scope and version |
| tools | runtime-enumerated names, schemas, server IDs, schema hashes |
| auth | signed-in identity, permission mode, token/connector state |
| entitlement | plan, org policy, feature gate, user-specific surface |
| context | truncation, stale summaries, conflicting injected state |
| external runtime | filesystem, terminal, browser, MCP, worker, telemetry |

Do not infer these from old docs when live enumeration/read-back exists.

## 3. Layer-state model

For each required capability maintain:

`DECLARED / VISIBLE / AUTHORIZED / LOADABLE / INVOKABLE / EFFECTIVE / VERIFIED`

Examples:

- Documentation says a connector exists: `DECLARED`.
- Tool appears in the current runtime list: `VISIBLE`.
- User/org permission allows it: `AUTHORIZED`.
- Host can initialize it without schema/auth errors: `LOADABLE`.
- A minimal call succeeds: `INVOKABLE`.
- The call produces the intended class of external effect: `EFFECTIVE`.
- Independent/read-back evidence confirms the acceptance-critical postcondition: `VERIFIED`.

Do not promote one state based on another.

## 4. Differential probe ladder

Prefer probes that change one variable at a time:

1. **listed vs invoked** — tool appears; can a minimal safe call execute?
2. **invoked vs effective** — response says success; did the intended state change?
3. **same model / different harness** — isolates harness/tooling effects.
4. **same harness / fresh session** — detects stale tool registration or context poisoning.
5. **same host / different permission** — only when the user authorizes the comparison.
6. **same tool / current schema** — runtime schema vs cached/configured schema.
7. **same task / with vs without skill** — detects skill negative transfer.
8. **current config / effective config** — detects ignored or shadowed settings.

A probe should have a predicted observation for competing hypotheses before it runs.

## 5. Bottleneck taxonomy

Classify at the earliest supported layer:

- `MODEL_LIMIT`
- `HARNESS_LIMIT`
- `TOOL_SURFACE_MISSING`
- `SCHEMA_OR_VERSION_DRIFT`
- `AUTH_OR_PERMISSION`
- `ENTITLEMENT_OR_PRODUCT_GATE`
- `SESSION_OR_REGISTRATION_STALE`
- `CONTEXT_OR_INSTRUCTION_INTERFERENCE`
- `ENVIRONMENT_OR_DEPENDENCY`
- `RUNTIME_EFFECT_FAILURE`
- `OBSERVABILITY_GAP`
- `UNKNOWN`

Use `UNKNOWN` until a discriminating observation exists.

## 6. Environment engineering before prompt inflation

If the failure is environmental, changing prompt rhetoric is not a fix. Prefer, when authorized:

- correct tool registration;
- current schema discovery;
- exact compatible version;
- proper app/profile/session identity;
- fresh task after capability registration when the host requires it;
- context/tool lazy loading;
- reliable read-back;
- reduced hidden coupling.

Do not claim a capability was “unlocked” merely because a prompt became more forceful.

## 7. Evidence standard

For any proposed capability change report:

- exact target identity;
- before fingerprint;
- one-variable probe;
- observed delta;
- after fingerprint;
- postcondition/read-back;
- regressions to protected capabilities;
- rollback path.

If host/runtime access is unavailable, label the diagnosis `STATIC/HYPOTHETICAL`, not `VERIFIED`.

## 8. Hard negatives

This skill must not turn these into capability workarounds:

- disabling required features to reduce failures;
- bypassing provider safety controls;
- bypassing account/access controls;
- license or DRM circumvention;
- inventing hidden settings or entitlements;
- treating a different, less-capable fallback as equivalent;
- treating tool install/config text as runtime proof.
