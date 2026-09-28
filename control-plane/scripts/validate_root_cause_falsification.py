#!/usr/bin/env python3
"""Validate root-cause-falsification policy and pressure cases."""

from __future__ import annotations
import json
from pathlib import Path

REQUIRED_TRUE = {
    ("goal_fidelity", "examples_are_nonbinding_unless_explicitly_promoted"),
    ("causal_model", "trigger_is_not_root_cause"),
    ("causal_model", "mutation_requires_mechanism_hypothesis"),
    ("repair_semantics", "limit_as_fix_forbidden"),
    ("repair_semantics", "capability_reduction_as_fix_forbidden"),
    ("repair_semantics", "mitigation_cannot_claim_fixed"),
    ("falsification", "universal_pass_invalidated_by_any_reproducible_in_scope_counterexample"),
    ("falsification", "verification_matrix_predeclared_before_results"),
    ("falsification", "all_in_scope_trials_count"),
    ("falsification", "success_cherry_picking_forbidden"),
    ("falsification", "original_failure_replay_required"),
    ("falsification", "retain_and_replay_failures"),
    ("evidence_routing", "single_anecdote_is_lead_only"),
    ("evidence_routing", "collapse_correlated_lineages"),
    ("evidence_routing", "official_docs_are_not_execution_proof"),
    ("evidence_routing", "official_unsupported_does_not_equal_empirically_impossible"),
    ("research_execution_loop", "one_search_hit_direct_to_patch_forbidden"),
    ("completion", "configuration_presence_is_not_completion"),
}

REQUIRED_CASES = {
    "rcf-001-one-counterexample-veto",
    "rcf-002-success-mining",
    "rcf-003-limit-is-mitigation",
    "rcf-004-example-not-constraint",
    "rcf-005-one-anecdote",
    "rcf-006-independent-convergence",
    "rcf-007-unsupported-not-impossible",
    "rcf-008-probabilistic-slo",
    "rcf-009-workaround-stack",
    "rcf-010-root-fix-closure",
}

def main() -> int:
    root = Path(__file__).resolve().parents[2]
    policy_path = root / "control-plane/ai-system/configs/root-cause-falsification-v1.json"
    cases_path = root / "plugins/ai-efficiency-operating-system/evals/root-cause-falsification-cases.jsonl"
    errors: list[str] = []

    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "errors": [f"policy: {exc}"]}, ensure_ascii=False))
        return 1

    if policy.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if policy.get("policy_id") != "root-cause-falsification-v1":
        errors.append("unexpected policy_id")
    if policy.get("default_enabled") is not True:
        errors.append("default_enabled must be true")

    for section, key in sorted(REQUIRED_TRUE):
        if (policy.get(section) or {}).get(key) is not True:
            errors.append(f"{section}.{key} must be true")

    classes = set((policy.get("repair_semantics") or {}).get("classes") or [])
    if classes != {"ROOT_FIX", "MITIGATION", "GUARDRAIL", "WORKAROUND", "DEGRADATION"}:
        errors.append("repair class set changed")

    practical = (policy.get("evidence_routing") or {}).get("practical_behavior_priority") or []
    for item in ("target_runtime", "independent_reproduction", "issue_pr_commit_failure_evidence", "independent_postmortem_or_production_report", "inspectable_benchmark"):
        if item not in practical:
            errors.append(f"practical evidence route missing: {item}")

    cases = []
    try:
        for line in cases_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                cases.append(json.loads(line))
    except Exception as exc:
        errors.append(f"cases: {exc}")

    ids = {case.get("id") for case in cases}
    for missing in sorted(REQUIRED_CASES - ids):
        errors.append(f"missing pressure case: {missing}")
    if len(cases) != len(ids):
        errors.append("duplicate pressure case id")

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors, "cases": len(cases)}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
