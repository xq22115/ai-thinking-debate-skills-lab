#!/usr/bin/env python3
"""Prepare a public holdout manifest plus a private salted oracle commitment.

This tool does NOT execute a model. For a real hidden run, the input blueprint,
private oracle, and salt must remain outside the public target-generation path
until target responses have been frozen.

The public commitment intentionally excludes the salt. A plain hash of a
low-entropy oracle can be brute-forced; the unrevealed random salt makes the
pre-run commitment materially stronger while preserving later verification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
from pathlib import Path
from typing import Any

DOMAIN = b"reasoning-holdout-oracle-v1\x00"
FORBIDDEN_PUBLIC_KEYS = {
    "scoring",
    "must_detect",
    "fail_if",
    "expected",
    "expected_answer",
    "gold_label",
    "oracle",
    "pair_rules",
}


class HoldoutError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise HoldoutError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HoldoutError(f"failed to parse JSON {path}: {exc}") from exc
    require(isinstance(value, dict), f"{path}: top-level JSON must be object")
    return value


def validate_blueprint(bp: dict[str, Any]) -> None:
    require(bp.get("schema_version") == "1.0", "blueprint.schema_version must be 1.0")
    require(bp.get("visibility") in {"PRIVATE_BLUEPRINT", "PUBLIC_NON_HIDDEN_EXAMPLE"},
            "blueprint.visibility invalid")
    for key in ["suite", "run_id"]:
        require(isinstance(bp.get(key), str) and bp[key], f"blueprint.{key} required")
    for key in ["contamination", "execution", "holdout", "judging"]:
        require(isinstance(bp.get(key), dict), f"blueprint.{key} must be object")
    cases = bp.get("cases")
    require(isinstance(cases, list) and cases, "blueprint.cases must be non-empty array")
    seen: set[str] = set()
    for case in cases:
        require(isinstance(case, dict), "blueprint case must be object")
        case_id = case.get("case_id")
        require(isinstance(case_id, str) and case_id, "case_id required")
        require(case_id not in seen, f"duplicate case_id={case_id}")
        seen.add(case_id)
        require(isinstance(case.get("prompt"), str), f"{case_id}.prompt must be string")
        scoring = case.get("scoring")
        require(isinstance(scoring, dict), f"{case_id}.scoring required")
        require(scoring.get("mode") in {"LABEL_SET", "EXACT_VALUE", "SEMANTIC_JUDGE"},
                f"{case_id}.scoring.mode unsupported")
    pair_rules = bp.get("pair_rules", [])
    require(isinstance(pair_rules, list), "blueprint.pair_rules must be array")
    for rule in pair_rules:
        require(isinstance(rule, dict), "pair rule must be object")
        for key in ["pair_id", "left_case_id", "right_case_id", "field"]:
            require(isinstance(rule.get(key), str) and rule[key], f"pair rule {key} required")
        require(rule.get("left_case_id") in seen and rule.get("right_case_id") in seen,
                f"pair rule {rule.get('pair_id')} references unknown case")
        require(rule.get("relation") in {"EQUAL", "NOT_EQUAL"},
                f"pair rule {rule.get('pair_id')} relation unsupported")


def make_public_manifest(bp: dict[str, Any]) -> dict[str, Any]:
    cases = []
    for item in bp["cases"]:
        public_case = {
            "case_id": item["case_id"],
            "prompt": item["prompt"],
            "pair_group": item.get("pair_group"),
            "presentation": item.get("presentation"),
        }
        cases.append(public_case)
    return {
        "schema_version": "1.0",
        "suite": bp["suite"],
        "run_id": bp["run_id"],
        "created_at": bp.get("created_at"),
        "contamination": bp["contamination"],
        "execution": bp["execution"],
        "holdout": bp["holdout"],
        "judging": bp["judging"],
        "cases": cases,
    }


def make_private_oracle(bp: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "suite": bp["suite"],
        "run_id": bp["run_id"],
        "cases": [
            {"case_id": item["case_id"], "scoring": item["scoring"]}
            for item in bp["cases"]
            if item["scoring"].get("mode") != "PAIR_ONLY"
        ],
        "pair_rules": bp.get("pair_rules", []),
    }


def collect_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_PUBLIC_KEYS:
                hits.append(child_path)
            hits.extend(collect_forbidden_keys(child, child_path))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            hits.extend(collect_forbidden_keys(child, f"{path}[{i}]"))
    return hits


def parse_salt_hex(value: str | None) -> bytes:
    if value is None:
        return secrets.token_bytes(32)
    try:
        salt = bytes.fromhex(value)
    except ValueError as exc:
        raise HoldoutError("--salt-hex must be valid hex") from exc
    require(len(salt) >= 16, "salt must be at least 16 bytes")
    return salt


def oracle_commitment(oracle: dict[str, Any], salt: bytes) -> str:
    return hashlib.sha256(DOMAIN + salt + b"\x00" + canonical_bytes(oracle)).hexdigest()


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--blueprint", type=Path, required=True)
    p.add_argument("--manifest-out", type=Path, required=True)
    p.add_argument("--oracle-out", type=Path, required=True)
    p.add_argument("--salt-out", type=Path, required=True,
                   help="PRIVATE file. Do not commit for a real hidden run before response freeze.")
    p.add_argument("--commitment-out", type=Path, required=True)
    p.add_argument("--salt-hex",
                   help="Deterministic test-only salt. Omit for cryptographically random production salt.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        bp = load_object(args.blueprint)
        validate_blueprint(bp)
        public_manifest = make_public_manifest(bp)
        private_oracle = make_private_oracle(bp)
        leaks = collect_forbidden_keys(public_manifest)
        require(not leaks, "public manifest contains private scoring keys: " + ", ".join(leaks))
        salt = parse_salt_hex(args.salt_hex)
        commitment_value = oracle_commitment(private_oracle, salt)
        commitment = {
            "schema_version": "1.0",
            "suite": bp["suite"],
            "run_id": bp["run_id"],
            "commitment_algorithm": "SHA256-SALTED-CANONICAL-JSON-v1",
            "domain": "reasoning-holdout-oracle-v1",
            "manifest_sha256": canonical_hash(public_manifest),
            "oracle_commitment_sha256": commitment_value,
            "salt_revealed": False,
            "oracle_revealed": False,
            "blueprint_visibility": bp["visibility"],
            "public_manifest_private_key_scan_passed": True,
        }
    except HoldoutError as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    args.manifest_out.write_text(json.dumps(public_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.oracle_out.write_text(json.dumps(private_oracle, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.salt_out.write_text(salt.hex() + "\n", encoding="utf-8")
    args.commitment_out.write_text(json.dumps(commitment, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PREPARED",
        "suite": bp["suite"],
        "run_id": bp["run_id"],
        "manifest_sha256": commitment["manifest_sha256"],
        "oracle_commitment_sha256": commitment_value,
        "salt_revealed": False,
        "oracle_revealed": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
