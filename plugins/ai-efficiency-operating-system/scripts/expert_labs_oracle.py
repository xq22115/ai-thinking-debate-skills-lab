#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def capability(d):
    if d.get("requests_safety_or_access_bypass"):
        return "BOUNDARY_BLOCKED"
    if d.get("same_model_harness_delta"):
        return "HARNESS_DIFFERENTIAL"
    if d.get("installed") and not d.get("visible"):
        return "REGISTRATION_OR_SESSION"
    if d.get("visible") and not d.get("authorized"):
        return "AUTH_OR_PERMISSION"
    if d.get("authorized") and d.get("visible") and not d.get("invokable"):
        return "LOAD_SCHEMA_OR_RUNTIME"
    if d.get("invokable") and not d.get("effective"):
        return "RUNTIME_EFFECT_FAILURE"
    if d.get("effective") and not d.get("verified"):
        return "OBSERVABILITY_GAP"
    if d.get("verified"):
        return "CAPABILITY_VERIFIED"
    return "UNKNOWN"


def mcp(d):
    if d.get("tool_metadata_injection"):
        return "QUARANTINE_METADATA"
    if d.get("schema_changed"):
        return "REFRESH_RUNTIME_SCHEMA"
    if d.get("namespace_collision"):
        return "RESOLVE_CANONICAL_ID"
    if d.get("entitlement_mismatch"):
        return "CURRENT_SURFACE_MISMATCH"
    if d.get("many_tools") and d.get("sparse_use"):
        return "DYNAMIC_DISCOVERY"
    return "VALIDATE_MINIMAL_CALL"


def reverse(d):
    if not d.get("authorized"):
        return "STOP_UNAUTHORIZED"
    if d.get("requests_access_drm_or_license_bypass"):
        return "STOP_BOUNDARY"
    if not d.get("artifact_hash_pinned"):
        return "PIN_ARTIFACT"
    if d.get("tool_version_mismatch"):
        return "PIN_TOOLCHAIN"
    if d.get("static_uncertainty") and d.get("dynamic_discriminates"):
        return "DYNAMIC_PIVOT"
    return "STATIC_ANALYSIS"


def runtime(d):
    if d.get("unknown_effect") and not d.get("replay_safe"):
        return "RECONCILE_BEFORE_REPLAY"
    if d.get("tool_success") and not d.get("postcondition"):
        return "UNVERIFIED_EFFECT"
    if d.get("model_event") and d.get("tool_event") and d.get("runtime_event") and d.get("artifact_hash") and d.get("postcondition"):
        return "CORROBORATED_CAUSAL_CHAIN"
    if not d.get("runtime_event"):
        return "RUNTIME_EVIDENCE_GAP"
    return "BUILD_PROVENANCE_GRAPH"


ROUTERS = {
    "capability": capability,
    "mcp": mcp,
    "reverse": reverse,
    "runtime": runtime,
}


def main(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    failures = []
    for row in rows:
        kind = row["kind"]
        got = ROUTERS[kind](row.get("input", {}))
        if got != row["expected"]:
            failures.append((row["id"], row["expected"], got))
    print(f"expert lab cases: {len(rows)}; failures: {len(failures)}")
    for rid, expected, got in failures:
        print(f"FAIL {rid}: expected={expected} got={got}")
    return 1 if failures else 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "evals" / "expert-labs-cases.jsonl"
    raise SystemExit(main(target))
