#!/usr/bin/env python3
"""Known-outcome oracle for ordinary-ChatGPT GitHub activation/root ownership classification."""

import json
import sys
from pathlib import Path


def classify(d):
    if d.get("depends_on_local_plugin") and not d.get("local_plugin_host_activation_verified"):
        return "CUSTOM_PLUGIN_ACTIVATION_UNVERIFIED"
    if not d.get("live_discovery_done", True) and not d.get("required_action_present", False):
        return "DISCOVER_LIVE_SURFACE_FIRST"
    if d.get("live_discovery_done") and d.get("required_action_present") is False:
        return "UPSTREAM_CAPABILITY_GAP"
    if d.get("required_action_present") and d.get("host_plugin_enabled") is False:
        return "HOST_PERMISSION_POLICY"
    if d.get("required_action_present") and d.get("host_plugin_enabled") and d.get("github_remote_permission_denied"):
        return "GITHUB_REMOTE_PERMISSION"
    if d.get("schema_current") is False and d.get("material_call_attempted"):
        return "CALLER_SCHEMA_STALE"
    if d.get("response_truncated") and d.get("treated_as_exhaustive"):
        return "CALLER_RESPONSE_TRUNCATION"
    if d.get("lower_layer_success") and (not d.get("readback_verified") or not d.get("postcondition_verified")):
        return "CALLER_CHAIN_BREAK"

    target = d.get("numeric_result_target")
    if isinstance(target, int) and target > 0:
        unique = int(d.get("unique_results", 0))
        if unique < target:
            if d.get("connector_exhausted"):
                return "SEARCH_EXHAUSTED_BELOW_TARGET"
            return "CALLER_SEARCH_UNDERFETCH"

    return "ROOT_PATH_OK"


def main(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    failures = []
    for row in rows:
        got = classify(row.get("input", {}))
        if got != row["expected"]:
            failures.append((row["id"], row["expected"], got))
    print(f"github root-control cases: {len(rows)}; failures: {len(failures)}")
    for rid, expected, got in failures:
        print(f"FAIL {rid}: expected={expected} got={got}")
    return 1 if failures else 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "evals" / "github-root-control-cases.jsonl"
    raise SystemExit(main(target))
