# 17 — Executable RC1 Validation Layer

Date: 2026-08-18

## Purpose

Move the project from specification-only artifacts toward executable, evidence-producing validation without overstating what has been tested.

## Components

### `tools/validate_rc1_package.py`

Deterministic static package validator.

Checks:
- required research/governance/eval files exist;
- exactly the nine canonical RC1 skills are present;
- every `SKILL.md` has matching `name` plus non-empty `description` frontmatter;
- key JSON ledgers/fixtures parse successfully;
- STATUS does not contain an unqualified terminal status such as `STABLE`, `DEPLOYED`, `HEALTHY`, or `HOST_LIVE_VERIFIED`;
- cross-chat convergence still names PR #46/#45/#29 and the current billing/spending blocker;
- role activation policy retains escalation/de-escalation/30-role signals.

Output status is limited to:
- `PASS_STATIC`
- `FAIL_STATIC`

It explicitly sets `host_live_verified=false`.

### `evals/run_policy_evals.py`

Executable fail-closed policy test harness.

Current deterministic cases:
1. false completion after file write only;
2. pre-step CI infrastructure failure;
3. role labels without runtime independence receipts;
4. visible tool action without observed authorization;
5. read/permission evidence without successful mutation read-back;
6. recovery after irreversible action receipt;
7. separation of VERIFIED from HOST_LIVE/DEPLOYED/HEALTHY.

## Executed receipt

A local deterministic run on 2026-08-18 produced:

- 7 passed
- 0 failed
- `PASS_POLICY`
- `semantic_agent_evals = NOT_RUN`
- `authentic_multi_agent_runtime = NOT_RUN`
- `host_live_verified = false`

The machine-readable receipt is stored at:

`evidence/rc1-policy-eval-2026-08-18.json`

## Important boundary

`PASS_POLICY` proves only that the deterministic policy implementation returned the expected fail-closed decisions for these cases.

It does **not** prove:
- model reasoning quality;
- genuine epistemic diversity;
- authentic 10/30-agent execution;
- host adapter compatibility;
- hosted GitHub CI health;
- deployment;
- stable release status.

Those remain separate release gates.
