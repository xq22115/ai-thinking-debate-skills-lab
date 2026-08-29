#!/usr/bin/env python3
"""Plant known-bad package states and require validate_plugin.py to reject each one."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def mutate_settings_schema(root):
    p = root / "settings.json"; x = json.loads(p.read_text()); x["schema"] = 2; write_json(p, x)


def mutate_research_provenance(root):
    p = root / "contracts/research-integrity.json"; x = json.loads(p.read_text()); x["source_policy"]["count_by_provenance_family_not_url"] = False; write_json(p, x)


def mutate_evaluator_lifecycle(root):
    p = root / "contracts/evaluator-governance.json"; x = json.loads(p.read_text()); x["states"] = ["ACTIVE"]; write_json(p, x)


def mutate_skill_inventory(root):
    p = root / "contracts/skill-composition.json"; x = json.loads(p.read_text()); x["nodes"].pop("evidence-watchdog"); write_json(p, x)


def mutate_replay_safety(root):
    p = root / "contracts/replay-checkpoints.json"; x = json.loads(p.read_text()); x["effect_replay"]["non_idempotent_unknown_without_reconciliation"] = "ALLOW_REPLAY"; write_json(p, x)


def mutate_validation_layer(root):
    p = root / "contracts/validation-policy.json"; x = json.loads(p.read_text()); x["invariants"]["lower_layer_pass_never_implies_higher_layer_pass"] = False; write_json(p, x)


def mutate_duplicate_behavior_id(root):
    p = root / "evals/behavior-cases.jsonl"; lines = p.read_text(encoding="utf-8").splitlines(); p.write_text("\n".join(lines + [lines[0]]) + "\n", encoding="utf-8")


def mutate_version_drift(root):
    p = root / ".codex-plugin/plugin.json"; x = json.loads(p.read_text()); x["version"] = "9.9.9-bad"; write_json(p, x)


MUTATIONS = [
    ("settings-schema", mutate_settings_schema),
    ("research-provenance", mutate_research_provenance),
    ("evaluator-lifecycle", mutate_evaluator_lifecycle),
    ("skill-inventory", mutate_skill_inventory),
    ("unsafe-replay", mutate_replay_safety),
    ("validation-overclaim", mutate_validation_layer),
    ("duplicate-behavior-id", mutate_duplicate_behavior_id),
    ("version-drift", mutate_version_drift),
]


def main():
    failures = []
    with tempfile.TemporaryDirectory(prefix="ai-efficiency-validator-mutations-") as td:
        base = Path(td)
        for label, mutation in MUTATIONS:
            candidate = base / label
            shutil.copytree(ROOT, candidate)
            mutation(candidate)
            env = dict(os.environ)
            env["AI_EFFICIENCY_REPO_ROOT"] = str(REPO)
            proc = subprocess.run(
                [sys.executable, str(candidate / "scripts/validate_plugin.py")],
                cwd=REPO,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=30,
            )
            if proc.returncode == 0:
                failures.append(label)
                print(f"FAIL {label}: validator accepted planted defect")
            else:
                print(f"PASS {label}: planted defect rejected")
    print(f"validator mutation cases: {len(MUTATIONS)}; failures: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
