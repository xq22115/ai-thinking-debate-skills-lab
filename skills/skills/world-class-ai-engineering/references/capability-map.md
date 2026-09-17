# Capability Map — World-Class AI Engineering

This reference maps recurring AI-engineering failure modes to the engineering capability required to close them. It is intentionally outcome-focused: a technique counts only when it changes evidence, behavior, or a falsifiable decision.

## 1. Goal / acceptance engineering

**Failure signals**
- visible symptom repaired while the actual outcome is still missing;
- one sub-requirement passes and silently substitutes for the whole task;
- tests become the goal instead of measuring the goal.

**Required capability**
- explicit root goal, protected capabilities, hard constraints, non-goals, and falsifiable acceptance criteria;
- criterion ledger with `UNSATISFIED → SATISFIED|BLOCKED|FAIL` transitions bound to evidence.

**Proof**
- reverse walk from final claim → acceptance test → current evidence → exact state/revision.

## 2. Current-source and version forensics

**Failure signals**
- outdated APIs, stale docs, search-index misses, release/HEAD/blob confusion;
- retrying different search words against the same index and treating no result as absence.

**Required capability**
- exact-object lookup, source/release/commit/issue triangulation, freshness windows, invalidation triggers;
- keep repository HEAD, file blob, package version, marketplace version, installed revision, and runtime version separate.

**Proof**
- exact identifiers recorded and a current direct fetch/read-back succeeds.

## 3. AI system architecture

**Failure signals**
- model, tool, memory, runtime, UI, and persistence logic tangled into one loop;
- no clear boundary for side effects or recovery.

**Required capability**
- separate planner/model decisions from deterministic execution;
- isolate effectful tools, persistence, evaluator, and policy boundaries;
- define stable contracts so internals can change without breaking consumers.

**Proof**
- failure can be localized to a layer; each component has an inspectable contract and test surface.

## 4. Tool / MCP contract engineering

**Failure signals**
- schema drift, namespace collision, wrong argument shape, tool poisoning, silent partial execution;
- configured connector mistaken for usable runtime capability.

**Required capability**
- discovery → schema resolution → authorization → invocation preflight → execution → postcondition read-back;
- distinguish visibility, authorization, registration, load, execution, and observable effect.

**2026 delta**
- MCP `2026-07-28` introduces a stateless protocol core, header-based routing (`Mcp-Method`, `Mcp-Name`), cacheable list results, extensions, and authorization hardening. Engineering assumptions built around sticky sessions or body inspection must be revalidated.

**Proof**
- representative live call plus owning-system postcondition evidence.

## 5. Host / account / session identity

**Failure signals**
- correct change applied to the wrong account, clone, workspace, profile, browser session, or runtime;
- two instances appear identical because they share state below the visible UI.

**Required capability**
- stable target identity tuple: host, account, workspace, profile/data directory, session, repository, branch, runtime revision;
- pre-mutation identity probe and post-mutation read-back from the same target.

**Proof**
- target identity is observable before and after the action; adjacent instances remain unchanged.

## 6. Memory / context integrity

**Failure signals**
- stale summaries override current evidence;
- untrusted repository/web/tool content persists into later runs;
- cross-chat or cross-agent contamination.

**Required capability**
- provenance-bearing memory, freshness/expiry, supersede/invalidate semantics, quarantine of unverified content, scoped namespaces;
- treat persistent memory as an attack surface, not a convenience layer.

**Proof**
- poisoned/stale fixture is rejected or isolated; current authoritative evidence wins.

## 7. Durable execution and recovery

**Failure signals**
- task disappears after interruption;
- retry duplicates side effects;
- resume restarts too much work or uses stale prerequisites;
- retry storm/backpressure collapse.

**Required capability**
- checkpoints at meaningful boundaries, idempotency keys, effect receipts, retry classification, bounded backoff, compensation/rollback, resume-time revalidation;
- split task-result state from infrastructure state.

**Proof**
- interruption test resumes safely; repeated execution does not duplicate the effect; rollback path is demonstrated.

## 8. Observability and runtime forensics

**Failure signals**
- “slow” or “stuck” agent with no attribution to model, tool, network, retries, UI, disk, or queue;
- successful final text hides failed tool calls or excessive retries.

**Required capability**
- trace/span hierarchy across agent turn, model generation, handoff, tool call, guardrail, external dependency, and effect receipt;
- latency, token, cache, retry, queue, error, and cost metrics with correlation IDs.

**Proof**
- a failure can be traced end-to-end and attributed to a causal layer without guessing.

## 9. Evaluation-driven engineering

**Failure signals**
- demo works once; regressions return later;
- evaluator shares the builder’s assumptions;
- aggregate score improves while hard cases degrade.

**Required capability**
- RED baseline before repair; target/protection/holdout/adversarial slices; independent/fresh-context evaluation when practical;
- failure corpus built from real incidents and prior user corrections;
- exact-revision evaluation.

**Proof**
- baseline fails for the intended reason, repaired state passes, hard slices do not regress.

## 10. GitHub / release reliability

**Failure signals**
- PR created or CI green is reported as completion;
- default branch is written directly without rollback-friendly isolation;
- tests ran on a different commit from the reported one.

**Required capability**
- base SHA → isolated branch → write → read-back → diff → exact-revision tests → CI/runtime check → rollback target.

**Proof**
- commit SHA, changed-file set, read-back bytes, workflow result, and requested behavior all refer to the same revision.

## 11. Computer Use / desktop agent engineering

**Failure signals**
- automation steals focus, moves the physical pointer, acts on the wrong window, or depends on fragile pixels;
- screenshot evidence proves appearance but not state change.

**Required capability**
- prefer semantic/DOM/accessibility/CLI channels; use isolated browser profiles/sessions; bound screenshots to target surface; virtual/background input when supported; explicit focus policy;
- post-action read-back through a stateful channel when available.

**Proof**
- target changes while unrelated foreground activity, other sessions, and physical input remain unaffected.

## 12. Performance and cost engineering without degradation

**Failure signals**
- “optimization” disables features, reduces verification, shrinks context blindly, or serializes useful work;
- latency improves while reliability or answer quality drops.

**Required capability**
- profile first; separate model latency, tool latency, network, queue, I/O, renderer, retry, and context costs;
- exploit caching, parallelism, batching, progressive disclosure, smaller evidence payloads, incremental recomputation, and hot/cold paths before removing capability.

**Proof**
- same acceptance/regression suite passes with improved measured latency/cost/resource use.

## 13. Security and capability boundaries

**Failure signals**
- untrusted content can instruct tools, write memory, or expand privileges;
- broad tool scopes make accidental cross-system actions possible.

**Required capability**
- least-capability tool surfaces, input/output/tool guardrails, scoped credentials, provenance labels, sandboxing, approval at high-impact boundaries, secret-safe telemetry;
- recognize that not every hosted/built-in tool shares the same guardrail pipeline.

**Proof**
- adversarial prompt/tool/memory fixtures cannot cross the declared boundary; legitimate workflows remain intact.

## 14. Multi-agent evidence quality

**Failure signals**
- many role labels but one underlying model/context and one shared blind spot;
- majority vote substitutes for evidence.

**Required capability**
- diversify mechanisms, evidence families, contexts, or execution environments; retain disagreements; use a fresh evaluator; route roles by information gain.

**Proof**
- “independence” is backed by distinct evidence or execution identity, not prose labels; the final decision cites discriminating evidence.

## Minimum competency bar

A world-class AI engineer can answer, for every material claim:

1. What exact layer owns this behavior?
2. What evidence shows the current state?
3. What failure would falsify the hypothesis?
4. What happens on interruption, retry, stale state, wrong identity, and version drift?
5. How do we observe it in production?
6. How do we prove an optimization did not degrade protected behavior?
7. What exact evidence is required before `PASS`?
