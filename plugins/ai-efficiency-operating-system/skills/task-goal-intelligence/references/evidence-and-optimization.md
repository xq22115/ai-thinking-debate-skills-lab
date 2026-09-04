# Evidence, Verification, and Optimization

## Fresh evidence before claims

Before any claim equivalent to complete/fixed/enabled/installed/connected/invokable/effective/verified:

1. name the owning observation that would prove the claim;
2. obtain that observation in the current target/revision/session when relevant;
3. inspect the actual result, not only an exit code or agent summary;
4. map it to the acceptance test;
5. only then choose a terminal status.

A weaker layer cannot prove a stronger one. Examples:

- package present != host loaded;
- host loaded != skill invoked;
- invoked != effective state change;
- command exit 0 != requested postcondition;
- PR/commit exists != deployment/consumer state;
- agent says PASS != independent evidence.

## Root-cause discipline

For failures, diagnose before patching:

1. reproduce or gather the closest observable failure evidence;
2. trace backward through component/ownership boundaries;
3. identify the first upstream state that becomes wrong;
4. state one falsifiable causal hypothesis;
5. test the smallest discriminating change/observation;
6. repair at the source;
7. re-run the original symptom plus protection tests.

Do not stack speculative fixes. After three materially distinct failed repairs to the same mechanism, promote to architectural review.

## Evidence mesh

Use two complementary pressures:

### Scale lane

Prefer mature implementations, repeated production use, maintained ecosystems, benchmark methodology, and multiple independent reproductions when estimating common reliability.

### Discrimination lane

Actively search rejected/reverted changes, long issue threads, negative results, hidden fixtures, maintained forks, migration failures, obscure design notes, opposite hypotheses, and reproducible edge cases.

Popularity is not correctness; obscurity is not credibility. The useful question is whether an item changes a live decision, causal model, target ranking, or acceptance verdict.

Opaque/anonymous/underground/onion/closed-community signals start as `LEAD`. Preserve provenance and corroboration state before promotion.

## Failure-trace optimizer loop

Treat the skill package as an optimizable program, not sacred prose.

Collect candidate training/eval material from:
- real user corrections;
- target-identity mistakes;
- neighboring-task substitutions;
- unnecessary clarification;
- stale historical claims;
- false completion;
- route-local blocker abandonment;
- progress theater;
- protected-capability regression.

For each failure trace store:
- original Goal Contract;
- relevant trajectory/actions;
- first upstream failure;
- textual failure feedback;
- expected behavior;
- protected slice(s).

Candidate edits may touch the whole skill folder: router, references, scripts, evals, policy metadata. Promotion requires:

- target cases improve;
- protection cases do not regress;
- held-out/adversarial cases improve or remain intact;
- no hard goal-fidelity slice is hidden by aggregate score.

Prefer textual failure feedback and trajectory inspection over adding another generic rule. If the same new rule cannot explain multiple real failures, it is probably overfit.
