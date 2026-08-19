---
name: completion-gate
description: Prevent false completion by requiring evidence for each claimed status. Use before saying a task is implemented, tested, verified, live, deployed, or healthy.
---

# Completion Gate

Version: `0.1.1-rc1`

## Status Vocabulary

Keep these states distinct:

`DRAFTED` → `PACKAGED` → `IMPLEMENTED` → `TESTED` → `REVIEWED` → `VERIFIED` → `HOST_LIVE_VERIFIED` → `DEPLOYED` → `HEALTHY`

Not every task requires every state, but no state may be inferred from an earlier one.

For execution/infrastructure outcomes also preserve:

`PASS | FAIL | BLOCKED | NOT_RUN`

When supported by evidence, refine `BLOCKED` into a cause such as `BILLING_BLOCKED`, `AUTH_BLOCKED`, `PERMISSION_BLOCKED`, `RUNNER_UNAVAILABLE`, or `DEPENDENCY_UNAVAILABLE`.

## Gate

Before terminal completion:

1. Enumerate every critical acceptance criterion.
2. Bind each criterion to concrete evidence from the actual target artifact/environment.
3. Bind change-sensitive evidence to the exact revision, run, job, deployment, or resource being claimed when applicable.
4. Confirm no blocking red-team finding remains open.
5. Confirm no critical unknown was closed without evidence.
6. Check the regression surface appropriate to the change.
7. Verify that tool receipts indicate the required outcome, not merely attempted execution.
8. For mutable host/platform claims, prefer direct backend read-back or a successful target-environment consumer check.
9. Distinguish **task failure** from **execution infrastructure failure**. If a workflow/job never reaches its steps, do not label the underlying tests failed.
10. State the highest status actually proven and stop there.

## Evidence Hierarchy

Prefer, when applicable:

1. direct target/backend read-back or user-visible outcome;
2. exact-revision functional evidence;
3. targeted automated tests on that revision;
4. relevant CI/runtime receipts bound to that revision;
5. static/package/config inspection.

Weaker evidence may support an intermediate state but cannot silently inherit a stronger one.

## Failure Behavior

If evidence is incomplete, return `PARTIAL`, `BLOCKED`, `NOT_RUN`, or the highest proven intermediate status with the exact missing evidence.

If infrastructure is blocked before execution, preserve separable verified artifacts while keeping execution-dependent criteria open.

## Prohibitions

Never convert any of the following into proof of completion by itself:

- confidence;
- verbosity or elapsed effort;
- file creation or commit existence;
- command exit without validating the actual acceptance criterion;
- configuration presence;
- an agent's own declaration;
- a role list presented as proof that independent agents ran;
- `steps=null`/runnerless workflow failure presented as a test failure;
- local deterministic tests presented as provider-live execution.

## Completion Receipt

For consequential work, return:

- criterion;
- status;
- strongest evidence;
- evidence revision/environment;
- unresolved gap;
- highest defensible overall state.
