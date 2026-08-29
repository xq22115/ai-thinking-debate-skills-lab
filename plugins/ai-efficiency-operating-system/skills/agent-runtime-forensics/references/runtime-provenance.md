# Runtime Provenance & Causality Model

Use with `agent-runtime-forensics` when completion or side effects require evidence beyond chat/tool prose.

## 1. Evidence planes

Keep at least three independent planes when available:

1. **Model/app plane** — prompts, model responses, tool requests, tool responses, app/session identity.
2. **Runtime plane** — process/thread, file, socket/network, browser/OS events, external service receipts.
3. **Artifact/postcondition plane** — content hashes, repository state, effective configuration, receiver read-back, final observable state.

A strong conclusion aligns planes; it does not let one plane impersonate another.

## 2. Scope identity

Every forensic record should carry enough identity to prevent cross-run contamination:

- run/session/task ID;
- goal/version when available;
- host/device/app/profile;
- target repository/workspace/process/document;
- branch/ref/artifact revision;
- start/end monotonic or wall-clock interval;
- agent/worker identity if multiple actors exist.

Events outside the bound scope are not silently imported as support.

## 3. Event normalization

Useful normalized event types:

- `MODEL_REQUEST / MODEL_RESPONSE`
- `TOOL_REQUEST / TOOL_RESPONSE`
- `PROCESS_START / PROCESS_EXIT`
- `FILE_CREATE / FILE_WRITE / FILE_RENAME / FILE_DELETE`
- `NETWORK_CONNECT / HTTP_REQUEST / HTTP_RESPONSE`
- `BROWSER_NAV / DOM_MUTATION`
- `EXTERNAL_EFFECT_RECEIPT`
- `ARTIFACT_HASH`
- `POSTCONDITION_READBACK`

Retain native IDs/timestamps as evidence pointers.

## 4. Causal edges

Use explicit edge meanings, for example:

- `REQUESTED_BY`
- `SPAWNED_BY`
- `READ_FROM`
- `WROTE_TO`
- `PRODUCED`
- `OBSERVED_BY`
- `CORROBORATES`
- `REFUTES`
- `SUPERSEDES`
- `UNKNOWN_RELATION`

Temporal adjacency is not automatically causation. A process touching a file during the same minute is supporting context, not proof that one specific tool call caused it.

## 5. Content addressing

Hash material artifacts/evidence when practical:

- before/after file content;
- generated artifact;
- repository commit/tree/blob;
- effective config snapshot;
- forensic manifest itself.

A content hash proves identity of bytes, not semantic correctness.

## 6. Taint and trust

Track taint for:

- retrieved/instruction-like external content;
- tool-generated code/commands;
- mutable persistent files;
- outputs from an untrusted/unknown server;
- evidence imported from another run.

Transformation or repetition does not remove taint or raise authority.

## 7. Effect truth

Stateful effect lifecycle:

`PREPARED → SENT/EXECUTING → OBSERVED → VERIFIED`

With alternatives:

`UNKNOWN / FAILED / CANCELLED`.

If the effect may have committed but confirmation is missing, keep `UNKNOWN`, read back the postcondition, and replay only when replay safety is established.

## 8. Diff / blame

For two runs or revisions distinguish:

- changed model/harness/instructions;
- changed tool surface/schema;
- changed environment/permission/session;
- changed artifact/target;
- changed runtime effect sequence;
- changed verifier/evidence.

Do not attribute outcome change to the model when the harness/tool/environment also changed.

## 9. Replay

Replay is a forensic experiment, not a default retry.

Before replay record:

- earliest checkpoint that must be re-executed;
- external effects already committed;
- idempotency/reconciliation status;
- target revision/environment;
- expected differentiating observations.

A non-idempotent UNKNOWN effect without reconciliation blocks automatic replay.

## 10. Forensic manifest

Minimum useful manifest:

- exact scope identity;
- ordered evidence pointers;
- artifact hashes;
- causal edges with confidence/support;
- missing edges/telemetry gaps;
- external effects and read-back;
- replay safety;
- contradictions;
- final evidence strength.

The manifest does **not** decide policy, safety, reward, or task completion by itself. It is evidence for the owning verifier.
