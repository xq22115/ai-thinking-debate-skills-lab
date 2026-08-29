#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
EXPECTED = [
    "chief-of-staff-core", "plan-arbiter", "evidence-watchdog", "executive-research",
    "memory-policy", "convergence-controller", "autonomy-contract", "persistent-work-ledger"
]
EXPLICIT = {"autonomy-contract", "persistent-work-ledger"}
DEPTH_LEVELS = ["SURFACE", "MECHANISM", "CODE_PATH", "DETERMINISTIC_REPRO", "COUNTEREXAMPLE", "FIX_STATUS", "REGRESSION", "GENERALIZATION"]


def fail(errors, message):
    errors.append(message)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
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
    plugin = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
    settings = json.loads((ROOT / "settings.json").read_text())
    marketplace = json.loads((REPO / ".agents" / "plugins" / "marketplace.json").read_text())

    if plugin.get("name") != "ai-efficiency-operating-system": fail(errors, "wrong plugin name")
    if plugin.get("skills") != "./skills/": fail(errors, "plugin skills path must be ./skills/")
    if settings.get("default_implicit_skills", []) + settings.get("explicit_only_skills", []) != EXPECTED:
        fail(errors, "settings skill inventory/order drift")
    names = [p.get("name") for p in marketplace.get("plugins", [])]
    if names.count("ai-efficiency-operating-system") != 1: fail(errors, "marketplace canonical plugin count != 1")

    for name in EXPECTED:
        path = ROOT / "skills" / name / "SKILL.md"
        if not path.exists():
            fail(errors, f"missing {path.relative_to(REPO)}")
            continue
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        if meta.get("name") != name: fail(errors, f"frontmatter name mismatch: {name}")
        desc = meta.get("description", "")
        if not desc.startswith("Use when"): fail(errors, f"description must start with 'Use when': {name}")
        if len(desc) > 1024: fail(errors, f"description too long: {name}")
        if len(text.splitlines()) > 500: fail(errors, f"SKILL.md over 500 lines: {name}")
        if name in EXPLICIT:
            agent = ROOT / "skills" / name / "agents" / "openai.yaml"
            if not agent.exists() or "allow_implicit_invocation: false" not in agent.read_text():
                fail(errors, f"explicit-only policy missing: {name}")

    adaptive = settings["research_profiles"]["ADAPTIVE"]
    strict = settings["research_profiles"]["STRICT_DEEPLOCK"]
    if adaptive.get("fixed_elapsed_time_is_depth") is not False: fail(errors, "adaptive time-depth invariant broken")
    if adaptive.get("fixed_source_count_is_quality") is not False: fail(errors, "adaptive source-count invariant broken")
    if strict.get("explicit_only") is not True: fail(errors, "strict profile must be explicit-only")
    if strict.get("if_required_telemetry_is_missing") != "PROCESS_COMPLETE_MAX": fail(errors, "strict telemetry fallback drift")

    depth_ref = ROOT / "skills" / "executive-research" / "references" / "deep-task-integrity.md"
    depth_text = depth_ref.read_text(encoding="utf-8") if depth_ref.exists() else ""
    positions = [depth_text.find(f"`{name}`") for name in DEPTH_LEVELS]
    if any(p < 0 for p in positions): fail(errors, "progressive depth ladder is incomplete")
    if positions != sorted(positions): fail(errors, "progressive depth ladder order drift")
    if "Do not force every task to level 7" not in depth_text: fail(errors, "adaptive depth stop guard missing")

    legacy_skill = REPO / "skills" / "skills" / "ai-efficiency-operating-system" / "SKILL.md"
    if legacy_skill.exists(): fail(errors, "legacy mega SKILL.md is still active")

    for rel in ["evals/routing-cases.jsonl", "evals/behavior-cases.jsonl", "references/2026-baseline.md", "MIGRATION.md"]:
        if not (ROOT / rel).exists(): fail(errors, f"missing {rel}")

    for fn in [ROOT / "evals" / "routing-cases.jsonl", ROOT / "evals" / "behavior-cases.jsonl"]:
        ids = []
        for line in fn.read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            obj = json.loads(line)
            ids.append(obj["id"])
        if len(ids) != len(set(ids)): fail(errors, f"duplicate IDs in {fn.name}")

    if errors:
        print("PLUGIN VALIDATION FAILED")
        for e in errors: print("-", e)
        return 1
    print("PLUGIN VALIDATION PASS")
    print(f"skills={len(EXPECTED)} implicit={len(settings['default_implicit_skills'])} explicit={len(settings['explicit_only_skills'])} depth_levels={len(DEPTH_LEVELS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
