#!/usr/bin/env python3
"""Validate the ordinary-ChatGPT <-> GitHub plugin bridge fail-closed."""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PLUGIN_ROOT = ROOT / "plugins/ai-efficiency-operating-system"
PLUGIN_MANIFEST = PLUGIN_ROOT / ".codex-plugin/plugin.json"
APP_MANIFEST = PLUGIN_ROOT / ".app.json"
MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
HOST_ADAPTERS = PLUGIN_ROOT / "host-adapters.json"
BRIDGE_PROFILE = PLUGIN_ROOT / "adapters/chatgpt/github-pull-runtime.json"
RUNTIME_PROBE = PLUGIN_ROOT / "adapters/chatgpt/RUNTIME_PROBE.md"
HOST_10WAY = PLUGIN_ROOT / "adapters/chatgpt/HOST_LIVE_10WAY.md"
TEN_WAY_CONFIG = ROOT / "control-plane/ai-system/configs/ten-way-unanimity-mode.json"
TEN_WAY_VALIDATOR = ROOT / "control-plane/scripts/validate_ten_way_unanimity_mode.py"
EXPECTED_PLUGIN = "ai-efficiency-operating-system"
EXPECTED_CONNECTOR = "connector_76869538009648d5b282a4bb21c3d157"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def _load(path: pathlib.Path, code: str, failures: list[str]) -> dict:
    if not path.is_file():
        failures.append(f"missing:{code}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        failures.append(f"invalid_json:{code}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"not_object:{code}")
        return {}
    return value


def _require(condition: bool, code: str, failures: list[str]) -> None:
    if not condition:
        failures.append(code)


def validate() -> list[str]:
    failures: list[str] = []
    plugin = _load(PLUGIN_MANIFEST, "plugin_manifest", failures)
    app = _load(APP_MANIFEST, "app_manifest", failures)
    marketplace = _load(MARKETPLACE, "marketplace", failures)
    adapters = _load(HOST_ADAPTERS, "host_adapters", failures)
    bridge = _load(BRIDGE_PROFILE, "bridge_profile", failures)
    ten_way = _load(TEN_WAY_CONFIG, "ten_way_config", failures)
    if failures:
        return sorted(set(failures))

    _require(plugin.get("name") == EXPECTED_PLUGIN, "plugin_name_mismatch", failures)
    version = plugin.get("version")
    _require(isinstance(version, str) and SEMVER.fullmatch(version) is not None, "plugin_version_invalid", failures)
    author = plugin.get("author")
    _require(isinstance(author, dict) and isinstance(author.get("name"), str) and bool(author.get("name", "").strip()), "plugin_author_name_missing", failures)
    _require(plugin.get("skills") == "./skills/", "plugin_skills_path_invalid", failures)
    _require(plugin.get("apps") == "./.app.json", "plugin_apps_path_invalid", failures)
    interface = plugin.get("interface") or {}
    capabilities = set(interface.get("capabilities") or [])
    _require({"Interactive", "Write"}.issubset(capabilities), "plugin_write_capability_missing", failures)
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        _require(isinstance(interface.get(key), str) and bool(interface.get(key, "").strip()), f"plugin_interface_missing:{key}", failures)
    prompts = interface.get("defaultPrompt")
    _require(isinstance(prompts, list) and 1 <= len(prompts) <= 3 and all(isinstance(x, str) and x.strip() for x in prompts), "plugin_default_prompt_invalid", failures)

    apps = app.get("apps")
    github = apps.get("github") if isinstance(apps, dict) else None
    _require(isinstance(github, dict), "github_app_alias_missing", failures)
    if isinstance(github, dict):
        _require(github.get("id") == EXPECTED_CONNECTOR, "github_connector_id_mismatch", failures)
        _require(set(github).issubset({"id", "category"}), "github_app_manifest_nonportable_fields", failures)

    entries = marketplace.get("plugins")
    entries = entries if isinstance(entries, list) else []
    matches = [item for item in entries if isinstance(item, dict) and item.get("name") == EXPECTED_PLUGIN]
    _require(len(matches) == 1, "marketplace_plugin_entry_count_invalid", failures)
    if len(matches) == 1:
        entry = matches[0]
        source = entry.get("source") or {}
        policy = entry.get("policy") or {}
        _require(source.get("source") == "local", "marketplace_source_type_invalid", failures)
        _require(source.get("path") == "./plugins/ai-efficiency-operating-system", "marketplace_source_path_invalid", failures)
        _require(policy.get("installation") == "AVAILABLE", "marketplace_installation_policy_invalid", failures)
        _require(policy.get("authentication") == "ON_INSTALL", "marketplace_authentication_policy_missing", failures)
        _require(entry.get("category") == "Productivity", "marketplace_category_invalid", failures)

    adapter_items = adapters.get("adapters")
    adapter_items = adapter_items if isinstance(adapter_items, list) else []
    bridge_adapters = [item for item in adapter_items if isinstance(item, dict) and item.get("name") == "github-pull-runtime"]
    _require(len(bridge_adapters) == 1, "github_host_adapter_registration_invalid", failures)
    if len(bridge_adapters) == 1:
        item = bridge_adapters[0]
        _require(item.get("host") == "ordinary-chatgpt", "github_host_adapter_host_invalid", failures)
        _require(item.get("app_manifest") == ".app.json", "github_host_adapter_app_manifest_invalid", failures)
        _require(item.get("app_alias") == "github", "github_host_adapter_alias_invalid", failures)
        _require(item.get("connector_id") == EXPECTED_CONNECTOR, "github_host_adapter_connector_mismatch", failures)
        _require(item.get("runtime_policy") == "adapters/chatgpt/github-pull-runtime.json", "github_host_adapter_runtime_policy_invalid", failures)

    _require(bridge.get("profile_id") == "ordinary-chatgpt-github-pull-v1", "bridge_profile_id_invalid", failures)
    _require(bridge.get("host") == "ordinary-chatgpt", "bridge_host_invalid", failures)
    _require(bridge.get("plugin") == EXPECTED_PLUGIN, "bridge_plugin_invalid", failures)
    _require(bridge.get("app_alias") == "github", "bridge_app_alias_invalid", failures)
    _require(bridge.get("connector_id") == EXPECTED_CONNECTOR, "bridge_connector_id_mismatch", failures)
    activation = bridge.get("activation_chain") or []
    for stage in ("marketplace_imported_or_synced", "github_app_connected", "tool_namespace_visible", "tool_invoked", "response_classified", "requested_effect_verified"):
        _require(stage in activation, f"bridge_activation_stage_missing:{stage}", failures)
    pull = bridge.get("pull_resolution") or {}
    _require(pull.get("search_miss_is_not_absence") is True, "bridge_search_miss_can_mean_absence", failures)
    _require(pull.get("two_same_mechanism_failures_require_route_change") is True, "bridge_stagnant_retry_allowed", failures)
    fallback = set(pull.get("fallback_routes") or [])
    for route in ("exact_repository_lookup", "direct_file_fetch", "code_search", "tree_or_contents_lookup", "known_url_or_ref_resolution"):
        _require(route in fallback, f"bridge_fallback_missing:{route}", failures)
    response = bridge.get("response_contract") or {}
    for key in ("transport_success_is_not_task_success", "empty_or_truncated_response_requires_targeted_refetch", "tool_error_must_preserve_error_code_and_target_identity", "partial_success_must_not_be_promoted_to_pass", "unknown_fields_or_response_shape_change_must_be_classified_before_retry"):
        _require(response.get(key) is True, f"bridge_response_contract_missing:{key}", failures)
    write = bridge.get("write_contract") or {}
    for key in ("prewrite_read_required", "current_blob_sha_required_for_update_or_delete", "dependent_same_path_writes_must_be_sequential", "stale_blob_sha_conflict_is_expected_detectable_failure", "readback_after_material_write", "readback_must_match_target_branch_and_intended_content", "commit_sha_alone_is_not_completion", "rollback_revision_recorded_before_first_write"):
        _require(write.get(key) is True, f"bridge_write_contract_missing:{key}", failures)

    host = ten_way.get("chatgpt_host_live") or {}
    _require(host.get("plugin_manifest") == "plugins/ai-efficiency-operating-system/.codex-plugin/plugin.json", "ten_way_plugin_manifest_not_canonical", failures)
    _require(host.get("plugin_version_source") == "plugin_manifest.version", "ten_way_plugin_version_not_manifest_derived", failures)
    _require("plugin_version" not in host, "ten_way_duplicate_version_constant_present", failures)
    _require(host.get("github_bridge_profile") == "plugins/ai-efficiency-operating-system/adapters/chatgpt/github-pull-runtime.json", "ten_way_bridge_profile_not_canonical", failures)
    _require(host.get("github_bridge_required_when_github_task") is True, "ten_way_github_bridge_not_required", failures)

    for path, markers in [
        (RUNTIME_PROBE, ["single package-version source of truth", "CHATGPT_GITHUB_BRIDGE_VERIFIED", "stale-SHA"]),
        (HOST_10WAY, ["duplicated hard-coded package version is forbidden", "Required GitHub bridge probe"]),
        (TEN_WAY_VALIDATOR, ["plugin_version_source", "GITHUB_APP_MANIFEST", "github-bridge=bound"]),
    ]:
        if not path.is_file():
            failures.append(f"missing:{path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            _require(marker.lower() in text.lower(), f"marker_missing:{path.name}:{marker}", failures)

    stale_targets = [RUNTIME_PROBE, HOST_10WAY, TEN_WAY_CONFIG, TEN_WAY_VALIDATOR]
    for path in stale_targets:
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        _require('"1.2.0"' not in text and "`1.2.0`" not in text, f"stale_plugin_version_literal:{path.name}", failures)

    return sorted(set(failures))


def main() -> int:
    failures = validate()
    if failures:
        for failure in failures:
            print("FAIL", failure)
        return 1
    plugin = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    print(f"PASS ordinary-chatgpt-github-bridge plugin={plugin['name']} version={plugin['version']} connector={EXPECTED_CONNECTOR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
