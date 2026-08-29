# ARR v1.3 durable-runtime reference

Use only on a host with real durable state and effect primitives.

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

## Effect state

Typical lifecycle:

`PREPARED → EXECUTING → VERIFIED`

with `UNKNOWN / FAILED / CANCELLED` alternatives.

For `UNKNOWN`: inspect durable action state, verify postcondition, converge to VERIFIED if effect exists, and re-execute only when replay safety is proven.

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
