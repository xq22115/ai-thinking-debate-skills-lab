#!/usr/bin/env python3
"""Ordinary-chat Superpowers bridge layered over the canonical route oracle.

The base router remains authoritative for research, capability, memory, planning,
convergence and completion. This shadow oracle fills implementation-process and
cross-locale routing gaps without mutating the canonical baseline.
"""

import json
import sys
from pathlib import Path

import route_oracle as base

BRIDGE = "superpowers-conversation-runtime"

LOCKED_BASE_ROUTES = {
    "evidence-watchdog",
    "plan-arbiter",
    "memory-policy",
    "convergence-controller",
    "capability-forensics",
    "mcp-surface-engineering",
    "agent-runtime-forensics",
    "chief-of-staff-core",
    "autonomy-contract",
    "persistent-work-ledger",
    "authorized-reverse-engineering",
    "invalid-explicit-skill",
    "capability-mismatch",
}


def _has(text, phrases):
    return any(p in text for p in phrases)


def ordinary_chat_signals(prompt):
    """Protect common zh-Hans/zh-Hant/en intent that the baseline may miss."""
    text = " ".join(prompt.lower().split())
    return {
        "text": text,
        "memory": _has(text, [
            "记住", "記住", "长期偏好", "長期偏好", "以后都沿用", "以後都沿用",
            "永久记忆", "永久記憶", "remember this", "from now on",
        ]),
        "goal_ambiguity": _has(text, [
            "歧义", "歧義", "验收条件", "驗收條件", "成功条件", "成功條件",
            "真正目标", "真正目標", "任务目标", "任務目標", "目标漂移", "目標漂移",
            "不要曲解", "不同理解", "different interpretation", "acceptance criteria",
        ]),
    }


def process_signals(prompt):
    text = " ".join(prompt.lower().split())

    debugging = _has(text, [
        " bug", "bug ", "debug", "failing test", "test failure", "测试失败", "測試失敗",
        "随机超时", "隨機超時", "timeout", "报错", "報錯", "unexpected behavior",
        "unexpected behaviour", "regression", "先找根因再修", "系統化 debug", "系统化 debug",
    ])

    behavior_change = _has(text, [
        "新增功能", "新增能力", "新增一個功能", "新增一个功能", "add feature", "new feature",
        "implement feature", "实现功能", "實作功能", "修改现有行为", "修改現有行為",
        "modify behavior", "modify behaviour", "behavior change", "behaviour change",
        "重构", "重構", "refactor", "做到可测试", "做到可測試",
    ])

    review_feedback = _has(text, [
        "pr review", "review feedback", "code review feedback", "review 的反馈", "review 的反饋",
        "评审意见", "評審意見", "审查意见", "審查意見",
    ])

    skill_noun = _has(text, ["agent skill", " skill", "skill ", "技能包", "技能"])
    skill_action = _has(text, [
        "修改", "編輯", "编辑", "创建", "建立", "新增", "改进", "改進", "improve", "edit", "create", "write",
    ])
    skill_authoring = skill_noun and skill_action

    approved_plan = _has(text, [
        "approved plan", "已批准的计划", "已批准的計畫", "按已确认的计划", "按已確認的計畫",
        "execute the plan", "执行这个计划", "執行這個計畫",
    ])

    settled_design = _has(text, [
        "design is approved", "design approved", "设计已确认", "設計已確認", "设计已经确认",
        "設計已經確認", "按既定设计", "按既定設計",
    ])

    return {
        "text": text,
        "debugging": debugging,
        "behavior_change": behavior_change,
        "review_feedback": review_feedback,
        "skill_authoring": skill_authoring,
        "approved_plan": approved_plan,
        "settled_design": settled_design,
    }


def upstream_process(prompt):
    s = process_signals(prompt)
    if s["skill_authoring"]:
        return "writing-skills"
    if s["review_feedback"]:
        return "receiving-code-review"
    if s["debugging"]:
        return "systematic-debugging"
    if s["approved_plan"]:
        return "executing-plans"
    if s["behavior_change"]:
        return "test-driven-development" if s["settled_design"] else "brainstorming"
    return None


def route(prompt, explicit=None, host_capabilities=None):
    base_primary = base.route(prompt, explicit, host_capabilities)
    if explicit:
        return base_primary

    locale = ordinary_chat_signals(prompt)
    if base_primary == "none" and locale["memory"]:
        return "memory-policy"

    process = upstream_process(prompt)
    if process is None:
        return base_primary
    if base_primary in LOCKED_BASE_ROUTES:
        return base_primary

    # Implementation-process signals are more discriminating than generic research
    # or goal wording. The bridge owns them while preserving higher-specificity
    # base routes such as capability, planning, completion and runtime forensics.
    return BRIDGE


def route_bundle(prompt, explicit=None, host_capabilities=None):
    primary = route(prompt, explicit, host_capabilities)
    base_primary = base.route(prompt, explicit, host_capabilities)
    if primary != BRIDGE:
        if primary != base_primary:
            return [primary]
        return base.route_bundle(prompt, explicit, host_capabilities)

    _, signals = base.analyze(prompt)
    locale = ordinary_chat_signals(prompt)
    bundle = []
    if signals.get("goal_ambiguity") or signals.get("complex") or locale["goal_ambiguity"]:
        bundle.append("task-goal-intelligence")
    bundle.append(BRIDGE)
    return bundle[:3]


def decision(prompt, explicit=None, host_capabilities=None):
    base_primary = base.route(prompt, explicit, host_capabilities)
    primary = route(prompt, explicit, host_capabilities)
    _, signals = base.analyze(prompt)
    locale = ordinary_chat_signals(prompt)
    process = upstream_process(prompt)
    architectural = primary == BRIDGE and (
        signals.get("goal_ambiguity") or signals.get("complex") or locale["goal_ambiguity"]
    )
    ceremony = "ARCHITECTURAL" if architectural else ("BOUNDED" if primary == BRIDGE else "BASE")
    return {
        "primary": primary,
        "bundle": route_bundle(prompt, explicit, host_capabilities),
        "upstream_process": process,
        "base_primary": base_primary,
        "ceremony": ceremony,
        "presentation": "quiet-by-default",
        "locale_protection": {k: v for k, v in locale.items() if k != "text"},
    }


def main(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    failures = []
    for row in rows:
        got = decision(row["prompt"], row.get("explicit"), row.get("host_capabilities"))
        if got["primary"] != row["expected"]:
            failures.append((row["id"], "primary", row["expected"], got["primary"]))
        if "expected_upstream_process" in row and got["upstream_process"] != row["expected_upstream_process"]:
            failures.append((row["id"], "upstream_process", row["expected_upstream_process"], got["upstream_process"]))
        if "expected_bundle" in row and got["bundle"] != row["expected_bundle"]:
            failures.append((row["id"], "bundle", row["expected_bundle"], got["bundle"]))

    print(f"superpowers routing cases: {len(rows)}; failures: {len(failures)}")
    for rid, field, expected, got in failures:
        print(f"FAIL {rid} {field}: expected={expected!r} got={got!r}")
    return 1 if failures else 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "evals" / "superpowers-conversation-routing-cases.jsonl"
    raise SystemExit(main(target))
