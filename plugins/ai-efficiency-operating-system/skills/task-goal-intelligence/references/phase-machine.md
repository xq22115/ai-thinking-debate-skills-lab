# Native Goal Phase Machine

This file is the executable workflow contract behind `task-goal-intelligence`. The top-level `SKILL.md` is a router; this file owns the phase semantics.

## State graph

`ORIENT -> DISCRIMINATE -> COMMIT -> EXECUTE -> VERIFY -> LEARN`

Recovery can interrupt any material phase:

`ORIENT|DISCRIMINATE|COMMIT|EXECUTE|VERIFY -> RECOVER -> nearest still-valid phase`

A user correction can interrupt any phase and returns to `ORIENT` for semantic rebase. Cosmetic restatements do not rewind the state.

## One-way complexity ratchet

Classify the task operating path before material execution:

- `DIRECT`: clear target, reversible action, low coordination, obvious acceptance.
- `INVESTIGATIVE`: ambiguous mechanism/target, current evidence needed, or failure diagnosis required.
- `ARCHITECTURAL`: multi-owner, long-horizon, high coupling, irreversible or broad system effect.

The path may move `DIRECT -> INVESTIGATIVE -> ARCHITECTURAL` when hidden complexity appears. Do not downgrade a live task merely to avoid evidence, coordination, verification, or a blocker. A genuine semantic user scope reduction is a new goal event and may reclassify the path.

## ORIENT

Entry:
- new substantive request;
- material correction;
- stale or contradicted historical state;
- target/runtime/repository/session identity changed.

Required output state:
- root goal;
- desired end state;
- target identity / owning system;
- hard constraints and negations;
- acceptance tests;
- known historical claims labeled current or stale;
- task path classification.

Exit gate:
- no unresolved missing field can silently change target, irreversible action, protected capability, or acceptance boundary.

## DISCRIMINATE

Enter only when plausible interpretations would produce materially different actions or acceptance proofs.

Required behavior:
- preserve the smallest set of consequential candidates;
- identify the observation with highest decision value;
- prefer current tool/runtime/source evidence over broad clarification;
- ask one discriminating question only when available evidence cannot resolve the fork efficiently.

Exit gate:
- remaining ambiguity does not change the next reversible action or acceptance boundary.

## COMMIT

Freeze a route-neutral Goal Contract before material execution.

Commit means:
- the end state and acceptance boundary are stable enough to act;
- the route is replaceable;
- examples, tool names, and implementation suggestions are not promoted to goal requirements without evidence;
- the nearest easier substitute has been explicitly rejected.

Exit gate:
- every planned material action maps to a goal node, decision-critical unknown, or acceptance test.

## EXECUTE

Use the smallest useful specialist bundle. The goal gate stays first; one primary specialist owns the phase; add `evidence-watchdog` when a state/completion claim must be proven.

Progress is not activity. A material step must produce at least one of:
- acceptance delta;
- evidence delta;
- decision-critical uncertainty delta;
- observable state delta.

Two consecutive material no-delta steps force `RECOVER`.

## VERIFY

Fresh evidence is mandatory before a state or completion claim.

Reverse-walk:

`claim -> acceptance test -> owning evidence -> current goal version -> causal path`

Rules:
- prior success prose is not fresh evidence;
- command/tool success is not the requested postcondition;
- agent self-report is not independent verification;
- verification must bind to the current target/revision/session when those dimensions matter;
- a stale or missing link blocks `DONE`.

Possible terminal statuses:
- `DONE`: all hard acceptance tests have current evidence;
- `DONE_WITH_CONCERNS`: acceptance passes but non-veto concerns remain;
- `BLOCKED`: a required acceptance condition cannot currently be advanced and the blocker is concrete;
- `NEEDS_CONTEXT`: only when a decision-critical fact cannot be recovered from available context/tools.

## RECOVER

Recovery changes method, not the root goal.

Enter on:
- a route failure;
- two no-delta material steps;
- a failed verification;
- a contradicted historical claim;
- repeated tool/specialist failure;
- evidence showing the current causal model is wrong.

Recovery sequence:
1. capture the failure fingerprint;
2. identify the first upstream failure;
3. isolate a route-local blocked slice;
4. continue all separable goal-advancing work;
5. select a causally different route/hypothesis/instrument/specialist;
6. return to the nearest still-valid phase.

Three materially distinct failed repairs to the same mechanism promote the task to architectural review rather than a fourth symptom patch.

## LEARN

After a material task, extract only durable learning that would change a future decision:
- a repeated user correction pattern;
- a target-identity trap;
- a false-completion signature;
- a route/tool mismatch;
- a reproducible hidden/rare mechanism;
- a new hard-negative case.

Do not convert one-off noise into a permanent rule. Candidate changes must be tested against target, protection, and holdout slices before promotion.
