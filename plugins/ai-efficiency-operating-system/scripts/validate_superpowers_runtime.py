#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "superpowers-conversation-runtime"
EXPECTED_PROCESS_MAP = {
    "debugging": "systematic-debugging",
    "behavior_change": "brainstorming",
    "settled_design_implementation": "test-driven-development",
    "approved_plan_execution": "executing-plans",
    "review_feedback": "receiving-code-review",
    "skill_authoring": "writing-skills",
    "completion_claim": "verification-before-completion",
}
REQUIRED_UPSTREAM_PATHS = {
    "skills/using-superpowers/SKILL.md",
    "skills/brainstorming/SKILL.md",
    "skills/systematic-debugging/SKILL.md",
    "skills/test-driven-development/SKILL.md",
    "skills/writing-plans/SKILL.md",
    "skills/executing-plans/SKILL.md",
    "skills/receiving-code-review/SKILL.md",
    "skills/writing-skills/SKILL.md",
    "skills/verification-before-completion/SKILL.md",
}
REQUIRED_PROCESS_COVERAGE = {
    "systematic-debugging",
    "brainstorming",
    "test-driven-development",
    "executing-plans",
    "receiving-code-review",
    "writing-skills",
    "verification-before-completion",
}


def fail(errors, message):
    errors.append(message)


def main():
    errors = []
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    policy = json.loads((SKILL_DIR / "runtime-policy.json").read_text(encoding="utf-8"))
    lock = json.loads((SKILL_DIR / "references" / "upstream-lock.json").read_text(encoding="utf-8"))
    host_adapters = json.loads((ROOT / "host-adapters.json").read_text(encoding="utf-8"))
    agent = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    eval_path = ROOT / "evals" / "superpowers-conversation-routing-cases.jsonl"
    rows = [json.loads(line) for line in eval_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    if not frontmatter:
        fail(errors, "missing skill frontmatter")
    else:
        meta = frontmatter.group(1)
        if "name: superpowers-conversation-runtime" not in meta:
            fail(errors, "wrong skill name")
        if "description: Use when" not in meta:
            fail(errors, "description must be trigger-only and start with Use when")

    body_words = len(skill.split())
    if body_words > 200:
        fail(errors, f"high-frequency bridge skill too large: {body_words} words > 200")
    for marker in ["Stay quiet by default", "DIRECT", "BOUNDED", "ARCHITECTURAL", "Never invent", "Do the work first"]:
        if marker.lower() not in skill.lower():
            fail(errors, f"missing bridge marker: {marker}")

    if "allow_implicit_invocation: true" not in agent:
        fail(errors, "ordinary-chat bridge must allow implicit invocation")

    adapters = host_adapters.get("adapters") or []
    matches = [item for item in adapters if item.get("name") == "superpowers-conversation-runtime"]
    if host_adapters.get("schema") != 1:
        fail(errors, "host-adapter schema must be 1")
    if len(matches) != 1:
        fail(errors, "Superpowers host adapter must be registered exactly once")
    else:
        adapter = matches[0]
        expected_adapter = {
            "host": "ordinary-chatgpt",
            "skill_path": "skills/superpowers-conversation-runtime",
            "allow_implicit_invocation": True,
            "canonical_router_membership": False,
            "shadow_oracle": "scripts/superpowers_route_oracle.py",
            "runtime_policy": "skills/superpowers-conversation-runtime/runtime-policy.json",
            "upstream_lock": "skills/superpowers-conversation-runtime/references/upstream-lock.json",
        }
        for key, expected in expected_adapter.items():
            if adapter.get(key) != expected:
                fail(errors, f"host-adapter registration drift: {key}")

    if policy.get("mode") != "ordinary-chat-progressive-ceremony":
        fail(errors, "wrong runtime mode")
    if policy.get("presentation", {}).get("default") != "quiet":
        fail(errors, "quiet presentation must be default")
    if policy.get("presentation", {}).get("announce_skill_names") is not False:
        fail(errors, "skill announcements must be disabled by default")
    if policy.get("ceremony", {}).get("levels") != ["DIRECT", "BOUNDED", "ARCHITECTURAL"]:
        fail(errors, "ceremony levels drift")
    if policy.get("ceremony", {}).get("one_way_complexity_ratchet") is not True:
        fail(errors, "complexity ratchet missing")
    if policy.get("process_map") != EXPECTED_PROCESS_MAP:
        fail(errors, "Superpowers process map drift")

    host = policy.get("host_adaptation", {})
    for key in [
        "never_invent_subagents",
        "never_invent_worktrees",
        "never_invent_background_execution",
        "never_claim_tests_without_execution",
        "use_runtime_features_only_when_available",
    ]:
        if host.get(key) is not True:
            fail(errors, f"host truth invariant missing: {key}")

    owners = policy.get("evidence_owner", {})
    expected_owners = {
        "library_framework_sdk_api": "Context7-first",
        "repository_pr_issue_actions": "GitHub",
        "user_files": "Files",
        "current_public_fact": "web",
        "stateful_change_completion": "owning-system-readback",
    }
    for key, expected in expected_owners.items():
        if owners.get(key) != expected:
            fail(errors, f"evidence owner drift: {key}")

    source = lock.get("source", {})
    if source.get("repo") != "obra/superpowers":
        fail(errors, "wrong upstream repo")
    if source.get("commit") != "b36e0829c6d0140e93cfef2ca599b1b07d4a7797":
        fail(errors, "unexpected upstream revision")
    if not REQUIRED_UPSTREAM_PATHS.issubset(set(source.get("paths", []))):
        fail(errors, "upstream lock misses required Superpowers process skills")

    ids = [row["id"] for row in rows]
    if len(rows) < 17:
        fail(errors, "insufficient ordinary-chat pressure cases")
    if len(ids) != len(set(ids)):
        fail(errors, "duplicate ordinary-chat pressure case ids")
    covered = {row.get("expected_upstream_process") for row in rows if row.get("expected_upstream_process")}
    missing_process = REQUIRED_PROCESS_COVERAGE - covered
    if missing_process:
        fail(errors, f"missing Superpowers process coverage: {sorted(missing_process)}")

    if errors:
        print("SUPERPOWERS RUNTIME VALIDATION FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("SUPERPOWERS RUNTIME VALIDATION PASS")
    print(
        f"cases={len(rows)} skill_words={body_words} upstream={source.get('commit')[:12]} "
        f"adapter=registered-isolated process_coverage={len(covered)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
