# Ordinary ChatGPT GitHub operation loop

Purpose: make GitHub-backed work from ordinary ChatGPT behave as a closed, evidence-bound operation rather than a sequence of loosely connected tool calls.

This loop applies to repository discovery, file/code retrieval, plugin/skill pulls, issue/PR inspection, branch/file mutation, workflow execution, and any task where GitHub state is part of the requested outcome.

## 1. The operation is one state machine

The canonical progression is:

`GOAL_LOCKED -> TARGET_RESOLVED -> AUTHORITY_RESOLVED -> READ_PLAN_READY -> SOURCE_READ -> EVIDENCE_SUFFICIENT -> TOOL_SCHEMA_READY -> INVOCATION_PREFLIGHT -> INVOKED -> RESPONSE_CLASSIFIED -> MUTATION_PREFLIGHT -> MUTATED -> READBACK_VERIFIED -> EXECUTION_OBSERVED -> ACCEPTANCE_VERIFIED -> REGRESSION_VERIFIED -> COMPLETE`

Not every task needs every state. Read-only work can skip mutation and execution states. A skipped state must be explicitly inapplicable; it cannot be silently promoted to PASS.

Allowed non-success terminals are `FAIL`, `BLOCKED`, and `NOT_RUN`.

## 2. Goal lock

Before consequential GitHub work, preserve a compact Goal Contract:

- objective;
- exact deliverable or requested effect;
- acceptance criteria;
- constraints and authority ceiling;
- target identity known so far;
- decision-critical unknowns;
- completion evidence plan;
- stop conditions.

A retrieval or tool failure never authorizes weakening the objective, deleting an acceptance criterion, or replacing an execution request with advice.

## 3. Operation envelope

Every material GitHub action should be representable by this envelope:

- `goal_id`: stable task identity;
- `operation_kind`: discover/read/search/inspect/create/update/delete/branch/pr/workflow/verify;
- `target`: owner, repository, branch/ref, path/issue/PR/workflow when applicable;
- `authority`: observed read/write/admin capability and any user constraint;
- `preconditions`: facts that must be true before invocation;
- `tool_identity`: exact action selected from the live GitHub tool surface;
- `schema_source`: live/discovered schema, never invented from memory when material;
- `arguments`: exact identifiers and parameters to send;
- `before_evidence`: revision/blob/metadata/state observed before the call;
- `expected_postcondition`: observable effect that would make the call useful;
- `result_class`: success/partial/error/empty/truncated/schema_mismatch/permission/stale_state;
- `evidence_delta`: what new trustworthy fact the call added;
- `legal_next_actions`: next transitions permitted by the observed result;
- `rollback`: exact base revision or compensating action for material writes.

The envelope is a decision record, not a demand to expose private chain-of-thought. Keep reasoning summaries concise and evidence based.

## 4. Read and discovery contract

### Exact identity beats ranked search

When owner/repository/path/ref is known, prefer exact lookup or direct fetch. Ranked repository/code search is discovery evidence, not authority.

A search miss never proves absence while a causally distinct exact route is available.

### Broad scan then targeted read

Use tree/contents/search to locate candidate paths, then fetch the exact file/object from the intended ref. Do not base material decisions on disconnected snippets when the complete source is available.

### Version dimensions stay separate

Track separately when applicable:

1. repository default branch;
2. branch HEAD commit;
3. file path and blob SHA;
4. tag/release/package/marketplace version;
5. imported or installed runtime revision.

Never merge these into a vague "latest" value.

### Truncation is partial evidence

An oversized, empty, truncated, or snippet-only response requires a targeted refetch before a conclusion that depends on omitted content.

## 5. Analysis and decision contract

Separate every material conclusion into:

- **Observed**: directly returned by GitHub or owning runtime;
- **Derived**: deterministic consequence of observed facts;
- **Hypothesis**: plausible explanation still needing a discriminating test;
- **Unknown**: not yet resolved.

Before mutation, the target, branch/ref, authority, intended bytes/state, rollback point, and acceptance check must be resolved.

Search depth is adaptive. Continue only while the next read can change a decision, close a hard criterion, resolve a contradiction, or select between routes. Source count or tool-call count alone is not depth.

## 6. Tool discovery and schema contract

Treat the live GitHub connector as a versioned runtime interface.

Before a material invocation when the action schema is not already current in context:

1. discover the relevant action narrowly;
2. verify required fields, enums, identifier types, and write semantics;
3. distinguish content references, repository identifiers, PR numbers, blob SHAs, branch refs, and connector IDs;
4. preserve opaque IDs exactly;
5. reject invented parameters or guessed endpoint behavior;
6. re-discover after a schema-mismatch signal rather than repeating a remembered call shape.

Do not load every GitHub action when a narrow discovery query is sufficient.

## 7. Invocation preflight

Before each consequential call, verify:

- the action can actually advance the current subgoal;
- target identity is unambiguous;
- required identifiers came from current evidence;
- the call is read-only, idempotent, conditionally idempotent, or effectful;
- effectful calls have a rollback/recovery path;
- dependent same-path writes are sequential;
- expected postcondition is stated;
- a failure classification route exists.

A call that cannot change the decision or state should normally not be made.

## 8. Response classification

Transport success is not task success. Classify the response before chaining another material action.

Minimum classes:

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

Preserve exact target, action, status/error, and evidence delta. Never turn an ambiguous or partial result into PASS to keep the workflow moving.

## 9. Mutation contract

For create/update/delete/branch/PR-affecting work:

1. record base revision and rollback target;
2. pre-read the current object from the exact target branch;
3. for update/delete, use the current blob SHA required by the live action schema;
4. prefer an isolated branch for non-trivial changes;
5. make the smallest causal change that satisfies the accepted goal;
6. serialize dependent writes to the same path;
7. independently read back every material write;
8. compare returned content/state with intended content/state;
9. inspect the complete changed-file set before release;
10. never use commit SHA or PR creation alone as completion proof.

## 10. Execution contract

Repository state and runtime execution are separate layers.

When the user asks to execute, test, install, activate, or prove behavior:

- a repository write proves only persisted source state;
- a workflow dispatch proves only that execution was requested;
- a green workflow proves only its declared checks on its exact commit;
- plugin configuration proves only configuration;
- installation proves only installed state;
- invocation proves only that a call ran;
- observable postcondition proves the requested effect.

Bind workflow evidence to the exact run and commit. If execution cannot be observed with available capabilities, mark that criterion `BLOCKED` or `NOT_RUN`; do not upgrade it to PASS.

## 11. Verification contract

Completion requires independent checks at the level of the user's claim.

For material work, verify as applicable:

- exact target and revision;
- persisted bytes/state by read-back;
- requested behavior/postcondition;
- at least one causally relevant failure or fallback path;
- adjacent supported path regression;
- applicable system invariants;
- no contradictory current evidence.

Use `PASS`, `FAIL`, `BLOCKED`, or `NOT_RUN` for each hard criterion.

## 12. Recovery matrix

Use the failure class to change mechanism, not wording:

| Failure signal | Required recovery |
|---|---|
| ranked/code search miss with known identity | exact repository/path/ref lookup |
| empty/truncated response | targeted fetch of the exact object/range |
| schema mismatch | rediscover the live action schema, rebuild arguments |
| stale blob SHA | re-read the same branch/path, reconcile, then retry with current SHA |
| permission blocked | read effective permissions; stop as BLOCKED if authority is genuinely absent |
| target ambiguity | resolve owner/repo/ref/path before mutation |
| partial success | read current remote state and continue only from observed state |
| workflow/request accepted but effect unknown | inspect exact run/result/postcondition |
| two same-mechanism failures without material evidence delta | choose a causally different route |
| repository state correct but host behavior missing | move verification to owning runtime; do not keep editing repository blindly |

The root goal and acceptance criteria survive route changes.

## 13. No-progress detector

After every failed or inconclusive attempt, compare the evidence fingerprint with the prior attempt.

A **material evidence delta** means at least one of these changed:

- exact target identity;
- current revision/blob/version;
- live tool schema or permission state;
- failure class;
- causal hypothesis discriminated by a new test;
- observable target state;
- legal next action.

If two attempts use the same causal mechanism and produce no material evidence delta, that mechanism is stalled and must be replaced.

## 14. Completion gate

`COMPLETE/PASS` is legal only when:

1. the requested target/effect is identified exactly;
2. all applicable mutations are read back on the exact branch/revision;
3. requested execution/activation is observed at the correct layer;
4. acceptance criteria are tested rather than inferred;
5. applicable invariants and adjacent paths are preserved;
6. contradictory evidence is resolved;
7. any required cleanup/rollback verification has completed.

If any required item is missing, use `FAIL`, `BLOCKED`, or `NOT_RUN` and retain the exact next actionable transition.

## 15. Operation-specific minimums

### Read/search

Exact identity when known -> complete object fetch -> version binding -> evidence sufficiency check.

### File write

Pre-read -> current blob SHA -> isolated branch when non-trivial -> write -> exact-branch read-back -> content comparison -> diff/regression.

### PR work

Resolve PR/base/head -> inspect changed files/patch -> perform requested review/update -> read PR metadata back -> verify checks when part of acceptance.

### Workflow work

Resolve workflow/ref -> confirm inputs/schema -> request execution -> bind run to exact commit -> inspect conclusion/log evidence -> verify requested postcondition.

### Plugin/skill pull

Source resolved -> registration resolved -> version resolved -> installed/synced -> read back -> discovered/registered -> executed -> observable effect -> regression preserved.

This document is the human-readable operational projection of `github-pull-runtime.json`; the validator must fail closed if required states or contracts disappear from the machine-readable profile.