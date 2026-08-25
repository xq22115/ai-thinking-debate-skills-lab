#!/usr/bin/env python3
"""Bind the repository-wide quality profile to prepared runtime assignments."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import pathlib
import sys

PROFILE_RELATIVE_PATH = pathlib.Path("ai-system/configs/continuous-thinking-global.json")
TASK_CLASSES = {"simple", "material", "critical"}
BINDING_START = "[QUALITY_PROFILE_BINDING]"
BINDING_END = "[/QUALITY_PROFILE_BINDING]"


def load_profile(repo_root: pathlib.Path | str) -> tuple[dict, str]:
    path = pathlib.Path(repo_root) / PROFILE_RELATIVE_PATH
    if not path.is_file():
        raise ValueError(f"quality_profile_missing:{path}")
    raw = path.read_bytes()
    try:
        profile = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"quality_profile_invalid:{type(exc).__name__}") from exc
    if not isinstance(profile, dict):
        raise ValueError("quality_profile_not_object")
    if profile.get("default_enabled") is not True:
        raise ValueError("quality_profile_not_default_enabled")
    profile_id = profile.get("profile_id")
    if not isinstance(profile_id, str) or not profile_id.strip():
        raise ValueError("quality_profile_id_missing")
    return profile, hashlib.sha256(raw).hexdigest()


def _reasoning_effort(profile: dict, task_class: str) -> str:
    runtime = profile.get("reasoning_runtime") or {}
    effort = (runtime.get("effort_by_task_class") or {}).get(task_class)
    if effort not in {"low", "medium", "high", "xhigh", "max"}:
        raise ValueError(f"quality_reasoning_effort_missing:{task_class}")
    if runtime.get("effort_must_be_runtime_bound") is not True:
        raise ValueError("quality_reasoning_effort_not_runtime_bound")
    return str(effort)


def build_runtime_directive(profile: dict, profile_sha256: str, task_class: str) -> str:
    if task_class not in TASK_CLASSES:
        raise ValueError(f"quality_task_class_invalid:{task_class}")
    route = (profile.get("depth_router") or {}).get(task_class) or {}
    stages = route.get("required_stages") or []
    pass_requires = (profile.get("release") or {}).get("pass_requires") or []
    research_policy = profile.get("research_and_experience") or {}
    output_delivery = profile.get("output_delivery") or {}
    effort = _reasoning_effort(profile, task_class)
    if not isinstance(stages, list) or not stages:
        raise ValueError(f"quality_route_missing:{task_class}")
    if not isinstance(pass_requires, list) or not pass_requires:
        raise ValueError("quality_release_requirements_missing")
    if research_policy.get("triggered_research_requires_tool_backed_evidence") is not True:
        raise ValueError("quality_research_evidence_gate_missing")
    if output_delivery.get("artificial_output_throttling_forbidden") is not True:
        raise ValueError("quality_output_throttling_guard_missing")
    runtime_attestation = research_policy.get("runtime_attestation") or {}
    deep_tools = runtime_attestation.get("required_successful_tools_for_material_or_critical") or []
    if task_class in {"material", "critical"} and set(deep_tools) != {"WebSearch", "WebFetch"}:
        raise ValueError("quality_deep_research_tool_attestation_missing")

    research_proof = (
        "For material/critical work, A03 must actually execute both WebSearch and WebFetch. "
        "A PostToolUse runtime receipt must attest both successful calls; self-reported sources or elapsed time cannot substitute."
        if task_class in {"material", "critical"}
        else "Use external research only when it can change the decision; never browse ceremonially."
    )
    return "\n".join([
        BINDING_START,
        f"profile_id={profile['profile_id']}",
        f"profile_sha256={profile_sha256}",
        f"task_class={task_class}",
        f"reasoning_effort={effort}",
        "required_stages=" + " -> ".join(str(x) for x in stages),
        "objective=Optimize for first-pass correctness and fewer user correction loops, not artificial delay, output length, source count, or agent count.",
        "preflight=Before material changes reconstruct outcome, current state, scope, dependencies, protected capabilities, failure evidence, acceptance criteria, causal model, and decision-critical unknowns.",
        "research=When fresh knowledge or expert operational experience can change the decision, or the user explicitly asks to search/browse/research/look up/verify current information/deep research, perform actual tool-backed research before release. Use current primary sources plus high-signal practitioner evidence and extract mechanism, preconditions, failure modes, verification, portable lesson, and invalidation condition.",
        "research_gate=A triggered research requirement is satisfied only by observable tool/source evidence. Record the trigger, sources or queries, evidence summary, decision impact, and stop reason. Internal memory, hidden reasoning, elapsed time, or delayed output cannot satisfy a research request.",
        "research_proof=" + research_proof,
        "delivery=Reasoning/research and answer delivery are separate phases. Once the release gate is satisfied, output normally and continuously. Never use sleep, artificial first-token delay, token-by-token throttling, or deliberate chunk pauses as a proxy for depth; slow streaming is not evidence of deep reasoning.",
        "stagnation=After two materially similar failures, change a major dimension before retrying: hypothesis, mechanism, diagnostic instrument, evidence family, environment, or verification method.",
        "verification=Prefer runtime or user-path evidence, then integration, read-back, unit/static, and diff/config inspection. Do not treat a file write, command exit, or unrelated green CI as proof of behavior.",
        "continuity=Do not stop at a foreseeable half-step or require repeated user continuation for predictable work; continue until PASS or a concrete external BLOCKED condition.",
        "adversarial=Before release, try to falsify the result and check scope drift, regression, stale state, partial satisfaction, and contradictory evidence.",
        "pass_requires=" + "; ".join(str(x) for x in pass_requires),
        BINDING_END,
    ])


def bind_preparation(
    preparation: dict,
    repo_root: pathlib.Path | str,
    *,
    task_class: str = "material",
) -> dict:
    if not isinstance(preparation, dict):
        raise ValueError("preparation_not_object")
    if preparation.get("result") != "PASS":
        raise ValueError("preparation_not_pass")
    assignments = preparation.get("assignments")
    if not isinstance(assignments, list) or not assignments:
        raise ValueError("preparation_assignments_missing")

    profile, profile_sha256 = load_profile(repo_root)
    directive = build_runtime_directive(profile, profile_sha256, task_class)
    profile_id = str(profile["profile_id"])
    effort = _reasoning_effort(profile, task_class)
    bound = copy.deepcopy(preparation)

    for row in bound["assignments"]:
        if not isinstance(row, dict):
            raise ValueError("assignment_not_object")
        existing = row.get("quality_profile_binding")
        prompt = str(row.get("prompt") or "")
        if existing:
            if not isinstance(existing, dict):
                raise ValueError("quality_binding_invalid")
            same = (
                existing.get("profile_id") == profile_id
                and existing.get("profile_sha256") == profile_sha256
                and existing.get("task_class") == task_class
                and existing.get("reasoning_effort") == effort
                and existing.get("bound") is True
            )
            if not same:
                raise ValueError("quality_binding_conflict")
            if BINDING_START not in prompt or BINDING_END not in prompt:
                raise ValueError("quality_binding_metadata_without_prompt")
            continue
        if BINDING_START in prompt or BINDING_END in prompt:
            raise ValueError("quality_binding_marker_without_metadata")
        row["prompt"] = directive + "\n\n" + prompt
        row["quality_profile_binding"] = {
            "bound": True,
            "profile_id": profile_id,
            "profile_sha256": profile_sha256,
            "task_class": task_class,
            "reasoning_effort": effort,
            "profile_path": PROFILE_RELATIVE_PATH.as_posix(),
        }

    bound["quality_profile_binding"] = {
        "bound": True,
        "profile_id": profile_id,
        "profile_sha256": profile_sha256,
        "task_class": task_class,
        "reasoning_effort": effort,
        "profile_path": PROFILE_RELATIVE_PATH.as_posix(),
        "assignment_count": len(bound["assignments"]),
    }
    return bound


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--preparation-json", required=True)
    parser.add_argument("--task-class", choices=sorted(TASK_CLASSES), default="material")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    preparation = json.loads(pathlib.Path(args.preparation_json).read_text(encoding="utf-8"))
    bound = bind_preparation(preparation, args.repo_root, task_class=args.task_class)
    text = json.dumps(bound, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
