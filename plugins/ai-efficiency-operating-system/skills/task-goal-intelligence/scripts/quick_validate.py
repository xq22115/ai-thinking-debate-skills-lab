#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
PLUGIN = SKILL.parents[1]
REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/upstream-lock.json",
    "references/phase-machine.md",
    "references/runtime-preamble.md",
    "references/evidence-and-optimization.md",
    "scripts/goal_skill_start.py",
    "scripts/quick_validate.py",
]
UPSTREAMS = {
    "openai-plugins": "1e285826e604f66f7208f7ac4dba0fe8341d1f57",
    "superpowers": "b36e0829c6d0140e93cfef2ca599b1b07d4a7797",
    "gstack": "0d1bd5616c0ef096bb7ccee336f63c60ee408618",
    "anthropic-skills": "41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f",
    "dspy-gepa": "59ce7601ec40cd2160ac64f476f9053efdc1599e",
}


def load_runtime():
    path = SKILL / "scripts" / "goal_skill_start.py"
    spec = importlib.util.spec_from_file_location("goal_skill_start", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load runtime preamble")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (SKILL / rel).exists():
            errors.append(f"missing skill package file: {rel}")

    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\nname: task-goal-intelligence\n"):
        errors.append("skill frontmatter/name missing")
    if len(text.splitlines()) > 260:
        errors.append(f"router SKILL.md too large: {len(text.splitlines())} lines > 260")
    for marker in (
        "Runtime preamble",
        "Interpretation",
        "Semantic delta",
        "Active routing handoffs",
        "Fallback/self-repair",
        "at most three implicit skills",
        "references/phase-machine.md",
        "references/evidence-and-optimization.md",
    ):
        if marker.lower() not in text.lower():
            errors.append(f"router marker missing: {marker}")

    agent = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "allow_implicit_invocation: true" not in agent:
        errors.append("task goal skill must remain implicit")

    lock = json.loads((SKILL / "references" / "upstream-lock.json").read_text(encoding="utf-8"))
    if (lock.get("policy") or {}).get("upstream_text_vendored") is not False:
        errors.append("upstream lock must forbid vendored upstream prose")
    observed = {row.get("id"): row.get("commit") for row in lock.get("sources", [])}
    if observed != UPSTREAMS:
        errors.append("upstream exact-revision lock drift")

    phase = (SKILL / "references" / "phase-machine.md").read_text(encoding="utf-8")
    for state in ("ORIENT", "DISCRIMINATE", "COMMIT", "EXECUTE", "VERIFY", "RECOVER", "LEARN"):
        if state not in phase:
            errors.append(f"phase missing: {state}")
    if "one-way complexity ratchet" not in phase.lower():
        errors.append("one-way complexity ratchet missing")

    runtime = load_runtime()
    smoke = runtime.evaluate_state({
        "root_goal": "verify",
        "desired_end_state": "verified",
        "target_identity": "runtime",
        "acceptance_tests": ["readback"],
        "goal_contract_committed": True,
        "completion_claim": True,
    })
    if smoke.get("phase") != "VERIFY" or smoke.get("gates", {}).get("fresh_verification_required") is not True:
        errors.append("runtime preamble completion smoke test failed")

    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors, "upstreams": len(observed)}, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
