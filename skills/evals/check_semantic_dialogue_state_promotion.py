#!/usr/bin/env python3
"""Combined promotion pre-gate for semantic dialogue-state behavioral reports.

This script does not run models or judges. It consumes three already-produced
behavioral reports (target, neighboring-capability protection, and lexical/domain
generalization protection) and checks whether they are coherent enough to advance
to repeated validation.

A PASS here is deliberately not a release or host-live claim.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

TREATMENT = "microscope-dialogue-state"
CORE = "microscope-core"


def load_report(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: report root must be an object")
    return value


def require_text(report: dict[str, Any], key: str, label: str) -> str:
    value = report.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: missing non-empty {key}")
    return value.strip()


def require_list(report: dict[str, Any], key: str, label: str) -> list[Any]:
    value = report.get(key)
    if not isinstance(value, list):
        raise ValueError(f"{label}: {key} must be a list")
    return value


def require_arm(report: dict[str, Any], arm: str, label: str) -> dict[str, Any]:
    arms = report.get("arms")
    if not isinstance(arms, dict):
        raise ValueError(f"{label}: arms must be an object")
    value = arms.get(arm)
    if not isinstance(value, dict):
        raise ValueError(f"{label}: missing arm {arm}")
    judged = value.get("cases_judged")
    if not isinstance(judged, int) or judged <= 0:
        raise ValueError(f"{label}: arm {arm} has no judged cases")
    return value


def blocked_cases(arm: dict[str, Any], label: str, arm_name: str) -> int:
    value = arm.get("blocked_cases", 0)
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{label}: invalid blocked_cases for {arm_name}")
    return value


def numeric_delta(report: dict[str, Any], key: str, label: str) -> float:
    deltas = report.get("treatment_deltas")
    if not isinstance(deltas, dict):
        raise ValueError(f"{label}: treatment_deltas must be an object")
    value = deltas.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label}: {key} must be numeric")
    return float(value)


def same_model_exposure(report: dict[str, Any], label: str) -> int:
    arms = report.get("arms")
    if not isinstance(arms, dict):
        raise ValueError(f"{label}: arms must be an object")
    total = 0
    for arm_name, arm in arms.items():
        if not isinstance(arm, dict):
            raise ValueError(f"{label}: arm {arm_name} must be an object")
        value = arm.get("same_model_judge_cases", 0)
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{label}: invalid same_model_judge_cases for {arm_name}")
        total += value
    return total


def disagreement_count(report: dict[str, Any], label: str) -> int:
    tasks = report.get("judge_disagreement_tasks", [])
    if not isinstance(tasks, list):
        raise ValueError(f"{label}: judge_disagreement_tasks must be a list")
    return len(tasks)


def evaluate(
    target: dict[str, Any],
    protection: dict[str, Any],
    generalization: dict[str, Any],
    min_target_delta: float,
) -> dict[str, Any]:
    reports = {
        "target": target,
        "protection": protection,
        "generalization": generalization,
    }

    identity: dict[str, dict[str, str]] = {}
    arms_by_report: dict[str, dict[str, dict[str, Any]]] = {}
    blocking: list[str] = []
    review_flags: list[str] = []

    for label, report in reports.items():
        identity[label] = {
            "repo_ref": require_text(report, "repo_ref", label),
            "model_id": require_text(report, "model_id", label),
            "provider": require_text(report, "provider", label),
            "fixture_suite": require_text(report, "fixture_suite", label),
            "suite_role": require_text(report, "suite_role", label),
        }
        status = require_text(report, "status", label)
        if status != "JUDGED":
            blocking.append(f"{label}_report_status_not_judged:{status}")
        core_arm = require_arm(report, CORE, label)
        treatment_arm = require_arm(report, TREATMENT, label)
        arms_by_report[label] = {CORE: core_arm, TREATMENT: treatment_arm}

    for key in ("repo_ref", "model_id", "provider"):
        values = {identity[label][key] for label in identity}
        if len(values) != 1:
            blocking.append(f"identity_mismatch:{key}:{sorted(values)}")

    suites = {identity[label]["fixture_suite"] for label in identity}
    if len(suites) != 3:
        blocking.append("fixture_suites_not_distinct")

    target_suite = identity["target"]["fixture_suite"].lower()
    protection_suite = identity["protection"]["fixture_suite"].lower()
    generalization_suite = identity["generalization"]["fixture_suite"].lower()

    if identity["target"]["suite_role"] != "target":
        blocking.append("target_report_not_target_role")
    if "protection" in target_suite or "generalization" in target_suite:
        blocking.append("target_report_wrong_fixture_suite")

    if identity["protection"]["suite_role"] != "protection":
        blocking.append("protection_report_not_protection_role")
    if "protection" not in protection_suite or "generalization" in protection_suite:
        blocking.append("protection_report_wrong_fixture_suite")

    if identity["generalization"]["suite_role"] != "protection":
        blocking.append("generalization_report_not_protection_role")
    if "protection" not in generalization_suite or "generalization" not in generalization_suite:
        blocking.append("generalization_report_wrong_fixture_suite")

    target_delta = numeric_delta(target, "overall_vs_microscope_core", "target")
    if target_delta <= min_target_delta:
        blocking.append(
            f"insufficient_target_gain:{target_delta}<=min:{min_target_delta}"
        )

    target_regressions = require_list(
        target, "treatment_regression_cases_vs_core", "target"
    )
    target_blocking_regressions = require_list(
        target, "treatment_blocking_regressions_vs_core", "target"
    )
    if target_regressions:
        blocking.append(f"target_case_regressions:{len(target_regressions)}")
    if target_blocking_regressions:
        blocking.append(
            f"target_blocking_regressions:{len(target_blocking_regressions)}"
        )

    target_treatment_blocks = blocked_cases(
        arms_by_report["target"][TREATMENT], "target", TREATMENT
    )
    if target_treatment_blocks:
        blocking.append(f"target_treatment_blocking_cases:{target_treatment_blocks}")

    for label, report in (
        ("protection", protection),
        ("generalization", generalization),
    ):
        veto = report.get("protection_promotion_veto")
        if veto is not False:
            blocking.append(f"{label}_promotion_veto_not_false:{veto!r}")
        regressions = require_list(
            report, "treatment_regression_cases_vs_core", label
        )
        blocking_regressions = require_list(
            report, "treatment_blocking_regressions_vs_core", label
        )
        if regressions:
            blocking.append(f"{label}_case_regressions:{len(regressions)}")
        if blocking_regressions:
            blocking.append(
                f"{label}_blocking_regressions:{len(blocking_regressions)}"
            )

    generalization_treatment_blocks = blocked_cases(
        arms_by_report["generalization"][TREATMENT],
        "generalization",
        TREATMENT,
    )
    if generalization_treatment_blocks:
        blocking.append(
            "generalization_treatment_blocking_cases:"
            f"{generalization_treatment_blocks}"
        )

    same_model_total = 0
    disagreement_total = 0
    for label, report in reports.items():
        same_model_total += same_model_exposure(report, label)
        disagreement_total += disagreement_count(report, label)

    if same_model_total:
        blocking.append(f"same_model_judge_exposure:{same_model_total}")
    if disagreement_total:
        review_flags.append(f"judge_disagreement_tasks:{disagreement_total}")

    decision = "BLOCKED" if blocking else "READY_FOR_REPEATED_VALIDATION"
    result = {
        "schema_version": 2,
        "decision": decision,
        "repo_ref": identity["target"]["repo_ref"],
        "model_id": identity["target"]["model_id"],
        "provider": identity["target"]["provider"],
        "target_delta_vs_core": target_delta,
        "min_target_delta": min_target_delta,
        "target_treatment_blocking_cases": target_treatment_blocks,
        "generalization_treatment_blocking_cases": generalization_treatment_blocks,
        "blocking_reasons": blocking,
        "review_flags": review_flags,
        "same_model_judge_exposure_cases": same_model_total,
        "judge_disagreement_task_count": disagreement_total,
        "status_boundary": (
            "READY_FOR_REPEATED_VALIDATION != REPEATED != STABLE != HOST_LIVE"
        ),
    }
    return result


def write_report(path: Path | None, result: dict[str, Any]) -> None:
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path is not None:
        path.write_text(text, encoding="utf-8")
    print(text, end="")


def synthetic_report(
    suite: str,
    role: str,
    target_delta: float,
    veto: bool | None,
    *,
    status: str = "JUDGED",
    same_model: int = 0,
    disagreement: bool = False,
    regressions: list[str] | None = None,
    blocking_regressions: list[str] | None = None,
    core_blocked: int = 0,
    treatment_blocked: int = 0,
) -> dict[str, Any]:
    return {
        "schema_version": 3,
        "repo_ref": "synthetic-ref",
        "model_id": "synthetic-model",
        "provider": "synthetic-provider",
        "fixture_suite": suite,
        "suite_role": role,
        "status": status,
        "arms": {
            CORE: {
                "cases_judged": 4,
                "blocked_cases": core_blocked,
                "same_model_judge_cases": 0,
            },
            TREATMENT: {
                "cases_judged": 4,
                "blocked_cases": treatment_blocked,
                "same_model_judge_cases": same_model,
            },
        },
        "treatment_deltas": {
            "overall_vs_microscope_core": target_delta,
        },
        "treatment_regression_cases_vs_core": regressions or [],
        "treatment_blocking_regressions_vs_core": blocking_regressions or [],
        "protection_promotion_veto": veto,
        "judge_disagreement_tasks": (
            [{"case_id": "synthetic"}] if disagreement else []
        ),
    }


def self_test() -> None:
    target = synthetic_report(
        "semantic-dialogue-state-v0.1", "target", 0.5, None
    )
    protection = synthetic_report(
        "semantic-dialogue-state-protection-v0.1", "protection", 0.0, False
    )
    generalization = synthetic_report(
        "semantic-dialogue-state-protection-generalization-v0.1",
        "protection",
        0.0,
        False,
        disagreement=True,
    )
    good = evaluate(target, protection, generalization, min_target_delta=0.0)
    assert good["decision"] == "READY_FOR_REPEATED_VALIDATION"
    assert good["review_flags"] == ["judge_disagreement_tasks:1"]
    assert good["target_treatment_blocking_cases"] == 0
    assert good["generalization_treatment_blocking_cases"] == 0

    bad_protection = synthetic_report(
        "semantic-dialogue-state-protection-v0.1",
        "protection",
        -0.2,
        True,
        regressions=["DSP3"],
    )
    bad = evaluate(target, bad_protection, generalization, min_target_delta=0.0)
    assert bad["decision"] == "BLOCKED"
    assert any(
        "protection_promotion_veto" in reason
        for reason in bad["blocking_reasons"]
    )
    assert any(
        "protection_case_regressions" in reason
        for reason in bad["blocking_reasons"]
    )

    blocked_target = synthetic_report(
        "semantic-dialogue-state-v0.1",
        "target",
        0.5,
        None,
        core_blocked=1,
        treatment_blocked=1,
    )
    blocked_target_result = evaluate(
        blocked_target, protection, generalization, min_target_delta=0.0
    )
    assert blocked_target_result["decision"] == "BLOCKED"
    assert any(
        "target_treatment_blocking_cases" in reason
        for reason in blocked_target_result["blocking_reasons"]
    )

    blocked_generalization = synthetic_report(
        "semantic-dialogue-state-protection-generalization-v0.1",
        "protection",
        0.0,
        False,
        core_blocked=1,
        treatment_blocked=1,
    )
    blocked_generalization_result = evaluate(
        target, protection, blocked_generalization, min_target_delta=0.0
    )
    assert blocked_generalization_result["decision"] == "BLOCKED"
    assert any(
        "generalization_treatment_blocking_cases" in reason
        for reason in blocked_generalization_result["blocking_reasons"]
    )

    same_model_generalization = synthetic_report(
        "semantic-dialogue-state-protection-generalization-v0.1",
        "protection",
        0.0,
        False,
        same_model=2,
    )
    same_model_result = evaluate(
        target, protection, same_model_generalization, min_target_delta=0.0
    )
    assert same_model_result["decision"] == "BLOCKED"
    assert any(
        "same_model_judge_exposure" in reason
        for reason in same_model_result["blocking_reasons"]
    )

    not_judged = synthetic_report(
        "semantic-dialogue-state-v0.1",
        "target",
        0.5,
        None,
        status="NOT_RUN",
    )
    not_judged_result = evaluate(
        not_judged, protection, generalization, min_target_delta=0.0
    )
    assert not_judged_result["decision"] == "BLOCKED"
    assert any(
        "target_report_status_not_judged" in reason
        for reason in not_judged_result["blocking_reasons"]
    )

    wrong_suite = synthetic_report(
        "semantic-dialogue-state-protection-generalization-v0.1",
        "protection",
        0.0,
        False,
    )
    wrong_suite_result = evaluate(
        target, wrong_suite, generalization, min_target_delta=0.0
    )
    assert wrong_suite_result["decision"] == "BLOCKED"
    assert any(
        "protection_report_wrong_fixture_suite" in reason
        or "fixture_suites_not_distinct" in reason
        for reason in wrong_suite_result["blocking_reasons"]
    )

    print("semantic dialogue-state promotion pre-gate self-test: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check")
    check.add_argument("target_report", type=Path)
    check.add_argument("protection_report", type=Path)
    check.add_argument("generalization_report", type=Path)
    check.add_argument("--min-target-delta", type=float, default=0.0)
    check.add_argument("--output", type=Path)
    check.add_argument("--require-ready", action="store_true")

    sub.add_parser("self-test")

    args = parser.parse_args()
    if args.command == "self-test":
        self_test()
        return

    result = evaluate(
        load_report(args.target_report),
        load_report(args.protection_report),
        load_report(args.generalization_report),
        min_target_delta=args.min_target_delta,
    )
    write_report(args.output, result)
    if (
        args.require_ready
        and result["decision"] != "READY_FOR_REPEATED_VALIDATION"
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
