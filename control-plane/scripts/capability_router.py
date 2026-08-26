#!/usr/bin/env python3
"""Deterministic, health-aware route selection for ordinary-chat capabilities.

The router ranks known capability IDs from the repository registry. It does not
execute tasks itself and never invents a capability that is absent from the
registry. Host-side apps remain conditional until their own preflight succeeds.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any

import capability_health

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "ai-system" / "configs" / "ordinary-chat-capabilities.json"

INTENT_ORDER: dict[str, list[str]] = {
    "repository_action": ["github-native"],
    "local_bounded": ["remote-desktop-commander", "chat-work-agent"],
    "local_long": ["chat-work-agent", "a01-a10-runtime"],
    "multi_step_repair": ["a01-a10-runtime", "chat-work-agent"],
    "browser_deterministic": ["playwright-cli", "browser-use-cli", "playwright-mcp"],
    "browser_adaptive": ["browser-use-cli", "playwright-mcp", "playwright-cli"],
    "browser_stateful": ["playwright-mcp", "browser-use-cli", "playwright-cli"],
    "project_recall": ["project-memory"],
    "observability": ["ordinary-chat-dashboard"],
    "capability_discovery": ["ordinary-chat-mcp"],
}

READ_ONLY_ONLY = {"ordinary-chat-dashboard", "project-memory"}
LOCAL_EXECUTION = {"chat-work-agent", "a01-a10-runtime", "playwright-cli", "browser-use-cli"}


def _registry() -> dict[str, dict[str, Any]]:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("capabilities"), list):
        raise ValueError("capability_registry_invalid")
    result: dict[str, dict[str, Any]] = {}
    for item in value["capabilities"]:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            result[item["id"]] = item
    return result


def _health_map() -> dict[str, dict[str, Any]]:
    payload = capability_health.cached_or_snapshot()
    items = payload.get("capabilities")
    if not isinstance(items, dict):
        return {}
    return {str(key): value for key, value in items.items() if isinstance(value, dict)}


def _candidate_state(capability_id: str, health: dict[str, dict[str, Any]]) -> tuple[str, bool | None]:
    item = health.get(capability_id, {})
    ready = item.get("ready")
    if ready is True:
        return "READY", True
    if ready is False:
        return "UNAVAILABLE", False
    return "CONDITIONAL", None


def route(
    intent: str,
    *,
    needs_write: bool = False,
    prefer_local: bool = False,
    require_ready: bool = False,
) -> dict[str, Any]:
    if intent not in INTENT_ORDER:
        return {
            "schemaVersion": 1,
            "result": "BLOCKED",
            "reason": "intent_invalid",
            "supported_intents": sorted(INTENT_ORDER),
        }

    registry = _registry()
    health = _health_map()
    ordered = INTENT_ORDER[intent]
    ranked: list[dict[str, Any]] = []

    for preference_index, capability_id in enumerate(ordered):
        metadata = registry.get(capability_id)
        if metadata is None:
            continue
        state, ready = _candidate_state(capability_id, health)
        if needs_write and capability_id in READ_ONLY_ONLY:
            state = "INCOMPATIBLE"
            ready = False

        score = 1000 - (preference_index * 100)
        if ready is True:
            score += 200
        elif ready is False:
            score -= 1200
        else:
            score -= 100
        if prefer_local and capability_id in LOCAL_EXECUTION:
            score += 40
        if needs_write and metadata.get("risk") in {"local_mutation", "governed_local_mutation", "long_running_local_mutation"}:
            score += 20

        ranked.append(
            {
                "id": capability_id,
                "score": score,
                "state": state,
                "ready": ready,
                "kind": metadata.get("kind"),
                "status": metadata.get("status"),
                "risk": metadata.get("risk"),
                "preflight_required": ready is None,
            }
        )

    ranked.sort(key=lambda item: (-int(item["score"]), str(item["id"])))
    selectable = [item for item in ranked if item["state"] not in {"UNAVAILABLE", "INCOMPATIBLE"}]
    if require_ready:
        selectable = [item for item in selectable if item["ready"] is True]

    selected = selectable[0] if selectable else None
    if selected is None:
        return {
            "schemaVersion": 1,
            "intent": intent,
            "needs_write": needs_write,
            "prefer_local": prefer_local,
            "require_ready": require_ready,
            "candidates": ranked,
            "result": "BLOCKED",
            "reason": "no_compatible_ready_route" if require_ready else "no_compatible_route",
        }

    result = "PASS" if selected["ready"] is True else "CONDITIONAL"
    return {
        "schemaVersion": 1,
        "intent": intent,
        "needs_write": needs_write,
        "prefer_local": prefer_local,
        "require_ready": require_ready,
        "selected": selected,
        "candidates": ranked,
        "result": result,
        "reason": None if result == "PASS" else "selected_route_requires_external_or_runtime_preflight",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intent", required=True, choices=sorted(INTENT_ORDER))
    parser.add_argument("--needs-write", action="store_true")
    parser.add_argument("--prefer-local", action="store_true")
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = route(
            args.intent,
            needs_write=args.needs_write,
            prefer_local=args.prefer_local,
            require_ready=args.require_ready,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {
            "schemaVersion": 1,
            "result": "FAIL",
            "reason": f"router_error:{type(exc).__name__}",
        }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("result") in {"PASS", "CONDITIONAL"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
