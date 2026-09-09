# Semantic Dialogue-State Target-Model Execution Isolation

Status: `EXPERIMENTAL / EXECUTION CONTRACT`

Purpose: define when externally recorded candidate outputs are valid evidence for DS/DSP/DSG behavioral comparison. This document does **not** prove a model run occurred; it defines the receipts required before `responses.jsonl` may be treated as comparison-grade target-model evidence.

## Why isolation is required

A model that has already seen the fixture answer keys, scoring rubric, other arms, or earlier judgments can appear to improve without the treatment being responsible.

Therefore:

`OUTPUT_EXISTS != COMPARISON_VALID`

`SEEN_RUBRIC != STRUCTURAL_COMPREHENSION`

`CROSS_ARM_MEMORY != TREATMENT_EFFECT`

The intended arm bundle is allowed exposure. Unintended exposure to fixture labels, `must_detect` / `fail_if`, judge tasks, scores, other-arm outputs, or prior benchmark coaching is contamination.

## Strict comparison unit

For a strict comparative run, every `request_id` is executed in a fresh isolated context containing only:

1. provider/host default system context that is common to all arms;
2. the exact arm instruction bundle identified by `bundle_sha256`;
3. the case `input` for that request;
4. the minimal output-format instruction already frozen in `requests.jsonl`.

Do not place two benchmark requests in the same conversational context when claiming a strict treatment effect. A new tab/window alone is insufficient unless the owning host actually gives a fresh conversation/context.

## Allowed arm exposure

- `direct` — no semantic skill bundle.
- `generic-careful` — only the frozen generic-careful instruction.
- `microscope-core` — exactly the frozen `semantic-argument-microscope/SKILL.md` bundle represented by the request hash.
- `microscope-dialogue-state` — exactly the frozen core skill plus `DIALOGUE_STATE.md` bundle represented by the request hash.

No arm may see another arm's output before producing its own output.

## Forbidden pre-response exposure

Before the candidate response is completed, the execution context must not expose:

- `must_detect` or `fail_if` fields;
- scoring-rubric dimension descriptions beyond the normal output contract;
- blocking-error labels;
- judge instructions or judge outputs;
- another arm's response for the same or another benchmark request;
- aggregate scores, promotion-gate results, or expected treatment direction;
- hidden answer keys or hand-written corrections derived from the fixture suite.

If any of these occur, mark the receipt `INVALID_FOR_COMPARISON`; do not silently keep the response as clean evidence.

## Required execution receipt per request

Record one receipt for every request, with at least:

- `request_id`;
- `run_id`;
- `case_id`;
- `arm`;
- `bundle_sha256`;
- `model_id`;
- `provider`;
- `surface` — API, ChatGPT Web, ChatGPT Desktop, or another explicit host label;
- `session_id_hash` — a non-secret hash/pseudonymous identifier, not a raw private session token;
- `fresh_context` — boolean;
- `fixture_answer_key_exposed_before_response` — boolean;
- `rubric_exposed_before_response` — boolean;
- `cross_arm_output_exposed_before_response` — boolean;
- `judge_information_exposed_before_response` — boolean;
- `arm_bundle_exposure` — one of `none`, `generic-careful`, `microscope-core`, `microscope-dialogue-state`;
- `output_sha256` — SHA-256 of the exact recorded response text;
- `started_at` and `finished_at` timestamps;
- `tool_access` and `sampling_settings` when observable, otherwise `unknown`;
- `status` — `OUTPUT_RECORDED`, `INVALID_FOR_COMPARISON`, or `BLOCKED`;
- optional `notes` for host limitations or anomalies.

The receipt identity is the request. Duplicate receipts for one request are invalid unless the run is explicitly modeled as a repeated run with distinct request/run identities.

## Strict clean-run requirements

A request is comparison-clean only when all are true:

- receipt identity matches the frozen request;
- receipt model/provider match the run manifest;
- `fresh_context == true`;
- the context/session identifier is not reused by another request in the same strict run;
- all forbidden-exposure booleans are `false`;
- `arm_bundle_exposure` matches the arm;
- `bundle_sha256` matches the request;
- `output_sha256` matches the exact `responses.jsonl` output;
- receipt status is `OUTPUT_RECORDED`.

A strict target-model run is complete only when every required request is clean. Partial execution may be recorded, but it cannot be promoted to a complete four-arm or protection/generalization comparison.

## Host limitations

If a host does not expose sampling settings, internal registration state, or a stable session identifier, record `unknown` rather than inventing values. A pseudonymous locally generated execution-unit ID may be used only to distinguish fresh contexts; it is not proof of host internals.

If a host cannot guarantee fresh isolated contexts, record the run as `INVALID_FOR_COMPARISON` or `BLOCKED` for strict causal comparison. The outputs may still be useful qualitatively, but they are not treatment-effect evidence.

## Current-chat contamination rule

A conversation that has already read the DS/DSP/DSG fixtures, answer keys, rubric, or implementation details is **not** a clean target-model execution context for those same fixtures.

Do not generate benchmark responses in that contaminated conversation and then label them `TARGET_MODEL_RUN`.

## Handoff to behavioral evaluation

Execution validation should happen before judge-task generation:

`prepare requests → isolated execution → execution receipts + responses → execution validation → blinded judge tasks → judgments → behavioral report → combined promotion pre-gate`

The execution validator checks provenance/isolation, not answer correctness. The behavioral evaluator and judge remain the owners of semantic scoring.

## Evidence boundary

A clean execution receipt can advance evidence to `TARGET_MODEL_RUN` only for the recorded requests. It does not establish `INDEPENDENT_JUDGED`, `REPEATED`, `HOST_LIVE_REGRESSION`, or model-weight change.

`CLEAN_EXECUTION_RECEIPT != GOOD_ANSWER`

`TARGET_MODEL_RUN != INDEPENDENT_JUDGED`
