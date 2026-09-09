#!/usr/bin/env python3
"""Verify that an owning-runtime target-execution receipt is bound to this run.

This verifier checks deterministic artifact binding and minimum provenance fields.
It does NOT prove that a runtime's freshness/independence assertions are truthful;
those semantic claims remain only as strong as the owning-runtime or external-job
receipt locator that made them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


class ReceiptError(ValueError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ReceiptError(f"failed to parse JSON {path}: {exc}") from exc


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise ReceiptError(f"{path}:{line_no}: record must be object")
            rows.append(value)
    except ReceiptError:
        raise
    except Exception as exc:
        raise ReceiptError(f"failed to parse JSONL {path}: {exc}") from exc
    return rows


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReceiptError(message)


def verify_receipt(manifest: dict[str, Any], responses: list[dict[str, Any]], receipt: dict[str, Any]) -> dict[str, Any]:
    require(receipt.get("schema_version") == "1.0", "execution receipt schema_version must be 1.0")
    require(receipt.get("status") == "PASS_TARGET_EXECUTION", "execution receipt status must be PASS_TARGET_EXECUTION")
    require(receipt.get("suite") == manifest.get("suite"), "execution receipt suite mismatch")
    require(receipt.get("run_id") == manifest.get("run_id"), "execution receipt run_id mismatch")

    target_id = manifest.get("execution", {}).get("target_id")
    require(isinstance(target_id, str) and target_id, "manifest.execution.target_id required for attested execution")
    require(receipt.get("target_id") == target_id, "execution receipt target_id mismatch")
    require(isinstance(receipt.get("execution_id"), str) and receipt["execution_id"], "execution receipt execution_id required")
    require(isinstance(receipt.get("created_at"), str) and receipt["created_at"], "execution receipt created_at required")

    provenance = receipt.get("provenance")
    require(isinstance(provenance, dict), "execution receipt provenance required")
    require(provenance.get("source_class") in {"OWNING_RUNTIME", "EXTERNAL_JOB"},
            "execution receipt source_class must be OWNING_RUNTIME or EXTERNAL_JOB")
    require(isinstance(provenance.get("source_name"), str) and provenance["source_name"],
            "execution receipt source_name required")
    require(isinstance(provenance.get("receipt_locator"), str) and provenance["receipt_locator"],
            "execution receipt receipt_locator required")
    require(provenance.get("target_executed_verified") is True,
            "execution receipt must verify target execution")

    binding = receipt.get("binding")
    require(isinstance(binding, dict), "execution receipt binding required")
    require(binding.get("manifest_canonical_sha256") == canonical_hash(manifest),
            "execution receipt manifest hash mismatch")
    normalized = sorted(responses, key=lambda row: row.get("case_id", ""))
    require(binding.get("responses_canonical_sha256") == canonical_hash(normalized),
            "execution receipt response-set hash mismatch")
    require(binding.get("response_count") == len(responses), "execution receipt response_count mismatch")

    for row in responses:
        require(row.get("run_id") == manifest.get("run_id"), "response run_id mismatch under execution receipt")

    boundary = receipt.get("boundary")
    require(isinstance(boundary, dict), "execution receipt boundary required")
    require(boundary.get("oracle_quality_verified") is False,
            "execution receipt must not claim oracle quality verification")
    require(boundary.get("judge_independence_verified") is False,
            "execution receipt must not claim judge independence verification")

    fresh_claim_verified = (
        provenance.get("fresh_context_verified") is True
        and provenance.get("expected_labels_hidden_verified") is True
        and manifest.get("contamination", {}).get("expected_labels_visible_to_generator") is False
        and manifest.get("execution", {}).get("fresh_context") is True
    )
    runtime_independence_verified = (
        provenance.get("runtime_independent_verified") is True
        and manifest.get("execution", {}).get("runtime_independent") is True
    )

    return {
        "schema_version": "1.0",
        "status": "PASS_EXECUTION_RECEIPT_BINDING",
        "verified": True,
        "suite": manifest.get("suite"),
        "run_id": manifest.get("run_id"),
        "target_id": target_id,
        "execution_id": receipt.get("execution_id"),
        "source_class": provenance.get("source_class"),
        "source_name": provenance.get("source_name"),
        "receipt_locator": provenance.get("receipt_locator"),
        "binding": {
            "manifest_canonical_sha256": canonical_hash(manifest),
            "responses_canonical_sha256": canonical_hash(normalized),
            "response_count": len(responses),
        },
        "fresh_context_claim_verified": fresh_claim_verified,
        "runtime_independence_claim_verified": runtime_independence_verified,
        "boundary": {
            "semantic_truth_of_runtime_claims_verified": False,
            "oracle_quality_verified": False,
            "judge_independence_verified": False,
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--responses", type=Path, required=True)
    p.add_argument("--receipt", type=Path, required=True)
    p.add_argument("--out", type=Path)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        manifest = load_json(args.manifest)
        receipt = load_json(args.receipt)
        responses = load_jsonl(args.responses)
        require(isinstance(manifest, dict), "manifest must be object")
        require(isinstance(receipt, dict), "execution receipt must be object")
        result = verify_receipt(manifest, responses, receipt)
    except ReceiptError as exc:
        result = {"status": "INVALID", "verified": False, "error": str(exc)}
        rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
        if args.out:
            args.out.write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
