# ChatGPT Web + Desktop — 10-Way HOST_LIVE Validation

Use this protocol only when the user explicitly requires ten independent agents and unanimous approval. It does not replace the lighter default probe.

## Target

Plugin: `ai-efficiency-operating-system`

Expected package: `1.1.0-rc1`

Pinned repository merge commit: `5c2b940c06c97c3ee48e9cdb8e66617032bb1ad2`

Required owning surfaces:

- **ChatGPT Web**
- **ChatGPT Desktop**

Both surfaces must expose and exercise the same plugin revision. Repository presence, CI success, a marketplace manifest, or a plugin listing alone is not HOST_LIVE evidence.

## Install / sync boundary

Import or sync the repository marketplace through the actual ChatGPT workspace plugin controls for the target account/workspace. The repository root is the marketplace source; the plugin is skills-only and should remain portable across supported Web/Desktop surfaces.

If the workspace/UI does not expose the import/install route, return `HOST_IMPORT_BLOCKED`. Do not relabel it PASS.

After install/sync, refresh or start a fresh supported task/session when the host requires capability registration refresh. Do not repeatedly reinstall merely to fix a stale session without evidence that installation itself is wrong.

## Required dual-surface evidence packet

Capture current evidence for each surface:

- target account/workspace identity;
- plugin visible/installed state;
- observed plugin name/version/revision when exposed;
- fresh-session registration state;
- one positive routing probe;
- one simple-task hard negative;
- one explicit-only Expert Lab probe;
- one postcondition/read-back probe where a state claim is made;
- timestamp/build/surface metadata sufficient to detect stale evidence.

The Web packet and Desktop packet must be current for the same validation run.

## Ten independent first-pass lanes

The flat local executor launches A01–A10 with `max_parallel=10` and `require_all_concurrent=True`. Each lane must produce its own process/session/receipt and reach its decision without consuming another lane's verdict.

1. **A01 — exact package identity**: verify package name/version/pinned revision and reject stale/superseded routes.
2. **A02 — ChatGPT Web**: verify Web discovery, fresh-session availability and required behavior evidence.
3. **A03 — ChatGPT Desktop**: verify Desktop discovery, fresh-session availability and required behavior evidence.
4. **A04 — default routing**: positive plan/research/completion routing cases.
5. **A05 — hard negatives**: simple tasks and specialist nouns must not trigger heavy workflows merely by keyword.
6. **A06 — explicit-only leakage**: autonomy, persistent ledger and Expert Labs must not appear implicitly.
7. **A07 — capability boundary**: distinguish plugin/app/auth/surface/session/tool/postcondition layers; this validation run is read-only despite A07's general write capability.
8. **A08 — MCP/tool truth**: no fabricated local MCP/tool availability; current runtime schema/session evidence outranks static assumptions.
9. **A09 — authorized reverse-engineering boundary**: verify the skill remains authorization-bounded and does not imply a binary-analysis runtime is installed.
10. **A10 — independent full acceptance**: independently test the complete dual-surface acceptance contract; it does not inherit A01–A09 votes in this first-pass mode.

## Proving "simultaneous"

Ten process launches are insufficient. Strict mode requires every actor receipt to contain:

- `spawn_monotonic_ns`
- `finish_monotonic_ns`

The aggregate must prove a **common runtime overlap**:

`max(spawn_monotonic_ns) < min(finish_monotonic_ns)`

and set:

`concurrency.common_overlap_proven = true`

If ten agents all PASS but execute serially or without a common overlap interval, strict result is FAIL with `ten_way_common_overlap_missing`.

## 10/10 unanimity gate

A release may report `PASS` only when all of the following are true in one run:

- exactly ten expected actors A01–A10 produced receipts;
- ten distinct process-instance IDs;
- ten distinct execution IDs;
- ten distinct backend session IDs;
- ten distinct workspaces;
- all ten structured decisions are `PASS`;
- no VETO / FAIL / BLOCKED / missing actor;
- common runtime overlap is proven;
- ChatGPT Web HOST_LIVE evidence is current;
- ChatGPT Desktop HOST_LIVE evidence is current;
- both surfaces correspond to the same exact plugin revision.

`9/10 PASS` is FAIL. Majority voting is not accepted.

## Completion states

- `PASS` — dual-surface evidence current, exact revision matched, 10/10 PASS, common runtime overlap proven.
- `FAIL` — a verifier disproves an acceptance condition or strict concurrency/unanimity fails.
- `BLOCKED` — an external dependency prevents execution, including unavailable owning surface or unauthenticated real agent backend.
- `HOST_IMPORT_BLOCKED` — ChatGPT workspace does not expose/permit the required plugin import/install route.
- `NOT_RUN` — required Web/Desktop or 10-agent runtime verification was not executed.

Do not convert `BLOCKED`, `HOST_IMPORT_BLOCKED`, or `NOT_RUN` into a success narrative.
