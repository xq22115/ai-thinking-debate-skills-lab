# ARR v1.3 durable-runtime reference

Use only on a host with real durable state and effect primitives. Machine replay invariants live in `../../../contracts/replay-checkpoints.json`.

## Separate semantic planes

1. logical — goal, plan, conversation, branch, checkpoint; rollback/fork may be valid;
2. control — identity, authority, approval, fencing, pending-event admission; monotonic where required;
3. effect/evidence — external effects, postconditions, evidence, completion proof;
4. delivery — sender dispatch, receiver read-back, ACK;
5. external temporal witness — separate durability domain when full primary-store rollback must be detectable.

Core invariant:

`logical rewind != authority rewind != effect rewind != delivery rewind`

## Goal CAS and authority

Effect-bearing actions bind the current `goal_version`. Goal updates create a new version; stale actions fail before execute/commit.

Authority grants should bind run, subject, goal version, ownership epoch/fence, capability, semantic scope, mode/expiry and parent grant when applicable. Consume one-shot authority before external dispatch, not after the response, so response loss cannot resurrect authority.

## Typed task graph and state planes

For durable long-horizon execution, use typed nodes where useful:

`AND / OR / PARALLEL / HYPOTHESIS / RECURSIVE_CALL_RETURN`

Break effect-bearing or acceptance-bearing work into atomic verifiable nodes. Keep:

- L0-style task/acceptance contract immutable except through explicit goal versioning;
- verifier/owning-runtime verified state separate from worker-local branch scratch;
- branch scratch local until independently admitted;
- a continuation/checkpoint cursor so resume does not require replaying a transcript summary.

Re-run only invalidated downstream nodes when dependencies make that safe.

## C0–C6 replay checkpoints

Use the earliest checkpoint whose assumptions were invalidated:

- `C0` — goal / policy / authority;
- `C1` — candidate plan / task graph;
- `C2` — target identity / compatibility / authority;
- `C3` — evidence cache / provenance / research state;
- `C4` — mechanism verdict / accepted change;
- `C5` — evaluator / regression state;
- `C6` — accepted completion / promotion / delivery.

Examples: a changed goal restarts at C0; stale source evidence at C3; invalid verifier/regression at C5. Do not replay unrelated upstream work merely because one downstream stage failed.

## Effect state

Typical lifecycle:

`PREPARED → EXECUTING → VERIFIED`

with `UNKNOWN / FAILED / CANCELLED` alternatives.

For `UNKNOWN`: inspect durable action state, verify postcondition, converge to VERIFIED if effect exists, and re-execute only when replay safety is proven.

For non-idempotent UNKNOWN effects with no reconciliation path: block replay. With reconciliation available: reconcile first. If the same semantic effect is already VERIFIED, return its prior receipt instead of executing again. Divergent irreversible history requires an explicit fork.

## Event and artifact integrity

Keep persistent event identity distinct from provider request/tool-call IDs. Reject duplicate event IDs and use deterministic digests where events participate in integrity checks.

Large payloads may be stored by content address rather than duplicated inside every control event. Indirection must include:

- digest + size verification;
- deduplication;
- live-reference/witness-aware retention;
- bounded quota/backpressure;
- explicit `UNAVAILABLE_ARTIFACT` on missing blobs.

Moving bytes out of the event stream does not eliminate storage obligations. Missing referenced data never becomes verification PASS.

## Execution envelope

Resume must reconstruct more than transcript text:

- state owner and goal version;
- workspace/cwd;
- tools and skills;
- hooks/instructions/rule versions;
- permission profile;
- runtime/protocol versions;
- freshness stamps.

Missing/stale capability or protocol-major drift can be a hard resume failure.

## Lifecycle and delivery

Distinguish:

`SCHEDULED → DISPATCHED → STARTED → EFFECT_OBSERVED → COMPLETED → DELIVERED → ACKED`

A future schedule timestamp is not evidence the prior execution ran. ACK comes from receiver or an independent observer, not the sender.

## Memory authority

Store content hash, source kind, provenance/derived-from lineage, authority level/ceiling and scope/version. Summary, echo and repetition do not raise authority.

## Semantic replay

Checkpoint an effect frontier. After restore, an already committed semantic intent returns the prior receipt; divergent irreversible history requires an explicit fork before new effects.
