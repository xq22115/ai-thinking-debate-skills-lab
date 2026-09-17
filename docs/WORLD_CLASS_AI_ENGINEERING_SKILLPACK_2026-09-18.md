# World-Class AI Engineering Skill Pack — 2026-09-18

## Why this pack exists

Cross-chat failure review showed that the recurring gap was not raw coding ability. The larger issue was engineering closure across AI-system boundaries: stale source assumptions, runtime/tool activation uncertainty, partial completion, missing read-back, weak recovery semantics, account/session identity drift, GUI non-interference, memory/context contamination, un-attributed latency, and verification that stopped at CI or configuration presence.

This pack adds a specialist engineering layer without replacing the repository's existing orchestration owners.

## Added capability areas

1. goal/acceptance engineering;
2. current-source and version forensics;
3. AI system architecture and boundary design;
4. tool/MCP contract engineering;
5. host/account/session identity;
6. memory/context integrity;
7. durable execution, retries, idempotency, checkpoints and recovery;
8. observability and runtime forensics;
9. evaluation-driven engineering and failure corpus;
10. GitHub/release reliability;
11. Computer Use / desktop non-interference engineering;
12. performance and cost engineering without capability degradation;
13. agent security and memory/tool poisoning resistance;
14. multi-agent evidence quality and independence.

## 2026 refresh incorporated

The skill explicitly accounts for:

- MCP `2026-07-28`: stateless protocol core, header routing, cacheable list results, extension framework and authorization hardening;
- OpenAI Agents SDK tracing and boundary-specific guardrails;
- OpenTelemetry GenAI observability conventions;
- durable pause/resume/checkpoint patterns from agent workflow engines;
- evaluation/graders as first-class release infrastructure;
- OWASP agent memory/context poisoning and tool-abuse threat models;
- Agent Skills progressive-disclosure packaging.

## Pack structure

- `skills/skills/world-class-ai-engineering/SKILL.md`
- `skills/skills/world-class-ai-engineering/references/capability-map.md`
- `skills/skills/world-class-ai-engineering/references/engineering-playbook.md`
- `skills/skills/world-class-ai-engineering/references/2026-source-notes.md`
- `skills/evals/world-class-ai-engineering-pressure-cases.jsonl`
- `control-plane/scripts/validate_world_class_ai_engineering_skill.py`
- `.github/workflows/world-class-ai-engineering-gate.yml`

## Design rule

This is a specialist, not another control-plane monarch. `ai-efficiency-operating-system` and `task-goal-intelligence` remain the orchestration/goal owners. Existing narrow skills remain the implementation references for evidence research, competing hypotheses, root-cause clustering, durable control, recovery, compatibility, completion gates and multi-agent deliberation.

## Acceptance contract

The package is acceptable only when:

- all required files are present at the exact revision;
- skill frontmatter is discoverable and trigger-oriented;
- the capability map covers the critical recurring failure domains;
- the playbook encodes baseline, failure-first design, tool/MCP preflight, observability, evals, desktop discipline, performance and release gates;
- the pressure corpus contains at least WCAE-01..WCAE-18 with unique IDs and explicit forbidden shortcuts;
- the validator passes on the exact PR revision;
- GitHub Actions runs the dedicated gate;
- no claim is made that repository packaging alone proves host-live installation or behavior.

## Status semantics

`PACKAGED` means the repository skill pack exists and validates structurally.

`HOST_LIVE` requires a target host to import/discover/load it.

`EFFECTIVE` requires a representative task to show the skill changed behavior.

`VERIFIED` requires the target acceptance criteria and regressions to pass with owning-system evidence.

Do not collapse these states.
