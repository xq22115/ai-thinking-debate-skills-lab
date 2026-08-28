# Skills Catalog

## RC1 portable core

### evidence-gap-research
Identify missing evidence before accepting claims. Outputs: claim ledger, missing evidence, source priority, contradiction list.

### competing-hypotheses
Maintain H1/H2/H3+, discriminating tests, counterevidence and confidence updates without collapsing alternatives too early.

### root-cause-clustering
Cluster symptoms by mechanism fingerprint/dependency graph; test and repair shared causes before symptom-by-symptom patching.

### completion-gate — `0.1.1-rc1`
Separate drafted / packaged / implemented / tested / reviewed / verified / host-live / deployed / healthy. Bind mutable claims to exact revision/runtime evidence and distinguish infrastructure blockers from task/test failure.

### recoverable-state
Persist task ID, state, checkpoint, pending actions, evidence refs, completed irreversible actions and rollback target.

### compatibility-audit — `0.1.1-rc1`
Produce host/OS/version/runtime/permission compatibility matrices. Separate current product guidance, repository content, repository metadata and runtime observation; record contradictions rather than collapsing them.

### multi-agent-deliberation — `0.1.1-rc1`
Treat 30 roles as a coverage pool. Activate a small set by evidence/method/capability diversity and marginal information gain. Preserve strong minority evidence; role labels do not prove runtime independence.

### capability-challenge — `0.1.1-rc1`
Distinguish `VISIBLE`, `AUTHORIZED`, and `VERIFIED`; classify missing tool, permission, auth, unsupported host/API, temporary/infrastructure failure, policy restriction, and unknown before saying `cannot`.

### durable-agent-control-plane — `0.1.1-rc1`
Durable task/run identity, isolated writer ownership, claims before mutation, claim-bound receipts, dependency-aware execution, recovery/rehydration, and separate task-result vs execution-infrastructure state.

## Orchestration layer

### ai-efficiency-operating-system — `0.3.0-rc1`

Canonical efficiency OS at repository path `skills/skills/ai-efficiency-operating-system/`.

v0.3 preserves v0.2's goal/evidence/context/execution architecture but deepens the root model:

> **implicit context is hidden state; hidden state must be made explicit, versioned, testable and recoverable.**

The package now composes the portable core with **47 unique machine-readable modules**, including:

- immutable task/goal contracts, corrections, ten-dimensional target identity and no-goal-shrink invariants;
- host/surface-specific instruction-scope/precedence audits plus instruction provenance and retest triggers;
- progressive disclosure, per-agent context lineage, semantic compaction with invariant rollback and content-addressed observation caching;
- failed-turn quarantine and recurrence-based memory authority rather than treating chat history as canonical state;
- raw input vs corrected intent vs generated rewrite fidelity, including proper nouns and code-switch preservation;
- E0–E6 evidence gating, coverage frontier, competing hypotheses and model-delta depth;
- adaptive multi-agent coalitions, selective disagreement and strict runtime-agent receipt requirements;
- parallel-read/serial-write ownership, short critical sections, durable event journal, idempotency/fencing and safe resume;
- changed-strategy bounded retry with circuit breaker, event-driven waiting and branch-scoped degradation;
- delivery truth from SENT → DELIVERED → ACKNOWLEDGED → INCORPORATED → VERIFIED;
- version-aware protocol contracts, including MCP 2026-07-28 compatibility and current deprecation signals;
- worker/verifier separation, alternate-path invariant testing, temporal rollback witnesses and physical materialization reverse coverage;
- activation precision/recall, paired no-skill marginal utility, holdout/regression promotion and no self-approval;
- hot-path amplification/retry/cache/backpressure controls and high-density verified finalization.

This is an orchestration package, not a renamed duplicate of the nine portable core skills. It must preserve required capabilities, concurrency, genuine reasoning and answer quality rather than trading them away for apparent speed.

Package files:

- `SKILL.md`
- `skillpack.json`
- `runtime-state.schema.json`
- `SOURCE-MATRIX.md`
- `EVALS.md`
- `VERIFICATION.md`
- `CHANGELOG.md`

Current package gate requires **47 unique modules and T01–T50** plus exact GitHub read-back. `HOST_LIVE` still requires owning-runtime invocation/postcondition evidence.

## Candidate supporting skills

These are useful catalog responsibilities but are not yet separate RC1 skill folders:

### skill-security-review
Check broad permissions, executable behavior, network calls, secrets, injection surface and supply-chain dependencies.

### source-ledger
Record claim ID, source class, source, type, date, version/commit/blob, support/contradiction, confidence and notes. Current archive implementation is `05-source-ledger.json`.

### capability-registry
Prevent duplicate prompts/skills/agents/tools by recording trigger, entrypoint, status, permissions, compatibility, verification and source revision.

## Package template

```text
skill-name/
├── SKILL.md
├── README.md                 # optional
├── COMPATIBILITY.md          # optional
├── EVALS.md                  # optional
├── SECURITY.md               # optional
├── CHANGELOG.md              # optional
├── tests/                    # optional
└── resources/                # optional
```

Portable semantic logic must not assume every host uses the same installation/package wrapper. For example, a `SKILL.md` procedural contract can be portable while a Codex plugin manifest, Claude integration path, Windows hook, or MCP declaration remains adapter-specific.

## SKILL.md minimum

```yaml
---
name: skill-name
description: What it does and when it activates
---
```

Then define objective, activation, non-goals, workflow, evidence requirements, failure modes, output contract, compatibility boundary and completion gate. Version/status may be recorded in the document or host-specific metadata when the target format has stricter frontmatter rules.

## Promotion gate

A skill becomes stable only after:
- structure/contract validation;
- positive and negative trigger evals;
- adversarial/falsification cases;
- permission and infrastructure-blocker cases where relevant;
- security review;
- current compatibility matrix;
- version/provenance recording;
- paired marginal-utility / no-skill comparison for automatically routed skills;
- target-host execution evidence for any host-specific claim.
