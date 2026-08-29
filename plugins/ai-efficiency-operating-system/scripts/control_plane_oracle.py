#!/usr/bin/env python3
"""Provider-free known-outcome oracle for AI Efficiency OS control contracts."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


def load_contract(name):
    return json.loads((CONTRACTS / name).read_text(encoding="utf-8"))


RESEARCH = load_contract("research-integrity.json")
EVALUATORS = load_contract("evaluator-governance.json")
COMPOSITION = load_contract("skill-composition.json")
REPLAY = load_contract("replay-checkpoints.json")
VALIDATION = load_contract("validation-policy.json")


def review_stop(x):
    epoch = x["surface_epoch"]
    lens_epochs = x.get("mandatory_lens_epochs", {})
    current_lenses = bool(lens_epochs) and all(v == epoch for v in lens_epochs.values())
    regression_current = x.get("regression_artifact_hash") == x.get("current_artifact_hash")
    critical_open = bool(x.get("critical_open"))
    if not current_lenses or not regression_current or critical_open:
        if x.get("no_delta_streak", 0) >= 2:
            return "PIVOT_BUT_CONTINUE"
        return "CONTINUE"
    return "STOP_OPTIONAL"


def research_release(x):
    if x.get("retrieved_instruction_executed"):
        return "BLOCKED"
    if not x.get("full_source_verified", False) and x.get("full_source_available", True):
        return "INCOMPLETE_EVIDENCE"
    citation_ok = all(x.get(k, False) for k in ("citation_source_accessible", "citation_relevant", "citation_fact_supported"))
    if not citation_ok:
        return "BLOCKED" if x.get("load_bearing", True) else "PARTIAL"
    if not x.get("counterevidence_receipt", False):
        return "INCOMPLETE_EVIDENCE"
    if x.get("overturning_conflict", False):
        return "CONTESTED"
    if not x.get("provenance_diversified", True):
        return "PARTIAL"
    return "RELEASE"


def tribunal(x):
    if x.get("deterministic") == "FAIL":
        return "FAIL"
    if x.get("high_impact", False):
        if x.get("deterministic") != "PASS":
            return "INSUFFICIENT_EVIDENCE"
        if x.get("independent_method") != "PASS":
            if x.get("independent_method") == "FAIL" or x.get("semantic") == "FAIL":
                return "REVIEW"
            return "INSUFFICIENT_EVIDENCE"
        if x.get("semantic") == "FAIL":
            return "REVIEW"
        return "PASS"
    votes = [v for v in (x.get("deterministic"), x.get("independent_method"), x.get("semantic")) if v in {"PASS", "FAIL"}]
    if "FAIL" in votes and "PASS" in votes:
        return "REVIEW"
    if "PASS" in votes:
        return "PASS"
    if "FAIL" in votes:
        return "FAIL"
    return "INSUFFICIENT_EVIDENCE"


def skill_promotion(x):
    if not x.get("compatible", True) or x.get("hard_negative_regression", False):
        return "REJECT"
    if x.get("candidate_quality", 0) < x.get("baseline_quality", 0):
        return "REJECT"
    if x.get("candidate_false_completion", 0) > x.get("baseline_false_completion", 0):
        return "REJECT"
    if x.get("candidate_source_violation", 0) > x.get("baseline_source_violation", 0):
        return "REJECT"
    gains = [
        x.get("candidate_tool_calls", 0) < x.get("baseline_tool_calls", 0),
        x.get("candidate_context", 0) < x.get("baseline_context", 0),
        x.get("candidate_duplicate_lineage", 0) < x.get("baseline_duplicate_lineage", 0),
        x.get("candidate_full_research_ratio", 0) < x.get("baseline_full_research_ratio", 0),
        x.get("candidate_accepted_per_cost", 0) > x.get("baseline_accepted_per_cost", 0),
    ]
    if not any(gains):
        return "HOLD"
    return "PROMOTE" if x.get("evidence_class") == "OBSERVED_TARGET" else "SHADOW_ONLY"


def replay(x):
    if x.get("prior_verified_effect", False):
        return "RETURN_PRIOR_RECEIPT"
    if x.get("effect_state") == "UNKNOWN" and x.get("non_idempotent", False):
        return "RECONCILE_FIRST" if x.get("reconciliation_available", False) else "BLOCK_REPLAY"
    failure = x.get("failure_class")
    checkpoint = REPLAY["failure_restart"].get(failure)
    return checkpoint or "NO_RESTART_MAPPING"


def validation(x):
    layers = VALIDATION["validation_layers"]
    highest = x.get("highest_observed_layer")
    claimed = x.get("claimed_layer")
    if highest not in layers or claimed not in layers:
        return "INVALID_LAYER"
    if layers.index(claimed) > layers.index(highest):
        return "OVERCLAIM"
    if x.get("receipt_fresh", True) is False:
        return "STALE_RECEIPT"
    if x.get("declared_gate", False) and not x.get("executable_owner", False):
        return "DESCRIPTIVE_ONLY"
    return "VALID"


HANDLERS = {
    "review_stop": review_stop,
    "research_release": research_release,
    "tribunal": tribunal,
    "skill_promotion": skill_promotion,
    "replay": replay,
    "validation": validation,
}


def main(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    failures = []
    for row in rows:
        kind = row.get("kind")
        if kind not in HANDLERS:
            failures.append((row.get("id"), row.get("expected"), f"unknown-kind:{kind}"))
            continue
        got = HANDLERS[kind](row.get("input", {}))
        if got != row.get("expected"):
            failures.append((row.get("id"), row.get("expected"), got))
    print(f"control-plane cases: {len(rows)}; failures: {len(failures)}")
    for rid, expected, got in failures:
        print(f"FAIL {rid}: expected={expected} got={got}")
    return 1 if failures else 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else ROOT / "evals" / "control-plane-cases.jsonl"
    raise SystemExit(main(target))
