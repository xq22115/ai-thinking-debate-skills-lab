# Engineering Research Baselines — Durable Agents, Supply Chain, Observability

## 2026-08-03 baseline conclusions

### Persistent sessions and grouped traces
Long-running multi-agent tasks should use persistent sessions and grouped traces rather than depend only on chat text memory.

### Git worktrees for parallel repair
Concurrent repairs in one Git repository should use isolated worktrees so each branch has its own HEAD/index and agents do not overwrite one shared working directory.

### Event history and replay
Durable workflows should persist append-only history sufficient to reconstruct state. Workflow logic must be replay-safe; external activities should be idempotent or explicitly non-retryable.

### Artifact provenance
Release artifacts require more than a filename. Useful controls include:
- provenance
- manifest
- SBOM
- attestation
- deterministic/reproducible packaging where practical

### Task identity
Time-ordered low-collision IDs such as RFC 9562 UUIDv7 were selected in one research line for durable task identities.

### Canonicalization honesty
One historical package used an internal `SUO-C14N-v1` JSON hashing profile and explicitly did **not** claim full RFC 8785 JCS compatibility. Cross-language signing should use a verified canonicalization implementation rather than assume a private profile is equivalent.

## v9 governance conclusions

### Prompt is instruction, not proof
Prompt text belongs to the Instruction Plane. It cannot serve as execution or acceptance evidence.

### Pin the full run context
Every important run should bind:
- model
- prompt
- tools
- schemas
- policy
- research snapshot
- capabilities
- environment
- code revision

### Multi-agent count is correlated evidence
Raw agent count is not equal to independent evidence count. Shared model, prompt, sources, tools and environment create correlation.

### External content is untrusted input
Retrieved content must not silently become executable instruction.

### Cross-system mutation protocol
Changes spanning files, registries, external APIs or remote systems should use a prepare/apply/commit/recover protocol rather than rely on `try/except` alone.

### Ambiguous external side effects
After an uncertain provider POST or other ambiguous external write, reconcile/read back before retry. Blind resend risks duplicate side effects.

### Release evaluation dimensions
A release process should consider:
- duplicate/repeat execution
- holdout evaluation
- flakiness
- calibration
- latency/tool budget
- incident regression

### Attestation honesty
Unsigned or unexecuted signatures/attestations must be labeled `UNSIGNED` / `NOT_EXECUTED`; templates are not signatures.

## Observability
OpenTelemetry GenAI/Agent/MCP fields should be version-pinned where used. Prompt, completion, tool arguments and conversation IDs may be sensitive and/or high-cardinality and should not be logged indiscriminately.

## SBOM
One v9 research line used CycloneDX 1.7 format for a locally generated offline SBOM. Local SBOM generation does not imply signature or external attestation.

## Supply-chain research track

Historical 2026 work also investigated AI/NPM supply-chain incidents and emphasized:
- lockfile discipline
- SBOMs
- dependency cooling periods
- malware gates
- credential isolation
- post-infection isolation and clean rebuild

Incident-specific package counts and advisory numbers are time-sensitive and should be rechecked against primary advisories before current operational use.

## n8n security track
Historical notes tracked 2026 n8n security advisories and upgrade baselines. Version-specific patch floors are archival until revalidated against current official advisories.

## Platform-skill compatibility lesson
A documented skill directory does not prove a specific desktop build actually indexed the skill. Installation evidence should be separated into:

`FILES_PRESENT → CLIENT_DISCOVERED → INVOCATION_OBSERVED → BEHAVIOR_VERIFIED`

Historical platform research also recorded:
- ChatGPT personal/workspace skills can be UI/account-managed and cannot be proven installed by filesystem copy alone.
- Codex skill indexing can require live restart/reload/discovery verification.
- Cline skills were treated as experimental in the researched snapshot.
- OpenHands documentation had path inconsistencies that should be preserved rather than guessed away.
- Roo Code was recorded as archived/shut down on 2026-05-15 in that research snapshot; this is time-sensitive archival information and should be rechecked before recommendation.

## Core principle
Engineering confidence should rise only when evidence crosses distinct boundaries:

`SOURCE → PACKAGE → FILESYSTEM → HOST DISCOVERY → LIVE INVOCATION → SEMANTIC/OPERATIONAL VALIDATION`
