#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONFIG = ROOT / "control-plane/ai-system/configs/ten-way-unanimity-mode.json"
EXECUTOR = ROOT / "control-plane/scripts/local_agent_executor.py"
HOST_DOC = ROOT / "plugins/ai-efficiency-operating-system/adapters/chatgpt/HOST_LIVE_10WAY.md"


def require(condition: bool, code: str, failures: list[str]) -> None:
    if not condition:
        failures.append(code)


def main() -> int:
    failures: list[str] = []
    if not CONFIG.is_file():
        print("FAIL ten_way_config_missing")
        return 1
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    require(cfg.get("schema_version") == 1, "ten_way_schema_version", failures)
    require(cfg.get("default_enabled") is False, "ten_way_must_be_explicit", failures)
    require(cfg.get("activation") == "explicit_user_request", "ten_way_activation_drift", failures)
    require(cfg.get("required_actor_count") == 10, "ten_way_actor_count_drift", failures)
    require(cfg.get("max_parallel") == 10, "ten_way_parallelism_drift", failures)
    require(cfg.get("require_all_concurrent") is True, "ten_way_concurrency_not_required", failures)
    require(cfg.get("common_runtime_overlap_required") is True, "ten_way_overlap_not_required", failures)
    require(cfg.get("all_agents_must_pass") is True, "ten_way_unanimity_not_required", failures)
    require(cfg.get("veto_tolerance") == 0, "ten_way_veto_tolerance_nonzero", failures)
    require(cfg.get("missing_actor_tolerance") == 0, "ten_way_missing_actor_tolerance_nonzero", failures)

    identity = cfg.get("identity_requirements") or {}
    for key in [
        "distinct_process_instance_ids",
        "distinct_execution_ids",
        "distinct_backend_session_ids",
        "distinct_workspaces",
        "model_self_asserted_independence_is_not_evidence",
    ]:
        require(identity.get(key) is True, f"ten_way_identity_missing:{key}", failures)

    temporal = cfg.get("temporal_proof") or {}
    require(temporal.get("per_actor_start_field") == "spawn_monotonic_ns", "ten_way_start_field_drift", failures)
    require(temporal.get("per_actor_finish_field") == "finish_monotonic_ns", "ten_way_finish_field_drift", failures)
    require(temporal.get("aggregate_field") == "concurrency.common_overlap_proven", "ten_way_overlap_field_drift", failures)
    require(temporal.get("strict_failure_code") == "ten_way_common_overlap_missing", "ten_way_failure_code_drift", failures)

    host = cfg.get("chatgpt_host_live") or {}
    require(host.get("target_surfaces") == ["chatgpt_web", "chatgpt_desktop"], "ten_way_surface_set_drift", failures)
    require(host.get("same_plugin_revision_required") is True, "ten_way_same_revision_not_required", failures)
    require(host.get("plugin_name") == "ai-efficiency-operating-system", "ten_way_plugin_name_drift", failures)
    require(host.get("plugin_version") == "1.1.0-rc1", "ten_way_plugin_version_drift", failures)
    require(host.get("repository_merge_commit") == "5c2b940c06c97c3ee48e9cdb8e66617032bb1ad2", "ten_way_plugin_commit_drift", failures)
    require(host.get("surface_evidence_required_before_agent_pass") is True, "ten_way_surface_evidence_not_required", failures)
    require(host.get("repository_or_ci_success_alone_is_host_live") is False, "ten_way_repo_can_fake_host_live", failures)
    require(host.get("web_and_desktop_both_required") is True, "ten_way_dual_surface_not_required", failures)

    lanes = cfg.get("ten_validation_lanes") or []
    require(len(lanes) == 10, "ten_way_lane_count_drift", failures)
    require(len(set(lanes)) == 10, "ten_way_lane_duplicate", failures)

    release = cfg.get("release") or {}
    required = set(release.get("pass_requires") or [])
    for item in [
        "ten_distinct_actor_receipts",
        "ten_PASS_decisions",
        "common_runtime_overlap_proven",
        "chatgpt_web_host_live_evidence",
        "chatgpt_desktop_host_live_evidence",
        "same_exact_plugin_revision_on_both_surfaces",
    ]:
        require(item in required, f"ten_way_release_requirement_missing:{item}", failures)
    require(release.get("blocked_or_not_run_must_not_be_relabelled_pass") is True, "ten_way_blocked_can_fake_pass", failures)
    require(release.get("host_import_blocked_is_PASS") is False, "ten_way_import_blocked_can_pass", failures)

    text = EXECUTOR.read_text(encoding="utf-8") if EXECUTOR.is_file() else ""
    for marker in ["require_all_concurrent", "finish_monotonic_ns", "common_overlap_proven", "ten_way_common_overlap_missing"]:
        require(marker in text, f"ten_way_executor_marker_missing:{marker}", failures)

    if not HOST_DOC.is_file():
        failures.append("ten_way_host_doc_missing")
    else:
        doc = HOST_DOC.read_text(encoding="utf-8")
        for marker in ["ChatGPT Web", "ChatGPT Desktop", "10/10", "common runtime overlap", "HOST_IMPORT_BLOCKED"]:
            require(marker in doc, f"ten_way_host_doc_marker_missing:{marker}", failures)

    if failures:
        for failure in failures:
            print("FAIL", failure)
        return 1
    print("PASS ten-way-concurrent-unanimity-v1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
