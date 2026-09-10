# ChatGPT Web + Desktop — 10-Way HOST_LIVE Validation

Use this strict protocol only when ten independent verification lanes are required. It does not replace the lighter runtime probe.

## Target

Plugin: `ai-efficiency-operating-system`

Expected package: read `version` from `plugins/ai-efficiency-operating-system/.codex-plugin/plugin.json` at the exact imported/synced revision. A duplicated hard-coded package version is forbidden.

GitHub binding: read `.app.json#apps.github.id` from the same exact imported/synced revision and verify the owning ChatGPT surface has the GitHub app available/connected before GitHub-backed lanes can PASS.

Revision rule: record the **exact installed/synced commit or package revision exposed by the owning surface**. Do not keep a stale hard-coded merge SHA in this protocol.

Required owning surfaces when dual-surface validation is requested:

- **ChatGPT Web**
- **ChatGPT Desktop**

Repository presence, CI success, a marketplace manifest, plugin listing, or connector visibility alone is not HOST_LIVE evidence.

## Install / sync boundary

Import or sync the repository marketplace through the actual supported workspace/plugin controls for the target account/workspace. The repository root is the marketplace source. The plugin contains skills plus an explicit GitHub app binding; repository presence does not prove either the plugin or the app is live on the owning ChatGPT surface.

If the workspace/UI does not expose or permit the import/install route, return `HOST_IMPORT_BLOCKED`. Do not relabel it PASS.

After install/sync, refresh or start a fresh supported task/session when the host requires capability registration refresh. Do not repeatedly reinstall merely to fix a stale session without evidence that installation itself is wrong.

## Required evidence packet per surface

Capture current evidence for each tested surface:

- target account/workspace identity;
- plugin visible/installed state;
- plugin version read from the exact imported manifest plus observed host version/revision when exposed;
- GitHub app declared/available/connected state when a GitHub lane is exercised;
- fresh-session registration/tool-namespace state;
- one **goal-gate implicit routing** probe;
- one **conditional specialist implicit activation** probe without an explicit `@skill` mention;
- one **simple/explanation hard negative** that must not activate a heavy specialist;
- one **bounded composition** probe proving no more than three implicit skills for a phase;
- one **fallback/self-repair** probe after a simulated/unavailable specialist or GitHub retrieval route;
- one postcondition/read-back probe where a state claim is made;
- timestamp/build/surface metadata sufficient to detect stale evidence.

The Web/Desktop packets must be current for the same validation run when both are required.

## Required GitHub bridge probe

When the validation concerns ordinary-ChatGPT GitHub pulls, each tested owning surface must additionally prove:

1. `.codex-plugin/plugin.json` points to `./.app.json`.
2. `.app.json` exposes the expected `github` connector binding.
3. The GitHub app is available/connected and its tool namespace is visible.
4. Exact repository lookup succeeds for a known target.
5. Exact-ref file retrieval succeeds.
6. A search miss does not become an absence claim until a causally distinct fallback is attempted.
7. Empty/truncated responses trigger targeted refetch rather than inference.
8. If a material write is tested, prewrite blob state is read, the write is sequential, and the resulting target branch is read back.
9. A safe stale-SHA or equivalent detectable failure is exercised when write-path verification is required, and accepted state is shown not to be corrupted.

## Required implicit probes

At least one probe from each relevant class:

1. **Capability gap** — same model or product behaves differently across harness/session/account/surface; expected conditional activation: `capability-forensics`.
2. **MCP/tool-surface pressure** — many/changing tools, schema drift, namespace collision or context pressure; expected: `mcp-surface-engineering`.
3. **Runtime effect mismatch** — tool/process reports success but real postcondition is missing; expected: `agent-runtime-forensics`.

A passing probe must show actual host routing evidence when the host exposes it, plus behavior consistent with the specialist's required workflow. Merely mentioning the skill name in prose is not proof of invocation.

## Hard negatives

Heavy specialists must stay dormant for explanation-only/simple requests such as:

- `MCP 是什麼？`
- `Ghidra 是做什麼的？`
- simple arithmetic/translation/rewrite.

Specialist nouns alone are not sufficient triggers.

## Ten independent first-pass lanes

If strict ten-lane validation is requested, each lane must produce an independent receipt and must not inherit another lane's verdict:

1. **A01 — exact package identity**: verify manifest-derived package version, exact imported revision, GitHub app binding and stale/superseded route rejection.
2. **A02 — ChatGPT Web**: verify discovery, fresh-session availability and required behavior evidence.
3. **A03 — ChatGPT Desktop**: verify discovery, fresh-session availability and required behavior evidence.
4. **A04 — default routing**: goal gate + plan/research/completion cases.
5. **A05 — hard negatives**: simple tasks and specialist nouns do not trigger heavy workflows by themselves.
6. **A06 — conditional auto-invoke**: capability/MCP/runtime specialists activate implicitly only on material signals; autonomy/ledger/authorized reverse stay explicit-only.
7. **A07 — capability truth**: distinguish declared/visible/authorized/loadable/invokable/effective/verified states, including GitHub app/tool namespace state.
8. **A08 — bounded composition + fallback**: at most three implicit skills; failed specialist/GitHub routes preserve root goal and fall back to a goal-advancing route.
9. **A09 — authorization boundary**: `authorized-reverse-engineering` remains explicit and does not imply a binary-analysis runtime exists.
10. **A10 — independent full acceptance**: independently test the complete surface contract, GitHub bridge when applicable, and postconditions.

## Proving simultaneous strict lanes

When strict concurrency is part of the acceptance contract, every actor receipt must contain:

- `spawn_monotonic_ns`
- `finish_monotonic_ns`

The aggregate must prove a common overlap:

`max(spawn_monotonic_ns) < min(finish_monotonic_ns)`

and set `concurrency.common_overlap_proven = true`.

Ten process launches without common overlap are not proof of simultaneous execution.

## Strict PASS gate

A strict run may report `PASS` only when all requested acceptance conditions are evidenced in one run, including exact revision, manifest-derived version, owning-surface freshness, GitHub app binding/connection when applicable, implicit routing, hard negatives, bounded composition, fallback behavior, postcondition evidence and any requested independent-lane/concurrency conditions.

No majority-vote shortcut: a required failing or missing lane keeps the run non-PASS.

## Completion states

- `PASS` — all requested owning-surface and behavioral evidence is current and passes.
- `FAIL` — an acceptance condition is disproved.
- `BLOCKED` — an external dependency prevents execution.
- `HOST_IMPORT_BLOCKED` — owning workspace does not expose/permit required import/install route.
- `NOT_RUN` — required owning-surface verification was not executed.

Do not convert `BLOCKED`, `HOST_IMPORT_BLOCKED`, or `NOT_RUN` into a success narrative.
