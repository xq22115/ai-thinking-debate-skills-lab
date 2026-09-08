#!/usr/bin/env python3
"""Structural validator for deep-semantic-debate-reasoning behavioral fixtures.

This validates the fixture assets themselves. It does not execute a target model
and must not be interpreted as behavioral verification.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "cases.jsonl"
RUBRIC = ROOT / "scoring-rubric.md"
EXPECTED_CASE_COUNT = 24
REQUIRED_KEYS = {"id", "input", "expected", "must_not"}


def fail(message: str) -> None:
    raise SystemExit(f"semantic fixture validation failed: {message}")


def main() -> None:
    if not CASES.is_file():
        fail(f"missing {CASES.name}")
    if not RUBRIC.is_file():
        fail(f"missing {RUBRIC.name}")

    rows: list[dict[str, object]] = []
    for lineno, raw in enumerate(CASES.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(f"{CASES.name}:{lineno}: invalid JSON: {exc}")
        if not isinstance(row, dict):
            fail(f"{CASES.name}:{lineno}: row must be an object")
        missing = REQUIRED_KEYS - row.keys()
        if missing:
            fail(f"{CASES.name}:{lineno}: missing keys {sorted(missing)}")
        if not isinstance(row["id"], str) or not row["id"].strip():
            fail(f"{CASES.name}:{lineno}: id must be a non-empty string")
        if not isinstance(row["input"], str) or not row["input"].strip():
            fail(f"{CASES.name}:{lineno}: input must be a non-empty string")
        for key in ("expected", "must_not"):
            value = row[key]
            if not isinstance(value, list) or not value:
                fail(f"{CASES.name}:{lineno}: {key} must be a non-empty list")
            if not all(isinstance(item, str) and item.strip() for item in value):
                fail(f"{CASES.name}:{lineno}: {key} items must be non-empty strings")
        rows.append(row)

    if len(rows) != EXPECTED_CASE_COUNT:
        fail(f"expected {EXPECTED_CASE_COUNT} cases, found {len(rows)}")

    ids = [str(row["id"]) for row in rows]
    if len(ids) != len(set(ids)):
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        fail(f"duplicate ids: {duplicates}")

    expected_prefixes = {f"semantic-{idx:02d}" for idx in range(1, EXPECTED_CASE_COUNT + 1)}
    observed_prefixes = {item[:11] for item in ids}
    missing_prefixes = sorted(expected_prefixes - observed_prefixes)
    if missing_prefixes:
        fail(f"missing numbered case prefixes: {missing_prefixes}")

    rubric_text = RUBRIC.read_text(encoding="utf-8")
    required_rubric_markers = [
        "Claim precision",
        "Common-ground integrity",
        "Critical-question utility",
        "Generalization",
        "Blocking errors",
        "Acceptance boundary",
    ]
    missing_markers = [marker for marker in required_rubric_markers if marker not in rubric_text]
    if missing_markers:
        fail(f"rubric missing required markers: {missing_markers}")

    print(f"semantic fixture validation: PASS ({len(rows)} cases, {len(set(ids))} unique ids)")
    print("behavioral status: NOT EXECUTED — target-model evaluation remains separate")


if __name__ == "__main__":
    main()
