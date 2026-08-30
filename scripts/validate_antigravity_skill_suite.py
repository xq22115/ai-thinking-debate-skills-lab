#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
INV = ROOT / ".agents" / "antigravity-skill-suite" / "source-inventory.json"
EXPECTED = {
    "agent-reliability-research", "authorized-reverse-engineering", "autonomy-contract",
    "capability-forensics", "capability-router", "compatibility-audit", "competing-hypotheses",
    "consensus-research", "convergence-engine", "cross-runtime-bridge", "deep-engineering",
    "engineering-benchmark", "evidence-gate", "github-operations", "goal-orchestrator",
    "legal-research-writing", "mature-content-fidelity", "mcp-surface-engineering", "memory-state",
    "multi-agent-deliberation", "plan-arbiter", "provider-capability-routing", "research-intelligence",
    "root-cause", "runtime-forensics", "runtime-health-routing", "runtime-scale-engineering",
    "source-router", "tool-acquisition-resilience", "web-session-recovery", "work-ledger",
    "workspace-execution", "writer-cognitive-os"
}
REQUIRED_HEADINGS = [
    "## Purpose", "## Activate when", "## Do not activate",
    "## Antigravity-native execution", "## Workflow", "## Validation", "## Boundaries"
]
FORBIDDEN_HOST_TOKENS = [
    "api_tool", "personal_context", "automations.create", ".codex-plugin",
    "agent_action_executor", "python_user_visible", "ordinary_chat"
]

def frontmatter(text):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out

def main():
    errors = []
    dirs = {p.name for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}
    if dirs != EXPECTED:
        errors.append(f"canonical skill set mismatch: missing={sorted(EXPECTED-dirs)} extra={sorted(dirs-EXPECTED)}")

    seen = set()
    for name in sorted(EXPECTED):
        path = SKILLS / name / "SKILL.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm.get("name") != name:
            errors.append(f"{name}: frontmatter name mismatch: {fm.get('name')!r}")
        if not fm.get("description"):
            errors.append(f"{name}: missing description")
        if fm.get("name") in seen:
            errors.append(f"duplicate frontmatter name: {fm.get('name')}")
        seen.add(fm.get("name"))
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"{name}: missing heading {heading}")
        low = text.lower()
        for token in FORBIDDEN_HOST_TOKENS:
            if token.lower() in low:
                errors.append(f"{name}: leaked host-specific implementation token {token}")

    inv = json.loads(INV.read_text(encoding="utf-8"))
    if inv.get("source_skill_instances") != 66:
        errors.append("inventory source_skill_instances must be 66")
    if inv.get("canonical_antigravity_skills") != 33:
        errors.append("inventory canonical_antigravity_skills must be 33")
    mappings = [item for items in inv.get("repos", {}).values() for item in items]
    if len(mappings) != 66:
        errors.append(f"inventory mapping count must be 66, got {len(mappings)}")
    targets = {m.get("target") for m in mappings}
    if not targets <= EXPECTED:
        errors.append(f"inventory maps to unknown targets: {sorted(targets-EXPECTED)}")
    if targets != EXPECTED:
        errors.append(f"canonical targets without source mapping: {sorted(EXPECTED-targets)}")

    result = {
        "source_skill_instances": len(mappings),
        "canonical_skills": len(dirs & EXPECTED),
        "mapped_targets": len(targets),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL"
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
