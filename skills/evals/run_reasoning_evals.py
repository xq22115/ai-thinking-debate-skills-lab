#!/usr/bin/env python3
"""Provider-neutral reasoning evaluation scorer.

This runner DOES NOT call a model. It consumes already-produced target responses
plus an optional private oracle, verified commit-reveal receipt, and optional
independent-judge results. It scores only what the supplied artifacts justify and
computes the highest evidence class supported by explicit separation/receipt
metadata.

This design intentionally keeps target execution, response freezing, private
scoring, commitment verification, and evidence promotion separate so a repository
harness cannot pretend it created fresh-context, private-oracle, independent-judge,
hidden-holdout, multi-agent, or host-live evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

EVIDENCE_LEVELS = [
    "FIXTURE_SPECIFIED",
    "STATIC_VALIDATED",
    "SAME_MODEL_SMOKE",
    "FRESH_CONTEXT_RUN",
    "PRIVATE_ORACLE_SCORED",
    "INDEPENDENT_JUDGED",
    "PERTURBED_HIDDEN",
    "UNSEEN_ADVERSARIAL",
    "REPEATED",
    "AUTHENTIC_MULTI_AGENT_RUNTIME",
    "HOST_LIVE_REGRESSION",
]


class EvalError(ValueError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - fail-closed CLI boundary
        raise EvalError(f"failed to parse JSON {path}: {exc}") from exc


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw.strip():
                continue
            item = json.loads(raw)
            if not isinstance(item, dict):
                raise EvalError(f"{path}:{line_no}: JSONL record must be an object")
            rows.append(item)
    except EvalError:
        raise
    except Exception as exc:  # pragma: no cover
        raise EvalError(f"failed to parse JSONL {path}: {exc}") from exc
    return rows


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvalError(message)


def index_unique(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        require(isinstance(value, str) and value, f"{label}: missing non-empty {key}")
        require(value not in out, f"{label}: duplicate {key}={value}")
        out[value] = row
    return out


def normalize_manifest(manifest: dict[str, Any]) -> None:
    require(manifest.get("schema_version") == "1.0", "manifest.schema_version must be 1.0")
    require(isinstance(manifest.get("suite"), str) and manifest["suite"], "manifest.suite required")
    require(isinstance(manifest.get("run_id"), str) and manifest["run_id"], "manifest.run_id required")
    require(isinstance(manifest.get("execution"), dict), "manifest.execution required")
    require(isinstance(manifest.get("contamination"), dict), "manifest.contamination required")
    require(isinstance(manifest.get("holdout"), dict), "manifest.holdout required")
    require(isinstance(manifest.get("judging", {}), dict), "manifest.judging must be object")


def validate_response_rows(manifest: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed = index_unique(rows, "case_id", "responses")
    run_id = manifest["run_id"]
    for case_id, row in indexed.items():
        require(row.get("run_id") == run_id, f"responses[{case_id}].run_id mismatch")
        require(isinstance(row.get("output"), dict), f"responses[{case_id}].output must be object")
    return indexed


def validate_judgment_rows(manifest: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed = index_unique(rows, "case_id", "judgments")
    run_id = manifest["run_id"]
    for case_id, row in indexed.items():
        require(row.get("run_id") == run_id, f"judgments[{case_id}].run_id mismatch")
        require(isinstance(row.get("pass"), bool), f"judgments[{case_id}].pass must be boolean")
    return indexed


def validate_reveal_receipt(manifest: dict[str, Any], responses: list[dict[str, Any]],
                            oracle: dict[str, Any], receipt: dict[str, Any]) -> bool:
    require(receipt.get("schema_version") == "1.0", "reveal receipt schema_version must be 1.0")
    require(receipt.get("status") == "PASS_COMMITMENT_REVEAL", "reveal receipt must be PASS_COMMITMENT_REVEAL")
    require(receipt.get("verified") is True, "reveal receipt verified must be true")
    require(receipt.get("commitment_algorithm") == "SHA256-SALTED-CANONICAL-JSON-v1",
            "reveal receipt commitment algorithm mismatch")
    require(receipt.get("suite") == manifest["suite"], "reveal receipt suite mismatch")
    require(receipt.get("run_id") == manifest["run_id"], "reveal receipt run_id mismatch")
    require(receipt.get("manifest_sha256") == canonical_hash(manifest),
            "reveal receipt manifest hash mismatch")
    require(receipt.get("oracle_canonical_sha256") == canonical_hash(oracle),
            "reveal receipt oracle hash mismatch")
    normalized = sorted(responses, key=lambda row: row.get("case_id", ""))
    require(receipt.get("responses_canonical_sha256") == canonical_hash(normalized),
            "reveal receipt response-set hash mismatch")
    require(receipt.get("response_count") == len(responses), "reveal receipt response_count mismatch")
    freeze_hash = receipt.get("freeze_receipt_sha256")
    commitment_hash = receipt.get("commitment_receipt_sha256")
    require(isinstance(freeze_hash, str) and len(freeze_hash) == 64,
            "reveal receipt freeze_receipt_sha256 missing")
    require(isinstance(commitment_hash, str) and len(commitment_hash) == 64,
            "reveal receipt commitment_receipt_sha256 missing")
    return True


def score_label_set(case_id: str, output: dict[str, Any], scoring: dict[str, Any]) -> dict[str, Any]:
    labels = output.get("labels")
    if not isinstance(labels, list) or not all(isinstance(x, str) for x in labels):
        return case_result(case_id, "LABEL_SET", "FAIL", ["output.labels must be list[str]"])
    observed = set(labels)
    required = set(scoring.get("must_detect", []))
    forbidden = set(scoring.get("fail_if", []))
    missing = sorted(required - observed)
    forbidden_hit = sorted(forbidden & observed)
    reasons: list[str] = []
    if missing:
        reasons.append("missing_required:" + ",".join(missing))
    if forbidden_hit:
        reasons.append("forbidden_observed:" + ",".join(forbidden_hit))
    return case_result(case_id, "LABEL_SET", "PASS" if not reasons else "FAIL", reasons or ["required labels present; forbidden labels absent"])


def score_exact(case_id: str, output: dict[str, Any], scoring: dict[str, Any]) -> dict[str, Any]:
    field = scoring.get("field")
    require(isinstance(field, str) and field, f"oracle {case_id}: EXACT_VALUE field required")
    expected = scoring.get("expected")
    observed = output.get(field)
    if observed == expected:
        return case_result(case_id, "EXACT_VALUE", "PASS", [f"{field} matched private oracle"])
    return case_result(case_id, "EXACT_VALUE", "FAIL", [f"{field} mismatch"])


def score_semantic_judge(case_id: str, judgment: dict[str, Any] | None) -> dict[str, Any]:
    if judgment is None:
        return case_result(case_id, "SEMANTIC_JUDGE", "UNSCORED", ["independent judgment missing"])
    reasons = judgment.get("reasons")
    if not isinstance(reasons, list) or not all(isinstance(x, str) for x in reasons):
        reasons = ["judge boolean result supplied"]
    return case_result(case_id, "SEMANTIC_JUDGE", "PASS" if judgment["pass"] else "FAIL", reasons)


def case_result(case_id: str, mode: str, result: str, reasons: list[str], *, response: Any | None = None,
                judgment: Any | None = None) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "scoring_mode": mode,
        "result": result,
        "reasons": reasons,
        "response_sha256": canonical_hash(response) if response is not None else None,
        "judge_sha256": canonical_hash(judgment) if judgment is not None else None,
    }


def score_oracle_cases(oracle: dict[str, Any], responses: dict[str, dict[str, Any]],
                       judgments: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    require(oracle.get("schema_version") == "1.0", "oracle.schema_version must be 1.0")
    oracle_cases = oracle.get("cases", [])
    require(isinstance(oracle_cases, list), "oracle.cases must be array")
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in oracle_cases:
        require(isinstance(item, dict), "oracle case must be object")
        case_id = item.get("case_id")
        require(isinstance(case_id, str) and case_id, "oracle case_id required")
        require(case_id not in seen, f"duplicate oracle case_id={case_id}")
        seen.add(case_id)
        scoring = item.get("scoring")
        require(isinstance(scoring, dict), f"oracle {case_id}: scoring object required")
        mode = scoring.get("mode")
        response = responses.get(case_id)
        if response is None:
            results.append(case_result(case_id, mode if isinstance(mode, str) else "UNSCORED", "UNSCORED", ["target response missing"]))
            continue
        output = response["output"]
        if mode == "LABEL_SET":
            result = score_label_set(case_id, output, scoring)
        elif mode == "EXACT_VALUE":
            result = score_exact(case_id, output, scoring)
        elif mode == "SEMANTIC_JUDGE":
            result = score_semantic_judge(case_id, judgments.get(case_id))
        else:
            result = case_result(case_id, "UNSCORED", "UNSCORED", [f"unsupported scoring mode: {mode!r}"])
        result["response_sha256"] = canonical_hash(response)
        if case_id in judgments:
            result["judge_sha256"] = canonical_hash(judgments[case_id])
        results.append(result)
    return results


def score_pair_rules(oracle: dict[str, Any], responses: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    pair_rules = oracle.get("pair_rules", [])
    require(isinstance(pair_rules, list), "oracle.pair_rules must be array")
    results: list[dict[str, Any]] = []
    for rule in pair_rules:
        require(isinstance(rule, dict), "pair rule must be object")
        pair_id = rule.get("pair_id")
        left_id = rule.get("left_case_id")
        right_id = rule.get("right_case_id")
        field = rule.get("field")
        relation = rule.get("relation", "EQUAL")
        require(all(isinstance(x, str) and x for x in [pair_id, left_id, right_id, field]),
                "pair_id/left_case_id/right_case_id/field required")
        left = responses.get(left_id)
        right = responses.get(right_id)
        case_id = f"PAIR::{pair_id}"
        if left is None or right is None:
            results.append(case_result(case_id, "PAIR_RELATION", "UNSCORED", ["both paired executions are required"]))
            continue
        lv = left["output"].get(field)
        rv = right["output"].get(field)
        if relation == "EQUAL":
            passed = lv == rv
        elif relation == "NOT_EQUAL":
            passed = lv != rv
        else:
            results.append(case_result(case_id, "PAIR_RELATION", "UNSCORED", [f"unsupported relation: {relation}"]))
            continue
        reasons = [f"{field} relation {relation} satisfied"] if passed else [f"{field} relation {relation} violated"]
        results.append(case_result(case_id, "PAIR_RELATION", "PASS" if passed else "FAIL", reasons,
                                   response={"left": left, "right": right}))
    return results


def infer_status(results: list[dict[str, Any]]) -> str:
    counts = {name: sum(1 for r in results if r["result"] == name) for name in ["PASS", "FAIL", "PARTIAL", "UNSCORED"]}
    if counts["FAIL"]:
        return "FAIL"
    if counts["UNSCORED"] and counts["PASS"]:
        return "PARTIAL"
    if counts["UNSCORED"] and not counts["PASS"]:
        return "UNSCORED_REQUIRES_JUDGE"
    if counts["PARTIAL"]:
        return "PARTIAL"
    return "PASS"


def promote_evidence(manifest: dict[str, Any], oracle_present: bool, oracle_hash: str | None,
                     private_scored_count: int, judgment_count: int, scored_pair_count: int,
                     commitment_reveal_verified: bool) -> tuple[str, list[str], list[str]]:
    execution = manifest.get("execution", {})
    contamination = manifest.get("contamination", {})
    holdout = manifest.get("holdout", {})
    judging = manifest.get("judging", {})

    level = "STATIC_VALIDATED"
    blockers: list[str] = []
    next_required: list[str] = []

    if not execution.get("target_executed"):
        blockers.append("target execution not evidenced")
        next_required.append("execute target and freeze response artifact")
        return level, blockers, next_required

    level = "SAME_MODEL_SMOKE"

    fresh_ok = execution.get("fresh_context") is True and contamination.get("expected_labels_visible_to_generator") is False
    if fresh_ok:
        level = "FRESH_CONTEXT_RUN"
    else:
        blockers.append("fresh context and hidden expected labels not both evidenced")
        next_required.append("fresh-context target run with expected labels withheld")
        return level, blockers, next_required

    oracle_ok = (
        oracle_present
        and bool(oracle_hash)
        and holdout.get("private_oracle_separated") is True
        and execution.get("responses_frozen_before_scoring") is True
        and private_scored_count > 0
        and commitment_reveal_verified
    )
    if oracle_ok:
        level = "PRIVATE_ORACLE_SCORED"
    else:
        blockers.append("private oracle separation/frozen-response/actual-scoring/commit-reveal proof incomplete")
        next_required.append("verify salted pre-run commitment against frozen responses and revealed oracle, then score at least one case")
        return level, blockers, next_required

    independent_judge_ok = (
        judging.get("independent") is True
        and judgment_count > 0
        and bool(judging.get("judge_receipts"))
    )
    if independent_judge_ok:
        level = "INDEPENDENT_JUDGED"
    else:
        blockers.append("independent judge evidence incomplete")
        next_required.append("independent judge or equivalent separated adjudication with receipt")
        return level, blockers, next_required

    hidden_ok = (
        holdout.get("hidden_variant") is True
        and holdout.get("variant_hidden_from_generator") is True
        and scored_pair_count > 0
    )
    if hidden_ok:
        level = "PERTURBED_HIDDEN"
    else:
        blockers.append("hidden perturbation relation not actually scored")
        next_required.append("execute both sides of at least one hidden paired/metamorphic relation and score it")
        return level, blockers, next_required

    if holdout.get("unseen_adversarial") is True:
        level = "UNSEEN_ADVERSARIAL"
    else:
        blockers.append("unseen adversarial generation not evidenced")
        next_required.append("independently/procedurally generate unseen adversarial cases")
        return level, blockers, next_required

    repeat_count = execution.get("repeat_count", 0)
    if isinstance(repeat_count, int) and repeat_count >= 3:
        level = "REPEATED"
    else:
        blockers.append("repeat count below minimum 3")
        next_required.append("repeat run sufficiently to estimate variance/calibration")
        return level, blockers, next_required

    multiagent_ok = (
        execution.get("authentic_multi_agent_runtime") is True
        and execution.get("runtime_independent") is True
        and len(execution.get("execution_receipts", [])) >= 2
    )
    if multiagent_ok:
        level = "AUTHENTIC_MULTI_AGENT_RUNTIME"
    else:
        blockers.append("authentic multi-agent runtime receipts incomplete")
        next_required.append("collect runtime-separated multi-agent receipts where the claim requires it")
        return level, blockers, next_required

    host_ok = execution.get("host_live_verified") is True and bool(execution.get("host_receipts"))
    if host_ok:
        level = "HOST_LIVE_REGRESSION"
    else:
        blockers.append("host-live receipt missing")
        next_required.append("run target-host regression and retain host receipt")

    return level, blockers, next_required


def make_result(manifest: dict[str, Any], responses: list[dict[str, Any]], oracle: dict[str, Any] | None,
                judgments: list[dict[str, Any]], oracle_hash: str | None,
                reveal_receipt: dict[str, Any] | None) -> dict[str, Any]:
    normalize_manifest(manifest)
    response_index = validate_response_rows(manifest, responses)
    judgment_index = validate_judgment_rows(manifest, judgments) if judgments else {}

    commitment_reveal_verified = False
    if reveal_receipt is not None:
        require(oracle is not None, "reveal receipt supplied without private oracle")
        commitment_reveal_verified = validate_reveal_receipt(manifest, responses, oracle, reveal_receipt)

    results: list[dict[str, Any]] = []
    if oracle is not None:
        require(oracle.get("suite") == manifest["suite"], "oracle.suite mismatch")
        require(oracle.get("run_id") == manifest["run_id"], "oracle.run_id mismatch")
        results.extend(score_oracle_cases(oracle, response_index, judgment_index))
        pair_results = score_pair_rules(oracle, response_index)
        results.extend(pair_results)
    else:
        pair_results = []
        for case_id, response in sorted(response_index.items()):
            results.append(case_result(case_id, "UNSCORED", "UNSCORED", ["private oracle not supplied"], response=response))

    counts = {name: sum(1 for r in results if r["result"] == name) for name in ["PASS", "FAIL", "PARTIAL", "UNSCORED"]}
    pair_failures = sum(1 for r in pair_results if r["result"] == "FAIL")
    scored_pair_count = sum(1 for r in pair_results if r["result"] in {"PASS", "FAIL"})
    private_scored_count = sum(
        1
        for r in results
        if r["result"] in {"PASS", "FAIL"}
        and r["scoring_mode"] in {"LABEL_SET", "EXACT_VALUE", "PAIR_RELATION"}
    )
    level, blockers, next_required = promote_evidence(
        manifest,
        oracle_present=oracle is not None,
        oracle_hash=oracle_hash,
        private_scored_count=private_scored_count,
        judgment_count=len(judgments),
        scored_pair_count=scored_pair_count,
        commitment_reveal_verified=commitment_reveal_verified,
    )

    execution_in = manifest.get("execution", {})
    judging_in = manifest.get("judging", {})
    holdout_in = manifest.get("holdout", {})
    contamination_in = manifest.get("contamination", {})

    result = {
        "schema_version": "1.0",
        "suite": manifest["suite"],
        "run_id": manifest["run_id"],
        "created_at": manifest.get("created_at"),
        "status": infer_status(results),
        "evidence_class": level,
        "contamination": {
            "authoring_overlap": contamination_in.get("authoring_overlap"),
            "fixture_visible_to_generator": contamination_in.get("fixture_visible_to_generator"),
            "expected_labels_visible_to_generator": contamination_in.get("expected_labels_visible_to_generator"),
            "notes": contamination_in.get("notes"),
        },
        "execution": {
            "target_executed": bool(execution_in.get("target_executed")),
            "fresh_context": execution_in.get("fresh_context"),
            "runtime_independent": execution_in.get("runtime_independent"),
            "responses_frozen_before_scoring": execution_in.get("responses_frozen_before_scoring"),
            "response_count": len(responses),
            "repeat_count": execution_in.get("repeat_count", 0) if isinstance(execution_in.get("repeat_count", 0), int) else 0,
            "target_id": execution_in.get("target_id"),
            "execution_receipts": execution_in.get("execution_receipts", []),
            "authentic_multi_agent_runtime": execution_in.get("authentic_multi_agent_runtime"),
            "host_live_verified": bool(execution_in.get("host_live_verified", False)),
            "host_receipts": execution_in.get("host_receipts", []),
        },
        "judging": {
            "mode": judging_in.get("mode", "NONE"),
            "independent": judging_in.get("independent"),
            "judgment_count": len(judgments),
            "judge_id": judging_in.get("judge_id"),
            "judge_receipts": judging_in.get("judge_receipts", []),
        },
        "holdout": {
            "private_oracle_separated": holdout_in.get("private_oracle_separated"),
            "hidden_variant": holdout_in.get("hidden_variant"),
            "variant_hidden_from_generator": holdout_in.get("variant_hidden_from_generator"),
            "oracle_hash_present": bool(oracle_hash),
            "commitment_reveal_verified": commitment_reveal_verified,
            "unseen_adversarial": holdout_in.get("unseen_adversarial"),
            "oracle_sha256": oracle_hash,
            "oracle_canonical_sha256": canonical_hash(oracle) if oracle is not None else None,
            "public_manifest_sha256": canonical_hash(manifest),
            "reveal_receipt_sha256": canonical_hash(reveal_receipt) if reveal_receipt is not None else None,
        },
        "summary": {
            "total": len(results),
            "passed": counts["PASS"],
            "failed": counts["FAIL"],
            "partial": counts["PARTIAL"],
            "unscored": counts["UNSCORED"],
            "pair_groups": len(pair_results),
            "pair_failures": pair_failures,
        },
        "cases": results,
        "promotion": {
            "max_evidence_class": level,
            "blocking_reasons": blockers,
            "next_required_evidence": next_required,
        },
    }
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True, help="public generation/run manifest JSON")
    parser.add_argument("--responses", type=Path, required=True, help="frozen target responses JSONL")
    parser.add_argument("--oracle", type=Path, help="private oracle JSON; keep outside public repo for reusable holdouts")
    parser.add_argument("--reveal-receipt", type=Path,
                        help="verified commit-reveal receipt binding manifest, frozen responses and oracle")
    parser.add_argument("--judgments", type=Path, help="independent judge results JSONL")
    parser.add_argument("--out", type=Path, help="write result receipt JSON instead of stdout only")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        manifest = load_json(args.manifest)
        require(isinstance(manifest, dict), "manifest must be object")
        responses = load_jsonl(args.responses)
        oracle = load_json(args.oracle) if args.oracle else None
        if oracle is not None:
            require(isinstance(oracle, dict), "oracle must be object")
        reveal_receipt = load_json(args.reveal_receipt) if args.reveal_receipt else None
        if reveal_receipt is not None:
            require(isinstance(reveal_receipt, dict), "reveal receipt must be object")
        judgments = load_jsonl(args.judgments) if args.judgments else []
        oracle_hash = sha256_bytes(args.oracle.read_bytes()) if args.oracle else None
        result = make_result(manifest, responses, oracle, judgments, oracle_hash, reveal_receipt)
    except EvalError as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
