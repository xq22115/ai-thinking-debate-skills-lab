#!/usr/bin/env python3
"""Evidence-gated 10-lane monitor for elite legal correspondence research."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "research-lanes.json"
DEFAULT_LEDGER = ROOT / "references" / "2026-summer-ai-writing-tools.json"
USER_AGENT = (
    "Mozilla/5.0 (compatible; EliteLegalCorrespondenceRadar/0.1; "
    "+https://github.com/xq22115/ai-thinking-debate-skills-lab)"
)
MAX_BYTES = 2_000_000
RELEVANCE_TERMS = (
    " ai ",
    "draft",
    "writing",
    "legal",
    "contract",
    "agent",
    "negotiat",
    "redline",
    "review",
    "work product",
    "work-product",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._anchor: list[str] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        values = dict(attrs)
        href = values.get("href")
        if href:
            self._href = href
            self._anchor = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return
        self.text_parts.append(text)
        if self._href is not None:
            self._anchor.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._anchor).strip()))
            self._href = None
            self._anchor = []


@dataclass(frozen=True)
class FetchObservation:
    requested_url: str
    final_url: str
    status: int
    fetched_at: str
    sha256: str
    text: str
    links: list[tuple[str, str]]

    def public(self) -> dict:
        return {
            "requested_url": self.requested_url,
            "final_url": self.final_url,
            "status": self.status,
            "fetched_at": self.fetched_at,
            "sha256": self.sha256,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def canonicalize_url(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    parts = urllib.parse.urlsplit(value)
    if parts.scheme.lower() not in {"http", "https"} or not parts.netloc:
        return ""
    query_pairs = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    kept = [
        (k, v)
        for k, v in query_pairs
        if not k.lower().startswith("utm_")
        and k.lower() not in {"fbclid", "gclid", "mc_cid", "mc_eid"}
    ]
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")
    return urllib.parse.urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), path, urllib.parse.urlencode(kept), "")
    )


def hostname(value: str) -> str:
    try:
        return urllib.parse.urlsplit(value).hostname or ""
    except ValueError:
        return ""


def domain_allowed(url: str, allowed_domains: Iterable[str]) -> bool:
    host = hostname(url).lower().rstrip(".")
    return any(host == d.lower().rstrip(".") for d in allowed_domains)


def parse_iso_date(value: str) -> date:
    return date.fromisoformat(value)


def date_in_window(value: str, start: str, end: str) -> bool:
    target = parse_iso_date(value)
    return parse_iso_date(start) <= target <= parse_iso_date(end)


def _decode_body(raw: bytes, content_type: str) -> str:
    charset = "utf-8"
    match = re.search(r"charset=([A-Za-z0-9._-]+)", content_type or "", re.I)
    if match:
        charset = match.group(1)
    try:
        return raw.decode(charset, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


def fetch_page(url: str, timeout: int = 25) -> FetchObservation:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.7",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raw = raw[:MAX_BYTES]
            text = _decode_body(raw, response.headers.get("Content-Type", ""))
            parser = PageParser()
            parser.feed(text)
            visible = html.unescape(" ".join(parser.text_parts))
            return FetchObservation(
                requested_url=url,
                final_url=canonicalize_url(response.geturl()),
                status=int(getattr(response, "status", 200) or 200),
                fetched_at=utc_now(),
                sha256=hashlib.sha256(raw).hexdigest(),
                text=visible,
                links=parser.links,
            )
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} for {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"network error for {url}: {exc.reason}") from exc


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def validate_contract(config: dict, ledger: dict) -> list[str]:
    errors: list[str] = []
    lanes = config.get("lanes")
    records = ledger.get("records")
    if not isinstance(lanes, list):
        return ["config.lanes must be a list"]
    if not isinstance(records, list):
        return ["ledger.records must be a list"]

    expected_count = int(config.get("lane_count", 0))
    if expected_count != 10:
        errors.append(f"lane_count must be 10, got {expected_count}")
    if len(lanes) != 10:
        errors.append(f"exactly 10 lanes required, got {len(lanes)}")
    if len(records) != 10:
        errors.append(f"exactly 10 ledger records required, got {len(records)}")

    start = str(config.get("window", {}).get("start", ""))
    end = str(config.get("window", {}).get("end", ""))
    try:
        parse_iso_date(start)
        parse_iso_date(end)
    except ValueError:
        errors.append("config research window must use ISO dates")
        return errors

    lane_ids: list[str] = []
    products: list[str] = []
    seed_urls: list[str] = []
    lane_map: dict[str, dict] = {}
    for lane in lanes:
        lane_id = str(lane.get("id", ""))
        product = str(lane.get("product", ""))
        seed = lane.get("seed") if isinstance(lane.get("seed"), dict) else {}
        seed_url = canonicalize_url(str(seed.get("url", "")))
        domains = lane.get("official_domains") or []
        lane_ids.append(lane_id)
        products.append(product.casefold())
        seed_urls.append(seed_url)
        lane_map[lane_id] = lane
        if not lane_id or not product or not seed_url:
            errors.append(f"lane has missing id/product/seed URL: {lane_id or '<missing>'}")
            continue
        if not domain_allowed(seed_url, domains):
            errors.append(f"{lane_id}: seed URL is outside official domains")
        try:
            if not date_in_window(str(seed.get("release_date", "")), start, end):
                errors.append(f"{lane_id}: seed release date outside research window")
        except ValueError:
            errors.append(f"{lane_id}: invalid seed release date")
        required_terms = seed.get("required_terms")
        if not isinstance(required_terms, list) or len(required_terms) < 2:
            errors.append(f"{lane_id}: at least two required terms are required")

    for label, values in (
        ("lane IDs", lane_ids),
        ("products", products),
        ("canonical seed URLs", seed_urls),
    ):
        if len(set(values)) != len(values):
            errors.append(f"duplicate {label} are forbidden")

    ledger_lanes: list[str] = []
    ledger_products: list[str] = []
    ledger_urls: list[str] = []
    for record in records:
        lane_id = str(record.get("lane", ""))
        product = str(record.get("product", ""))
        url = canonicalize_url(str(record.get("official_url", "")))
        status = str(record.get("verification_status", ""))
        ledger_lanes.append(lane_id)
        ledger_products.append(product.casefold())
        ledger_urls.append(url)
        lane = lane_map.get(lane_id)
        if lane is None:
            errors.append(f"ledger record references unknown lane {lane_id}")
            continue
        if product.casefold() != str(lane.get("product", "")).casefold():
            errors.append(f"{lane_id}: ledger product does not match lane product")
        if url != canonicalize_url(str(lane.get("seed", {}).get("url", ""))):
            errors.append(f"{lane_id}: ledger URL does not match lane seed URL")
        if status != "VERIFIED_OFFICIAL":
            errors.append(f"{lane_id}: baseline record must be VERIFIED_OFFICIAL")
        if not domain_allowed(url, lane.get("official_domains") or []):
            errors.append(f"{lane_id}: ledger URL is outside official domains")
        try:
            if not date_in_window(str(record.get("release_date", "")), start, end):
                errors.append(f"{lane_id}: ledger release date outside research window")
        except ValueError:
            errors.append(f"{lane_id}: invalid ledger release date")
        specialization = str(record.get("specialization", "")).casefold()
        if not any(term in specialization for term in ("draft", "writing", "legal", "contract")):
            errors.append(f"{lane_id}: specialization lacks writing/legal drafting evidence")

    for label, values in (
        ("ledger lanes", ledger_lanes),
        ("ledger products", ledger_products),
        ("ledger URLs", ledger_urls),
    ):
        if len(set(values)) != len(values):
            errors.append(f"duplicate {label} are forbidden")
    if set(ledger_lanes) != set(lane_ids):
        errors.append("ledger lanes must exactly match config lanes")
    return errors


def _resolve_link(base_url: str, href: str) -> str:
    return canonicalize_url(urllib.parse.urljoin(base_url, href))


def _candidate_score(url: str, anchor: str) -> int:
    haystack = f" {url} {anchor} ".casefold()
    return sum(1 for term in RELEVANCE_TERMS if term in haystack)


def discover_candidates(
    observation: FetchObservation,
    allowed_domains: Iterable[str],
    limit: int,
) -> list[dict]:
    scored: dict[str, tuple[int, str]] = {}
    for href, anchor in observation.links:
        url = _resolve_link(observation.final_url or observation.requested_url, href)
        if not url or not domain_allowed(url, allowed_domains):
            continue
        score = _candidate_score(url, anchor)
        if score <= 0:
            continue
        previous = scored.get(url)
        if previous is None or score > previous[0]:
            scored[url] = (score, anchor.strip())
    rows = [
        {"url": url, "score": score, "anchor": anchor[:240]}
        for url, (score, anchor) in scored.items()
    ]
    rows.sort(key=lambda row: (-int(row["score"]), str(row["url"])))
    return rows[:limit]


def find_lane(config: dict, lane_id: str) -> dict:
    for lane in config.get("lanes", []):
        if lane.get("id") == lane_id:
            return lane
    raise ValueError(f"unknown lane: {lane_id}")


def scan_lane(config: dict, ledger: dict, lane_id: str, timeout: int = 25) -> dict:
    contract_errors = validate_contract(config, ledger)
    if contract_errors:
        return {
            "schema_version": 1,
            "lane": lane_id,
            "status": "FAIL",
            "scanned_at": utc_now(),
            "errors": contract_errors,
        }

    lane = find_lane(config, lane_id)
    seed = lane["seed"]
    errors: list[str] = []
    observations: list[dict] = []
    candidates: list[dict] = []

    seed_observation: FetchObservation | None = None
    try:
        seed_observation = fetch_page(str(seed["url"]), timeout=timeout)
        observations.append({"kind": "seed", **seed_observation.public()})
    except RuntimeError as exc:
        errors.append(str(exc))

    if seed_observation is not None:
        if not domain_allowed(seed_observation.final_url, lane["official_domains"]):
            errors.append("seed redirected outside the lane's official domains")
        folded = seed_observation.text.casefold()
        terms = [str(term) for term in seed.get("required_terms", [])]
        matched = [term for term in terms if term.casefold() in folded]
        minimum_matches = min(2, len(terms))
        if len(matched) < minimum_matches:
            errors.append(
                f"seed content signal too weak: matched {len(matched)}/{len(terms)} required terms"
            )
        observations[-1]["required_terms_matched"] = matched
        observations[-1]["required_terms_missing"] = [term for term in terms if term not in matched]

    discovery_limit = int(config.get("policy", {}).get("discovery_candidate_limit_per_lane", 20))
    seen_discovery: set[str] = set()
    for discovery_url in lane.get("discovery_urls", []):
        canonical = canonicalize_url(str(discovery_url))
        if not canonical or canonical in seen_discovery:
            continue
        seen_discovery.add(canonical)
        try:
            observation = fetch_page(canonical, timeout=timeout)
            observations.append({"kind": "discovery", **observation.public()})
            candidates.extend(
                discover_candidates(observation, lane["official_domains"], discovery_limit)
            )
        except RuntimeError as exc:
            observations.append(
                {
                    "kind": "discovery",
                    "requested_url": canonical,
                    "fetched_at": utc_now(),
                    "error": str(exc),
                }
            )

    deduped: dict[str, dict] = {}
    seed_canonical = canonicalize_url(str(seed["url"]))
    for candidate in candidates:
        url = str(candidate["url"])
        if url == seed_canonical:
            continue
        existing = deduped.get(url)
        if existing is None or int(candidate["score"]) > int(existing["score"]):
            deduped[url] = candidate

    sorted_candidates = sorted(
        deduped.values(), key=lambda row: (-int(row["score"]), str(row["url"]))
    )[:discovery_limit]

    status = "PASS" if not errors else "FAIL"
    return {
        "schema_version": 1,
        "lane": lane_id,
        "product": lane["product"],
        "status": status,
        "scanned_at": utc_now(),
        "release_date": seed["release_date"],
        "official_url": seed["url"],
        "observations": observations,
        "new_candidates": sorted_candidates,
        "errors": errors,
    }


def read_receipts(inputs_dir: Path) -> list[dict]:
    receipts: list[dict] = []
    for path in sorted(inputs_dir.rglob("*.json")):
        try:
            row = load_json(path)
        except (OSError, json.JSONDecodeError, ValueError):
            continue
        if "lane" in row and "status" in row:
            receipts.append(row)
    return receipts


def adjudicate_receipts(config: dict, ledger: dict, receipts: list[dict]) -> dict:
    errors = validate_contract(config, ledger)
    expected = {str(lane["id"]) for lane in config.get("lanes", [])}
    seen: dict[str, dict] = {}
    for receipt in receipts:
        lane_id = str(receipt.get("lane", ""))
        if lane_id in seen:
            errors.append(f"duplicate worker receipt for {lane_id}")
            continue
        seen[lane_id] = receipt

    missing = sorted(expected - set(seen))
    extra = sorted(set(seen) - expected)
    if missing:
        errors.append(f"missing worker receipts: {', '.join(missing)}")
    if extra:
        errors.append(f"unexpected worker receipts: {', '.join(extra)}")

    for lane_id in sorted(expected & set(seen)):
        receipt = seen[lane_id]
        if receipt.get("status") != "PASS":
            errors.append(f"{lane_id}: worker status is {receipt.get('status')}")
        lane = find_lane(config, lane_id)
        if canonicalize_url(str(receipt.get("official_url", ""))) != canonicalize_url(
            str(lane["seed"]["url"])
        ):
            errors.append(f"{lane_id}: receipt official URL drifted from configured seed")

    candidate_map: dict[str, dict] = {}
    for receipt in seen.values():
        for candidate in receipt.get("new_candidates", []) or []:
            url = canonicalize_url(str(candidate.get("url", "")))
            if not url:
                continue
            row = dict(candidate)
            row["url"] = url
            row["discovered_by"] = receipt.get("lane")
            previous = candidate_map.get(url)
            if previous is None or int(row.get("score", 0)) > int(previous.get("score", 0)):
                candidate_map[url] = row

    return {
        "schema_version": 1,
        "status": "PASS" if not errors else "FAIL",
        "adjudicated_at": utc_now(),
        "expected_lanes": sorted(expected),
        "received_lanes": sorted(seen),
        "errors": errors,
        "baseline_records": ledger.get("records", []),
        "new_candidates": sorted(
            candidate_map.values(),
            key=lambda row: (-int(row.get("score", 0)), str(row.get("url", ""))),
        ),
        "worker_receipts": [seen[lane] for lane in sorted(seen)],
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def command_validate(args: argparse.Namespace) -> int:
    config = load_json(Path(args.config))
    ledger = load_json(Path(args.ledger))
    errors = validate_contract(config, ledger)
    payload = {"status": "PASS" if not errors else "FAIL", "errors": errors}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def command_scan(args: argparse.Namespace) -> int:
    config = load_json(Path(args.config))
    ledger = load_json(Path(args.ledger))
    result = scan_lane(config, ledger, args.lane, timeout=args.timeout)
    write_json(Path(args.out), result)
    print(json.dumps({"lane": args.lane, "status": result["status"]}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


def command_merge(args: argparse.Namespace) -> int:
    config = load_json(Path(args.config))
    ledger = load_json(Path(args.ledger))
    receipts = read_receipts(Path(args.inputs_dir))
    result = adjudicate_receipts(config, ledger, receipts)
    write_json(Path(args.out), result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "received_lanes": len(result["received_lanes"]),
                "candidate_count": len(result["new_candidates"]),
                "errors": result["errors"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["status"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate the ten-lane baseline contract")
    validate.set_defaults(func=command_validate)

    scan = sub.add_parser("scan", help="run one independent live research lane")
    scan.add_argument("--lane", required=True)
    scan.add_argument("--out", required=True)
    scan.add_argument("--timeout", type=int, default=25)
    scan.set_defaults(func=command_scan)

    merge = sub.add_parser("merge", help="adjudicate all ten worker receipts")
    merge.add_argument("--inputs-dir", required=True)
    merge.add_argument("--out", required=True)
    merge.set_defaults(func=command_merge)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
