# Evidence and completion gate

Machine-enforced lifecycle and validation invariants live in `../../../contracts/evaluator-governance.json` and `../../../contracts/validation-policy.json`. This reference explains their application.

## Claim record

For each acceptance-critical claim keep:

- requirement ID;
- exact claim;
- target/ref/runtime identity;
- supporting evidence;
- contradicting evidence;
- source/provenance family;
- validator/observer identity;
- observed time and freshness;
- status `PROVEN | PARTIAL | CONTESTED | UNKNOWN | FAILED`.

## Validation truth is layered

Keep four different questions separate:

1. `STRUCTURAL` — schemas, manifests, paths and hashes are valid.
2. `INSTALLED_TEMPLATE` — the intended package/template/import exists on the target installation surface.
3. `EXECUTABLE` — the relevant validator/skill/tool path was actually executed in the tested environment.
4. `BEHAVIORAL_TARGET` — the owning runtime/user path produced the required postcondition.

A lower-layer PASS never implies a higher-layer PASS. An archived release report is history, not proof for a changed artifact. Fresh receipts bind exact artifact/revision, target, observer, scope and validation layer.

A YAML/Markdown gate with no executable owner is descriptive only. It cannot unlock VERIFIED.

## Postcondition examples

- file change → read exact file/ref back;
- configuration → read effective configuration, not only source file;
- service fix → exercise a real request/path;
- installation → enumerate/load/invoke the capability;
- GitHub change → inspect exact commit/diff and relevant checks;
- UI behavior → exercise the user path;
- delivery → receiver or independent observer reads the object back.

## False-completion vetoes

Do not close a task while any active hard criterion has:

- no proof surface;
- stale target/version evidence;
- unresolved contradiction that can change the verdict;
- effect state `UNKNOWN` whose resolution changes acceptance;
- executor-only proof when independence is required;
- missing receiver/read-back for a delivery claim;
- host-live claim based only on repository/package presence;
- a claimed validation layer above the strongest observed layer;
- an archived/stale receipt for the current artifact.

## Evaluator admission and tribunal

A verifier is `(name, version, configuration, method_family)`, not a timeless label. Lifecycle:

`PROPOSED → ACTIVE → QUARANTINED / DEPRECATED`

Admission for material certification should preserve known-outcome/golden cases, false-accept and false-reject observations, disagreement evidence, known failure codes and scope/version. A modified verifier does not inherit admission merely from its name.

For high-impact PASS:

- one admitted deterministic/direct method must pass;
- an independent method must corroborate when the contract requires independent certification;
- deterministic/direct FAIL vetoes semantic PASS;
- material method disagreement returns `REVIEW`, not averaged confidence;
- a single semantic judge is insufficient merely because it is newer, larger or persuasive.

Bias diagnostics can include order/position, surface formatting, language, prompt lineage and shared evidence route. Known systematic mismatch can quarantine or deprecate the evaluator.

## Promotion evidence

Distinguish `SIMULATED_CONTROL` from `OBSERVED_TARGET` telemetry. Synthetic or planted known-outcome tests can validate the control mechanism but are capped at `SHADOW_ONLY`. Production/host promotion additionally requires observed-target evidence, protected quality non-regression and an actual efficiency/cost gain.

Sparse critics are failure detectors. Their findings contribute zero extra consensus votes; trigger them only when the corresponding risk is present.

## Honest terminal states

Use `PARTIAL`, `BLOCKED`, `UNKNOWN`, or `FAILED_VALIDATION` when appropriate. Never shrink the original target so that a proxy can be called complete.
