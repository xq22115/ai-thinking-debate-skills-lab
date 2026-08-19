#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_control_contracts.py"
spec = importlib.util.spec_from_file_location("validate_control_contracts", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def write(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def validate(manifest_text: str, workflows: dict[str, str]):
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        manifest = root / ".github" / "required-checks.yml"
        workflow_dir = root / ".github" / "workflows"
        write(manifest, manifest_text)
        for filename, text in workflows.items():
            write(workflow_dir / filename, text)
        return module.validate_contracts(manifest, workflow_dir)


def manifest(name: str, mode: str, paths: list[str] | None = None) -> str:
    lines = ["version: 1", "required_checks:", "  workflows:", f"    - name: {name}", f"      mode: {mode}"]
    if paths is not None:
        lines.append("      paths:")
        lines.extend(f"        - {path}" for path in paths)
    return "\n".join(lines) + "\n"


def workflow(name: str, trigger_lines: list[str]) -> str:
    return "\n".join([f"name: {name}", "", "on:", *trigger_lines, "", "jobs:", "  test:", "    runs-on: ubuntu-latest"]) + "\n"


def assert_has_failure(receipt, kind: str) -> None:
    kinds = [item["kind"] for item in receipt["failures"]]
    assert kind in kinds, (kind, receipt)


def test_exact_path_contract_passes() -> None:
    receipt = validate(
        manifest("Validate Admin", "paths", ["docs/admin.md"]),
        {"admin.yml": workflow("Validate Admin", ["  pull_request:", "    paths:", "      - docs/admin.md"])},
    )
    assert receipt["result"] == "PASS", receipt


def test_broader_prefix_trigger_covers_manifest_path() -> None:
    receipt = validate(
        manifest("Workflow Security", "paths", [".github/workflows/**"]),
        {"security.yml": workflow("Workflow Security", ["  pull_request:", "    paths:", "      - .github/**"])},
    )
    assert receipt["result"] == "PASS", receipt


def test_missing_trigger_path_fails() -> None:
    receipt = validate(
        manifest("Agent Core Health", "paths", ["scripts/apply_agent_core_admin.py"]),
        {"health.yml": workflow("Agent Core Health", ["  pull_request:", "    paths:", "      - .github/**"])},
    )
    assert_has_failure(receipt, "manifest-path-not-triggerable")


def test_always_check_cannot_be_path_filtered() -> None:
    receipt = validate(
        manifest("Core CI", "always"),
        {"ci.yml": workflow("Core CI", ["  pull_request:", "    paths:", "      - src/**"])},
    )
    assert_has_failure(receipt, "always-check-is-path-filtered")


def test_paths_ignore_is_rejected_for_required_check() -> None:
    receipt = validate(
        manifest("Core CI", "always"),
        {"ci.yml": workflow("Core CI", ["  pull_request:", "    paths-ignore:", "      - docs/**"])},
    )
    assert_has_failure(receipt, "paths-ignore-unsafe-for-required-check")


def test_explicit_types_must_keep_default_current_head_events() -> None:
    receipt = validate(
        manifest("Core CI", "always"),
        {"ci.yml": workflow("Core CI", ["  pull_request:", "    types: [opened, reopened]"])},
    )
    assert_has_failure(receipt, "pull-request-types-may-miss-current-head")


def test_duplicate_workflow_names_fail_resolution() -> None:
    receipt = validate(
        manifest("Core CI", "always"),
        {
            "ci-a.yml": workflow("Core CI", ["  pull_request:"]),
            "ci-b.yml": workflow("Core CI", ["  pull_request:"]),
        },
    )
    assert_has_failure(receipt, "workflow-name-resolution")


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"control_contract_unit_tests=PASS count={len(tests)}")
