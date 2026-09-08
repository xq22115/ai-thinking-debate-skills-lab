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

### Multi-judge record identity

A candidate/judge task may have more than one judgment. Each judgment should include:

- `judge_task_id` — the candidate task being scored;
- `judge.id` — the judge identity/model label;
- `judgment_id` — unique record identity; the harness can deterministically derive one when omitted;
- optional `variant_id` — use a distinct value for intentional repeats such as an order swap or a second prompting variant from the same judge.

The tuple `(judge_task_id, judge.id, variant_id)` must be unique. This prevents an accidental duplicate from masquerading as independent evidence while still allowing deliberate repeated measurements.

### Case-first aggregation

Do **not** pool every judgment directly into an arm mean. That would overweight candidates that happened to receive more judges.

Aggregation order is:

`raw judgments → one aggregate per candidate/judge_task → one aggregate per arm`

For each candidate/task:

- compute a mean for each applicable dimension across its judgments;
- compute the candidate overall score from those dimension means;
- preserve whether **any** judge reported a blocking error and whether **all** judges did;
- preserve dimension-level score disagreement;
- preserve blocking-set disagreement;
- preserve judge count and same-model-family judge exposure.

Then give each candidate/task equal weight in arm-level statistics regardless of how many judgments it received.

The report should expose at least:

- `mean_judges_per_case`;
- `judge_disagreement_cases` / `judge_disagreement_rate`;
- dimension disagreement details for affected tasks;
- blocking disagreement;
- `blocked_cases` as the conservative any-judge blocking count;
- `blocked_all_judges_cases` separately;
- same-model-family judge exposure.

A disagreement is evidence about evaluation uncertainty; do not erase it by replacing all judgments with a single majority label.

## Blocking-error policy

A blocking error defined in the rubric is a serious case-level failure signal. With a single judge, the case is blocked if that judge records a valid blocking error. With multiple judges, report both:

- **any-judge block** — conservative failure signal used by the current treatment regression check;
- **all-judge block** — stronger agreement that the block is present.

If judges disagree on a blocking error, preserve that disagreement for review rather than silently converting it to consensus. Aggregate dimension points may still be reported diagnostically, but they cannot erase a recorded blocking-error signal.

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
- judge count and same-model-family judge exposure;
- exact model + repo revision;
- remaining unknowns.

## Status boundary

`HARNESS_READY != MODEL_RUN_COMPLETE != JUDGE_VALIDATED != HOST_LIVE`.

The repository may package and validate this protocol without access to a provider model. Behavioral verification requires real recorded outputs and judgments bound to an exact run manifest.
