#!/usr/bin/env python3
"""Install the repository's canonical skill-authoring capability into Copilot user scope.

This is an explicit foreground installer. It creates no background service.
It backs up an existing target, copies the canonical package, and emits a
hash-bound read-back receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): sha256(p)
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def backup(path: Path, stamp: str) -> str | None:
    if not path.exists():
        return None
    target = path.with_name(f"{path.name}.bak-{stamp}")
    path.rename(target)
    return str(target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--copilot-home",
        type=Path,
        default=Path.home() / ".copilot",
        help="Copilot user configuration directory (default: ~/.copilot)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    source_skill = repo_root / "skills" / "skills" / "skill-authoring-engine"
    source_agent = repo_root / "deploy" / "copilot-user" / "skill-architect.agent.md"

    if not (source_skill / "SKILL.md").is_file():
        raise SystemExit(f"missing canonical skill: {source_skill / 'SKILL.md'}")
    if not source_agent.is_file():
        raise SystemExit(f"missing personal agent projection: {source_agent}")

    skill_target = args.copilot_home / "skills" / "skill-authoring-engine"
    agent_target = args.copilot_home / "agents" / "skill-architect.agent.md"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    plan = {
        "source_skill": str(source_skill),
        "source_agent": str(source_agent),
        "skill_target": str(skill_target),
        "agent_target": str(agent_target),
        "dry_run": args.dry_run,
    }
    if args.dry_run:
        print(json.dumps({"status": "DRY_RUN", **plan}, indent=2))
        return 0

    args.copilot_home.mkdir(parents=True, exist_ok=True)
    skill_target.parent.mkdir(parents=True, exist_ok=True)
    agent_target.parent.mkdir(parents=True, exist_ok=True)

    backups = {
        "skill": backup(skill_target, stamp),
        "agent": backup(agent_target, stamp),
    }

    shutil.copytree(source_skill, skill_target)
    shutil.copy2(source_agent, agent_target)

    source_hashes = snapshot(source_skill)
    target_hashes = snapshot(skill_target)
    agent_source_hash = sha256(source_agent)
    agent_target_hash = sha256(agent_target)

    verified = (
        source_hashes == target_hashes
        and agent_source_hash == agent_target_hash
        and (skill_target / "SKILL.md").is_file()
        and agent_target.is_file()
    )

    receipt = {
        "status": "PASS" if verified else "FAIL",
        **plan,
        "backups": backups,
        "skill_hashes": target_hashes,
        "agent_sha256": agent_target_hash,
        "copied_file_count": len(target_hashes) + 1,
        "repository_projection_only": False,
        "copilot_host_loaded_or_executed": False,
        "note": "Filesystem installation/read-back is verified; Copilot discovery/execution requires a subsequent host run.",
    }
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if verified else 1


if __name__ == "__main__":
    raise SystemExit(main())
