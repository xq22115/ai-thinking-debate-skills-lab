from __future__ import annotations

import unittest
import tempfile
import json
from pathlib import Path

from validate_formal_dialectical import validate_source_ledger

from formal_dialectical_reference import (
    collective_support_state,
    grounded_labels,
    minimal_downstream_revision,
    minimal_single_edge_flip_set,
    resolve_defeats,
)


class FormalDialecticalReferenceTests(unittest.TestCase):
    def test_attack_types_are_preserved_and_attack_is_not_automatically_defeat(self):
        attacks = [
            {"source": "A", "target": "B", "type": "undermine"},
            {"source": "C", "target": "D", "type": "undercut", "preference_blocked": True},
            {"source": "E", "target": "F", "type": "rebut"},
        ]
        defeats = resolve_defeats(attacks)
        self.assertEqual([(d["source"], d["target"], d["type"]) for d in defeats], [
            ("A", "B", "undermine"), ("E", "F", "rebut")
        ])
    def test_grounded_two_cycle_is_undecided_not_arbitrary_winner(self):
        labels = grounded_labels(
            ["A", "B"],
            [
                {"source": "A", "target": "B", "type": "rebut"},
                {"source": "B", "target": "A", "type": "rebut"},
            ],
        )
        self.assertEqual(labels, {"A": "UNDEC", "B": "UNDEC"})

    def test_collective_support_requires_every_member(self):
        self.assertEqual(collective_support_state(["SUPPORTED", "SUPPORTED"]), "SUPPORTED")
        self.assertEqual(collective_support_state(["SUPPORTED", "UNKNOWN"]), "UNKNOWN")
        self.assertEqual(collective_support_state(["SUPPORTED", "REJECTED"]), "REJECTED")

    def test_unknown_is_not_false_and_uncertain_warrant_propagates(self):
        self.assertEqual(collective_support_state(["SUPPORTED", "UNKNOWN"]), "UNKNOWN")
        self.assertEqual(
            collective_support_state(["SUPPORTED", "SUPPORTED"], warrant_state="UNKNOWN"),
            "UNKNOWN",
        )
    def test_minimal_single_edge_flip_set_finds_decision_critical_relation(self):
        arguments = ["A", "B", "C"]
        attacks = [
            {"source": "A", "target": "C", "type": "rebut"},
            {"source": "B", "target": "A", "type": "rebut"},
        ]
        flips = minimal_single_edge_flip_set(arguments, attacks, target="C")
        self.assertEqual(flips, [{"source": "B", "target": "A", "type": "rebut"}])

    def test_minimal_revision_changes_only_downstream_dependents(self):
        state = {"P": "SUPPORTED", "Q": "SUPPORTED", "R": "SUPPORTED", "X": "SUPPORTED"}
        dependencies = {"Q": ["P"], "R": ["Q"], "X": []}
        revised, changed = minimal_downstream_revision(
            state,
            evidence_updates={"P": "REJECTED"},
            dependencies=dependencies,
        )
        self.assertEqual(revised["P"], "REJECTED")
        self.assertEqual(revised["Q"], "REJECTED")
        self.assertEqual(revised["R"], "REJECTED")
        self.assertEqual(revised["X"], "SUPPORTED")
        self.assertEqual(changed, {"P", "Q", "R"})

    def test_source_ledger_gate_rejects_under_100_duplicates_and_out_of_window(self):
        base={"quality_gate":{"counted_unique_count":100,"passed":True},"sources":[]}
        for i in range(100):
            base["sources"].append({"title":f"Unique reasoning source {i}","publication_date":"2026-07-20","counted_for_100_source_gate":True})
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"ledger.json"
            path.write_text(json.dumps(base),encoding="utf-8")
            validate_source_ledger(path)
            base["quality_gate"]["counted_unique_count"]=99
            base["quality_gate"]["passed"]=False
            path.write_text(json.dumps(base),encoding="utf-8")
            with self.assertRaises(ValueError): validate_source_ledger(path)
            base["quality_gate"]["counted_unique_count"]=100; base["quality_gate"]["passed"]=True
            base["sources"][1]["title"]=base["sources"][0]["title"]
            path.write_text(json.dumps(base),encoding="utf-8")
            with self.assertRaises(ValueError): validate_source_ledger(path)
            base["sources"][1]["title"]="Restored unique"; base["sources"][2]["publication_date"]="2026-05-31"
            path.write_text(json.dumps(base),encoding="utf-8")
            with self.assertRaises(ValueError): validate_source_ledger(path)


if __name__ == "__main__":
    unittest.main()
