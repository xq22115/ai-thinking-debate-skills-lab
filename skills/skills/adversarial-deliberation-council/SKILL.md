---
name: adversarial-deliberation-council
description: Orchestrate evidence-bearing multi-role deliberation for complex AI research, architecture, automation, settings, troubleshooting, and cross-system work. Use when materially different interpretations or routes exist, prior attempts failed, the user asks for expert debate, or false completion would be costly.
---

# Adversarial Deliberation Council

Version: `1.0.0`

## Objective

Improve **decision quality × goal fidelity × verified completion** by forcing materially different specialist roles to challenge one another with evidence, counterexamples, and acceptance tests.

This is not a request to expose private chain-of-thought. Each seat contributes only externally useful artifacts: claims, evidence, objections, discriminating tests, route proposals, and revised conclusions.

## Trigger

Activate when one or more are true:

- the task is complex, research-heavy, architectural, cross-tool, cross-repo, cross-chat, or long-horizon;
- several plausible interpretations or causal models would produce different actions;
- the user explicitly asks for multiple experts, debate, red-team review, or stronger critical thinking;
- a route has failed twice without material evidence gain;
- the requested effect spans GitHub, Notion, local runtime, web, IDE agents, MCP, or hosted AI surfaces;
- completion could be falsely inferred from docs, config presence, installation, self-report, or green CI alone.

Do not invoke merely to increase agent count. Every seat must have a unique decision-changing job.

## Council Seats

Use the minimum useful subset, normally 4–7 seats.

1. **Goal Contract Auditor** — reconstructs root goal, hard constraints, negations, target identity, protected capabilities, and acceptance tests.
2. **Systems Architect** — proposes the smallest coherent architecture and identifies source-of-truth ownership, dependency boundaries, and integration points.
3. **Evidence Gap Researcher** — identifies claims that actually need proof, searches high-signal evidence, and distinguishes fact from hypothesis.
4. **Competing Hypotheses Analyst** — maintains materially different explanations or solution models and chooses discriminating observations rather than confirmation volume.
5. **Adversarial Red Team** — attacks the leading plan for semantic drift, hidden assumptions, easier-neighbor substitution, overclaiming, brittle coupling, and failure modes.
6. **Route Recovery Engineer** — when a path stalls, proposes causally independent alternatives that preserve the user's required capability and acceptance criteria.
7. **Owning Runtime Verifier / Jury** — decides whether the requested effect is actually proven in the system that owns it; rejects self-report, file-exists, install-only, or simulation-only proof.

When existing repo agents or skills cover a seat, compose them instead of duplicating their logic. Prefer:

- `.agents/agents/goal-contract-auditor.md`
- `.agents/agents/anti-evasion-red-team.md`
- `.agents/agents/route-recovery-engineer.md`
- `.agents/agents/owning-runtime-verifier.md`
- `.agents/agents/contribution-evidence-auditor.md`
- `skills/skills/task-goal-intelligence/SKILL.md`
- `skills/skills/competing-hypotheses/SKILL.md`
- `skills/skills/evidence-gap-research/SKILL.md`
- `skills/skills/root-cause-clustering/SKILL.md`
- `skills/skills/capability-challenge/SKILL.md`
- `skills/skills/compatibility-audit/SKILL.md`
- `skills/skills/completion-gate/SKILL.md`

## Phase 0 — Goal Freeze

Before debate, publish a compact `GOAL_CONTRACT`:

- `ROOT_GOAL`
- `DESIRED_END_STATE`
- `HARD_CONSTRAINTS`
- `NEGATIONS`
- `PROTECTED_CAPABILITIES`
- `TARGET_IDENTITY`
- `ACCEPTANCE_TESTS`
- `DECISION_CRITICAL_UNKNOWNS`
- `CURRENT_BLOCKER`

A blocker is not a replacement mission. A route may change; the root goal may not silently change.

## Phase 1 — Independent Briefs

Each active seat returns the same structured brief before seeing the synthesis:

- `CLAIM`
- `WHY_IT_MATTERS`
- `EVIDENCE`
- `COUNTEREVIDENCE`
- `ASSUMPTIONS`
- `PREDICTED_FAILURE`
- `DISCRIMINATING_TEST`
- `RECOMMENDED_ACTION`
- `CONFIDENCE`

A seat that cannot add a unique claim, test, falsification, implementation delta, or verification step is removed from the council.

## Phase 2 — Cross-Examination

Require direct disagreement, not polite convergence.

- Each seat challenges at least one consequential claim from another seat.
- Prefer attacks on causal ownership, target identity, acceptance proof, version/runtime assumptions, and protected capabilities.
- Formulate the strongest opposite hypothesis for the current leader.
- Search for or request the smallest observation that would flip the ranking.
- Record contradictions explicitly instead of averaging them away.

Use a contradiction ledger:

`CLAIM_A ↔ CLAIM_B → DISCRIMINATING_EVIDENCE → RESULT → SURVIVING_MODEL`

## Phase 3 — Reverse Diagnostics

For failures, configuration ambiguity, or "底層" questions, reason backward from the observed symptom:

`OBSERVED_EFFECT → OWNING_RUNTIME → ACTIVE_CONFIG/REVISION → CALL/EXECUTION PATH → DEPENDENCY/BOUNDARY → REQUIRED PROOF`

Classify each suspected mechanism as one of:

- verified causal owner;
- plausible hypothesis;
- stale or superseded configuration;
- external platform boundary;
- missing permission/capability;
- temporary runtime failure;
- unsupported assumption.

Do not treat reverse diagnostics as permission to claim control of hosted model weights, server-side policies, entitlements, or hidden product internals that the runtime cannot actually modify.

## Phase 4 — Source-of-Truth Arbitration

Use the owner that can prove the effect:

- **GitHub**: code, config, commit, PR, issue, Actions, test artifacts, exact revisions.
- **Notion**: cross-project context, decisions, research, skill registry, blackboard, acceptance debt.
- **Local runtime / Desktop Commander / IDE**: files, processes, installed config, logs, live invocation, UI effect.
- **Hosted product surface**: only capabilities exposed by that product/session; repository presence is not proof of hosted activation.

Cross-system claims require both sides when appropriate: e.g. GitHub exact ref plus local runtime read-back, or Notion decision owner plus GitHub executable truth.

## Phase 5 — Decision Synthesis

The chair produces a compact decision record:

- winning interpretation / architecture;
- strongest defeated alternative and why it lost;
- decisive evidence;
- unresolved uncertainty;
- next material action;
- rollback or fallback route;
- acceptance proof required before `PASS`;
- confidence with reason.

Do not expose hidden reasoning transcripts. Expose the evidence-bearing debate outcome.

## Anti-Headcount Theater

Agent count is never a quality metric.

A counted seat must contribute at least one of:

- unique evidence;
- unique falsification;
- unique implementation delta;
- unique runtime test;
- unique failure mode;
- unique integration constraint;
- unique acceptance verification.

If several seats converge without independent evidence, collapse them into one.

## Stall and Route-Switch Rule

If the same target + mechanism + failure fingerprint repeats twice without material evidence gain:

1. freeze that route;
2. preserve the evidence and blocker;
3. ask the Route Recovery seat for at least two causally independent alternatives;
4. choose by expected decision/evidence gain;
5. continue the root goal without lowering required quality, features, tests, or acceptance criteria.

## Completion Jury

Before declaring completion, the Runtime Verifier/Jury must answer:

- Is target identity proven?
- Is the requested effect visible in the owning system?
- Did any user requirement get silently weakened?
- Are all material writes read back?
- Are configs/skills actually loaded where claimed, not merely stored?
- Did a simpler neighboring task substitute for the real one?
- Are remaining blockers explicitly bounded?

`PASS` requires owning-system evidence. Otherwise use `PARTIAL`, `BLOCKED`, or `UNVERIFIED`.

## User-Facing Output

Keep visible output concise and high-density:

1. decision;
2. major disagreement;
3. decisive evidence;
4. what was changed or verified;
5. remaining blocker/debt;
6. confidence.

For long-running work, provide brief progress updates but do not dump private reasoning.
