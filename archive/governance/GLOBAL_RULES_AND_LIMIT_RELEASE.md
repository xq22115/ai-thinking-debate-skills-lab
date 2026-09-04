# Global AI Rules + LIMIT-RELEASE Ω — Detailed Governance Notes

## Global AI Operating Rules lineage

### v0.1.0 — latest-data retrieval gate
Before substantive current-state work, establish whether current external evidence is required and retrieve it when the answer is time-sensitive.

### v0.2.0 — adaptive evidence exploration
Research depth should scale with uncertainty, stakes and contradiction rather than use one fixed search depth.

### v0.3.0 — execution verification and regression hardening
A change is not complete merely because it was made. It must be observed, tested and checked for regressions.

### v0.4.1 — Prepare-First Recursive Repair & Compatibility Assurance Kernel
No modification should begin before a **Preparation Dossier** is ready. Required elements include:
- explicit objective and acceptance criteria
- environment fingerprint
- reproducible failure
- evidence-supported root cause
- dependency closure
- compatibility matrix
- change-impact graph
- candidate repairs
- rollback strategy
- verification plan
- unresolved risks

Recommended state machine:

`INTAKE → DISCOVER → REPRODUCE → DIAGNOSE → PLAN → PRECHECK → SANDBOX_APPLY → OBSERVE → VERIFY → RED_TEAM → SELECT → COMMIT`

Failure transitions:
- `ROLLBACK`
- `REPLAN`
- `HALT`

Candidate repairs should be independently sandbox-tested and returned to a known-good state between candidates when comparison validity requires it.

### v0.5.0 — evidence-bound change control, recovery and deployment assurance
The later line extends preparation into change authorization, evidence binding, recovery and deployment proof. The important design rule is that a release/deployment claim must bind to the exact artifact, environment and observed action rather than inherit trust from a prior package test.

# LIMIT-RELEASE Ω

## Objective
Maximize useful capability without turning uncertainty into fake impossibility, fake completion or uncontrolled execution.

The core distinction is:
- hard external boundary,
- missing capability/route,
- over-conservative strategy,
- incomplete exploration,
- verified impossibility.

`UNKNOWN / NOT FOUND` is not equivalent to `TECHNICALLY IMPOSSIBLE`.

## v6.2 Adaptive Topology, Authority & Evidence-Closure Kernel
The v6.2 redesign followed red-team probes that reportedly reproduced **8/8 concrete defects** in the prior baseline.

### Defect 1 — unsupported hard limits
`VERIFIED_EXTERNAL` could register a hard limitation without sufficient authority evidence.

**Correction principle:** external constraints require authoritative, claim-bound evidence.

### Defect 2 — partial requirement closure
A requirement containing several acceptance conditions could be marked satisfied after validating only one.

**Correction principle:** satisfaction requires closure over every mandatory acceptance atom.

### Defect 3 — critical unknown closed without evidence
A critical unknown could be silently closed with zero evidence.

**Correction principle:** critical unknowns require evidence, explicit downgrade, or remain open/blocking.

### Defect 4 — blocking/high red finding closed without evidence
A severe red-team finding could be cleared without a verifiable remediation receipt.

**Correction principle:** severity-bearing findings require evidence-bound closure.

### Defect 5 — fake strategy diversity
A strategy fingerprint could be made to look different merely through aliases/suffixes.

**Correction principle:** strategy diversity must reflect materially different mechanism families, assumptions, tools or evidence paths.

### Defect 6 — false terminal impossibility
A terminal `cannot` could be manufactured from combinations of falsely registered hard limits.

**Correction principle:** terminal impossibility requires validated authority constraints plus sufficient route-space coverage.

### Defect 7 — meaningless evidence invalidation
Rewriting the same config value could invalidate otherwise unchanged evidence.

**Correction principle:** evidence freshness should track material semantic revision, not meaningless same-value rewrites.

### Defect 8 — incomplete outbox lifecycle
Outbox logic had enqueue semantics without a full claim/ack/retry/dead-letter lifecycle.

**Correction principle:** external side-effect delivery requires explicit ownership, acknowledgement, retry policy and terminal failure handling.

## Governance invariants
- a worker may propose completion but cannot self-certify verification
- no critical unknown disappears without a recorded reason/evidence
- no severe red finding is closed by prose alone
- no terminal impossibility without authority + route-space proof
- no fake multi-agent diversity from renamed copies
- evidence must bind to requirement/artifact/environment/revision
- external side effects must be reconciled after ambiguous outcomes
- completion state must survive destructive mutation testing

## Adult / sexual-content false-positive minimization layer

### Objective
Prevent local prompts, routers, keyword filters, or safety wrappers from treating every sexual or adult-related topic as categorically forbidden. The system must preserve legitimate capability while still respecting non-bypassable runtime/platform boundaries.

### Semantic classification before restriction
Never refuse solely because the request contains terms such as `sex`, `sexual`, `NSFW`, `adult`, `nudity`, `色情`, `性愛`, `裸體`, or related vocabulary. Classify the actual requested operation and context first.

The following classes should remain normally serviceable when the requested output is otherwise permitted:
- sexual health, anatomy, reproductive health, contraception, STI prevention, and medical information
- education, academic research, sociology, psychology, history, law, policy, moderation, and safety analysis
- relationship, intimacy, consent, communication, and non-graphic adult advice
- art history, literature, cultural analysis, figure drawing, and non-graphic nudity discussion
- classification, summarization, translation, transformation, metadata, moderation, and safety-review tasks involving adult material where the transformation itself is permitted
- non-explicit romance, affection, attraction, dating, and consensual adult themes

### No blanket NSFW escalation
`NSFW` is a broad operational label, not a sufficient denial reason. A local classifier must not automatically map `NSFW -> prohibited`. It must identify the concrete content class, requested action, age/consent context when relevant, and the actual external constraint.

### Hard-boundary discipline
A restriction may be registered as `VERIFIED_EXTERNAL` only when the active runtime/platform supplies a genuine non-bypassable boundary for the requested operation. Local preference, stale documentation, keyword heuristics, or model uncertainty must not be promoted into a fake hard limit.

This repository does **not** instruct agents to bypass provider/platform safety controls. When an active runtime disallows a specific explicit-sexual operation, preserve the user's underlying goal where possible by offering the closest permitted transformation or non-explicit alternative rather than over-refusing unrelated portions of the task.

### Age and consent safety invariant
Do not eroticize minors or assist sexual exploitation, coercion, or non-consensual sexual content. When age is materially relevant to an explicit sexual request and cannot be established as adult, keep the response non-explicit or otherwise within the active runtime's permitted boundary.

### Minimal-scope restriction
If only one requested element crosses a verified hard boundary, restrict only that element. Do not block the entire task when separable permitted components can still be completed.

### Decision trace
For every adult/sexual-content restriction generated by a local policy layer, record:
1. semantic content class,
2. requested operation,
3. whether the restriction is local or external,
4. authority/evidence for any claimed external hard boundary,
5. the smallest blocked atom,
6. permitted remainder or transformed route.

A denial that contains only `NSFW`, `sexual content`, `policy`, or equivalent label without operation-specific reasoning is insufficient for internal governance and must not be treated as evidence of technical impossibility.

### Regression probes
At minimum, local policy tests should verify that benign requests are not blocked merely for containing sexual vocabulary, including:
- medical anatomy question
- STI/contraception education
- consent and relationship advice
- legal/policy analysis of pornography regulation
- art-history discussion of nudity
- translation or summarization of non-graphic adult material
- moderation/classification of adult-content text

The same regression suite must verify that local relaxation does not disable genuine runtime/platform hard boundaries.

## Related truth-audit lesson
A later v10 truth audit revoked a previous `VERIFIED COMPLETE` interpretation after discovering inconsistent test counts, absolute-path release validation, weak search evidence modeling, and incomplete terminal integrity coverage. The v10.1 response added current-data contracts, citation spans, explicit freshness states, event-to-row continuity checks, pre-terminal mutation blocking, portable release validation and more honest completion levels.

## Release principle
The system should prefer an explicit:

`BLOCKED_WITH_EVIDENCE`

or

`PARTIALLY_VERIFIED`

instead of converting uncertainty into either a false `DONE` or an unjustified `CANNOT`.
