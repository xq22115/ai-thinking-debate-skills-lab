from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "monitor_sources.py"
SPEC = importlib.util.spec_from_file_location("monitor_sources", SCRIPT)
assert SPEC and SPEC.loader
monitor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = monitor
SPEC.loader.exec_module(monitor)


class MonitorSourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = monitor.load_json(monitor.DEFAULT_CONFIG)
        cls.ledger = monitor.load_json(monitor.DEFAULT_LEDGER)

    def test_baseline_contract_is_exactly_ten_and_valid(self) -> None:
        self.assertEqual(monitor.validate_contract(self.config, self.ledger), [])
        self.assertEqual(len(self.config["lanes"]), 10)
        self.assertEqual(len(self.ledger["records"]), 10)

    def test_url_canonicalization_strips_tracking_and_fragment(self) -> None:
        url = "HTTPS://Example.COM/a/?utm_source=x&keep=1#section"
        self.assertEqual(monitor.canonicalize_url(url), "https://example.com/a?keep=1")

    def test_domain_validation_is_exact_not_suffix_trick(self) -> None:
        self.assertTrue(monitor.domain_allowed("https://clio.com/a", ["clio.com"]))
        self.assertFalse(monitor.domain_allowed("https://evilclio.com/a", ["clio.com"]))
        self.assertFalse(monitor.domain_allowed("https://clio.com.evil.example/a", ["clio.com"]))

    def test_window_is_inclusive(self) -> None:
        self.assertTrue(monitor.date_in_window("2026-06-01", "2026-06-01", "2026-08-31"))
        self.assertTrue(monitor.date_in_window("2026-08-31", "2026-06-01", "2026-08-31"))
        self.assertFalse(monitor.date_in_window("2026-09-01", "2026-06-01", "2026-08-31"))

    def test_candidate_discovery_keeps_only_official_relevant_links(self) -> None:
        observation = monitor.FetchObservation(
            requested_url="https://example.com/blog",
            final_url="https://example.com/blog",
            status=200,
            fetched_at="2026-08-28T00:00:00+00:00",
            sha256="abc",
            text="",
            links=[
                ("/legal-ai-drafting", "Legal AI drafting update"),
                ("https://example.com/about", "About us"),
                ("https://evil.example/legal-ai", "Legal AI"),
            ],
        )
        rows = monitor.discover_candidates(observation, ["example.com"], 10)
        self.assertEqual([row["url"] for row in rows], ["https://example.com/legal-ai-drafting"])

    def _synthetic_receipts(self) -> list[dict]:
        receipts: list[dict] = []
        for lane in self.config["lanes"]:
            receipts.append(
                {
                    "schema_version": 1,
                    "lane": lane["id"],
                    "product": lane["product"],
                    "status": "PASS",
                    "official_url": lane["seed"]["url"],
                    "new_candidates": [],
                    "errors": [],
                }
            )
        return receipts

    def test_adjudicator_accepts_exact_ten_independent_passes(self) -> None:
        result = monitor.adjudicate_receipts(
            self.config, self.ledger, self._synthetic_receipts()
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["errors"], [])
        self.assertEqual(len(result["received_lanes"]), 10)

    def test_adjudicator_fails_closed_when_one_lane_is_missing(self) -> None:
        receipts = self._synthetic_receipts()[:-1]
        result = monitor.adjudicate_receipts(self.config, self.ledger, receipts)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("missing worker receipts" in err for err in result["errors"]))

    def test_adjudicator_rejects_duplicate_worker_receipt(self) -> None:
        receipts = self._synthetic_receipts()
        receipts.append(dict(receipts[0]))
        result = monitor.adjudicate_receipts(self.config, self.ledger, receipts)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("duplicate worker receipt" in err for err in result["errors"]))

    def test_merge_reader_ignores_unrelated_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "noise.json").write_text(json.dumps({"hello": "world"}), encoding="utf-8")
            for row in self._synthetic_receipts():
                (root / f"{row['lane']}.json").write_text(
                    json.dumps(row), encoding="utf-8"
                )
            receipts = monitor.read_receipts(root)
            self.assertEqual(len(receipts), 10)


if __name__ == "__main__":
    unittest.main()
