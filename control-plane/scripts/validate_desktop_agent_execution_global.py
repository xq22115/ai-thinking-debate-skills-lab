#!/usr/bin/env python3
"""Fail-closed validation for the repository-wide desktop-agent execution policy."""
from __future__ import annotations

import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "control-plane/ai-system/configs/desktop-agent-execution-global.json"
DOC_PATH = REPO_ROOT / "docs/DESKTOP_AGENT_EXECUTION_POLICY.md"
AGENTS_PATH = REPO_ROOT / "AGENTS.md"


def require(condition: bool, code: str, failures: list[str]) -> None:
    if not condition:
        failures.append(code)


def load_json(path: pathlib.Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected_object:{path}")
    return value


def validate() -> list[str]:
    failures: list[str] = []
    for path, code in [
        (CONFIG_PATH, "desktop_config_missing"),
        (DOC_PATH, "desktop_policy_doc_missing"),
        (AGENTS_PATH, "root_agents_missing"),
    ]:
        if not path.is_file():
            failures.append(code)
    if failures:
        return failures

    try:
        config = load_json(CONFIG_PATH)
    except Exception as exc:
        return [f"desktop_config_invalid:{type(exc).__name__}:{exc}"]

    agents = AGENTS_PATH.read_text(encoding="utf-8")
    doc = DOC_PATH.read_text(encoding="utf-8")

    require(config.get("schema_version") == 1, "schema_version_mismatch", failures)
    require(config.get("default_enabled") is True, "desktop_profile_not_default_enabled", failures)

    foreground = config.get("foreground_non_interference") or {}
    require(foreground.get("default") is True, "foreground_non_interference_not_default", failures)
    require(foreground.get("forbid_focus_steal_for_inspection") is True, "focus_steal_allowed", failures)
    require(
        foreground.get("forbid_user_pointer_takeover_when_background_path_exists") is True,
        "user_pointer_takeover_allowed",
        failures,
    )
    require(
        foreground.get("prefer_target_window_capture_over_full_screen") is True,
        "target_window_capture_not_preferred",
        failures,
    )

    browser = config.get("local_browser") or {}
    require(browser.get("default_target") == "existing_local_chrome", "existing_local_chrome_not_default", failures)
    require(browser.get("preserve_authenticated_profile") is True, "authenticated_profile_not_preserved", failures)
    require(browser.get("private_aliases_must_be_local_untracked") is True, "private_aliases_can_be_committed", failures)
    chrome = browser.get("chrome_136_plus") or {}
    require(
        chrome.get("default_data_dir_remote_debugging_assumed_supported") is False,
        "default_profile_cdp_incorrectly_assumed_supported",
        failures,
    )
    require(
        chrome.get("do_not_relaunch_real_profile_with_debug_port_as_default") is True,
        "real_profile_debug_relaunch_allowed_by_default",
        failures,
    )

    target = config.get("target_identity_gate") or {}
    required_signals = {
        "requested_identity",
        "process_identity",
        "filesystem_or_install_identity",
        "session_or_ui_identity",
        "runtime_functional_identity",
    }
    require(
        required_signals.issubset(set(target.get("required_signal_families") or [])),
        "five_signal_target_gate_incomplete",
        failures,
    )
    require(target.get("conflict_behavior") == "fail_closed_before_write", "target_conflict_not_fail_closed", failures)
    require(target.get("name_match_alone_sufficient") is False, "name_match_can_authorize_write", failures)
    require(
        (target.get("antigravity") or {}).get("material_edit_requires_five_signal_gate") is True,
        "antigravity_five_signal_gate_missing",
        failures,
    )

    devices = config.get("multi_device_isolation") or {}
    require(devices.get("simultaneous_online_allowed") is True, "dual_device_online_not_allowed", failures)
    require(devices.get("device_id_alone_is_proof") is False, "device_id_trusted_without_fingerprint", failures)
    require(devices.get("prewrite_fingerprint_required") is True, "prewrite_device_fingerprint_missing", failures)
    required_fingerprint = {
        "expected_device_identifier_or_alias",
        "hostname",
        "operating_system",
        "home_or_user_root_path",
        "device_specific_read_only_sentinel",
    }
    require(
        required_fingerprint.issubset(set(devices.get("fingerprint_fields") or [])),
        "device_fingerprint_incomplete",
        failures,
    )
    require(devices.get("fingerprint_mismatch_behavior") == "abort_write", "device_mismatch_not_fail_closed", failures)
    affinity = devices.get("stateful_session_affinity") or {}
    require(affinity.get("persist_device_fingerprint_with_session_id") is True, "session_device_binding_missing", failures)
    require(affinity.get("verify_before_follow_up") is True, "session_affinity_not_reverified", failures)

    parallel = config.get("parallel_work") or {}
    require(parallel.get("maximum_default_distinct_lanes") == 5, "five_lane_parallel_cap_drift", failures)
    require(parallel.get("require_causal_distinction") is True, "parallel_lanes_need_not_be_distinct", failures)
    require(parallel.get("shared_evidence_ledger_required") is True, "parallel_evidence_ledger_missing", failures)
    require(parallel.get("lane_may_not_silently_redefine_target") is True, "parallel_target_drift_allowed", failures)

    failure = config.get("failure_learning") or {}
    require(failure.get("materially_similar_failure_limit") == 2, "two_strike_pivot_missing", failures)
    require(failure.get("repeat_same_mechanism_after_limit") is False, "stagnant_retry_allowed", failures)

    research = config.get("research") or {}
    require(research.get("conversation_memory_alone_is_authority") is False, "memory_only_authority_allowed", failures)
    require(research.get("independent_corroboration_required_when_material") is True, "cross_source_corroboration_missing", failures)

    preservation = config.get("capability_preservation") or {}
    require(preservation.get("obvious_degradation_is_default_fix") is False, "obvious_degradation_defaulted", failures)

    release = config.get("release") or {}
    require(release.get("no_connected_real_machine_is_blocked") is True, "offline_machine_can_fake_pass", failures)
    require(
        release.get("blocked_or_not_run_must_not_be_relabelled_pass") is True,
        "blocked_or_not_run_can_fake_pass",
        failures,
    )

    for token, code in [
        ("docs/DESKTOP_AGENT_EXECUTION_POLICY.md", "agents_desktop_policy_reference_missing"),
        ("control-plane/ai-system/configs/desktop-agent-execution-global.json", "agents_desktop_config_reference_missing"),
    ]:
        require(token in agents, code, failures)

    for token, code in [
        ("Chrome 136+", "chrome_136_constraint_not_documented"),
        ("Five-signal target identity gate", "five_signal_gate_not_documented"),
        ("Mac/Windows dual-lane isolation", "dual_lane_isolation_not_documented"),
        ("wrong-device routing", "remote_routing_failure_mode_not_documented"),
        ("Foreground non-interference", "foreground_non_interference_not_documented"),
    ]:
        require(token in doc, code, failures)

    return failures


def main() -> int:
    failures = validate()
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("PASS desktop-agent-execution-global")
    return 0


if __name__ == "__main__":
    sys.exit(main())
