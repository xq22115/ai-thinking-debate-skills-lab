#!/usr/bin/env python3
"""Legal Writing Radar: official-source research + evidence-bound drafting logic.

The scanner is intentionally conservative:
- only vendor-controlled hosts configured per lane are followed;
- unknown publication dates remain unknown;
- network failures are recorded, never converted into evidence;
- the seed catalog is independently validated before adjudication.

GitHub Actions provides best-effort scheduled scans. ``watch`` is the continuous
polling mode for an authorized always-on/self-hosted runtime.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from typing import Iterable
from urllib.parse import urljoin, urlsplit, urlunsplit

ROOT = pathlib.Path(__file__).resolve().parent
LANES_FILE = ROOT / "config" / "research_lanes.json"
CATALOG_FILE = ROOT / "evidence" / "verified-tools-2026-06-08.json"
DEFAULT_SINCE = "2026-06-01"
DEFAULT_UNTIL = "2026-08-31"
USER_AGENT = "LegalWritingRadar/1.0 (+https://github.com/xq22115/ai-thinking-debate-skills-lab)"

_CONTEXT_DEPENDENT_LABELS = [
    "without prejudice",
    "for settlement purposes only",
    "subject to contract",
    "attorney-client privileged",
    "attorney work product",
    "all rights reserved",
]
_ALLOWED_MODES = {
    "executive-counsel",
    "transactional",
    "dispute-preservation",
    "international-project",
}


def _load_json(path: pathlib.Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _parse_date(value: object) -> dt.date | None:
    text = str(value or "").strip()
    try:
        return dt.date.fromisoformat(text)
    except ValueError:
        return None


def _normalize_host(host: str) -> str:
    host = host.strip().lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def _host_allowed(url: str, allowed_hosts: Iterable[str]) -> bool:
    host = _normalize_host(urlsplit(url).hostname or "")
    for allowed in allowed_hosts:
        normalized = _normalize_host(str(allowed))
        if host == normalized or host.endswith("." + normalized):
            return True
    return False


def _normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme.lower() not in {"http", "https"} or not parts.netloc:
        return ""
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    path = path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def validate_catalog(catalog: dict, lanes_config: dict, since: str, until: str) -> list[str]:
    """Return every fail-closed catalog validation error."""
    errors: list[str] = []
    start = _parse_date(since)
    end = _parse_date(until)
    if start is None or end is None or start > end:
        return ["invalid requested date window"]

    lanes = lanes_config.get("lanes")
    items = catalog.get("items")
    if not isinstance(lanes, list):
        return ["research_lanes.json must contain a lanes array"]
    if not isinstance(items, list):
        return ["catalog must contain an items array"]
    if len(lanes) != 10:
        errors.append(f"expected exactly 10 research lanes, found {len(lanes)}")
    if len(items) != 10:
        errors.append(f"expected exactly 10 accepted catalog items, found {len(items)}")

    lane_by_id: dict[str, dict] = {}
    seen_lane_ids: set[str] = set()
    seen_lane_tools: set[str] = set()
    for lane in lanes:
        if not isinstance(lane, dict):
            errors.append("lane entry is not an object")
            continue
        lane_id = str(lane.get("lane_id") or "")
        tool_id = str(lane.get("tool_id") or "")
        if lane_id in seen_lane_ids:
            errors.append(f"duplicate lane_id: {lane_id}")
        if tool_id in seen_lane_tools:
            errors.append(f"duplicate configured tool_id: {tool_id}")
        seen_lane_ids.add(lane_id)
        seen_lane_tools.add(tool_id)
        if lane_id:
            lane_by_id[lane_id] = lane
        hosts = lane.get("official_hosts")
        if not isinstance(hosts, list) or not hosts:
            errors.append(f"lane {lane_id or '?'} has no official-domain allowlist")

    seen_tool_ids: set[str] = set()
    seen_urls: set[str] = set()
    seen_vendors: set[str] = set()
    for index, row in enumerate(items, 1):
        if not isinstance(row, dict):
            errors.append(f"item {index} is not an object")
            continue
        lane_id = str(row.get("lane_id") or "")
        tool_id = str(row.get("tool_id") or "")
        vendor = str(row.get("vendor") or "").strip().lower()
        official_url = str(row.get("official_url") or "")
        normalized_url = _normalize_url(official_url)

        if tool_id in seen_tool_ids:
            errors.append(f"duplicate tool_id: {tool_id}")
        seen_tool_ids.add(tool_id)
        if normalized_url and normalized_url in seen_urls:
            errors.append(f"duplicate official_url: {official_url}")
        if normalized_url:
            seen_urls.add(normalized_url)
        if vendor and vendor in seen_vendors:
            errors.append(f"duplicate vendor assignment: {row.get('vendor')}")
        if vendor:
            seen_vendors.add(vendor)

        lane = lane_by_id.get(lane_id)
        if lane is None:
            errors.append(f"item {index} references unknown lane_id: {lane_id}")
        else:
            if tool_id != str(lane.get("tool_id") or ""):
                errors.append(f"lane {lane_id} tool_id does not match configured independent lane")
            if not official_url.startswith("https://") or not _host_allowed(
                official_url, lane.get("official_hosts") or []
            ):
                errors.append(
                    f"lane {lane_id} source is not on its configured official domain: {official_url}"
                )

        release_date = _parse_date(row.get("release_date"))
        if release_date is None:
            errors.append(f"lane {lane_id} has invalid or missing release_date")
        elif not (start <= release_date <= end):
            errors.append(
                f"lane {lane_id} release_date {release_date.isoformat()} is outside requested window"
            )

        capabilities = row.get("writing_capabilities")
        if not isinstance(capabilities, list) or not capabilities or not all(
            isinstance(item, str) and item.strip() for item in capabilities
        ):
            errors.append(f"lane {lane_id} lacks explicit writing/drafting capability evidence")
        if not str(row.get("specialization") or "").strip():
            errors.append(f"lane {lane_id} lacks specialization evidence")
        if not str(row.get("evidence_note") or "").strip():
            errors.append(f"lane {lane_id} lacks an evidence note")

    expected_ids = set(lane_by_id)
    actual_ids = {str(row.get("lane_id") or "") for row in items if isinstance(row, dict)}
    if expected_ids != actual_ids:
        errors.append(
            "accepted catalog lane coverage does not exactly match the ten configured independent lanes"
        )
    return errors


_META_DATE_PATTERNS = [
    re.compile(
        r"<meta[^>]+(?:property|name)=[\"'](?:article:published_time|datepublished|date)[\"'][^>]+content=[\"'](\d{4}-\d{2}-\d{2})(?:[T\s][^\"']*)?[\"']",
        re.IGNORECASE,
    ),
    re.compile(
        r"<meta[^>]+content=[\"'](\d{4}-\d{2}-\d{2})(?:[T\s][^\"']*)?[\"'][^>]+(?:property|name)=[\"'](?:article:published_time|datepublished|date)[\"']",
        re.IGNORECASE,
    ),
    re.compile(r"[\"']datePublished[\"']\s*:\s*[\"'](\d{4}-\d{2}-\d{2})", re.IGNORECASE),
    re.compile(r"<time[^>]+datetime=[\"'](\d{4}-\d{2}-\d{2})(?:[T\s][^\"']*)?[\"']", re.IGNORECASE),
]


def extract_published_date(html: str) -> str | None:
    """Extract only an explicit machine-readable page publication date."""
    for pattern in _META_DATE_PATTERNS:
        match = pattern.search(html)
        if match and _parse_date(match.group(1)) is not None:
            return match.group(1)
    return None


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lowered = tag.lower()
        if lowered == "a":
            values = dict(attrs)
            self._href = values.get("href")
            self._text = []
        elif lowered == "title":
            self._in_title = True

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        if lowered == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None
            self._text = []
        elif lowered == "title":
            self._in_title = False


def discover_official_links(
    base_url: str,
    html: str,
    allowed_hosts: set[str] | list[str],
    keywords: set[str] | list[str],
) -> list[str]:
    """Discover unique keyword-relevant links while staying inside official hosts."""
    parser = _LinkParser()
    parser.feed(html)
    normalized_keywords = {str(item).lower().strip() for item in keywords if str(item).strip()}
    output: list[str] = []
    seen: set[str] = set()
    for href, anchor in parser.links:
        candidate = _normalize_url(urljoin(base_url, href))
        if not candidate or not _host_allowed(candidate, allowed_hosts):
            continue
        haystack = f"{candidate} {anchor}".lower()
        if normalized_keywords and not any(keyword in haystack for keyword in normalized_keywords):
            continue
        if candidate not in seen:
            seen.add(candidate)
            output.append(candidate)
    return output


def _fetch(url: str, timeout: int = 20) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(2_500_000)
            charset = response.headers.get_content_charset() or "utf-8"
            html = raw.decode(charset, errors="replace")
            return {
                "reachable": True,
                "status": int(getattr(response, "status", 200)),
                "final_url": str(response.geturl()),
                "html": html,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "error": None,
            }
    except urllib.error.HTTPError as exc:
        return {
            "reachable": False,
            "status": int(exc.code),
            "final_url": str(getattr(exc, "url", url)),
            "html": "",
            "sha256": None,
            "error": f"HTTPError: {exc.code}",
        }
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {
            "reachable": False,
            "status": None,
            "final_url": url,
            "html": "",
            "sha256": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


def _page_evidence(url: str, lane: dict, since: dt.date, until: dt.date) -> tuple[dict, list[str]]:
    fetched = _fetch(url)
    html = str(fetched.pop("html"))
    parser = _LinkParser()
    if html:
        parser.feed(html)
    published = extract_published_date(html) if html else None
    parsed_date = _parse_date(published)
    keywords = [str(word).lower() for word in lane.get("keywords") or []]
    lowered = f"{url} {parser.title} {html[:250000]}".lower()
    matched = sorted({word for word in keywords if word and word in lowered})
    evidence = {
        "url": url,
        **fetched,
        "official_domain_verified": _host_allowed(
            str(fetched.get("final_url") or url), lane.get("official_hosts") or []
        ),
        "title": re.sub(r"\s+", " ", parser.title).strip()[:300],
        "published_date": published,
        "date_in_requested_window": bool(parsed_date and since <= parsed_date <= until),
        "matched_keywords": matched,
        "content_sha256": fetched.get("sha256"),
    }
    discovered = discover_official_links(
        str(fetched.get("final_url") or url),
        html,
        lane.get("official_hosts") or [],
        lane.get("keywords") or [],
    ) if html else []
    return evidence, discovered


def scan_lane(lane: dict, since: str = DEFAULT_SINCE, until: str = DEFAULT_UNTIL) -> dict:
    """Run one independent official-source lane and return an evidence artifact.

    Reachability errors are observational evidence, not a reason to fabricate a
    publication date. The command still emits an artifact so an independent
    adjudicator can distinguish "source blocked us" from "scan never ran".
    """
    start = _parse_date(since)
    end = _parse_date(until)
    if start is None or end is None:
        raise ValueError("invalid scan date window")

    queue: list[str] = []
    for url in list(lane.get("seed_urls") or []) + list(lane.get("discovery_urls") or []):
        normalized = _normalize_url(str(url))
        if normalized and normalized not in queue:
            queue.append(normalized)
    pages: list[dict] = []
    seen: set[str] = set()
    index = 0
    while index < len(queue) and len(seen) < 16:
        url = queue[index]
        index += 1
        if url in seen:
            continue
        seen.add(url)
        page, links = _page_evidence(url, lane, start, end)
        pages.append(page)
        if url in {_normalize_url(str(item)) for item in lane.get("discovery_urls") or []}:
            for link in links[:12]:
                if link not in seen and link not in queue:
                    queue.append(link)

    return {
        "schema_version": 1,
        "lane_id": str(lane.get("lane_id") or ""),
        "tool_id": str(lane.get("tool_id") or ""),
        "vendor": str(lane.get("vendor") or ""),
        "product": str(lane.get("product") or ""),
        "official_hosts": list(lane.get("official_hosts") or []),
        "requested_window": {"since": since, "until": until},
        "scanned_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "pages": pages,
        "summary": {
            "pages_attempted": len(pages),
            "reachable": sum(1 for page in pages if page.get("reachable") is True),
            "official_domain_verified": sum(
                1 for page in pages if page.get("official_domain_verified") is True
            ),
            "dated_in_window": sum(1 for page in pages if page.get("date_in_requested_window") is True),
            "network_or_http_failures": sum(1 for page in pages if page.get("reachable") is False),
        },
    }


def adjudicate_lane_artifacts(directory: pathlib.Path, lanes_config: dict) -> list[str]:
    errors: list[str] = []
    expected = {str(lane["lane_id"]): str(lane["tool_id"]) for lane in lanes_config.get("lanes") or []}
    found: dict[str, dict] = {}
    for path in sorted(directory.glob("lane-*.json")):
        try:
            row = _load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"unreadable artifact {path.name}: {exc}")
            continue
        lane_id = str(row.get("lane_id") or "")
        if lane_id in found:
            errors.append(f"duplicate lane artifact: {lane_id}")
            continue
        found[lane_id] = row
        if lane_id not in expected:
            errors.append(f"unexpected lane artifact: {lane_id}")
            continue
        if str(row.get("tool_id") or "") != expected[lane_id]:
            errors.append(f"lane {lane_id} artifact tool identity mismatch")
        pages = row.get("pages")
        if not isinstance(pages, list) or not pages:
            errors.append(f"lane {lane_id} produced no scan attempt evidence")
        else:
            if any(page.get("official_domain_verified") is False and page.get("reachable") is True for page in pages):
                errors.append(f"lane {lane_id} followed a reachable non-official source")
    missing = sorted(set(expected) - set(found))
    if missing:
        errors.append(f"missing independent lane artifacts: {', '.join(missing)}")
    if len(found) != 10:
        errors.append(f"expected exactly 10 lane artifacts, found {len(found)}")
    return errors


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value is None or value == "":
        return []
    return [str(value)]


def build_correspondence_blueprint(facts: dict, mode: str) -> dict:
    """Build a high-stakes correspondence blueprint without inventing authority.

    This encodes the *functional architecture* of elite legal/business writing,
    not an imitation of any named lawyer's personal wording.
    """
    if mode not in _ALLOWED_MODES:
        raise ValueError(f"unsupported mode: {mode}")
    objective = str(facts.get("objective") or "").strip()
    if not objective:
        raise ValueError("objective is required")

    authority = _as_list(facts.get("contract_anchors")) + _as_list(facts.get("legal_authorities"))
    if not authority:
        authority = ["[VERIFY CONTRACT / LEGAL AUTHORITY]"]
    known_facts = _as_list(facts.get("known_facts"))
    requested_action = str(facts.get("requested_action") or "").strip()
    deadline = str(facts.get("deadline") or "").strip() or None
    confirmed_input = _as_list(facts.get("legal_labels_confirmed"))
    confirmed_lookup = {item.casefold(): item for item in confirmed_input}
    confirmed = [
        confirmed_lookup[label.casefold()]
        for label in _CONTEXT_DEPENDENT_LABELS
        if label.casefold() in confirmed_lookup
    ]
    # Preserve user-confirmed custom settlement/privilege wording too.
    confirmed.extend(
        item for item in confirmed_input if item.casefold() not in {value.casefold() for value in confirmed}
    )

    blueprint = {
        "mode": mode,
        "position": objective,
        "audience": str(facts.get("audience") or "decision-maker / counsel").strip(),
        "record": known_facts or ["[INSERT VERIFIED CONTEMPORANEOUS FACTS / CHRONOLOGY]"],
        "authority_anchors": authority,
        "analysis": _as_list(facts.get("analysis")) or [
            "Connect each verified fact to the stated authority or commercial premise; separate fact, inference, and requested decision."
        ],
        "commercial_effect": _as_list(facts.get("commercial_effect")) or [
            "[STATE PRACTICAL / COMMERCIAL / PROJECT CONSEQUENCE WITHOUT OVERCLAIMING]"
        ],
        "ask": requested_action or "[STATE ONE CLEAR ACTION / DECISION REQUIRED]",
        "deadline": deadline,
        "reservations": _as_list(facts.get("reservations")) or [
            "Preserve only rights actually supported by the verified contract/law; do not use boilerplate as a substitute for a required notice."
        ],
        "confirmed_legal_labels": confirmed,
        "style_controls": [
            "decision-first: state the position or requested decision before background",
            "record-anchored: use dates, matter/project references and contemporaneous documents",
            "authority-bound: cite verified contract clauses, precedent or law; never invent one",
            "calibrated commitment: distinguish proposal, present position, condition and final commitment",
            "explicit close: one owner, one ask, one deadline or next step",
            "short professional paragraphs; remove adjectives that do not change legal/commercial meaning",
        ],
        "drafting_sequence": [
            "position / decision",
            "record / chronology",
            "verified authority or contract anchor",
            "analysis / consequence",
            "commercial or project effect",
            "requested action and deadline",
            "narrow, verified reservation if needed",
        ],
    }

    if mode == "transactional":
        blueprint["transaction_controls"] = {
            "commitment_state": str(facts.get("commitment_state") or "proposal / subject to verification"),
            "conditions": _as_list(facts.get("conditions")),
            "reciprocity": _as_list(facts.get("reciprocity")),
        }
    elif mode == "dispute-preservation":
        blueprint["disabled_legal_labels"] = [
            label for label in _CONTEXT_DEPENDENT_LABELS if label.casefold() not in confirmed_lookup
        ]
        blueprint["dispute_controls"] = [
            "state the disputed proposition precisely rather than attacking motive",
            "identify the record and the verified legal/contractual basis",
            "preserve a required notice/deadline independently of settlement language",
            "do not apply privilege, work-product, settlement or without-prejudice labels without verified basis",
        ]
    elif mode == "international-project":
        blueprint["project_reference"] = str(
            facts.get("project_reference") or "[INSERT PROJECT / CONTRACT / PACKAGE REFERENCE]"
        )
        blueprint["claim_logic"] = {
            "cause": str(facts.get("cause") or "[STATE VERIFIED EVENT / INSTRUCTION / CONDITION]"),
            "effect": str(facts.get("effect") or "[STATE DEMONSTRABLE TIME / COST / SCOPE EFFECT]"),
            "entitlement": str(
                facts.get("entitlement")
                or "[VERIFY ENTITLEMENT AGAINST CONTRACT AND APPLICABLE LAW]"
            ),
            "quantum": str(
                facts.get("quantum")
                or "[SUPPORT QUANTUM WITH CONTEMPORANEOUS RECORDS / VALUATION]"
            ),
        }
        blueprint["project_controls"] = [
            "verify notice addressee, form, delivery method and time bar before sending",
            "separate instruction/request for instruction from a claim of entitlement",
            "link cause -> effect -> entitlement -> quantum; do not skip causal proof",
            "name the contemporaneous records being preserved or requested",
        ]
    return blueprint


def _write_json(path: pathlib.Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _lane_by_id(config: dict, lane_id: str) -> dict:
    for lane in config.get("lanes") or []:
        if str(lane.get("lane_id") or "") == lane_id:
            return lane
    raise ValueError(f"unknown lane: {lane_id}")


def _cmd_verify(_: argparse.Namespace) -> int:
    lanes = _load_json(LANES_FILE)
    catalog = _load_json(CATALOG_FILE)
    window = lanes.get("research_window") or {}
    errors = validate_catalog(
        catalog,
        lanes,
        str(window.get("since") or DEFAULT_SINCE),
        str(window.get("until") or DEFAULT_UNTIL),
    )
    print(json.dumps({
        "status": "PASS" if not errors else "FAIL",
        "accepted_count": len(catalog.get("items") or []),
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def _cmd_scan(args: argparse.Namespace) -> int:
    config = _load_json(LANES_FILE)
    lane = _lane_by_id(config, args.lane)
    window = config.get("research_window") or {}
    artifact = scan_lane(
        lane,
        str(window.get("since") or DEFAULT_SINCE),
        str(window.get("until") or DEFAULT_UNTIL),
    )
    output = pathlib.Path(args.output)
    _write_json(output, artifact)
    print(json.dumps({
        "status": "RECORDED",
        "lane_id": artifact["lane_id"],
        "output": str(output),
        "summary": artifact["summary"],
    }, ensure_ascii=False, indent=2))
    return 0


def _cmd_adjudicate(args: argparse.Namespace) -> int:
    lanes = _load_json(LANES_FILE)
    catalog = _load_json(CATALOG_FILE)
    window = lanes.get("research_window") or {}
    errors = validate_catalog(
        catalog,
        lanes,
        str(window.get("since") or DEFAULT_SINCE),
        str(window.get("until") or DEFAULT_UNTIL),
    )
    errors.extend(adjudicate_lane_artifacts(pathlib.Path(args.directory), lanes))
    print(json.dumps({
        "status": "PASS" if not errors else "FAIL",
        "lane_artifact_count": len(list(pathlib.Path(args.directory).glob("lane-*.json"))),
        "accepted_seed_count": len(catalog.get("items") or []),
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def _cmd_compose(args: argparse.Namespace) -> int:
    facts = _load_json(pathlib.Path(args.input))
    blueprint = build_correspondence_blueprint(facts, args.mode)
    if args.output:
        _write_json(pathlib.Path(args.output), blueprint)
    else:
        print(json.dumps(blueprint, ensure_ascii=False, indent=2))
    return 0


def _cmd_watch(args: argparse.Namespace) -> int:
    if args.interval < 60:
        raise ValueError("watch interval must be at least 60 seconds")
    config = _load_json(LANES_FILE)
    window = config.get("research_window") or {}
    output_root = pathlib.Path(args.output_dir)
    try:
        while True:
            stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            run_dir = output_root / stamp
            for lane in config.get("lanes") or []:
                artifact = scan_lane(
                    lane,
                    str(window.get("since") or DEFAULT_SINCE),
                    str(window.get("until") or DEFAULT_UNTIL),
                )
                _write_json(run_dir / f"lane-{lane['lane_id']}.json", artifact)
            errors = adjudicate_lane_artifacts(run_dir, config)
            _write_json(run_dir / "adjudication.json", {
                "status": "PASS" if not errors else "FAIL",
                "errors": errors,
            })
            print(f"[{stamp}] scanned {len(config.get('lanes') or [])} lanes -> {run_dir}", flush=True)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Official-source AI legal writing research radar")
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify", help="verify the immutable ten-source seed catalog")
    verify.set_defaults(func=_cmd_verify)

    scan = sub.add_parser("scan", help="scan one independent official-source lane")
    scan.add_argument("--lane", required=True)
    scan.add_argument("--output", required=True)
    scan.set_defaults(func=_cmd_scan)

    adjudicate = sub.add_parser("adjudicate", help="independently validate ten lane artifacts")
    adjudicate.add_argument("--directory", required=True)
    adjudicate.set_defaults(func=_cmd_adjudicate)

    compose = sub.add_parser("compose", help="turn verified facts into a correspondence blueprint")
    compose.add_argument("--mode", required=True, choices=sorted(_ALLOWED_MODES))
    compose.add_argument("--input", required=True)
    compose.add_argument("--output")
    compose.set_defaults(func=_cmd_compose)

    watch = sub.add_parser("watch", help="continuous polling for an authorized always-on runtime")
    watch.add_argument("--interval", type=int, default=900)
    watch.add_argument("--output-dir", default=str(ROOT / "runtime-evidence"))
    watch.set_defaults(func=_cmd_watch)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
