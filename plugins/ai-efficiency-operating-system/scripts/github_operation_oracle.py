#!/usr/bin/env python3
"""Known-outcome oracle for the ordinary ChatGPT GitHub operation loop."""

import json
import sys
from pathlib import Path


def classify(d):
    if d.get("explanation_only"):
        return "NO_SPECIALIST"
    if d.get("permission_blocked"):
        return "VERIFY_EFFECTIVE_PERMISSION"
    if d.get("target_ambiguous"):
        return "RESOLVE_TARGET_IDENTITY"
    if d.get("schema_mismatch"):
        return "REDISCOVER_LIVE_SCHEMA"
    if d.get("stale_blob_sha"):
        return "REREAD_RECONCILE_CURRENT_SHA"
    if d.get("search_miss") and d.get("exact_identity_known"):
        return "PIVOT_EXACT_LOOKUP"
    if d.get("partial_or_ambiguous_response"):
        return "READ_CURRENT_REMOTE_STATE"
    if d.get("workflow_accepted") and not d.get("execution_observed"):
        return "EXECUTION_NOT_PROVEN"
    if d.get("same_mechanism_failures", 0) >= 2 and not d.get("material_evidence_delta"):
        return "CHANGE_CAUSAL_MECHANISM"
    if (
        d.get("target_resolved")
        and d.get("schema_resolved")
        and d.get("readback_verified")
        and d.get("acceptance_verified")
        and d.get("regression_verified")
    ):
        return "GITHUB_OPERATION_VERIFIED"
    return "BUILD_OPERATION_ENVELOPE"


def main(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    failures = []
    for row in rows:
        got = classify(row.get("input", {}))
        if got != row["expected"]:
            failures.append((row["id"], row["expected"], got))
    print(f"github operation cases: {len(rows)}; failures: {len(failures)}")
    for rid, expected, got in failures:
        print(f"FAIL {rid}: expected={expected} got={got}")
    return 1 if failures else 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "evals" / "github-operation-cases.jsonl"
    raise SystemExit(main(target))
