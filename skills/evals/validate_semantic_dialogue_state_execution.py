#!/usr/bin/env python3
"""Validate target-model execution isolation receipts for semantic DS evals.

This validator checks provenance/isolation only. It does not score answer quality,
judge outputs, or prove host-live implicit routing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

EXPECTED_ARM_EXPOSURE = {
    "direct": "none",
    "generic-careful": "generic-careful",
    "microscope-core": "microscope-core",
    "microscope-dialogue-state": "microscope-dialogue-state",
}

FORBIDDEN_EXPOSURE_FIELDS = (
    "fixture_answer_key_exposed_before_response",
    "rubric_exposed_before_response",
    "cross_arm_output_exposed_before_response",
    "judge_information_exposed_before_response",
)

VALID_STATUSES = {"OUTPUT_RECORDED", "INVALID_FOR_COMPARISON", "BLOCKED"}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def dump_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def dump_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def index_unique(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label}: missing non-empty {key}")
        value = value.strip()
        if value in result:
            raise ValueError(f"{label}: duplicate {key}={value}")
        result[value] = row
    return result


def require_text(row: dict[str, Any], key: str, label: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: missing non-empty {key}")
    return value.strip()


def require_bool(row: dict[str, Any], key: str, label: str) -> bool:
    value = row.get(key)
    if not isinstance(value, bool):
        raise ValueError(f"{label}: {key} must be boolean")
    return value


def prepare_template(run_dir: Path, output: Path | None = None) -> Path:
    """Generate a non-validating receipt template from frozen manifest/requests.

    Template placeholders intentionally remain null/FILL_ME so the file cannot be
    mistaken for proof of execution. Copy/fill it into execution_receipts.jsonl
    only after each request is actually executed.
    """

    manifest = load_json(run_dir / "manifest.json")
    if not isinstance(manifest, dict):
        raise ValueError("manifest.json root must be an object")
    run_id = require_text(manifest, "run_id", "manifest")
    model_id = require_text(manifest, "model_id", "manifest")
    provider = require_text(manifest, "provider", "manifest")
    requests = load_jsonl(run_dir / "requests.jsonl")
    index_unique(requests, "request_id", "requests")

    rows: list[dict[str, Any]] = []
    for request in requests:
        request_id = require_text(request, "request_id", "request")
        case_id = require_text(request, "case_id", f"request {request_id}")
        arm = require_text(request, "arm", f"request {request_id}")
        bundle_sha256 = require_text(request, "bundle_sha256", f"request {request_id}")
        expected_exposure = EXPECTED_ARM_EXPOSURE.get(arm)
        if expected_exposure is None:
            raise ValueError(f"request {request_id}: unknown arm {arm}")
        rows.append(
            {
                "request_id": request_id,
                "run_id": run_id,
                "case_id": case_id,
                "arm": arm,
                "bundle_sha256": bundle_sha256,
                "model_id": model_id,
                "provider": provider,
                "surface": "FILL_ME",
                "session_id_hash": "FILL_ME_UNIQUE_HASH",
                "fresh_context": None,
                "fixture_answer_key_exposed_before_response": None,
                "rubric_exposed_before_response": None,
                "cross_arm_output_exposed_before_response": None,
                "judge_information_exposed_before_response": None,
                "arm_bundle_exposure": expected_exposure,
                "output_sha256": "FILL_AFTER_RESPONSE",
                "started_at": "FILL_ME",
                "finished_at": "FILL_ME",
                "tool_access": "unknown",
                "sampling_settings": "unknown",
                "status": "FILL_ME",
                "notes": "",
            }
        )

    output = output or (run_dir / "execution_receipts.template.jsonl")
    dump_jsonl(output, rows)
    print(f"prepared {len(rows)} execution receipt templates at {output}")
    return output


def validate(run_dir: Path, allow_partial: bool = False) -> dict[str, Any]:
    manifest = load_json(run_dir / "manifest.json")
    if not isinstance(manifest, dict):
        raise ValueError("manifest.json root must be an object")

    run_id = require_text(manifest, "run_id", "manifest")
    model_id = require_text(manifest, "model_id", "manifest")
    provider = require_text(manifest, "provider", "manifest")

    requests = index_unique(load_jsonl(run_dir / "requests.jsonl"), "request_id", "requests")
    receipts = index_unique(
        load_jsonl(run_dir / "execution_receipts.jsonl"), "request_id", "execution receipts"
    )
    responses = index_unique(load_jsonl(run_dir / "responses.jsonl"), "request_id", "responses")

    unknown_receipts = sorted(set(receipts) - set(requests))
    unknown_responses = sorted(set(responses) - set(requests))
    if unknown_receipts:
        raise ValueError(f"execution receipts contain unknown request ids: {unknown_receipts[:5]}")
    if unknown_responses:
        raise ValueError(f"responses contain unknown request ids: {unknown_responses[:5]}")

    missing_receipts = sorted(set(requests) - set(receipts))
    if missing_receipts and not allow_partial:
        raise ValueError(f"missing execution receipts for {len(missing_receipts)} requests")

    invalid_reasons: dict[str, list[str]] = defaultdict(list)
    status_counts: Counter[str] = Counter()
    session_to_requests: dict[str, list[str]] = defaultdict(list)

    for request_id, receipt in receipts.items():
        request = requests[request_id]
        label = f"receipt {request_id}"

        receipt_run_id = require_text(receipt, "run_id", label)
        receipt_case_id = require_text(receipt, "case_id", label)
        receipt_arm = require_text(receipt, "arm", label)
        receipt_bundle = require_text(receipt, "bundle_sha256", label)
        receipt_model = require_text(receipt, "model_id", label)
        receipt_provider = require_text(receipt, "provider", label)
        require_text(receipt, "surface", label)
        session_hash = require_text(receipt, "session_id_hash", label)
        arm_exposure = require_text(receipt, "arm_bundle_exposure", label)
        output_hash = require_text(receipt, "output_sha256", label)
        require_text(receipt, "started_at", label)
        require_text(receipt, "finished_at", label)
        require_text(receipt, "tool_access", label)
        require_text(receipt, "sampling_settings", label)
        status = require_text(receipt, "status", label)
        fresh_context = require_bool(receipt, "fresh_context", label)

        if status not in VALID_STATUSES:
            raise ValueError(f"{label}: invalid status {status}")
        status_counts[status] += 1
        session_to_requests[session_hash].append(request_id)

        if receipt_run_id != run_id:
            invalid_reasons[request_id].append("run_id_mismatch")
        if receipt_case_id != request.get("case_id"):
            invalid_reasons[request_id].append("case_id_mismatch")
        if receipt_arm != request.get("arm"):
            invalid_reasons[request_id].append("arm_mismatch")
        if receipt_bundle != request.get("bundle_sha256"):
            invalid_reasons[request_id].append("bundle_sha256_mismatch")
        if receipt_model != model_id:
            invalid_reasons[request_id].append("model_id_mismatch")
        if receipt_provider != provider:
            invalid_reasons[request_id].append("provider_mismatch")
        if not fresh_context:
            invalid_reasons[request_id].append("fresh_context_false")

        for field in FORBIDDEN_EXPOSURE_FIELDS:
            if require_bool(receipt, field, label):
                invalid_reasons[request_id].append(field)

        expected_exposure = EXPECTED_ARM_EXPOSURE.get(str(request.get("arm")))
        if expected_exposure is None:
            invalid_reasons[request_id].append("unknown_request_arm")
        elif arm_exposure != expected_exposure:
            invalid_reasons[request_id].append(
                f"arm_bundle_exposure_mismatch:{arm_exposure}!={expected_exposure}"
            )

        response = responses.get(request_id)
        if status == "OUTPUT_RECORDED":
            if response is None:
                invalid_reasons[request_id].append("missing_recorded_response")
            else:
                output_text = response.get("output")
                if not isinstance(output_text, str) or not output_text.strip():
                    invalid_reasons[request_id].append("empty_response_output")
                elif sha256_text(output_text) != output_hash:
                    invalid_reasons[request_id].append("output_sha256_mismatch")
                for field in ("case_id", "arm"):
                    if response.get(field) not in (None, request.get(field)):
                        invalid_reasons[request_id].append(f"response_{field}_mismatch")
        elif response is not None:
            output_text = response.get("output")
            if isinstance(output_text, str) and output_text.strip() and sha256_text(output_text) != output_hash:
                invalid_reasons[request_id].append("nonclean_output_sha256_mismatch")

        if status == "INVALID_FOR_COMPARISON":
            invalid_reasons[request_id].append("receipt_marked_invalid_for_comparison")
        elif status == "BLOCKED":
            invalid_reasons[request_id].append("receipt_marked_blocked")

    reused_sessions = {
        session: ids for session, ids in session_to_requests.items() if len(ids) > 1
    }
    for ids in reused_sessions.values():
        for request_id in ids:
            invalid_reasons[request_id].append("session_context_reused")

    clean_ids = sorted(
        request_id
        for request_id in receipts
        if not invalid_reasons.get(request_id)
        and receipts[request_id].get("status") == "OUTPUT_RECORDED"
    )
    invalid_ids = sorted(set(receipts) - set(clean_ids))
    missing_responses_for_recorded = sorted(
        request_id
        for request_id, receipt in receipts.items()
        if receipt.get("status") == "OUTPUT_RECORDED" and request_id not in responses
    )

    complete = (
        not missing_receipts
        and not missing_responses_for_recorded
        and len(receipts) == len(requests)
    )
    clean_complete = complete and len(clean_ids) == len(requests)
    decision = "CLEAN_COMPLETE" if clean_complete else "PARTIAL_OR_INVALID"

    summary = {
        "schema_version": 1,
        "run_id": run_id,
        "model_id": model_id,
        "provider": provider,
        "requests": len(requests),
        "receipts": len(receipts),
        "responses": len(responses),
        "clean_requests": len(clean_ids),
        "invalid_or_blocked_requests": len(invalid_ids),
        "missing_receipts": len(missing_receipts),
        "missing_responses_for_recorded": len(missing_responses_for_recorded),
        "reused_session_contexts": len(reused_sessions),
        "status_counts": dict(sorted(status_counts.items())),
        "decision": decision,
        "invalid_reasons": {key: sorted(set(value)) for key, value in sorted(invalid_reasons.items())},
        "status_boundary": "CLEAN_COMPLETE == EXECUTION_PROVENANCE_VALIDATED; NOT ANSWER QUALITY OR HOST_LIVE",
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return summary


def synthetic_files(run_dir: Path, contaminated: bool = False) -> None:
    manifest = {
        "run_id": "synthetic-run",
        "model_id": "synthetic-model",
        "provider": "synthetic-provider",
    }
    requests = [
        {
            "request_id": "req-direct",
            "case_id": "DS1",
            "arm": "direct",
            "bundle_sha256": sha256_text(""),
        },
        {
            "request_id": "req-ds",
            "case_id": "DS1",
            "arm": "microscope-dialogue-state",
            "bundle_sha256": sha256_text("synthetic-ds-bundle"),
        },
    ]
    responses = [
        {"request_id": "req-direct", "case_id": "DS1", "arm": "direct", "output": "direct output"},
        {"request_id": "req-ds", "case_id": "DS1", "arm": "microscope-dialogue-state", "output": "ds output"},
    ]
    receipts: list[dict[str, Any]] = []
    for index, (request, response) in enumerate(zip(requests, responses), 1):
        receipts.append(
            {
                "request_id": request["request_id"],
                "run_id": "synthetic-run",
                "case_id": request["case_id"],
                "arm": request["arm"],
                "bundle_sha256": request["bundle_sha256"],
                "model_id": "synthetic-model",
                "provider": "synthetic-provider",
                "surface": "synthetic",
                "session_id_hash": f"session-{index}",
                "fresh_context": True,
                "fixture_answer_key_exposed_before_response": False,
                "rubric_exposed_before_response": False,
                "cross_arm_output_exposed_before_response": contaminated and index == 2,
                "judge_information_exposed_before_response": False,
                "arm_bundle_exposure": EXPECTED_ARM_EXPOSURE[request["arm"]],
                "output_sha256": sha256_text(response["output"]),
                "started_at": "2026-09-09T00:00:00Z",
                "finished_at": "2026-09-09T00:00:01Z",
                "tool_access": "unknown",
                "sampling_settings": "unknown",
                "status": "OUTPUT_RECORDED",
            }
        )

    dump_json(run_dir / "manifest.json", manifest)
    dump_jsonl(run_dir / "requests.jsonl", requests)
    dump_jsonl(run_dir / "responses.jsonl", responses)
    dump_jsonl(run_dir / "execution_receipts.jsonl", receipts)


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="semantic-execution-template-") as tmp:
        template_dir = Path(tmp)
        dump_json(
            template_dir / "manifest.json",
            {"run_id": "template-run", "model_id": "template-model", "provider": "template-provider"},
        )
        dump_jsonl(
            template_dir / "requests.jsonl",
            [
                {
                    "request_id": "template-direct",
                    "case_id": "DS1",
                    "arm": "direct",
                    "bundle_sha256": sha256_text(""),
                },
                {
                    "request_id": "template-core",
                    "case_id": "DS2",
                    "arm": "microscope-core",
                    "bundle_sha256": sha256_text("core"),
                },
            ],
        )
        template_path = prepare_template(template_dir)
        template_rows = load_jsonl(template_path)
        assert len(template_rows) == 2
        assert template_rows[0]["arm_bundle_exposure"] == "none"
        assert template_rows[1]["arm_bundle_exposure"] == "microscope-core"
        assert template_rows[0]["fresh_context"] is None
        assert template_rows[0]["status"] == "FILL_ME"

    with tempfile.TemporaryDirectory(prefix="semantic-execution-clean-") as tmp:
        clean_dir = Path(tmp)
        synthetic_files(clean_dir, contaminated=False)
        clean = validate(clean_dir)
        assert clean["decision"] == "CLEAN_COMPLETE"
        assert clean["clean_requests"] == 2

    with tempfile.TemporaryDirectory(prefix="semantic-execution-contaminated-") as tmp:
        dirty_dir = Path(tmp)
        synthetic_files(dirty_dir, contaminated=True)
        dirty = validate(dirty_dir)
        assert dirty["decision"] == "PARTIAL_OR_INVALID"
        assert dirty["clean_requests"] == 1
        assert "cross_arm_output_exposed_before_response" in dirty["invalid_reasons"]["req-ds"]

    print("semantic dialogue-state execution isolation self-test: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    template = sub.add_parser("prepare-template")
    template.add_argument("run_dir", type=Path)
    template.add_argument("--output", type=Path)

    check = sub.add_parser("validate")
    check.add_argument("run_dir", type=Path)
    check.add_argument("--allow-partial", action="store_true")
    check.add_argument("--require-clean", action="store_true")

    sub.add_parser("self-test")

    args = parser.parse_args()
    if args.command == "self-test":
        self_test()
        return
    if args.command == "prepare-template":
        prepare_template(args.run_dir, args.output)
        return

    result = validate(args.run_dir, allow_partial=args.allow_partial)
    if args.require_clean and result["decision"] != "CLEAN_COMPLETE":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
