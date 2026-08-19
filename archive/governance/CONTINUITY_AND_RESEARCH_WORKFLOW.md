# Cross-Chat Continuity + High-Quality Research Workflow

## Cross-Chat Task Continuity Protocol v1.0

### Objective
Prevent complex tasks from becoming disconnected, restarted, falsely repeated or silently “completed” when the user switches chat, device or interface.

### Core model
Every non-trivial task should have a unique `TASK-ID` and a durable task ledger.

A continuity record should preserve at least:
- task name and objective
- acceptance criteria
- current phase/state
- completed work
- unresolved items
- evidence/artifacts already produced
- decisions and rejected alternatives
- blockers and retry history
- repository/branch/commit where applicable
- next executable action

### Continuity principle
A new conversation should reconstruct task state from evidence/ledger rather than rerun the entire task from memory.

The ledger is not proof of external completion by itself. External writes, installations, deployments and runtime behavior must still be re-observed.

## High-Quality Research Workflow v1

### 1. Decompose the research question
Break a broad question into explicit claim families and uncertainty classes.

### 2. Build a key-claims list
Before searching, identify the claims that will actually determine the conclusion.

### 3. Design precise queries
Use different query families for:
- current status/version
- primary documentation
- implementation details
- failure reports
- counter-evidence
- independent evaluations

### 4. Define source quotas and selection rules
Prioritize:
1. official documentation / standards
2. primary research papers
3. original repositories / release notes
4. high-quality independent engineering evidence

Exclude or clearly downgrade unsourced reposts and circular summaries.

### 5. Record provenance
For important sources record when possible:
- author/organization
- title
- date/version
- URL/repository
- commit SHA or release tag
- access/retrieval time

### 6. Maintain a Claim–Evidence Matrix
Each important claim should map to one or more supporting/contradicting sources and an evidence grade.

### 7. Detect source dependencies
Ten pages repeating one upstream claim are not ten independent sources.

### 8. Contradiction matrix
When reliable sources disagree, preserve the disagreement and identify:
- different versions/timeframes
- different environments
- different definitions
- different measurement methods
- unresolved uncertainty

### 9. Explicit falsification
Ask what evidence would overturn the preferred answer. Search for that evidence before closing.

### 10. Freshness gate
Current product/version/compatibility claims require current evidence. Historical research is preserved as archival context but must not silently become current installation guidance.

## Root-cause repair integration

When multiple failures appear as A, B and C, do not automatically patch them independently. Cluster symptoms and test whether they share one underlying mechanism.

Recommended sequence:

`SYMPTOMS → COMMON INVARIANT → COMPETING ROOT HYPOTHESES → MINIMAL FALSIFICATION TESTS → ROOT REPAIR → REGRESSION MATRIX`

A repair is stronger when one change explains and fixes several previously separate failures without creating new violations.

## Long-running engineering foundation recovered from 2026 research

Useful durable patterns include:
- grouped traces + persistent sessions for multi-agent tasks
- Git worktrees for isolated concurrent repair within one repository
- append-only event histories with replay
- idempotent or explicitly non-retryable external activities
- artifact provenance + Manifest + SBOM + attestation
- time-ordered task identifiers such as UUIDv7
- prompt/completion/tool argument trace fields treated as potentially sensitive
- pinning model, prompt, tools, schemas, policy, research, capabilities, environment and code revision per run
- external content treated as untrusted data, not silently promoted to instructions
- prepare/apply/commit/recover semantics for cross-system changes
- reconciliation/compensation after ambiguous external side effects instead of blind retry
- holdout, flakiness, calibration, latency/tool-budget and incident regression checks before release

## Completion rule
Research completion is not “I found many sources.” It is:

`KEY CLAIMS CLOSED + CONTRADICTIONS ADDRESSED + FRESHNESS CHECKED + FALSIFICATION ATTEMPTED + UNCERTAINTY PRESERVED`
