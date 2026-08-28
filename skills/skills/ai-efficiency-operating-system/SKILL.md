---
name: ai-efficiency-operating-system
description: Canonical orchestration skill for maximizing verified AI task progress by converting implicit context into explicit contracts, protecting the real goal, demand-loading context/tools, making execution recoverable, and requiring exact-target verification without sacrificing required capabilities, concurrency, reasoning depth or answer quality.
---

# AI Efficiency Operating System

Version: `0.3.0-rc1`  
Status: `GITHUB_PACKAGE_EVOLVED / HOST_LIVE_UNVERIFIED`  
Canonical owner: `xq22115/ai-thinking-debate-skills-lab/skills/skills/ai-efficiency-operating-system`

## 0. v0.3 thesis — implicit context is hidden state

v0.2 established goal control, evidence levels, demand-loaded context/tools, recoverable execution and owning-runtime completion gates. Cross-chat recovery exposed a deeper shared failure class:

> **Implicit context is hidden state, and hidden state is an efficiency/reliability bug.**

Agents become slow, wrong, repetitive or falsely complete when they silently assume:

- which user instruction is currently authoritative;
- which host/surface/version an instruction applies to;
- whether a summary preserved every protected invariant;
- whether a child/resumed agent inherited the latest state;
- whether a failed turn is allowed to become durable truth;
- whether a cached observation still matches the current revision;
- whether another retry actually changes the strategy;
- whether a sent handoff was incorporated;
- whether a protocol version/transport/auth assumption is current;
- whether a skill should activate at all;
- whether the worker that changed the target may also self-certify completion;
- whether a restored state store is newer than the last irreversible effect;
- whether files described by a validator physically exist.

v0.3 converts those assumptions into explicit, inspectable and testable contracts.

This package remains the **single canonical efficiency orchestration owner**. Do not create `efficiency-v3`, `ai-efficiency-plus`, or parallel aliases for the same responsibility.

## 1. Root objective and protected invariants

Maximize:

> **verified goal attainment per unit of context, tool work, latency, repeated effort and human correction**

while preserving the user's actual requirements.

Protected invariants unless explicitly changed by the user:

- the active `ROOT_GOAL`;
- hard constraints and negative requirements;
- required features and tools;
- required concurrency / number of simultaneous chats or work units;
- genuine reasoning and research depth;
- answer quality;
- native Stop/control ownership;
- required workload size;
- evidence quality;
- recoverability and rollback;
- truthful completion state.

The performance invariant remains:

> `不卡頓 != 秒回`

Do not make the system look faster by reducing protected work. Deep reasoning time, model stream cadence, UI publication cadence, history/evidence materialization and tool/network I/O are separate budgets.

## 2. Compile the task before substantive work

Maintain a durable task contract:

- `PRIMARY_TASK`
- `DESIRED_END_STATE`
- `ROOT_GOAL`
- `NEGATIONS`
- `HARD_CONSTRAINTS`
- `ACCEPTANCE_TESTS`
- `CURRENT_BLOCKER`
- `NEXT_ACTION`
- `EVIDENCE`

Classify later user content as:

- `CORRECTION`
- `ADD`
- `UPDATE`
- `EXAMPLE`
- `DISTRACTOR`

An explicit user correction outranks an older assistant assumption. Retrieval, memory, summaries, tool output and agent opinions may update evidence but may not silently rewrite the task.

Every substantive action/tool call must have a credible causal path to the active task contract. If it does not, do not execute it.

## 3. Ten-dimensional target identity lock

Before a material mutation, re-read the exact target rather than trusting stale prose.

Check, as applicable:

1. active root goal / latest correction;
2. product or execution surface;
3. repository / workspace identity;
4. canonical architecture or semantic owner;
5. branch/ref/PR;
6. exact head/revision/version;
7. merge-base / ahead / behind / supersession relation;
8. exact changed paths / object identities;
9. exact-head test/review/readiness evidence;
10. owning-runtime/native behavioral acceptance requirement.

Current structured state outranks PR descriptions, old chat summaries and historical receipts for mutable facts.

Cross-chat rule:

> **diagnosis may fan out; shared mutable ownership and finalization are single-writer.**

## 4. Instruction scope, precedence and provenance

### 4.1 No universal instruction hierarchy

Portable instructions do not imply portable precedence.

For each active instruction source record:

- source ID and provenance;
- host/product surface;
- path/account/workspace scope;
- import/merge behavior;
- priority or observed precedence;
- applicable model/runtime/protocol version;
- purpose;
- evidence;
- introduced date/version;
- retest triggers;
- current status.

Do not assume `AGENTS.md`, `CLAUDE.md`, account Custom Instructions, repository instructions, skill instructions and runtime policy merge the same way across products.

If precedence is ambiguous, use a harmless conflict probe against the exact host/version instead of guessing.

### 4.2 Retest durable rules

A workaround is not eternal truth.

Retest or retire a durable instruction when any material dependency changes, including:

- host/client version;
- model family;
- protocol version;
- repository path/owner;
- runtime or permission surface;
- observed behavior contradicting the workaround;
- upstream fix/deprecation.

Keep provenance with the rule so later sessions know **why it exists**.

## 5. Context economy, lineage and semantic compaction

Treat context as scarce working memory, not as an append-only archive.

Use progressive disclosure:

1. task contract + compact capability index;
2. selected skill metadata;
3. selected `SKILL.md`;
4. only required references/schemas/scripts;
5. exact source evidence when a claim becomes material.

Rules:

- discover many, load few;
- keep one semantic owner for each durable rule;
- reference unchanged large evidence instead of reinjecting it;
- summaries are navigation/index artifacts, not final authority;
- rehydrate exact sources when the claim matters again.

### 5.1 Per-agent/session context lineage

A subagent, resumed chat or delegated runtime may not share the same context window.

Record:

- parent run/session;
- checkpoint ID;
- inherited state digest;
- local additions/corrections;
- evidence pointers;
- current goal hash;
- reconciliation result before mutation.

Never infer that a child inherited a correction merely because the parent did.

### 5.2 Semantic compaction with rollback

Compaction must preserve semantic units.

Do not split or discard:

- tool call ↔ tool response pairs;
- current task contract;
- protected invariants;
- exact evidence required for material claims;
- unresolved contradictions;
- strong minority hypotheses;
- pending irreversible actions;
- ownership/revision facts;
- rollback target.

After compaction, validate invariants. If a protected item is missing or changed, roll back the compaction or rehydrate from source.

### 5.3 Content-addressed observation cache

Cache stable large observations by:

`target identity + query/path + revision/version + content hash`

Reference the cache until any identity/content component changes.

A blob SHA mismatch, branch move, file update, permission change or protocol/runtime change invalidates the relevant cache entry.

## 6. Failed-turn and memory hygiene

### 6.1 Failed turns are transactions

A blocked, malformed, empty, interrupted or invalid turn does **not** become durable truth.

Turn states:

`RECEIVED → VALIDATED → COMMITTED`

or:

`RECEIVED/VALIDATED → QUARANTINED`

Only committed, evidence-backed deltas may update durable task state.

Examples of quarantined material:

- auth-blocked runtime probe output presented as successful execution;
- malformed connector request;
- empty agent response;
- tool call interrupted before postcondition;
- unsupported inference from an error wrapper.

### 6.2 Memory authority and recurrence

Do not consolidate every event into durable memory.

Promote memory/rules when a mechanism is:

- recurrent or materially important;
- validated by current evidence;
- scoped to the correct surface/version;
- provenance-labelled;
- equipped with a retest/expiry trigger.

A one-off outage cannot become “this tool is unavailable forever.”

Prefer recurrence-triggered consolidation over expensive full-memory rewriting every turn.

## 7. Input fidelity before reasoning

When input passes through speech/dictation/cleanup or another preprocessing stage, separate:

`RAW_INPUT → CORRECTED_INTENT → GENERATED_REWRITE`

Do not measure them as one “accuracy” number.

Preserve, unless explicitly corrected:

- proper nouns;
- technical terms and mixed-language tokens;
- file/repository/product names;
- dates/times;
- negations;
- numbers and identifiers;
- the user's final course correction.

Useful metrics:

- Proper-Noun Exact Match;
- Code-Switch Retention;
- Correction Intent Accuracy;
- Hallucination Rate;
- Deletion Rate.

Example: “下午兩點——不對，三點半” should resolve intent to 3:30 while the raw provenance remains distinguishable from AI cleanup.

## 8. Reasoning and research: model delta, not performance theater

A unit of work counts as deeper only if it adds at least one:

- new mechanism;
- falsified hypothesis;
- stronger causal evidence;
- discriminating experiment;
- meaningful global-model delta;
- sharper failure boundary.

Not depth:

- fixed waiting;
- slow output;
- token drip;
- repeated polling;
- tool/network waiting;
- verbosity;
- duplicated sources;
- raw source count;
- role/headcount.

Maintain a coverage frontier:

- `COVERED`
- `PARTIAL`
- `UNKNOWN`
- `EXCLUDED`

Rank gaps by:

`goal impact × uncertainty × blocking power × verifiability`

Maintain competing hypotheses and seek falsifiers. If the same mechanism repeatedly fails, change mechanism/route/source rather than retrying cosmetically.

Stop research when testing/execution/read-back has higher expected information gain.

## 9. Adaptive multi-agent topology

Use the smallest coalition that adds distinct value.

A role is justified only by a distinct:

- evidence channel;
- method;
- capability;
- falsification pressure;
- verification duty;
- domain specialty;
- security/recovery obligation.

Route and retain:

- new evidence;
- material contradiction;
- falsifiers/discriminating tests;
- blocking risks;
- strong minority evidence;
- confidence changes with reasons.

Compress repeated agreement and paraphrase.

### 9.1 A01–A10 canonical topology

Reuse these names only:

- **A01 Orchestrator** — task contract, source coverage, dependency graph, acceptance ownership.
- **A02 Architect/Claimant** — candidate architecture and causal mechanism.
- **A03 Source Research** — original chat/library/repository/current external evidence.
- **A04 Root Cause** — shared mechanism clustering and discriminating tests.
- **A05 Adversarial** — omission, proxy win, regression, injection and false-completion attacks.
- **A06 Cross Exam** — user directive vs evidence vs synthesis; naming/claim challenge.
- **A07 Implementer** — identity-locked scoped mutation.
- **A08 Verifier** — structure, exact revision, alternate paths, read-back and owning-runtime acceptance.
- **A09 Risk** — rollback, permissions, blast radius, compatibility and irreversible actions.
- **A10 Adjudicator** — best evidence-weighted solution plus unresolved minority evidence.

### 9.2 Real-agent proof

Do not call ten role labels “ten agents.”

A genuine independent-agent claim requires:

- distinct runtime/session identity;
- independent execution start receipt;
- task-bound terminal receipt;
- evidence of non-shared execution when independence matters.

Without them, label the work `INDEPENDENT_REVIEW_WORKSTREAMS`.

## 10. Execution, ownership and retry

### 10.1 Parallel reads, serial conflicting writes

Parallelize independent research/read-only inspections.

For mutable targets:

- one current writer/owner per semantic target;
- re-read the current revision immediately before write;
- use CAS/expected-head/version tokens where possible;
- serialize conflicting writes;
- read back after mutation;
- recompute downstream topology if another chat/worker advanced the target.

### 10.2 Short critical sections

Hold locks/leases only around the minimum state transition that truly requires mutual exclusion.

Move slow:

- network I/O;
- model calls;
- retries/backoff;
- long validation;
- remote settlement

outside shared/global critical sections unless correctness requires otherwise.

A lock should protect admission/ownership, not unnecessarily serialize the entire remote operation.

### 10.3 Changed-strategy retry + circuit breaker

Every retry must state what changed:

- route;
- hypothesis;
- parameters;
- permission/auth state;
- version;
- timing/backoff;
- target identity.

Default failure-class cap: **3 attempts** unless the task contract or provider semantics justify another value.

After the cap:

- open a circuit breaker;
- preserve the failure receipt;
- update the hypothesis/route;
- surface the blocker.

Never blindly replay a rejected side effect.

### 10.4 Event-driven waiting

If the platform provides a task/event/hook state, persist the pending obligation and resume on signal rather than repeatedly running full reasoning merely to wait.

Idle waiting is not deliberation.

### 10.5 Branch-scoped degradation

A local outage/restriction degrades only the affected branch/tool/surface.

Do not globally disable unrelated capabilities because one executor is offline.

This does not bypass higher-priority safety/platform restrictions.

## 11. Durable continuity and handoff truth

Chat history is not the canonical task database for long work.

Persist:

- task/run IDs;
- goal hash/task contract;
- current owner/revision;
- event journal;
- checkpoints;
- irreversible receipts;
- pending obligations;
- idempotency/fencing state;
- rollback target;
- protocol/runtime identity.

Handoff/message states:

`SENT → DELIVERED → ACKNOWLEDGED → INCORPORATED → VERIFIED`

Do not collapse them.

A successful send/hook/task transport is not domain completion. Receiver read-back proves incorporation; acceptance evidence proves verification.

On resume, reconcile live state before acting.

## 12. Protocol/version compatibility is part of correctness

Before protocol-sensitive behavior, record:

- protocol version;
- transport;
- client/server SDK versions;
- negotiated extensions/capabilities;
- auth mode;
- host/runtime version.

For MCP specifically, the official `2026-07-28` release changes the protocol core to stateless request/response and removes the old initialize/session pattern. Apply those semantics only when the actual peer supports/negotiates that contract.

Current architecture must also honor deprecations. OpenAI's 2026-08-24 release notes deprecate `codex mcp-server` in favor of **Codex app server**; old chat history must not freeze a deprecated transport as the permanent core.

Protocol assumptions are versioned evidence, not memories.

## 13. Skill admission: precision, recall and marginal utility

A skill can be individually “correct” and still reduce system quality if it triggers too broadly or adds context without value.

Before promotion evaluate:

1. positive trigger recall;
2. hard-negative trigger precision;
3. exact host/version compatibility;
4. behavior/constraint coverage;
5. context/token cost;
6. paired baseline vs skill-enabled outcome;
7. representative holdout/regression;
8. alternate-path invariants;
9. no protected capability regression.

A generated/modified skill may **not self-approve**.

“More skills” is not inherently better. Keep the minimum semantic owners that improve verified outcomes.

## 14. Worker and completion judge separation

For material completion, separate execution from certification.

The worker/implementer may provide:

- mutation receipt;
- claimed postcondition;
- tests it ran.

A verifier must independently check the acceptance duty appropriate to the claim.

Repository write ≠ host activation.  
CI PASS ≠ deployment.  
Transport success ≠ task success.  
Agent “done” ≠ verified completion.

## 15. Performance engineering without goal shrink

Separate budgets for:

- genuine reasoning/research;
- model generation;
- UI publish/render;
- history/evidence materialization;
- tool/network I/O.

Investigate:

- context pollution;
- repeated schema/tool discovery;
- duplicated full-history transforms;
- cache misses;
- retry storms;
- queue/scheduler contention;
- lock scope;
- serialization;
- cross-tab shared failure domains;
- resource bottlenecks;
- incremental O(N²)-like work;
- stale workflow generations.

Hot paths should process deltas.

Heavy full-history normalization, hashing, evidence materialization and global scans belong in cold paths/checkpoints when possible.

Do not “fix” speed by:

- reducing required chat count;
- disabling required tools/features;
- lowering reasoning depth;
- lowering answer quality;
- shortening required work;
- hiding real 429/errors;
- artificial token/character pacing.

## 16. Evidence and completion state

Evidence levels:

- `E0` Unsupported
- `E1` Indirect context
- `E2` Authoritative static
- `E3` Deterministic check
- `E4` Independent corroboration
- `E5` Owning-runtime postcondition
- `E6` Repeated reliability/regression/recovery

Completion states:

`DRAFTED → PACKAGED → IMPLEMENTED → TESTED → VERIFIED → HOST_LIVE → DEPLOYED → HEALTHY`

A claim cannot advance past its evidence.

### Physical materialization gate

A package PASS requires both:

- **declared → actual**: every required declared artifact physically exists;
- **actual → declared**: every core artifact is represented by the package contract/catalog.

Where material, verify exact hashes/content identities.

Do not validate a file merely because a plan/report says it should exist.

### Temporal witness

For state whose rollback would repeat irreversible work or lose authority generation, keep an independent monotonic witness/frontier when practical.

On resume/startup, reject a primary store that has regressed behind the witness.

## 17. Alternate-path invariant testing

Correctness/security controls must be tested on every materially distinct path that can bypass them.

As relevant, test:

- foreground;
- background;
- subagent;
- worktree/branch;
- compaction;
- resume/restart;
- headless;
- cross-session;
- alternate transport/provider.

A foreground PASS cannot certify a background path that was never exercised.

## 18. Runtime state contract

Long-horizon state is defined in `runtime-state.schema.json` and includes:

- task/run identity and goal hash;
- task contract + target identity lock;
- instruction scope/provenance;
- context lineage;
- memory authority;
- input fidelity;
- tool/protocol route;
- agents/workstreams;
- hypothesis/evidence ledgers;
- event journal + failed-turn quarantine;
- delivery ledger;
- observation cache;
- retry/circuit breaker state;
- writer lease + idempotency;
- mutation/verifier receipts;
- alternate-path checks;
- temporal witnesses;
- rollback target;
- completion state + pending obligations.

## 19. Evolution loop

Do not evolve by unbounded prompt accretion.

Use:

`freeze baseline → execute → evaluate → attribute earliest causal failure → minimal causal patch → target set → protection set → hard negatives → holdout/regression → adjudicate → promote/hold/reject → rollback reference`

Record why a patch was added and what evidence would remove it later.

Prefer deleting redundant instructions when a leaner contract performs equal or better.

## 20. Output contract

For a substantive run, persist or report as applicable:

1. task contract / goal hash;
2. exact target identity;
3. active instruction scope/provenance;
4. activated modules and why;
5. context/tool route;
6. evidence/hypothesis state;
7. agent topology + independence status;
8. execution ownership/idempotency/retry state;
9. mutation/read-back receipts;
10. verifier/alternate-path evidence;
11. completion state;
12. rollback target;
13. unresolved obligations/blockers;
14. concise decision-focused final result.

## 21. Package files

Required canonical files:

- `SKILL.md`
- `skillpack.json`
- `runtime-state.schema.json`
- `SOURCE-MATRIX.md`
- `EVALS.md`
- `VERIFICATION.md`
- `CHANGELOG.md`

The catalog entry remains `skills/02-skills-catalog.md`.

## 22. v0.3 completion gate

`PACKAGED` requires:

- all seven required package files physically present;
- parseable JSON / JSON Schema;
- **47 unique module IDs**;
- A01–A10 exact unique role identities;
- E0–E6 exactly once;
- T01–T50 eval contract present;
- catalog points to this same canonical package/version;
- no competing efficiency alias.

`GITHUB_COMMITTED` requires an exact commit/ref receipt.

`GITHUB_READ_BACK_VERIFIED` requires exact-ref read-back of the committed artifacts and version/identity/count checks.

`HOST_LIVE` requires the target host/runtime to load/invoke **this exact version** and an owning-runtime postcondition.

`HEALTHY` requires repeated regression/recovery evidence.

Never promote beyond the strongest observed evidence.
