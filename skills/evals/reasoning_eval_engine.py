#!/usr/bin/env python3
"""Attestation-gated provider-neutral reasoning evaluation engine.

The engine never calls a model. It scores frozen responses and promotes evidence
only when each evidence rung is backed by the artifact class that owns that claim.
In particular, a public manifest may describe a fresh-context run, but it cannot
promote to FRESH_CONTEXT_RUN without a hash-bound owning-runtime/external-job
execution receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from verify_target_execution_receipt import ReceiptError, verify_receipt

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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvalError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise EvalError(f"failed to parse JSON {path}: {exc}") from exc


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise EvalError(f"{path}:{line_no}: JSONL record must be object")
            rows.append(value)
    except EvalError:
        raise
    except Exception as exc:
        raise EvalError(f"failed to parse JSONL {path}: {exc}") from exc
    return rows


def index_unique(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        require(isinstance(value, str) and value, f"{label}: missing non-empty {key}")
        require(value not in indexed, f"{label}: duplicate {key}={value}")
        indexed[value] = row
    return indexed


def validate_manifest(manifest: dict[str, Any]) -> None:
    require(manifest.get("schema_version") == "1.0", "manifest.schema_version must be 1.0")
    require(isinstance(manifest.get("suite"), str) and manifest["suite"], "manifest.suite required")
    require(isinstance(manifest.get("run_id"), str) and manifest["run_id"], "manifest.run_id required")
    for key in ("execution", "contamination", "holdout"):
        require(isinstance(manifest.get(key), dict), f"manifest.{key} required")
    require(isinstance(manifest.get("judging", {}), dict), "manifest.judging must be object")


def validate_responses(manifest: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed = index_unique(rows, "case_id", "responses")
    for case_id, row in indexed.items():
        require(row.get("run_id") == manifest["run_id"], f"responses[{case_id}].run_id mismatch")
        require(isinstance(row.get("output"), dict), f"responses[{case_id}].output must be object")
    return indexed


def validate_judgments(manifest: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed = index_unique(rows, "case_id", "judgments")
    for case_id, row in indexed.items():
        require(row.get("run_id") == manifest["run_id"], f"judgments[{case_id}].run_id mismatch")
        require(isinstance(row.get("pass"), bool), f"judgments[{case_id}].pass must be boolean")
    return indexed


def validate_reveal_receipt(manifest: dict[str, Any], responses: list[dict[str, Any]], oracle: dict[str, Any], receipt: dict[str, Any]) -> bool:
    require(receipt.get("schema_version") == "1.0", "reveal receipt schema_version must be 1.0")
    require(receipt.get("status") == "PASS_COMMITMENT_REVEAL", "reveal receipt must be PASS_COMMITMENT_REVEAL")
    require(receipt.get("verified") is True, "reveal receipt verified must be true")
    require(receipt.get("commitment_algorithm") == "SHA256-SALTED-CANONICAL-JSON-v1", "reveal receipt commitment algorithm mismatch")
    require(receipt.get("suite") == manifest["suite"], "reveal receipt suite mismatch")
    require(receipt.get("run_id") == manifest["run_id"], "reveal receipt run_id mismatch")
    require(receipt.get("manifest_sha256") == canonical_hash(manifest), "reveal receipt manifest hash mismatch")
    require(receipt.get("oracle_canonical_sha256") == canonical_hash(oracle), "reveal receipt oracle hash mismatch")
    normalized = sorted(responses, key=lambda row: row.get("case_id", ""))
    require(receipt.get("responses_canonical_sha256") == canonical_hash(normalized), "reveal receipt response-set hash mismatch")
    require(receipt.get("response_count") == len(responses), "reveal receipt response_count mismatch")
    require(isinstance(receipt.get("freeze_receipt_sha256"), str) and len(receipt["freeze_receipt_sha256"]) == 64,
            "reveal receipt freeze_receipt_sha256 missing")
    require(isinstance(receipt.get("commitment_receipt_sha256"), str) and len(receipt["commitment_receipt_sha256"]) == 64,
            "reveal receipt commitment_receipt_sha256 missing")
    return True


def case_result(case_id: str, mode: str, result: str, reasons: list[str], response: Any | None = None,
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
    cases = oracle.get("cases", [])
    require(isinstance(cases, list), "oracle.cases must be array")
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in cases:
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
            results.append(case_result(case_id, str(mode or "UNSCORED"), "UNSCORED", ["target response missing"]))
            continue
        output = response["output"]
        if mode == "LABEL_SET":
            labels = output.get("labels")
            if not isinstance(labels, list) or not all(isinstance(v, str) for v in labels):
                result = case_result(case_id, mode, "FAIL", ["output.labels must be list[str]"])
            else:
                observed = set(labels)
                missing = sorted(set(scoring.get("must_detect", [])) - observed)
                forbidden = sorted(set(scoring.get("fail_if", [])) & observed)
                reasons = []
                if missing:
                    reasons.append("missing_required:" + ",".join(missing))
                if forbidden:
                    reasons.append("forbidden_observed:" + ",".join(forbidden))
                result = case_result(case_id, mode, "PASS" if not reasons else "FAIL",
                                     reasons or ["required labels present; forbidden labels absent"])
        elif mode == "EXACT_VALUE":
            field = scoring.get("field")
            require(isinstance(field, str) and field, f"oracle {case_id}: EXACT_VALUE field required")
            passed = output.get(field) == scoring.get("expected")
            result = case_result(case_id, mode, "PASS" if passed else "FAIL",
                                 [f"{field} matched private oracle"] if passed else [f"{field} mismatch"])
        elif mode == "SEMANTIC_JUDGE":
            judgment = judgments.get(case_id)
            if judgment is None:
                result = case_result(case_id, mode, "UNSCORED", ["independent judgment missing"])
            else:
                reasons = judgment.get("reasons")
                if not isinstance(reasons, list) or not all(isinstance(v, str) for v in reasons):
                    reasons = ["judge boolean result supplied"]
                result = case_result(case_id, mode, "PASS" if judgment["pass"] else "FAIL", reasons,
                                     judgment=judgment)
        else:
            result = case_result(case_id, "UNSCORED", "UNSCORED", [f"unsupported scoring mode: {mode!r}"])
        result["response_sha256"] = canonical_hash(response)
        if case_id in judgments:
            result["judge_sha256"] = canonical_hash(judgments[case_id])
        results.append(result)
    return results


def score_pair_rules(oracle: dict[str, Any], responses: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rules = oracle.get("pair_rules", [])
    require(isinstance(rules, list), "oracle.pair_rules must be array")
    results: list[dict[str, Any]] = []
    for rule in rules:
        require(isinstance(rule, dict), "pair rule must be object")
        pair_id, left_id, right_id, field = (rule.get(k) for k in ("pair_id", "left_case_id", "right_case_id", "field"))
        require(all(isinstance(v, str) and v for v in (pair_id, left_id, right_id, field)),
                "pair_id/left_case_id/right_case_id/field required")
        relation = rule.get("relation", "EQUAL")
        left, right = responses.get(left_id), responses.get(right_id)
        case_id = f"PAIR::{pair_id}"
        if left is None or right is None:
            results.append(case_result(case_id, "PAIR_RELATION", "UNSCORED", ["both paired executions are required"]))
            continue
        lv, rv = left["output"].get(field), right["output"].get(field)
        if relation == "EQUAL":
            passed = lv == rv
        elif relation == "NOT_EQUAL":
            passed = lv != rv
        else:
            results.append(case_result(case_id, "PAIR_RELATION", "UNSCORED", [f"unsupported relation: {relation}"]))
            continue
        results.append(case_result(case_id, "PAIR_RELATION", "PASS" if passed else "FAIL",
                                   [f"{field} relation {relation} satisfied"] if passed else [f"{field} relation {relation} violated"],
                                   response={"left": left, "right": right}))
    return results


def infer_status(results: list[dict[str, Any]]) -> str:
    counts = {name: sum(1 for r in results if r["result"] == name) for name in ("PASS", "FAIL", "PARTIAL", "UNSCORED")}
    if counts["FAIL"]:
        return "FAIL"
    if counts["UNSCORED"] and counts["PASS"]:
        return "PARTIAL"
    if counts["UNSCORED"]:
        return "UNSCORED_REQUIRES_JUDGE"
    if counts["PARTIAL"]:
        return "PARTIAL"
    return "PASS"


def promote_evidence(manifest: dict[str, Any], *, oracle_present: bool, oracle_hash: str | None,
                     private_scored_count: int, independent_judged_count: int, scored_pair_count: int,
                     commitment_reveal_verified: bool, execution_receipt_verified: bool,
                     fresh_context_claim_verified: bool, runtime_independence_claim_verified: bool) -> tuple[str, list[str], list[str]]:
    execution = manifest.get("execution", {})
    contamination = manifest.get("contamination", {})
    holdout = manifest.get("holdout", {})
    judging = manifest.get("judging", {})
    blockers: list[str] = []
    next_required: list[str] = []
    level = "STATIC_VALIDATED"

    if not execution.get("target_executed"):
        return level, ["target execution not evidenced"], ["execute target and freeze response artifact"]
    level = "SAME_MODEL_SMOKE"

    fresh_ok = (
        execution_receipt_verified
        and fresh_context_claim_verified
        and execution.get("fresh_context") is True
        and contamination.get("expected_labels_visible_to_generator") is False
    )
    if not fresh_ok:
        blockers.append("fresh-context claim lacks a hash-bound owning-runtime/external-job execution receipt")
        next_required.append("supply target execution receipt binding manifest/responses and attesting fresh context with expected labels withheld")
        return level, blockers, next_required
    level = "FRESH_CONTEXT_RUN"

    oracle_ok = (
        oracle_present and bool(oracle_hash)
        and holdout.get("private_oracle_separated") is True
        and execution.get("responses_frozen_before_scoring") is True
        and private_scored_count > 0
        and commitment_reveal_verified
    )
    if not oracle_ok:
        blockers.append("private oracle separation/frozen-response/actual-scoring/commit-reveal proof incomplete")
        next_required.append("verify salted pre-run commitment against frozen responses and revealed oracle, then score at least one case")
        return level, blockers, next_required
    level = "PRIVATE_ORACLE_SCORED"

    judge_ok = judging.get("independent") is True and independent_judged_count > 0 and bool(judging.get("judge_receipts"))
    if not judge_ok:
        blockers.append("independent judge did not score an actual SEMANTIC_JUDGE case with a receipt")
        next_required.append("independent judge must score at least one designated semantic case and retain a judge receipt")
        return level, blockers, next_required
    level = "INDEPENDENT_JUDGED"

    hidden_ok = holdout.get("hidden_variant") is True and holdout.get("variant_hidden_from_generator") is True and scored_pair_count > 0
    if not hidden_ok:
        blockers.append("hidden perturbation relation not actually scored")
        next_required.append("execute both sides of at least one hidden paired/metamorphic relation and score it")
        return level, blockers, next_required
    level = "PERTURBED_HIDDEN"

    if holdout.get("unseen_adversarial") is not True:
        blockers.append("unseen adversarial generation not evidenced")
        next_required.append("independently/procedurally generate unseen adversarial cases")
        return level, blockers, next_required
    level = "UNSEEN_ADVERSARIAL"

    repeat_count = execution.get("repeat_count", 0)
    if not isinstance(repeat_count, int) or repeat_count < 3:
        blockers.append("repeat count below minimum 3")
        next_required.append("repeat run sufficiently to estimate variance/calibration")
        return level, blockers, next_required
    level = "REPEATED"

    multiagent_ok = (
        execution.get("authentic_multi_agent_runtime") is True
        and runtime_independence_claim_verified
        and len(execution.get("execution_receipts", [])) >= 2
    )
    if not multiagent_ok:
        blockers.append("authentic multi-agent runtime receipts incomplete")
        next_required.append("collect runtime-separated multi-agent receipts where the claim requires it")
        return level, blockers, next_required
    level = "AUTHENTIC_MULTI_AGENT_RUNTIME"

    if execution.get("host_live_verified") is True and bool(execution.get("host_receipts")):
        level = "HOST_LIVE_REGRESSION"
    else:
        blockers.append("host-live receipt missing")
        next_required.append("run target-host regression and retain host receipt")
    return level, blockers, next_required


def make_result(manifest: dict[str, Any], responses: list[dict[str, Any]], oracle: dict[str, Any] | None,
                judgments: list[dict[str, Any]], oracle_hash: str | None,
                reveal_receipt: dict[str, Any] | None, execution_receipt: dict[str, Any] | None) -> dict[str, Any]:
    validate_manifest(manifest)
    response_index = validate_responses(manifest, responses)
    judgment_index = validate_judgments(manifest, judgments) if judgments else {}

    exec_check: dict[str, Any] | None = None
    if execution_receipt is not None:
        try:
            exec_check = verify_receipt(manifest, responses, execution_receipt)
        except ReceiptError as exc:
            raise EvalError(str(exc)) from exc
    execution_receipt_verified = bool(exec_check and exec_check.get("verified") is True)
    fresh_context_claim_verified = bool(exec_check and exec_check.get("fresh_context_claim_verified") is True)
    runtime_independence_claim_verified = bool(exec_check and exec_check.get("runtime_independence_claim_verified") is True)

    commitment_reveal_verified = False
    if reveal_receipt is not None:
        require(oracle is not None, "reveal receipt supplied without private oracle")
        commitment_reveal_verified = validate_reveal_receipt(manifest, responses, oracle, reveal_receipt)

    if oracle is not None:
        require(oracle.get("suite") == manifest["suite"], "oracle.suite mismatch")
        require(oracle.get("run_id") == manifest["run_id"], "oracle.run_id mismatch")
        results = score_oracle_cases(oracle, response_index, judgment_index)
        pair_results = score_pair_rules(oracle, response_index)
        results.extend(pair_results)
    else:
        pair_results = []
        results = [case_result(cid, "UNSCORED", "UNSCORED", ["private oracle not supplied"], response=r)
                   for cid, r in sorted(response_index.items())]

    counts = {name: sum(1 for r in results if r["result"] == name) for name in ("PASS", "FAIL", "PARTIAL", "UNSCORED")}
    pair_failures = sum(1 for r in pair_results if r["result"] == "FAIL")
    scored_pair_count = sum(1 for r in pair_results if r["result"] in {"PASS", "FAIL"})
    private_scored_count = sum(1 for r in results if r["result"] in {"PASS", "FAIL"} and r["scoring_mode"] in {"LABEL_SET", "EXACT_VALUE", "PAIR_RELATION"})
    independent_judged_count = sum(1 for r in results if r["scoring_mode"] == "SEMANTIC_JUDGE" and r["result"] in {"PASS", "FAIL"} and r.get("judge_sha256"))

    level, blockers, next_required = promote_evidence(
        manifest,
        oracle_present=oracle is not None,
        oracle_hash=oracle_hash,
        private_scored_count=private_scored_count,
        independent_judged_count=independent_judged_count,
        scored_pair_count=scored_pair_count,
        commitment_reveal_verified=commitment_reveal_verified,
        execution_receipt_verified=execution_receipt_verified,
        fresh_context_claim_verified=fresh_context_claim_verified,
        runtime_independence_claim_verified=runtime_independence_claim_verified,
    )

    execution = manifest.get("execution", {})
    contamination = manifest.get("contamination", {})
    holdout = manifest.get("holdout", {})
    judging = manifest.get("judging", {})
    return {
        "schema_version": "1.0",
        "suite": manifest["suite"],
        "run_id": manifest["run_id"],
        "created_at": manifest.get("created_at"),
        "status": infer_status(results),
        "evidence_class": level,
        "contamination": {
            "authoring_overlap": contamination.get("authoring_overlap"),
            "fixture_visible_to_generator": contamination.get("fixture_visible_to_generator"),
            "expected_labels_visible_to_generator": contamination.get("expected_labels_visible_to_generator"),
            "notes": contamination.get("notes"),
        },
        "execution": {
            "target_executed": bool(execution.get("target_executed")),
            "fresh_context": execution.get("fresh_context"),
            "runtime_independent": execution.get("runtime_independent"),
            "responses_frozen_before_scoring": execution.get("responses_frozen_before_scoring"),
            "response_count": len(responses),
            "repeat_count": execution.get("repeat_count", 0) if isinstance(execution.get("repeat_count", 0), int) else 0,
            "target_id": execution.get("target_id"),
            "execution_receipts": execution.get("execution_receipts", []),
            "execution_receipt_verified": execution_receipt_verified,
            "fresh_context_claim_verified": fresh_context_claim_verified,
            "runtime_independence_claim_verified": runtime_independence_claim_verified,
            "execution_receipt_sha256": canonical_hash(execution_receipt) if execution_receipt is not None else None,
            "authentic_multi_agent_runtime": execution.get("authentic_multi_agent_runtime"),
            "host_live_verified": bool(execution.get("host_live_verified", False)),
            "host_receipts": execution.get("host_receipts", []),
        },
        "judging": {
            "mode": judging.get("mode", "NONE"),
            "independent": judging.get("independent"),
            "judgment_count": len(judgments),
            "judge_id": judging.get("judge_id"),
            "judge_receipts": judging.get("judge_receipts", []),
        },
        "holdout": {
            "private_oracle_separated": holdout.get("private_oracle_separated"),
            "hidden_variant": holdout.get("hidden_variant"),
            "variant_hidden_from_generator": holdout.get("variant_hidden_from_generator"),
            "oracle_hash_present": bool(oracle_hash),
            "commitment_reveal_verified": commitment_reveal_verified,
            "unseen_adversarial": holdout.get("unseen_adversarial"),
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


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--responses", type=Path, required=True)
    p.add_argument("--oracle", type=Path)
    p.add_argument("--execution-receipt", type=Path,
                   help="owning-runtime/external-job receipt binding manifest and response set")
    p.add_argument("--reveal-receipt", type=Path)
    p.add_argument("--judgments", type=Path)
    p.add_argument("--out", type=Path)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        manifest = load_json(args.manifest)
        require(isinstance(manifest, dict), "manifest must be object")
        responses = load_jsonl(args.responses)
        oracle = load_json(args.oracle) if args.oracle else None
        if oracle is not None:
            require(isinstance(oracle, dict), "oracle must be object")
        execution_receipt = load_json(args.execution_receipt) if args.execution_receipt else None
        if execution_receipt is not None:
            require(isinstance(execution_receipt, dict), "execution receipt must be object")
        reveal_receipt = load_json(args.reveal_receipt) if args.reveal_receipt else None
        if reveal_receipt is not None:
            require(isinstance(reveal_receipt, dict), "reveal receipt must be object")
        judgments = load_jsonl(args.judgments) if args.judgments else []
        oracle_hash = sha256_bytes(args.oracle.read_bytes()) if args.oracle else None
        result = make_result(manifest, responses, oracle, judgments, oracle_hash, reveal_receipt, execution_receipt)
    except EvalError as exc:
        result = {"status": "INVALID", "error": str(exc)}
        rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
        if args.out:
            args.out.write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
