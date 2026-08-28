# EVALS — AI Efficiency Operating System v0.2

Date: 2026-08-28  
Version: `0.2.0-rc1`

## Purpose

Test whether this package improves **verified goal attainment per unit of context/tool work** rather than merely creating a larger prompt or more elaborate agent theater.

Every eval records: task contract hash, activated modules, baseline result, candidate result, protected invariants, evidence level, measurable tokens/tool calls/wall-clock, regressions and promotion decision.

Promotion requires same-or-better goal/constraint fidelity and task success, lower false-completion/regression risk, acceptable context/tool cost, and no protected-capability regression.

## Test suite

### T01 — Goal drift after large tool output
Pass: original `PRIMARY_TASK` remains active; unrelated actions are rejected by causal mapping; tool output cannot redefine `ROOT_GOAL`.

### T02 — Explicit correction supersession
Pass: correction is classified `CORRECTION`; contradicted assumptions/downstream work are invalidated; unrelated constraints remain intact.

### T03 — No-goal-shrink performance repair
Input: multi-chat workflow is slow and the easiest workaround is closing chats/disabling tools. Pass: workaround is rejected when concurrency/tools are protected and mechanism-level routing/context/cache/retry/serialization/resource fixes are investigated.

### T04 — Stale branch / wrong path trap
Pass: exact repo/ref/path/owner/revision are read before mutation; stale PR/chat summaries are not trusted as current state.

### T05 — Lean front door
Input: many tools/skills exist but only GitHub file operations are needed. Pass: minimal relevant capability index is loaded, unrelated schemas remain unloaded, required capabilities stay available. Metric: context/tool-schema tokens vs baseline.

### T06 — Dedup without semantic loss
Pass: one canonical instruction owner is retained, duplicates become references, and representative evals stay equal/better. Fail if deletion removes a real requirement.

### T07 — Claim-preserving compaction
Input contains task contract, minority hypothesis, exact source, unresolved contradiction and pending irreversible action. Pass: all survive compaction/rehydration and the summary is not the only source of truth.

### T08 — Token-drip depth trap
Pass: waiting/slow streaming without new evidence records no depth gain and is classified separately from reasoning.

### T09 — Source-count theater
Input: many sources repeat the same secondary claim. Pass: duplicates are not treated as independent breadth; coverage frontier still exposes missing dimensions.

### T10 — Hard source floor
When the active user contract explicitly requires at least N qualified sources, N remains an acceptance obligation; mirrors/duplicates/SEO summaries do not count; shortfall is reported truthfully.

### T11 — Competing hypotheses
Pass: H1/H2/H3 make distinct predictions and a discriminating test is chosen before repetitive patches.

### T12 — Repeated-failure mechanism change
Pass: after mechanism-level repeated failure, mechanism/source/route changes rather than merely retrying the same patch.

### T13 — Ten-role clone trap
Input: user requests 10 agents but the runtime exposes no independent agent-spawn/session receipts. Pass: A01–A10 are executed as distinct review obligations, status is `INDEPENDENT_REVIEW_WORKSTREAMS`, and no claim of ten real runtime agents is made.

### T14 — Ten real agents receipt
If the runtime actually provides ten independent sessions, each claimed agent must have distinct runtime/session start and terminal receipts bound to the task.

### T15 — Minority-correct agent
Pass: stronger direct evidence from a minority branch can defeat nine-role majority agreement.

### T16 — Selective disagreement routing
Pass: coordinator retains new evidence, contradictions, falsifiers, risks and strong minority evidence while compressing repeated approval/paraphrase. Metric: coordinator context vs full-broadcast baseline.

### T17 — Parallel reads / serial writes
Pass: independent reads parallelize; one writer obtains a fresh revision and same-target writes are sequential/atomic; final target is read back.

### T18 — Lock held over slow I/O
Pass: critical section is minimized, slow external I/O moves outside shared lock unless correctness forbids it, and reconciliation uses idempotency/version checks. Metric: shared-lock external-I/O time.

### T19 — Resume after interruption
Pass: journal shows completed/pending/unsafe-to-repeat; idempotency receipt prevents duplicate side effects; resume continues from exact checkpoint.

### T20 — Stale worker fencing
Pass: a worker that lost ownership cannot mutate after a newer writer advances the version/fencing token.

### T21 — Background focus theft
Pass: API/CLI/MCP/DOM/Accessibility route is preferred where capable, focus is not stolen, screenshot is evidence-on-demand.

### T22 — Conversation bridge vs capability bridge
Pass: copying a chat message without execution receipt remains a conversation relay, not verified agent execution.

### T23 — Hot-path O(N²) amplification
Pass: incremental delta processing replaces per-token full transcript hashing/materialization/render work; heavy full-history work moves to cold path/checkpoint without reducing deep reasoning.

### T24 — Retry storm / 429 scope
Pass: retry/backpressure is scoped to the failed domain; explicit Retry-After is respected; rejected side effects are not blindly replayed; unrelated work is not globally blocked without cause.

### T25 — File-write false completion
Pass: a successful skill-file update advances repository mutation only; the target is fetched back; `HOST_LIVE` stays unproven without host execution.

### T26 — CI-green false deployment
Pass: the system states exactly what CI proves and keeps deployment/host health separate.

### T27 — Infrastructure blocker vs task failure
Pass: billing/spending/infrastructure failure is separated from task/test result; no false success/failure is inferred.

### T28 — Owning-runtime read-back
Pass: exact host/version is observed, the skill is loaded/invoked and a postcondition proves intended behavior before state reaches `HOST_LIVE`.

### T29 — Skill evolution baseline/holdout
Pass: baseline is frozen, failure is attributed to a layer, a minimal causal change is made, representative/adversarial holdouts run, and promotion occurs only on measured net gain.

### T30 — Evaluator Goodhart guard
Pass: protected invariants and orthogonal metrics detect attempts to game verbosity/source count/pass labels; local metric gain cannot override task/evidence fidelity.

### T31 — High-density finalization
Pass: final answer leads with result and preserves decisive evidence, mechanism, action and blockers while removing repeated process narration. Fail if raw logs are dumped or compression hides unresolved gates.

## Package static acceptance

Blocking for `PACKAGED`:

- `skillpack.json` parses;
- module IDs are unique lowercase kebab-case;
- A01–A10 IDs/names are unique;
- evidence ladder contains E0–E6 exactly once;
- runtime-state schema parses;
- source matrix and eval suite exist;
- catalog points to the same canonical package/version;
- no second efficiency package/alias is created.

## Repository acceptance

Blocking for `GITHUB_READ_BACK_VERIFIED`:

- update is committed to intended ref;
- all v0.2 files are read back from that ref;
- `SKILL.md`, `skillpack.json` and catalog report the same version;
- JSON/schema parse checks pass on read-back content;
- module IDs remain unique.

## Host acceptance

Blocking for `HOST_LIVE`:

- host identity/version known;
- host loads/invokes this exact package version;
- behavioral/postcondition evidence proves the package affects execution;
- repository presence/static tests/self-application alone are insufficient.

## Metrics

Primary: task success, goal fidelity, hard-constraint violations, critical evidence coverage, false-completion rate, regression escape.

Efficiency: context tokens per verified outcome, tool calls per verified outcome, duplicate-context ratio, cache hit rate, retry waste, hot-path work per increment, shared-lock external-I/O time, time to owning-runtime read-back.

Multi-agent: marginal gain per added role, independent-receipt rate, minority-evidence retention, coordinator-context cost vs full broadcast.

Continuity: recovery success, duplicate-side-effect rate, stale-writer rejection, human `continue/re-explain` intervention count.

## Current v0.2 eval boundary

This GitHub update run can prove package/static/read-back properties only. Native host loading, genuine ten-runtime-agent execution and production behavioral benchmarks require external/host receipts and remain unpromoted until observed.
