#!/usr/bin/env python3
"""Validate Agent Core required-check routing against actual GitHub workflow triggers.

This compiler checks the contract between `.github/required-checks.yml` and the
`on.pull_request` trigger of every workflow referenced by the manifest. It is
purposefully dependency-free so it can run on GitHub-hosted runners without
installing a YAML package.

The main safety invariant is simple: if Merge Readiness can require a workflow
for a changed path, GitHub must be able to trigger that workflow for the same
path. Otherwise a PR can become permanently blocked waiting for a check that
will never exist.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Iterable

_GLOB_CHARS = set("*?[")
_REQUIRED_DEFAULT_PR_TYPES = {"opened", "synchronize", "reopened"}


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _inline_list(value: str) -> list[str]:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return []
    body = value[1:-1].strip()
    if not body:
        return []
    return [_scalar(item.strip()) for item in body.split(",") if item.strip()]


@dataclass(frozen=True)
class ManifestEntry:
    name: str
    mode: str
    paths: tuple[str, ...]


@dataclass(frozen=True)
class WorkflowContract:
    path: str
    name: str
    has_pull_request: bool
    pull_request_paths: tuple[str, ...] | None
    pull_request_paths_ignore: tuple[str, ...]
    pull_request_types: tuple[str, ...] | None


def parse_manifest(text: str) -> list[ManifestEntry]:
    lines = text.splitlines()
    entries: list[ManifestEntry] = []
    current_name: str | None = None
    current_mode: str | None = None
    current_paths: list[str] = []
    collecting_paths = False

    def flush() -> None:
        nonlocal current_name, current_mode, current_paths, collecting_paths
        if current_name is not None:
            entries.append(
                ManifestEntry(
                    name=current_name,
                    mode=current_mode or "",
                    paths=tuple(current_paths),
                )
            )
        current_name = None
        current_mode = None
        current_paths = []
        collecting_paths = False

    for raw in lines:
        line = raw.rstrip()
        name_match = re.match(r"^\s{4}-\s+name:\s*(.+?)\s*$", line)
        if name_match:
            flush()
            current_name = _scalar(name_match.group(1))
            continue
        if current_name is None:
            continue
        mode_match = re.match(r"^\s{6}mode:\s*(\S+)\s*$", line)
        if mode_match:
            current_mode = _scalar(mode_match.group(1))
            collecting_paths = False
            continue
        if re.match(r"^\s{6}paths:\s*$", line):
            collecting_paths = True
            continue
        if collecting_paths:
            path_match = re.match(r"^\s{8}-\s*(.+?)\s*$", line)
            if path_match:
                current_paths.append(_scalar(path_match.group(1)))
                continue
            if line.strip() and _indent(line) <= 6:
                collecting_paths = False
    flush()
    return entries


def _collect_block_list(lines: list[str], start: int, item_indent: int) -> tuple[list[str], int]:
    values: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        match = re.match(rf"^\s{{{item_indent}}}-\s*(.+?)\s*$", line)
        if not match:
            break
        values.append(_scalar(match.group(1)))
        i += 1
    return values, i


def parse_workflow(path: pathlib.Path) -> WorkflowContract:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    top_name = ""
    for line in lines:
        match = re.match(r"^name:\s*(.+?)\s*$", line.rstrip())
        if match:
            top_name = _scalar(match.group(1))
            break

    has_pull_request = False
    pr_paths: list[str] | None = None
    paths_ignore: list[str] = []
    pr_types: list[str] | None = None

    for i, raw in enumerate(lines):
        line = raw.rstrip()
        match = re.match(r"^\s{2}pull_request:\s*(.*?)\s*$", line)
        if not match:
            continue
        has_pull_request = True
        inline = match.group(1).strip()
        # `pull_request: {}` or an empty mapping is universal unless nested
        # path filters say otherwise.
        j = i + 1
        while j < len(lines):
            child = lines[j].rstrip()
            if not child.strip() or child.lstrip().startswith("#"):
                j += 1
                continue
            if _indent(child) <= 2:
                break
            paths_match = re.match(r"^\s{4}paths:\s*(.*?)\s*$", child)
            if paths_match:
                rest = paths_match.group(1)
                inline_paths = _inline_list(rest)
                if inline_paths:
                    pr_paths = inline_paths
                    j += 1
                    continue
                values, j = _collect_block_list(lines, j + 1, 6)
                pr_paths = values
                continue
            ignore_match = re.match(r"^\s{4}paths-ignore:\s*(.*?)\s*$", child)
            if ignore_match:
                rest = ignore_match.group(1)
                inline_values = _inline_list(rest)
                if inline_values:
                    paths_ignore = inline_values
                    j += 1
                    continue
                values, j = _collect_block_list(lines, j + 1, 6)
                paths_ignore = values
                continue
            types_match = re.match(r"^\s{4}types:\s*(.*?)\s*$", child)
            if types_match:
                rest = types_match.group(1)
                inline_values = _inline_list(rest)
                if inline_values:
                    pr_types = inline_values
                    j += 1
                    continue
                values, j = _collect_block_list(lines, j + 1, 6)
                pr_types = values
                continue
            j += 1
        break

    return WorkflowContract(
        path=path.as_posix(),
        name=top_name,
        has_pull_request=has_pull_request,
        pull_request_paths=None if pr_paths is None else tuple(pr_paths),
        pull_request_paths_ignore=tuple(paths_ignore),
        pull_request_types=None if pr_types is None else tuple(pr_types),
    )


def _static_prefix(pattern: str) -> str:
    positions = [pattern.find(char) for char in _GLOB_CHARS if char in pattern]
    cut = min(positions) if positions else len(pattern)
    return pattern[:cut].rstrip("/")


def pattern_covers(trigger_pattern: str, required_pattern: str) -> bool:
    if trigger_pattern == required_pattern:
        return True
    if trigger_pattern in {"**", "**/*", "*"}:
        return True

    required_is_literal = not any(char in required_pattern for char in _GLOB_CHARS)
    if required_is_literal and fnmatch.fnmatchcase(required_pattern, trigger_pattern):
        return True

    if trigger_pattern.endswith("/**"):
        trigger_prefix = trigger_pattern[:-3].rstrip("/")
        required_prefix = _static_prefix(required_pattern)
        return required_prefix == trigger_prefix or required_prefix.startswith(trigger_prefix + "/")

    return False


def validate_contracts(manifest: pathlib.Path, workflows_dir: pathlib.Path) -> dict[str, object]:
    entries = parse_manifest(manifest.read_text(encoding="utf-8"))
    workflow_files = sorted([*workflows_dir.glob("*.yml"), *workflows_dir.glob("*.yaml")])
    contracts = [parse_workflow(path) for path in workflow_files]

    failures: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    by_name: dict[str, list[WorkflowContract]] = {}
    for contract in contracts:
        if contract.name:
            by_name.setdefault(contract.name, []).append(contract)

    seen_manifest_names: set[str] = set()
    for entry in entries:
        if entry.name in seen_manifest_names:
            failures.append({"kind": "duplicate-manifest-name", "workflow": entry.name})
            continue
        seen_manifest_names.add(entry.name)

        matches = by_name.get(entry.name, [])
        if len(matches) != 1:
            failures.append(
                {
                    "kind": "workflow-name-resolution",
                    "workflow": entry.name,
                    "matches": [item.path for item in matches],
                    "expected_match_count": 1,
                }
            )
            continue

        contract = matches[0]
        if not contract.has_pull_request:
            failures.append(
                {"kind": "missing-pull-request-trigger", "workflow": entry.name, "path": contract.path}
            )
            continue

        if contract.pull_request_paths_ignore:
            failures.append(
                {
                    "kind": "paths-ignore-unsafe-for-required-check",
                    "workflow": entry.name,
                    "path": contract.path,
                    "paths_ignore": list(contract.pull_request_paths_ignore),
                }
            )

        if contract.pull_request_types is not None:
            missing_types = sorted(_REQUIRED_DEFAULT_PR_TYPES - set(contract.pull_request_types))
            if missing_types:
                failures.append(
                    {
                        "kind": "pull-request-types-may-miss-current-head",
                        "workflow": entry.name,
                        "path": contract.path,
                        "missing_types": missing_types,
                    }
                )

        if entry.mode == "always":
            if contract.pull_request_paths is not None:
                failures.append(
                    {
                        "kind": "always-check-is-path-filtered",
                        "workflow": entry.name,
                        "path": contract.path,
                        "trigger_paths": list(contract.pull_request_paths),
                    }
                )
        elif entry.mode == "paths":
            if not entry.paths:
                failures.append({"kind": "manifest-paths-empty", "workflow": entry.name})
                continue
            if contract.pull_request_paths is None:
                warnings.append(
                    {
                        "kind": "path-scoped-check-runs-universally",
                        "workflow": entry.name,
                        "path": contract.path,
                    }
                )
                continue
            uncovered = [
                required
                for required in entry.paths
                if not any(pattern_covers(trigger, required) for trigger in contract.pull_request_paths)
            ]
            if uncovered:
                failures.append(
                    {
                        "kind": "manifest-path-not-triggerable",
                        "workflow": entry.name,
                        "path": contract.path,
                        "uncovered_manifest_paths": uncovered,
                        "trigger_paths": list(contract.pull_request_paths),
                    }
                )
        else:
            failures.append(
                {"kind": "unknown-manifest-mode", "workflow": entry.name, "mode": entry.mode}
            )

    return {
        "schemaVersion": 1,
        "manifest": manifest.as_posix(),
        "workflow_directory": workflows_dir.as_posix(),
        "manifest_workflow_count": len(entries),
        "workflow_file_count": len(workflow_files),
        "failures": failures,
        "warnings": warnings,
        "result": "PASS" if not failures else "FAIL",
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=".github/required-checks.yml")
    parser.add_argument("--workflows", default=".github/workflows")
    parser.add_argument("--output", default="control-contract-receipt.json")
    args = parser.parse_args(list(argv) if argv is not None else None)

    receipt = validate_contracts(pathlib.Path(args.manifest), pathlib.Path(args.workflows))
    pathlib.Path(args.output).write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
