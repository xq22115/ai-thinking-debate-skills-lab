#!/usr/bin/env python3
"""Validate the structural contract of a SKILL.md package using stdlib only."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_PATTERNS = (
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["missing YAML frontmatter opening delimiter"]

    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, ["missing YAML frontmatter closing delimiter"]

    block = text[4:end]
    data: dict[str, str] = {}
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"unsupported frontmatter line: {raw}")
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, errors


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"missing {skill_file}"]

    text = skill_file.read_text(encoding="utf-8")
    data, fm_errors = parse_frontmatter(text)
    errors.extend(fm_errors)

    name = data.get("name", "")
    description = data.get("description", "")

    if not name:
        errors.append("frontmatter.name is required")
    elif not NAME_RE.fullmatch(name):
        errors.append("frontmatter.name must be lowercase kebab-case")
    elif name != skill_dir.name:
        errors.append(
            f"frontmatter.name {name!r} does not match directory {skill_dir.name!r}"
        )

    if not description:
        errors.append("frontmatter.description is required")
    elif len(description) > 1024:
        errors.append("frontmatter.description exceeds 1024 characters")

    line_count = len(text.splitlines())
    if line_count > 500:
        errors.append(f"SKILL.md is too large ({line_count} lines > 500); use references/")

    if "## Trigger" not in text and "# Trigger" not in text:
        errors.append("missing explicit Trigger section")

    if "verification" not in text.lower():
        errors.append("skill does not describe verification")

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"possible secret matching {pattern.pattern!r} found in SKILL.md")

    for folder in ("references", "scripts", "tests", "evals", "assets"):
        path = skill_dir / folder
        if path.exists() and not path.is_dir():
            errors.append(f"{path} exists but is not a directory")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()

    errors = validate(args.skill_dir)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {args.skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
