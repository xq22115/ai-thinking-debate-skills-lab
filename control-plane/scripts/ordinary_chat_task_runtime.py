#!/usr/bin/env python3
"""Durable declarative task runtime for ordinary-chat GitHub execution.

Requests contain a goal, dependency-aware structured steps, mutation scope, and
acceptance criteria. Requests never carry shell commands. Executable commands come
only from the version-controlled recipe registry.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from typing import Any

REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,79}$")
STEP_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
MUTATING_ACTIONS = {"write_text", "replace_text", "json_set"}
SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{12,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/-]{12,}", re.I),
]


class TaskError(RuntimeError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: pathlib.Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise TaskError(f"invalid JSON {path}: {exc}") from exc


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def redact(text: str, limit: int = 8000) -> str:
    value = text[-limit:]
    for pattern in SECRET_PATTERNS:
        value = pattern.sub("[REDACTED]", value)
    return value


def safe_rel(root: pathlib.Path, raw: str) -> tuple[str, pathlib.Path]:
    if not isinstance(raw, str) or not raw.strip():
        raise TaskError("path must be a non-empty string")
    normalized = raw.replace("\\", "/")
    posix = pathlib.PurePosixPath(normalized)
    if posix.is_absolute() or ".." in posix.parts:
        raise TaskError(f"unsafe path: {raw}")
    rel = posix.as_posix()
    if rel.startswith("./"):
        rel = rel[2:]
    resolved = (root / rel).resolve()
    if resolved != root and root not in resolved.parents:
        raise TaskError(f"path escapes repository: {raw}")
    return rel, resolved


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def excluded_path(path: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
        if pattern.endswith("/**"):
            base = pattern[:-3]
            if path == base or path.startswith(base + "/"):
                return True
    return False


def is_mutation_allowed(path: str, request: dict[str, Any], config: dict[str, Any]) -> bool:
    mutation = request.get("mutation", {})
    requested = mutation.get("allowed_paths", [])
    global_allowed = config["mutation"]["globalAllowedPaths"]
    protected = config["mutation"]["protectedPaths"]
    return bool(requested) and matches(path, requested) and matches(path, global_allowed) and not matches(path, protected)


def snapshot(root: pathlib.Path, config: dict[str, Any]) -> dict[str, str]:
    excluded = config.get("snapshotExclude", [])
    result: dict[str, str] = {}
    for base, dirs, files in os.walk(root):
        base_path = pathlib.Path(base)
        rel_base = base_path.relative_to(root)
        kept_dirs: list[str] = []
        for name in dirs:
            candidate = (rel_base / name).as_posix()
            if candidate.startswith("./"):
                candidate = candidate[2:]
            if not excluded_path(candidate, excluded):
                kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in files:
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            if excluded_path(rel, excluded) or path.is_symlink():
                continue
            try:
                result[rel] = sha256_file(path)
            except OSError:
                continue
    return result


def diff_snapshots(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))


def validate_request(request: Any, config: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise TaskError("request must be an object")
    allowed_top = {"schemaVersion", "request_id", "goal", "intent", "mode", "steps", "acceptance", "mutation", "metadata"}
    extras = sorted(set(request) - allowed_top)
    if extras:
        raise TaskError(f"unsupported top-level fields: {extras}")
    if request.get("schemaVersion") != config["requestSchemaVersion"]:
        raise TaskError("request schemaVersion mismatch")
    if request.get("intent") != config["intent"]:
        raise TaskError("intent mismatch")
    if request.get("mode") not in config["allowedModes"]:
        raise TaskError("unsupported mode")
    request_id = request.get("request_id")
    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id):
        raise TaskError("invalid request_id")
    goal = request.get("goal")
    if not isinstance(goal, str) or len(goal.strip()) < 12:
        raise TaskError("goal is too short")
    steps = request.get("steps")
    if not isinstance(steps, list) or not steps or len(steps) > config["maxSteps"]:
        raise TaskError("steps must be a non-empty bounded list")
    ids: set[str] = set()
    for step in steps:
        if not isinstance(step, dict) or set(step) - {"id", "action", "depends_on", "with"}:
            raise TaskError("each step must use only id/action/depends_on/with")
        step_id = step.get("id")
        if not isinstance(step_id, str) or not STEP_ID_RE.fullmatch(step_id) or step_id in ids:
            raise TaskError(f"invalid or duplicate step id: {step_id}")
        ids.add(step_id)
        action = step.get("action")
        if action not in config["enabledActions"]:
            raise TaskError(f"unsupported action for {step_id}: {action}")
        if request.get("mode") == "audit" and action in MUTATING_ACTIONS:
            raise TaskError(f"audit mode cannot run mutating action: {action}")
        if not isinstance(step.get("with", {}), dict):
            raise TaskError(f"with must be an object for {step_id}")
        deps = step.get("depends_on", [])
        if not isinstance(deps, list) or not all(isinstance(dep, str) for dep in deps):
            raise TaskError(f"depends_on must be a string list for {step_id}")
    for step in steps:
        unknown = sorted(set(step.get("depends_on", [])) - ids)
        if unknown:
            raise TaskError(f"unknown dependencies for {step['id']}: {unknown}")
    acceptance = request.get("acceptance")
    if not isinstance(acceptance, list) or not acceptance:
        raise TaskError("acceptance must be a non-empty list")
    mutation = request.get("mutation", {})
    if not isinstance(mutation, dict) or set(mutation) - {"required", "commit", "allowed_paths"}:
        raise TaskError("invalid mutation policy")
    if not isinstance(mutation.get("required", False), bool) or not isinstance(mutation.get("commit", False), bool):
        raise TaskError("mutation.required and mutation.commit must be booleans")
    allowed_paths = mutation.get("allowed_paths", [])
    if not isinstance(allowed_paths, list) or not all(isinstance(path, str) for path in allowed_paths):
        raise TaskError("mutation.allowed_paths must be a string list")
    if request.get("mode") == "audit" and (mutation.get("required") or mutation.get("commit")):
        raise TaskError("audit mode cannot require or commit mutations")
    return request


def allowed_fetch_url(url: str, config: dict[str, Any]) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise TaskError("fetch_url requires credential-free https URL")
    host = parsed.hostname.lower()
    if host not in config["fetch"]["allowedHosts"]:
        raise TaskError(f"fetch host is not allowed: {host}")
    return parsed


def filtered_env(config: dict[str, Any]) -> dict[str, str]:
    return {key: os.environ[key] for key in config["recipes"]["passEnv"] if key in os.environ}


def run_recipe(name: str, root: pathlib.Path, config: dict[str, Any]) -> dict[str, Any]:
    recipes = config["recipes"]["definitions"]
    if name not in recipes:
        raise TaskError(f"unknown recipe: {name}")
    transcript: list[dict[str, Any]] = []
    for command in recipes[name]["commands"]:
        argv = command.get("argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(v, str) for v in argv):
            raise TaskError(f"invalid recipe argv: {name}")
        cwd_rel, cwd = safe_rel(root, command.get("cwd", "."))
        if not cwd.is_dir():
            raise TaskError(f"recipe cwd missing: {cwd_rel}")
        timeout = int(command.get("timeoutSeconds", config["recipes"]["defaultTimeoutSeconds"]))
        started = time.time()
        proc = subprocess.run(argv, cwd=cwd, env=filtered_env(config), capture_output=True, text=True, timeout=timeout, shell=False)
        item = {
            "argv": argv,
            "cwd": cwd_rel,
            "exit_code": proc.returncode,
            "duration_ms": int((time.time() - started) * 1000),
            "stdout_tail": redact(proc.stdout),
            "stderr_tail": redact(proc.stderr),
        }
        transcript.append(item)
        if proc.returncode != 0:
            raise TaskError(f"recipe {name} failed: {json.dumps(item, ensure_ascii=False)}")
    return {"recipe": name, "commands": transcript}


def json_pointer_set(document: Any, pointer: str, value: Any) -> Any:
    if not pointer.startswith("/"):
        raise TaskError("json_set pointer must start with /")
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
    if not parts or any(not part for part in parts):
        raise TaskError("json_set pointer contains an empty segment")
    if not isinstance(document, dict):
        raise TaskError("json_set currently requires object root")
    cursor = document
    for part in parts[:-1]:
        current = cursor.get(part)
        if current is None:
            cursor[part] = {}
            current = cursor[part]
        if not isinstance(current, dict):
            raise TaskError(f"json_set non-object parent at {part}")
        cursor = current
    cursor[parts[-1]] = value
    return document


def json_pointer_get(document: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise TaskError("JSON pointer must start with /")
    cursor = document
    for raw in pointer[1:].split("/"):
        part = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(cursor, list):
            cursor = cursor[int(part)]
        else:
            cursor = cursor[part]
    return cursor


def execute_step(step: dict[str, Any], root: pathlib.Path, request: dict[str, Any], config: dict[str, Any], output_dir: pathlib.Path) -> dict[str, Any]:
    action = step["action"]
    args = step.get("with", {})
    if action == "read_text":
        rel, path = safe_rel(root, args["path"])
        text = path.read_text(encoding="utf-8")
        limit = min(int(args.get("max_chars", 20000)), config["maxReadChars"])
        return {"path": rel, "sha256": sha256_file(path), "text": redact(text, limit)}
    if action == "search_text":
        pattern = args.get("pattern")
        if not isinstance(pattern, str) or not pattern:
            raise TaskError("search_text requires pattern")
        includes = args.get("include", ["**/*"])
        if not isinstance(includes, list) or not all(isinstance(v, str) for v in includes):
            raise TaskError("search_text include must be a string list")
        regex = re.compile(pattern) if args.get("regex", False) else None
        found: list[dict[str, Any]] = []
        seen: set[str] = set()
        for include in includes:
            for path in root.glob(include):
                if not path.is_file() or path.is_symlink():
                    continue
                rel = path.relative_to(root).as_posix()
                if rel in seen or excluded_path(rel, config.get("snapshotExclude", [])):
                    continue
                seen.add(rel)
                try:
                    if path.stat().st_size > config["maxSearchFileBytes"]:
                        continue
                    lines = path.read_text(encoding="utf-8").splitlines()
                except (UnicodeDecodeError, OSError):
                    continue
                for number, line in enumerate(lines, 1):
                    ok = bool(regex.search(line)) if regex else pattern in line
                    if ok:
                        found.append({"path": rel, "line": number, "text": redact(line, 1000)})
                        if len(found) >= config["maxSearchMatches"]:
                            return {"matches": found, "truncated": True}
        return {"matches": found, "truncated": False}
    if action in MUTATING_ACTIONS:
        rel, path = safe_rel(root, args["path"])
        if not is_mutation_allowed(rel, request, config):
            raise TaskError(f"mutation not allowed: {rel}")
        path.parent.mkdir(parents=True, exist_ok=True)
        before = sha256_file(path) if path.exists() else None
        if action == "write_text":
            content = args.get("content")
            if not isinstance(content, str):
                raise TaskError("write_text content must be a string")
            path.write_text(content, encoding="utf-8")
        elif action == "replace_text":
            find = args.get("find")
            replacement = args.get("replace")
            expected = int(args.get("expected_count", 1))
            if not isinstance(find, str) or not isinstance(replacement, str) or not find:
                raise TaskError("replace_text requires non-empty find and string replace")
            text = path.read_text(encoding="utf-8")
            count = text.count(find)
            if count != expected:
                raise TaskError(f"replace_text expected {expected} occurrence(s), found {count} in {rel}")
            path.write_text(text.replace(find, replacement, expected), encoding="utf-8")
        else:
            document = load_json(path)
            document = json_pointer_set(document, args.get("pointer", ""), args.get("value"))
            write_json(path, document)
        return {"path": rel, "before_sha256": before, "after_sha256": sha256_file(path)}
    if action == "fetch_url":
        url = args.get("url")
        if not isinstance(url, str):
            raise TaskError("fetch_url requires url")
        allowed_fetch_url(url, config)
        req = urllib.request.Request(url, headers={"User-Agent": "ordinary-chat-task-runtime/5.1"})
        with urllib.request.urlopen(req, timeout=config["fetch"]["timeoutSeconds"]) as response:  # noqa: S310
            final_url = response.geturl()
            allowed_fetch_url(final_url, config)
            data = response.read(config["fetch"]["maxBytes"] + 1)
            if len(data) > config["fetch"]["maxBytes"]:
                raise TaskError("fetch_url response exceeds maxBytes")
        artifact = output_dir / "fetch" / f"{step['id']}.bin"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(data)
        return {"url": url, "final_url": final_url, "bytes": len(data), "sha256": sha256_bytes(data), "artifact": artifact.as_posix()}
    if action == "run_recipe":
        name = args.get("recipe")
        if not isinstance(name, str):
            raise TaskError("run_recipe requires recipe")
        return run_recipe(name, root, config)
    raise TaskError(f"unimplemented action: {action}")


def acceptance_checks(request: dict[str, Any], root: pathlib.Path, steps: dict[str, Any], changed_paths: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for index, check in enumerate(request["acceptance"], 1):
        if not isinstance(check, dict) or "type" not in check:
            results.append({"id": index, "result": "FAIL", "detail": "invalid acceptance check"})
            continue
        kind = check["type"]
        ok = False
        detail: Any = None
        try:
            if kind == "step_passed":
                step_id = check["step_id"]
                ok = steps.get(step_id, {}).get("status") in {"PASS", "RESUMED"}
                detail = {"step_id": step_id, "status": steps.get(step_id, {}).get("status")}
            elif kind == "file_exists":
                rel, path = safe_rel(root, check["path"])
                ok = path.is_file()
                detail = rel
            elif kind == "file_contains":
                rel, path = safe_rel(root, check["path"])
                needle = check["text"]
                ok = isinstance(needle, str) and needle in path.read_text(encoding="utf-8")
                detail = rel
            elif kind == "file_sha256":
                rel, path = safe_rel(root, check["path"])
                actual = sha256_file(path)
                ok = actual == check.get("sha256")
                detail = {"path": rel, "actual": actual}
            elif kind == "json_equals":
                rel, path = safe_rel(root, check["path"])
                actual = json_pointer_get(load_json(path), check["pointer"])
                ok = actual == check.get("value")
                detail = {"path": rel, "actual": actual}
            elif kind == "changed_path":
                expected = check["path"]
                ok = expected in changed_paths
                detail = {"expected": expected, "changed_paths": changed_paths}
            elif kind == "no_unexpected_changes":
                expected = sorted(check.get("paths", []))
                ok = sorted(changed_paths) == expected
                detail = {"expected": expected, "actual": changed_paths}
            else:
                detail = f"unknown acceptance type: {kind}"
        except Exception as exc:  # noqa: BLE001
            detail = str(exc)
        results.append({"id": index, "type": kind, "result": "PASS" if ok else "FAIL", "detail": detail})
    return results


def execute(request_path: pathlib.Path, config_path: pathlib.Path, state_path: pathlib.Path, output_path: pathlib.Path, resume_probe: bool) -> dict[str, Any]:
    root = pathlib.Path.cwd().resolve()
    config = load_json(config_path)
    request = validate_request(load_json(request_path), config)
    request_sha = sha256_bytes(canonical_json(request))
    state: dict[str, Any] = {"schemaVersion": 1, "request_sha256": request_sha, "steps": {}}
    if state_path.exists():
        state = load_json(state_path)
        if state.get("request_sha256") != request_sha:
            raise TaskError("state belongs to a different request revision")
    before = snapshot(root, config)
    steps_by_id = {step["id"]: step for step in request["steps"]}
    step_order = [step["id"] for step in request["steps"]]
    pending = set(step_order)
    run_results: dict[str, Any] = {}
    executed = 0
    resumed = 0
    output_dir = output_path.parent
    while pending:
        progress = False
        for step_id in step_order:
            if step_id not in pending:
                continue
            step = steps_by_id[step_id]
            deps = step.get("depends_on", [])
            if any(dep in pending for dep in deps):
                continue
            progress = True
            pending.remove(step_id)
            failed_deps = [dep for dep in deps if run_results.get(dep, {}).get("status") not in {"PASS", "RESUMED"}]
            step_hash = sha256_bytes(canonical_json(step))
            prior = state.get("steps", {}).get(step_id)
            if failed_deps:
                result = {"status": "BLOCKED", "reason": f"failed dependencies: {failed_deps}", "step_hash": step_hash}
            elif prior and prior.get("step_hash") == step_hash and prior.get("status") == "PASS":
                result = dict(prior)
                result["status"] = "RESUMED"
                result["resumed_from_state"] = True
                resumed += 1
            elif prior and prior.get("step_hash") != step_hash:
                result = {"status": "FAIL", "reason": "step changed under the same request_id", "step_hash": step_hash}
            else:
                started = time.time()
                try:
                    evidence = execute_step(step, root, request, config, output_dir)
                    result = {"status": "PASS", "step_hash": step_hash, "duration_ms": int((time.time() - started) * 1000), "evidence": evidence}
                except Exception as exc:  # noqa: BLE001
                    result = {"status": "FAIL", "step_hash": step_hash, "duration_ms": int((time.time() - started) * 1000), "reason": redact(str(exc), 4000)}
                executed += 1
                state.setdefault("steps", {})[step_id] = result
                write_json(state_path, state)
            run_results[step_id] = result
        if not progress:
            for step_id in step_order:
                if step_id in pending:
                    run_results[step_id] = {"status": "FAIL", "reason": "dependency cycle", "step_hash": sha256_bytes(canonical_json(steps_by_id[step_id]))}
            pending.clear()
    after = snapshot(root, config)
    changed_paths = diff_snapshots(before, after)
    if not resume_probe:
        state["primary_changed_paths"] = changed_paths
        write_json(state_path, state)
    acceptance_basis = state.get("primary_changed_paths", changed_paths) if resume_probe else changed_paths
    unexpected = [path for path in changed_paths if not is_mutation_allowed(path, request, config)]
    checks = acceptance_checks(request, root, run_results, acceptance_basis)
    steps_ok = all(item.get("status") in {"PASS", "RESUMED"} for item in run_results.values())
    acceptance_ok = all(item["result"] == "PASS" for item in checks)
    mutation_required = bool(request.get("mutation", {}).get("required", False))
    if resume_probe:
        effect_ok = executed == 0 and resumed == len(steps_by_id) and not changed_paths
    else:
        effect_ok = not mutation_required or bool(changed_paths)
    scope_ok = not unexpected
    result = {
        "schemaVersion": 1,
        "request_id": request["request_id"],
        "request_sha256": request_sha,
        "goal_sha256": sha256_bytes(request["goal"].encode("utf-8")),
        "resume_probe": resume_probe,
        "executed_steps": executed,
        "resumed_steps": resumed,
        "steps": run_results,
        "changed_paths": changed_paths,
        "acceptance_changed_paths_basis": acceptance_basis,
        "unexpected_changes": unexpected,
        "acceptance": checks,
        "proofs": {
            "M1_goal_contract": "PASS",
            "M2_effect_or_execution": "PASS" if effect_ok and scope_ok else "FAIL",
            "M3_outcome_acceptance": "PASS" if acceptance_ok else "FAIL",
            "M5_receipt_integrity": "PASS" if steps_ok and scope_ok and len(run_results) == len(steps_by_id) else "FAIL",
        },
    }
    result["outcome"] = "PASS" if steps_ok and acceptance_ok and effect_ok and scope_ok else "FAIL"
    write_json(output_path, result)
    return result


def adjudicate(request_path: pathlib.Path, primary_path: pathlib.Path, resume_path: pathlib.Path, output_path: pathlib.Path) -> dict[str, Any]:
    request = load_json(request_path)
    primary = load_json(primary_path)
    resume = load_json(resume_path)
    step_count = len(request.get("steps", []))
    same_request = primary.get("request_sha256") == resume.get("request_sha256")
    m4 = (
        resume.get("outcome") == "PASS"
        and resume.get("resume_probe") is True
        and resume.get("executed_steps") == 0
        and resume.get("resumed_steps") == step_count
        and resume.get("changed_paths") == []
        and same_request
    )
    methods = {
        "M1_goal_contract": primary.get("proofs", {}).get("M1_goal_contract") == "PASS",
        "M2_effect_or_execution": primary.get("proofs", {}).get("M2_effect_or_execution") == "PASS",
        "M3_outcome_acceptance": primary.get("proofs", {}).get("M3_outcome_acceptance") == "PASS",
        "M4_durable_resume": m4,
        "M5_receipt_integrity": primary.get("proofs", {}).get("M5_receipt_integrity") == "PASS",
    }
    report = {
        "schemaVersion": 1,
        "request_id": request.get("request_id"),
        "request_sha256": primary.get("request_sha256"),
        "goal_sha256": primary.get("goal_sha256"),
        "completion_methods": {name: "PASS" if passed else "FAIL" for name, passed in methods.items()},
        "completion_methods_passed": sum(methods.values()),
        "changed_paths": primary.get("changed_paths", []),
        "primary_outcome": primary.get("outcome"),
        "resume_outcome": resume.get("outcome"),
        "result": "PASS" if all(methods.values()) and primary.get("outcome") == "PASS" else "FAIL",
    }
    write_json(output_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("execute")
    run.add_argument("--request", required=True)
    run.add_argument("--config", required=True)
    run.add_argument("--state", required=True)
    run.add_argument("--output", required=True)
    run.add_argument("--resume-probe", action="store_true")
    judge = sub.add_parser("adjudicate")
    judge.add_argument("--request", required=True)
    judge.add_argument("--primary", required=True)
    judge.add_argument("--resume", required=True)
    judge.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.command == "execute":
            result = execute(pathlib.Path(args.request), pathlib.Path(args.config), pathlib.Path(args.state), pathlib.Path(args.output), args.resume_probe)
        else:
            result = adjudicate(pathlib.Path(args.request), pathlib.Path(args.primary), pathlib.Path(args.resume), pathlib.Path(args.output))
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
        return 0 if result.get("outcome", result.get("result")) == "PASS" else 1
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"result": "FAIL", "error": redact(str(exc), 4000)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
