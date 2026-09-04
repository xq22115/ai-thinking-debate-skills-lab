#!/usr/bin/env python3
"""Additive OpenClaw adapter installer for AI Efficiency Operating System.

This installer edits only documented OpenClaw config paths, preserves existing
array entries, never lowers configured concurrency, backs up the active config,
and validates the resulting configuration. It does not install models,
credentials, or change provider/auth settings.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ADAPTER_SKILLS = [
    "openclaw-goal-orchestrator",
    "openclaw-evidence-gate",
    "openclaw-runtime-recovery",
    "openclaw-learning-loop",
]
PRODUCTION_TOOLS = ["sessions_spawn", "sessions_yield", "subagents", "skill_workshop"]
LAB_TOOLS = PRODUCTION_TOOLS + ["agents_wait"]


class InstallError(RuntimeError):
    pass


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(args, text=True, capture_output=True)
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise InstallError(f"command failed ({proc.returncode}): {' '.join(args)}\n{detail}")
    return proc


def openclaw(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["openclaw", *args], check=check)


def get_json(path: str) -> tuple[bool, Any]:
    proc = openclaw("config", "get", path, "--json", check=False)
    if proc.returncode != 0:
        return False, None
    try:
        return True, json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise InstallError(f"non-JSON response from config get {path}") from exc


def set_value(path: str, value: Any, *, dry_run: bool) -> str:
    exists, current = get_json(path)
    if exists and current == value:
        return f"KEEP {path}={json.dumps(value, ensure_ascii=False)}"

    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    args = ["config", "set", path, encoded, "--strict-json"]
    if dry_run:
        args.append("--dry-run")
    else:
        if exists:
            args += ["--expect-current-json", json.dumps(current, ensure_ascii=False, separators=(",", ":"))]
        else:
            args.append("--expect-current-absent")
    openclaw(*args)
    return f"{'DRY-RUN' if dry_run else 'SET'} {path}={encoded}"


def append_unique(path: str, additions: list[str], *, dry_run: bool) -> str:
    exists, current = get_json(path)
    if not exists:
        current = []
    if not isinstance(current, list) or any(not isinstance(item, str) for item in current):
        raise InstallError(f"{path} must be a string array; found {type(current).__name__}")
    merged = list(current)
    for item in additions:
        if item not in merged:
            merged.append(item)
    return set_value(path, merged, dry_run=dry_run)


def numeric_floor(path: str, floor: int, *, dry_run: bool) -> str:
    exists, current = get_json(path)
    if exists:
        if isinstance(current, bool) or not isinstance(current, (int, float)):
            raise InstallError(f"{path} must be numeric to apply a floor")
        desired = max(int(current), floor)
    else:
        desired = floor
    return set_value(path, desired, dry_run=dry_run)


def active_config_path() -> Path:
    proc = openclaw("config", "file", "--json")
    data = json.loads(proc.stdout)
    path = data.get("path")
    if not isinstance(path, str) or not path:
        raise InstallError("openclaw config file --json did not return a path")
    return Path(path).expanduser().resolve()


def backup_config(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = path.with_name(f"{path.name}.aos-openclaw-backup-{stamp}")
    shutil.copy2(path, backup)
    try:
        os.chmod(backup, 0o600)
    except OSError:
        pass
    return backup


def adapter_root() -> Path:
    return Path(__file__).resolve().parents[1]


def skill_root() -> Path:
    return adapter_root() / "skills"


def require_runtime() -> None:
    if shutil.which("openclaw") is None:
        raise InstallError("openclaw CLI is not on PATH")
    openclaw("--version")


def configure(args: argparse.Namespace) -> list[str]:
    changes: list[str] = []
    root = str(skill_root().resolve())
    changes.append(append_unique("skills.load.extraDirs", [root], dry_run=args.dry_run))
    changes.append(set_value("skills.load.watch", True, dry_run=args.dry_run))

    if args.learning != "keep":
        changes.append(
            set_value("skills.workshop.autonomous.mode", args.learning, dry_run=args.dry_run)
        )
        if args.learning == "auto":
            changes.append(set_value("skills.workshop.approvalPolicy", "auto", dry_run=args.dry_run))

    tools = LAB_TOOLS if args.mode == "lab" else PRODUCTION_TOOLS
    changes.append(append_unique("tools.alsoAllow", tools, dry_run=args.dry_run))
    changes.append(
        set_value("agents.defaults.subagents.delegationMode", "prefer", dry_run=args.dry_run)
    )
    changes.append(numeric_floor("agents.defaults.maxConcurrent", 4, dry_run=args.dry_run))
    changes.append(
        numeric_floor("agents.defaults.subagents.maxConcurrent", 8, dry_run=args.dry_run)
    )

    # Respect existing skill visibility policy. If a default/agent allowlist exists,
    # append the adapter skills instead of replacing that list.
    default_exists, _ = get_json("agents.defaults.skills")
    if default_exists:
        changes.append(
            append_unique("agents.defaults.skills", ADAPTER_SKILLS, dry_run=args.dry_run)
        )
    if args.agent:
        agent_path = f"agents.entries.{args.agent}.skills"
        agent_exists, _ = get_json(agent_path)
        if agent_exists:
            changes.append(append_unique(agent_path, ADAPTER_SKILLS, dry_run=args.dry_run))

    if args.mode == "lab":
        changes.append(set_value("tools.codeMode", True, dry_run=args.dry_run))
        changes.append(set_value("tools.swarm.enabled", True, dry_run=args.dry_run))
        changes.append(numeric_floor("tools.swarm.maxConcurrent", 8, dry_run=args.dry_run))
        changes.append(
            numeric_floor("tools.swarm.maxChildrenPerGroup", 50, dry_run=args.dry_run)
        )
        changes.append(
            numeric_floor("tools.swarm.maxTotalPerGroup", 200, dry_run=args.dry_run)
        )
        changes.append(
            numeric_floor("tools.swarm.waitTimeoutSecondsMax", 600, dry_run=args.dry_run)
        )

    return changes


def verify(args: argparse.Namespace) -> None:
    openclaw("config", "validate")
    list_args = ["skills", "list", "--json"]
    if args.agent:
        list_args += ["--agent", args.agent]
    proc = openclaw(*list_args)
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        payload = proc.stdout

    text = json.dumps(payload, ensure_ascii=False) if not isinstance(payload, str) else payload
    missing = [name for name in ADAPTER_SKILLS if name not in text]
    if missing:
        raise InstallError(
            "config is valid, but adapter skills are not visible yet: "
            + ", ".join(missing)
            + ". Start a new session or restart the Gateway, then rerun with --verify-only."
        )

    for name in ADAPTER_SKILLS:
        info_args = ["skills", "info", name, "--json"]
        if args.agent:
            info_args += ["--agent", args.agent]
        openclaw(*info_args)

    if args.deep_verify:
        openclaw("doctor", "--deep")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["production", "lab"], default="production")
    parser.add_argument("--learning", choices=["auto", "propose", "keep"], default="auto")
    parser.add_argument("--agent", help="Optional OpenClaw agent id whose explicit skill allowlist should be extended.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--deep-verify", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        require_runtime()
        if args.verify_only:
            verify(args)
            print("OPENCLAW_ADAPTER_VERIFIED")
            return 0

        config = active_config_path()
        backup = None if args.dry_run else backup_config(config)
        changes = configure(args)
        for line in changes:
            print(line)

        if args.dry_run:
            print("DRY_RUN_COMPLETE")
            return 0

        verify(args)
        print(f"CONFIG_BACKUP={backup}" if backup else "CONFIG_BACKUP=none-config-created-by-openclaw")
        print(f"MODE={args.mode}")
        print(f"LEARNING={args.learning}")
        print("OPENCLAW_ADAPTER_VERIFIED")
        return 0
    except (InstallError, json.JSONDecodeError, OSError) as exc:
        print(f"OPENCLAW_ADAPTER_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
