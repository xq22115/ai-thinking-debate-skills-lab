#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from route_oracle import fallback_chain, route, route_bundle


def main(path):
    failures = []
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        explicit = row.get("explicit")
        caps = row.get("host_capabilities")
        if "expected_primary" in row:
            got = route(row["prompt"], explicit, caps)
            if got != row["expected_primary"]:
                failures.append((row["id"], "primary", row["expected_primary"], got))
        if "expected_bundle" in row:
            got = route_bundle(row["prompt"], explicit, caps)
            if got != row["expected_bundle"]:
                failures.append((row["id"], "bundle", row["expected_bundle"], got))
        if "expected_fallback" in row:
            primary = route(row["prompt"], explicit, caps)
            got = fallback_chain(primary)
            if got != row["expected_fallback"]:
                failures.append((row["id"], "fallback", row["expected_fallback"], got))
    print(f"composition cases: {len(rows)}; failures: {len(failures)}")
    for rid, field, expected, got in failures:
        print(f"FAIL {rid} {field}: expected={expected} got={got}")
    return 1 if failures else 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "evals" / "composition-cases.jsonl"
    raise SystemExit(main(target))
