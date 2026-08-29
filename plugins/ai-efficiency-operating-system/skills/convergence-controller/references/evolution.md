# Skill evolution and convergence

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

## Noise control

Do not market movement inside an evaluation noise band as improvement. Preserve judge disagreement and position-bias diagnostics where semantic graders are used. Deterministic checks should remain provider-free whenever possible.

## Convergence rules

- no-progress fingerprint repeated twice → change route/layer or stop;
- new post-freeze gates require controller/user authority;
- one failed tool/provider path does not redefine the goal;
- repeated infrastructure failure is not evidence the underlying skill logic is wrong;
- aggregate benchmark gain does not justify universal activation when hard-negative/task slices regress;
- prefer deleting redundant guidance when a leaner owner passes the same target/protection/holdout cases.
