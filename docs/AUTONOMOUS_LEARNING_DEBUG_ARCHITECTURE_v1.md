# Autonomous Learning & Debug Architecture v1

## Goal

Turn this repository's existing evidence-bound multi-agent control plane into an executable learning/debugging loop.

The design is intentionally conservative about what may become "learned truth": an agent may generate a candidate lesson, but only verified, sufficiently independent evidence may promote it to reusable operational knowledge.

## Architecture

```text
Task / CI failure / runtime symptom
            |
            v
   Failure fingerprinting
            |
            v
  Competing hypotheses <------ Active lesson registry
            |
            v
 Discriminating experiment
            |
            v
 Repair candidate + rollback
            |
            v
 Verification / regression
            |
            v
  Evidence-bound lesson candidate
            |
            v
 Promotion gate / contradiction gate
            |
      +-----+------+
      |            |
   ACTIVE       CANDIDATE
      |
      v
 Future retrieval + invalidation checks
```

## Components

- `control-plane/autonomy/engine.py`
  - stable failure fingerprints that remove volatile IDs, timestamps, addresses, and counters;
  - lesson candidate scoring and promotion;
  - contradiction-aware demotion logic;
  - known-lesson retrieval for future incidents;
  - two-strike pivot enforcement for repeated failed mechanisms.
- `control-plane/autonomy/config.json`
  - machine-readable thresholds and invariants.
- `.github/agents/*.agent.md`
  - explicit orchestrator, debugger, and learning-curator roles for GitHub Copilot custom agents.
- `.github/instructions/autonomy.instructions.md`
  - path-scoped rules for the autonomy control plane.
- `.github/workflows/autonomous-learning-debug-gate.yml`
  - syntax, config, unit-test, and architecture regression gate.

## Learning policy

A lesson is not promoted because an LLM said it worked. Promotion requires all configured gates:

1. minimum verified supporting evidence;
2. minimum distinct independent evidence groups;
3. confidence above threshold;
4. contradiction ratio below threshold;
5. root cause, diagnostic, repair, verification, reuse conditions, and invalidation conditions are all present.

Lessons can later be deprecated when direct contradictory evidence crosses the configured threshold.

## Debugging policy

For ambiguous incidents:

1. fingerprint the observed failure;
2. retrieve matching active lessons;
3. construct materially distinct hypotheses;
4. choose a discriminating test;
5. after two failures using the same mechanism, pivot at least one major dimension:
   hypothesis, mechanism, diagnostic instrument, environment, or verification method;
6. bind the repair to rollback and verification evidence;
7. only then create a lesson candidate.

## Why this is different from prompt-only "self improvement"

Prompt-only systems often accumulate prose without proving that the advice is correct. This design stores compact, machine-readable operational lessons with provenance, confidence, contradictions, reuse boundaries, and invalidation conditions.

The result is a repository that can improve its *decision support* over time without silently rewriting its own success criteria.

## Runtime integration

The engine is stdlib-only Python so it can run in GitHub Actions, local shells, Copilot/Claude/Codex tool calls, or a future OpenAI Agents SDK / MCP service.

A future runtime adapter may feed trace/tool events into this engine, but adapters must not weaken the promotion gate or bypass repository acceptance tests.
