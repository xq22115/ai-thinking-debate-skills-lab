# OpenClaw Native Adapter — AI Efficiency Operating System

Status: **PACKAGE_CANDIDATE / SOURCE_LOCKED / HOST_LIVE_UNVERIFIED**

This adapter maps the existing AI Efficiency Operating System goal/evidence/recovery semantics onto current OpenClaw-native skills, sub-agents, Skill Workshop, and optional Swarm. It is additive: it does not replace model/provider/auth configuration, does not reduce existing concurrency, and does not disable an already-enabled capability.

## Why this adapter exists

The canonical plugin already owns goal integrity, evidence gates, recovery, memory and runtime forensics. OpenClaw adds host-native primitives that should be used instead of pretending the ChatGPT adapter is portable unchanged:

- workspace/extra-root `SKILL.md` discovery;
- isolated/forked sub-agents with parent review;
- Skill Workshop and autonomous learning;
- Code Mode + experimental Swarm collectors;
- config read/write/validate primitives.

The adapter therefore preserves **TRUTH HARD / METHOD SOFT** while changing the execution harness.

## Skill set

- `openclaw-goal-orchestrator` — Goal Contract, deterministic adaptive role selection, sub-agent/Swarm fan-out, parent synthesis.
- `openclaw-evidence-gate` — completion/read-back/host-live truth boundary.
- `openclaw-runtime-recovery` — first-upstream-failure diagnosis and materially different route selection.
- `openclaw-learning-loop` — evidence-backed Skill Workshop learning with counterexample/rollback protection.

Only these host adapter skills are exposed through this adapter root. Authority-bearing canonical skills are not bulk-exported into OpenClaw, so OpenAI-specific implicit/explicit invocation policy cannot be accidentally lost at the host boundary.

## Production and Lab

### Production

Uses stable OpenClaw primitives:

- `sessions_spawn`, `sessions_yield`, `subagents`;
- Skill Workshop;
- adaptive role selection;
- config validation and skill inventory read-back.

The installer raises concurrency only to a minimum floor (`agents.defaults.maxConcurrent >= 4`, `subagents.maxConcurrent >= 8`); higher existing values are preserved.

### Lab

Adds the production settings and enables:

- `tools.codeMode`;
- `tools.swarm.enabled`;
- Swarm floor `maxConcurrent >= 8`;
- `maxChildrenPerGroup >= 50`;
- `maxTotalPerGroup >= 200`;
- `waitTimeoutSecondsMax >= 600`.

Swarm remains an opt-in lab path because the upstream documentation marks it experimental. Production mode never disables an already-enabled Swarm.

## Install

Run on the OpenClaw Gateway host from this repository checkout:

```bash
python3 plugins/ai-efficiency-operating-system/adapters/openclaw/scripts/install_adapter.py --mode production
```

For the experimental lab profile:

```bash
python3 plugins/ai-efficiency-operating-system/adapters/openclaw/scripts/install_adapter.py --mode lab
```

Useful controls:

```bash
# inspect planned writes only
python3 plugins/ai-efficiency-operating-system/adapters/openclaw/scripts/install_adapter.py --dry-run

# preserve existing autonomous-learning mode
python3 plugins/ai-efficiency-operating-system/adapters/openclaw/scripts/install_adapter.py --learning keep

# target an agent that already has an explicit skills allowlist
python3 plugins/ai-efficiency-operating-system/adapters/openclaw/scripts/install_adapter.py --agent <agent-id>

# read-back only after a Gateway restart/new session
python3 plugins/ai-efficiency-operating-system/adapters/openclaw/scripts/install_adapter.py --verify-only
```

The installer:

1. resolves the active OpenClaw config path;
2. creates a permission-restricted backup;
3. appends this adapter's skill root without deleting existing roots;
4. enables skill watching;
5. configures Workshop learning (`auto` by default, or `propose`/`keep`);
6. appends required sub-agent/Workshop tools without deleting existing tools;
7. raises concurrency floors without lowering higher values;
8. extends existing default/target-agent skill allowlists instead of replacing them;
9. uses conditional config writes to reject stale-current races;
10. runs `openclaw config validate`;
11. requires all four adapter skills to appear in the selected OpenClaw inventory.

It does **not** change model selection, credentials, providers, channels, browser profile, OS permissions, agent workspaces, or existing named agent ownership.

## Adaptive specialist topology

The deterministic baseline is `scripts/role_router.py` with 16 regression cases. It can select zero to nine child roles; there is deliberately no fixed N.

Children are specialized, not clones. The parent retains Goal Contract and completion authority. Child results are evidence for synthesis, not terminal truth.

## Self-learning boundary

OpenClaw's native Workshop is used for durable learning. The adapter itself is loaded from an extra root and remains the stable host contract. Learned procedures belong in writable workspace skills/proposals.

Auto-learning is useful only after verification. The adapter rejects routine success, transient failures, raw external instructions, secrets, and unsupported negative claims as training material. Broad rules require a positive case plus a protection/counterexample case.

## Verification

Repository package verification:

```bash
python3 plugins/ai-efficiency-operating-system/adapters/openclaw/scripts/validate_adapter.py
```

Host-live verification requires the Gateway itself:

```bash
openclaw config validate
openclaw skills list --json
openclaw skills info openclaw-goal-orchestrator --json
openclaw skills info openclaw-evidence-gate --json
openclaw skills info openclaw-runtime-recovery --json
openclaw skills info openclaw-learning-loop --json
```

Then run behavioral probes from `HOST_LIVE_GATES.md`.

`GITHUB_COMMITTED != HOST_LIVE`. A PR/CI pass proves packaging and deterministic routing only.

## Upstream lock

The current design is pinned to `openclaw/openclaw` commit `d84cdc5c03d378c0f50db1b0abb17537f390b01c`, checked 2026-09-04. See `upstream-lock.json`. Re-audit before changing config fields or relying on new OpenClaw runtime behavior.
