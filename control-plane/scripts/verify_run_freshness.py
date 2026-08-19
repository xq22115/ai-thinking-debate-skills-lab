#!/usr/bin/env python3
"""Fail closed when the trusted base has moved since a run was pinned."""
from __future__ import annotations

import argparse
import json
import pathlib
import re

SHA40 = re.compile(r"^[0-9a-f]{40}$")


def verify_freshness(pinned_base_sha: str, current_base_sha: str) -> dict[str, object]:
    failures: list[str] = []
    if not SHA40.fullmatch(str(pinned_base_sha)):
        failures.append("invalid_pinned_base_sha")
    if not SHA40.fullmatch(str(current_base_sha)):
        failures.append("invalid_current_base_sha")
    if not failures and pinned_base_sha != current_base_sha:
        failures.append("base_head_drift")
    return {
        "schemaVersion": 1,
        "pinned_base_sha": pinned_base_sha,
        "current_base_sha": current_base_sha,
        "failures": failures,
        "result": "PASS" if not failures else "VETO",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pinned", required=True)
    parser.add_argument("--current", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    result = verify_freshness(args.pinned, args.current)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
