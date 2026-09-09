# Semantic Dialogue-State Behavioral Evaluation Protocol

Status: `EXPERIMENTAL / PROVIDER-NEUTRAL HARNESS`

Purpose: turn the target, neighboring-capability protection, and lexical/domain generalization suites into reproducible behavioral-evaluation workflows without pretending that repository CI is model-behavior evidence.

## Evaluation arms

The harness supports four comparable arms:

1. `direct` — answer the case without extra reasoning instructions.
2. `generic-careful` — add only a generic instruction to reason carefully.
3. `microscope-core` — load the canonical `semantic-argument-microscope/SKILL.md` but not `DIALOGUE_STATE.md`.
4. `microscope-dialogue-state` — load `SKILL.md` plus `DIALOGUE_STATE.md`.

For the target DS1–DS8 suite, normally run all four arms. For protection suites DSP1–DSP12 and DSG1–DSG12, the minimum useful comparison is arms 3 and 4 because the protection claim is whether the new reference regresses the existing semantic core or only succeeds when canonical vocabulary is present.

The treatment claim is not `arm 4 sounds better`. The useful comparison is whether arm 4 improves target dialogue-state behavior without degrading neighboring capabilities or losing the same structural relation under paraphrase/domain shifts.

## Executable preparation

The same provider-neutral runner handles all suites.

Target run:

```text
python skills/evals/run_semantic_dialogue_state_eval.py prepare RUN_DIR \
  --repo-ref EXACT_SHA \
  --model-id MODEL_ID \
  --provider PROVIDER \
  --fixture skills/evals/semantic-dialogue-state-fixtures.json \
  --arms direct generic-careful microscope-core microscope-dialogue-state
```

Neighboring-capability protection run:

```text
python skills/evals/run_semantic_dialogue_state_eval.py prepare PROTECTION_RUN_DIR \
  --repo-ref EXACT_SHA \
  --model-id MODEL_ID \
  --provider PROVIDER \
  --fixture skills/evals/semantic-dialogue-state-protection-fixtures.json \
  --arms microscope-core microscope-dialogue-state
```

Lexical/domain generalization holdout:

```text
python skills/evals/run_semantic_dialogue_state_eval.py prepare GENERALIZATION_RUN_DIR \
  --repo-ref EXACT_SHA \
  --model-id MODEL_ID \
  --provider PROVIDER \
  --fixture skills/evals/semantic-dialogue-state-generalization-holdout.json \
  --arms microscope-core microscope-dialogue-state
```

The harness does not make provider calls. Execute the prepared requests through the selected provider/runtime, record outputs in `responses.jsonl`, record one `execution_receipts.jsonl` row per request, validate execution isolation, then use `prepare-judge`, record `judgments.jsonl`, and run `summarize`.

`manifest.json` binds exact fixture path/hash, instruction bundle hashes, model/provider label, arms and repository revision so runs can be reproduced without silently changing the test surface.

## Campaign packet preparation

For a strict DS + DSP + DSG campaign, prefer the campaign preparer over three manually assembled commands. It freezes one shared `repo_ref`, `model_id`, `provider`, and `seed`, then composes the existing run preparer and execution-receipt template generator:

```text
python skills/evals/prepare_semantic_dialogue_state_campaign.py prepare CAMPAIGN_DIR \
  --repo-ref EXACT_SHA \
  --model-id MODEL_ID \
  --provider PROVIDER \
  --seed SEED

python skills/evals/prepare_semantic_dialogue_state_campaign.py validate CAMPAIGN_DIR
```

The packet contains:

```text
CAMPAIGN_DIR/
  campaign_manifest.json
  target/
    manifest.json
    bundles.json
    requests.jsonl
    execution_receipts.template.jsonl
  protection/
    manifest.json
    bundles.json
    requests.jsonl
    execution_receipts.template.jsonl
  generalization/
    manifest.json
    bundles.json
    requests.jsonl
    execution_receipts.template.jsonl
```

The target run is frozen to all four arms. DSP and DSG are frozen to `microscope-core` versus `microscope-dialogue-state`. The generalization run retains the harness/promotion-gate compatibility role `protection`; its distinct DSG fixture suite/path still identifies it as the generalization holdout.

`campaign_manifest.json` links all three run IDs and records each fixture/path/hash, arm set, request count, run-manifest hash, bundle hash, request-file hash, ordered request-ID hash, and receipt-template hash. Validation fails on repo/model/provider/seed identity drift, suite/path/arm drift, run-link drift, file-hash drift, request-identity drift, or a receipt template that prematurely claims execution state.

The generated receipt templates deliberately keep host/session/timestamps/output hash, fresh-context evidence, contamination booleans and status unresolved until real execution. A prepared packet is therefore bookkeeping/provenance infrastructure, not model evidence.

`CAMPAIGN_PACKET_VALID != TARGET_MODEL_RUN`.

`PREPARED_NOT_EXECUTED != OUTPUT_RECORDED`.

After campaign preparation, each request still requires one fresh isolated target-model context and a completed execution receipt before judging.

## Target-model execution isolation

Before a recorded response can count as comparison-grade `TARGET_MODEL_RUN` evidence, validate it against `semantic-dialogue-state-execution-isolation.md` with:

```text
python skills/evals/validate_semantic_dialogue_state_execution.py validate RUN_DIR --require-clean
```

Strict comparative runs use one fresh isolated context per `request_id`. The candidate context may see only the common host/provider defaults, its frozen arm bundle, the case input, and the output contract. Before response completion it must not see fixture answer keys, `must_detect` / `fail_if`, scoring-rubric details, blocking-error labels, judge information, other-arm outputs, aggregate scores, or prior benchmark coaching.

Each execution receipt binds:

- request/run/case/arm identity;
- exact `bundle_sha256`;
- model/provider/surface identity;
- pseudonymous `session_id_hash`;
- fresh-context state;
- forbidden-exposure booleans;
- intended arm-bundle exposure;
- exact response `output_sha256`;
- observable tool/sampling metadata or `unknown`;
- execution status.

A reused context, cross-arm memory, rubric leakage, answer-key exposure, judge leakage, identity mismatch, or response-hash mismatch makes the affected request invalid for strict comparison. Record that state; do not repair it by narrative.

A conversation that has already read DS/DSP/DSG answer keys, rubric details, implementation logic, or prior arm outputs is not a clean target-model execution context for those same benchmark requests.

`OUTPUT_EXISTS != COMPARISON_VALID`.

`CLEAN_EXECUTION_RECEIPT != GOOD_ANSWER`.

## Run manifest

Every run should record at least:

- `run_id` and timestamp;
- repository exact ref / commit SHA;
- fixture suite, fixture path and fixture hash;
- target/protection suite role;
- model/provider identifier;
- sampling/temperature/settings when exposed;
- tool/retrieval access;
- selected arms;
- prompt/instruction bundle hash;
- case id;
- response id/hash when available;
- execution-receipt validation state;
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

On protection cases, the absence of unnecessary dialogue-state machinery is itself evidence of correct routing discipline. On generalization cases, credit the correct relation/state behavior rather than reuse of canonical vocabulary. Do not reward verbosity or ceremonial ledgers.

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

### DSP neighboring-capability holdout

DSP1–DSP12 deliberately sample capabilities the dialogue-state reference must not damage:

- definition/QUD/pragmatic interpretation;
- defeasible revision and stance freedom;
- critical-question ranking and steelman fidelity;
- causal association/intervention/global-graph reasoning;
- simple direct definition application where dialogue-state machinery should remain dormant.

### DSG anti-leakage/generalization holdout

DSG1–DSG12 deliberately reduce canonical words such as `agreed`, `common ground`, `criterion lock`, or familiar domain cues. They use paraphrase, changed domains, loaded formulations, bounded concessions, stale/withdrawn positions and support-graph transfer.

The purpose is to distinguish:

`STRUCTURAL_UNDERSTANDING` from `LEXICAL_CUE_MATCHING`.

A model that performs well only when fixture language resembles the skill text has not demonstrated robust generalization.

### Promotion veto

Run the same model/revision under `microscope-core` and `microscope-dialogue-state`. Protection reports record:

- per-case regressions vs core;
- new blocking regressions vs core;
- judge disagreement;
- `protection_promotion_veto`.

The current veto is conservative: if the treatment has any lower per-case aggregate score than core or introduces a blocking error where core did not, the protection report sets `protection_promotion_veto=true` pending review.

Do not promote the extension merely because DS1–DS8 improves if DSP or DSG regresses. A hard-slice regression outranks an aggregate target gain.

`TARGET_GAIN != SAFE_PROMOTION`.

## Minimum acceptance report

A behavioral evaluation should report:

- target DS1–DS8 attempted / completed / invalid;
- DSP1–DSP12 attempted / completed / invalid;
- DSG1–DSG12 attempted / completed / invalid;
- clean execution-receipt count and invalid/blocked execution count;
- blocking-error count and rate per arm;
- average applicable score by dimension per arm;
- treatment delta vs `direct` and vs `microscope-core` where those arms exist;
- cases where treatment regressed;
- protection promotion veto state for both protection suites;
- judge disagreement / order-swap instability when measured;
- judge count and same-model-family judge exposure;
- exact model + repo revision;
- remaining unknowns.

## Evidence levels

Keep these states separate:

`FIXTURE_SPECIFIED → STATIC_VALIDATED → HARNESS_SELF_TESTED → TARGET_MODEL_RUN → INDEPENDENT_JUDGED → REPEATED → HOST_LIVE_REGRESSION`

`TARGET_MODEL_RUN` requires clean execution provenance for the compared requests. A synthetic execution-receipt self-test validates only the isolation validator itself; it does not create a real target-model run.

Synthetic target/protection self-tests prove harness plumbing only. Static DSG validation proves only that the anti-leakage suite is packaged and executable through the generalized harness. A valid campaign packet proves only three-suite preparation/identity integrity. None of these prove real model generalization.

## Status boundary

`HARNESS_READY != MODEL_RUN_COMPLETE != JUDGE_VALIDATED != HOST_LIVE`.

`CAMPAIGN_PACKET_VALID != TARGET_MODEL_RUN != INDEPENDENT_JUDGED != REPEATED != HOST_LIVE`.

The repository may package and validate this protocol without access to a provider model. Behavioral verification requires real isolated recorded outputs and judgments bound to an exact run manifest and, when using a campaign packet, its frozen campaign identity.
