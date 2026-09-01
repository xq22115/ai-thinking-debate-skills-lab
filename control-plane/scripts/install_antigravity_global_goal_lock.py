#!/usr/bin/env python3
"""Project the canonical Antigravity goal-lock rule into ~/.gemini/GEMINI.md.

The installer is additive and idempotent: it owns one fenced block, preserves all
unmanaged user content, creates a timestamped backup before material changes,
and writes atomically. Repository presence alone is not treated as global load.
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


def install(home: Path, *, backup: bool = True) -> dict:
    target = home.expanduser().resolve() / ".gemini/GEMINI.md"
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    block = _managed_block()
    desired = _replace_managed(existing, block)
    changed = desired != existing
    backup_path: Path | None = None

    if changed:
        target.parent.mkdir(parents=True, exist_ok=True)
        if backup and target.exists():
            stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup_path = target.with_name(f"{target.name}.goal-lock.bak.{stamp}")
            suffix = 1
            while backup_path.exists():
                backup_path = target.with_name(
                    f"{target.name}.goal-lock.bak.{stamp}.{suffix}"
                )
                suffix += 1
            backup_path.write_text(existing, encoding="utf-8")
        _atomic_write(target, desired)

    digest = hashlib.sha256(block.encode("utf-8")).hexdigest()
    return {
        "status": "UPDATED" if changed else "UNCHANGED",
        "target": str(target),
        "changed": changed,
        "backup": str(backup_path) if backup_path else None,
        "managed_block_sha256": digest,
        "begin_marker_count": desired.count(BEGIN),
        "end_marker_count": desired.count(END),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Home directory whose .gemini/GEMINI.md should be updated.",
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
