#!/usr/bin/env python3
"""Static + deterministic regression gate for the OpenClaw native adapter."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EVALS = ROOT / "evals" / "openclaw-adapter-cases.jsonl"
ROUTER = ROOT / "scripts" / "role_router.py"
LOCK = ROOT / "upstream-lock.json"

EXPECTED_SKILLS = {
    "openclaw-goal-orchestrator",
    "openclaw-evidence-gate",
    "openclaw-runtime-recovery",
    "openclaw-learning-loop",
    "openclaw-lobster-workflows",
}
EXPECTED_CLASSES = {
    "direct",
    "research",
    "execution",
    "forensics",
    "falsification",
    "impact",
    "compatibility",
    "recovery",
    "learning",
    "architecture",
    "combined",
    "pressure",
    "workflow",
}
OPENCLAW_SHA = "d84cdc5c03d378c0f50db1b0abb17537f390b01c"
EXPECTED_PLANES = {"parent", "agents", "lobster", "hybrid"}


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def load_router():
    spec = importlib.util.spec_from_file_location("openclaw_role_router", ROUTER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load role router")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    errors: list[str] = []

    present = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
    if present != EXPECTED_SKILLS:
        errors.append(f"skill inventory drift: {sorted(present)}")

    for path in sorted(SKILLS.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        name = path.parent.name
        if meta.get("name") != name:
            errors.append(f"frontmatter name mismatch: {name}")
        desc = meta.get("description", "")
        if not desc.startswith("Use when"):
            errors.append(f"description must start with Use when: {name}")
        if len(desc) > 160:
            errors.append(f"description exceeds OpenClaw 160-char guidance: {name}")

    orchestrator = (SKILLS / "openclaw-goal-orchestrator" / "SKILL.md").read_text(encoding="utf-8")
    for marker in [
        "No fixed child count",
        "child result is evidence",
        "sessions_spawn",
        "Swarm",
        "Lobster",
        "hybrid",
        "isolated",
        "fork",
        "parent owns the final completion claim",
        "role_router.py",
    ]:
        if marker.lower() not in orchestrator.lower():
            errors.append(f"orchestrator marker missing: {marker}")

    evidence = (SKILLS / "openclaw-evidence-gate" / "SKILL.md").read_text(encoding="utf-8")
    for marker in ["claim → acceptance", "owning evidence", "read-back", "HOST_LIVE"]:
        if marker.lower() not in evidence.lower():
            errors.append(f"evidence marker missing: {marker}")

    recovery = (SKILLS / "openclaw-runtime-recovery" / "SKILL.md").read_text(encoding="utf-8")
    for marker in ["two consecutive", "three materially distinct", "blocked slice", "different causal route"]:
        if marker.lower() not in recovery.lower():
            errors.append(f"recovery marker missing: {marker}")

    learning = (SKILLS / "openclaw-learning-loop" / "SKILL.md").read_text(encoding="utf-8")
    for marker in [
        "Represent → Hypothesize → Discriminate → Execute → Measure → Attribute → Abstract → Encode",
        "Skill Workshop",
        "secrets",
        "counterexample",
        "rollback",
    ]:
        if marker.lower() not in learning.lower():
            errors.append(f"learning marker missing: {marker}")

    lobster = (SKILLS / "openclaw-lobster-workflows" / "SKILL.md").read_text(encoding="utf-8")
    for marker in [
        "Sub-agents / Swarm",
        "needs_approval",
        "resume",
        "openclaw.invoke",
        "sandboxed",
        "openclaw-evidence-gate",
    ]:
        if marker.lower() not in lobster.lower():
            errors.append(f"lobster marker missing: {marker}")

    role_pool = json.loads(
        (SKILLS / "openclaw-goal-orchestrator" / "references" / "role-pool.json").read_text(encoding="utf-8")
    )
    if set((role_pool.get("execution_planes") or {}).keys()) != EXPECTED_PLANES:
        errors.append("execution-plane contract drift")

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    if lock.get("openclaw", {}).get("commit") != OPENCLAW_SHA:
        errors.append("OpenClaw upstream lock drift")
    if lock.get("checked_at") != "2026-09-04":
        errors.append("OpenClaw checked_at drift")
    surfaces = set(lock.get("openclaw", {}).get("surfaces") or [])
    if "docs/tools/lobster.md" not in surfaces:
        errors.append("Lobster upstream surface is not pinned")
    if "src/config/schema.help.runtime.ts" not in surfaces:
        errors.append("absolute tool-policy source is not pinned")

    rows = [
        json.loads(line)
        for line in EVALS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) < 20:
        errors.append("need at least 20 adapter regression cases")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate eval ids")
    classes = {row["class"] for row in rows}
    if not EXPECTED_CLASSES.issubset(classes):
        errors.append(f"missing eval classes: {sorted(EXPECTED_CLASSES - classes)}")

    router = load_router()
    counts = set()
    planes = set()
    for row in rows:
        routed = router.route(row["state"])
        actual = routed["roles"]
        plane = routed["execution_plane"]
        expected = row["expected_roles"]
        expected_plane = row["expected_plane"]
        counts.add(len(actual))
        planes.add(plane)
        if actual != expected:
            errors.append(f"{row['id']}: expected roles {expected}, got {actual}")
        if plane != expected_plane:
            errors.append(f"{row['id']}: expected plane {expected_plane}, got {plane}")
    if len(counts) < 5 or 0 not in counts:
        errors.append("role routing does not demonstrate adaptive fan-out including zero-child paths")
    if planes != EXPECTED_PLANES:
        errors.append(f"execution-plane coverage drift: {sorted(planes)}")

    installer = (ROOT / "scripts" / "install_adapter.py").read_text(encoding="utf-8")
    for marker in [
        "--expect-current-json",
        "--expect-current-absent",
        "numeric_floor",
        "skills.load.extraDirs",
        "ensure_tools_allowed",
        "allow_path",
        "also_allow_path",
        "agents.entries.{args.agent}.tools",
        "lobster",
        "config\", \"validate",
        "CONFIG_BACKUP",
    ]:
        if marker not in installer:
            errors.append(f"installer invariant missing: {marker}")

    if errors:
        print("OPENCLAW ADAPTER VALIDATION FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("OPENCLAW ADAPTER VALIDATION PASS")
    print(
        f"skills={len(EXPECTED_SKILLS)} evals={len(rows)} fanout_counts={sorted(counts)} "
        f"planes={sorted(planes)} upstream={OPENCLAW_SHA[:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
