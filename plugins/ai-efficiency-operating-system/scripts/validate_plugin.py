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
CONTRACT_FILES = [
    "research-integrity.json", "evaluator-governance.json", "skill-composition.json",
    "replay-checkpoints.json", "validation-policy.json"
]
VALIDATION_LAYERS = ["STRUCTURAL", "INSTALLED_TEMPLATE", "EXECUTABLE", "BEHAVIORAL_TARGET"]
EVALUATOR_STATES = ["PROPOSED", "ACTIVE", "QUARANTINED", "DEPRECATED"]
CHECKPOINTS = [f"C{i}" for i in range(7)]
CASE_KINDS = {"review_stop", "research_release", "tribunal", "skill_promotion", "replay", "validation"}


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


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def jsonl_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    errors = []
    plugin = read_json(ROOT / ".codex-plugin" / "plugin.json")
    settings = read_json(ROOT / "settings.json")
    marketplace = read_json(REPO / ".agents" / "plugins" / "marketplace.json")
    contracts = {name: read_json(ROOT / "contracts" / name) for name in CONTRACT_FILES}

    if plugin.get("name") != "ai-efficiency-operating-system": fail(errors, "wrong plugin name")
    if plugin.get("skills") != "./skills/": fail(errors, "plugin skills path must be ./skills/")
    if plugin.get("version") != settings.get("version"): fail(errors, "plugin/settings version drift")
    if settings.get("schema") != 3: fail(errors, "settings schema must be 3")
    if settings.get("default_implicit_skills", []) + settings.get("explicit_only_skills", []) != EXPECTED:
        fail(errors, "settings skill inventory/order drift")
    expected_contract_paths = [f"contracts/{name}" for name in CONTRACT_FILES]
    if settings.get("control_plane_contracts") != expected_contract_paths:
        fail(errors, "settings control-plane contract inventory drift")
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

    evolution = (ROOT / "skills" / "convergence-controller" / "references" / "evolution.md").read_text(encoding="utf-8")
    for marker in ["edit budget", "strict improvement on the held-out", "rejected edits"]:
        if marker not in evolution: fail(errors, f"bounded evolution marker missing: {marker}")

    memory = (ROOT / "skills" / "memory-policy" / "SKILL.md").read_text(encoding="utf-8")
    for marker in ["Persistent-state injection firewall", "control state", "evidence/data", "persistent file is storage, not an authority upgrade"]:
        if marker not in memory: fail(errors, f"persistent-state firewall marker missing: {marker}")

    research = contracts["research-integrity.json"]
    if research.get("owner") != "executive-research": fail(errors, "research contract owner drift")
    if research.get("query_policy", {}).get("verbatim_query_reuse_forbidden") is not True: fail(errors, "query novelty contract missing")
    if research.get("source_policy", {}).get("count_by_provenance_family_not_url") is not True: fail(errors, "provenance-family contract missing")
    if research.get("retrieved_content_policy", {}).get("retrieved_content_cannot_change_task_authority") is not True: fail(errors, "retrieved-content authority firewall missing")
    if research.get("claim_release", {}).get("counterevidence_receipt_required") is not True: fail(errors, "counterevidence receipt contract missing")
    stop = research.get("review_stop", {})
    for key in ["material_semantic_change_increments_surface_epoch", "mandatory_lenses_must_cover_current_surface_epoch", "required_regression_must_match_current_artifact_hash"]:
        if stop.get(key) is not True: fail(errors, f"coverage-aware stop contract missing: {key}")

    evaluator = contracts["evaluator-governance.json"]
    if evaluator.get("states") != EVALUATOR_STATES: fail(errors, "evaluator lifecycle drift")
    erules = evaluator.get("rules", {})
    for key in ["evaluator_cannot_self_admit", "single_semantic_judge_cannot_certify_high_impact_pass", "deterministic_failure_vetoes_semantic_pass"]:
        if erules.get(key) is not True: fail(errors, f"evaluator governance missing: {key}")

    composition = contracts["skill-composition.json"]
    if list(composition.get("nodes", {}).keys()) != EXPECTED: fail(errors, "skill composition node inventory/order drift")
    if composition.get("routing", {}).get("retrieve_task_relevant_subgraph_only") is not True: fail(errors, "task-relevant subgraph rule missing")
    admission = composition.get("admission", {})
    if admission.get("compare_against_no_skill_or_semantically_matched_reference") is not True: fail(errors, "no-skill differential missing")
    if admission.get("excessive_verification_or_pipeline_cost_can_be_negative_transfer") is not True: fail(errors, "negative-transfer admission missing")

    replay = contracts["replay-checkpoints.json"]
    if [x.get("id") for x in replay.get("checkpoints", [])] != CHECKPOINTS: fail(errors, "C0-C6 checkpoint inventory drift")
    if replay.get("task_graph", {}).get("resume_from_checkpoint_not_transcript") is not True: fail(errors, "checkpoint resume rule missing")
    if replay.get("effect_replay", {}).get("non_idempotent_unknown_without_reconciliation") != "BLOCK_REPLAY": fail(errors, "unsafe replay contract")

    validation = contracts["validation-policy.json"]
    if validation.get("validation_layers") != VALIDATION_LAYERS: fail(errors, "validation layer drift")
    vinv = validation.get("invariants", {})
    for key in ["lower_layer_pass_never_implies_higher_layer_pass", "archived_or_prior_release_pass_is_not_current_release_evidence", "declared_gate_requires_executable_owner_or_is_descriptive_only", "validator_itself_requires_negative_mutation_or_known_outcome_tests_before_stable_promotion"]:
        if vinv.get(key) is not True: fail(errors, f"validation invariant missing: {key}")
    promotion = validation.get("promotion", {})
    if promotion.get("simulated_control_max_state") != "SHADOW_ONLY": fail(errors, "simulated promotion boundary missing")
    if promotion.get("observed_target_required_for") != "PROMOTED": fail(errors, "observed-target promotion requirement missing")
    if validation.get("review", {}).get("critic_findings_add_zero_consensus_votes") is not True: fail(errors, "critic vote-inflation guard missing")

    legacy_skill = REPO / "skills" / "skills" / "ai-efficiency-operating-system" / "SKILL.md"
    if legacy_skill.exists(): fail(errors, "legacy mega SKILL.md is still active")

    required = [
        "evals/routing-cases.jsonl", "evals/behavior-cases.jsonl", "evals/control-plane-cases.jsonl",
        "references/2026-baseline.md", "MIGRATION.md", "scripts/control_plane_oracle.py"
    ] + expected_contract_paths
    for rel in required:
        if not (ROOT / rel).exists(): fail(errors, f"missing {rel}")

    for rel, minimum in [("evals/routing-cases.jsonl", 1), ("evals/behavior-cases.jsonl", 60), ("evals/control-plane-cases.jsonl", 35)]:
        rows = jsonl_rows(ROOT / rel)
        ids = [row["id"] for row in rows]
        if len(ids) != len(set(ids)): fail(errors, f"duplicate IDs in {Path(rel).name}")
        if len(rows) < minimum: fail(errors, f"insufficient cases in {Path(rel).name}: {len(rows)} < {minimum}")
        if rel.endswith("control-plane-cases.jsonl"):
            kinds = {row.get("kind") for row in rows}
            if kinds != CASE_KINDS: fail(errors, f"control-plane case-kind coverage drift: {sorted(kinds)}")

    if errors:
        print("PLUGIN VALIDATION FAILED")
        for e in errors: print("-", e)
        return 1
    print("PLUGIN VALIDATION PASS")
    print(f"version={plugin.get('version')} skills={len(EXPECTED)} contracts={len(CONTRACT_FILES)} behavior_cases=60+ control_plane_cases=35+")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
