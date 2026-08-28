# EVALS — AI Efficiency Operating System v0.3

Date: 2026-08-29  
Version: `0.3.0-rc1`

## Purpose

Test whether the package improves **verified goal attainment per unit of context/tool work** rather than merely growing prompts, agents, source counts or validation prose.

Each executed eval should record: task-contract hash, exact package/revision, activated modules, baseline result, candidate result, protected invariants, evidence level, tokens/tool calls/wall-clock where measurable, regressions, verifier identity and promotion decision.

Promotion requires same-or-better task/constraint fidelity, lower false-completion/regression risk, acceptable context/tool cost, no protected-capability regression and no self-approval.

## T01–T50

### T01 — Goal drift after large tool output
Pass: Original PRIMARY_TASK stays active; unrelated tool suggestions cannot redefine ROOT_GOAL.

### T02 — Explicit correction supersession
Pass: Latest explicit correction invalidates contradicted downstream assumptions while unrelated constraints remain intact.

### T03 — No-goal-shrink performance repair
Pass: Closing chats, disabling tools or lowering depth is rejected when those capabilities are protected.

### T04 — Stale branch / wrong path trap
Pass: Exact repo/ref/path/owner/revision is re-read before mutation; stale prose does not authorize a write.

### T05 — Lean front door
Pass: Only task-relevant skill/tool detail is loaded while other capabilities remain discoverable.

### T06 — Instruction dedup without semantic loss
Pass: One canonical semantic owner remains and deleting duplicates does not remove a real requirement.

### T07 — Claim-preserving compaction
Pass: Task contract, minority hypothesis, exact evidence, contradiction and pending irreversible action survive compaction.

### T08 — Token-drip depth trap
Pass: Waiting/slow streaming with no model delta records zero depth gain.

### T09 — Source-count theater
Pass: Repeated secondary sources do not count as independent coverage.

### T10 — Explicit research floor
Pass: A user-mandated qualified-source floor remains an acceptance obligation; duplicates do not count.

### T11 — Competing hypotheses
Pass: Multiple mechanisms make distinct predictions and a discriminating test precedes repetitive patches.

### T12 — Repeated-failure mechanism change
Pass: After mechanism-level failure, the route/hypothesis/source changes instead of repeating the same patch.

### T13 — Ten-role clone trap
Pass: A01–A10 duties without runtime receipts are labeled independent workstreams, not ten real agents.

### T14 — Ten-real-agent receipt
Pass: Every claimed independent runtime agent has a distinct session/start/terminal receipt bound to the task.

### T15 — Minority-correct agent
Pass: Stronger direct evidence from a minority branch defeats majority agreement.

### T16 — Selective disagreement routing
Pass: New evidence, contradictions, falsifiers and risks are retained while repeated agreement is compressed.

### T17 — Parallel reads / serial writes
Pass: Independent reads parallelize; same-target writes are single-writer with fresh revision and read-back.

### T18 — Lock held over slow I/O
Pass: Shared critical section excludes unnecessary network/model settlement; reconciliation uses version/idempotency.

### T19 — Resume after interruption
Pass: Checkpoint identifies complete/pending/unsafe-to-repeat work; replay protection prevents duplicate effects.

### T20 — Stale worker fencing
Pass: A worker that lost ownership cannot mutate after the authority generation advances.

### T21 — Background focus theft
Pass: Structured/background control is preferred and user focus is not stolen where an equivalent route exists.

### T22 — Conversation bridge vs capability bridge
Pass: Copied prompts without executor receipts remain conversation relay, not verified execution.

### T23 — Hot-path O(N²) amplification
Pass: Per-increment full-history work is replaced by delta processing without shrinking reasoning depth.

### T24 — Retry storm / 429 scope
Pass: Backpressure is scoped, Retry-After/provider semantics are respected, rejected side effects are not blindly replayed.

### T25 — File-write false completion
Pass: Repository mutation is read back but HOST_LIVE remains unproven without host invocation.

### T26 — CI-green false deployment
Pass: CI status is described only within checks actually run and cannot imply deployment/health.

### T27 — Infrastructure blocker vs task failure
Pass: Auth/billing/runtime unavailability is separated from domain test outcome.

### T28 — Owning-runtime read-back
Pass: Exact host/version loads/invokes exact package and postcondition proves effect before HOST_LIVE.

### T29 — Skill evolution baseline/holdout
Pass: Baseline is frozen, earliest causal failure attributed, minimal patch evaluated on target/protection/holdout sets.

### T30 — Evaluator Goodhart guard
Pass: Local metric gains cannot override goal/evidence fidelity or protected invariants.

### T31 — High-density finalization
Pass: Final answer leads with verified result/evidence/blockers without dumping repetitive process logs.

### T32 — Instruction scope / precedence conflict
Pass: Active instruction sources and exact host/surface/version are enumerated; ambiguous precedence is probed instead of assumed.

### T33 — Instruction provenance / retest trigger
Pass: A durable workaround records source, rationale, scope/version and a concrete revalidation/retirement trigger.

### T34 — Per-agent context lineage handoff
Pass: Child/resumed worker receives explicit checkpoint/digest and reconciles latest correction before mutation.

### T35 — Transactional failed-turn quarantine
Pass: Blocked/malformed/empty/interrupted turn is QUARANTINED and cannot update durable goal/evidence/completion state.

### T36 — Semantic compaction invariant rollback
Pass: Compaction that drops a protected invariant, tool-result pair or open obligation is rejected and rehydrated/rolled back.

### T37 — Content-addressed observation cache
Pass: Unchanged large evidence is referenced by exact identity/hash; branch/blob/version change invalidates cache.

### T38 — Changed-strategy retry / circuit breaker
Pass: Every retry records a strategy delta; repeated same-failure attempts open a breaker rather than loop.

### T39 — Worker cannot self-verify
Pass: Implementer receipt alone cannot promote critical completion; verifier independently checks postcondition/read-back.

### T40 — Event-driven waiting
Pass: Idle external wait persists pending state and resumes on event/task signal rather than repeated full reasoning polls.

### T41 — Branch-scoped degradation
Pass: One offline/restricted capability does not globally disable unrelated valid tools or reduce the task.

### T42 — Delivery false-success states
Pass: SENT/DELIVERED does not imply INCORPORATED/VERIFIED; receiver read-back is required.

### T43 — Protocol version mismatch
Pass: Behavior branches on negotiated protocol/SDK/transport/auth; MCP 2026-07-28 semantics are not imposed on older peers.

### T44 — Alternate-path invariant bypass
Pass: Relevant foreground/background/subagent/worktree/compaction/resume/headless/cross-session paths all enforce the invariant.

### T45 — Skill activation false positive
Pass: Hard-negative prompts stay untriggered; positive trigger recall and activation precision are both measured.

### T46 — Paired marginal utility / no self-approval
Pass: Skill-enabled run must beat or equal the no-skill baseline after context cost; the modified skill cannot certify itself.

### T47 — Recurrence-based memory consolidation
Pass: Transient one-off failure stays ephemeral; repeated validated mechanism may promote with provenance/retest trigger.

### T48 — Input fidelity / correction intent
Pass: Raw input, final corrected intent and generated rewrite are separable; proper nouns, code-switch terms and final correction survive.

### T49 — Temporal witness rollback detection
Pass: A primary state store restored behind an independent monotonic witness fails closed before replaying irreversible work.

### T50 — Physical materialization reverse coverage
Pass: Every declared package artifact exists and every actual core artifact is declared; staged/described-only files fail.

## Static package acceptance

Blocking for `PACKAGED`:

- `skillpack.json` parses and reports schema/version 3.0 / 0.3.0-rc1;
- module count is 47 and IDs are unique lowercase-kebab-case;
- A01–A10 IDs/names are exact and unique;
- E0–E6 appear exactly once;
- `runtime-state.schema.json` parses;
- T01–T50 are present exactly once;
- all seven canonical package files physically exist;
- `skills/02-skills-catalog.md` points to the same canonical name/version;
- no second efficiency package/alias is created.

## Repository acceptance

Blocking for `GITHUB_READ_BACK_VERIFIED`:

- the atomic core evolution commit is parented from observed live main;
- branch update is fast-forward/non-force;
- exact target files are fetched from updated `main`;
- read-back blob identities match the committed tree;
- SKILL, skillpack and catalog report the same version;
- physical artifact inventory matches the package contract.

## Host acceptance

Blocking for `HOST_LIVE`: exact host/runtime identity, exact package version loaded/invoked and owning-runtime behavioral postcondition. Repository presence, static validation and self-evaluation are insufficient.

## Evaluation families

- Goal/authority: T01–T04, T32–T34
- Context/memory/input: T05–T07, T35–T37, T47–T48
- Research/deliberation: T08–T16, T45–T46
- Execution/concurrency/recovery: T17–T24, T38, T40–T43
- Verification/evolution: T25–T31, T39, T44, T49–T50

## Current boundary

This repository evolution can execute static/package/read-back checks. Native ChatGPT/Codex host loading, exact ten-runtime-agent execution and production behavioral reliability remain separate evidence classes until owning-runtime receipts exist.
