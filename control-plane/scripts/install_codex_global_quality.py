#!/usr/bin/env python3
"""Safely install the continuous-quality contract into Codex user instructions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


BEGIN_MARKER = "<!-- BEGIN AI-THINKING-DEBATE-SKILLS-LAB CONTINUOUS-QUALITY -->"
END_MARKER = "<!-- END AI-THINKING-DEBATE-SKILLS-LAB CONTINUOUS-QUALITY -->"
BACKUP_DIRNAME = "quality-installer-backups"

POLICY = """# Continuous Quality + Durability Kernel

Optimize for verified goal completion, not artificial conservatism, ceremony, delay, token count, or source count.

Truth lock:
- never claim an action, source, state, or completion that was not observed;
- UNKNOWN is first-class;
- configured, registered, loaded, executed, and observable effect are different states.

Goal and capability:
- compile the real objective, desired end state, hard constraints, negations, acceptance tests, and protected capabilities;
- keep the goal stable while changing routes aggressively when evidence justifies it;
- terminology alone is not intent; judge the actual requested action, context, authorization, actionability, and risk;
- narrow only the necessary portion and continue useful allowed work;
- do not solve one symptom by silently disabling a required capability.

Expert problem solving:
- compare causally distinct routes rather than renaming the same attempt;
- use direct repair, alternate layer, diagnostic change, bridge/adapter/wrapper, compatibility path, state reconstruction, shadow/canary, or rollback when they better fit the mechanism;
- after two materially similar failures, another materially similar retry is forbidden until the hypothesis, mechanism, instrument, environment, evidence family, or verification method changes;
- current primary docs, source/commits/issues, practitioner evidence, and runtime reproduction have different roles; popularity is discovery, not proof.

No silent policy decay:
- repository or file presence is not proof the instruction was loaded;
- conversation summaries are caches/indexes, not canonical mutable state;
- failed turns, partial streams, empty messages, tool errors, and stale summaries do not automatically become durable truth;
- keep broad-scope instructions small and demand-load detail instead of growing one monolithic prompt.

Rehydrate the active instruction stack when possible at session/thread start, after context compaction or summary replacement, after cwd/repository/workspace/surface changes, after instruction revision changes, when provenance is unknown or contradictory, and before material writes when active rules cannot be proven loaded.
Rehydrate by resolving host/surface and instruction precedence/provenance, restoring the goal contract and unresolved gates from durable state, loading only task-relevant policy/skill detail, quarantining stale/failed context, and recording which instruction sources/revisions were actually loaded.

For non-trivial work:
- reconstruct the real current state and causal path before editing;
- choose high-information-gain investigation over symptom patching;
- preserve working behavior unless the task explicitly changes it;
- verify at the highest practical layer: runtime/user path > integration/functional > read-back > unit/static > configuration inspection;
- a file write, command exit, CI status, PR creation, or agent self-report is not completion evidence by itself;
- challenge material results with a contradiction, edge case, alternate-path, or adversarial check when practical;
- continue foreseeable work until every hard acceptance criterion is satisfied or a concrete external dependency blocks further progress.

Never simulate deep thinking with sleep, slow streaming, artificial first-token delay, or fixed research quotas. Use the maximum useful reasoning, research, testing, route freedom, and independent evaluation justified by uncertainty and impact.
"""


class ManagedBlockError(ValueError):
    """Raised when a managed block is structurally unsafe to modify."""


def managed_block() -> str:
    return f"{BEGIN_MARKER}\n{POLICY.strip()}\n{END_MARKER}"


def read_text_exact(path: Path) -> str:
    """Read UTF-8 without universal-newline translation."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text_exact(path: Path, content: str) -> None:
    """Write UTF-8 without platform newline translation."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(content)


def resolve_codex_home(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    if os.environ.get("CODEX_HOME"):
        return Path(os.environ["CODEX_HOME"]).expanduser()
    return Path.home() / ".codex"


def active_agents_file(codex_home: Path) -> Path:
    """Mirror Codex global-instruction precedence: non-empty override, then AGENTS."""
    override = codex_home / "AGENTS.override.md"
    if override.is_file() and read_text_exact(override).strip():
        return override
    return codex_home / "AGENTS.md"


def managed_region(content: str) -> tuple[int, int] | None:
    """Return the exact managed region, rejecting duplicate or broken markers."""
    begin_count = content.count(BEGIN_MARKER)
    end_count = content.count(END_MARKER)
    if begin_count == 0 and end_count == 0:
        return None
    if begin_count != 1 or end_count != 1:
        raise ManagedBlockError(
            f"unsafe managed-marker cardinality: begin={begin_count}, end={end_count}"
        )
    start = content.find(BEGIN_MARKER)
    end_start = content.find(END_MARKER)
    if end_start < start:
        raise ManagedBlockError("managed block end marker precedes begin marker")
    return start, end_start + len(END_MARKER)


def backup_existing(codex_home: Path, target: Path, content: str) -> Path | None:
    """Create a content-addressed rollback copy once for each original state."""
    if not target.exists():
        return None
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
    backup_dir = codex_home / BACKUP_DIRNAME
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f"{target.name}.{digest}.bak"
    if not backup.exists():
        write_text_exact(backup, content)
    return backup


def atomic_write(target: Path, content: str) -> None:
    """Replace one instruction file atomically while retaining its mode when possible."""
    target.parent.mkdir(parents=True, exist_ok=True)
    prior_mode = target.stat().st_mode if target.exists() else None
    temp = target.with_name(f".{target.name}.tmp-{os.getpid()}")
    try:
        write_text_exact(temp, content)
        if prior_mode is not None:
            os.chmod(temp, prior_mode)
        os.replace(temp, target)
    finally:
        if temp.exists():
            temp.unlink()


def content_with_installed_block(existing: str) -> tuple[str, bool]:
    block = managed_block()
    region = managed_region(existing)
    if region is not None:
        start, end = region
        current = existing[start:end]
        if current == block:
            return existing, False
        return existing[:start] + block + existing[end:], True

    if not existing:
        return f"{block}\n", True
    if existing.endswith("\n\n"):
        separator = ""
    elif existing.endswith("\n"):
        separator = "\n"
    else:
        separator = "\n\n"
    return f"{existing}{separator}{block}\n", True


def install(codex_home: Path) -> dict[str, object]:
    codex_home.mkdir(parents=True, exist_ok=True)
    target = active_agents_file(codex_home)
    existing = read_text_exact(target) if target.exists() else ""
    content, changed = content_with_installed_block(existing)
    backup = None
    if changed:
        backup = backup_existing(codex_home, target, existing)
        atomic_write(target, content)
    return {
        "status": "PASS",
        "command": "install",
        "target": str(target),
        "changed": changed,
        "backup": str(backup) if backup else None,
    }


def check(codex_home: Path) -> dict[str, object]:
    target = active_agents_file(codex_home)
    content = read_text_exact(target) if target.exists() else ""
    try:
        region = managed_region(content)
        installed = region is not None and content[region[0] : region[1]] == managed_block()
        error = None
    except ManagedBlockError as exc:
        installed = False
        error = str(exc)
    return {
        "status": "PASS" if installed else "FAIL",
        "command": "check",
        "target": str(target),
        "installed": installed,
        "error": error,
    }


def uninstall(codex_home: Path) -> dict[str, object]:
    """Remove our block from both candidates because precedence can change over time."""
    candidates = [codex_home / "AGENTS.override.md", codex_home / "AGENTS.md"]
    planned: list[tuple[Path, str, tuple[int, int]]] = []

    # Validate every candidate first so malformed state cannot cause a partial uninstall.
    for target in candidates:
        if not target.exists():
            continue
        existing = read_text_exact(target)
        region = managed_region(existing)
        if region is not None:
            planned.append((target, existing, region))

    changed_targets: list[str] = []
    backups: list[str] = []
    for target, existing, (start, end) in planned:
        backup = backup_existing(codex_home, target, existing)
        if backup is not None:
            backups.append(str(backup))
        remaining = existing[:start] + existing[end:]
        if remaining.strip():
            atomic_write(target, remaining)
        else:
            target.unlink()
        changed_targets.append(str(target))

    return {
        "status": "PASS",
        "command": "uninstall",
        "changed": bool(changed_targets),
        "targets": changed_targets,
        "backups": backups,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install", "check", "uninstall"))
    parser.add_argument("--codex-home")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    codex_home = resolve_codex_home(args.codex_home)
    try:
        if args.command == "install":
            result = install(codex_home)
        elif args.command == "uninstall":
            result = uninstall(codex_home)
        else:
            result = check(codex_home)
    except (ManagedBlockError, OSError, UnicodeError) as exc:
        try:
            target = str(active_agents_file(codex_home))
        except (OSError, UnicodeError):
            target = str(codex_home)
        result = {
            "status": "FAIL",
            "command": args.command,
            "target": target,
            "error": str(exc),
        }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
