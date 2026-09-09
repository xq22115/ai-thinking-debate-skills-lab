#!/usr/bin/env python3
"""Verify a salted private-oracle reveal against a pre-run commitment.

This tool requires a response-freeze receipt. A successful verification proves
that the revealed oracle matches the earlier commitment and that the exact
public manifest/response set was frozen before scoring. It does not prove oracle
quality, judge independence, model freshness, or reasoning correctness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

DOMAIN = b"reasoning-holdout-oracle-v1\x00"


class RevealError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RevealError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RevealError(f"failed to parse JSON {path}: {exc}") from exc
    require(isinstance(value, dict), f"{path}: top-level must be object")
    return value


def load_salt(path: Path) -> bytes:
    try:
        salt = bytes.fromhex(path.read_text(encoding="utf-8").strip())
    except ValueError as exc:
        raise RevealError("salt file must contain hex") from exc
    require(len(salt) >= 16, "salt must be at least 16 bytes")
    return salt


def oracle_commitment(oracle: dict[str, Any], salt: bytes) -> str:
    return hashlib.sha256(DOMAIN + salt + b"\x00" + canonical_bytes(oracle)).hexdigest()


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--commitment", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--freeze-receipt", type=Path, required=True)
    p.add_argument("--oracle", type=Path, required=True)
    p.add_argument("--salt", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        commitment = load_object(args.commitment)
        manifest = load_object(args.manifest)
        freeze = load_object(args.freeze_receipt)
        oracle = load_object(args.oracle)
        salt = load_salt(args.salt)

        require(commitment.get("schema_version") == "1.0", "commitment.schema_version must be 1.0")
        require(commitment.get("commitment_algorithm") == "SHA256-SALTED-CANONICAL-JSON-v1",
                "unsupported commitment algorithm")
        require(commitment.get("domain") == "reasoning-holdout-oracle-v1", "commitment domain mismatch")
        require(freeze.get("status") == "FROZEN", "response freeze receipt missing FROZEN status")

        suite = commitment.get("suite")
        run_id = commitment.get("run_id")
        for label, obj in [("manifest", manifest), ("freeze", freeze), ("oracle", oracle)]:
            require(obj.get("suite") == suite, f"{label}.suite mismatch")
            require(obj.get("run_id") == run_id, f"{label}.run_id mismatch")

        manifest_hash = canonical_hash(manifest)
        require(manifest_hash == commitment.get("manifest_sha256"), "manifest commitment mismatch")
        require(manifest_hash == freeze.get("manifest_sha256"), "freeze receipt bound to different manifest")

        expected = commitment.get("oracle_commitment_sha256")
        observed = oracle_commitment(oracle, salt)
        require(isinstance(expected, str) and len(expected) == 64, "oracle commitment missing")
        require(observed == expected, "oracle/salt reveal does not match pre-run commitment")

        responses_hash = freeze.get("responses_canonical_sha256")
        require(isinstance(responses_hash, str) and len(responses_hash) == 64,
                "freeze receipt responses hash missing")
        response_count = freeze.get("response_count")
        require(isinstance(response_count, int) and response_count > 0,
                "freeze receipt must bind at least one response")

        receipt = {
            "schema_version": "1.0",
            "status": "PASS_COMMITMENT_REVEAL",
            "verified": True,
            "suite": suite,
            "run_id": run_id,
            "commitment_algorithm": commitment["commitment_algorithm"],
            "manifest_sha256": manifest_hash,
            "oracle_canonical_sha256": canonical_hash(oracle),
            "oracle_commitment_sha256": observed,
            "salt_sha256": hashlib.sha256(salt).hexdigest(),
            "responses_canonical_sha256": responses_hash,
            "response_count": response_count,
            "freeze_receipt_sha256": canonical_hash(freeze),
            "commitment_receipt_sha256": canonical_hash(commitment),
            "boundary": {
                "commitment_matches_reveal": True,
                "manifest_matches_commitment": True,
                "responses_frozen_before_reveal_contract": True,
                "oracle_quality_verified": False,
                "model_freshness_verified": False,
                "judge_independence_verified": False
            }
        }
    except RevealError as exc:
        invalid = {"schema_version": "1.0", "status": "INVALID", "verified": False, "error": str(exc)}
        args.out.write_text(json.dumps(invalid, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(invalid, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    args.out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
