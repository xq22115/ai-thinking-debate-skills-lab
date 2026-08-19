#!/usr/bin/env python3
"""Deterministic static validator for Evidence-Gated Deliberation & Skills OS RC1.

This validates package structure and truth-boundary invariants. It does NOT claim
model/runtime/host-live verification.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SKILLS = {
    "evidence-gap-research",
    "competing-hypotheses",
    "root-cause-clustering",
    "completion-gate",
    "recoverable-state",
    "compatibility-audit",
    "multi-agent-deliberation",
    "capability-challenge",
    "durable-agent-control-plane",
}

REQUIRED_FILES = [
    "README.md",
    "STATUS.md",
    "00-cross-chat-research-map.md",
    "01-30-role-deliberation.md",
    "02-skills-catalog.md",
    "03-2026-current-evidence.md",
    "04-reference-architecture.md",
    "05-source-ledger.json",
    "06-evaluation-suite.md",
    "07-deliberation-router-spec.md",
    "08-portability-matrix.md",
    "09-research-backlog.md",
    "10-ci-diagnosis.md",
    "11-cross-chat-convergence.md",
    "12-upstream-source-lock.json",
    "15-machine-readable-governance.md",
    "16-governance-autonomy-convergence.md",
    "evals/rc1-fixtures.json",
    "evals/control-plane-fixtures.json",
    "data/role_activation_policy.yaml",
    "data/claim_obligation_graph.json",
]

FORBIDDEN_UNQUALIFIED = [
    re.compile(r"(?im)^\s*(status|current status)\s*:\s*(stable|deployed|healthy|host[_ -]?live[_ -]?verified)\s*$"),
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    try:
        _, fm, _ = text.split("---", 2)
    except ValueError:
        return {}
    out: dict[str, str] = {}
    for raw in fm.strip().splitlines():
        if ":" not in raw:
            continue
        k, v = raw.split(":", 1)
        out[k.strip()] = v.strip().strip('"\'')
    return out


def check_json(path: Path) -> tuple[bool, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"invalid JSON: {exc}"
    return True, f"json_type={type(data).__name__}"


def main() -> int:
    checks: list[dict[str, object]] = []

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "ok": ok, "detail": detail})

    for rel in REQUIRED_FILES:
        p = ROOT / rel
        record(f"required_file:{rel}", p.is_file() and p.stat().st_size > 0, "present" if p.is_file() else "missing")

    skills_dir = ROOT / "skills"
    found = {p.parent.name for p in skills_dir.glob("*/SKILL.md")}
    record("skills:set", found == REQUIRED_SKILLS, f"found={sorted(found)}")

    for name in sorted(REQUIRED_SKILLS):
        p = skills_dir / name / "SKILL.md"
        if not p.is_file():
            record(f"skill:{name}", False, "SKILL.md missing")
            continue
        text = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        ok = fm.get("name") == name and bool(fm.get("description"))
        record(f"skill:{name}", ok, f"frontmatter_name={fm.get('name')!r} description={'yes' if fm.get('description') else 'no'}")

    for rel in [
        "05-source-ledger.json",
        "12-upstream-source-lock.json",
        "evals/rc1-fixtures.json",
        "evals/control-plane-fixtures.json",
        "data/claim_obligation_graph.json",
    ]:
        p = ROOT / rel
        ok, detail = check_json(p) if p.is_file() else (False, "missing")
        record(f"json:{rel}", ok, detail)

    status = (ROOT / "STATUS.md").read_text(encoding="utf-8") if (ROOT / "STATUS.md").is_file() else ""
    for i, pattern in enumerate(FORBIDDEN_UNQUALIFIED, 1):
        m = pattern.search(status)
        record(f"truth_boundary:{i}", m is None, f"forbidden_match={m.group(0)!r}" if m else "no unqualified terminal status")

    convergence = (ROOT / "11-cross-chat-convergence.md").read_text(encoding="utf-8") if (ROOT / "11-cross-chat-convergence.md").is_file() else ""
    for token in ["PR #46", "PR #45", "PR #29", "BLOCKED_BY_BILLING_OR_SPENDING_LIMIT"]:
        record(f"convergence_token:{token}", token in convergence, "present" if token in convergence else "missing")

    policy = (ROOT / "data/role_activation_policy.yaml").read_text(encoding="utf-8") if (ROOT / "data/role_activation_policy.yaml").is_file() else ""
    for token in ["30", "escal", "de-escal"]:
        record(f"role_policy_token:{token}", token.lower() in policy.lower(), "present" if token.lower() in policy.lower() else "missing")

    failed = [c for c in checks if not c["ok"]]
    report = {
        "validator": "validate_rc1_package.py",
        "scope": "static-package-and-truth-boundary",
        "host_live_verified": False,
        "total_checks": len(checks),
        "failed_checks": len(failed),
        "status": "PASS_STATIC" if not failed else "FAIL_STATIC",
        "checks": checks,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
