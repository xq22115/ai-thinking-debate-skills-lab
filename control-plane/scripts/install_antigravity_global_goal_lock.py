#!/usr/bin/env python3
"""Project Antigravity goal-lock rules and five recovery subagents globally.

The installer projects the canonical always-on rule into ``~/.gemini/GEMINI.md``
and the five canonical custom subagents into ``~/.gemini/config/agents/``. It is
additive/idempotent, preserves unmanaged GEMINI.md content, backs up every
existing file before a material replacement, and writes each target atomically.
Repository presence alone is never treated as proof that Antigravity loaded the
projection; the caller must still read back the owning machine/runtime.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import tempfile


BEGIN = "<!-- AI-THINKING-DEBATE:ANTIGRAVITY-GOAL-LOCK:BEGIN -->"
END = "<!-- AI-THINKING-DEBATE:ANTIGRAVITY-GOAL-LOCK:END -->"
AGENT_NAMES = (
    "goal-contract-auditor",
    "route-recovery-engineer",
    "anti-evasion-red-team",
    "contribution-evidence-auditor",
    "owning-runtime-verifier",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _rule_body() -> str:
    source = _repo_root() / ".agents/rules/goal-fidelity-anti-evasion.md"
    text = source.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        closing = text.find("\n---\n", 4)
        if closing != -1:
            text = text[closing + 5 :]
    return text.strip()


def _managed_block() -> str:
    body = _rule_body()
    return (
        f"{BEGIN}\n"
        "# Antigravity Global Goal Fidelity / Anti-Evasion Rule\n\n"
        f"{body}\n"
        f"{END}"
    )


def _replace_managed(existing: str, block: str) -> str:
    start = existing.find(BEGIN)
    end = existing.find(END)
    if start == -1 and end == -1:
        prefix = existing.rstrip()
        return f"{prefix}\n\n{block}\n" if prefix else f"{block}\n"
    if start == -1 or end == -1 or end < start:
        raise ValueError("partial or malformed Antigravity goal-lock managed block")
    end += len(END)
    before = existing[:start].rstrip()
    after = existing[end:].lstrip("\n")
    pieces = [part for part in (before, block, after.rstrip()) if part]
    return "\n\n".join(pieces).rstrip() + "\n"


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _backup_path(path: Path, stamp: str) -> Path:
    candidate = path.with_name(f"{path.name}.goal-lock.bak.{stamp}")
    suffix = 1
    while candidate.exists():
        candidate = path.with_name(f"{path.name}.goal-lock.bak.{stamp}.{suffix}")
        suffix += 1
    return candidate


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _agent_sources() -> dict[str, str]:
    source_dir = _repo_root() / ".agents/agents"
    result: dict[str, str] = {}
    for name in AGENT_NAMES:
        path = source_dir / f"{name}.md"
        if not path.is_file():
            raise FileNotFoundError(f"missing canonical Antigravity subagent: {path}")
        text = path.read_text(encoding="utf-8")
        required = (
            f"name: {name}",
            "subagent: true",
            "mainAgent: false",
            "model: pro",
        )
        for marker in required:
            if marker not in text:
                raise ValueError(f"canonical subagent {name} missing marker: {marker}")
        result[name] = text
    return result


def install(home: Path, *, backup: bool = True) -> dict:
    resolved_home = home.expanduser().resolve()
    gemini_target = resolved_home / ".gemini/GEMINI.md"
    gemini_existing = gemini_target.read_text(encoding="utf-8") if gemini_target.exists() else ""
    block = _managed_block()
    gemini_desired = _replace_managed(gemini_existing, block)

    # Build and validate the complete projection plan before mutating any target.
    agent_sources = _agent_sources()
    agent_plans: list[dict] = []
    for name, desired in agent_sources.items():
        target = resolved_home / ".gemini/config/agents" / f"{name}.md"
        exists = target.exists()
        existing = target.read_text(encoding="utf-8") if exists else ""
        agent_plans.append(
            {
                "name": name,
                "target": target,
                "exists": exists,
                "existing": existing,
                "desired": desired,
                "changed": (not exists) or existing != desired,
            }
        )

    gemini_changed = gemini_desired != gemini_existing
    any_changed = gemini_changed or any(plan["changed"] for plan in agent_plans)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") if any_changed else ""

    gemini_backup: Path | None = None
    if gemini_changed:
        gemini_target.parent.mkdir(parents=True, exist_ok=True)
        if backup and gemini_target.exists():
            gemini_backup = _backup_path(gemini_target, stamp)
            _atomic_write(gemini_backup, gemini_existing)
        _atomic_write(gemini_target, gemini_desired)

    agent_results: list[dict] = []
    for plan in agent_plans:
        target: Path = plan["target"]
        backup_path: Path | None = None
        if plan["changed"]:
            if backup and plan["exists"]:
                backup_path = _backup_path(target, stamp)
                _atomic_write(backup_path, plan["existing"])
            _atomic_write(target, plan["desired"])
        agent_results.append(
            {
                "name": plan["name"],
                "target": str(target),
                "changed": bool(plan["changed"]),
                "backup": str(backup_path) if backup_path else None,
                "sha256": _sha256(plan["desired"]),
            }
        )

    return {
        "status": "UPDATED" if any_changed else "UNCHANGED",
        "changed": any_changed,
        "rule": {
            "target": str(gemini_target),
            "changed": gemini_changed,
            "backup": str(gemini_backup) if gemini_backup else None,
            "managed_block_sha256": _sha256(block),
            "begin_marker_count": gemini_desired.count(BEGIN),
            "end_marker_count": gemini_desired.count(END),
        },
        "agents": agent_results,
        "agent_count": len(agent_results),
        "all_agent_targets_global": all(
            "/.gemini/config/agents/" in result["target"] for result in agent_results
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Home directory whose .gemini/GEMINI.md and .gemini/config/agents should be updated.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip backup creation (intended for disposable test homes only).",
    )
    args = parser.parse_args()

    try:
        result = install(args.home, backup=not args.no_backup)
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
