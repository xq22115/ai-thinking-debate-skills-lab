#!/usr/bin/env python3
"""Prepare and validate one frozen DS/DSP/DSG evaluation campaign packet.

This module composes the existing provider-neutral run preparer and execution
receipt template generator. It does not call a model provider or judge.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from run_semantic_dialogue_state_eval import (
    ARMS,
    FIXTURES,
    PROTECTION_FIXTURES,
    ROOT,
    load_json,
    load_jsonl,
    prepare,
    stable_id,
)
from validate_semantic_dialogue_state_execution import prepare_template

GENERALIZATION_FIXTURES = ROOT / "skills/evals/semantic-dialogue-state-generalization-holdout.json"
CORE_TREATMENT_ARMS = ("microscope-core", "microscope-dialogue-state")

SUITE_CONFIG: dict[str, dict[str, Any]] = {
    "target": {
        "fixture": FIXTURES,
        "arms": ARMS,
        "run_suite_role": "target",
    },
    "protection": {
        "fixture": PROTECTION_FIXTURES,
        "arms": CORE_TREATMENT_ARMS,
        "run_suite_role": "protection",
    },
    "generalization": {
        "fixture": GENERALIZATION_FIXTURES,
        "arms": CORE_TREATMENT_ARMS,
        # The existing promotion gate treats DSG as a protection-role report.
        "run_suite_role": "protection",
    },
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def require_int(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label} must be an integer")
    return value


def resolve_child(campaign_dir: Path, relative: str, label: str) -> Path:
    child = (campaign_dir / relative).resolve()
    root = campaign_dir.resolve()
    if child != root and root not in child.parents:
        raise ValueError(f"{label} escapes campaign directory")
    return child


def prepare_campaign(
    campaign_dir: Path,
    repo_ref: str,
    model_id: str,
    provider: str,
    seed: int,
    campaign_id: str | None = None,
) -> dict[str, Any]:
    """Prepare three linked runs with one frozen identity and receipt templates."""

    repo_ref = require_text(repo_ref, "repo_ref")
    model_id = require_text(model_id, "model_id")
    provider = require_text(provider, "provider")
    seed = require_int(seed, "seed")

    if campaign_dir.exists() and any(campaign_dir.iterdir()):
        raise ValueError(f"campaign destination must be empty: {campaign_dir}")
    campaign_dir.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now(timezone.utc).isoformat()
    if campaign_id is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        campaign_id = (
            f"semantic-ds-campaign-{timestamp}-"
            f"{stable_id(repo_ref, model_id, provider, str(seed))[:8]}"
        )
    campaign_id = require_text(campaign_id, "campaign_id")

    suites: dict[str, dict[str, Any]] = {}
    for role, config in SUITE_CONFIG.items():
        run_dir = campaign_dir / role
        prepare(
            run_dir,
            repo_ref=repo_ref,
            model_id=model_id,
            provider=provider,
            seed=seed,
            fixture_path=config["fixture"],
            arms=tuple(config["arms"]),
        )
        template_path = prepare_template(run_dir)
        manifest = load_json(run_dir / "manifest.json")
        requests = load_jsonl(run_dir / "requests.jsonl")

        suites[role] = {
            "run_dir": role,
            "run_id": manifest["run_id"],
            "fixture_suite": manifest["fixture_suite"],
            "fixture_path": manifest["fixture_path"],
            "fixture_sha256": manifest["fixture_sha256"],
            "run_suite_role": manifest["suite_role"],
            "arms": manifest["arms"],
            "case_count": manifest["case_count"],
            "request_count": manifest["request_count"],
            "manifest_sha256": sha256_file(run_dir / "manifest.json"),
            "bundles_sha256": sha256_file(run_dir / "bundles.json"),
            "requests_sha256": sha256_file(run_dir / "requests.jsonl"),
            "execution_receipt_template_sha256": sha256_file(template_path),
            "request_ids_sha256": hashlib.sha256(
                "\n".join(row["request_id"] for row in requests).encode("utf-8")
            ).hexdigest(),
        }

    campaign = {
        "schema_version": 1,
        "campaign_id": campaign_id,
        "created_at": created_at,
        "repo_ref": repo_ref,
        "model_id": model_id,
        "provider": provider,
        "seed": seed,
        "suites": suites,
        "status": "PREPARED_NOT_EXECUTED",
        "status_boundary": (
            "CAMPAIGN_PACKET_VALID != TARGET_MODEL_RUN != INDEPENDENT_JUDGED "
            "!= REPEATED != HOST_LIVE"
        ),
    }
    dump_json(campaign_dir / "campaign_manifest.json", campaign)
    validate_campaign(campaign_dir)
    print(f"prepared semantic dialogue-state campaign {campaign_id} at {campaign_dir}")
    return campaign


def validate_campaign(campaign_dir: Path) -> dict[str, Any]:
    """Validate frozen campaign identity, suite shapes, hashes, and templates."""

    campaign_path = campaign_dir / "campaign_manifest.json"
    campaign = load_json(campaign_path)
    if not isinstance(campaign, dict):
        raise ValueError("campaign manifest root must be an object")

    campaign_id = require_text(campaign.get("campaign_id"), "campaign.campaign_id")
    repo_ref = require_text(campaign.get("repo_ref"), "campaign.repo_ref")
    model_id = require_text(campaign.get("model_id"), "campaign.model_id")
    provider = require_text(campaign.get("provider"), "campaign.provider")
    seed = require_int(campaign.get("seed"), "campaign.seed")

    suites = campaign.get("suites")
    if not isinstance(suites, dict) or set(suites) != set(SUITE_CONFIG):
        raise ValueError("campaign suites must be exactly target/protection/generalization")

    run_ids: set[str] = set()
    fixture_suites: set[str] = set()
    validated_requests = 0

    for role, config in SUITE_CONFIG.items():
        entry = suites[role]
        if not isinstance(entry, dict):
            raise ValueError(f"campaign suite {role} must be an object")
        run_dir_name = require_text(entry.get("run_dir"), f"campaign.suites.{role}.run_dir")
        if run_dir_name != role:
            raise ValueError(f"suite path drift: {role} run_dir must be {role}")
        run_dir = resolve_child(campaign_dir, run_dir_name, f"suite {role}")
        manifest_path = run_dir / "manifest.json"
        requests_path = run_dir / "requests.jsonl"
        bundles_path = run_dir / "bundles.json"
        template_path = run_dir / "execution_receipts.template.jsonl"
        for path in (manifest_path, requests_path, bundles_path, template_path):
            if not path.is_file():
                raise ValueError(f"campaign suite {role} missing {path.name}")

        manifest = load_json(manifest_path)
        if not isinstance(manifest, dict):
            raise ValueError(f"{role} manifest root must be an object")

        for field, expected in (
            ("repo_ref", repo_ref),
            ("model_id", model_id),
            ("provider", provider),
            ("seed", seed),
        ):
            if manifest.get(field) != expected:
                raise ValueError(
                    f"identity drift: {role}.{field}={manifest.get(field)!r} "
                    f"!= campaign {expected!r}"
                )

        expected_fixture = config["fixture"].relative_to(ROOT).as_posix()
        if manifest.get("fixture_path") != expected_fixture:
            raise ValueError(
                f"suite fixture drift: {role}={manifest.get('fixture_path')!r} "
                f"!= {expected_fixture!r}"
            )
        expected_arms = list(config["arms"])
        if manifest.get("arms") != expected_arms:
            raise ValueError(
                f"suite arm drift: {role}={manifest.get('arms')!r} != {expected_arms!r}"
            )
        if manifest.get("suite_role") != config["run_suite_role"]:
            raise ValueError(
                f"suite role drift: {role}={manifest.get('suite_role')!r} "
                f"!= {config['run_suite_role']!r}"
            )

        run_id = require_text(manifest.get("run_id"), f"{role}.run_id")
        if run_id in run_ids:
            raise ValueError(f"run_id collision across campaign suites: {run_id}")
        run_ids.add(run_id)
        fixture_suite = require_text(manifest.get("fixture_suite"), f"{role}.fixture_suite")
        if fixture_suite in fixture_suites:
            raise ValueError(f"fixture suite collision across campaign: {fixture_suite}")
        fixture_suites.add(fixture_suite)

        if entry.get("run_id") != run_id:
            raise ValueError(f"campaign link drift: {role}.run_id does not match run manifest")
        if entry.get("fixture_path") != manifest.get("fixture_path"):
            raise ValueError(f"campaign link drift: {role}.fixture_path does not match run manifest")
        if entry.get("fixture_sha256") != manifest.get("fixture_sha256"):
            raise ValueError(f"campaign link drift: {role}.fixture_sha256 does not match run manifest")
        if entry.get("arms") != manifest.get("arms"):
            raise ValueError(f"campaign link drift: {role}.arms does not match run manifest")
        if entry.get("run_suite_role") != manifest.get("suite_role"):
            raise ValueError(f"campaign link drift: {role}.run_suite_role does not match run manifest")

        hash_checks = {
            "manifest_sha256": manifest_path,
            "bundles_sha256": bundles_path,
            "requests_sha256": requests_path,
            "execution_receipt_template_sha256": template_path,
        }
        for field, path in hash_checks.items():
            actual = sha256_file(path)
            if entry.get(field) != actual:
                raise ValueError(f"campaign hash drift: {role}.{field}")

        requests = load_jsonl(requests_path)
        templates = load_jsonl(template_path)
        if len(requests) != manifest.get("request_count"):
            raise ValueError(f"request count drift: {role}")
        if len(templates) != len(requests):
            raise ValueError(f"receipt template count drift: {role}")
        if entry.get("request_count") != len(requests):
            raise ValueError(f"campaign request count drift: {role}")

        request_ids_hash = hashlib.sha256(
            "\n".join(row["request_id"] for row in requests).encode("utf-8")
        ).hexdigest()
        if entry.get("request_ids_sha256") != request_ids_hash:
            raise ValueError(f"request identity set drift: {role}")

        for request, template in zip(requests, templates):
            request_id = require_text(request.get("request_id"), f"{role}.request.request_id")
            for field, expected in (
                ("request_id", request_id),
                ("run_id", run_id),
                ("case_id", request.get("case_id")),
                ("arm", request.get("arm")),
                ("bundle_sha256", request.get("bundle_sha256")),
                ("model_id", model_id),
                ("provider", provider),
            ):
                if template.get(field) != expected:
                    raise ValueError(
                        f"receipt template drift: {role}.{request_id}.{field}"
                    )
            if template.get("fresh_context") is not None:
                raise ValueError(f"receipt template prematurely claims fresh context: {request_id}")
            if template.get("status") != "FILL_ME":
                raise ValueError(f"receipt template prematurely claims execution status: {request_id}")
        validated_requests += len(requests)

    result = {
        "schema_version": 1,
        "campaign_id": campaign_id,
        "repo_ref": repo_ref,
        "model_id": model_id,
        "provider": provider,
        "seed": seed,
        "suite_count": len(SUITE_CONFIG),
        "request_count": validated_requests,
        "decision": "CAMPAIGN_PACKET_VALID",
        "status_boundary": (
            "CAMPAIGN_PACKET_VALID == PREPARATION_INTEGRITY_ONLY; "
            "NOT TARGET_MODEL_RUN OR HOST_LIVE"
        ),
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return result


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="semantic-campaign-self-test-") as tmp:
        campaign_dir = Path(tmp) / "campaign"
        prepare_campaign(
            campaign_dir,
            repo_ref="synthetic-ref",
            model_id="synthetic-model",
            provider="synthetic-provider",
            seed=11,
            campaign_id="synthetic-campaign",
        )
        valid = validate_campaign(campaign_dir)
        assert valid["decision"] == "CAMPAIGN_PACKET_VALID"

        path = campaign_dir / "generalization" / "manifest.json"
        manifest = load_json(path)
        manifest["model_id"] = "drifted-model"
        dump_json(path, manifest)
        try:
            validate_campaign(campaign_dir)
        except ValueError as exc:
            assert "identity drift" in str(exc)
        else:
            raise AssertionError("identity drift must invalidate the campaign packet")

    print("semantic dialogue-state campaign packet self-test: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser("prepare")
    p_prepare.add_argument("campaign_dir", type=Path)
    p_prepare.add_argument("--repo-ref", required=True)
    p_prepare.add_argument("--model-id", required=True)
    p_prepare.add_argument("--provider", default="unknown")
    p_prepare.add_argument("--seed", type=int, default=0)
    p_prepare.add_argument("--campaign-id")

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("campaign_dir", type=Path)

    sub.add_parser("self-test")

    args = parser.parse_args()
    if args.command == "prepare":
        prepare_campaign(
            args.campaign_dir,
            repo_ref=args.repo_ref,
            model_id=args.model_id,
            provider=args.provider,
            seed=args.seed,
            campaign_id=args.campaign_id,
        )
    elif args.command == "validate":
        validate_campaign(args.campaign_dir)
    elif args.command == "self-test":
        self_test()


if __name__ == "__main__":
    main()
