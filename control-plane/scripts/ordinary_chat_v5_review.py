#!/usr/bin/env python3
"""Ten heterogeneous review lanes for the ordinary-chat v5 task runtime.

These are deterministic independent review lanes, not simulated AI agents.
"""
from __future__ import annotations

import argparse
import ast
import json
import pathlib
import subprocess
import sys
from typing import Any, Callable

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "control-plane/ai-system/configs"
RUNTIME = ROOT / "control-plane/scripts/ordinary_chat_task_runtime.py"
ROUTER = ROOT / "control-plane/scripts/capability_router.py"
TEST_FILE = ROOT / "control-plane/tests/test_ordinary_chat_task_runtime.py"
TASK_WORKFLOW = ROOT / ".github/workflows/ordinary-chat-task-execute.yml"
SELFTEST_CONFIG = CONFIG_DIR / "ordinary-chat-immediate-use.json"
TASK_CONFIG = CONFIG_DIR / "ordinary-chat-task-runtime.json"
CAPS = CONFIG_DIR / "ordinary-chat-capabilities.json"
ROUTING = CONFIG_DIR / "ordinary-chat-routing.json"
SKILL = ROOT / "skills/ordinary-chat-agent-router/SKILL.md"
E2E_LEDGER = ROOT / "research/ordinary-chat-upstreams/2026-08-27-v5-e2e-result.json"


class ReviewFailure(RuntimeError):
    pass


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def run_test(name: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(TEST_FILE), f"OrdinaryChatTaskRuntimeTests.{name}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        raise ReviewFailure(f"test failed {name}: {proc.stdout[-2000:]} {proc.stderr[-2000:]}")
    return name


def lane_a01() -> list[str]:
    cfg = load(TASK_CONFIG)
    require(cfg["requestSchemaVersion"] == 2, "task request schema must be v2")
    require(cfg["intent"] == "ordinary_chat_task", "task intent mismatch")
    require(0 < cfg["maxSteps"] <= 64, "step fanout must be bounded")
    require("write_text" in cfg["enabledActions"] and "run_recipe" in cfg["enabledActions"], "expected task actions missing")
    require("control-plane/scripts/ordinary_chat_task_runtime.py" in cfg["mutation"]["protectedPaths"], "runtime must be request-protected")
    return ["request_schema_v2", "bounded_steps", "protected_runtime"]


def lane_a02() -> list[str]:
    routing = load(ROUTING)
    caps = load(CAPS)
    capmap = {item["id"]: item for item in caps["capabilities"]}
    require(capmap["github-task-runtime"]["status"] == "e2e_verified", "task runtime not marked E2E verified")
    require(capmap["github-actions-relay"]["status"] == "implemented_self_test_only", "self-test relay must not be task executor")
    rules = {item["name"]: item for item in routing["rules"]}
    require(rules["ordinary-chat-real-github-task"]["route"] == "github-task-runtime", "real task route mismatch")
    require(rules["ordinary-chat-infrastructure-self-test"]["taskExecutor"] is False, "self-test incorrectly marked task executor")
    return ["real_task_route", "selftest_separation", "e2e_capability_state"]


def lane_a03() -> list[str]:
    return [run_test("test_real_mutation_resume_and_five_method_adjudication"), run_test("test_dependency_execution_is_deterministic_even_when_dependency_appears_later")]


def lane_a04() -> list[str]:
    return [run_test("test_state_rejects_changed_request_revision"), run_test("test_real_mutation_resume_and_five_method_adjudication")]


def lane_a05() -> list[str]:
    routing = load(ROUTING)
    workflow = TASK_WORKFLOW.read_text(encoding="utf-8")
    cloud = routing["cloudTask"]
    require(cloud["sourceAndTaskEvidenceBranchesSeparated"] is True, "source/task evidence separation disabled")
    require(cloud["taskBranchPrefix"] == "chat-task/", "task branch prefix mismatch")
    require("startsWith(github.ref, 'refs/heads/chat-task/')" in workflow, "commit step not restricted to task branch")
    tracked_argv = "['git', 'diff', '--name-only', 'HEAD']"
    untracked_argv = "['git', 'ls-files', '--others', '--exclude-standard']"
    require(tracked_argv in workflow and untracked_argv in workflow, "tracked/untracked provenance argv check missing")
    require("if actual != expected:" in workflow, "working-tree equality gate missing")
    return ["branch_separation", "tracked_untracked_diff_argv", "working_tree_equality_gate", "task_branch_commit_only"]


def lane_a06() -> list[str]:
    source = RUNTIME.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "os" and node.func.attr == "system":
                raise ReviewFailure("os.system must not exist")
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                raise ReviewFailure(f"{node.func.id} must not exist")
            if isinstance(node.func, ast.Attribute) and node.func.attr == "run":
                for kw in node.keywords:
                    if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        raise ReviewFailure("subprocess shell=True must not exist")
    cfg = load(TASK_CONFIG)
    for recipe, spec in cfg["recipes"]["definitions"].items():
        for command in spec["commands"]:
            require(isinstance(command.get("argv"), list) and command["argv"], f"recipe {recipe} must use argv list")
    workflow = TASK_WORKFLOW.read_text(encoding="utf-8")
    require("@latest" not in workflow, "task workflow action must not float on @latest")
    return ["no_dynamic_shell", "recipe_argv_only", "pinned_actions"]


def lane_a07() -> list[str]:
    cfg = load(TASK_CONFIG)
    fetch = cfg["fetch"]
    require(fetch["allowedHosts"] and all("*" not in host and "/" not in host for host in fetch["allowedHosts"]), "fetch hosts must be exact names")
    require(0 < fetch["maxBytes"] <= 4 * 1024 * 1024, "fetch maxBytes too large or invalid")
    require(0 < fetch["timeoutSeconds"] <= 60, "fetch timeout invalid")
    source = RUNTIME.read_text(encoding="utf-8")
    require('parsed.scheme != "https"' in source, "https-only fetch enforcement missing")
    require('host not in config["fetch"]["allowedHosts"]' in source, "fetch allowlist enforcement missing")
    return ["https_only", "exact_host_allowlist", "bounded_fetch"]


def lane_a08() -> list[str]:
    names = [
        "test_rejects_command_field_in_request",
        "test_protected_runtime_path_is_not_mutable",
        "test_dependency_cycle_fails",
        "test_audit_mode_rejects_mutation",
        "test_registry_recipe_side_effect_outside_request_scope_vetoes_completion",
        "test_unknown_recipe_fails_without_fallback",
    ]
    return [run_test(name) for name in names]


def lane_a09() -> list[str]:
    workflow = TASK_WORKFLOW.read_text(encoding="utf-8")
    for token in ["completion-report.json", "run-pointer.json", "SHA256SUMS.json", "actions/upload-artifact@", "state.json"]:
        require(token in workflow, f"receipt component missing: {token}")
    ledger = load(E2E_LEDGER)
    require(ledger["completionMethods"]["M5_receipt_integrity"] == "PASS", "E2E receipt integrity not attested")
    require(ledger["independentArtifactVerification"]["manifestHashErrors"] == 0, "independent artifact hash verification failed")
    require(ledger["independentArtifactVerification"]["manifestEntriesVerified"] >= 6, "insufficient independently verified artifact entries")
    return ["receipt_bundle_components", "sha256_manifest", "independent_artifact_hash_check"]


def lane_a10() -> list[str]:
    selftest = load(SELFTEST_CONFIG)
    caps = load(CAPS)
    skill = SKILL.read_text(encoding="utf-8").lower()
    ledger = load(E2E_LEDGER)
    require(selftest.get("taskExecutor") is False and selftest.get("purpose") == "infrastructure_self_test_only", "self-test can still masquerade as task completion")
    capmap = {item["id"]: item for item in caps["capabilities"]}
    require(capmap["github-actions-relay"]["kind"] == "cloud_self_test_relay", "old relay kind is ambiguous")
    require("a self-test is diagnostic evidence only" in skill, "skill lacks anti-fake-completion rule")
    require(ledger["primary"]["executedSteps"] > 0 and ledger["resume"]["executedSteps"] == 0, "E2E does not prove real execution plus zero-reexecution resume")
    require(ledger["taskBotDiff"]["otherPathsRestrictedToTaskResultNamespace"] is True, "E2E provenance not isolated")
    return ["selftest_not_task_completion", "real_e2e_execution", "resume_zero_reexecution", "evidence_namespace_isolated"]


LANES: dict[str, Callable[[], list[str]]] = {
    "A01": lane_a01,
    "A02": lane_a02,
    "A03": lane_a03,
    "A04": lane_a04,
    "A05": lane_a05,
    "A06": lane_a06,
    "A07": lane_a07,
    "A08": lane_a08,
    "A09": lane_a09,
    "A10": lane_a10,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True, choices=sorted(LANES))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result: dict[str, Any] = {"schemaVersion": 1, "lane": args.lane, "result": "FAIL", "checks": []}
    try:
        result["checks"] = LANES[args.lane]()
        result["result"] = "PASS"
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"{type(exc).__name__}:{exc}"
    path = pathlib.Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
