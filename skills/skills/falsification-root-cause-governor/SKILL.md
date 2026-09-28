---
name: falsification-root-cause-governor
description: Use when a repair, diagnosis, reliability or performance task risks being declared successful from a workaround, feature reduction, cherry-picked passing runs, confirmation-only evidence, or a source claim that has not been bound to the target runtime.
---

# Falsification Root-Cause Governor

Version: `0.1.0-rc1`

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Objective

Protect the user's terminal outcome by rejecting fake fixes and forcing a causal, counterexample-aware verification loop.

## Logic contract

- A valid in-scope reproducible counterexample refutes a universal success claim.
- One counterexample does not by itself refute a probabilistic claim such as "95% succeeds"; measure the rate.
- A few successes do not erase a known intermittent failure distribution.
- `MITIGATION != ROOT_CAUSE_FIX`.
- `WORKAROUND != REPAIR`.
- `FEATURE_REDUCTION != SUCCESS` unless the user explicitly authorized that tradeoff.
- `CONFIGURED != RUNTIME_EFFECTIVE`.
- `OFFICIAL_UNSUPPORTED != EMPIRICALLY_IMPOSSIBLE`.
- `COMMUNITY_CONSENSUS != TARGET_RUNTIME_PROOF`.
- `SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`.

## Workflow

1. Lock PRIMARY_TASK, DESIRED_END_STATE, protected capabilities and forbidden fake fixes.
2. Preserve and reproduce a representative failure when practical.
3. Capture baseline frequency, timing, environment and owning-runtime evidence.
4. Build materially distinct causal hypotheses.
5. For each hypothesis, specify a discriminating prediction and cheapest test.
6. Use third-party operational evidence to discover mechanisms, preferring reproducible issues/code/benchmarks and independent reports; de-duplicate shared upstream sources.
7. Test whether external evidence matches the target environment before applying the recipe.
8. Repair the smallest correct causal owner, not the most visible symptom.
9. Read back the loaded/runtime state.
10. Re-run the original failure, negative controls, adjacent regression and stress/metamorphic cases as appropriate.
11. If a valid in-scope counterexample remains, revoke the completion claim and update the causal model.
12. Keep mitigations explicit and separate until the root cause is closed.

## High-value techniques

Use only when they discriminate a live hypothesis or protect a required invariant:

- property-based testing + shrinking;
- stateful invariant testing;
- metamorphic testing;
- differential testing;
- binary search / delta debugging;
- record/replay;
- tracing, profiling, flame graphs, eBPF;
- fault injection / chaos experiments;
- negative controls;
- safe AB/ABAB rollback confirmation;
- canary + rollback;
- repeated-trial failure-rate measurement.

## Intermittent-failure gate

If the pre-fix failure probability is approximately `p0` and trials are reasonably independent/stationary, an all-pass run length

`N >= ceil(log(alpha) / log(1 - p0))`

can be used as a planning aid to make persistence of the old rate less compatible with the observations at significance level `alpha`.

Do not use this formula when independence/stationarity is implausible without stratifying or redesigning the test.

## Source policy

For operational failure modes, prefer:

1. target-bound traces/reproduction;
2. exact third-party code/issues/PRs/benchmarks with repro detail;
3. multiple independent practitioner reproductions;
4. official documentation for normative support/configuration semantics.

Official material is neither ignored nor treated as a universal veto. Third-party material is neither dismissed nor promoted to target proof without reproduction.

## Completion states

Only return `ROOT_CAUSE_FIX_VERIFIED` when the causal mechanism, runtime state, original failure, repeated/stress behavior and protected regressions are all adequately verified.

Otherwise return one of:

- `MITIGATED_NOT_FIXED`;
- `HYPOTHESIS_ONLY`;
- `PARTIALLY_VERIFIED`;
- `COUNTEREXAMPLE_REMAINS`;
- `UNRESOLVED_WITH_EVIDENCE_GAP`.

## Failure modes

- limiting tabs/concurrency/features and calling it fixed;
- retrying until one pass;
- treating two successes as proof against an intermittent baseline;
- applying the first web recipe found;
- counting mirrors/copy-posts as independent corroboration;
- converting "unsupported" into "impossible";
- solving the example instead of the user's actual task;
- averaging away a hard failure;
- adding wrapper/guardrail layers instead of repairing the owner;
- claiming completion from file/config state without runtime read-back.
