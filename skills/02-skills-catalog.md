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

### ai-efficiency-operating-system — `0.1.0-rc1`
Canonical efficiency orchestrator that composes the portable core with root-goal/task compilation, identity/path locking, demand-driven context/tool routing, parallel-read/serial-write execution, research saturation stopping, cross-chat convergence, runtime-performance diagnosis and high-density verified finalization. Package: `skills/ai-efficiency-operating-system/` relative to this catalog's `skills/` package root (repository path `skills/skills/ai-efficiency-operating-system/`). Machine-readable contract: `skillpack.json`.

This is an orchestration skill, not a renamed duplicate of the nine portable core skills. It must preserve required capabilities and quality rather than trading them away for apparent speed.

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
- target-host execution evidence for any host-specific claim.
