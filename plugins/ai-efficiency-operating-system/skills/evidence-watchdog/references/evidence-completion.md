# Evidence and completion gate

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
- host-live claim based only on repository/package presence.

## Verifier admission

A verifier is `(name, version, configuration)`. For material certification, preserve canary/holdout evidence and false-accept failures. A newer/larger judge is not automatically more trustworthy.

## Honest terminal states

Use `PARTIAL`, `BLOCKED`, `UNKNOWN`, or `FAILED_VALIDATION` when appropriate. Never shrink the original target so that a proxy can be called complete.
