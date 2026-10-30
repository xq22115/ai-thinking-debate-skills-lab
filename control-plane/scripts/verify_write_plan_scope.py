#!/usr/bin/env python3
"""Verify that actual changed repository paths stay inside an approved write plan."""
from __future__ import annotations

import fnmatch
import json
import pathlib


def _valid_path(value: str) -> bool:
    # Do not silently normalize away "." or repeated separators in a scope.
    if not value or value.startswith("/") or "\\" in value:
        return False
    parts = value.split("/")
    return parts[0] != ".git" and all(part not in {"", ".", ".."} for part in parts)


def _matches(path: str, pattern: str) -> bool:
    """Segment-aware glob: * matches one component, ** matches zero or more."""
    if not _valid_path(path) or not _valid_path(pattern):
        return False
    path_parts = path.split("/")
    positions = {0}
    for token in pattern.split("/"):
        if token == "**":
            positions = set(range(min(positions), len(path_parts) + 1)) if positions else set()
        else:
            positions = {
                position + 1
                for position in positions
                if position < len(path_parts)
                and fnmatch.fnmatchcase(path_parts[position], token)
            }
        if not positions:
            return False
    return len(path_parts) in positions


def verify_scope(plan: dict, changed_paths: list[str]) -> dict:
    declared = [str(item) for item in (plan.get("write_set") or [])]
    invalid_patterns = sorted({pattern for pattern in declared if not _valid_path(pattern)})
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
    veto = bool(invalid_patterns or invalid or undeclared)
    return {
        "schemaVersion": 1,
        "actor_id": plan.get("actor_id"),
        "declared_write_set": declared,
        "changed_paths": [str(path) for path in changed_paths],
        "invalid_changed_paths": invalid,
        "invalid_declared_patterns": invalid_patterns,
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
