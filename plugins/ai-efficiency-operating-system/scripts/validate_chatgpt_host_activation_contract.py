#!/usr/bin/env python3
"""Fail-closed validator for repository-to-ordinary-ChatGPT plugin activation readiness."""

import json
import re
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
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")


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
    activation_text = ACTIVATION.read_text(encoding="utf-8").lower()

    if plugin.get("name") != EXPECTED_NAME:
        errors.append("plugin name drift")
    version = plugin.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append("plugin version must be canonical SemVer")
    if version != settings.get("version"):
        errors.append("plugin/settings version drift")

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
        # Repository catalog metadata is validated for drift only. It is never
        # accepted as proof of the workspace's effective install/auth state.
        if policy.get("installation") != "AVAILABLE":
            errors.append("repository marketplace installation metadata drift")
        if policy.get("authentication") != "ON_INSTALL":
            errors.append("repository marketplace authentication metadata drift")

    activation_truth = upstream.get("local_package_activation_truth") or {}
    if activation_truth.get("custom_plugin_host_live_status") != "UNVERIFIED":
        errors.append("repository package must not preclaim ChatGPT HOST_LIVE")
    for key in (
        "repository_marketplace_presence_does_not_prove_chatgpt_import",
        "repository_marketplace_policy_values_do_not_set_workspace_effective_policy",
    ):
        if activation_truth.get(key) is not True:
            errors.append(f"missing marketplace activation truth:{key}")

    activation_contract = upstream.get("activation_contract") or {}
    for key in (
        "github_marketplace_import_is_host_admin_operation",
        "github_marketplace_sync_is_not_git_push",
        "repository_marketplace_policy_values_are_not_workspace_effective_policy",
        "workspace_settings_control_installation_and_authentication",
        "marketplace_import_or_sync_does_not_connect_member_accounts",
        "marketplace_import_or_sync_does_not_grant_required_app_access",
    ):
        if activation_contract.get(key) is not True:
            errors.append(f"missing host activation boundary:{key}")

    required = set(activation_contract.get("before_claiming_local_skill_effect_in_ordinary_chat") or [])
    for item in (
        "workspace_effective_installation_policy_observed",
        "required_app_enabled_and_accessible_for_member_role",
        "member_authentication_observed_if_required",
        "skill_or_plugin_visible_on_current_surface",
        "behavioral_probe_exercises_the_loaded_revision",
    ):
        if item not in required:
            errors.append(f"missing host activation evidence requirement:{item}")

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

    # Human probe checks intentionally target semantic invariants rather than
    # one brittle sentence shape. Changing prose must not weaken these claims.
    semantic_markers = (
        "git repo -> marketplace catalog -> chatgpt marketplace import/sync",
        "repository marketplace policy is not workspace effective policy",
        "does not connect members' provider accounts",
        "does not grant required-app access",
        "git push is not sync evidence",
        "custom_plugin_activation_unverified",
        "host_import_blocked",
        "canonical github connector and this local orchestration plugin are separate activation dimensions",
        "chatgpt_local_plugin_host_live",
    )
    for marker in semantic_markers:
        if marker not in activation_text:
            errors.append(f"activation probe semantic invariant missing:{marker}")

    if errors:
        print("CHATGPT HOST ACTIVATION CONTRACT FAIL")
        for error in errors:
            print("-", error)
        return 1

    print("CHATGPT HOST ACTIVATION CONTRACT PASS")
    print(f"plugin={EXPECTED_NAME} version={version} host_live=UNVERIFIED marketplace_ready=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
