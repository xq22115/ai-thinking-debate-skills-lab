#!/usr/bin/env python3
"""Fail-closed preflight for multi-chat / multi-agent write plans.

Plans declare repository-relative write sets before mutation. Disjoint plans may
run in parallel. Overlapping plans require an explicit dependency edge; otherwise
the preflight returns VETO. The checker is dependency-free so it can run locally
or in GitHub Actions.
"""
from __future__ import annotations

import fnmatch
import json
import pathlib
from typing import Iterable

GLOB_CHARS = set("*?[")


def _invalid_pattern(value: str) -> bool:
    if not value or value.startswith("/") or "\\" in value:
        return True
    parts = pathlib.PurePosixPath(value).parts
    return ".." in parts or (parts and parts[0] == ".git")


def _has_glob(value: str) -> bool:
    return any(ch in value for ch in GLOB_CHARS)


def _static_prefix(value: str) -> str:
    cut = len(value)
    for ch in GLOB_CHARS:
        pos = value.find(ch)
        if pos >= 0:
            cut = min(cut, pos)
    return value[:cut].rstrip("/")


def patterns_overlap(left: str, right: str) -> bool:
    if left == right:
        return True
    left_glob = _has_glob(left)
    right_glob = _has_glob(right)
    if not left_glob and not right_glob:
        return False
    if left_glob and not right_glob:
        return fnmatch.fnmatchcase(right, left)
    if right_glob and not left_glob:
        return fnmatch.fnmatchcase(left, right)
    left_prefix = _static_prefix(left)
    right_prefix = _static_prefix(right)
    if not left_prefix or not right_prefix:
        return True
    return (
        left_prefix == right_prefix
        or left_prefix.startswith(right_prefix + "/")
        or right_prefix.startswith(left_prefix + "/")
    )


def _dependency_cycle(plans_by_actor: dict[str, dict]) -> bool:
    graph = {
        actor: [dep for dep in plan.get("depends_on", []) if dep in plans_by_actor]
        for actor, plan in plans_by_actor.items()
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dependency in graph[node]:
            if visit(dependency):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph if node not in visited)


def evaluate_plans(plans: Iterable[dict]) -> dict:
    plans = list(plans)
    failures: list[str] = []
    unresolved: list[dict] = []
    serialized: list[dict] = []

    actors = [str(plan.get("actor_id", "")) for plan in plans]
    branches = [str(plan.get("branch", "")) for plan in plans]
    if len(set(actors)) != len(actors):
        failures.append("duplicate_actor_id")
    if len(set(branches)) != len(branches):
        failures.append("duplicate_branch")

    base_shas = {str(plan.get("base_sha", "")) for plan in plans}
    issue_numbers = {plan.get("issue_number") for plan in plans}
    run_ids = {str(plan.get("run_id", "")) for plan in plans}
    if len(base_shas) != 1:
        failures.append("base_sha_mismatch")
    if len(issue_numbers) != 1:
        failures.append("issue_number_mismatch")
    if len(run_ids) != 1:
        failures.append("run_id_mismatch")

    plans_by_actor = {
        str(plan.get("actor_id", "")): plan for plan in plans if plan.get("actor_id")
    }
    for plan in plans:
        actor = str(plan.get("actor_id", ""))
        for pattern in plan.get("write_set", []) or []:
            pattern = str(pattern)
            if _invalid_pattern(pattern):
                failures.append(f"invalid_write_pattern:{actor}:{pattern}")
        for dependency in plan.get("depends_on", []) or []:
            if dependency not in plans_by_actor:
                failures.append(f"unknown_dependency:{actor}:{dependency}")
            if dependency == actor:
                failures.append(f"self_dependency:{actor}")

    if _dependency_cycle(plans_by_actor):
        failures.append("dependency_cycle")

    for index, left in enumerate(plans):
        for right in plans[index + 1 :]:
            left_actor = str(left.get("actor_id", ""))
            right_actor = str(right.get("actor_id", ""))
            for left_pattern in left.get("write_set", []) or []:
                for right_pattern in right.get("write_set", []) or []:
                    if not patterns_overlap(str(left_pattern), str(right_pattern)):
                        continue
                    conflict = {
                        "actors": [left_actor, right_actor],
                        "patterns": [str(left_pattern), str(right_pattern)],
                        "reason": "write_set_overlap",
                    }
                    left_dependencies = set(left.get("depends_on", []) or [])
                    right_dependencies = set(right.get("depends_on", []) or [])
                    if right_actor in left_dependencies or left_actor in right_dependencies:
                        serialized.append(conflict)
                    else:
                        unresolved.append(conflict)

    veto = bool(failures or unresolved)
    return {
        "schemaVersion": 1,
        "plan_count": len(plans),
        "parallel_safe": not unresolved and not serialized and not failures,
        "serialized_conflicts": serialized,
        "unresolved_conflicts": unresolved,
        "failures": failures,
        "result": "VETO" if veto else "PASS",
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("plan_dir")
    parser.add_argument("--output")
    args = parser.parse_args()
    directory = pathlib.Path(args.plan_dir)
    plans = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(directory.glob("*.json"))
    ]
    result = evaluate_plans(plans)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
