# Skill evolution and convergence

## Whole-folder ownership

A skill failure may live in prose, a helper script, reference data, routing metadata, host adapter or packaging. Do not force every defect into more instructions.

A candidate change may atomically update the whole skill folder, but the evaluation surface remains independent.

## Promotion protocol

`failure trace → baseline/failing case → candidate change → target set → protection set → holdout → full regression → independent review → PROMOTE | HOLD | REJECT → rollback reference`

Keep a persistent decision history in Git issues/commits/PRs or another auditable store when available.

## Noise control

Do not market movement inside an evaluation noise band as improvement. Preserve judge disagreement and position-bias diagnostics where semantic graders are used. Deterministic checks should remain provider-free whenever possible.

## Convergence rules

- no-progress fingerprint repeated twice → change route/layer or stop;
- new post-freeze gates require controller/user authority;
- one failed tool/provider path does not redefine the goal;
- repeated infrastructure failure is not evidence the underlying skill logic is wrong;
- prefer deleting redundant guidance when a leaner owner passes the same target/protection/holdout cases.
