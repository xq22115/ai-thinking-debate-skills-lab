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
EXECUTION_PROTOCOL = HERE / "semantic-dialogue-state-execution-isolation.md"
HARNESS = HERE / "run_semantic_dialogue_state_eval.py"
EXECUTION_VALIDATOR = HERE / "validate_semantic_dialogue_state_execution.py"
CAMPAIGN_PREPARER = HERE / "prepare_semantic_dialogue_state_campaign.py"
CAMPAIGN_TEST = HERE / "test_prepare_semantic_dialogue_state_campaign.py"
PROMOTION_GATE = HERE / "check_semantic_dialogue_state_promotion.py"
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


def require_markers(path: Path, markers: list[str], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{label} missing markers: {missing}")


def main() -> None:
    for path in (
        FIXTURE,
        PROTECTION,
        GENERALIZATION,
        RUBRIC,
        PROTOCOL,
        EXECUTION_PROTOCOL,
        HARNESS,
        EXECUTION_VALIDATOR,
        CAMPAIGN_PREPARER,
        CAMPAIGN_TEST,
        PROMOTION_GATE,
        REFERENCE,
    ):
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

    require_markers(
        REFERENCE,
        [
            "Common-Ground Ledger",
            "Dialogue-State Delta",
            "ASSUMED_FOR_TEST != AGREED",
            "UNANSWERED_PRESUPPOSITION != COMMON_GROUND",
            "Provenance Laundering",
            "Structural Generalization Guard",
        ],
        "reference",
    )

    require_markers(
        RUBRIC,
        [
            "Common-ground integrity",
            "Dialogue-state delta",
            "Evidence/provenance fidelity",
            "Structural generalization",
            "Blocking errors",
            "Protection-holdout metrics",
            "unnecessary_dialogue_state_invention",
            "promotion veto",
            "Acceptance boundary",
        ],
        "rubric",
    )

    require_markers(
        PROTOCOL,
        [
            "Evaluation arms",
            "Campaign packet preparation",
            "campaign_manifest.json",
            "CAMPAIGN_PACKET_VALID",
            "Run manifest",
            "Judge protocol",
            "Multi-judge record identity",
            "Case-first aggregation",
            "Protection baseline",
            "DSG1–DSG12",
            "TARGET_GAIN != SAFE_PROMOTION",
            "HARNESS_READY != MODEL_RUN_COMPLETE != JUDGE_VALIDATED != HOST_LIVE",
        ],
        "protocol",
    )

    require_markers(
        EXECUTION_PROTOCOL,
        [
            "Strict comparison unit",
            "Forbidden pre-response exposure",
            "Required execution receipt per request",
            "INVALID_FOR_COMPARISON",
            "Current-chat contamination rule",
            "CLEAN_EXECUTION_RECEIPT != GOOD_ANSWER",
            "TARGET_MODEL_RUN != INDEPENDENT_JUDGED",
        ],
        "execution isolation protocol",
    )

    require_markers(
        HARNESS,
        [
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
        ],
        "harness",
    )

    require_markers(
        EXECUTION_VALIDATOR,
        [
            "EXPECTED_ARM_EXPOSURE",
            "fixture_answer_key_exposed_before_response",
            "cross_arm_output_exposed_before_response",
            "session_context_reused",
            "output_sha256_mismatch",
            "CLEAN_COMPLETE",
            "PARTIAL_OR_INVALID",
            "prepare_template",
            "self_test",
        ],
        "execution receipt validator",
    )

    require_markers(
        CAMPAIGN_PREPARER,
        [
            "SUITE_CONFIG",
            "prepare_campaign",
            "validate_campaign",
            "execution_receipts.template.jsonl",
            "identity drift",
            "PREPARED_NOT_EXECUTED",
            "CAMPAIGN_PACKET_VALID",
            "self_test",
        ],
        "campaign packet preparer",
    )

    require_markers(
        CAMPAIGN_TEST,
        [
            "test_prepare_campaign_binds_identity_and_suite_shapes",
            "test_prepare_campaign_generates_frozen_receipt_templates",
            "test_validate_campaign_rejects_identity_drift",
        ],
        "campaign packet contract test",
    )

    require_markers(
        PROMOTION_GATE,
        [
            "READY_FOR_REPEATED_VALIDATION",
            "protection_promotion_veto",
            "same_model_judge_exposure",
            "judge_disagreement_tasks",
            "target_case_regressions",
            "generalization_report_wrong_fixture_suite",
            "READY_FOR_REPEATED_VALIDATION != REPEATED != STABLE != HOST_LIVE",
            "self_test",
        ],
        "promotion pre-gate",
    )

    print(
        "semantic dialogue-state assets: PASS "
        f"({len(target_cases)} target + {len(protection_cases)} protection + "
        f"{len(generalization_cases)} generalization cases)"
    )
    print(
        "harness packaging: PASS — reusable fixture/arm execution + frozen three-suite campaign "
        "identity + receipt templates + isolated execution validation + multi-judge disagreement + "
        "protection veto + combined promotion pre-gate present"
    )
    print(
        "behavioral status: NOT EXECUTED — campaign preparation is not target-model evidence; "
        "real target-model, protection/generalization, repeated validation and host-live checks "
        "remain separate"
    )


if __name__ == "__main__":
    main()
