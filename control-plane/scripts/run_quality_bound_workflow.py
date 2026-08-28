#!/usr/bin/env python3
"""Run the local workflow only after binding the continuous-thinking quality profile."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import uuid
from urllib.parse import urlsplit, urlunsplit

try:
    from scripts.continuous_thinking_runtime_binding import bind_preparation
    from scripts.run_local_agent_workflow import run_workflow
except ModuleNotFoundError:
    from continuous_thinking_runtime_binding import bind_preparation
    from run_local_agent_workflow import run_workflow


_BINDING_IDENTITY_FIELDS = (
    "bound",
    "profile_id",
    "profile_sha256",
    "task_class",
    "reasoning_effort",
    "profile_path",
)
_DEEP_TASK_CLASSES = {"material", "critical"}
_RESEARCH_ACTOR = "A03"
_REQUIRED_RESEARCH_TOOLS = {"WebSearch", "WebFetch"}
_THINKING_DISABLE_ENV = (
    "CLAUDE_CODE_DISABLE_THINKING",
    "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING",
    "MAX_THINKING_TOKENS",
)


def _binding_identity(payload: dict) -> dict[str, object]:
    binding = payload.get("quality_profile_binding")
    if not isinstance(binding, dict):
        raise ValueError("quality_binding_evidence_invalid")
    return {field: binding.get(field) for field in _BINDING_IDENTITY_FIELDS}


def _verify_resume_binding(evidence_path: pathlib.Path, bound: dict) -> None:
    if not evidence_path.is_file():
        raise ValueError("resume_quality_binding_evidence_missing")
    try:
        prior = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("resume_quality_binding_evidence_invalid") from exc
    if not isinstance(prior, dict):
        raise ValueError("resume_quality_binding_evidence_invalid")
    if _binding_identity(prior) != _binding_identity(bound):
        raise ValueError("resume_quality_binding_mismatch")


def _fresh_research_audit_dir(output: pathlib.Path) -> pathlib.Path:
    path = output / "research-tool-audit" / uuid.uuid4().hex
    path.mkdir(parents=True, exist_ok=False)
    return path.resolve()


def _read_research_receipts(audit_dir: pathlib.Path, actor_id: str) -> list[dict]:
    actor_dir = audit_dir / actor_id
    if not actor_dir.is_dir():
        return []
    receipts: list[dict] = []
    for path in sorted(actor_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            row = dict(payload)
            row["receipt_file"] = str(path)
            receipts.append(row)
    return receipts


def _normalize_query(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _normalize_url(value: object) -> str:
    text = str(value or "").strip()
    if not text.startswith(("http://", "https://")):
        return ""
    parts = urlsplit(text)
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def _receipt_is_accepted_for_effort(row: dict, expected_effort: str) -> bool:
    return (
        row.get("schemaVersion") == 2
        and row.get("quality_evidence_accepted") is True
        and row.get("post_tool_success") is True
        and row.get("hook_event_name") == "PostToolUse"
        and row.get("actor_id") == _RESEARCH_ACTOR
        and row.get("requested_effort") == expected_effort
        and row.get("effective_effort") == expected_effort
        and row.get("effort_readback_source") in {"hook_payload", "CLAUDE_EFFORT"}
        and isinstance(row.get("recorded_at_ns"), int)
        and row.get("recorded_at_ns", 0) > 0
    )


def _research_cycle_state(receipts: list[dict]) -> tuple[dict[str, object], list[str]]:
    rows = sorted(receipts, key=lambda row: int(row["recorded_at_ns"]))
    searches = [
        row for row in rows
        if row.get("tool_name") == "WebSearch" and _normalize_query(row.get("query"))
    ]
    fetches = [
        row for row in rows
        if row.get("tool_name") == "WebFetch" and _normalize_url(row.get("url"))
    ]
    state: dict[str, object] = {
        "discover_search": False,
        "initial_inspection": False,
        "distinct_challenge_search": False,
        "distinct_followup_inspection": False,
        "complete": False,
    }
    failures: list[str] = []
    if not searches:
        failures.append("research_cycle_discover_search_missing:A03")
        return state, failures
    state["discover_search"] = True

    first_search = searches[0]
    initial_fetches = [
        row for row in fetches
        if int(row["recorded_at_ns"]) > int(first_search["recorded_at_ns"])
    ]
    if not initial_fetches:
        failures.append("research_cycle_initial_inspection_missing:A03")
        return state, failures
    state["initial_inspection"] = True

    first_fetch = initial_fetches[0]
    prior_queries = {
        _normalize_query(row.get("query"))
        for row in searches
        if int(row["recorded_at_ns"]) <= int(first_fetch["recorded_at_ns"])
    }
    challenge_searches = [
        row for row in searches
        if int(row["recorded_at_ns"]) > int(first_fetch["recorded_at_ns"])
        and _normalize_query(row.get("query")) not in prior_queries
    ]
    if not challenge_searches:
        failures.append("research_cycle_distinct_challenge_search_missing:A03")
        return state, failures
    state["distinct_challenge_search"] = True

    challenge = challenge_searches[0]
    prior_urls = {
        _normalize_url(row.get("url"))
        for row in fetches
        if int(row["recorded_at_ns"]) < int(challenge["recorded_at_ns"])
    }
    followup_fetches = [
        row for row in fetches
        if int(row["recorded_at_ns"]) > int(challenge["recorded_at_ns"])
        and _normalize_url(row.get("url")) not in prior_urls
    ]
    if not followup_fetches:
        failures.append("research_cycle_distinct_followup_inspection_missing:A03")
        return state, failures
    state["distinct_followup_inspection"] = True
    state["complete"] = True
    return state, failures


def _research_attestation(
    result: dict[str, object],
    task_class: str,
    audit_dir: pathlib.Path,
    expected_effort: str,
) -> tuple[dict[str, object], list[str]]:
    receipts = _read_research_receipts(audit_dir, _RESEARCH_ACTOR)
    accepted_receipts = [
        row for row in receipts if _receipt_is_accepted_for_effort(row, expected_effort)
    ]
    observed_tools = {
        str(row.get("tool_name") or "")
        for row in accepted_receipts
    }
    cycle_state, cycle_failures = _research_cycle_state(accepted_receipts)
    attestation: dict[str, object] = {
        "schemaVersion": 3,
        "required": task_class in _DEEP_TASK_CLASSES,
        "actor_id": _RESEARCH_ACTOR,
        "expected_effort": expected_effort,
        "required_tools": sorted(_REQUIRED_RESEARCH_TOOLS) if task_class in _DEEP_TASK_CLASSES else [],
        "observed_tools": sorted(observed_tools),
        "receipt_count": len(receipts),
        "accepted_receipt_count": len(accepted_receipts),
        "observed_effective_efforts": sorted({
            str(row.get("effective_effort") or "") for row in accepted_receipts
        }),
        "falsification_cycle": cycle_state,
        "audit_dir": str(audit_dir),
        "fresh_audit_per_run": True,
        "result": "NOT_REQUIRED" if task_class not in _DEEP_TASK_CLASSES else "NOT_EVALUATED",
    }
    if task_class not in _DEEP_TASK_CLASSES:
        return attestation, []
    if result.get("result") != "PASS":
        attestation["result"] = "NOT_EVALUATED"
        attestation["reason"] = "workflow_not_pass"
        return attestation, []

    failures: list[str] = []
    executions = result.get("executions")
    if not isinstance(executions, dict):
        failures.append(f"research_execution_missing:{_RESEARCH_ACTOR}")
    else:
        execution = executions.get(_RESEARCH_ACTOR)
        if not isinstance(execution, dict):
            failures.append(f"research_execution_missing:{_RESEARCH_ACTOR}")
        else:
            decision = execution.get("decision")
            if not isinstance(decision, dict) or decision.get("decision") != "PASS":
                failures.append(f"research_actor_not_pass:{_RESEARCH_ACTOR}")
            else:
                quality = decision.get("reasoning_quality")
                if not isinstance(quality, dict):
                    failures.append(f"research_reasoning_quality_missing:{_RESEARCH_ACTOR}")
                elif quality.get("research_stop_reason") != "decision_saturated":
                    failures.append(f"research_not_decision_saturated:{_RESEARCH_ACTOR}")

    for row in receipts:
        tool = str(row.get("tool_name") or "")
        if not _receipt_is_accepted_for_effort(row, expected_effort):
            failures.append(f"research_receipt_not_effort_attested:{_RESEARCH_ACTOR}:{tool or 'unknown'}")
            continue
        if tool == "WebSearch" and not str(row.get("query") or "").strip():
            failures.append(f"web_search_query_missing:{_RESEARCH_ACTOR}")
        if tool == "WebFetch" and not str(row.get("url") or "").startswith(("http://", "https://")):
            failures.append(f"web_fetch_url_missing:{_RESEARCH_ACTOR}")
        if not str(row.get("tool_use_id") or "").strip():
            failures.append(f"research_tool_use_id_missing:{_RESEARCH_ACTOR}:{tool}")

    missing_tools = sorted(_REQUIRED_RESEARCH_TOOLS - observed_tools)
    failures.extend(
        f"successful_tool_receipt_missing:{_RESEARCH_ACTOR}:{tool}"
        for tool in missing_tools
    )
    failures.extend(cycle_failures)

    failures = sorted(set(failures))
    attestation["result"] = "PASS" if not failures else "FAIL"
    attestation["failures"] = failures
    return attestation, failures


def _restore_environment(previous: dict[str, str | None]) -> None:
    for key, value in previous.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def run_quality_bound_workflow(
    preparation: dict,
    repo_root: pathlib.Path | str,
    claude_path: pathlib.Path | str,
    output_dir: pathlib.Path | str,
    *,
    task_class: str = "material",
    max_parallel: int = 3,
    timeout_seconds: float = 180.0,
    max_budget_usd: float = 0.05,
    model: str | None = None,
    resume_existing: bool = False,
) -> dict[str, object]:
    bound = bind_preparation(preparation, repo_root, task_class=task_class)
    binding = bound["quality_profile_binding"]
    effort = str(binding.get("reasoning_effort") or "")
    if effort not in {"low", "medium", "high", "xhigh", "max"}:
        raise ValueError(f"quality_reasoning_effort_invalid:{effort}")

    output = pathlib.Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    evidence_path = output / "quality-bound-preparation.json"
    if resume_existing:
        _verify_resume_binding(evidence_path, bound)
    evidence_path.write_text(
        json.dumps(bound, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    audit_dir = _fresh_research_audit_dir(output)

    managed_keys = [
        "CLAUDE_CODE_EFFORT_LEVEL",
        "QUALITY_RESEARCH_AUDIT_DIR",
        "QUALITY_TASK_CLASS",
        *_THINKING_DISABLE_ENV,
    ]
    previous = {key: os.environ.get(key) for key in managed_keys}
    cleared_disablers: list[str] = []
    os.environ["CLAUDE_CODE_EFFORT_LEVEL"] = effort
    os.environ["QUALITY_RESEARCH_AUDIT_DIR"] = str(audit_dir)
    os.environ["QUALITY_TASK_CLASS"] = task_class
    if task_class in _DEEP_TASK_CLASSES:
        for key in _THINKING_DISABLE_ENV:
            value = os.environ.get(key)
            should_clear = (
                (key == "MAX_THINKING_TOKENS" and value == "0")
                or (key != "MAX_THINKING_TOKENS" and value == "1")
            )
            if should_clear:
                os.environ.pop(key, None)
                cleared_disablers.append(key)
    try:
        result = run_workflow(
            bound,
            claude_path,
            output,
            max_parallel=max_parallel,
            timeout_seconds=timeout_seconds,
            max_budget_usd=max_budget_usd,
            model=model,
            resume_existing=resume_existing,
        )
    finally:
        _restore_environment(previous)

    result = dict(result)
    attestation, research_failures = _research_attestation(
        result, task_class, audit_dir, effort
    )
    if research_failures and result.get("result") == "PASS":
        existing = result.get("failures")
        failures = list(existing) if isinstance(existing, list) else []
        failures.extend(research_failures)
        result["failures"] = sorted(set(str(item) for item in failures))
        result["result"] = "FAIL"

    result["quality_profile_binding"] = binding
    result["reasoning_runtime"] = {
        "schemaVersion": 3,
        "task_class": task_class,
        "requested_effort": effort,
        "effort_bound_via_environment": "CLAUDE_CODE_EFFORT_LEVEL",
        "effective_effort_verified_by_research_hook": (
            attestation.get("result") == "PASS" if task_class in _DEEP_TASK_CLASSES else False
        ),
        "adaptive_research_saturation_verified": (
            bool((attestation.get("falsification_cycle") or {}).get("complete"))
            if task_class in _DEEP_TASK_CLASSES else False
        ),
        "thinking_disable_overrides_cleared_for_run": sorted(cleared_disablers),
        "environment_restored_after_run": True,
    }
    result["research_runtime_attestation"] = attestation
    result["delivery_contract"] = {
        "reasoning_and_delivery_are_separate_phases": True,
        "artificial_output_throttling_forbidden": True,
        "slow_streaming_is_not_depth_evidence": True,
        "normal_continuous_delivery_after_release_gate": True,
    }
    (output / "quality-bound-workflow.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preparation-json", required=True)
    parser.add_argument("--repo-root")
    parser.add_argument("--claude-path", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--task-class", choices=["simple", "material", "critical"], default="material")
    parser.add_argument("--max-parallel", type=int, default=3)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--max-budget-usd", type=float, default=0.05)
    parser.add_argument("--model")
    parser.add_argument("--resume-existing", action="store_true")
    args = parser.parse_args(argv)

    preparation = json.loads(pathlib.Path(args.preparation_json).read_text(encoding="utf-8"))
    repo_root = args.repo_root or preparation.get("source_repo") or "."
    result = run_quality_bound_workflow(
        preparation,
        repo_root,
        args.claude_path,
        args.output_dir,
        task_class=args.task_class,
        max_parallel=args.max_parallel,
        timeout_seconds=args.timeout_seconds,
        max_budget_usd=args.max_budget_usd,
        model=args.model,
        resume_existing=args.resume_existing,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("result") == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
