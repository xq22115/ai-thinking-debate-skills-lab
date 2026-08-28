#!/usr/bin/env python3
"""Ten-branch legal AI writing research runner.

Each agent has a distinct vendor/query/watch set. Discovery is keyless (Bing News RSS)
and verification re-fetches configured official pages. The adjudicator refuses duplicate
agent IDs/vendors, seed identity drift, incomplete date provenance, and redirected live
evidence that leaves the configured official domain.
"""
from __future__ import annotations

import argparse
import email.utils
import hashlib
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

UA = "legal-writing-intelligence/0.2 (+https://github.com/)"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _host(url: str) -> str:
    return (urllib.parse.urlparse(url).hostname or "").lower().removeprefix("www.")


def host_allowed(url: str, allowed: list[str]) -> bool:
    host = _host(url)
    normalized = [str(d).lower().removeprefix("www.") for d in allowed]
    return any(host == d or host.endswith("." + d) for d in normalized)


def fetch(url: str, timeout: int = 20) -> tuple[int, str, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/rss+xml,application/xml;q=0.9,*/*;q=0.5",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read(1_500_000)
        charset = resp.headers.get_content_charset() or "utf-8"
        return (
            int(resp.status),
            raw.decode(charset, errors="replace"),
            str(resp.geturl()),
        )


def bing_news(query: str) -> list[dict[str, Any]]:
    url = "https://www.bing.com/news/search?" + urllib.parse.urlencode(
        {"q": query, "format": "rss"}
    )
    status, body, _ = fetch(url)
    if status != 200:
        return []
    root = ET.fromstring(body)
    out: list[dict[str, Any]] = []
    for item in root.findall(".//item")[:20]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        parsed = email.utils.parsedate_to_datetime(pub).date().isoformat() if pub else None
        out.append({"title": title, "url": link, "published": parsed})
    return out


def html_fingerprint(text: str) -> str:
    collapsed = re.sub(r"\s+", " ", text).strip().encode("utf-8")
    return hashlib.sha256(collapsed).hexdigest()


def run_agent(config: dict[str, Any], agent_id: str) -> dict[str, Any]:
    agents = {a["id"]: a for a in config["agents"]}
    if agent_id not in agents:
        raise ValueError(f"unknown agent: {agent_id}")
    agent = agents[agent_id]
    discovery = []
    try:
        discovery = bing_news(agent["query"])
    except Exception as exc:  # discovery is informative, never a pass condition
        discovery = [{"error": type(exc).__name__, "message": str(exc)}]

    official_evidence = []
    for url in agent["watch_urls"]:
        if not host_allowed(url, agent["official_domains"]):
            raise ValueError(f"watch URL outside official domains for {agent_id}: {url}")
        try:
            status, body, final_url = fetch(url)
            official_evidence.append(
                {
                    "url": url,
                    "final_url": final_url,
                    "http_status": status,
                    "sha256": html_fingerprint(body),
                    "bytes": len(body.encode("utf-8")),
                    "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                }
            )
        except Exception as exc:
            official_evidence.append(
                {
                    "url": url,
                    "error": type(exc).__name__,
                    "message": str(exc),
                    "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                }
            )

    return {
        "agent_id": agent_id,
        "vendor": agent["vendor"],
        "query": agent["query"],
        "date_window": config["date_window"],
        "discovery": discovery,
        "official_evidence": official_evidence,
    }


def parse_release_date(value: str) -> tuple[date, date]:
    """Parse exact dates plus legacy month-only values.

    Month-only parsing remains for backward compatibility with old artifacts, but current
    seed acceptance requires exact-day evidence.
    """
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        d = date.fromisoformat(value)
        return d, d
    if re.fullmatch(r"\d{4}-\d{2}", value):
        year, month = map(int, value.split("-"))
        start = date(year, month, 1)
        if month == 12:
            end = date(year, 12, 31)
        else:
            end = date.fromordinal(date(year, month + 1, 1).toordinal() - 1)
        return start, end
    raise ValueError(f"unsupported release_date: {value}")


def validate_seed(seed: dict[str, Any], config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    reports = seed.get("reports", [])
    start = date.fromisoformat(config["date_window"]["start"])
    end = date.fromisoformat(config["date_window"]["end"])
    config_agents = {a["id"]: a for a in config["agents"]}

    if len(reports) != 10:
        errors.append(f"expected 10 reports, found {len(reports)}")
    ids = [r.get("agent_id") for r in reports]
    vendors = [r.get("vendor") for r in reports]
    urls = [r.get("official_url") for r in reports]
    if len(set(ids)) != len(ids):
        errors.append("duplicate agent_id")
    if len(set(vendors)) != len(vendors):
        errors.append("duplicate vendor")
    if len(set(urls)) != len(urls):
        errors.append("duplicate official_url")
    if set(ids) != set(config_agents):
        errors.append(f"seed agent set mismatch: got {sorted(set(ids))}")

    for report in reports:
        aid = report.get("agent_id")
        release_date = str(report.get("release_date", ""))
        if report.get("date_precision") != "day" or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}", release_date
        ):
            errors.append(f"exact day release date required for {aid}: {release_date}")
        try:
            lo, hi = parse_release_date(release_date)
            if hi < start or lo > end:
                errors.append(f"out-of-window release: {aid} {release_date}")
        except Exception as exc:
            errors.append(str(exc))
            continue

        expected = config_agents.get(aid)
        if expected is None:
            errors.append(f"unknown seed agent: {aid}")
            continue
        if report.get("vendor") != expected["vendor"]:
            errors.append(f"vendor mismatch for {aid}")

        official_url = str(report.get("official_url", ""))
        if not host_allowed(official_url, expected["official_domains"]):
            errors.append(f"non-official URL for {aid}: {official_url}")
        if official_url not in expected["watch_urls"]:
            errors.append(f"seed/watch URL mismatch for {aid}: {official_url}")

        if not str(report.get("source_kind", "")).startswith("official_"):
            errors.append(f"non-official source kind for {aid}")
        if not str(report.get("writing_relevance", "")).strip():
            errors.append(f"missing writing relevance for {aid}")
        if not str(report.get("adversarial_check", "")).strip():
            errors.append(f"missing adversarial check for {aid}")
        if report.get("status") != "verified":
            errors.append(f"verification status must be exactly verified for {aid}")
    return errors


def validate_live(live: list[dict[str, Any]], config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    by_id = {a["id"]: a for a in config["agents"]}
    ids = [x.get("agent_id") for x in live]
    vendors = [x.get("vendor") for x in live]
    queries = [x.get("query") for x in live]
    expected_ids = set(by_id)

    if len(live) != 10:
        errors.append(f"expected 10 live agent artifacts, found {len(live)}")
    if len(set(ids)) != len(ids):
        errors.append("duplicate live agent artifacts")
    if len(set(vendors)) != len(vendors):
        errors.append("duplicate live vendors")
    if len(set(queries)) != len(queries):
        errors.append("duplicate live queries")
    if set(ids) != expected_ids:
        errors.append(f"live agent set mismatch: got {sorted(set(ids))}")

    for item in live:
        aid = item.get("agent_id")
        if aid not in by_id:
            continue
        expected = by_id[aid]
        if item.get("vendor") != expected["vendor"]:
            errors.append(f"vendor mismatch for {aid}")
        if item.get("query") != expected["query"]:
            errors.append(f"query mismatch for {aid}")
        evidence = item.get("official_evidence") or []
        live_ok = [
            e
            for e in evidence
            if isinstance(e.get("http_status"), int)
            and 200 <= e["http_status"] < 400
        ]
        if not live_ok:
            errors.append(f"no live official-source fetch succeeded for {aid}")
            continue
        for ev in live_ok:
            requested_url = str(ev.get("url", ""))
            final_url = str(ev.get("final_url", ""))
            if requested_url not in expected["watch_urls"]:
                errors.append(f"unconfigured live evidence URL for {aid}: {requested_url}")
            if not host_allowed(requested_url, expected["official_domains"]):
                errors.append(
                    f"live evidence outside official domains for {aid}: {requested_url}"
                )
            if not final_url:
                errors.append(f"missing final URL evidence for {aid}")
            elif not host_allowed(final_url, expected["official_domains"]):
                errors.append(
                    f"final URL outside official domains for {aid}: {final_url}"
                )
    return errors


def adjudicate(
    result_dir: Path, seed_path: Path, config_path: Path, out: Path
) -> dict[str, Any]:
    config = load_json(config_path)
    seed = load_json(seed_path)
    errors = validate_seed(seed, config)
    files = sorted(result_dir.rglob("agent-*.json"))
    live = [load_json(p) for p in files]
    errors.extend(validate_live(live, config))
    report = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "seed": seed,
        "live_agents": live,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "agents.json",
    )
    parser.add_argument("--agent")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--adjudicate", type=Path)
    parser.add_argument(
        "--seed",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "resources"
        / "verified-tools-2026-06-08.json",
    )
    args = parser.parse_args()

    config = load_json(args.config)
    if args.adjudicate:
        report = adjudicate(args.adjudicate, args.seed, args.config, args.out)
        return 0 if report["status"] == "PASS" else 1
    if not args.agent:
        parser.error("--agent is required unless --adjudicate is used")
    result = run_agent(config, args.agent)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
