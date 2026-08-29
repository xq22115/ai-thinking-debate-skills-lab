#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

EXPLICIT = {"autonomy-contract", "persistent-work-ledger"}


def route(prompt, explicit=None, host_capabilities=None):
    caps = set(host_capabilities or [])
    text = prompt.lower()
    if explicit:
        if explicit not in EXPLICIT:
            return "invalid-explicit-skill"
        if explicit == "persistent-work-ledger" and not {"filesystem", "durable_state"}.issubset(caps):
            return "capability-mismatch"
        return explicit

    simple = [r"^\s*2\s*\+\s*2", r"翻成英文", r"translate this", r"改寫這句", r"rewrite this sentence"]
    if any(re.search(p, text) for p in simple):
        return "none"

    convergence = ["無限循環", "review 已經", "review again", "keep improving", "再試第三次", "同樣的方法", "skill 改到變好", "regression"]
    if any(k in text for k in convergence):
        return "convergence-controller"

    # Phase/decision intent beats keyword overlap. A document or subject merely
    # mentioning an architecture is not automatically a planning task.
    plan = ["方案", "plan", "順序", "sequence", "tradeoff", "trade-off", "哪個路線", "哪個方法", "先查", "規劃", "選架構", "choose architecture", "architecture option"]
    if any(k in text for k in plan):
        return "plan-arbiter"

    completion = ["已完成", "完成了", "算修好了", "真的 live", "已經生效", "是不是已經生效", "deployed", "installed", "configured", "done", "postcondition"]
    if any(k in text for k in completion):
        return "evidence-watchdog"

    memory = ["記住", "永久記憶", "memory", "前一個聊天室", "恢復真正有效", "rehydrat", "stale memory"]
    if any(k in text for k in memory):
        return "memory-policy"

    research = ["研究", "查 ", "最新", "根因", "root cause", "交叉比對", "證據", "evidence", "深入", "來源", "counterevidence", "版本", "why"]
    if any(k in text for k in research):
        return "executive-research"

    complex_terms = ["多階段", "multi-stage", "多個硬限制", "多個工具", "兩個帳號", "複雜任務", "背景一直做"]
    if any(k in text for k in complex_terms):
        return "chief-of-staff-core"

    return "none"


def main(path):
    failures = []
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
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
