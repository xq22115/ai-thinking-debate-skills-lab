import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


research = load_module("research", ROOT / "src" / "research.py")
writer = load_module("writer", ROOT / "src" / "writer.py")


class PluginTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "agents.json").read_text(encoding="utf-8"))
        self.seed = json.loads(
            (ROOT / "resources" / "verified-tools-2026-06-08.json").read_text(
                encoding="utf-8"
            )
        )

    def _successful_live_receipts(self):
        live = []
        for agent in self.config["agents"]:
            watch_url = agent["watch_urls"][0]
            live.append(
                {
                    "agent_id": agent["id"],
                    "vendor": agent["vendor"],
                    "query": agent["query"],
                    "official_evidence": [
                        {
                            "url": watch_url,
                            "final_url": watch_url,
                            "http_status": 200,
                        }
                    ],
                }
            )
        return live

    def test_exactly_ten_independent_agents(self):
        agents = self.config["agents"]
        self.assertEqual(10, len(agents))
        self.assertEqual(10, len({a["id"] for a in agents}))
        self.assertEqual(10, len({a["vendor"] for a in agents}))
        self.assertEqual(10, len({a["query"] for a in agents}))

    def test_seed_is_verified_and_in_window(self):
        self.assertEqual([], research.validate_seed(self.seed, self.config))

    def test_all_seed_urls_are_https(self):
        self.assertTrue(
            all(r["official_url"].startswith("https://") for r in self.seed["reports"])
        )

    def test_parser_still_understands_month_precision_for_legacy_inputs(self):
        lo, hi = research.parse_release_date("2026-07")
        self.assertEqual("2026-07-01", lo.isoformat())
        self.assertEqual("2026-07-31", hi.isoformat())

    def test_seed_acceptance_requires_exact_day_precision(self):
        seed = copy.deepcopy(self.seed)
        seed["reports"][0]["release_date"] = "2026-07"
        seed["reports"][0]["date_precision"] = "month"
        errors = research.validate_seed(seed, self.config)
        self.assertTrue(any("exact day" in error for error in errors))

    def test_seed_rejects_vendor_identity_drift(self):
        seed = copy.deepcopy(self.seed)
        seed["reports"][0]["vendor"] = "Different Vendor"
        errors = research.validate_seed(seed, self.config)
        self.assertTrue(any("vendor mismatch" in error for error in errors))

    def test_seed_rejects_missing_writing_relevance(self):
        seed = copy.deepcopy(self.seed)
        seed["reports"][0]["writing_relevance"] = ""
        errors = research.validate_seed(seed, self.config)
        self.assertTrue(any("writing relevance" in error for error in errors))

    def test_seed_rejects_partial_verification_status(self):
        seed = copy.deepcopy(self.seed)
        seed["reports"][0]["status"] = "verified_with_date_precision_limit"
        errors = research.validate_seed(seed, self.config)
        self.assertTrue(any("verification status" in error for error in errors))

    def test_live_validation_fails_closed_without_official_fetch(self):
        live = []
        for agent in self.config["agents"]:
            live.append(
                {
                    "agent_id": agent["id"],
                    "vendor": agent["vendor"],
                    "query": agent["query"],
                    "official_evidence": [
                        {"url": agent["watch_urls"][0], "error": "HTTPError"}
                    ],
                }
            )
        errors = research.validate_live(live, self.config)
        self.assertTrue(
            any("no live official-source fetch succeeded" in e for e in errors)
        )

    def test_live_validation_accepts_ten_distinct_official_fetches(self):
        self.assertEqual(
            [], research.validate_live(self._successful_live_receipts(), self.config)
        )

    def test_live_validation_rejects_cross_domain_final_redirect(self):
        live = self._successful_live_receipts()
        live[0]["official_evidence"][0]["final_url"] = (
            "https://untrusted.example/evidence"
        )
        errors = research.validate_live(live, self.config)
        self.assertTrue(any("final URL outside official domains" in e for e in errors))

    def test_writer_requires_evidence_fields(self):
        with self.assertRaises(ValueError):
            writer.draft_letter({"matter": "X"})

    def test_writer_requires_scope_before_reserving_rights(self):
        with self.assertRaisesRegex(ValueError, "reservation_scope"):
            writer.draft_letter(
                {
                    "matter": "Project Falcon — Milestone 4",
                    "purpose": "We need written confirmation of the recovery plan.",
                    "mode": "project-escalation",
                    "facts": ["Milestone 4 was due August 20, 2026."],
                    "asks": ["Provide the revised critical-path schedule."],
                    "reserve_rights": True,
                }
            )

    def test_writer_contains_precise_ask_and_scoped_reservation(self):
        text = writer.draft_letter(
            {
                "matter": "Project Falcon — Milestone 4",
                "purpose": "We need written confirmation of the recovery plan.",
                "recipient": "Counsel",
                "mode": "project-escalation",
                "facts": [
                    "Milestone 4 was due August 20, 2026.",
                    "The current forecast is August 31, 2026.",
                ],
                "asks": [
                    "Provide the revised critical-path schedule.",
                    "Identify the accountable executive for each recovery action.",
                ],
                "deadline": "August 29, 2026 at 5:00 p.m. New York time",
                "reserve_rights": True,
                "reservation_scope": "our position regarding responsibility for delay",
                "disputed": True,
            }
        )
        self.assertIn("Please confirm", text)
        self.assertIn("not intended to waive", text)
        self.assertIn("our position regarding responsibility for delay", text)
        self.assertIn("critical path", text)
        self.assertNotIn("hereinafter", text.lower())


if __name__ == "__main__":
    unittest.main()
