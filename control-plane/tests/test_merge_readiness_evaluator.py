#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evaluate_merge_readiness.py"
spec = importlib.util.spec_from_file_location("evaluate_merge_readiness", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_latest_failure_masks_older_success() -> None:
    runs = [
        {
            "id": 10,
            "name": "Core CI",
            "head_sha": "abc",
            "created_at": "2026-08-17T01:00:00Z",
            "status": "completed",
            "conclusion": "success",
        },
        {
            "id": 11,
            "name": "Core CI",
            "head_sha": "abc",
            "created_at": "2026-08-17T01:01:00Z",
            "status": "completed",
            "conclusion": "failure",
        },
    ]
    selected, matches = module.latest_run_for(runs, "Core CI", "abc")
    assert selected and selected["id"] == 11
    assert len(matches) == 2
    assert module.selected_run_succeeded(selected) is False


def test_latest_success_wins_after_rerun() -> None:
    runs = [
        {
            "id": 20,
            "name": "Core CI",
            "head_sha": "abc",
            "created_at": "2026-08-17T01:00:00Z",
            "status": "completed",
            "conclusion": "failure",
        },
        {
            "id": 21,
            "name": "Core CI",
            "head_sha": "abc",
            "created_at": "2026-08-17T01:02:00Z",
            "status": "completed",
            "conclusion": "success",
        },
    ]
    selected, _ = module.latest_run_for(runs, "Core CI", "abc")
    assert selected and selected["id"] == 21
    assert module.selected_run_succeeded(selected) is True


def test_same_timestamp_uses_higher_run_id_as_latest() -> None:
    runs = [
        {
            "id": 40,
            "name": "Core CI",
            "head_sha": "abc",
            "created_at": "2026-08-17T03:00:00Z",
            "status": "completed",
            "conclusion": "success",
        },
        {
            "id": 41,
            "name": "Core CI",
            "head_sha": "abc",
            "created_at": "2026-08-17T03:00:00Z",
            "status": "completed",
            "conclusion": "failure",
        },
    ]
    selected, _ = module.latest_run_for(runs, "Core CI", "abc")
    assert selected and selected["id"] == 41
    assert module.selected_run_succeeded(selected) is False


def test_control_plane_paths_come_from_policy() -> None:
    policy = {
        "control_plane": {
            "paths": [".github/**", "scripts/apply_agent_core_admin.py"],
            "dependabot_protected_allowlist": [".github/workflows/**"],
        }
    }
    risk = module.determine_risk(["scripts/apply_agent_core_admin.py"], policy)
    assert risk["control_plane"] is True
    assert risk["protected_paths"] == ["scripts/apply_agent_core_admin.py"]
    assert risk["failures"] == []


def test_missing_control_plane_policy_fails_closed() -> None:
    risk = module.determine_risk(["src/app.py"], {})
    assert risk["failures"]


def test_manifest_routing_is_path_aware() -> None:
    manifest = {
        "version": 1,
        "required_checks": {
            "workflows": [
                {"name": "PR Risk Router", "mode": "always"},
                {
                    "name": "Validate Agent Admin Convergence",
                    "mode": "paths",
                    "paths": ["scripts/apply_agent_core_admin.py"],
                },
            ]
        },
    }
    required, failures = module.required_workflow_names(
        ["scripts/apply_agent_core_admin.py"], manifest
    )
    assert failures == []
    assert required == ["PR Risk Router", "Validate Agent Admin Convergence"]


def test_unrelated_head_runs_are_ignored() -> None:
    runs = [
        {
            "id": 30,
            "name": "Core CI",
            "head_sha": "old",
            "created_at": "2026-08-17T02:00:00Z",
            "status": "completed",
            "conclusion": "success",
        }
    ]
    selected, matches = module.latest_run_for(runs, "Core CI", "new")
    assert selected is None
    assert matches == []


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"merge_readiness_evaluator_tests=PASS count={len(tests)}")
