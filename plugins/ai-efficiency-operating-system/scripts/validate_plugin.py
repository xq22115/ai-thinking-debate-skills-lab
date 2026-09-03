#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]

DEFAULT_IMPLICIT = [
    "task-goal-intelligence",
    "chief-of-staff-core",
    "plan-arbiter",
    "evidence-watchdog",
    "executive-research",
    "memory-policy",
    "convergence-controller",
]
CONDITIONAL_IMPLICIT = [
    "capability-forensics",
    "mcp-surface-engineering",
    "agent-runtime-forensics",
]
EXPLICIT_ONLY = [
    "autonomy-contract",
    "persistent-work-ledger",
    "authorized-reverse-engineering",
]
EXPERT = [
    "capability-forensics",
    "mcp-surface-engineering",
    "authorized-reverse-engineering",
    "agent-runtime-forensics",
]
EXPECTED = DEFAULT_IMPLICIT + CONDITIONAL_IMPLICIT + EXPLICIT_ONLY
DEPTH_LEVELS = ["SURFACE", "MECHANISM", "CODE_PATH", "DETERMINISTIC_REPRO", "COUNTEREXAMPLE", "FIX_STATUS", "REGRESSION", "GENERALIZATION"]
EXPERT_REFS = {
    "capability-forensics": ("references/capability-fingerprinting.md", ["DECLARED / VISIBLE / AUTHORIZED / LOADABLE / INVOKABLE / EFFECTIVE / VERIFIED", "Environment engineering before prompt inflation", "Differential probe"]),
    "mcp-surface-engineering": ("references/mcp-surface-contract.md", ["Dynamic discovery", "Tool-poisoning", "Minimal Capability Frontier", "pre-execution boundary"]),
    "authorized-reverse-engineering": ("references/reverse-engineering-playbook.md", ["Static-first", "Cross-binary transfer", "Hard stop conditions"]),
    "agent-runtime-forensics": ("references/runtime-provenance.md", ["Evidence planes", "Causal edges", "Replay"]),
}
EXTRA_REFS = {
    "skills/capability-forensics/references/capability-boundary-recon.md": [
        "PLAN/ROLLOUT", "WORKSPACE POLICY", "PLUGIN INSTALL", "SESSION REGISTRATION", "Desktop-only", "MODEL_OR_REASONING_LIMIT"
    ],
    "skills/executive-research/references/ai-ecosystem-recon.md": [
        "change archaeology", "Harness differential", "Citation-chain audit", "Retrieved-content injection firewall"
    ],
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
    if settings.get("schema") != 4: fail(errors, "settings schema must be 4")
    if settings.get("default_implicit_skills") != DEFAULT_IMPLICIT: fail(errors, "default implicit skill inventory/order drift")
    if settings.get("conditional_implicit_skills") != CONDITIONAL_IMPLICIT: fail(errors, "conditional implicit skill inventory/order drift")
    if settings.get("explicit_only_skills") != EXPLICIT_ONLY: fail(errors, "explicit-only skill inventory/order drift")
    if set(DEFAULT_IMPLICIT + CONDITIONAL_IMPLICIT + EXPLICIT_ONLY) != set(EXPECTED): fail(errors, "skill inventory classification drift")

    names = [p.get("name") for p in marketplace.get("plugins", [])]
    if names.count("ai-efficiency-operating-system") != 1: fail(errors, "marketplace canonical plugin count != 1")

    routing = settings.get("routing", {})
    if routing.get("router_version") != 2: fail(errors, "router_version must be 2")
    if routing.get("goal_gate_skill") != "task-goal-intelligence": fail(errors, "task-goal-intelligence must own the goal gate")
    if routing.get("max_implicit_skills") != 3: fail(errors, "implicit composition must be bounded to three skills")
    if routing.get("deterministic_baseline_required") is not True: fail(errors, "deterministic routing baseline is required")
    if routing.get("semantic_rerank_optional_after_eligibility_filter") is not True: fail(errors, "semantic rerank must stay behind eligibility filter")
    if routing.get("route_bundle_enabled") is not True: fail(errors, "route bundles must be enabled")
    for name in CONDITIONAL_IMPLICIT:
        if name not in (routing.get("conditional_specialists") or {}):
            fail(errors, f"missing conditional specialist contract: {name}")

    composition = settings.get("composition") or {}
    required_compositions = {
        "complex_research",
        "capability_bottleneck",
        "many_tool_or_mcp_surface",
        "runtime_effect_mismatch",
        "architecture_choice",
        "repeated_failure",
        "cross_session_context",
        "complex_multi_stage",
    }
    if not required_compositions.issubset(set(composition)):
        fail(errors, "composition contract missing required route bundle")
    for key, bundle in composition.items():
        if not isinstance(bundle, list) or not bundle or len(bundle) > 3:
            fail(errors, f"invalid bounded composition: {key}")
        elif bundle[0] != "task-goal-intelligence":
            fail(errors, f"composition must start from task-goal-intelligence: {key}")

    fallback_rules = settings.get("fallback_rules") or {}
    for key in (
        "route_failure_does_not_change_root_goal",
        "after_repeated_failure_choose_materially_different_route",
        "unavailable_specialist_must_fall_back_to_goal_advancing_base_skill",
        "host_capability_mismatch_must_be_reported_not_fabricated",
        "completion_requires_postcondition_evidence",
    ):
        if fallback_rules.get(key) is not True:
            fail(errors, f"fallback invariant missing: {key}")
    if int(fallback_rules.get("retry_same_route_without_new_evidence_limit", -1)) > 1:
        fail(errors, "same-route retry limit must be <= 1 without new evidence")

    labs = settings.get("expert_labs", {})
    if labs.get("activation") != "conditional-demand-loaded": fail(errors, "expert labs activation must be conditional-demand-loaded")
    if labs.get("default_enabled") is not False: fail(errors, "expert labs must not be globally default-enabled")
    if labs.get("implicit_eligible") != CONDITIONAL_IMPLICIT: fail(errors, "expert lab implicit-eligible inventory drift")
    if labs.get("explicit_only") != ["authorized-reverse-engineering"]: fail(errors, "authorized reverse engineering must remain expert explicit-only")
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

        agent = ROOT / "skills" / name / "agents" / "openai.yaml"
        if not agent.exists():
            fail(errors, f"missing OpenAI skill policy: {name}")
            continue
        agent_text = agent.read_text(encoding="utf-8")
        if name in DEFAULT_IMPLICIT or name in CONDITIONAL_IMPLICIT:
            if "allow_implicit_invocation: true" not in agent_text:
                fail(errors, f"implicit invocation policy missing: {name}")
        elif name in EXPLICIT_ONLY:
            if "allow_implicit_invocation: false" not in agent_text:
                fail(errors, f"explicit-only policy missing: {name}")

    task_goal = (ROOT / "skills" / "task-goal-intelligence" / "SKILL.md").read_text(encoding="utf-8")
    for marker in ["Interpretation", "Semantic delta", "Active routing handoffs", "Fallback/self-repair", "at most three implicit skills"]:
        if marker.lower() not in task_goal.lower(): fail(errors, f"task-goal routing marker missing: {marker}")

    for name, (rel, markers) in EXPERT_REFS.items():
        path = ROOT / "skills" / name / rel
        if not path.exists():
            fail(errors, f"missing expert reference: {name}/{rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker.lower() not in text.lower():
                fail(errors, f"expert reference marker missing: {name}: {marker}")

    for rel, markers in EXTRA_REFS.items():
        path = ROOT / rel
        if not path.exists():
            fail(errors, f"missing reference: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker.lower() not in text.lower():
                fail(errors, f"reference marker missing: {rel}: {marker}")

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
        "evals/routing-cases.jsonl",
        "evals/composition-cases.jsonl",
        "evals/behavior-cases.jsonl",
        "evals/expert-labs-cases.jsonl",
        "scripts/route_oracle.py",
        "scripts/composition_oracle.py",
        "scripts/expert_labs_oracle.py",
        "references/2026-baseline.md",
        "MIGRATION.md",
    ]
    for rel in required:
        if not (ROOT / rel).exists(): fail(errors, f"missing {rel}")

    minimums = {
        "routing-cases.jsonl": 55,
        "composition-cases.jsonl": 15,
        "behavior-cases.jsonl": 55,
        "expert-labs-cases.jsonl": 25,
    }
    for name, minimum in minimums.items():
        path = ROOT / "evals" / name
        if not path.exists():
            continue
        rows, ids = load_jsonl(path)
        if len(ids) != len(set(ids)): fail(errors, f"duplicate IDs in {name}")
        if len(rows) < minimum: fail(errors, f"insufficient {name}: {len(rows)} < {minimum}")

    route_oracle = (ROOT / "scripts" / "route_oracle.py").read_text(encoding="utf-8")
    for marker in ["CONDITIONAL_IMPLICIT", "route_bundle", "fallback_chain", "deterministic baseline", "_is_explanation_only"]:
        if marker.lower() not in route_oracle.lower(): fail(errors, f"routing oracle marker missing: {marker}")

    composition_oracle = (ROOT / "scripts" / "composition_oracle.py").read_text(encoding="utf-8")
    for marker in ["route_bundle", "fallback_chain", "expected_bundle"]:
        if marker not in composition_oracle: fail(errors, f"composition oracle marker missing: {marker}")

    if errors:
        print("PLUGIN VALIDATION FAILED")
        for e in errors:
            print("-", e)
        return 1
    print("PLUGIN VALIDATION PASS")
    print(
        f"skills={len(EXPECTED)} default_implicit={len(DEFAULT_IMPLICIT)} "
        f"conditional_implicit={len(CONDITIONAL_IMPLICIT)} explicit={len(EXPLICIT_ONLY)} "
        f"expert={len(EXPERT)} depth_levels={len(DEPTH_LEVELS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
