#!/usr/bin/env python3
"""Provider-neutral harness for semantic dialogue-state behavioral evaluation.

This script does not call any model provider. It prepares reproducible requests,
validates externally-recorded responses, creates blinded judge tasks, validates
structured judgments, and summarizes arm-level behavioral results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "skills/evals/semantic-dialogue-state-fixtures.json"
RUBRIC = ROOT / "skills/evals/semantic-dialogue-state-scoring-rubric.md"
PROTOCOL = ROOT / "skills/evals/semantic-dialogue-state-eval-protocol.md"
CORE_SKILL = ROOT / "skills/skills/semantic-argument-microscope/SKILL.md"
DIALOGUE_STATE = ROOT / "skills/skills/semantic-argument-microscope/DIALOGUE_STATE.md"

ARMS = (
    "direct",
    "generic-careful",
    "microscope-core",
    "microscope-dialogue-state",
)

DIMENSIONS = (
    "common_ground_integrity",
    "dialogue_state_delta",
    "argument_target_comprehension",
    "evidence_provenance_fidelity",
    "reasoning_alignment_fidelity",
    "repair_quality",
    "structural_generalization",
    "calibration",
)

BLOCKING_ERROR_IDS = (
    "assumed_for_test_to_agreed",
    "silence_or_presupposition_to_agreement",
    "definition_mismatch_to_consensus",
    "rhetoric_or_volume_as_evidence",
    "wrong_rebuttal_target_credited",
    "shared_conclusion_to_shared_reasoning",
    "domain_vocabulary_changes_relation",
    "host_live_claim_without_verification",
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def dump_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def dump_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            value = json.loads(stripped)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: expected JSON object")
            rows.append(value)
    return rows


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:20]


def arm_bundle_text(arm: str) -> str:
    if arm == "direct":
        return ""
    if arm == "generic-careful":
        return (
            "Reason carefully. Give a concise, auditable answer. Distinguish what is "
            "established from what is assumed or uncertain."
        )
    core = read_text(CORE_SKILL)
    if arm == "microscope-core":
        return core
    if arm == "microscope-dialogue-state":
        return core + "\n\n--- DEMAND-LOADED REFERENCE ---\n\n" + read_text(DIALOGUE_STATE)
    raise ValueError(f"unknown arm: {arm}")


def prepare(run_dir: Path, repo_ref: str, model_id: str, provider: str, seed: int) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    fixtures = load_json(FIXTURES)
    cases = fixtures.get("cases") or []
    if not cases:
        raise ValueError("fixture suite has no cases")

    run_id = f"ds-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{stable_id(repo_ref, model_id, str(seed))[:8]}"
    bundles: dict[str, dict[str, Any]] = {}
    for arm in ARMS:
        text = arm_bundle_text(arm)
        bundles[arm] = {
            "arm": arm,
            "sha256": sha256_text(text),
            "instruction_text": text,
            "source_paths": (
                []
                if arm in {"direct", "generic-careful"}
                else [str(CORE_SKILL.relative_to(ROOT))]
                + ([str(DIALOGUE_STATE.relative_to(ROOT))] if arm == "microscope-dialogue-state" else [])
            ),
        }

    requests: list[dict[str, Any]] = []
    for case in cases:
        case_id = case["id"]
        for arm in ARMS:
            request_id = stable_id(run_id, case_id, arm)
            requests.append(
                {
                    "request_id": request_id,
                    "run_id": run_id,
                    "case_id": case_id,
                    "arm": arm,
                    "bundle_sha256": bundles[arm]["sha256"],
                    "input": case["input"],
                    "required_output": "concise auditable reasoning summary; no private chain-of-thought required",
                }
            )

    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repo_ref": repo_ref,
        "model_id": model_id,
        "provider": provider,
        "seed": seed,
        "fixture_suite": fixtures.get("suite"),
        "fixture_sha256": sha256_text(read_text(FIXTURES)),
        "rubric_sha256": sha256_text(read_text(RUBRIC)),
        "protocol_sha256": sha256_text(read_text(PROTOCOL)),
        "arms": list(ARMS),
        "case_count": len(cases),
        "request_count": len(requests),
        "tool_access": "unknown",
        "sampling_settings": "unknown",
        "status": "NOT_RUN",
        "status_boundary": "HARNESS_READY != MODEL_RUN_COMPLETE != JUDGE_VALIDATED != HOST_LIVE",
    }
    dump_json(run_dir / "manifest.json", manifest)
    dump_json(run_dir / "bundles.json", bundles)
    dump_jsonl(run_dir / "requests.jsonl", requests)
    print(f"prepared {len(requests)} requests across {len(cases)} cases in {run_dir}")


def index_unique(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"{label}: missing non-empty {key}")
        if value in result:
            raise ValueError(f"{label}: duplicate {key}={value}")
        result[value] = row
    return result


def validate_responses(run_dir: Path, allow_partial: bool = False) -> dict[str, Any]:
    requests = load_jsonl(run_dir / "requests.jsonl")
    responses = load_jsonl(run_dir / "responses.jsonl")
    req_by_id = index_unique(requests, "request_id", "requests")
    resp_by_id = index_unique(responses, "request_id", "responses")

    unknown = sorted(set(resp_by_id) - set(req_by_id))
    missing = sorted(set(req_by_id) - set(resp_by_id))
    if unknown:
        raise ValueError(f"responses contain unknown request ids: {unknown[:5]}")
    if missing and not allow_partial:
        raise ValueError(f"missing {len(missing)} responses")

    for request_id, response in resp_by_id.items():
        output = response.get("output")
        if not isinstance(output, str) or not output.strip():
            raise ValueError(f"response {request_id} has empty output")
        request = req_by_id[request_id]
        for field in ("case_id", "arm"):
            if response.get(field) not in (None, request[field]):
                raise ValueError(f"response {request_id} mismatches request {field}")

    summary = {
        "requests": len(requests),
        "responses": len(responses),
        "missing": len(missing),
        "complete": not missing,
    }
    print(json.dumps(summary, sort_keys=True))
    return summary


def prepare_judge_tasks(run_dir: Path, blind_seed: int) -> None:
    validate_responses(run_dir, allow_partial=False)
    fixtures = load_json(FIXTURES)
    cases = {case["id"]: case for case in fixtures["cases"]}
    requests = index_unique(load_jsonl(run_dir / "requests.jsonl"), "request_id", "requests")
    responses = index_unique(load_jsonl(run_dir / "responses.jsonl"), "request_id", "responses")

    rng = random.Random(blind_seed)
    request_ids = list(requests)
    rng.shuffle(request_ids)
    labels = {request_id: f"candidate-{idx + 1:03d}" for idx, request_id in enumerate(request_ids)}

    tasks: list[dict[str, Any]] = []
    for request_id in request_ids:
        request = requests[request_id]
        response = responses[request_id]
        case = cases[request["case_id"]]
        tasks.append(
            {
                "judge_task_id": stable_id("judge", request_id, str(blind_seed)),
                "request_id": request_id,
                "candidate_label": labels[request_id],
                "case_id": request["case_id"],
                "case_input": case["input"],
                "must_detect": case.get("must_detect", []),
                "fail_if": case.get("fail_if", []),
                "candidate_output": response["output"],
                "dimensions": list(DIMENSIONS),
                "allowed_scores": [0, 1, 2, None],
                "known_blocking_error_ids": list(BLOCKING_ERROR_IDS),
                "rubric_path": str(RUBRIC.relative_to(ROOT)),
                "judge_instruction": (
                    "Score observable output only. Use 0/1/2 or null per dimension. "
                    "List blocking error IDs only when the rubric condition is actually met. "
                    "Do not infer private chain-of-thought or reward verbosity/style."
                ),
            }
        )
    dump_jsonl(run_dir / "judge_tasks.jsonl", tasks)
    dump_json(run_dir / "blind_map.json", {"blind_seed": blind_seed, "labels": labels})
    print(f"prepared {len(tasks)} blinded judge tasks")


def validate_judgments(run_dir: Path, allow_partial: bool = False) -> dict[str, Any]:
    tasks = index_unique(load_jsonl(run_dir / "judge_tasks.jsonl"), "judge_task_id", "judge tasks")
    judgments = index_unique(load_jsonl(run_dir / "judgments.jsonl"), "judge_task_id", "judgments")
    unknown = sorted(set(judgments) - set(tasks))
    missing = sorted(set(tasks) - set(judgments))
    if unknown:
        raise ValueError(f"judgments contain unknown task ids: {unknown[:5]}")
    if missing and not allow_partial:
        raise ValueError(f"missing {len(missing)} judgments")

    for task_id, judgment in judgments.items():
        scores = judgment.get("scores")
        if not isinstance(scores, dict):
            raise ValueError(f"judgment {task_id}: scores must be an object")
        unknown_dims = set(scores) - set(DIMENSIONS)
        if unknown_dims:
            raise ValueError(f"judgment {task_id}: unknown dimensions {sorted(unknown_dims)}")
        for dim in DIMENSIONS:
            value = scores.get(dim)
            if value not in (0, 1, 2, None):
                raise ValueError(f"judgment {task_id}: invalid score for {dim}: {value}")
        blocks = judgment.get("blocking_errors", [])
        if not isinstance(blocks, list) or any(not isinstance(item, str) for item in blocks):
            raise ValueError(f"judgment {task_id}: blocking_errors must be a string list")
        unknown_blocks = set(blocks) - set(BLOCKING_ERROR_IDS)
        if unknown_blocks:
            raise ValueError(f"judgment {task_id}: unknown blocking errors {sorted(unknown_blocks)}")
        judge = judgment.get("judge")
        if not isinstance(judge, dict) or not str(judge.get("id", "")).strip():
            raise ValueError(f"judgment {task_id}: judge.id is required")
        if judgment.get("request_id") not in (None, tasks[task_id]["request_id"]):
            raise ValueError(f"judgment {task_id}: request_id mismatch")

    summary = {
        "judge_tasks": len(tasks),
        "judgments": len(judgments),
        "missing": len(missing),
        "complete": not missing,
    }
    print(json.dumps(summary, sort_keys=True))
    return summary


def mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 4) if values else None


def summarize(run_dir: Path) -> dict[str, Any]:
    validate_judgments(run_dir, allow_partial=False)
    requests = index_unique(load_jsonl(run_dir / "requests.jsonl"), "request_id", "requests")
    tasks = index_unique(load_jsonl(run_dir / "judge_tasks.jsonl"), "judge_task_id", "judge tasks")
    judgments = index_unique(load_jsonl(run_dir / "judgments.jsonl"), "judge_task_id", "judgments")

    per_arm: dict[str, dict[str, Any]] = {}
    per_case_arm: dict[tuple[str, str], dict[str, Any]] = {}
    for arm in ARMS:
        per_arm[arm] = {
            "cases_judged": 0,
            "blocked_cases": 0,
            "dimension_values": {dim: [] for dim in DIMENSIONS},
            "overall_values": [],
            "same_model_judge_cases": 0,
        }

    for task_id, judgment in judgments.items():
        task = tasks[task_id]
        request = requests[task["request_id"]]
        arm = request["arm"]
        scores = judgment["scores"]
        applicable = [float(v) for v in scores.values() if v is not None]
        overall = mean(applicable)
        blocked = bool(judgment.get("blocking_errors"))
        bucket = per_arm[arm]
        bucket["cases_judged"] += 1
        bucket["blocked_cases"] += int(blocked)
        if judgment.get("judge", {}).get("same_model_family_as_generator") is True:
            bucket["same_model_judge_cases"] += 1
        for dim in DIMENSIONS:
            value = scores.get(dim)
            if value is not None:
                bucket["dimension_values"][dim].append(float(value))
        if overall is not None:
            bucket["overall_values"].append(float(overall))
        per_case_arm[(request["case_id"], arm)] = {
            "overall": overall,
            "blocked": blocked,
            "blocking_errors": judgment.get("blocking_errors", []),
        }

    arm_report: dict[str, Any] = {}
    for arm, bucket in per_arm.items():
        judged = bucket["cases_judged"]
        arm_report[arm] = {
            "cases_judged": judged,
            "blocked_cases": bucket["blocked_cases"],
            "blocking_error_rate": round(bucket["blocked_cases"] / judged, 4) if judged else None,
            "mean_overall_applicable_score": mean(bucket["overall_values"]),
            "mean_by_dimension": {
                dim: mean(bucket["dimension_values"][dim]) for dim in DIMENSIONS
            },
            "same_model_judge_cases": bucket["same_model_judge_cases"],
        }

    treatment = "microscope-dialogue-state"
    regression_cases: list[str] = []
    blocked_regressions: list[str] = []
    cases = sorted({case_id for case_id, _ in per_case_arm})
    for case_id in cases:
        treatment_row = per_case_arm.get((case_id, treatment))
        core_row = per_case_arm.get((case_id, "microscope-core"))
        if not treatment_row or not core_row:
            continue
        if (
            treatment_row["overall"] is not None
            and core_row["overall"] is not None
            and treatment_row["overall"] < core_row["overall"]
        ):
            regression_cases.append(case_id)
        if treatment_row["blocked"] and not core_row["blocked"]:
            blocked_regressions.append(case_id)

    def delta(a: str, b: str, field: str) -> float | None:
        av = arm_report[a].get(field)
        bv = arm_report[b].get(field)
        if av is None or bv is None:
            return None
        return round(float(av) - float(bv), 4)

    manifest = load_json(run_dir / "manifest.json")
    report = {
        "schema_version": 1,
        "run_id": manifest["run_id"],
        "repo_ref": manifest["repo_ref"],
        "model_id": manifest["model_id"],
        "provider": manifest["provider"],
        "arms": arm_report,
        "treatment_deltas": {
            "overall_vs_direct": delta(treatment, "direct", "mean_overall_applicable_score"),
            "overall_vs_microscope_core": delta(treatment, "microscope-core", "mean_overall_applicable_score"),
            "blocking_rate_vs_direct": delta(treatment, "direct", "blocking_error_rate"),
            "blocking_rate_vs_microscope_core": delta(treatment, "microscope-core", "blocking_error_rate"),
        },
        "treatment_regression_cases_vs_core": regression_cases,
        "treatment_blocking_regressions_vs_core": blocked_regressions,
        "status": "JUDGED",
        "status_boundary": "JUDGED != INDEPENDENTLY_VALIDATED != HOST_LIVE",
    }
    dump_json(run_dir / "report.json", report)
    print(json.dumps(report["treatment_deltas"], sort_keys=True))
    return report


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="semantic-ds-eval-") as tmp:
        run_dir = Path(tmp)
        prepare(run_dir, "self-test-ref", "synthetic-model", "synthetic", 7)
        requests = load_jsonl(run_dir / "requests.jsonl")
        responses = [
            {
                "request_id": row["request_id"],
                "case_id": row["case_id"],
                "arm": row["arm"],
                "output": f"Synthetic auditable output for {row['case_id']} / {row['arm']}",
            }
            for row in requests
        ]
        dump_jsonl(run_dir / "responses.jsonl", responses)
        validate_responses(run_dir)
        prepare_judge_tasks(run_dir, blind_seed=11)
        tasks = load_jsonl(run_dir / "judge_tasks.jsonl")
        judgments: list[dict[str, Any]] = []
        req_index = index_unique(requests, "request_id", "requests")
        for task in tasks:
            arm = req_index[task["request_id"]]["arm"]
            treatment = arm == "microscope-dialogue-state"
            score = 2 if treatment else 1
            judgments.append(
                {
                    "judge_task_id": task["judge_task_id"],
                    "request_id": task["request_id"],
                    "scores": {dim: score for dim in DIMENSIONS},
                    "blocking_errors": [],
                    "judge": {
                        "id": "synthetic-independent-judge",
                        "same_model_family_as_generator": False,
                    },
                }
            )
        dump_jsonl(run_dir / "judgments.jsonl", judgments)
        validate_judgments(run_dir)
        report = summarize(run_dir)
        assert report["treatment_deltas"]["overall_vs_microscope_core"] == 1.0
        assert report["treatment_blocking_regressions_vs_core"] == []
    print("semantic dialogue-state eval harness self-test: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser("prepare")
    p_prepare.add_argument("run_dir", type=Path)
    p_prepare.add_argument("--repo-ref", required=True)
    p_prepare.add_argument("--model-id", required=True)
    p_prepare.add_argument("--provider", default="unknown")
    p_prepare.add_argument("--seed", type=int, default=0)

    p_resp = sub.add_parser("validate-responses")
    p_resp.add_argument("run_dir", type=Path)
    p_resp.add_argument("--allow-partial", action="store_true")

    p_judge = sub.add_parser("prepare-judge")
    p_judge.add_argument("run_dir", type=Path)
    p_judge.add_argument("--blind-seed", type=int, default=0)

    p_judgments = sub.add_parser("validate-judgments")
    p_judgments.add_argument("run_dir", type=Path)
    p_judgments.add_argument("--allow-partial", action="store_true")

    p_summary = sub.add_parser("summarize")
    p_summary.add_argument("run_dir", type=Path)

    sub.add_parser("self-test")

    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.run_dir, args.repo_ref, args.model_id, args.provider, args.seed)
    elif args.command == "validate-responses":
        validate_responses(args.run_dir, allow_partial=args.allow_partial)
    elif args.command == "prepare-judge":
        prepare_judge_tasks(args.run_dir, blind_seed=args.blind_seed)
    elif args.command == "validate-judgments":
        validate_judgments(args.run_dir, allow_partial=args.allow_partial)
    elif args.command == "summarize":
        summarize(args.run_dir)
    elif args.command == "self-test":
        self_test()


if __name__ == "__main__":
    main()
