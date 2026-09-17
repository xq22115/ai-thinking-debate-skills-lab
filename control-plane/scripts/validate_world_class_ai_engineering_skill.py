#!/usr/bin/env python3
"""Fail-closed structural gate for the world-class AI engineering skill pack."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "skills" / "skills" / "world-class-ai-engineering"
SKILL = SKILL_DIR / "SKILL.md"
CAPABILITY_MAP = SKILL_DIR / "references" / "capability-map.md"
PLAYBOOK = SKILL_DIR / "references" / "engineering-playbook.md"
SOURCE_NOTES = SKILL_DIR / "references" / "2026-source-notes.md"
EVALS = ROOT / "skills" / "evals" / "world-class-ai-engineering-pressure-cases.jsonl"

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


for path in [SKILL, CAPABILITY_MAP, PLAYBOOK, SOURCE_NOTES, EVALS]:
    require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

if not errors:
    skill_text = SKILL.read_text(encoding="utf-8")
    cap_text = CAPABILITY_MAP.read_text(encoding="utf-8")
    playbook_text = PLAYBOOK.read_text(encoding="utf-8")
    source_text = SOURCE_NOTES.read_text(encoding="utf-8")

    frontmatter = re.match(r"^---\n(.*?)\n---\n", skill_text, re.S)
    require(frontmatter is not None, "SKILL.md must start with YAML frontmatter")
    if frontmatter:
        fm = frontmatter.group(1)
        require("name: world-class-ai-engineering" in fm, "wrong skill name")
        description = next((line.split(":", 1)[1].strip() for line in fm.splitlines() if line.startswith("description:")), "")
        require(description.startswith("Use when "), "description must be trigger-only and start with 'Use when '")
        require(len(description) <= 500, "description should stay compact for discovery")

    for phrase in [
        "FILE_EXISTS != REGISTERED != LOADED != EXECUTED != EFFECTIVE != VERIFIED",
        "CI_GREEN != USER_PATH_VERIFIED",
        "FAST != CORRECT",
        "MORE_AGENTS != MORE_INDEPENDENT_EVIDENCE",
        "ai-efficiency-operating-system",
        "task-goal-intelligence",
    ]:
        require(phrase in skill_text, f"SKILL.md missing invariant/delegation marker: {phrase}")

    for phrase in [
        "Tool / MCP contract engineering",
        "Memory / context integrity",
        "Durable execution and recovery",
        "Observability and runtime forensics",
        "Evaluation-driven engineering",
        "Computer Use / desktop agent engineering",
        "Performance and cost engineering without degradation",
        "Security and capability boundaries",
        "Multi-agent evidence quality",
    ]:
        require(phrase in cap_text, f"capability map missing domain: {phrase}")

    for phrase in [
        "Phase 2 — Evidence and baseline",
        "Phase 4 — Design for failure",
        "Phase 5 — Tool and MCP preflight",
        "Phase 7 — Observability",
        "Phase 8 — Evaluation",
        "Phase 9 — Desktop / Computer Use discipline",
        "Phase 10 — Performance engineering",
        "Phase 12 — Release gate",
    ]:
        require(phrase in playbook_text, f"engineering playbook missing phase: {phrase}")

    for url in [
        "https://blog.modelcontextprotocol.io/posts/2026-07-28/",
        "https://openai.github.io/openai-agents-python/tracing/",
        "https://opentelemetry.io/blog/2026/genai-observability/",
        "https://docs.langchain.com/oss/javascript/langgraph/thinking-in-langgraph",
        "https://docs.temporal.io/",
        "https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html",
        "https://agentskills.io/specification",
    ]:
        require(url in source_text, f"source notes missing upstream reference: {url}")

    cases = []
    for line_no, line in enumerate(EVALS.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"eval JSONL line {line_no} invalid: {exc}")
            continue
        for key in ["id", "scenario", "failure", "required_behavior", "forbidden_shortcut", "evidence"]:
            require(bool(case.get(key)), f"eval {line_no} missing {key}")
        cases.append(case)

    ids = [case.get("id") for case in cases]
    require(len(cases) >= 18, f"expected at least 18 pressure cases, found {len(cases)}")
    require(len(ids) == len(set(ids)), "pressure-case ids must be unique")

    required_case_ids = {f"WCAE-{i:02d}" for i in range(1, 19)}
    require(required_case_ids.issubset(set(ids)), "pressure corpus is missing required WCAE-01..WCAE-18 cases")

    corpus = "\n".join(json.dumps(case, sort_keys=True) for case in cases)
    for marker in [
        "CONFIGURED",
        "GitHub",
        "timeout",
        "interrupted",
        "desktop",
        "latency",
        "MCP",
        "guardrail",
        "memory",
        "skill",
        "agents",
        "eval",
    ]:
        require(marker.lower() in corpus.lower(), f"pressure corpus missing failure family: {marker}")

if errors:
    print("WORLD_CLASS_AI_ENGINEERING_GATE=FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("WORLD_CLASS_AI_ENGINEERING_GATE=PASS")
print("pressure_cases>=18")
print("frontmatter=valid")
print("references=present")
print("current_2026_sources=registered")
