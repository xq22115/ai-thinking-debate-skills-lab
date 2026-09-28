---
name: root-cause-falsification
description: Enforce goal fidelity, mechanism-level repair, counterexample-first verification, anti-success-mining, and independent real-world evidence. Use for debugging, repair, optimization, capability claims, flaky behavior, performance problems, repeated workarounds, or any task where a few successes could hide real failures.
---

# Root Cause Falsification

Version: `1.1.0`

## Core invariants

- `EXAMPLE != REQUIREMENT`: numbers, tools, commands, and scenarios offered as examples do not become constraints unless the user makes them normative.
- `TRIGGER != ROOT_CAUSE`: a condition that exposes a defect is not automatically the mechanism that owns it.
- `MITIGATION != FIX`: caps, throttles, disabling features, reducing concurrency, reducing quality, warnings, watchdogs, or avoiding the trigger do not count as a root fix unless they remove the owning mechanism.
- `ONE_REPRODUCIBLE_IN_SCOPE_COUNTEREXAMPLE => UNIVERSAL_PASS_FALSE`: one real in-scope failure falsifies a zero-failure claim such as “fixed”, “always works”, or “correct for all accepted cases”.
- `SUCCESS_SAMPLE != SUCCESS_UNIVERSE`: never cherry-pick successful runs, stop after the first success, or discard failures from the verification denominator.
- `OFFICIAL_SUPPORT != REAL_WORLD_EFFECT`: official/canonical material owns supported syntax, contracts, versions, limits, and lifecycle; practical quality and reliability require target-runtime and independent field evidence.
- `FILE_CHANGED != BEHAVIOR_FIXED`; `FAILED_ROUTE != GOAL_IMPOSSIBLE`.

## 1. Goal lock before diagnosis

Compile:
- ROOT_GOAL and DESIRED_END_STATE;
- PROTECTED_CAPABILITIES and NEGATIONS;
- TARGET_IDENTITY and current environment;
- ACCEPTANCE_TESTS and explicit FALSIFIERS;
- examples/distractors separated from requirements;
- nearest easier wrong task that must not replace the goal.

Route, tool, architecture, and hypothesis may change aggressively. The goal may not drift because one example is concrete or one blocker is convenient.

## 2. Causal trace before mutation

Build the smallest useful chain:

`symptom -> exposing condition -> mechanism -> owning layer -> intervention -> predicted state change -> observable test -> falsifier`.

A proposed change is not a repair candidate until it names the mechanism and explains why the owning layer should change. Prefer one discriminating probe over many speculative edits.

Classify every proposed change:
- `ROOT_FIX`: changes or removes the causal mechanism at its owning layer.
- `MITIGATION`: lowers exposure or impact without removing the mechanism.
- `GUARDRAIL`: prevents a triggering condition.
- `WORKAROUND`: routes around the defective path.
- `DEGRADATION`: reduces a requested capability, quality, concurrency, scale, or workflow.

Only `ROOT_FIX` may settle a “fix the problem” task as fixed. Other classes are explicitly temporary unless the user requested that tradeoff.

## 3. Evidence routing by claim type

For contract facts, use the current owning/canonical source first: exact API, schema, version, supported option, hard limit, lifecycle, or owner-controlled semantics.

For practical behavior and repair quality, prioritize:
1. actual target-runtime reproduction/read-back;
2. independent reproducible implementations or experiments;
3. issue/PR/commit evidence exposing real failure mechanisms;
4. independent postmortems and long-term production reports;
5. benchmarks with inspectable harnesses and matched target conditions;
6. current maintainers/engineers with directly relevant artifacts;
7. official documentation for declared support boundaries.

A single anecdote is a lead, not a verdict. Collapse forks, copied recipes, same-project statements, and derivative reports into one lineage. Multiple independent sources pointing to the same mechanism increase priority; popularity alone does not.

## 4. Search-test-update loop

Never use “find one web answer -> patch immediately” as the default loop.

Use:
`observe locally -> generate competing hypotheses -> search independent evidence -> qualify lineage/scope/version -> run the cheapest discriminating local test -> update hypothesis -> mutate -> read back -> falsify -> regress`.

External evidence proposes or reprioritizes hypotheses. The target environment settles whether the mechanism applies here.

## 5. Falsification-dominant verification

Before observing post-fix results, predeclare the verification matrix: scope, trial count/window, relevant environment variants, protected capabilities, success metric, and failure condition.

Then:
1. replay the original failure first;
2. preserve every in-scope failure and reduce it to the smallest reproducible case when practical;
3. run the same acceptance path across the declared matrix;
4. count all in-scope runs, not only successful ones;
5. run at least one negative/adversarial/nearby-regression test;
6. compare before/after behavior when a baseline exists;
7. read back the owning runtime/state, not only configuration.

For deterministic/universal claims, any reproducible in-scope counterexample blocks `PASS`.

For probabilistic/SLO claims, do not misuse one failure as proof that an explicitly nonzero error budget failed. Instead evaluate the declared rate/latency/reliability threshold and confidence window. The same failure still disproves stronger wording such as “never fails”.

Previously failing cases become permanent regression cases until scope/version invalidates them. This mirrors property-based testing practice: failures are saved, replayed, and minimized rather than ignored because later random examples pass.

## 6. Anti-success-mining gate

Forbidden:
- stop verification after first success;
- select a “good” time window after seeing results;
- exclude failures without a predeclared scope reason;
- replace a failed user path with an easier proxy test;
- call intermittent success “fixed” while the original failure remains reproducible;
- compare different environments or loads and attribute the difference to the patch.

If results are flaky, report the full observed distribution and keep status below `ROOT_FIX_VERIFIED` until the acceptance contract is actually met.

## 7. Escalation and architecture reset

After two materially similar no-delta failures, change a major dimension: causal hypothesis, diagnostic instrument, evidence family, execution layer, architecture, or verification method.

After three repair attempts that merely move the symptom or create new guardrails, question the architecture rather than stacking another patch.

Prefer deleting obsolete mitigations once the root fix is verified. Net complexity should fall or remain justified.

## 8. Advanced discriminating techniques

Use advanced techniques only when they distinguish a live causal hypothesis or verify a protected invariant:

- **property-based testing + shrinking** — generate broad inputs and reduce failures to minimal counterexamples;
- **stateful invariant testing** — test properties across action sequences, not one happy path;
- **metamorphic testing** — verify expected relations when a complete oracle is unavailable;
- **differential testing** — compare versions/accounts/surfaces/implementations under matched inputs;
- **binary search / delta debugging** — isolate the smallest commit/config/input delta that flips the behavior;
- **record/replay** — turn nondeterministic failures into inspectable repeatable evidence when supported;
- **tracing / profiling / flame graphs / eBPF** — locate hidden latency, resource, lock, or execution-path concentration;
- **fault injection / chaos experiments** — deliberately perturb assumptions when safe to test resilience hypotheses;
- **negative controls / placebo changes** — detect false causal attribution;
- **A/B or ABAB rollback confirmation** — verify that the suspected intervention repeatedly moves the outcome while other variables stay controlled;
- **canary + rollback** — limit blast radius while measuring the real effect of an effectful change.

Do not add these techniques ceremonially. Every technique must have a named hypothesis, predicted observation, falsifier, and acceptance obligation.

### Intermittent-failure planning

A few passing trials never erase a known intermittent baseline.

If the pre-fix failure probability is approximately `p0`, trials are reasonably independent/stationary, and the intended false-negative risk is `alpha`, an all-pass planning length may use:

`N >= ceil(log(alpha) / log(1 - p0))`.

This is only a planning aid, not a universal proof formula. If independence/stationarity is implausible, stratify by environment/state/load or redesign the experiment. Always retain and report the pre/post trial counts, failure counts, conditions, and confidence limitations.

Field-practice anchors: `../../plugins/ai-efficiency-operating-system/references/root-cause-falsification-field-practice.md`.

## 8. Deterministic receipt gate

When a material repair or completion claim can be represented as structured evidence, adjudicate it with:

`control-plane/scripts/evaluate_root_cause_falsification_receipt.py <receipt.json>`.

The evaluator is deliberately narrower than model reasoning. It does not discover the root cause; it prevents a completed repair from being overstated after the evidence exists. In particular it deterministically blocks universal PASS when a reproducible in-scope counterexample remains, downgrades guardrail/workaround/degradation changes to `MITIGATION_ONLY`, requires predeclared/all-counted verification and original-failure replay, and separates probabilistic SLO claims from universal zero-failure claims.

## 9. Completion states

Use only:
- `ROOT_CAUSE_PROVEN`
- `ROOT_FIX_VERIFIED`
- `MITIGATION_ONLY`
- `PARTIAL`
- `CONTESTED`
- `BLOCKED`
- `FAIL`

`ROOT_FIX_VERIFIED` requires: original goal preserved, mechanism-level change demonstrated, original failure no longer reproducible inside the declared acceptance scope, protected capability not degraded, adversarial/regression checks passed, and no reproducible in-scope counterexample remains.

Do not expose private chain-of-thought. Report the goal, competing hypotheses that mattered, evidence, causal mechanism, change class, tests, counterexamples, and remaining uncertainty.