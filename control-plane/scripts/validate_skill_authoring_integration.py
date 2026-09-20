#!/usr/bin/env python3
"""Fail-closed static integration validator for the skill-authoring capability."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED = {
    "canonical_skill": ROOT / "skills/skills/skill-authoring-engine/SKILL.md",
    "github_projection": ROOT / ".github/skills/skill-authoring-engine/SKILL.md",
    "github_agent": ROOT / ".github/agents/skill-architect.agent.md",
    "personal_agent": ROOT / "deploy/copilot-user/skill-architect.agent.md",
    "config": ROOT / "control-plane/ai-system/configs/skill-authoring-engine.json",
    "registry": ROOT / "control-plane/ai-system/registry.yml",
    "copilot_bootstrap": ROOT / ".github/copilot-instructions.md",
    "runtime_policy": ROOT / "plugins/ai-efficiency-operating-system/skills/superpowers-conversation-runtime/runtime-policy.json",
    "routing_fixtures": ROOT / "plugins/ai-efficiency-operating-system/evals/superpowers-conversation-routing-cases.jsonl",
    "installer": ROOT / "control-plane/scripts/install_copilot_user_skill_authoring.py",
}


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out: dict[str, str] = {}
    for raw in m.group(1).splitlines():
        if ":" not in raw:
            continue
        k, v = raw.split(":", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def main() -> int:
    errors: list[str] = []

    for label, path in REQUIRED.items():
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing_or_empty:{label}:{path}")

    if errors:
        for error in errors:
            print("FAIL", error)
        return 1

    cfg = json.loads(REQUIRED["config"].read_text(encoding="utf-8"))
    if cfg.get("id") != "skill-authoring-engine":
        errors.append("config_id_mismatch")
    if cfg.get("routing", {}).get("semantic_owner") != "skill_authoring":
        errors.append("semantic_owner_mismatch")
    if cfg.get("routing", {}).get("upstream_process_method") != "writing-skills":
        errors.append("writing_skills_method_missing")
    if cfg.get("multi_agent", {}).get("fixed_agent_count_forbidden") is not True:
        errors.append("adaptive_agent_count_invariant_missing")
    if cfg.get("personal_copilot_projection", {}).get("readback_hash_verification") is not True:
        errors.append("personal_readback_hash_gate_missing")

    for label in ("canonical_skill", "github_projection"):
        meta = frontmatter(REQUIRED[label].read_text(encoding="utf-8"))
        if meta.get("name") != "skill-authoring-engine":
            errors.append(f"{label}_name_mismatch")
        if not meta.get("description"):
            errors.append(f"{label}_description_missing")

    github_meta = frontmatter(REQUIRED["github_agent"].read_text(encoding="utf-8"))
    if not github_meta.get("description"):
        errors.append("github_agent_description_missing")
    if github_meta.get("target") != "github-copilot":
        errors.append("github_agent_target_mismatch")
    if github_meta.get("disable-model-invocation") != "false":
        errors.append("github_agent_auto_delegation_not_enabled")
    if github_meta.get("user-invocable") != "true":
        errors.append("github_agent_user_invocation_not_enabled")

    personal_meta = frontmatter(REQUIRED["personal_agent"].read_text(encoding="utf-8"))
    if not personal_meta.get("description"):
        errors.append("personal_agent_description_missing")
    if personal_meta.get("disable-model-invocation") != "false":
        errors.append("personal_agent_auto_delegation_not_enabled")
    if personal_meta.get("user-invocable") != "true":
        errors.append("personal_agent_user_invocation_not_enabled")

    policy = json.loads(REQUIRED["runtime_policy"].read_text(encoding="utf-8"))
    if policy.get("process_map", {}).get("skill_authoring") != "writing-skills":
        errors.append("runtime_process_method_drift")
    if policy.get("specialist_map", {}).get("skill_authoring") != "skill-authoring-engine":
        errors.append("runtime_specialist_drift")

    registry = REQUIRED["registry"].read_text(encoding="utf-8")
    for token in (
        "skill_authoring:",
        "../skills/skills/skill-authoring-engine/SKILL.md",
        "../.github/skills/skill-authoring-engine/SKILL.md",
        "../.github/agents/skill-architect.agent.md",
        "scripts/install_copilot_user_skill_authoring.py",
    ):
        if token not in registry:
            errors.append(f"registry_missing:{token}")

    bootstrap = REQUIRED["copilot_bootstrap"].read_text(encoding="utf-8")
    for token in (
        ".github/skills/skill-authoring-engine/SKILL.md",
        "skills/skills/skill-authoring-engine/SKILL.md",
        "Skill Architect",
    ):
        if token not in bootstrap:
            errors.append(f"copilot_bootstrap_missing:{token}")

    rows = [
        json.loads(line)
        for line in REQUIRED["routing_fixtures"].read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by_id = {row["id"]: row for row in rows}
    for case_id in ("SP06", "SP18", "SP19"):
        row = by_id.get(case_id)
        if not row:
            errors.append(f"routing_fixture_missing:{case_id}")
            continue
        if row.get("expected_upstream_process") != "writing-skills":
            errors.append(f"routing_method_mismatch:{case_id}")
        if "skill-authoring-engine" not in row.get("expected_bundle", []):
            errors.append(f"routing_specialist_missing:{case_id}")

    negative = by_id.get("SP20")
    if not negative or negative.get("expected") != "none":
        errors.append("hard_negative_skill_word_case_missing")

    if errors:
        print("SKILL AUTHORING INTEGRATION VALIDATION FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("SKILL AUTHORING INTEGRATION VALIDATION PASS")
    print(f"required_files={len(REQUIRED)} routing_cases={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
