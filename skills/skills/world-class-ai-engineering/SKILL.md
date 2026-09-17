---
name: world-class-ai-engineering
description: Use when designing, debugging, reviewing, hardening, or shipping agentic or LLM systems where runtime truth, tool or MCP behavior, evaluation, durability, observability, security, performance, or cross-host portability materially affect correctness.
---

# World-Class AI Engineering

Version: `0.1.0-rc1`

Status: `EXPERIMENTAL / PORTABLE SPECIALIST`

## Purpose

Treat AI engineering as an end-to-end systems discipline, not prompt writing plus a successful tool call. The unit of correctness is the observable user/runtime outcome on the exact reported state.

This skill is **not** a replacement orchestrator. Keep `ai-efficiency-operating-system` and `task-goal-intelligence` as coordination owners; load this specialist when the engineering substrate itself is the problem.

## Capability Stack

Reason across these layers without collapsing them:

1. goal and acceptance contract;
2. model/inference behavior;
3. context, retrieval, memory, and provenance;
4. tools, MCP, schemas, authorization, and side effects;
5. agent/workflow state, retries, checkpoints, idempotency, and recovery;
6. host/session/account/runtime identity and activation;
7. observability: traces, spans, logs, metrics, receipts, costs, and latency;
8. evaluation: baseline, holdout, adversarial, regression, and failure corpus;
9. deployment/release: exact revision, read-back, CI/runtime verification, rollback;
10. security, privacy, capability boundaries, and memory/tool poisoning resistance.

## Engineering Loop

`CONTRACT → TOPOLOGY → EVIDENCE → FAILURE-FIRST → DESIGN → IMPLEMENT → VERIFY → OPERATE → RELEASE`

At each transition:

- keep `OBSERVED`, `DERIVED`, `HYPOTHESIS`, and `UNKNOWN` separate;
- choose the next action by information gain, not ceremony;
- after two same-mechanism no-delta failures, change hypothesis, instrument, environment, or mechanism;
- preserve a rollback target before material writes;
- test the requested effect at the highest practical layer.

## Non-Negotiable Failure Checks

Before `PASS`, try to falsify the design with at least the applicable cases:

- configured but not loaded/executed;
- stale revision or wrong account/session;
- partial success followed by failure;
- duplicate/reordered/retried side effects;
- network/dependency timeout;
- permission or entitlement mismatch;
- checkpoint/resume after interruption;
- memory/context poisoning or stale state;
- tool/schema/version drift;
- happy-path eval that hides regression;
- latency/cost improvement that silently removes capability;
- desktop automation that steals focus or mutates the wrong target.

## 2026 Engineering Deltas

Current practice must account for MCP `2026-07-28` stateless routing/caching/auth changes, end-to-end agent tracing and tool guardrails, standardized GenAI telemetry, durable resume semantics, and memory/context poisoning as a first-class attack surface.

## Evidence Gate

`FILE_EXISTS != REGISTERED != LOADED != EXECUTED != EFFECTIVE != VERIFIED`

`CI_GREEN != USER_PATH_VERIFIED`

`FAST != CORRECT`

`MORE_AGENTS != MORE_INDEPENDENT_EVIDENCE`

Do not promote a lower-layer success to a higher-layer claim.

## Load These References

- `references/capability-map.md` — gaps, symptoms, proof standards.
- `references/engineering-playbook.md` — execution and verification playbook.
- `references/2026-source-notes.md` — current upstream evidence and invalidation triggers.
- `../../evals/world-class-ai-engineering-pressure-cases.jsonl` — pressure/failure corpus.

## Existing Specialists To Delegate To

Use existing repo skills instead of duplicating them: `task-goal-intelligence`, `evidence-gap-research`, `competing-hypotheses`, `root-cause-clustering`, `durable-agent-control-plane`, `recoverable-state`, `completion-gate`, `compatibility-audit`, `multi-agent-deliberation`, plus the canonical plugin specialists for GitHub operations, MCP surface engineering, capability forensics, runtime forensics, convergence, and evidence watching.
