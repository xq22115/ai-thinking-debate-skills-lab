#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
START = ROOT / "skills" / "task-goal-intelligence" / "scripts" / "goal_skill_start.py"
DEFAULT_CASES = ROOT / "evals" / "task-goal-native-state-cases.jsonl"


def load_runtime():
    spec = importlib.util.spec_from_file_location("goal_skill_start", START)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load goal_skill_start.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_cases(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict) or "id" not in row or "state" not in row or "expected_phase" not in row:
            raise ValueError(f"invalid case at line {number}")
        rows.append(row)
    return rows


def main() -> int:
    cases_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CASES
    runtime = load_runtime()
    errors: list[str] = []
    ids: list[str] = []
    phases: set[str] = set()

    for case in load_cases(cases_path):
        case_id = str(case["id"])
        ids.append(case_id)
        result = runtime.evaluate_state(case["state"])
        phases.add(result["phase"])
        if result["phase"] != case["expected_phase"]:
            errors.append(f"{case_id}: phase {result['phase']} != {case['expected_phase']}")
        if "expected_path" in case and result["path"] != case["expected_path"]:
            errors.append(f"{case_id}: path {result['path']} != {case['expected_path']}")
        if "expected_goal_version" in case and result["goal_version"] != case["expected_goal_version"]:
            errors.append(f"{case_id}: goal_version {result['goal_version']} != {case['expected_goal_version']}")
        for field in case.get("expected_missing", []):
            if field not in result["missing_core_fields"]:
                errors.append(f"{case_id}: expected missing field not reported: {field}")
        for gate, expected in (case.get("expected_gates") or {}).items():
            actual = result["gates"].get(gate)
            if actual is not expected:
                errors.append(f"{case_id}: gate {gate}={actual!r} != {expected!r}")

    if len(ids) != len(set(ids)):
        errors.append("duplicate case IDs")
    if len(ids) < 30:
        errors.append(f"insufficient state-machine cases: {len(ids)} < 30")
    required_phases = {"ORIENT", "DISCRIMINATE", "COMMIT", "EXECUTE", "VERIFY", "RECOVER", "LEARN"}
    if phases != required_phases:
        errors.append(f"phase coverage mismatch: {sorted(phases)}")

    payload = {
        "status": "PASS" if not errors else "FAIL",
        "cases": len(ids),
        "phases": sorted(phases),
        "errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
