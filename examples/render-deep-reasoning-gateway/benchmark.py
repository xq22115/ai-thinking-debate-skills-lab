#!/usr/bin/env python3
import argparse
import json
import statistics
import time
from pathlib import Path
from typing import Any

import httpx

DEFAULT_CASES = [
    {
        "id": "bat-ball",
        "prompt": "A bat and a ball cost $1.10 total. The bat costs $1.00 more than the ball. What does the ball cost? Explain briefly.",
        "expected_any": ["$0.05", "5 cents", "five cents"],
    },
    {
        "id": "decimal-order",
        "prompt": "Which number is larger, 9.11 or 9.9? Explain why in one or two sentences.",
        "expected_any": ["9.9"],
    },
    {
        "id": "logic",
        "prompt": "All bloops are razzies. No razzies are lazzies. Can any bloop be a lazzy? Give the logical conclusion and reason.",
        "expected_any": ["no", "cannot"],
    },
]


def load_cases(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return DEFAULT_CASES
    return json.loads(Path(path).read_text(encoding="utf-8"))


def heuristic_score(answer: str, expected_any: list[str]) -> float:
    lowered = answer.lower()
    return 1.0 if any(term.lower() in lowered for term in expected_any) else 0.0


def reasoning_tokens(payload: dict[str, Any]) -> int:
    total = 0
    for item in payload.get("passes", []):
        usage = item.get("usage") or {}
        details = usage.get("output_tokens_details") or {}
        value = details.get("reasoning_tokens")
        if isinstance(value, int):
            total += value
    return total


def call_gateway(client: httpx.Client, url: str, token: str, prompt: str, config: dict[str, Any]) -> dict[str, Any]:
    response = client.post(
        f"{url.rstrip('/')}/v1/think",
        headers={"Authorization": f"Bearer {token}"},
        json={"prompt": prompt, **config},
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare baseline and deep gateway configurations.")
    parser.add_argument("--url", required=True, help="Render gateway base URL")
    parser.add_argument("--token", required=True, help="GATEWAY_TOKEN")
    parser.add_argument("--cases", help="Optional JSON array of benchmark cases")
    parser.add_argument("--output", default="benchmark-results.json")
    args = parser.parse_args()

    cases = load_cases(args.cases)
    configs = {
        "baseline": {"strategy": "single", "effort": "medium", "mode": "standard"},
        "deep": {"strategy": "deep", "effort": "max", "mode": "pro"},
    }
    rows: list[dict[str, Any]] = []

    with httpx.Client(timeout=6000.0) as client:
        for case in cases:
            for label, config in configs.items():
                started = time.perf_counter()
                payload = call_gateway(client, args.url, args.token, case["prompt"], config)
                wall_ms = int((time.perf_counter() - started) * 1000)
                rows.append(
                    {
                        "case_id": case["id"],
                        "config": label,
                        "wall_ms": wall_ms,
                        "gateway_ms": payload.get("total_elapsed_ms"),
                        "pass_count": len(payload.get("passes", [])),
                        "reasoning_tokens": reasoning_tokens(payload),
                        "heuristic_score": heuristic_score(payload.get("answer", ""), case.get("expected_any", [])),
                        "answer": payload.get("answer", ""),
                    }
                )

    summary: dict[str, Any] = {}
    for label in configs:
        selected = [row for row in rows if row["config"] == label]
        summary[label] = {
            "median_wall_ms": statistics.median(row["wall_ms"] for row in selected),
            "mean_quality_score": statistics.mean(row["heuristic_score"] for row in selected),
            "mean_reasoning_tokens": statistics.mean(row["reasoning_tokens"] for row in selected),
            "mean_pass_count": statistics.mean(row["pass_count"] for row in selected),
        }

    baseline = summary["baseline"]
    deep = summary["deep"]
    summary["read_back"] = {
        "more_model_work_observed": deep["mean_pass_count"] > baseline["mean_pass_count"],
        "higher_wall_time_observed": deep["median_wall_ms"] > baseline["median_wall_ms"],
        "reasoning_tokens_increased": deep["mean_reasoning_tokens"] > baseline["mean_reasoning_tokens"],
        "quality_non_regression_on_cases": deep["mean_quality_score"] >= baseline["mean_quality_score"],
        "note": "Heuristic quality is a smoke test only; use a larger blinded eval set for production decisions.",
    }

    result = {"summary": summary, "rows": rows}
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
