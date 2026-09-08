#!/usr/bin/env python3
"""Validate semantic dialogue-state evaluation assets.

Static validation only. This does not execute a target model or prove host-live behavior.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURE = HERE / "semantic-dialogue-state-fixtures.json"
PROTECTION = HERE / "semantic-dialogue-state-protection-fixtures.json"
GENERALIZATION = HERE / "semantic-dialogue-state-generalization-holdout.json"
RUBRIC = HERE / "semantic-dialogue-state-scoring-rubric.md"
PROTOCOL = HERE / "semantic-dialogue-state-eval-protocol.md"
HARNESS = HERE / "run_semantic_dialogue_state_eval.py"
REFERENCE = ROOT / "skills" / "semantic-argument-microscope" / "DIALOGUE_STATE.md"
EXPECTED_TARGET_CASES = 8
EXPECTED_PROTECTION_CASES = 12
EXPECTED_GENERALIZATION_CASES = 12


def fail(message: str) -> None:
    raise SystemExit(f"semantic dialogue-state asset validation failed: {message}")


def load_cases(path: Path, expected_count: int, prefix: str) -> list[dict]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid fixture JSON in {path.name}: {exc}")
    if not isinstance(payload, dict):
        fail(f"{path.name}: fixture root must be an object")
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != expected_count:
        found = len(cases) if isinstance(cases, list) else "non-list"
        fail(f"{path.name}: expected {expected_count} cases, found {found}")

    ids: list[str] = []
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            fail(f"{path.name}: case {index} must be an object")
        for key in ("id", "input", "must_detect", "fail_if"):
            if key not in case:
                fail(f"{path.name}: case {index} missing {key}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            fail(f"{path.name}: case {index} id must be a non-empty string")
        if not case_id.startswith(prefix):
            fail(f"{path.name}: {case_id} must start with {prefix}")
        ids.append(case_id)
        if not isinstance(case["input"], str) or not case["input"].strip():
            fail(f"{case_id}: input must be a non-empty string")
        for key in ("must_detect", "fail_if"):
            value = case[key]
            if not isinstance(value, list) or not value:
                fail(f"{case_id}: {key} must be a non-empty list")
            if not all(isinstance(item, str) and item.strip() for item in value):
                fail(f"{case_id}: {key} items must be non-empty strings")

    if len(ids) != len(set(ids)):
        fail(f"{path.name}: duplicate fixture ids")
    return cases


def exact_prefixes(ids: set[str], stem: str, count: int) -> None:
    expected = {f"{stem}{n}" for n in range(1, count + 1)}
    observed = {case_id.split("-", 1)[0] for case_id in ids}
    if observed != expected:
        fail(
            f"{stem} case prefixes mismatch: expected {sorted(expected)}, "
            f"found {sorted(observed)}"
        )


def main() -> None:
    for path in (FIXTURE, PROTECTION, GENERALIZATION, RUBRIC, PROTOCOL, HARNESS, REFERENCE):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT.parent)}")

    target_cases = load_cases(FIXTURE, EXPECTED_TARGET_CASES, "DS")
    protection_cases = load_cases(PROTECTION, EXPECTED_PROTECTION_CASES, "DSP")
    generalization_cases = load_cases(
        GENERALIZATION, EXPECTED_GENERALIZATION_CASES, "DSG"
    )

    target_ids = {case["id"] for case in target_cases}
    protection_ids = {case["id"] for case in protection_cases}
    generalization_ids = {case["id"] for case in generalization_cases}
    if target_ids & protection_ids:
        fail("target/protection fixture ids overlap")
    if target_ids & generalization_ids:
        fail("target/generalization fixture ids overlap")
    if protection_ids & generalization_ids:
        fail("protection/generalization fixture ids overlap")

    exact_prefixes(target_ids, "DS", EXPECTED_TARGET_CASES)
    exact_prefixes(protection_ids, "DSP", EXPECTED_PROTECTION_CASES)
    exact_prefixes(generalization_ids, "DSG", EXPECTED_GENERALIZATION_CASES)

    generalization_payload = json.loads(GENERALIZATION.read_text(encoding="utf-8"))
    generalization_suite = str(generalization_payload.get("suite", ""))
    if "protection" not in generalization_suite or "generalization" not in generalization_suite:
        fail("generalization suite name must identify both protection and generalization roles")

    reference_text = REFERENCE.read_text(encoding="utf-8")
    reference_markers = [
        "Common-Ground Ledger",
        "Dialogue-State Delta",
        "ASSUMED_FOR_TEST != AGREED",
        "UNANSWERED_PRESUPPOSITION != COMMON_GROUND",
        "Provenance Laundering",
        "Structural Generalization Guard",
    ]
    missing_reference = [m for m in reference_markers if m not in reference_text]
    if missing_reference:
        fail(f"reference missing markers: {missing_reference}")

    rubric_text = RUBRIC.read_text(encoding="utf-8")
    rubric_markers = [
        "Common-ground integrity",
        "Dialogue-state delta",
        "Evidence/provenance fidelity",
        "Structural generalization",
        "Blocking errors",
        "Protection-holdout metrics",
        "unnecessary_dialogue_state_invention",
        "promotion veto",
        "Acceptance boundary",
    ]
    missing_rubric = [m for m in rubric_markers if m not in rubric_text]
    if missing_rubric:
        fail(f"rubric missing markers: {missing_rubric}")

    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    protocol_markers = [
        "Evaluation arms",
        "Run manifest",
        "Judge protocol",
        "Multi-judge record identity",
        "Case-first aggregation",
        "Protection baseline",
        "TARGET_GAIN != SAFE_PROMOTION",
        "HARNESS_READY != MODEL_RUN_COMPLETE != JUDGE_VALIDATED != HOST_LIVE",
    ]
    missing_protocol = [m for m in protocol_markers if m not in protocol_text]
    if missing_protocol:
        fail(f"protocol missing markers: {missing_protocol}")

    harness_text = HARNESS.read_text(encoding="utf-8")
    harness_markers = [
        '"direct"',
        '"generic-careful"',
        '"microscope-core"',
        '"microscope-dialogue-state"',
        "PROTECTION_FIXTURES",
        "fixture_path",
        "normalize_arms",
        "prepare_judge_tasks",
        "normalize_judgments",
        "judge_disagreement_tasks",
        "protection_promotion_veto",
        "validate_judgments",
        "treatment_blocking_regressions_vs_core",
        "self_test",
    ]
    missing_harness = [m for m in harness_markers if m not in harness_text]
    if missing_harness:
        fail(f"harness missing markers: {missing_harness}")

    print(
        "semantic dialogue-state assets: PASS "
        f"({len(target_cases)} target + {len(protection_cases)} protection + "
        f"{len(generalization_cases)} generalization cases)"
    )
    print(
        "harness packaging: PASS — reusable fixture/arm execution + multi-judge disagreement + "
        "protection veto present"
    )
    print(
        "behavioral status: NOT EXECUTED — real target-model, protection/generalization, "
        "and host-live checks remain separate"
    )


if __name__ == "__main__":
    main()
