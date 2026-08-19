#!/usr/bin/env python3
"""Executable deterministic policy evals for RC1 truth boundaries.

These tests validate policy logic only. They do not evaluate model reasoning quality
and do not constitute host-live or authentic multi-agent execution evidence.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

TERMINAL = {"VERIFIED", "HOST_LIVE_VERIFIED", "DEPLOYED", "HEALTHY", "STABLE"}


@dataclass
class Result:
    case: str
    passed: bool
    decision: str
    detail: str


def completion_gate(*, implemented: bool, runtime_executed: bool, tests_executed: bool,
                    tests_passed: bool, host_verified: bool, deployed: bool, healthy: bool) -> str:
    if healthy and deployed and host_verified and tests_executed and tests_passed:
        return "HEALTHY"
    if deployed and host_verified and tests_executed and tests_passed:
        return "DEPLOYED"
    if host_verified and tests_executed and tests_passed:
        return "HOST_LIVE_VERIFIED"
    if runtime_executed and tests_executed and tests_passed:
        return "VERIFIED"
    if tests_executed and tests_passed:
        return "TESTED"
    if implemented:
        return "IMPLEMENTED"
    return "DRAFTED"


def ci_classification(*, conclusion: str, steps_observed: bool, billing_annotation: bool) -> str:
    if conclusion == "failure" and not steps_observed:
        return "BLOCKED_BY_BILLING_OR_SPENDING_LIMIT" if billing_annotation else "PRE_STEP_INFRA_FAILURE"
    if conclusion == "failure" and steps_observed:
        return "TEST_OR_WORKFLOW_FAILURE"
    if conclusion == "success" and steps_observed:
        return "CI_EXECUTED_SUCCESS"
    return "UNKNOWN"


def independence_credit(*, role_labels: int, distinct_runtime_attestations: int) -> str:
    if distinct_runtime_attestations >= role_labels and role_labels > 1:
        return "RUNTIME_INDEPENDENCE_EVIDENCED"
    if role_labels > 1:
        return "LOGICAL_ROLE_DIVERSITY_ONLY"
    return "SINGLE_ACTOR"


def capability_state(*, visible: bool, permission_observed: bool, successful_readback_after_write: bool) -> str:
    if not visible:
        return "NOT_VISIBLE"
    if not permission_observed:
        return "VISIBLE_AUTH_UNKNOWN"
    if not successful_readback_after_write:
        return "AUTHORIZED_UNVERIFIED"
    return "VISIBLE_AUTHORIZED_VERIFIED"


def resume_decision(*, irreversible_action_receipt: bool, action_pending: bool) -> str:
    if irreversible_action_receipt and action_pending:
        return "REHYDRATE_AND_DO_NOT_REPLAY_COMPLETED_ACTION"
    if action_pending:
        return "EXECUTE_PENDING_ACTION"
    return "NO_ACTION_REQUIRED"


def main() -> int:
    results: list[Result] = []

    status = completion_gate(
        implemented=True, runtime_executed=False, tests_executed=False,
        tests_passed=False, host_verified=False, deployed=False, healthy=False,
    )
    results.append(Result("false-completion-001", status == "IMPLEMENTED", status,
                          "file write without runtime/test evidence must stop at IMPLEMENTED"))

    ci = ci_classification(conclusion="failure", steps_observed=False, billing_annotation=True)
    results.append(Result("prestep-infrastructure-001", ci == "BLOCKED_BY_BILLING_OR_SPENDING_LIMIT", ci,
                          "pre-step failure must not be mislabeled as TEST_FAILED"))

    ind = independence_credit(role_labels=10, distinct_runtime_attestations=0)
    results.append(Result("role-label-independence-001", ind == "LOGICAL_ROLE_DIVERSITY_ONLY", ind,
                          "role labels alone are not runtime independence evidence"))

    cap = capability_state(visible=True, permission_observed=False, successful_readback_after_write=False)
    results.append(Result("visible-not-authorized-001", cap == "VISIBLE_AUTH_UNKNOWN", cap,
                          "schema visibility does not prove authorization"))

    cap2 = capability_state(visible=True, permission_observed=True, successful_readback_after_write=False)
    results.append(Result("read-does-not-prove-write-001", cap2 == "AUTHORIZED_UNVERIFIED", cap2,
                          "permission/read evidence without successful mutation read-back is not VERIFIED"))

    resume = resume_decision(irreversible_action_receipt=True, action_pending=True)
    results.append(Result("resume-001", resume == "REHYDRATE_AND_DO_NOT_REPLAY_COMPLETED_ACTION", resume,
                          "durable receipt blocks duplicate irreversible replay"))

    highest = completion_gate(
        implemented=True, runtime_executed=True, tests_executed=True,
        tests_passed=True, host_verified=False, deployed=False, healthy=False,
    )
    results.append(Result("status-separation-001", highest == "VERIFIED", highest,
                          "passing runtime/tests does not imply host-live/deployed/healthy"))

    failed = [r for r in results if not r.passed]
    output = {
        "suite": "rc1-deterministic-policy-evals",
        "scope": "policy-logic-only",
        "semantic_agent_evals": "NOT_RUN",
        "authentic_multi_agent_runtime": "NOT_RUN",
        "host_live_verified": False,
        "cases": [asdict(r) for r in results],
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "status": "PASS_POLICY" if not failed else "FAIL_POLICY",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
