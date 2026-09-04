#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "native-goal-harness.json"
SKILL = ROOT / "skills" / "task-goal-intelligence"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    settings = json.loads((ROOT / "settings.json").read_text(encoding="utf-8"))
    plugin = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))

    if plugin.get("version") != "1.3.0" or settings.get("version") != "1.3.0":
        errors.append("native package version must be 1.3.0 in plugin + settings")
    if plugin.get("version") != settings.get("version"):
        errors.append("plugin/settings version drift")
    binding = settings.get("native_goal_harness") or {}
    if binding.get("profile") != "./native-goal-harness.json" or binding.get("revision") != "4.0.0-native":
        errors.append("settings native_goal_harness binding drift")
    if binding.get("host_pressure_holdout_pass_not_preclaimed") is not True:
        errors.append("settings must preserve HOST_LIVE holdout truth boundary")

    if config.get("revision") != "4.0.0-native":
        errors.append("native harness revision drift")
    arch = config.get("architecture") or {}
    for key in (
        "skill_spec",
        "thin_router",
        "runtime_preamble",
        "quick_validator",
        "state_machine",
        "verification_optimizer",
        "upstream_lock",
        "state_eval",
        "host_pressure_holdout",
    ):
        rel = arch.get(key)
        if not rel or not (ROOT / rel).exists():
            errors.append(f"native architecture target missing: {key} -> {rel}")
    if int(arch.get("router_line_budget", 0)) != 260:
        errors.append("router line budget must remain 260")

    phase = config.get("phase_machine") or {}
    expected_states = ["ORIENT", "DISCRIMINATE", "COMMIT", "EXECUTE", "VERIFY", "RECOVER", "LEARN"]
    if phase.get("states") != expected_states:
        errors.append("native phase inventory/order drift")
    if phase.get("complexity_ratchet") != "ONE_WAY_UNLESS_USER_SEMANTIC_SCOPE_CHANGE":
        errors.append("complexity ratchet drift")
    if phase.get("three_failed_repairs_promote_architectural_review") is not True:
        errors.append("architectural escalation gate missing")

    runtime = config.get("runtime") or {}
    for key in (
        "native_preamble_preferred_when_executable",
        "degraded_inline_mode_when_unavailable",
        "degraded_mode_may_not_lower_goal_or_acceptance",
        "optional_runtime_instrumentation_failure_may_not_replace_user_task",
        "runtime_output_must_be_current_invocation_bound",
    ):
        if runtime.get(key) is not True:
            errors.append(f"runtime invariant missing: {key}")

    routing = config.get("routing") or {}
    if int(routing.get("max_implicit_skills", 0)) != 3:
        errors.append("native routing max implicit skills must remain 3")
    for key in (
        "goal_gate_first",
        "process_before_implementation_when_process_skill_materially_applies",
        "phase_before_keyword_similarity",
        "route_change_does_not_change_goal",
        "nearest_easier_task_probe_before_scope_reduction",
    ):
        if routing.get(key) is not True:
            errors.append(f"routing invariant missing: {key}")

    verification = config.get("verification") or {}
    expected_reverse = ["claim", "acceptance_test", "owning_evidence", "current_goal_version", "causal_path"]
    if verification.get("reverse_walk") != expected_reverse:
        errors.append("completion reverse-walk drift")
    for key in (
        "fresh_evidence_before_success_claim",
        "historical_claim_is_not_current_evidence",
        "agent_self_report_is_not_independent_proof",
        "command_success_is_not_postcondition_success",
    ):
        if verification.get(key) is not True:
            errors.append(f"verification invariant missing: {key}")

    optimization = config.get("optimization") or {}
    if optimization.get("promotion_slices") != ["target", "protection", "holdout", "adversarial"]:
        errors.append("optimizer promotion slices drift")
    if optimization.get("aggregate_score_cannot_override_hard_slice_regression") is not True:
        errors.append("hard-slice veto missing")
    if optimization.get("host_pressure_holdout_is_packaged_not_preclaimed_passed") is not True:
        errors.append("host holdout truth boundary missing")

    router = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if len(router.splitlines()) > 260:
        errors.append(f"thin router exceeded 260 lines: {len(router.splitlines())}")
    for rel in (
        "references/phase-machine.md",
        "references/runtime-preamble.md",
        "references/evidence-and-optimization.md",
        "references/upstream-lock.json",
    ):
        if rel not in router:
            errors.append(f"router does not progressively disclose: {rel}")

    holdout = load_jsonl(ROOT / arch["host_pressure_holdout"])
    ids = [row.get("id") for row in holdout]
    classes = {row.get("class") for row in holdout}
    if len(holdout) < 24:
        errors.append(f"insufficient host pressure holdout: {len(holdout)} < 24")
    if len(ids) != len(set(ids)):
        errors.append("duplicate host pressure holdout IDs")
    required_classes = {
        "semantic_minimization", "neighbor_task", "historical_claim", "recovery",
        "partial_blocker", "progress_theater", "semantic_delta", "completion",
        "capability_truth", "context_drift", "complexity", "architecture",
        "research", "provenance", "ambiguity", "debugging", "optimizer"
    }
    if not required_classes.issubset(classes):
        errors.append(f"pressure holdout class coverage missing: {sorted(required_classes - classes)}")
    for row in holdout:
        if not row.get("prompt") or not row.get("must") or not row.get("must_not"):
            errors.append(f"incomplete pressure holdout case: {row.get('id')}")

    commands = [
        [sys.executable, str(SKILL / "scripts" / "quick_validate.py")],
        [sys.executable, str(ROOT / "scripts" / "task_goal_native_oracle.py"), str(ROOT / "evals" / "task-goal-native-state-cases.jsonl")],
    ]
    command_results = []
    for command in commands:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        command_results.append({"command": command[-1], "returncode": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()})
        if proc.returncode != 0:
            errors.append(f"sub-validator failed: {command[-1]}: {proc.stdout.strip()} {proc.stderr.strip()}")

    print(json.dumps({
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "package_version": plugin.get("version"),
        "pressure_holdout_cases": len(holdout),
        "pressure_holdout_classes": len(classes),
        "subvalidators": command_results,
    }, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
