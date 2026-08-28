#!/usr/bin/env python3
"""Install the continuous-quality contract into Codex user instructions."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


BEGIN_MARKER = "<!-- BEGIN AI-THINKING-DEBATE-SKILLS-LAB CONTINUOUS-QUALITY -->"
END_MARKER = "<!-- END AI-THINKING-DEBATE-SKILLS-LAB CONTINUOUS-QUALITY -->"

POLICY = """# Continuous Quality Contract

Optimize for first-pass correctness and complete task closure, not artificial delay, token count, source count, or ceremony.

For non-trivial work:
- reconstruct the real current state, dependencies, protected capabilities, constraints, and observable acceptance criteria before editing;
- treat the first plausible answer as a hypothesis until evidence verifies it;
- prefer root-cause and high-information-gain investigation over symptom patching;
- when current, version-sensitive, unfamiliar, ambiguous, or repeatedly failing, use current primary documentation plus high-signal maintainer/practitioner evidence when it can change the decision;
- compare causally distinct routes instead of renaming the same approach;
- after two materially similar failures, change the hypothesis, mechanism, diagnostic instrument, evidence family, environment, or verification method before trying again;
- preserve working behavior unless the task explicitly changes it;
- verify at the highest practical layer: runtime/user path > integration/functional > read-back > unit/static > configuration inspection;
- a file write, command exit, CI status, PR creation, or agent self-report is not completion evidence by itself;
- challenge the proposed result with a contradiction, edge-case, or adversarial check when practical;
- continue foreseeable work until every hard acceptance criterion is satisfied or a concrete external dependency blocks further progress;
- do not make the user repeatedly request continuation for work that can be completed in the same task;
- keep final output concise and evidence-dense after the quality gates pass.

Never simulate deep thinking with sleep, slow streaming, artificial first-token delay, or fixed research quotas. Use the maximum useful reasoning, research, testing, and independent evaluation justified by uncertainty and impact.
"""


def managed_block() -> str:
    return f"{BEGIN_MARKER}\n{POLICY.strip()}\n{END_MARKER}"


def resolve_codex_home(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    if os.environ.get("CODEX_HOME"):
        return Path(os.environ["CODEX_HOME"]).expanduser()
    return Path.home() / ".codex"


def active_agents_file(codex_home: Path) -> Path:
    override = codex_home / "AGENTS.override.md"
    if override.is_file() and override.read_text(encoding="utf-8").strip():
        return override
    return codex_home / "AGENTS.md"


def install(codex_home: Path) -> dict[str, object]:
    codex_home.mkdir(parents=True, exist_ok=True)
    target = active_agents_file(codex_home)
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    block = managed_block()
    if block in existing:
        changed = False
    else:
        prefix = existing.rstrip()
        content = f"{prefix}\n\n{block}\n" if prefix else f"{block}\n"
        target.write_text(content, encoding="utf-8")
        changed = True
    return {"status": "PASS", "command": "install", "target": str(target), "changed": changed}


def check(codex_home: Path) -> dict[str, object]:
    target = active_agents_file(codex_home)
    content = target.read_text(encoding="utf-8") if target.exists() else ""
    ok = managed_block() in content
    return {"status": "PASS" if ok else "FAIL", "command": "check", "target": str(target), "installed": ok}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install", "check"))
    parser.add_argument("--codex-home")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    codex_home = resolve_codex_home(args.codex_home)
    result = install(codex_home) if args.command == "install" else check(codex_home)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
