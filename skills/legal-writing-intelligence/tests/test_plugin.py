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
        self.seed = json.loads((ROOT / "resources" / "verified-tools-2026-06-08.json").read_text(encoding="utf-8"))

    def test_exactly_ten_independent_agents(self):
        agents = self.config["agents"]
        self.assertEqual(10, len(agents))
        self.assertEqual(10, len({a["id"] for a in agents}))
        self.assertEqual(10, len({a["vendor"] for a in agents}))
        self.assertEqual(10, len({a["query"] for a in agents}))

    def test_seed_is_verified_and_in_window(self):
        self.assertEqual([], research.validate_seed(self.seed, self.config))

    def test_all_seed_urls_are_https(self):
        self.assertTrue(all(r["official_url"].startswith("https://") for r in self.seed["reports"]))

    def test_month_precision_date_is_supported(self):
        lo, hi = research.parse_release_date("2026-07")
        self.assertEqual("2026-07-01", lo.isoformat())
        self.assertEqual("2026-07-31", hi.isoformat())

    def test_live_validation_fails_closed_without_official_fetch(self):
        live = []
        for agent in self.config["agents"]:
            live.append({
                "agent_id": agent["id"],
                "vendor": agent["vendor"],
                "query": agent["query"],
                "official_evidence": [{"url": agent["watch_urls"][0], "error": "HTTPError"}],
            })
        errors = research.validate_live(live, self.config)
        self.assertTrue(any("no live official-source fetch succeeded" in e for e in errors))

    def test_live_validation_accepts_ten_distinct_official_fetches(self):
        live = []
        for agent in self.config["agents"]:
            live.append({
                "agent_id": agent["id"],
                "vendor": agent["vendor"],
                "query": agent["query"],
                "official_evidence": [{"url": agent["watch_urls"][0], "http_status": 200}],
            })
        self.assertEqual([], research.validate_live(live, self.config))

    def test_writer_requires_evidence_fields(self):
        with self.assertRaises(ValueError):
            writer.draft_letter({"matter": "X"})

    def test_writer_contains_precise_ask_and_reservation(self):
        text = writer.draft_letter({
            "matter": "Project Falcon — Milestone 4",
            "purpose": "We need written confirmation of the recovery plan.",
            "recipient": "Counsel",
            "mode": "project-escalation",
            "facts": ["Milestone 4 was due August 20, 2026.", "The current forecast is August 31, 2026."],
            "asks": ["Provide the revised critical-path schedule.", "Identify the accountable executive for each recovery action."],
            "deadline": "August 29, 2026 at 5:00 p.m. New York time",
            "reserve_rights": True,
            "disputed": True
        })
        self.assertIn("Please confirm", text)
        self.assertIn("All rights and remedies are expressly reserved", text)
        self.assertIn("critical path", text)
        self.assertNotIn("hereinafter", text.lower())


if __name__ == "__main__":
    unittest.main()
