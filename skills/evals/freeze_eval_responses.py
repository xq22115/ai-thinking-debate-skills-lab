#!/usr/bin/env python3
"""Freeze target responses before private holdout reveal/scoring.

Produces a content-addressed receipt binding the public manifest to the exact
response set. It never reads an oracle and therefore can run before reveal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class FreezeError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FreezeError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise FreezeError(f"failed to parse JSON {path}: {exc}") from exc
    require(isinstance(value, dict), f"{path}: top-level must be object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw.strip():
                continue
            value = json.loads(raw)
            require(isinstance(value, dict), f"{path}:{line_no}: record must be object")
            rows.append(value)
    except FreezeError:
        raise
    except Exception as exc:
        raise FreezeError(f"failed to parse JSONL {path}: {exc}") from exc
    return rows


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--responses", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        manifest = load_json(args.manifest)
        rows = load_jsonl(args.responses)
        suite = manifest.get("suite")
        run_id = manifest.get("run_id")
        require(isinstance(suite, str) and suite, "manifest.suite required")
        require(isinstance(run_id, str) and run_id, "manifest.run_id required")
        require(rows, "at least one response required to freeze")

        manifest_cases = manifest.get("cases", [])
        require(isinstance(manifest_cases, list), "manifest.cases must be array")
        allowed = {
            item.get("case_id")
            for item in manifest_cases
            if isinstance(item, dict) and isinstance(item.get("case_id"), str)
        }
        seen: set[str] = set()
        normalized: list[dict[str, Any]] = []
        for row in rows:
            case_id = row.get("case_id")
            require(isinstance(case_id, str) and case_id, "response.case_id required")
            require(case_id not in seen, f"duplicate response case_id={case_id}")
            seen.add(case_id)
            require(row.get("run_id") == run_id, f"response {case_id} run_id mismatch")
            require(case_id in allowed, f"response {case_id} not present in manifest")
            require(isinstance(row.get("output"), dict), f"response {case_id}.output must be object")
            normalized.append(row)

        normalized.sort(key=lambda item: item["case_id"])
        receipt = {
            "schema_version": "1.0",
            "status": "FROZEN",
            "suite": suite,
            "run_id": run_id,
            "frozen_at": datetime.now(timezone.utc).isoformat(),
            "manifest_sha256": canonical_hash(manifest),
            "responses_canonical_sha256": canonical_hash(normalized),
            "response_count": len(normalized),
            "case_ids": [item["case_id"] for item in normalized],
            "oracle_seen_by_freezer": False,
        }
    except FreezeError as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    args.out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
