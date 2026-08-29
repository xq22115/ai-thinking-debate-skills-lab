#!/usr/bin/env python3
"""Validate the global-policy durability, rehydration, and entrypoint contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(repo_root: Path, manifest_path: Path) -> list[str]:
    errors: list[str] = []

    try:
        manifest = json.loads(read_text(manifest_path))
    except Exception as exc:
        return [f"cannot load manifest: {exc}"]

    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    kernel = manifest.get("kernel") or {}
    kernel_rel = kernel.get("path")
    if not kernel_rel:
        errors.append("kernel.path is required")
    else:
        kernel_path = repo_root / kernel_rel
        if not kernel_path.is_file():
            errors.append(f"missing kernel: {kernel_rel}")
        else:
            size = kernel_path.stat().st_size
            max_bytes = int(kernel.get("max_bytes", 0) or 0)
            if max_bytes and size > max_bytes:
                errors.append(f"kernel exceeds max_bytes: {size} > {max_bytes}")

    budget = manifest.get("context_budget") or {}
    root_agents = repo_root / "AGENTS.md"
    if not root_agents.is_file():
        errors.append("missing root AGENTS.md")
    else:
        hard_max = int(budget.get("root_agents_hard_max_bytes", 0) or 0)
        size = root_agents.stat().st_size
        if hard_max and size > hard_max:
            errors.append(f"AGENTS.md exceeds hard context budget: {size} > {hard_max}")

    policies = manifest.get("canonical_policies") or []
    ids: list[str] = []
    owners: list[str] = []
    for policy in policies:
        pid = policy.get("id")
        owner = policy.get("semantic_owner")
        path = policy.get("path")
        if not pid or not owner or not path:
            errors.append(f"malformed canonical policy: {policy!r}")
            continue
        ids.append(pid)
        owners.append(owner)
        if not (repo_root / path).is_file():
            errors.append(f"missing canonical policy path: {path}")

    if len(ids) != len(set(ids)):
        errors.append("canonical policy ids must be unique")
    if len(owners) != len(set(owners)):
        errors.append("semantic_owner collisions are forbidden")

    for entry in manifest.get("entrypoints") or []:
        rel = entry.get("path")
        markers = entry.get("required_markers") or []
        if not rel:
            errors.append(f"entrypoint path missing: {entry!r}")
            continue
        path = repo_root / rel
        if not path.is_file():
            errors.append(f"missing entrypoint: {rel}")
            continue
        text = read_text(path)
        for marker in markers:
            if marker not in text:
                errors.append(f"entrypoint {rel} missing marker: {marker}")

    rehydration = manifest.get("rehydration") or {}
    if not rehydration.get("required"):
        errors.append("rehydration.required must be true")
    if not rehydration.get("silent_drop_forbidden"):
        errors.append("rehydration.silent_drop_forbidden must be true")
    triggers = set(rehydration.get("triggers") or [])
    required_triggers = {
        "context_compaction_or_summary_replacement",
        "cwd_repository_workspace_or_surface_change",
        "instruction_or_policy_revision_change",
        "active_instruction_provenance_unknown",
        "before_material_write_when_active_rules_cannot_be_proven_loaded",
    }
    missing = sorted(required_triggers - triggers)
    if missing:
        errors.append(f"missing required rehydration triggers: {missing}")

    provenance = manifest.get("instruction_provenance") or {}
    if not provenance.get("repository_presence_is_not_loaded"):
        errors.append("repository presence must not count as loaded instruction state")

    durable = manifest.get("durable_state") or {}
    if not durable.get("chat_history_is_not_canonical"):
        errors.append("chat history must not be canonical durable state")
    if not durable.get("failed_turn_quarantine"):
        errors.append("failed-turn quarantine must be enabled")

    platform_truth = manifest.get("platform_truth") or {}
    ordinary_chat = str(platform_truth.get("ordinary_chat", ""))
    if "not inherently global instructions" not in ordinary_chat:
        errors.append("ordinary_chat truth boundary must explicitly reject repo-presence-as-global-loading")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "manifest",
        nargs="?",
        default="control-plane/ai-system/configs/global-policy-manifest.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    manifest_path = repo_root / args.manifest
    errors = validate(repo_root, manifest_path)
    result = {
        "status": "PASS" if not errors else "FAIL",
        "manifest": str(manifest_path.relative_to(repo_root)),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
