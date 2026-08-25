# Debate 03 — Agent Runtime

## Position
Keep the repository's A01–A10 local workflow as the primary long-loop runtime. Add external runtimes only as optional adapters.

## Evidence From This Repo
`run_local_agent_workflow.py` already provides dependency-aware waves, parallel actors, backend authentication probes, independent process/session attestations, resumable receipts, finalization, adjudication, and base-freshness gates.

## Adopt
1. Treat A01–A10 as the trusted execution kernel.
2. Add an ordinary-chat launcher and capability/status interface around it.
3. Make concurrency, timeouts, budget, model, and resume behavior explicit inputs with safe caps.
4. Preserve PASS / FAIL / VETO / BLOCKED semantics end-to-end.
5. Consider OpenHands only as an optional secondary adapter for developer GUI or isolated workspace scenarios.

## Reject
- Replacing the mature executor just because another agent framework is popular.
- Running agent processes without receipts/finalization.
- Host-filesystem unrestricted mode as the default for third-party runtimes.
- Equating 'continuous thinking' text with an autonomous execution loop.

## Acceptance
PASS when ordinary chat can launch and observe the existing workflow without weakening its dependency, attestation, receipt, freshness, and veto gates.
