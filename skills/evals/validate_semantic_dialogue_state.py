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
RUBRIC = HERE / "semantic-dialogue-state-scoring-rubric.md"
REFERENCE = ROOT / "skills" / "semantic-argument-microscope" / "DIALOGUE_STATE.md"
EXPECTED_CASES = 8


def fail(message: str) -> None:
    raise SystemExit(f"semantic dialogue-state asset validation failed: {message}")


def main() -> None:
    for path in (FIXTURE, RUBRIC, REFERENCE):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT.parent)}")

    try:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid fixture JSON: {exc}")

    if not isinstance(payload, dict):
        fail("fixture root must be an object")
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != EXPECTED_CASES:
        fail(f"expected {EXPECTED_CASES} cases, found {len(cases) if isinstance(cases, list) else 'non-list'}")

    ids: list[str] = []
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            fail(f"case {index} must be an object")
        for key in ("id", "input", "must_detect", "fail_if"):
            if key not in case:
                fail(f"case {index} missing {key}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            fail(f"case {index} id must be a non-empty string")
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
        fail("duplicate fixture ids")
    expected_prefixes = {f"DS{n}" for n in range(1, EXPECTED_CASES + 1)}
    observed_prefixes = {case_id.split("-", 1)[0] for case_id in ids}
    if observed_prefixes != expected_prefixes:
        fail(f"case prefixes mismatch: expected {sorted(expected_prefixes)}, found {sorted(observed_prefixes)}")

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
        "Acceptance boundary",
    ]
    missing_rubric = [m for m in rubric_markers if m not in rubric_text]
    if missing_rubric:
        fail(f"rubric missing markers: {missing_rubric}")

    print(f"semantic dialogue-state assets: PASS ({len(cases)} cases, {len(set(ids))} unique ids)")
    print("behavioral status: NOT EXECUTED — target-model and host-live checks remain separate")


if __name__ == "__main__":
    main()
