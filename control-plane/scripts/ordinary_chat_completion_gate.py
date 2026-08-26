#!/usr/bin/env python3
"""Five-proof completion gate for the ordinary-chat GitHub execution relay.

The relay accepts a small declarative request only. It never accepts an arbitrary
command, shell fragment, executable path, or environment override from the request.
Ten independent verification lanes produce evidence; aggregation requires all five
completion methods to pass before the task can be called immediately usable.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTROL_PLANE = REPO_ROOT / "control-plane"
CONFIG = CONTROL_PLANE / "ai-system" / "configs" / "ordinary-chat-immediate-use.json"
CAPABILITIES = CONTROL_PLANE / "ai-system" / "configs" / "ordinary-chat-capabilities.json"
ROUTING = CONTROL_PLANE / "ai-system" / "configs" / "ordinary-chat-routing.json"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ordinary-chat-immediate-use.yml"
MCP_DIR = CONTROL_PLANE / "ai-system" / "mcp"
REQUEST_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,80}$")
ALLOWED_REQUEST_KEYS = {
    "schemaVersion",
    "request_id",
    "goal",
    "intent",
    "mode",
    "requested_completion_methods",
}
REQUIRED_METHODS = ["M1", "M2", "M3", "M4", "M5"]
LANES = [f"A{i:02d}" for i in range(1, 11)]
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
]


class GateError(RuntimeError):
    pass


def _json_load(path: pathlib.Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GateError(f"json_root_not_object:{path}")
    return value


def _write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _run(command: list[str], *, cwd: pathlib.Path | None = None, timeout: int = 180) -> dict[str, Any]:
    started = time.monotonic()
    try:
        cp = subprocess.run(
            command,
            cwd=str(cwd or REPO_ROOT),
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
            env=dict(os.environ),
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "reason": "timeout",
            "duration_ms": int((time.monotonic() - started) * 1000),
            "stdout_tail": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
        }
    return {
        "ok": cp.returncode == 0,
        "returncode": cp.returncode,
        "duration_ms": int((time.monotonic() - started) * 1000),
        "stdout_tail": cp.stdout[-2000:],
        "stderr_tail": cp.stderr[-2000:],
    }


def validate_request(path: pathlib.Path) -> tuple[dict[str, Any], list[str]]:
    failures: list[str] = []
    try:
        request = _json_load(path)
    except (OSError, json.JSONDecodeError, GateError) as exc:
        return {}, [f"request_unreadable:{type(exc).__name__}"]

    unknown = sorted(set(request) - ALLOWED_REQUEST_KEYS)
    if unknown:
        failures.append("request_unknown_fields:" + ",".join(unknown))
    if request.get("schemaVersion") != 1:
        failures.append("request_schema_invalid")
    request_id = request.get("request_id")
    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id):
        failures.append("request_id_invalid")
    goal = request.get("goal")
    if not isinstance(goal, str) or not goal.strip():
        failures.append("goal_empty")
    elif len(goal) > 4000:
        failures.append("goal_too_large")
    if request.get("intent") != "ordinary_chat_immediate_use":
        failures.append("intent_invalid")
    if request.get("mode") not in {"prove-ready", "audit"}:
        failures.append("mode_invalid")
    methods = request.get("requested_completion_methods")
    if methods != REQUIRED_METHODS:
        failures.append("completion_method_set_invalid")
    return request, failures


def _base_report(lane: str, request: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "lane": lane,
        "request_id": request.get("request_id"),
        "goal_sha256": hashlib.sha256(str(request.get("goal", "")).encode("utf-8")).hexdigest(),
        "repository": os.environ.get("GITHUB_REPOSITORY"),
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "generated_at_unix": int(time.time()),
        "checks": [],
        "result": "PASS",
    }


def _append(report: dict[str, Any], name: str, ok: bool, **details: Any) -> None:
    item = {"name": name, "result": "PASS" if ok else "FAIL"}
    item.update(details)
    report["checks"].append(item)
    if not ok:
        report["result"] = "FAIL"


def _append_run(report: dict[str, Any], name: str, run_result: dict[str, Any]) -> None:
    """Attach subprocess evidence without duplicating the positional success flag."""
    ok = bool(run_result.get("ok"))
    details = {key: value for key, value in run_result.items() if key != "ok"}
    _append(report, name, ok, **details)


def _registry() -> dict[str, dict[str, Any]]:
    value = _json_load(CAPABILITIES)
    items = value.get("capabilities")
    if not isinstance(items, list):
        raise GateError("capability_registry_invalid")
    return {str(item.get("id")): item for item in items if isinstance(item, dict) and item.get("id")}


def _lane_a01(report: dict[str, Any], request_path: pathlib.Path, request: dict[str, Any], request_failures: list[str]) -> None:
    _append(report, "request_schema", not request_failures, failures=request_failures)
    config = _json_load(CONFIG)
    _append(report, "goal_binding", config.get("allowedIntent") == request.get("intent"))
    methods = [item.get("id") for item in config.get("completionMethods", []) if isinstance(item, dict)]
    _append(report, "method_set", methods == REQUIRED_METHODS, configured=methods)
    _append(report, "request_path_scoped", request_path.resolve().is_relative_to((CONTROL_PLANE / "ordinary-chat-requests").resolve()))


def _lane_a02(report: dict[str, Any]) -> None:
    registry = _registry()
    relay = registry.get("github-actions-relay")
    _append(report, "github_actions_runtime", os.environ.get("GITHUB_ACTIONS") == "true")
    _append(report, "github_run_identity", bool(os.environ.get("GITHUB_RUN_ID") and os.environ.get("GITHUB_SHA")))
    _append(report, "relay_registry", isinstance(relay, dict) and relay.get("status") == "implemented")
    routing = _json_load(ROUTING)
    text = json.dumps(routing, sort_keys=True)
    _append(report, "relay_routing", "github-actions-relay" in text)


def _lane_a03(report: dict[str, Any]) -> None:
    commands = [
        [sys.executable, "-m", "py_compile", "control-plane/scripts/ordinary_chat_bridge.py", "control-plane/scripts/project_memory.py", "control-plane/scripts/capability_health.py", "control-plane/scripts/capability_router.py", "control-plane/scripts/run_reconciler.py", "control-plane/ordinary-chat-dashboard/server.py"],
        [sys.executable, "control-plane/tests/test_ordinary_chat_bridge.py"],
        [sys.executable, "control-plane/tests/test_project_memory.py"],
        [sys.executable, "control-plane/tests/test_capability_router.py"],
        [sys.executable, "control-plane/tests/test_run_reconciler.py"],
        [sys.executable, "control-plane/tests/test_ordinary_chat_dashboard.py"],
    ]
    for index, command in enumerate(commands, 1):
        _append_run(report, f"execution_{index}", _run(command, timeout=180))


def _lane_a04(report: dict[str, Any]) -> None:
    _append_run(report, "chaos_suite", _run([sys.executable, "control-plane/tests/test_ordinary_chat_chaos.py"], timeout=180))
    reconciler = CONTROL_PLANE / "scripts" / "run_reconciler.py"
    _append(report, "reconciler_present", reconciler.is_file())
    text = reconciler.read_text(encoding="utf-8") if reconciler.is_file() else ""
    _append(report, "no_auto_retry_in_reconciler", "subprocess.Popen" not in text and "retry" not in text.lower())


def _required_pack_files() -> list[pathlib.Path]:
    return [
        CONFIG,
        CAPABILITIES,
        ROUTING,
        WORKFLOW,
        CONTROL_PLANE / "scripts" / "ordinary_chat_completion_gate.py",
        CONTROL_PLANE / "scripts" / "ordinary_chat_bridge.py",
        CONTROL_PLANE / "scripts" / "capability_health.py",
        CONTROL_PLANE / "scripts" / "capability_router.py",
        CONTROL_PLANE / "scripts" / "run_reconciler.py",
        CONTROL_PLANE / "tests" / "test_ordinary_chat_chaos.py",
        CONTROL_PLANE / "ai-system" / "mcp" / "package.json",
        REPO_ROOT / "skills" / "ordinary-chat-agent-router" / "SKILL.md",
    ]


def _build_pack(zip_path: pathlib.Path, extras: list[pathlib.Path] | None = None) -> dict[str, str]:
    files = _required_pack_files() + list(extras or [])
    manifest: dict[str, str] = {}
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            if not path.is_file():
                raise GateError(f"required_pack_file_missing:{path.relative_to(REPO_ROOT)}")
            rel = path.relative_to(REPO_ROOT).as_posix()
            archive.write(path, rel)
            manifest[rel] = _sha256(path)
    return manifest


def _lane_a05(report: dict[str, Any]) -> None:
    missing = [str(path.relative_to(REPO_ROOT)) for path in _required_pack_files() if not path.is_file()]
    _append(report, "required_files", not missing, missing=missing)
    if missing:
        return
    with tempfile.TemporaryDirectory() as temp:
        zip_path = pathlib.Path(temp) / "pack.zip"
        manifest = _build_pack(zip_path)
        _append(report, "zip_created", zip_path.is_file() and zip_path.stat().st_size > 0, size=zip_path.stat().st_size)
        with zipfile.ZipFile(zip_path, "r") as archive:
            names = sorted(archive.namelist())
            bad = archive.testzip()
        _append(report, "zip_roundtrip", bad is None and names == sorted(manifest), bad_member=bad)
        _append(report, "sha256_manifest", len(manifest) == len(names), entries=len(manifest))


def _lane_a06(report: dict[str, Any]) -> None:
    node = _run(["node", "--version"], cwd=MCP_DIR, timeout=30)
    _append_run(report, "node_available", node)
    version_text = node.get("stdout_tail", "").strip().lstrip("v")
    major = int(version_text.split(".", 1)[0]) if version_text and version_text.split(".", 1)[0].isdigit() else 0
    _append(report, "node_20_plus", major >= 20, observed=version_text)
    install = _run(["npm", "install", "--no-audit", "--no-fund"], cwd=MCP_DIR, timeout=240)
    _append_run(report, "mcp_dependency_install", install)
    if install.get("ok"):
        _append_run(report, "mcp_check", _run(["npm", "run", "check"], cwd=MCP_DIR, timeout=240))
    package = _json_load(MCP_DIR / "package.json")
    _append(report, "mcp_v2_packages", "@modelcontextprotocol/server" in package.get("dependencies", {}) and "@modelcontextprotocol/client" in package.get("devDependencies", {}))
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in (MCP_DIR / "src").glob("*.ts"))
    _append(report, "protocol_2026_07_28", "2026-07-28" in source_text)


def _lane_a07(report: dict[str, Any]) -> None:
    text = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
    uses = re.findall(r"^\s*-?\s*uses:\s*([^\s]+)", text, flags=re.MULTILINE)
    pinned = bool(uses) and all(re.fullmatch(r"[^@]+@[0-9a-f]{40}", item) for item in uses)
    _append(report, "pinned_actions", pinned, uses=uses)
    _append(report, "no_latest_in_relay_workflow", "@latest" not in text)
    _append(report, "no_request_command_field", "command" not in ALLOWED_REQUEST_KEYS)
    _append(report, "request_has_no_env_override", "env" not in ALLOWED_REQUEST_KEYS and "environment" not in ALLOWED_REQUEST_KEYS)


def _lane_a08(report: dict[str, Any]) -> None:
    config = _json_load(CONFIG)
    relay = config.get("relay", {})
    _append(report, "local_device_not_required", relay.get("localDeviceRequired") is False)
    _append(report, "work_or_codex_not_required", relay.get("workOrCodexRequired") is False)
    workflow_text = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
    _append(report, "workflow_independent_of_chat_work_agent", "CHAT_WORK_AGENT_PATH" not in workflow_text)
    _append(report, "workflow_independent_of_claude", "CLAUDE_PATH" not in workflow_text)


def _lane_a09(report: dict[str, Any]) -> None:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    sha = os.environ.get("GITHUB_SHA", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    _append(report, "repository_identity", repo == "xq22115/ai-thinking-debate-skills-lab", observed=repo)
    _append(report, "github_sha", bool(re.fullmatch(r"[0-9a-f]{40}", sha)), observed=sha)
    _append(report, "github_run_id", run_id.isdigit(), observed=run_id)
    _append(report, "proof_metadata", bool(report.get("goal_sha256") and report.get("generated_at_unix")))


def _scan_secrets(paths: list[pathlib.Path]) -> list[str]:
    findings: list[str] = []
    for root in paths:
        candidates = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
        for path in candidates:
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    findings.append(str(path.relative_to(REPO_ROOT)))
                    break
    return sorted(set(findings))


def _unsafe_python_execution(path: pathlib.Path) -> list[str]:
    """Detect executable AST constructs, not detector strings/comments in source."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id in {"eval", "exec"}:
            findings.append(func.id)
        if (
            isinstance(func, ast.Attribute)
            and func.attr == "system"
            and isinstance(func.value, ast.Name)
            and func.value.id == "os"
        ):
            findings.append("os.system")
        for keyword in node.keywords:
            if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                findings.append("shell_true")
    return sorted(set(findings))


def _lane_a10(report: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory() as temp:
        bad = pathlib.Path(temp) / "bad.json"
        bad.write_text(json.dumps({
            "schemaVersion": 1,
            "request_id": "bad-command",
            "goal": "prove readiness",
            "intent": "ordinary_chat_immediate_use",
            "mode": "prove-ready",
            "requested_completion_methods": REQUIRED_METHODS,
            "command": "echo should-not-run",
        }), encoding="utf-8")
        _, failures = validate_request(bad)
        _append(report, "negative_request_command_rejected", any(item.startswith("request_unknown_fields") for item in failures), failures=failures)
    unsafe = _unsafe_python_execution(pathlib.Path(__file__))
    _append(report, "no_shell_true", "shell_true" not in unsafe, findings=unsafe)
    _append(report, "no_os_system", "os.system" not in unsafe, findings=unsafe)
    _append(report, "no_eval_exec", "eval" not in unsafe and "exec" not in unsafe, findings=unsafe)
    workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
    _append(report, "workflow_no_user_shell_expression", "request.command" not in workflow and "inputs.command" not in workflow)
    findings = _scan_secrets([
        CONTROL_PLANE / "scripts",
        CONTROL_PLANE / "ai-system" / "configs",
        CONTROL_PLANE / "ai-system" / "mcp",
        REPO_ROOT / "skills" / "ordinary-chat-agent-router",
    ])
    _append(report, "secret_prefix_scan", not findings, findings=findings)


LANE_FUNCS = {
    "A01": _lane_a01,
    "A02": _lane_a02,
    "A03": _lane_a03,
    "A04": _lane_a04,
    "A05": _lane_a05,
    "A06": _lane_a06,
    "A07": _lane_a07,
    "A08": _lane_a08,
    "A09": _lane_a09,
    "A10": _lane_a10,
}


def run_lane(lane: str, request_path: pathlib.Path, output: pathlib.Path) -> int:
    request, failures = validate_request(request_path)
    report = _base_report(lane, request)
    try:
        if lane == "A01":
            _lane_a01(report, request_path, request, failures)
        else:
            _append(report, "request_valid", not failures, failures=failures)
            if not failures:
                LANE_FUNCS[lane](report)
    except Exception as exc:  # evidence must survive an unexpected verifier failure
        _append(report, "lane_exception", False, exception=type(exc).__name__, message=str(exc)[:500])
    _write_json(output, report)
    return 0 if report["result"] == "PASS" else 1


def aggregate(request_path: pathlib.Path, reports_dir: pathlib.Path, output_dir: pathlib.Path) -> int:
    request, request_failures = validate_request(request_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    lane_reports: dict[str, dict[str, Any]] = {}
    for lane in LANES:
        matches = list(reports_dir.rglob(f"{lane}.json"))
        if len(matches) == 1:
            try:
                lane_reports[lane] = _json_load(matches[0])
            except Exception as exc:
                lane_reports[lane] = {"lane": lane, "result": "FAIL", "reason": f"report_unreadable:{type(exc).__name__}"}
        else:
            lane_reports[lane] = {"lane": lane, "result": "FAIL", "reason": f"report_count:{len(matches)}"}

    config = _json_load(CONFIG)
    methods: list[dict[str, Any]] = []
    for method in config.get("completionMethods", []):
        lane_ids = method.get("lanes", []) if isinstance(method, dict) else []
        lane_results = {lane: lane_reports.get(lane, {}).get("result") for lane in lane_ids}
        ok = bool(lane_ids) and all(value == "PASS" for value in lane_results.values())
        methods.append({
            "id": method.get("id"),
            "name": method.get("name"),
            "lanes": lane_results,
            "result": "PASS" if ok else "FAIL",
        })

    all_lanes_pass = all(lane_reports[lane].get("result") == "PASS" for lane in LANES)
    all_methods_pass = len(methods) == 5 and all(method["result"] == "PASS" for method in methods)
    overall = "PASS" if not request_failures and all_lanes_pass and all_methods_pass else "FAIL"
    report = {
        "schemaVersion": 1,
        "request_id": request.get("request_id"),
        "goal": request.get("goal"),
        "goal_sha256": hashlib.sha256(str(request.get("goal", "")).encode("utf-8")).hexdigest(),
        "github_repository": os.environ.get("GITHUB_REPOSITORY"),
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "generated_at_unix": int(time.time()),
        "completion_methods": methods,
        "completion_methods_passed": sum(1 for item in methods if item["result"] == "PASS"),
        "lanes_passed": sum(1 for item in lane_reports.values() if item.get("result") == "PASS"),
        "request_failures": request_failures,
        "result": overall,
    }
    _write_json(output_dir / "completion-report.json", report)
    _write_json(output_dir / "lane-reports.json", {"schemaVersion": 1, "lanes": lane_reports})

    extras = [request_path, output_dir / "completion-report.json", output_dir / "lane-reports.json"]
    zip_path = output_dir / "ordinary-chat-v4-use-pack.zip"
    try:
        manifest = _build_pack(zip_path, extras=extras)
        manifest[zip_path.name] = _sha256(zip_path)
    except Exception as exc:
        report["result"] = "FAIL"
        report.setdefault("artifact_failures", []).append(f"pack_build_failed:{type(exc).__name__}:{exc}")
        _write_json(output_dir / "completion-report.json", report)
        manifest = {}

    _write_json(output_dir / "artifact-manifest.json", {"schemaVersion": 1, "sha256": manifest})
    sums = "\n".join(f"{digest}  {name}" for name, digest in sorted(manifest.items())) + ("\n" if manifest else "")
    (output_dir / "SHA256SUMS").write_text(sums, encoding="utf-8")
    readme = f"""# Ordinary Chat v4 — README FIRST\n\nResult: **{report['result']}**\nRequest: `{request.get('request_id')}`\nGitHub run: `{os.environ.get('GITHUB_RUN_ID', '')}`\nGit SHA: `{os.environ.get('GITHUB_SHA', '')}`\n\nThis bundle proves the GitHub-mediated ordinary-chat execution route.\nA PASS requires all five completion methods and all ten verification lanes.\nThe relay does not require Work/Codex or an online local device.\nIt also does not accept arbitrary shell commands from request JSON.\n\nFiles to inspect first:\n1. `completion-report.json`\n2. `lane-reports.json`\n3. `artifact-manifest.json`\n4. `SHA256SUMS`\n"""
    (output_dir / "README-FIRST.md").write_text(readme, encoding="utf-8")
    return 0 if report["result"] == "PASS" and manifest else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    lane = sub.add_parser("lane")
    lane.add_argument("--lane", required=True, choices=LANES)
    lane.add_argument("--request", required=True)
    lane.add_argument("--output", required=True)
    agg = sub.add_parser("aggregate")
    agg.add_argument("--request", required=True)
    agg.add_argument("--reports-dir", required=True)
    agg.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)
    if args.command == "lane":
        return run_lane(args.lane, pathlib.Path(args.request).resolve(), pathlib.Path(args.output).resolve())
    return aggregate(pathlib.Path(args.request).resolve(), pathlib.Path(args.reports_dir).resolve(), pathlib.Path(args.output_dir).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
