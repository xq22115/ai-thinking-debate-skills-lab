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

### ai-efficiency-operating-system — `0.4.0-rc1`

Canonical efficiency OS: `skills/skills/ai-efficiency-operating-system/`.

v0.4 keeps v0.3's rule that implicit context must become explicit state, then adds a deeper invariant:

> **proposal, authority, effect, observation, evidence, verdict and delivery are different truth channels.**

The package now contains **57 unique machine-readable modules** and T01–T70. Major capabilities include:

- durable task/goal contracts, correction/supersession, exact-target identity and no-goal-shrink;
- host/version-scoped instruction and memory authority;
- progressive disclosure, context lineage, semantic compaction rollback and content-addressed observations;
- E0–E6 evidence, competing hypotheses and model-delta research;
- A01–A10 adaptive review with real-agent receipts and correlated-consensus clustering;
- semantic action identity, goal CAS, leases/fencing, first-class UNKNOWN effects and safe replay;
- interaction-topology preflight for approvals/auth/input in delegated or non-interactive work;
- timely ACT/GATHER/ABSTAIN decisions and tool-invocation vs tool-adjudication separation;
- receiver-side delivery truth, structured successor handoffs and liveness receipts;
- model/host-aware reversible skill lifecycle with leave-one-out marginal utility;
- versioned verifier admission/canaries;
- hot-path/backpressure/performance controls without shrinking protected work;
- physical/distribution parity and owning-runtime completion gates.

This orchestration layer composes rather than renames the portable core skills.

Package files:

- `SKILL.md`
- `skillpack.json`
- `runtime-state.schema.json`
- `SOURCE-MATRIX.md`
- `EVALS.md`
- `VERIFICATION.md`
- `CHANGELOG.md`

Current package gate requires **57 unique modules and T01–T70** plus exact GitHub read-back. `HOST_LIVE` still requires owning-runtime invocation/postcondition evidence.

## Candidate supporting skills

### skill-security-review
Check broad permissions, executable behavior, network calls, secrets, injection surface and supply-chain dependencies.

### source-ledger
Record claim ID, source class, source, type, date, version/commit/blob, support/contradiction, confidence and notes.

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

Portable semantic logic must not assume every host uses the same package wrapper.

## SKILL.md minimum

```yaml
---
name: skill-name
description: What it does and when it activates
---
```

Then define objective, activation, non-goals, workflow, evidence requirements, failure modes, output contract, compatibility boundary and completion gate.

## Promotion gate

A skill becomes stable only after structure validation, positive/hard-negative trigger evals, adversarial cases, compatibility/provenance recording, paired marginal utility, target/protection/holdout regression checks and target-host evidence for host-specific claims.
