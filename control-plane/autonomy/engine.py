#!/usr/bin/env python3
"""Evidence-bound autonomous learning and debugging primitives.

This module intentionally uses only the Python standard library so the same
logic can run locally and inside GitHub Actions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

VOLATILE_PATTERNS = [
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I), "<uuid>"),
    (re.compile(r"\b0x[0-9a-f]+\b", re.I), "<addr>"),
    (re.compile(r"\b[0-9a-f]{12,64}\b", re.I), "<hex>"),
    (re.compile(r"\b\d{4}-\d{2}-\d{2}[T ][0-9:.+-]+Z?\b", re.I), "<time>"),
    (re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?(?![A-Za-z])"), "<n>"),
    (re.compile(r"[/\\](?:Users|home|tmp|var|private|workspace)[/\\][^\s:]+", re.I), "<path>"),
]

PIVOT_DIMENSIONS = {
    "hypothesis",
    "mechanism",
    "diagnostic_instrument",
    "environment",
    "verification_method",
}


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_failure(text: str) -> str:
    value = text.strip().lower()
    for pattern, replacement in VOLATILE_PATTERNS:
        value = pattern.sub(replacement, value)
    value = re.sub(r"\s+", " ", value)
    return value


def failure_fingerprint(text: str, prefix_length: int = 24) -> str:
    normalized = normalize_failure(text)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return digest[:prefix_length]


def verified_evidence(evidence: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [e for e in evidence if bool(e.get("verified")) and e.get("verdict", "support") == "support"]


def contradiction_evidence(evidence: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [e for e in evidence if bool(e.get("verified")) and e.get("verdict") == "contradict"]


def score_candidate(candidate: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    evidence = list(candidate.get("evidence") or [])
    support = verified_evidence(evidence)
    contradictions = contradiction_evidence(evidence)
    independent_groups = {
        str(e.get("independent_group") or e.get("source") or "")
        for e in support
        if (e.get("independent_group") or e.get("source"))
    }

    total_verified = len(support) + len(contradictions)
    contradiction_ratio = len(contradictions) / total_verified if total_verified else 1.0

    # Beta(1,1) posterior mean. Deterministic and deliberately conservative.
    confidence = (len(support) + 1) / (len(support) + len(contradictions) + 2)

    policy = config["promotion"]
    reasons: list[str] = []
    if len(support) < int(policy["min_verified_support"]):
        reasons.append("insufficient_verified_support")
    if len(independent_groups) < int(policy["min_independent_groups"]):
        reasons.append("insufficient_independent_groups")
    if confidence < float(policy["min_confidence"]):
        reasons.append("confidence_below_threshold")
    if contradiction_ratio > float(policy["max_contradiction_ratio"]):
        reasons.append("contradiction_ratio_too_high")

    required = config.get("required_lesson_fields", [])
    missing = [field for field in required if not candidate.get(field)]
    if missing:
        reasons.append("missing_required_fields:" + ",".join(missing))

    return {
        "promotable": not reasons,
        "confidence": round(confidence, 6),
        "verified_support": len(support),
        "verified_contradictions": len(contradictions),
        "independent_groups": sorted(independent_groups),
        "contradiction_ratio": round(contradiction_ratio, 6),
        "reasons": reasons,
    }


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    rows: list[dict[str, Any]] = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{p}:{i}: invalid JSON: {exc}") from exc
    return rows


def append_jsonl(path: str | Path, row: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def promote_candidate(candidate: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    assessment = score_candidate(candidate, config)
    promoted = dict(candidate)
    promoted["assessment"] = assessment
    promoted["status"] = "active" if assessment["promotable"] else "candidate"
    promoted["confidence"] = assessment["confidence"]
    return promoted


def lesson_rank(
    lesson: dict[str, Any],
    fingerprint: str | None,
    component: str | None,
    terms: Iterable[str],
) -> float:
    if lesson.get("status") != "active":
        return -1.0
    score = 0.0
    if fingerprint and lesson.get("fingerprint") == fingerprint:
        score += 10.0
    if component and str(lesson.get("component", "")).lower() == component.lower():
        score += 3.0

    haystack = " ".join(
        str(lesson.get(k, ""))
        for k in ("title", "root_cause", "diagnostic", "repair", "component")
    ).lower()
    for term in {t.lower() for t in terms if t}:
        if term in haystack:
            score += 1.0
    score += float(lesson.get("confidence", 0.0))
    return score


def query_lessons(
    lessons: Iterable[dict[str, Any]],
    fingerprint: str | None = None,
    component: str | None = None,
    terms: Iterable[str] = (),
    limit: int = 5,
) -> list[dict[str, Any]]:
    ranked = [
        (lesson_rank(item, fingerprint, component, terms), item)
        for item in lessons
    ]
    ranked = [pair for pair in ranked if pair[0] >= 0]
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [dict(item, retrieval_score=round(score, 6)) for score, item in ranked[:limit]]


def next_strategy(run_state: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    attempts = list(run_state.get("attempts") or [])
    if not attempts:
        return {"pivot_required": False, "reason": "no_prior_attempt"}

    current_mechanism = attempts[-1].get("mechanism")
    consecutive = 0
    for attempt in reversed(attempts):
        if attempt.get("mechanism") == current_mechanism and attempt.get("outcome") != "pass":
            consecutive += 1
        else:
            break

    limit = int(config["debugging"]["same_mechanism_strike_limit"])
    pivot_required = consecutive >= limit
    return {
        "pivot_required": pivot_required,
        "same_mechanism_failures": consecutive,
        "mechanism": current_mechanism,
        "allowed_pivot_dimensions": sorted(PIVOT_DIMENSIONS),
        "reason": "two_strike_rule" if pivot_required else "mechanism_retry_still_allowed",
    }


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        promotion = config["promotion"]
        if int(promotion["min_verified_support"]) < 1:
            errors.append("min_verified_support must be >= 1")
        if int(promotion["min_independent_groups"]) < 1:
            errors.append("min_independent_groups must be >= 1")
        if not 0 <= float(promotion["min_confidence"]) <= 1:
            errors.append("min_confidence must be in [0,1]")
        if not 0 <= float(promotion["max_contradiction_ratio"]) <= 1:
            errors.append("max_contradiction_ratio must be in [0,1]")
        limit = int(config["debugging"]["same_mechanism_strike_limit"])
        if limit < 1:
            errors.append("same_mechanism_strike_limit must be >= 1")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid config structure: {exc}")
    return errors


def cli() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p_fp = sub.add_parser("fingerprint")
    p_fp.add_argument("--text")
    p_fp.add_argument("--file")
    p_fp.add_argument("--prefix-length", type=int, default=24)

    p_cfg = sub.add_parser("validate-config")
    p_cfg.add_argument("--config", required=True)

    p_eval = sub.add_parser("evaluate-candidate")
    p_eval.add_argument("--candidate", required=True)
    p_eval.add_argument("--config", required=True)

    p_promote = sub.add_parser("promote")
    p_promote.add_argument("--candidate", required=True)
    p_promote.add_argument("--config", required=True)
    p_promote.add_argument("--store", required=True)

    p_query = sub.add_parser("query")
    p_query.add_argument("--store", required=True)
    p_query.add_argument("--fingerprint")
    p_query.add_argument("--component")
    p_query.add_argument("--term", action="append", default=[])
    p_query.add_argument("--limit", type=int, default=5)

    p_next = sub.add_parser("next-strategy")
    p_next.add_argument("--state", required=True)
    p_next.add_argument("--config", required=True)

    args = parser.parse_args()

    if args.command == "fingerprint":
        if bool(args.text) == bool(args.file):
            parser.error("provide exactly one of --text or --file")
        text = args.text if args.text is not None else Path(args.file).read_text(encoding="utf-8")
        print(json.dumps({"fingerprint": failure_fingerprint(text, args.prefix_length), "normalized": normalize_failure(text)}))
        return 0

    if args.command == "validate-config":
        errors = validate_config(load_json(args.config))
        print(json.dumps({"valid": not errors, "errors": errors}))
        return 0 if not errors else 2

    if args.command == "evaluate-candidate":
        result = score_candidate(load_json(args.candidate), load_json(args.config))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["promotable"] else 2

    if args.command == "promote":
        row = promote_candidate(load_json(args.candidate), load_json(args.config))
        append_jsonl(args.store, row)
        print(json.dumps(row, ensure_ascii=False, sort_keys=True))
        return 0 if row["status"] == "active" else 2

    if args.command == "query":
        rows = read_jsonl(args.store)
        print(json.dumps(query_lessons(rows, args.fingerprint, args.component, args.term, args.limit), ensure_ascii=False))
        return 0

    if args.command == "next-strategy":
        print(json.dumps(next_strategy(load_json(args.state), load_json(args.config)), ensure_ascii=False, sort_keys=True))
        return 0

    raise AssertionError("unreachable")


if __name__ == "__main__":
    sys.exit(cli())
