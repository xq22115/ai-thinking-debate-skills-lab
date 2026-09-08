#!/usr/bin/env python3
"""Provider-neutral semantic dialogue-state behavioral evaluation harness.

The harness does not call a model provider. It prepares reproducible requests,
validates externally recorded candidate outputs, creates blinded judge tasks,
accepts one or more judgments per candidate, preserves judge disagreement, and
summarizes case-first arm-level results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import tempfile
from collections import defaultdict
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


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:20]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def dump_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: expected JSON object")
            rows.append(value)
    return rows


def dump_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def index_unique(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"{label}: missing non-empty {key}")
        if value in out:
            raise ValueError(f"{label}: duplicate {key}={value}")
        out[value] = row
    return out


def mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 4) if values else None


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

    run_id = (
        f"ds-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-"
        f"{stable_id(repo_ref, model_id, str(seed))[:8]}"
    )

    bundles: dict[str, dict[str, Any]] = {}
    for arm in ARMS:
        text = arm_bundle_text(arm)
        sources: list[str] = []
        if arm not in {"direct", "generic-careful"}:
            sources.append(str(CORE_SKILL.relative_to(ROOT)))
        if arm == "microscope-dialogue-state":
            sources.append(str(DIALOGUE_STATE.relative_to(ROOT)))
        bundles[arm] = {
            "arm": arm,
            "sha256": sha256_text(text),
            "instruction_text": text,
            "source_paths": sources,
        }

    requests: list[dict[str, Any]] = []
    for case in cases:
        for arm in ARMS:
            request_id = stable_id(run_id, case["id"], arm)
            requests.append(
                {
                    "request_id": request_id,
                    "run_id": run_id,
                    "case_id": case["id"],
                    "arm": arm,
                    "bundle_sha256": bundles[arm]["sha256"],
                    "input": case["input"],
                    "required_output": (
                        "concise auditable reasoning summary; no private chain-of-thought required"
                    ),
                }
            )

    manifest = {
        "schema_version": 2,
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

    request_ids = list(requests)
    random.Random(blind_seed).shuffle(request_ids)
    labels = {request_id: f"candidate-{idx + 1:03d}" for idx, request_id in enumerate(request_ids)}

    tasks: list[dict[str, Any]] = []
    for request_id in request_ids:
        request = requests[request_id]
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
                "candidate_output": responses[request_id]["output"],
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


def normalize_judgments(
    rows: list[dict[str, Any]], tasks: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_slots: set[tuple[str, str, str]] = set()

    for row in rows:
        task_id = row.get("judge_task_id")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("judgment: judge_task_id is required")
        if task_id not in tasks:
            raise ValueError(f"judgment references unknown judge_task_id={task_id}")

        judge = row.get("judge")
        if not isinstance(judge, dict) or not str(judge.get("id", "")).strip():
            raise ValueError(f"judgment {task_id}: judge.id is required")
        judge_id = str(judge["id"]).strip()
        variant_id = str(row.get("variant_id", "default")).strip() or "default"
        judgment_id = row.get("judgment_id")
        if judgment_id is None:
            judgment_id = stable_id("judgment", task_id, judge_id, variant_id)
        if not isinstance(judgment_id, str) or not judgment_id:
            raise ValueError(f"judgment {task_id}: judgment_id must be a non-empty string")
        if judgment_id in seen_ids:
            raise ValueError(f"duplicate judgment_id={judgment_id}")
        seen_ids.add(judgment_id)

        slot = (task_id, judge_id, variant_id)
        if slot in seen_slots:
            raise ValueError(
                "duplicate judgment slot for "
                f"task={task_id}, judge={judge_id}, variant={variant_id}; "
                "use a distinct variant_id for an intentional repeat/order-swap"
            )
        seen_slots.add(slot)

        item = dict(row)
        item["judgment_id"] = judgment_id
        item["variant_id"] = variant_id
        normalized.append(item)

    return normalized


def validate_judgments(run_dir: Path, allow_partial: bool = False) -> dict[str, Any]:
    tasks = index_unique(load_jsonl(run_dir / "judge_tasks.jsonl"), "judge_task_id", "judge tasks")
    judgments = normalize_judgments(load_jsonl(run_dir / "judgments.jsonl"), tasks)
    covered_tasks = {row["judge_task_id"] for row in judgments}
    missing = sorted(set(tasks) - covered_tasks)
    if missing and not allow_partial:
        raise ValueError(f"missing judgments for {len(missing)} judge tasks")

    judges_per_task: dict[str, set[str]] = defaultdict(set)
    for judgment in judgments:
        task_id = judgment["judge_task_id"]
        scores = judgment.get("scores")
        if not isinstance(scores, dict):
            raise ValueError(f"judgment {task_id}: scores must be an object")
        unknown_dims = set(scores) - set(DIMENSIONS)
        if unknown_dims:
            raise ValueError(f"judgment {task_id}: unknown dimensions {sorted(unknown_dims)}")
        for dim in DIMENSIONS:
            if scores.get(dim) not in (0, 1, 2, None):
                raise ValueError(f"judgment {task_id}: invalid score for {dim}: {scores.get(dim)}")

        blocks = judgment.get("blocking_errors", [])
        if not isinstance(blocks, list) or any(not isinstance(item, str) for item in blocks):
            raise ValueError(f"judgment {task_id}: blocking_errors must be a string list")
        unknown_blocks = set(blocks) - set(BLOCKING_ERROR_IDS)
        if unknown_blocks:
            raise ValueError(f"judgment {task_id}: unknown blocking errors {sorted(unknown_blocks)}")
        if judgment.get("request_id") not in (None, tasks[task_id]["request_id"]):
            raise ValueError(f"judgment {task_id}: request_id mismatch")
        judges_per_task[task_id].add(str(judgment["judge"]["id"]))

    summary = {
        "judge_tasks": len(tasks),
        "judgments": len(judgments),
        "tasks_covered": len(covered_tasks),
        "tasks_with_multiple_judges": sum(1 for ids in judges_per_task.values() if len(ids) > 1),
        "unique_judges": len({str(row["judge"]["id"]) for row in judgments}),
        "missing": len(missing),
        "complete": not missing,
    }
    print(json.dumps(summary, sort_keys=True))
    return summary


def aggregate_task_judgments(rows: list[dict[str, Any]]) -> dict[str, Any]:
    dimension_values: dict[str, list[float]] = {dim: [] for dim in DIMENSIONS}
    block_sets: list[set[str]] = []
    judge_ids: set[str] = set()
    same_model_exposure = False

    for judgment in rows:
        judge_ids.add(str(judgment["judge"]["id"]))
        same_model_exposure = same_model_exposure or (
            judgment.get("judge", {}).get("same_model_family_as_generator") is True
        )
        for dim in DIMENSIONS:
            value = judgment.get("scores", {}).get(dim)
            if value is not None:
                dimension_values[dim].append(float(value))
        block_sets.append(set(judgment.get("blocking_errors", [])))

    mean_by_dimension = {dim: mean(values) for dim, values in dimension_values.items()}
    overall = mean([float(v) for v in mean_by_dimension.values() if v is not None])
    dimension_disagreements = {
        dim: sorted(set(values))
        for dim, values in dimension_values.items()
        if len(set(values)) > 1
    }
    blocking_disagreement = len({tuple(sorted(blocks)) for blocks in block_sets}) > 1
    blocking_union = sorted(set().union(*block_sets)) if block_sets else []

    return {
        "judge_count": len(rows),
        "unique_judge_count": len(judge_ids),
        "same_model_judge_exposure": same_model_exposure,
        "mean_by_dimension": mean_by_dimension,
        "overall": overall,
        "blocked_any": any(block_sets),
        "blocked_all": bool(block_sets) and all(block_sets),
        "blocking_errors_union": blocking_union,
        "dimension_disagreements": dimension_disagreements,
        "blocking_disagreement": blocking_disagreement,
        "judge_disagreement": bool(dimension_disagreements) or blocking_disagreement,
    }


def summarize(run_dir: Path) -> dict[str, Any]:
    validate_judgments(run_dir, allow_partial=False)
    requests = index_unique(load_jsonl(run_dir / "requests.jsonl"), "request_id", "requests")
    tasks = index_unique(load_jsonl(run_dir / "judge_tasks.jsonl"), "judge_task_id", "judge tasks")
    judgments = normalize_judgments(load_jsonl(run_dir / "judgments.jsonl"), tasks)

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for judgment in judgments:
        grouped[judgment["judge_task_id"]].append(judgment)

    per_arm = {
        arm: {
            "cases_judged": 0,
            "blocked_cases": 0,
            "blocked_all_judges_cases": 0,
            "judge_disagreement_cases": 0,
            "dimension_values": {dim: [] for dim in DIMENSIONS},
            "overall_values": [],
            "judge_counts": [],
            "same_model_judge_cases": 0,
        }
        for arm in ARMS
    }
    per_case_arm: dict[tuple[str, str], dict[str, Any]] = {}
    disagreement_tasks: list[dict[str, Any]] = []

    for task_id, task_rows in grouped.items():
        task = tasks[task_id]
        request = requests[task["request_id"]]
        arm = request["arm"]
        agg = aggregate_task_judgments(task_rows)
        bucket = per_arm[arm]
        bucket["cases_judged"] += 1
        bucket["blocked_cases"] += int(agg["blocked_any"])
        bucket["blocked_all_judges_cases"] += int(agg["blocked_all"])
        bucket["judge_disagreement_cases"] += int(agg["judge_disagreement"])
        bucket["judge_counts"].append(float(agg["judge_count"]))
        bucket["same_model_judge_cases"] += int(agg["same_model_judge_exposure"])
        for dim in DIMENSIONS:
            value = agg["mean_by_dimension"][dim]
            if value is not None:
                bucket["dimension_values"][dim].append(float(value))
        if agg["overall"] is not None:
            bucket["overall_values"].append(float(agg["overall"]))

        per_case_arm[(request["case_id"], arm)] = {
            "overall": agg["overall"],
            "blocked": agg["blocked_any"],
            "blocked_all_judges": agg["blocked_all"],
            "blocking_errors": agg["blocking_errors_union"],
            "judge_disagreement": agg["judge_disagreement"],
            "judge_count": agg["judge_count"],
        }
        if agg["judge_disagreement"]:
            disagreement_tasks.append(
                {
                    "case_id": request["case_id"],
                    "arm": arm,
                    "judge_count": agg["judge_count"],
                    "dimension_disagreements": agg["dimension_disagreements"],
                    "blocking_disagreement": agg["blocking_disagreement"],
                }
            )

    arm_report: dict[str, Any] = {}
    for arm, bucket in per_arm.items():
        judged = bucket["cases_judged"]
        arm_report[arm] = {
            "cases_judged": judged,
            "blocked_cases": bucket["blocked_cases"],
            "blocking_error_rate": round(bucket["blocked_cases"] / judged, 4) if judged else None,
            "blocked_all_judges_cases": bucket["blocked_all_judges_cases"],
            "blocking_all_judges_rate": (
                round(bucket["blocked_all_judges_cases"] / judged, 4) if judged else None
            ),
            "judge_disagreement_cases": bucket["judge_disagreement_cases"],
            "judge_disagreement_rate": (
                round(bucket["judge_disagreement_cases"] / judged, 4) if judged else None
            ),
            "mean_judges_per_case": mean(bucket["judge_counts"]),
            "mean_overall_applicable_score": mean(bucket["overall_values"]),
            "mean_by_dimension": {
                dim: mean(bucket["dimension_values"][dim]) for dim in DIMENSIONS
            },
            "same_model_judge_cases": bucket["same_model_judge_cases"],
        }

    treatment = "microscope-dialogue-state"
    regression_cases: list[str] = []
    blocked_regressions: list[str] = []
    for case_id in sorted({case_id for case_id, _ in per_case_arm}):
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
        "schema_version": 2,
        "run_id": manifest["run_id"],
        "repo_ref": manifest["repo_ref"],
        "model_id": manifest["model_id"],
        "provider": manifest["provider"],
        "judgment_count": len(judgments),
        "arms": arm_report,
        "treatment_deltas": {
            "overall_vs_direct": delta(treatment, "direct", "mean_overall_applicable_score"),
            "overall_vs_microscope_core": delta(
                treatment, "microscope-core", "mean_overall_applicable_score"
            ),
            "blocking_rate_vs_direct": delta(treatment, "direct", "blocking_error_rate"),
            "blocking_rate_vs_microscope_core": delta(
                treatment, "microscope-core", "blocking_error_rate"
            ),
            "judge_disagreement_rate_vs_core": delta(
                treatment, "microscope-core", "judge_disagreement_rate"
            ),
        },
        "treatment_regression_cases_vs_core": regression_cases,
        "treatment_blocking_regressions_vs_core": blocked_regressions,
        "judge_disagreement_tasks": sorted(
            disagreement_tasks, key=lambda row: (row["case_id"], row["arm"])
        ),
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
        dump_jsonl(
            run_dir / "responses.jsonl",
            [
                {
                    "request_id": row["request_id"],
                    "case_id": row["case_id"],
                    "arm": row["arm"],
                    "output": f"Synthetic auditable output for {row['case_id']} / {row['arm']}",
                }
                for row in requests
            ],
        )
        validate_responses(run_dir)
        prepare_judge_tasks(run_dir, blind_seed=11)
        tasks = load_jsonl(run_dir / "judge_tasks.jsonl")
        req_index = index_unique(requests, "request_id", "requests")

        judgments: list[dict[str, Any]] = []
        disagreement_injected = False
        for task in tasks:
            arm = req_index[task["request_id"]]["arm"]
            base_score = 2 if arm == "microscope-dialogue-state" else 1
            for judge_idx, judge_id in enumerate(
                ("synthetic-independent-judge-a", "synthetic-independent-judge-b")
            ):
                score = base_score
                if arm == "direct" and judge_idx == 1 and not disagreement_injected:
                    score = 0
                    disagreement_injected = True
                judgments.append(
                    {
                        "judgment_id": stable_id(
                            "self-test-judgment", task["judge_task_id"], judge_id
                        ),
                        "judge_task_id": task["judge_task_id"],
                        "request_id": task["request_id"],
                        "scores": {dim: score for dim in DIMENSIONS},
                        "blocking_errors": [],
                        "judge": {
                            "id": judge_id,
                            "same_model_family_as_generator": False,
                        },
                    }
                )

        assert disagreement_injected
        dump_jsonl(run_dir / "judgments.jsonl", judgments)
        validation = validate_judgments(run_dir)
        assert validation["tasks_with_multiple_judges"] == len(tasks)
        report = summarize(run_dir)
        assert report["treatment_deltas"]["overall_vs_microscope_core"] == 1.0
        assert report["treatment_blocking_regressions_vs_core"] == []
        assert report["judge_disagreement_tasks"]
        assert report["arms"]["direct"]["judge_disagreement_cases"] >= 1
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
