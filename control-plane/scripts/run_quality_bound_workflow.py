#!/usr/bin/env python3
"""Run the local workflow only after binding the continuous-thinking quality profile."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

try:
    from scripts.continuous_thinking_runtime_binding import bind_preparation
    from scripts.run_local_agent_workflow import run_workflow
except ModuleNotFoundError:
    from continuous_thinking_runtime_binding import bind_preparation
    from run_local_agent_workflow import run_workflow


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
    (output / "quality-bound-preparation.json").write_text(
        json.dumps(bound, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
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
    result = dict(result)
    result["quality_profile_binding"] = bound["quality_profile_binding"]
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
