#!/usr/bin/env python3
"""Validate context-first capability routing invariants fail-closed."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

REQUIRED_BENIGN_CONTEXTS = {
    "analysis", "classification", "critique", "defensive_security",
    "education", "fiction", "harm_prevention", "historical_discussion",
    "legal_or_policy_analysis", "quotation", "research", "summarization",
    "translation",
}
REQUIRED_BOUNDARIES = {
    "higher_priority_instructions",
    "host_or_platform_safety_enforcement",
    "tool_permissions_and_access_control",
    "applicable_law_and_user_authorization",
}


def validate(payload: dict) -> dict[str, object]:
    failures: list[str] = []
    if payload.get("schema_version") != 1:
        failures.append("schema_version_must_be_1")
    if payload.get("mode") != "context_first":
        failures.append("mode_must_be_context_first")

    invariants = payload.get("invariants") if isinstance(payload.get("invariants"), dict) else {}
    if not invariants:
        failures.append("invariants_missing")
    if invariants.get("keyword_only_blocking") is not False:
        failures.append("keyword_only_blocking_must_be_false")
    for name in [
        "keyword_presence_is_not_intent",
        "preserve_contextually_needed_terms",
        "narrow_refusal_only",
        "continue_allowed_subtasks",
        "prefer_safe_transformation_over_blanket_refusal",
        "do_not_claim_product_policy_changes",
        "do_not_attempt_safety_bypass_or_filter_evasion",
    ]:
        if invariants.get(name) is not True:
            failures.append(f"{name}_must_be_true")

    contexts = payload.get("benign_contexts_to_preserve") if isinstance(payload.get("benign_contexts_to_preserve"), list) else []
    missing_contexts = sorted(REQUIRED_BENIGN_CONTEXTS - set(contexts))
    if missing_contexts:
        failures.append("missing_benign_contexts:" + ",".join(missing_contexts))

    boundaries = payload.get("non_override_boundaries") if isinstance(payload.get("non_override_boundaries"), list) else []
    missing_boundaries = sorted(REQUIRED_BOUNDARIES - set(boundaries))
    if missing_boundaries:
        failures.append("missing_non_override_boundaries:" + ",".join(missing_boundaries))

    response_policy = payload.get("response_policy") if isinstance(payload.get("response_policy"), dict) else {}
    mixed = str(response_policy.get("mixed_request", ""))
    if "complete_allowed_parts" not in mixed or "limit_only_the_disallowed_part" not in mixed:
        failures.append("mixed_request_must_preserve_allowed_scope")
    if "do_not_force_euphemisms" not in str(response_policy.get("terminology", "")):
        failures.append("terminology_preservation_missing")

    return {"schemaVersion": 1, "failures": sorted(set(failures)), "result": "PASS" if not failures else "FAIL"}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", default="ai-system/configs/context-first-capability-routing.json")
    args = parser.parse_args(argv)
    path = pathlib.Path(args.config)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = {"schemaVersion": 1, "failures": [f"config_load_failed:{type(exc).__name__}"], "result": "FAIL"}
    else:
        result = validate(payload if isinstance(payload, dict) else {})
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
