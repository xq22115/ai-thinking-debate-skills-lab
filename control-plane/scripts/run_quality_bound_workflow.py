#!/usr/bin/env python3
"""Run the local workflow only after binding the continuous-thinking quality profile."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

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
    "profile_path",
)
_TASK_EFFORT = {
    "simple": "medium",
    "material": "high",
    "critical": "xhigh",
}
_RESEARCH_REQUIRED_TASK_CLASSES = {"material", "critical"}
_RESEARCH_ACTOR = "A03"


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


def _research_failures(result: dict[str, object], task_class: str) -> list[str]:
    """Require observable research receipts for deep work instead of self-reported depth."""
    if task_class not in _RESEARCH_REQUIRED_TASK_CLASSES or result.get("result") != "PASS":
        return []
    executions = result.get("executions")
    if not isinstance(executions, dict):
        return [f"research_execution_missing:{_RESEARCH_ACTOR}"]
    row = executions.get(_RESEARCH_ACTOR)
    if not isinstance(row, dict):
        return [f"research_execution_missing:{_RESEARCH_ACTOR}"]
    decision = row.get("decision")
    if not isinstance(decision, dict) or decision.get("decision") != "PASS":
        return [f"research_actor_not_pass:{_RESEARCH_ACTOR}"]
    quality = decision.get("reasoning_quality")
    if not isinstance(quality, dict):
        return [f"research_reasoning_quality_missing:{_RESEARCH_ACTOR}"]
    if quality.get("research_stop_reason") != "decision_saturated":
        return [f"research_not_decision_saturated:{_RESEARCH_ACTOR}"]

    evidence = decision.get("evidence")
    if not isinstance(evidence, list):
        return [f"research_evidence_missing:{_RESEARCH_ACTOR}"]
    search_receipts = []
    fetched_sources = []
    for item in evidence:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("kind") or "").strip().lower()
        reference = str(item.get("reference") or "").strip()
        if kind in {"web_search", "websearch", "search"} and reference:
            search_receipts.append(reference)
        if kind in {"web_fetch", "webfetch", "source", "primary_source"} and reference.startswith(("https://", "http://")):
            fetched_sources.append(reference)
    failures: list[str] = []
    if not search_receipts:
        failures.append(f"web_search_receipt_missing:{_RESEARCH_ACTOR}")
    if not fetched_sources:
        failures.append(f"fetched_source_url_missing:{_RESEARCH_ACTOR}")
    return failures


def _apply_research_gate(result: dict[str, object], task_class: str) -> dict[str, object]:
    failures = _research_failures(result, task_class)
    if not failures:
        return result
    gated = dict(result)
    existing = gated.get("failures")
    failure_list = list(existing) if isinstance(existing, list) else []
    failure_list.extend(failures)
    gated["failures"] = sorted(set(str(x) for x in failure_list))
    gated["result"] = "FAIL"
    gated["research_gate"] = {
        "result": "FAIL",
        "actor_id": _RESEARCH_ACTOR,
        "failures": sorted(set(failures)),
    }
    return gated


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
    output = pathlib.Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    evidence_path = output / "quality-bound-preparation.json"
    if resume_existing:
        _verify_resume_binding(evidence_path, bound)
    evidence_path.write_text(
        json.dumps(bound, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    effort = _TASK_EFFORT[task_class]
    prior_effort = os.environ.get("CLAUDE_CODE_EFFORT_LEVEL")
    prior_max_thinking = os.environ.get("MAX_THINKING_TOKENS")
    cleared_thinking_disable = task_class in _RESEARCH_REQUIRED_TASK_CLASSES and prior_max_thinking == "0"
    os.environ["CLAUDE_CODE_EFFORT_LEVEL"] = effort
    if cleared_thinking_disable:
        os.environ.pop("MAX_THINKING_TOKENS", None)
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
        if prior_effort is None:
            os.environ.pop("CLAUDE_CODE_EFFORT_LEVEL", None)
        else:
            os.environ["CLAUDE_CODE_EFFORT_LEVEL"] = prior_effort
        if cleared_thinking_disable:
            os.environ["MAX_THINKING_TOKENS"] = "0"

    result = _apply_research_gate(dict(result), task_class)
    result["quality_profile_binding"] = bound["quality_profile_binding"]
    result["reasoning_runtime"] = {
        "task_class": task_class,
        "effort": effort,
        "thinking_enabled": True,
        "cleared_inherited_max_thinking_tokens_zero": cleared_thinking_disable,
    }
    result["delivery_contract"] = {
        "deliberation_precedes_final_release": True,
        "artificial_wait_forbidden": True,
        "token_drip_as_depth_signal_forbidden": True,
        "progress_updates_require_information_gain": True,
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
