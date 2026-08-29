# Deep Task Integrity — research/depth reference

This reference preserves the strongest prior Deep Task Integrity mechanics while keeping the model-facing skill thin.

## Complexity router

- `LIGHT`: simple lookup/transformation; no full harness.
- `DEEP`: ambiguous causality, research, diagnosis, comparison or high cost of error.
- `LONG`: DEEP plus multiple stages/tools/files/iterations.
- `RESEARCH_HARD`: unstable facts, source conflict, sparse indexing, version ambiguity or broad historical/technical coverage.

Use STANDARD / DEEP / FORENSIC depth according to unresolved information, never to consume time.

## Source-bound obligations

Every HARD/IMPORTANT source requirement maps to at least one obligation. Every derived obligation maps back to a source requirement and may refine but not weaken it.

## Root-cause graph

`SYMPTOM → MECHANISM → HYPOTHESIS → PREDICTED_OBSERVATION → DISCRIMINATOR → RESULT → ROOT/CONTRIBUTING_CAUSE → REPAIR → REGRESSION`

Prefer shared upstream causes only when mechanism and recovery boundary genuinely match.

## Temporal breadth

Track where relevant:

- `EVENT_TIME`
- `PUBLISHED_TIME`
- `EFFECTIVE_TIME`
- `OBSERVED_TIME`
- `VERSION_TIME`
- `SUPERSESSION`

Research lanes:

`NOW / RECENT_DELTA / PRE_CHANGE_BASELINE / ORIGIN / TRANSITION / CURRENT`

## Twelve search operations

Use only the routes that can change an obligation or hypothesis:

1. `LITERAL` — exact wording, IDs, errors.
2. `MECHANISM` — subsystem/process/root cause.
3. `EVIDENCE_VOCABULARY` — terms likely to appear in evidence.
4. `ADVERSARIAL` — failures, regressions, counterexamples.
5. `VERSION` — release/tag/commit/build/model/surface.
6. `PROVENANCE` — original author/repo/paper/postmortem.
7. `CITATION_GRAPH` — references backward and citing work forward.
8. `ARTIFACT` — docs, changelog, issue, PR, commit, source, benchmark, PDF, dataset.
9. `STRUCTURAL_DOC` — headings/sections/bounded reads instead of opaque snippets.
10. `TEMPORAL` — origin → transition → current; event date and publication date separately.
11. `COMMUNITY_DISCOVERY` — operational friction/terminology; corroborate material claims.
12. `SOURCE_INVERSION` — pivot from promising result to author/org/repo/issues/releases.

Every query must answer: which unresolved hypothesis or obligation could this change?

## Ten heterogeneous review lanes

For RESEARCH_HARD, lanes are failure detectors, not votes:

1. INTENT_COMPILER
2. CONSTRAINT_SENTINEL
3. ROOT_CAUSE_ANALYST
4. EVIDENCE_INVESTIGATOR
5. DEPTH_VALUE_CRITIC
6. RED_TEAM
7. EXECUTION_ENGINEER
8. EARLY_VERIFIER
9. COMPLETION_JUDGE
10. INTEGRATOR

When actual independent agent runtimes are available, prefer isolated first pass before cross-examination. A role name is not evidence of an independent runtime. Collapse duplicate model/prompt/evidence lineages and reassign freed capacity to missing evidence or minority hypotheses.

## Search audit after drift

Do not blindly restart a long search:

1. `LOCALIZE` the earliest critical error/drift.
2. `ATTRIBUTE` it to query choice, source quality, evidence misuse, temporal/version mismatch, reasoning error or premature closure.
3. `REPAIR` from that point with a different discriminator/search route.

## Lifecycle epoch

Start a new evidence epoch after material compaction/reset, resume/fork/backtrack, worker return, cwd/repo/worktree/environment change, instruction/config/skill change, tool/permission change or user contract revision. Historical evidence remains useful but does not automatically prove current state.

## Anti-patterns

Reject:

- "think harder/longer" with no evidence target;
- fixed source counts as general quality proxies;
- ten roles repeating one premise;
- newest-only research for evolving mechanisms;
- date-filter-only historical research;
- snippets used as final evidence when the source is openable;
- equivalent queries with zero MATERIAL DELTA;
- novelty theater after a simple explanation is causally proven;
- completion based on executor self-report.
