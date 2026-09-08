# Semantic Dialogue-State Behavioral Evaluation Protocol

Status: `EXPERIMENTAL / PROVIDER-NEUTRAL HARNESS`

Purpose: turn `semantic-dialogue-state-fixtures.json` from a static specification into a reproducible behavioral-evaluation workflow without pretending that repository CI is model-behavior evidence.

## Evaluation arms

Run the same case under four comparable arms:

1. `direct` — answer the case without extra reasoning instructions.
2. `generic-careful` — add only a generic instruction to reason carefully.
3. `microscope-core` — load the canonical `semantic-argument-microscope/SKILL.md` but not `DIALOGUE_STATE.md`.
4. `microscope-dialogue-state` — load `SKILL.md` plus `DIALOGUE_STATE.md` only when the fixture matches its trigger.

The treatment claim is not `arm 4 sounds better`. The useful comparison is whether arm 4 improves the dialogue-state dimensions and blocking-error rate without degrading protection dimensions or unrelated cases.

## Run manifest

Every run should record at least:

- `run_id` and timestamp;
- repository exact ref / commit SHA;
- fixture suite version;
- model/provider identifier;
- sampling/temperature/settings when exposed;
- tool/retrieval access;
- arm;
- prompt/instruction bundle hash;
- case id;
- response id/hash;
- judge identity and judge mode;
- whether generator and judge are the same model family;
- whether candidate labels/order were blinded or swapped;
- execution status (`NOT_RUN`, `OUTPUT_RECORDED`, `JUDGED`, `INVALID`).

Do not infer unavailable provider settings. Record them as `unknown`.

## Output contract for candidate models

Grade observable/auditable output, not private chain-of-thought. A candidate response may be concise, but it should expose enough structure to judge the relevant behavior, for example:

- normalized state/claim;
- common-ground classification when material;
- dialogue-state change when material;
- actual rebuttal/support target;
- evidence/provenance distinction;
- repair or decisive next test;
- calibrated conclusion/uncertainty.

Do not reward verbosity by itself.

## Judge protocol

Use `semantic-dialogue-state-scoring-rubric.md` and score applicable dimensions `0/1/2`, plus explicit blocking errors.

Preferred safeguards:

- blind model/arm labels during judging;
- do not show aggregate arm scores before individual-case scoring;
- avoid letting a candidate model grade itself when an independent judge is available;
- for pairwise preference claims, repeat with candidate order swapped and report disagreement;
- preserve raw per-dimension scores instead of only one aggregate number;
- audit a sample of judge decisions against the fixture `must_detect` / `fail_if` fields;
- if multiple judges are used, report disagreement rather than forcing consensus.

`JUDGE_CONSENSUS != GROUND_TRUTH`.

## Blocking-error policy

A blocking error defined in the rubric fails that case for the arm regardless of aggregate dimension points. Aggregate score may still be reported diagnostically, but it cannot override the block.

## Protection baseline

Before claiming improvement, verify that the treatment does not worsen at least:

- literal/pragmatic boundary;
- QUD/crux fidelity;
- warrant/evidence fidelity;
- stance freedom / defeasible revision;
- causal/abductive separation when the case is causal;
- concise direct answers on cases where dialogue-state machinery is unnecessary.

Do not promote the extension if it gains DS-suite points by over-triggering, over-interpreting, or adding verbosity without decision value.

## Minimum acceptance report

A behavioral run should report:

- cases attempted / completed / invalid;
- blocking-error count and rate per arm;
- average applicable score by dimension per arm;
- treatment delta vs `direct` and vs `microscope-core`;
- cases where treatment regressed;
- judge disagreement / order-swap instability when measured;
- exact model + repo revision;
- remaining unknowns.

## Status boundary

`HARNESS_READY != MODEL_RUN_COMPLETE != JUDGE_VALIDATED != HOST_LIVE`.

The repository may package and validate this protocol without access to a provider model. Behavioral verification requires real recorded outputs and judgments bound to an exact run manifest.