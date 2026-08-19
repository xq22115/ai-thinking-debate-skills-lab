# 09 — Research Backlog & Upgrade Path

## P0 — Must verify before calling this system production-ready

1. Recover the actual latest copies of prior skillpacks from Library/filesystem.
2. Deduplicate conflicting version lineages.
3. Choose one canonical base architecture.
4. Build executable eval fixtures for completion, recovery, and root-cause tests.
5. Add per-host compatibility adapters.
6. Add security review for skills/tools/MCP boundaries.
7. Establish release tags and a changelog.
8. Validate on at least one real long-horizon task end to end.

## P1 — High-value upgrades

- Dynamic role activation based on information gain.
- Disagreement retention instead of full debate broadcast.
- Claim/evidence graph.
- Automatic stale-source invalidation.
- Regression dependency graph.
- Checkpoint receipt format.
- Host capability probe.
- Skill trigger eval harness.
- Cost dashboard for tokens/tool calls/elapsed time.

## P2 — Research experiments

- 1 vs 3 vs 7 vs 15 vs 30 role scaling.
- Same-model vs heterogeneous-model councils.
- Majority vote vs evidence-weighted judge.
- Full broadcast vs selective disagreement retention.
- Human checkpoint at plan level vs action level.
- Persistent external state vs transcript-only continuation.

## Canonical release path

`archive → normalize → validate → eval → adapter-test → security-review → release-candidate → host-live verification → stable`

## Proposed next release

`Evidence-Gated Deliberation & Skills OS v0.1.0-rc1`

RC1 acceptance:
- research lineage mapped;
- 2026 evidence refreshed;
- 30-role router specified;
- eval suite defined;
- portability matrix present;
- no unsupported host-live claims.
