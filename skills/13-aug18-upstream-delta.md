# 2026-08-18 Upstream Delta Review

Snapshot: 2026-08-18 evening, Asia/Singapore.

This note records changes discovered after the first v1.1 research archive was staged. It exists to prevent stale architectural advice from being treated as current merely because the source URL is still valid.

## 1. OpenAI Agents SDK

Locked commit: `82e3571fc55a8583239c74a0cec8c5497f0d7a2c`.

Observed signal: workflow execution was moved out of repository skills on 2026-08-18. A nearby commit made runtime-probe approval explicit in skills.

### Research consequence

Do not collapse the concepts of **skill**, **workflow runtime**, and **execution harness** into one abstraction. Skills should describe reusable capability/procedure; the runtime owns orchestration, tool execution, state transitions, approval, and recovery.

## 2. Microsoft Agent Framework

Locked commit: `1b45c15749dbef06b9b97b5d09b7f0b3b1e7ceb3`.

Observed signal: .NET 1.18.0 release work landed on 2026-08-18; Python workflow tracing and secure deserialization work also landed the same day.

### Research consequence

The Microsoft comparison baseline in this archive should be **Agent Framework**, with AutoGen retained as historical/maintenance context rather than the default greenfield recommendation.

## 3. Google ADK

Locked commit: `029c17b3384f4ad584c4b4f6f83335be98a04f02`.

Related commit: `6e0facf9370261c788149a5330bb5632985e3531` adds telemetry for `load_skill_resource`.

### Research consequence

Skill loading itself is an observable runtime event. The reference architecture should treat skill discovery/loading as part of tracing and provenance, not as invisible prompt preprocessing.

## 4. LangGraph

Locked release commit: `644815f9e5bc52ad8f7a5227a456227e9c3e639b` (`langgraph 1.2.11`).

### Research consequence

Explicit graph/state orchestration remains a current option for systems where checkpointing, branching, interrupts, and deterministic control-flow are first-class requirements.

## 5. Anthropic Skills

Locked commit: `f379e5ad66e2febc1616cf8d6284666fecbe514e`.

Recent changes include an opt-in discernment skill and prompt-audit work.

### Research consequence

Two reusable patterns deserve promotion into this archive:

1. **discernment nudge** — after consequential answers, surface targeted checks rather than generic caveats;
2. **prompt audit** — date and inventory the instruction surface instead of letting old rules accumulate invisibly.

## 6. Superpowers

Locked release commit: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` (`v6.3.0`).

Relevant themes include a three-path brainstorming router, plan-scoped SDD workspaces, resume-based fix loops, bounded waits, micro-task batching, evidence-bearing preflight, and stronger falsifiability discipline.

### Research consequence

The best pattern is not maximal ceremony. Use **adaptive ceremony**:

- spike / bounded / architectural paths;
- approval gates only where consequence warrants them;
- batch same-shape microtasks;
- retain independent verification and evidence gates.

## 7. OpenClaw

Repository head observed: `43c31ea0567983e06dfcf2f54a5dab46f1fa647f`.

Research-relevant commit: `7c65bbcee31bd31fa5b46c84f3a3f54c2cc522fb` tracks context-window provenance and context ownership through sessions, listings, status, cron, and finalization.

### Research consequence

A durable agent should not store only **how much context** remains. It should also retain **where the context limit came from**, who owns/overrode it, and whether that provenance survives resume/finalization. This is directly relevant to cross-chat continuity and long-running agent work.

## 8. MCP

Locked repository commit: `4df2d6b6e3588efb46e7542d98498e5c630a0a86`; protocol baseline remains the 2026-07-28 specification used by the archive.

### Research consequence

Treat protocol capability discovery as dynamic. Do not assume a 2025-era client/server/session behavior is still valid simply because the endpoint name is unchanged.

---

# Cross-source synthesis

The strongest 2026 convergence is:

```text
skill = reusable capability contract
workflow = explicit task/control graph
harness = execution + tools + sandbox + approvals
state = durable external record
trace = provenance of decisions/tools/skills/state
verifier = independent outcome check
router = adaptive depth/parallelism/ceremony
```

This supersedes the weaker pattern:

```text
one giant prompt + fixed agent count + shared chat history + self-declared completion
```

## New design rule

> **Scale by unresolved information and consequence, not by agent count or prompt length.**

A 30-role framework is useful as a coverage map. Actual runtime fan-out should remain adaptive.
