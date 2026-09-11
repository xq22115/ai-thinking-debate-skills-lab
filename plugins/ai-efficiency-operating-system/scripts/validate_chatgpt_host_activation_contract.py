#!/usr/bin/env python3
"""Fail-closed validator for repository-to-ordinary-ChatGPT plugin activation readiness."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
MARKETPLACE = REPO / ".agents" / "plugins" / "marketplace.json"
PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
SETTINGS = ROOT / "settings.json"
ACTIVATION = ROOT / "adapters" / "chatgpt" / "HOST_ACTIVATION_PROBE.md"
UPSTREAM = ROOT / "adapters" / "chatgpt" / "github-upstream-capability-contract.json"
HOST_ADAPTERS = ROOT / "host-adapters.json"
EXPECTED_NAME = "ai-efficiency-operating-system"
EXPECTED_SOURCE_PATH = "./plugins/ai-efficiency-operating-system"


def main():
    errors = []
    for path in (MARKETPLACE, PLUGIN, SETTINGS, ACTIVATION, UPSTREAM, HOST_ADAPTERS):
        if not path.exists():
            errors.append(f"missing:{path.relative_to(REPO)}")
    if errors:
        print("CHATGPT HOST ACTIVATION CONTRACT FAIL")
        for error in errors:
            print("-", error)
        return 1

    marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    plugin = json.loads(PLUGIN.read_text(encoding="utf-8"))
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))
    adapters = json.loads(HOST_ADAPTERS.read_text(encoding="utf-8"))
    activation_text = ACTIVATION.read_text(encoding="utf-8")

    if plugin.get("name") != EXPECTED_NAME:
        errors.append("plugin name drift")
    if plugin.get("version") != settings.get("version"):
        errors.append("plugin/settings version drift")
    if plugin.get("version") != "1.4.1":
        errors.append("host-activation correction must publish package version 1.4.1")

    matches = [row for row in marketplace.get("plugins", []) if row.get("name") == EXPECTED_NAME]
    if len(matches) != 1:
        errors.append("marketplace must contain exactly one ai-efficiency-operating-system entry")
    else:
        entry = matches[0]
        source = entry.get("source") or {}
        policy = entry.get("policy") or {}
        if source.get("source") != "local":
            errors.append("marketplace source kind must remain local")
        if source.get("path") != EXPECTED_SOURCE_PATH:
            errors.append("marketplace source path drift")
        if policy.get("installation") != "AVAILABLE":
            errors.append("marketplace installation policy must remain AVAILABLE")
        if policy.get("authentication") != "ON_INSTALL":
            errors.append("marketplace authentication policy must remain ON_INSTALL")

    activation_truth = upstream.get("local_package_activation_truth") or {}
    if activation_truth.get("custom_plugin_host_live_status") != "UNVERIFIED":
        errors.append("repository package must not preclaim ChatGPT HOST_LIVE")
    if activation_truth.get("repository_marketplace_presence_does_not_prove_chatgpt_import") is not True:
        errors.append("marketplace presence/import truth boundary missing")

    activation_contract = upstream.get("activation_contract") or {}
    if activation_contract.get("github_marketplace_import_is_host_admin_operation") is not True:
        errors.append("marketplace import host/admin boundary missing")
    if activation_contract.get("github_marketplace_sync_is_not_git_push") is not True:
        errors.append("Git push vs marketplace sync boundary missing")

    github_adapters = [
        row for row in (adapters.get("adapters") or [])
        if isinstance(row, dict) and row.get("name") == "github-pull-runtime"
    ]
    if len(github_adapters) != 1:
        errors.append("GitHub host adapter must resolve exactly once")
    else:
        adapter = github_adapters[0]
        if adapter.get("host_activation_required_for_local_skill_effect") is not True:
            errors.append("host activation gate missing from adapter")
        if adapter.get("repo_package_is_not_host_installation") is not True:
            errors.append("repo-package/install separation missing from adapter")
        if adapter.get("current_local_plugin_host_live_status") != "UNVERIFIED":
            errors.append("adapter must not preclaim local plugin HOST_LIVE")

    for marker in (
        "GIT REPO -> MARKETPLACE CATALOG -> CHATGPT MARKETPLACE IMPORT/SYNC",
        "Git push is not sync evidence",
        "CUSTOM_PLUGIN_ACTIVATION_UNVERIFIED",
        "HOST_IMPORT_BLOCKED",
        "canonical GitHub connector and this local orchestration plugin are separate activation dimensions",
        "CHATGPT_LOCAL_PLUGIN_HOST_LIVE",
    ):
        if marker.lower() not in activation_text.lower():
            errors.append(f"activation probe marker missing:{marker}")

    if errors:
        print("CHATGPT HOST ACTIVATION CONTRACT FAIL")
        for error in errors:
            print("-", error)
        return 1

    print("CHATGPT HOST ACTIVATION CONTRACT PASS")
    print(f"plugin={EXPECTED_NAME} version={plugin['version']} host_live=UNVERIFIED marketplace_ready=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
