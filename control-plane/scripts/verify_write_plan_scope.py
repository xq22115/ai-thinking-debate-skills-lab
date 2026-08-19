#!/usr/bin/env python3
"""Verify that actual changed repository paths stay inside an approved write plan."""
from __future__ import annotations

import fnmatch
import json
import pathlib


def _valid_path(value: str) -> bool:
    if not value or value.startswith("/") or "\\" in value:
        return False
    parts = pathlib.PurePosixPath(value).parts
    return ".." not in parts and not (parts and parts[0] == ".git")


def _matches(path: str, pattern: str) -> bool:
    if path == pattern:
        return True
    return fnmatch.fnmatchcase(path, pattern)


def verify_scope(plan: dict, changed_paths: list[str]) -> dict:
    declared = [str(item) for item in (plan.get("write_set") or [])]
    invalid = sorted(
        {str(path) for path in changed_paths if not _valid_path(str(path))}
    )
    undeclared = sorted(
        {
            str(path)
            for path in changed_paths
            if _valid_path(str(path))
            and not any(_matches(str(path), pattern) for pattern in declared)
        }
    )
    veto = bool(invalid or undeclared)
    return {
        "schemaVersion": 1,
        "actor_id": plan.get("actor_id"),
        "declared_write_set": declared,
        "changed_paths": [str(path) for path in changed_paths],
        "invalid_changed_paths": invalid,
        "undeclared_paths": undeclared,
        "result": "VETO" if veto else "PASS",
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("plan_json")
    parser.add_argument("changed_paths_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    plan = json.loads(pathlib.Path(args.plan_json).read_text(encoding="utf-8"))
    changed_paths = json.loads(
        pathlib.Path(args.changed_paths_json).read_text(encoding="utf-8")
    )
    result = verify_scope(plan, changed_paths)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
