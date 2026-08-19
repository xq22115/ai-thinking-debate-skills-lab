# 07 — Deliberation Router Specification v1.1

## Objective

Select the smallest useful deliberation topology for the task.

## 1. Inputs

- task risk: low / medium / high / critical
- uncertainty: low / medium / high
- reversibility: reversible / costly / irreversible
- evidence conflict: none / moderate / severe
- domain breadth: narrow / cross-domain
- compatibility surface: single-host / multi-host
- security sensitivity: normal / elevated
- acceptance-test clarity: clear / ambiguous

## 2. Default routing

### Tier 0 — deterministic
Use 1 execution agent.

Use when:
- task is mechanical;
- acceptance test is explicit;
- authoritative source is unambiguous.

### Tier 1 — independent alternatives
Use 3 independent reasoners + 1 judge.

Use when:
- multiple plausible approaches exist;
- cost of error is moderate.

### Tier 2 — adversarial deliberation
Use 5–9 roles:
- 2–3 independent hypotheses;
- evidence auditor;
- red team;
- falsifier;
- domain specialist;
- integrator/judge.

Use when:
- evidence conflicts;
- root cause is uncertain;
- architecture decision affects multiple components.

### Tier 3 — extended council
Activate 10–18 specialist roles.

Use when:
- cross-platform;
- security-sensitive;
- deployment/recovery implications;
- high-impact irreversible actions.

### Tier 4 — 30-role pool
Use up to 30 roles only if distinct responsibilities remain.

Rule:
No role may exist solely to increase agent count.

## 3. Escalation triggers

Escalate one tier if any occurs:

- two strong competing hypotheses remain;
- evidence conflict cannot be resolved;
- red team finds a blocking flaw;
- compatibility differs by OS/host/version;
- critical action lacks rollback;
- acceptance criteria cannot be objectively tested.

## 4. De-escalation triggers

Reduce active roles when:

- hypotheses converge on the same mechanism;
- new messages become redundant;
- marginal information gain is near zero;
- authoritative primary evidence resolves dispute;
- cost exceeds expected decision value.

## 5. Message policy

Do not broadcast everything.

Always retain:
- new evidence;
- material contradiction;
- discriminating test;
- blocking risk;
- minority hypothesis with strong evidence;
- changed confidence with reason.

Drop/compress:
- repeated agreement;
- paraphrases;
- stylistic commentary;
- unsupported confidence.

## 6. Judge policy

The judge ranks claims by:

1. reproducible direct evidence;
2. current primary/spec/vendor evidence;
3. independent corroboration;
4. coherent inference;
5. popularity/majority only as a weak signal.

## 7. Termination

Debate stops when one of these holds:

- acceptance evidence is complete;
- remaining hypotheses are non-material;
- expected value of another round is lower than cost;
- a hard blocker is identified and documented;
- execution/eval is now more informative than further discussion.

## 8. Anti-patterns

- 30 homogeneous clones.
- Majority vote without provenance.
- Endless critique with no discriminating test.
- One agent writes the answer and 29 agents merely approve it.
- Treating verbosity as depth.
- Treating hidden chain-of-thought length as a quality metric.
