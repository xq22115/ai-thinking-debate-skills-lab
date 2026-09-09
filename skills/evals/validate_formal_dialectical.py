from __future__ import annotations

import json
from pathlib import Path

from formal_dialectical_reference import (
    collective_support_state,
    grounded_labels,
    minimal_downstream_revision,
    minimal_single_edge_flip_set,
    resolve_defeats,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "skills/evals/formal-dialectical-fixtures.json"
REFERENCE = ROOT / "skills/skills/semantic-argument-microscope/FORMAL_DIALECTICAL_REASONING.md"
SOURCE_LEDGER = ROOT / "skills/18-formal-dialectical-reasoning-source-ledger.json"


def validate_source_ledger(path: Path = SOURCE_LEDGER) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    gate = payload.get("quality_gate") or {}
    counted = int(gate.get("counted_unique_count", 0))
    if counted < 100 or gate.get("passed") is not True:
        raise ValueError(f"formal source ledger requires >=100 counted unique sources, got {counted}")
    rows = [r for r in payload.get("sources", []) if r.get("counted_for_100_source_gate") is True]
    if len(rows) < 100:
        raise ValueError(f"formal source ledger has only {len(rows)} countable rows")
    titles = [" ".join(str(r.get("title", "")).casefold().split()) for r in rows]
    if any(not title for title in titles) or len(titles) != len(set(titles)):
        raise ValueError("formal source ledger contains missing or duplicate counted titles")
    for row in rows:
        date = str(row.get("publication_date", ""))
        if not ("2026-06-01" <= date <= "2026-09-09"):
            raise ValueError(f"counted source outside priority window: {row.get('title')} ({date})")


def validate_assets() -> None:
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        raise ValueError("formal fixture suite must contain exactly F1-F12")
    ids = [case.get("id") for case in cases]
    if ids != [f"F{i}" for i in range(1, 13)]:
        raise ValueError("formal fixture ids must be ordered F1-F12")
    for case in cases:
        if not case.get("name") or not case.get("input"):
            raise ValueError(f"incomplete case: {case.get('id')}")
        must = case.get("must_detect")
        if not isinstance(must, list) or not must:
            raise ValueError(f"missing must_detect: {case.get('id')}")
    text = REFERENCE.read_text(encoding="utf-8")
    required = [
        "ATTACK != DEFEAT",
        "UNKNOWN != FALSE",
        "SOLVER_CORRECTNESS != PARSER_CORRECTNESS",
        "UNCERTAINTY MUST PROPAGATE",
        "MINIMAL_VERDICT_FLIP_SET",
        "UNDER_REVISION",
        "OVER_REVISION",
    ]
    missing = [token for token in required if token not in text]
    if missing:
        raise ValueError(f"formal reference missing invariants: {missing}")


def self_test() -> None:
    attacks = [
        {"source": "A", "target": "B", "type": "undercut", "preference_blocked": True},
        {"source": "C", "target": "B", "type": "rebut"},
    ]
    if resolve_defeats(attacks) != [{"source": "C", "target": "B", "type": "rebut"}]:
        raise AssertionError("attack-to-defeat resolution failed")
    labels = grounded_labels(
        ["A", "B"],
        [{"source": "A", "target": "B", "type": "rebut"},
         {"source": "B", "target": "A", "type": "rebut"}],
    )
    if labels != {"A": "UNDEC", "B": "UNDEC"}:
        raise AssertionError("grounded two-cycle handling failed")
    if collective_support_state(["SUPPORTED", "UNKNOWN"]) != "UNKNOWN":
        raise AssertionError("UNKNOWN collapsed into false/true")
    if collective_support_state(["SUPPORTED", "SUPPORTED"], "UNKNOWN") != "UNKNOWN":
        raise AssertionError("warrant uncertainty did not propagate")
    graph = [
        {"source": "A", "target": "C", "type": "rebut"},
        {"source": "B", "target": "A", "type": "rebut"},
    ]
    flips = minimal_single_edge_flip_set(["A", "B", "C"], graph, "C")
    if flips != [{"source": "B", "target": "A", "type": "rebut"}]:
        raise AssertionError("minimal flip-set reference failed")
    revised, changed = minimal_downstream_revision(
        {"P": "SUPPORTED", "Q": "SUPPORTED", "R": "SUPPORTED", "X": "SUPPORTED"},
        {"P": "REJECTED"},
        {"Q": ["P"], "R": ["Q"], "X": []},
    )
    if revised["X"] != "SUPPORTED" or changed != {"P", "Q", "R"}:
        raise AssertionError("bounded revision failed")


if __name__ == "__main__":
    validate_assets()
    validate_source_ledger()
    self_test()
    print("formal dialectical assets + executable reference: PASS (F1-F12)")
    print("status boundary: STATIC/REFERENCE VERIFIED; target-model and host-live behavior NOT EXECUTED")
