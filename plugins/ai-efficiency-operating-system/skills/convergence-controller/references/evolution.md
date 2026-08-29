# Skill evolution and convergence

Machine contracts: `../../../contracts/research-integrity.json`, `../../../contracts/skill-composition.json`, and `../../../contracts/validation-policy.json`.

## Whole-folder ownership

A skill failure may live in prose, a helper script, reference data, routing metadata, host adapter or packaging. Do not force every defect into more instructions.

A candidate change may atomically update the whole skill folder, but the evaluation surface remains independent.

## Promotion protocol

`failure trace → baseline/failing case → bounded candidate change → target set → protection set → holdout → full regression → independent review → PROMOTE | HOLD | REJECT → rollback reference`

Keep a persistent decision history in Git issues/commits/PRs or another auditable store when available.

## Bounded evolution

Treat a skill update like a controlled training step rather than unconstrained rewriting:

- define an edit budget for the round: which semantic owner/files may change and how much;
- prefer small add/delete/replace deltas that address the earliest causal failure;
- require strict improvement on the held-out acceptance metric before promotion;
- retain rejected edits with their failure reason so later rounds do not rediscover the same bad mutation;
- allow slower/meta updates only after repeated evidence shows the current skill structure itself is the bottleneck;
- never optimize directly against hidden/gold answers embedded in the model-facing skill.

A larger skill is not progress. If the same behavior can be preserved with less trigger overlap/context cost, prefer the leaner owner.

## No-skill / matched-reference attribution

A candidate skill is not promoted merely because a with-skill run looks good. Compare it with a no-skill or semantically matched reference under the same task slice and host/model/version envelope. Measure both functional outcome and efficiency/cost.

Reject or adapt when:

- hard-negative cases regress;
- host/model/version compatibility is absent;
- excessive verification or implementation ceremony lowers useful outcome;
- the candidate only improves a proxy while protected behavior worsens.

This prevents aggregate benchmark gains from turning into universal activation.

## Shadow before observed-target promotion

Known-outcome/synthetic controls are valuable for proving the control plane, but classify them `SIMULATED_CONTROL`. They may reach `SHADOW_ONLY`, never full promotion.

`PROMOTED` requires `OBSERVED_TARGET` evidence plus non-regression on quality success, false completion and source violations, and at least one measured efficiency/cost gain. No measured gain returns HOLD.

## Noise control

Do not market movement inside an evaluation noise band as improvement. Preserve judge disagreement and position-bias diagnostics where semantic graders are used. Deterministic checks should remain provider-free whenever possible.

## Coverage-aware convergence

The old rule “two no-progress fingerprints → pivot” remains a route-change trigger, not a universal stop condition.

Before optional review can stop:

1. material semantic changes have advanced `surface_epoch`;
2. every mandatory lens has reviewed the current epoch;
3. required broad regression is bound to the exact current artifact hash;
4. no unresolved CRITICAL/HIGH finding can change acceptance.

Only then may low marginal utility or repeated no-delta rounds stop optional review. This prevents a late CRITICAL result from being skipped after two low-yield rounds.

## Convergence rules

- no-progress fingerprint repeated twice → change route/layer or stop only if coverage-aware conditions also allow stop;
- new post-freeze gates require controller/user authority;
- one failed tool/provider path does not redefine the goal;
- repeated infrastructure failure is not evidence the underlying skill logic is wrong;
- aggregate benchmark gain does not justify universal activation when hard-negative/task slices regress;
- prefer deleting redundant guidance when a leaner owner passes the same target/protection/holdout cases;
- integration/stateful evals must isolate trials when shared process state can contaminate later verdicts;
- the validator itself needs planted/known-outcome or mutation tests capable of demonstrating that bad states are rejected.
