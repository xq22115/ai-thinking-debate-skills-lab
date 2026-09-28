---
name: falsification-root-cause-governor
description: Use when debugging, repair, performance, reliability, connectivity, tool/runtime mismatch, or repeated failure can be falsely declared fixed by limiting workload, masking symptoms, cherry-picking successes, or applying single-source recipes.
---

# Falsification Root-Cause Governor

The objective is not to make the symptom disappear once. The objective is to identify and repair the causal mechanism while preserving the user's intended capability.

## Hard invariants

- `MITIGATION != ROOT_CAUSE_FIX`.
- `WORKAROUND != REPAIR`.
- `FEWER_FEATURES != SUCCESS` unless the user explicitly authorizes that tradeoff.
- `ONE_PASS != FIXED`.
- `FEW_PASSES != EVIDENCE_AGAINST_REPEATED_FAILURES`.
- `RETRY_UNTIL_PASS != VERIFICATION`.
- `CONFIG_WRITTEN != RUNTIME_EFFECTIVE`.
- `OFFICIAL_UNSUPPORTED != EMPIRICALLY_IMPOSSIBLE`.
- `POPULAR_RECIPE != TARGET_BOUND_PROOF`.
- `SOURCE_COUNT != INDEPENDENT_CORROBORATION`.
- `SYMPTOM_DISAPPEARANCE != CAUSAL_CLOSURE`.

A reproducible in-scope counterexample vetoes any universal claim such as "fixed", "always works", or "no longer fails". A counterexample outside the declared scope does not automatically refute a scoped claim. For probabilistic claims such as "usually works", estimate failure rate instead of using universal logic.

## Goal lock before diagnosis

Record:

- PRIMARY_TASK;
- DESIRED_END_STATE;
- protected capabilities that must not regress;
- forbidden fake fixes: feature reduction, arbitrary caps, retries, masking, disabling, bypassing, or extra guardrails unless explicitly accepted;
- observable acceptance criteria;
- rollback point.

Examples supplied by the user are evidence about logic, not permission to redefine the task around the example.

## Failure-first evidence

Before modifying the system:

1. reproduce at least one representative failure when practical;
2. preserve the failing input/state/trace;
3. capture baseline frequency, timing, resource and environment evidence when relevant;
4. identify the earliest layer where observed state diverges from expected state;
5. distinguish deterministic, intermittent and environment-dependent failures.

Do not delete, hide or average away failure evidence because a later run succeeds.

## Competing causal hypotheses

For every serious candidate root cause, require:

- predicted observation if true;
- predicted observation if false;
- cheapest discriminating test;
- affected layer/component;
- expected repair mechanism;
- expected regression surface.

A cause that predicts nothing testable remains a hypothesis.

Prefer interventions that change the suspected cause while holding other variables stable. Use binary search, delta debugging, differential comparison, record/replay, tracing, profiling, fault injection, invariant testing or controlled perturbation when they reduce ambiguity.

## Third-party-first operational evidence

For operational behavior and failure modes, prefer reproducible third-party engineering evidence over marketing/support-language authority:

1. exact code, issue, PR, benchmark, trace or reproducer;
2. independent practitioner/tooling reports with enough detail to reproduce;
3. multiple independent reports pointing to the same mechanism;
4. official documentation for normative support/status and configuration semantics.

Do not treat official documentation as runtime proof or as a veto on observed working behavior. Do not treat community reports as target-runtime proof either.

For an actionable non-trivial repair discovered online, target at least three independent evidence families when practical, or two strong independent third-party sources plus target-local reproduction. Mirrors, copied posts and articles sharing one upstream source count as one family.

## Search-test-repair loop

1. lock goal and anti-goals;
2. reproduce and baseline;
3. collect owning-runtime evidence;
4. form competing causal hypotheses;
5. search multiple independent third-party evidence families if the cause is uncertain;
6. run discriminating tests before applying recipes;
7. patch the smallest correct causal owner, not the most visible symptom;
8. read back loaded/runtime state, not only files or commands;
9. run target, negative, adjacent-regression and stress/metamorphic checks;
10. if any valid in-scope counterexample remains, revoke the completion claim and update the causal model.

Online research and local execution should alternate when each can change the next action. Do not "find one fix, apply one fix" without checking whether the evidence matches the actual mechanism.

## Intermittent failures

Do not use two or three successful trials to erase an intermittent baseline.

If the pre-fix failure probability is approximately `p0` and trials are reasonably independent/stationary, an all-pass run length of

`N >= ceil(log(alpha) / log(1 - p0))`

makes persistence of the old failure rate less compatible with the observations at significance level `alpha`. Treat this only as a planning aid; non-independent or drifting systems require stronger design, stratification, or longer observation.

Always report pre/post counts and conditions, not only "passed".

## Advanced verification patterns

Use when materially useful:

- property-based testing and shrinking to find minimal counterexamples;
- stateful invariant testing across action sequences;
- metamorphic testing where no complete oracle exists;
- differential testing across versions/accounts/surfaces;
- negative controls and placebo changes;
- binary search / delta debugging over commits, config or inputs;
- record/replay for nondeterministic execution;
- traces, flame graphs, eBPF/profilers for hidden latency/resource paths;
- fault injection / chaos experiments for resilience hypotheses;
- A/B or ABAB rollback confirmation when safe;
- canary plus rollback for effectful changes.

Do not add techniques for ceremony. Each technique must discriminate a live hypothesis or verify a protected invariant.

## Forbidden completion shortcuts

Never close as fixed solely because:

- a limit/cap reduced the symptom;
- a feature was disabled;
- load was reduced;
- retries eventually passed;
- one or two runs succeeded;
- an official page says unsupported;
- one forum/GitHub answer suggested a workaround;
- aggregate averages improved while a hard failure remains;
- the config file contains the intended value;
- a tool returned success without the target postcondition.

Allowed temporary mitigations must be labeled `MITIGATION`, include the capability/tradeoff cost, and remain separate from the root-cause repair.

## Completion gate

Return `ROOT_CAUSE_FIX_VERIFIED` only when all material gates pass:

- baseline failure was characterized or explicitly marked not reproducible;
- selected cause has discriminating evidence;
- the change acts on the causal mechanism;
- runtime read-back proves the intended revision/state is loaded;
- the original failure no longer reproduces under a justified repeated/stress plan;
- no valid in-scope counterexample remains in the executed test set;
- protected adjacent capabilities did not regress;
- workaround/capability-reduction was not silently substituted for success;
- unresolved unknowns are explicit.

Otherwise return one of: `MITIGATED_NOT_FIXED`, `HYPOTHESIS_ONLY`, `PARTIALLY_VERIFIED`, `COUNTEREXAMPLE_REMAINS`, or `UNRESOLVED_WITH_EVIDENCE_GAP`.

Read `../../references/falsification-root-cause-field-practice.md` for external technique anchors.
