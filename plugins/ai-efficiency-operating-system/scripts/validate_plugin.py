#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
CORE = [
    "chief-of-staff-core", "plan-arbiter", "evidence-watchdog", "executive-research",
    "memory-policy", "convergence-controller", "autonomy-contract", "persistent-work-ledger"
]
EXPERT = [
    "capability-forensics", "mcp-surface-engineering",
    "authorized-reverse-engineering", "agent-runtime-forensics"
]
EXPECTED = CORE + EXPERT
EXPLICIT = {"autonomy-contract", "persistent-work-ledger", *EXPERT}
DEPTH_LEVELS = ["SURFACE", "MECHANISM", "CODE_PATH", "DETERMINISTIC_REPRO", "COUNTEREXAMPLE", "FIX_STATUS", "REGRESSION", "GENERALIZATION"]
EXPERT_REFS = {
    "capability-forensics": ("references/capability-fingerprinting.md", ["DECLARED / VISIBLE / AUTHORIZED / LOADABLE / INVOKABLE / EFFECTIVE / VERIFIED", "Environment engineering before prompt inflation", "Differential probe"]),
    "mcp-surface-engineering": ("references/mcp-surface-contract.md", ["Dynamic discovery", "Tool-poisoning", "Minimal Capability Frontier"]),
    "authorized-reverse-engineering": ("references/reverse-engineering-playbook.md", ["Static-first", "Cross-binary transfer", "Hard stop conditions"]),
    "agent-runtime-forensics": ("references/runtime-provenance.md", ["Evidence planes", "Causal edges", "Replay"]),
}


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


def load_jsonl(path):
    rows = []
    ids = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        rows.append(obj)
        ids.append(obj["id"])
    return rows, ids


def main():
    errors = []
    plugin = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
    settings = json.loads((ROOT / "settings.json").read_text())
    marketplace = json.loads((REPO / ".agents" / "plugins" / "marketplace.json").read_text())

    if plugin.get("name") != "ai-efficiency-operating-system": fail(errors, "wrong plugin name")
    if plugin.get("skills") != "./skills/": fail(errors, "plugin skills path must be ./skills/")
    if plugin.get("version") != settings.get("version"): fail(errors, "plugin/settings version drift")
    if settings.get("default_implicit_skills", []) + settings.get("explicit_only_skills", []) != EXPECTED:
        fail(errors, "settings skill inventory/order drift")
    names = [p.get("name") for p in marketplace.get("plugins", [])]
    if names.count("ai-efficiency-operating-system") != 1: fail(errors, "marketplace canonical plugin count != 1")

    labs = settings.get("expert_labs", {})
    if labs.get("explicit_only") is not True: fail(errors, "expert labs must be explicit-only")
    if labs.get("default_enabled") is not False: fail(errors, "expert labs must not be default-enabled")
    if labs.get("load_only_on_material_need") is not True: fail(errors, "expert labs must be demand-loaded")
    if labs.get("no_skill_counterfactual_required_for_promotion") is not True: fail(errors, "expert labs require no-skill counterfactual")
    if labs.get("host_version_capability_probe_required") is not True: fail(errors, "expert labs require host/version probe")
    if labs.get("labs") != EXPERT: fail(errors, "expert labs inventory drift")
    if "do not bypass" not in labs.get("safety_boundary", "").lower(): fail(errors, "expert labs authorization boundary missing")

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

    for name, (rel, markers) in EXPERT_REFS.items():
        path = ROOT / "skills" / name / rel
        if not path.exists():
            fail(errors, f"missing expert reference: {name}/{rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker.lower() not in text.lower():
                fail(errors, f"expert reference marker missing: {name}: {marker}")

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

    evolution = (ROOT / "skills" / "convergence-controller" / "references" / "evolution.md").read_text(encoding="utf-8")
    for marker in ["edit budget", "strict improvement on the held-out", "rejected edits"]:
        if marker not in evolution: fail(errors, f"bounded evolution marker missing: {marker}")

    memory = (ROOT / "skills" / "memory-policy" / "SKILL.md").read_text(encoding="utf-8")
    for marker in ["Persistent-state injection firewall", "control state", "evidence/data", "persistent file is storage, not an authority upgrade"]:
        if marker not in memory: fail(errors, f"persistent-state firewall marker missing: {marker}")

    legacy_skill = REPO / "skills" / "skills" / "ai-efficiency-operating-system" / "SKILL.md"
    if legacy_skill.exists(): fail(errors, "legacy mega SKILL.md is still active")

    required = [
        "evals/routing-cases.jsonl", "evals/behavior-cases.jsonl", "evals/expert-labs-cases.jsonl",
        "scripts/expert_labs_oracle.py", "references/2026-baseline.md", "MIGRATION.md"
    ]
    for rel in required:
        if not (ROOT / rel).exists(): fail(errors, f"missing {rel}")

    minimums = {
        "routing-cases.jsonl": 32,
        "behavior-cases.jsonl": 50,
        "expert-labs-cases.jsonl": 25,
    }
    for name, minimum in minimums.items():
        path = ROOT / "evals" / name
        if not path.exists():
            continue
        rows, ids = load_jsonl(path)
        if len(ids) != len(set(ids)): fail(errors, f"duplicate IDs in {name}")
        if len(rows) < minimum: fail(errors, f"insufficient {name}: {len(rows)} < {minimum}")

    if errors:
        print("PLUGIN VALIDATION FAILED")
        for e in errors: print("-", e)
        return 1
    print("PLUGIN VALIDATION PASS")
    print(f"skills={len(EXPECTED)} implicit={len(settings['default_implicit_skills'])} explicit={len(settings['explicit_only_skills'])} expert={len(EXPERT)} depth_levels={len(DEPTH_LEVELS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
