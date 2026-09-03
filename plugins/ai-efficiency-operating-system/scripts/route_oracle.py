#!/usr/bin/env python3
"""Deterministic baseline for semantic auto-invoke routing.

The host may add a learned/semantic reranker after this eligibility layer, but the
deterministic baseline remains canonical for regression, hard-negative, bundle and
fallback tests.
"""

import json
import re
import sys
from pathlib import Path

DEFAULT_IMPLICIT = {
    "task-goal-intelligence", "chief-of-staff-core", "plan-arbiter",
    "evidence-watchdog", "executive-research", "memory-policy",
    "convergence-controller",
}
CONDITIONAL_IMPLICIT = {
    "capability-forensics", "mcp-surface-engineering", "agent-runtime-forensics",
}
EXPLICIT_ONLY = {
    "autonomy-contract", "persistent-work-ledger", "authorized-reverse-engineering",
}
ALL_SKILLS = DEFAULT_IMPLICIT | CONDITIONAL_IMPLICIT | EXPLICIT_ONLY

FALLBACKS = {
    "capability-forensics": ["executive-research", "evidence-watchdog"],
    "mcp-surface-engineering": ["capability-forensics", "executive-research", "evidence-watchdog"],
    "agent-runtime-forensics": ["capability-forensics", "evidence-watchdog"],
    "executive-research": ["task-goal-intelligence", "evidence-watchdog"],
    "plan-arbiter": ["chief-of-staff-core"],
    "convergence-controller": ["chief-of-staff-core", "evidence-watchdog"],
}

PRIORITY = [
    "agent-runtime-forensics", "mcp-surface-engineering", "capability-forensics",
    "evidence-watchdog", "convergence-controller", "plan-arbiter", "memory-policy",
    "executive-research", "chief-of-staff-core", "task-goal-intelligence",
]

TERMS = {
    "plan": [
        "方案", "plan", "順序", "sequence", "tradeoff", "trade-off", "哪個路線", "哪個方法",
        "先查", "規劃", "選架構", "choose architecture", "architecture option", "比較 a/b", "比較 a / b",
        "比較兩個", "比較兩種", "兩個 architecture", "保留能力",
    ],
    "completion": [
        "已完成", "完成了", "算修好了", "真的 live", "已經生效", "是不是已經生效", "deployed",
        "installed", "configured", "done", "postcondition", "read-back", "read back", "驗收", "verify",
    ],
    "memory": [
        "記住", "永久記憶", "memory", "前一個聊天室", "跨 session", "cross-session", "恢復真正有效",
        "rehydrat", "stale memory", "先前決策", "previous chat",
    ],
    "convergence": [
        "無限循環", "review 已經", "review again", "keep improving", "再試第三次", "同樣的方法", "重複失敗",
        "一直失敗", "失敗三次", "原路重試", "同樣循環", "換 route", "materially different route",
        "skill 改到變好", "regression", "別停下來", "修到 pass", "fix until pass",
    ],
    "research": [
        "研究", "查 ", "查找", "最新", "根因", "root cause", "交叉比對", "證據", "evidence", "深入",
        "來源", "counterevidence", "版本", "why", "為什麼", "issue", "pr", "commit", "benchmark", "大神",
        "maintainer", "失敗案例",
    ],
    "complex": [
        "多階段", "multi-stage", "多個硬限制", "多個工具", "兩個帳號", "複雜任務", "背景一直做",
        "長流程", "long-horizon", "multi-tool", "多步", "端到端", "end-to-end",
    ],
    "goal_ambiguity": [
        "真正目標", "原始目標", "理解任務", "任務目標", "真正任務", "別搞錯目標", "走錯目標",
        "鎖定目標", "目標漂移", "goal drift", "latent intent", "underlying purpose", "target identity",
        "歧義", "ambigu", "到底要做什麼", "不要曲解", "成功條件", "驗收條件", "acceptance criteria",
        "真正要達成", "先理解",
    ],
    "capability_problem": [
        "能力限制", "capability limit", "capability bottleneck", "卡在哪一層", "卡在哪", "不能用", "用不了",
        "沒有工具", "工具不見", "missing tool", "permission", "權限", "entitlement", "session", "surface",
        "同一模型", "same model", "桌面版", "desktop", "web 版", "網頁版", "登入", "帳號", "profile",
        "plugin", "connector", "model vs", "harness", "為什麼這邊沒有", "why is it unavailable",
    ],
    "capability_diagnosis": [
        "為什麼", "why", "診斷", "diagnose", "判斷", "到底", "差異", "差別", "不同", "bottleneck",
        "限制", "卡", "哪一層", "layer", "能不能", "可不可以", "是否真的", "真正原因", "invokable",
        "effective", "visible", "authorized",
    ],
    "mcp_surface": [
        "mcp", "tool surface", "工具面", "tool schema", "schema drift", "dynamic discovery", "tool discovery",
        "動態工具", "動態載入", "lazy loading", "deferred tool", "namespace collision", "tool poisoning",
        "context 很肥", "context 太肥", "context window", "100+ tools", "150 個", "很多 tools", "很多工具",
        "多個 mcp", "tool registry", "工具 registry", "工具清單太多", "schema version",
    ],
    "mcp_pressure": [
        "很多", "100+", "150", "動態", "dynamic", "schema", "drift", "context", "collision", "namespace",
        "poison", "registry", "entitlement", "lazy", "deferred", "discover", "discovery", "版本",
    ],
    "runtime_effect": [
        "工具說", "tool said", "寫入成功", "write succeeded", "success but", "檔案沒有變", "file did not change",
        "state 沒變", "state didn't change", "沒有生效", "not effective", "process", "程序", "network", "artifact",
        "causal chain", "因果鏈", "runtime provenance", "runtime trace", "工具回傳成功", "實際沒變", "postcondition missing",
    ],
}


def _count(text, phrases):
    return sum(1 for phrase in phrases if phrase in text)


def _is_simple(text):
    patterns = [
        r"^\s*2\s*\+\s*2", r"^\s*\d+\s*[+\-*/]\s*\d+\s*[?？]?\s*$",
        r"翻成英文", r"translate this", r"改寫這句", r"rewrite this sentence",
    ]
    return any(re.search(pattern, text) for pattern in patterns)


def _is_explanation_only(text):
    explain = any(p in text for p in ["是什麼", "what is", "請解釋", "解釋一下", "explain "])
    operational = any(p in text for p in [
        "幫我", "請查", "研究", "修", "設定", "配置", "診斷", "debug", "fix", "比較", "設計", "做 ",
        "怎麼做", "怎麼修", "why", "為什麼", "生效", "invoke", "dynamic discovery", "schema drift",
    ])
    return explain and not operational


def analyze(prompt):
    text = " ".join(prompt.lower().split())
    signals = {name: _count(text, phrases) for name, phrases in TERMS.items()}
    signals["runtime_mismatch"] = int(
        signals["runtime_effect"] >= 2
        or any(a in text and b in text for a, b in [
            ("成功", "沒"), ("success", "not"), ("寫入", "沒有變"),
            ("tool", "state"), ("configured", "state"), ("configured", "not effective"),
        ])
    )
    # Capability nouns such as Desktop/plugin/account are weak evidence. A heavy
    # capability specialist needs an actual diagnostic/contrast signal too.
    signals["capability_gap"] = int(
        signals["capability_problem"] >= 1 and signals["capability_diagnosis"] >= 1
    )
    signals["tool_surface_pressure"] = int(
        signals["mcp_surface"] >= 2
        or (signals["mcp_surface"] >= 1 and signals["mcp_pressure"] >= 1)
    )
    signals["substantive"] = int(any(signals[name] for name in [
        "plan", "completion", "memory", "convergence", "research", "complex",
        "goal_ambiguity", "capability_problem", "mcp_surface", "runtime_effect",
    ]))
    return text, signals


def score_routes(prompt):
    text, s = analyze(prompt)
    if _is_simple(text) or _is_explanation_only(text):
        return {"none": 100}, s

    scores = {name: 0 for name in PRIORITY}
    scores["agent-runtime-forensics"] = 8 * s["runtime_mismatch"] + 2 * s["runtime_effect"]
    scores["mcp-surface-engineering"] = 8 * s["tool_surface_pressure"] + 2 * s["mcp_surface"]
    scores["capability-forensics"] = 8 * s["capability_gap"] + s["capability_problem"]
    scores["evidence-watchdog"] = 5 * s["completion"]
    scores["convergence-controller"] = 6 * s["convergence"]
    scores["plan-arbiter"] = 5 * s["plan"]
    scores["memory-policy"] = 5 * s["memory"]
    scores["executive-research"] = 4 * s["research"]
    # The goal gate is included in the bundle; for a complex multi-stage task the
    # chief-of-staff remains primary phase owner.
    scores["chief-of-staff-core"] = 8 * s["complex"]
    scores["task-goal-intelligence"] = 5 * s["goal_ambiguity"]

    if s["research"] and s["capability_gap"]:
        scores["capability-forensics"] += 3
    if s["research"] and s["tool_surface_pressure"]:
        scores["mcp-surface-engineering"] += 3
    if s["research"] and s["runtime_mismatch"]:
        scores["agent-runtime-forensics"] += 3
    return scores, s


def route(prompt, explicit=None, host_capabilities=None):
    caps = set(host_capabilities or [])
    if explicit:
        if explicit not in ALL_SKILLS:
            return "invalid-explicit-skill"
        if explicit == "persistent-work-ledger" and not {"filesystem", "durable_state"}.issubset(caps):
            return "capability-mismatch"
        return explicit

    scores, _ = score_routes(prompt)
    if "none" in scores:
        return "none"
    best = max(scores.values()) if scores else 0
    if best <= 0:
        return "none"
    winners = {name for name, score in scores.items() if score == best}
    for name in PRIORITY:
        if name in winners:
            return name
    return "none"


def route_bundle(prompt, explicit=None, host_capabilities=None):
    primary = route(prompt, explicit, host_capabilities)
    if primary in {"none", "invalid-explicit-skill", "capability-mismatch"}:
        return [] if primary == "none" else [primary]
    if explicit:
        return [primary]

    _, s = analyze(prompt)
    bundle = []
    if s["substantive"] and primary != "task-goal-intelligence":
        bundle.append("task-goal-intelligence")
    bundle.append(primary)

    needs_verifier = (
        s["completion"] > 0 or s["runtime_mismatch"]
        or primary in {
            "capability-forensics", "mcp-surface-engineering", "agent-runtime-forensics",
            "convergence-controller", "chief-of-staff-core",
        }
        or (primary == "executive-research" and s["complex"] > 0)
    )
    if needs_verifier and "evidence-watchdog" not in bundle:
        bundle.append("evidence-watchdog")

    deduped = []
    for item in bundle:
        if item not in deduped:
            deduped.append(item)
    return deduped[:3]


def fallback_chain(primary):
    return FALLBACKS.get(primary, [])


def decision(prompt, explicit=None, host_capabilities=None):
    scores, signals = score_routes(prompt)
    primary = route(prompt, explicit, host_capabilities)
    return {
        "primary": primary,
        "bundle": route_bundle(prompt, explicit, host_capabilities),
        "fallback": fallback_chain(primary),
        "signals": signals,
        "scores": scores,
    }


def main(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    failures = []
    for row in rows:
        got = route(row["prompt"], row.get("explicit"), row.get("host_capabilities"))
        if got != row["expected"]:
            failures.append((row["id"], row["expected"], got))
    print(f"routing cases: {len(rows)}; failures: {len(failures)}")
    for rid, expected, got in failures:
        print(f"FAIL {rid}: expected={expected} got={got}")
    return 1 if failures else 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "evals" / "routing-cases.jsonl"
    raise SystemExit(main(target))
