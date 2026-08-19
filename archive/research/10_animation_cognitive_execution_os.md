# Animation Cognitive Execution OS v1.2.0

## Verdict preserved from test report
`ENGINEERING RELEASE GATES: PASS`

Boundary: this verdict is limited to the local filesystem/runtime/build environment. It does **not** prove the user's Chrome extension, ChatGPT account, Apple applications, live research providers or live language models were tested.

## Evidence matrix
- resumable pytest matrix: **129/129 PASS** across **21/21 shards**
- deterministic capability evaluation: **11/11 PASS**
- mutation attacks: **13/13 blocked**
- finite executable model: **1717 states / 4929 transitions**
- intentionally unsafe finalize mutation: counterexample found in **21 states**
- static/security audit: **74 Python files, 0 issues, 0 secret files**
- dependency assurance: **5 exact installed distributions**
- core branch coverage: **75.37%** over the retained 128-test core dataset
- release-only CLI bootstrap test: PASS
- reference animation forensics: PASS
- static repeated-frame fake: rejected as expected

## Failure/recovery behaviors actually exercised
- same-transaction state + hash-linked event writes using `BEGIN IMMEDIATE`
- process death before commit
- process death after WAL commit but before checkpoint
- concurrent event writers
- lease contenders and fencing tokens
- outbox ownership
- audit proof + completion event + certificate + COMPLETE state atomicity
- direct-SQL invalid-state attempts against database triggers
- trigger bypass followed by event-chain tamper detection
- migration replay keyed by source DB SHA-256
- bitemporal memory/entity/relation writes and event rollback
- research query/source/claim atomicity and source immutability
- Native Messaging truncation, oversize, invalid UTF-8, path traversal and replay mutations
- snapshot v2 online backup + manifest binding
- ZIP-slip rejection and offline restore
- candidate installation ordering and current-version activation gates
- direct CLI execution from `/tmp` without externally supplied `PYTHONPATH`

## Coverage honesty
The complete 129-test release matrix passed. The retained branch-coverage dataset covered the original 128 core-scope tests. A later attempt to rerun coverage across all 129 tests was externally terminated; partial coverage data was discarded rather than claimed.

## Formal-method boundary
A finite executable model was explored to depth 10 and detected the injected unsafe finalize transition. TLA+ specifications were supplied, but TLC was **not** executed.

Evidence label:
`FINITE_EXECUTABLE_MODEL_TESTED + SPEC_PROVIDED_NOT_TLC_EXECUTED`

## Animation-quality boundary
The report included motion/geometry proxy metrics and a deliberately static negative example. These checks do **not** establish:
- character identity fidelity
- semantic correctness
- aesthetic quality
- licensing status
- Apple-client compatibility

## Engineering significance
This project is valuable beyond animation because it demonstrates several general reliability patterns:
- atomic completion and evidence transitions
- crash recovery around WAL/checkpoint boundaries
- lease/fencing semantics
- append-only integrity chains
- bitemporal memory rollback
- mutation testing
- release-gate honesty
- backup/restore verification
- installation activation ordering

These patterns can be reused by long-running desktop/agent systems where a task must survive crashes and cannot self-declare completion without durable evidence.
