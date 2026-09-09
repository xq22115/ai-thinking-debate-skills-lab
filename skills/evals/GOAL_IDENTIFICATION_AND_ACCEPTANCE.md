# Goal Identification and Acceptance Contract

Status: `CURRENT`
Updated: 2026-09-10

## Root goal

Turn the reasoning/debate skill lab into an evidence-backed, contamination-resistant evaluation system that can support a genuinely attributable fresh-context/private-holdout target-model execution, without allowing metadata, consensus, visible fixtures, or self-issued receipts to masquerade as stronger evidence.

## Ten independent goal-identification methods

| Method | Question | Converged result |
|---|---|---|
| 1. Literal imperative extraction | What concrete actions are repeatedly requested? | research deeply, execute, test, read back, and do not overclaim |
| 2. Deliverable reverse-engineering | What artifact would make the request objectively inspectable? | canonical repo contracts + receipts + CI + durable registry |
| 3. Current-state gap analysis | What is missing after the existing commit-reveal harness? | independently attributable target execution provenance |
| 4. Blocker inversion | What single false assumption could create a fake success? | trusting `manifest.fresh_context=true` as execution evidence |
| 5. Causal why-chain | Why is fresh-context/private holdout needed? | to separate learned/general reasoning from fixture familiarity or benchmark leakage |
| 6. Adversarial failure analysis | How could a system game the evaluation? | self-assert freshness, reuse visible labels, submit unrelated judge receipts, mutate responses, optimize evaluator artifacts |
| 7. Evidence-ladder analysis | Which promotion step has weakest ownership? | `SAME_MODEL_SMOKE -> FRESH_CONTEXT_RUN` without an owning-runtime receipt |
| 8. QUD/stakeholder analysis | What question must the evaluation actually answer? | did a specified target produce these responses under an independently attributable evaluation context? |
| 9. Counterfactual success test | What observation would change the project state? | hash-bound external/owning-runtime execution receipt + frozen responses + later commit-reveal scoring |
| 10. Owning-system reconciliation | Which system owns each truth claim? | GitHub owns executable contract; owning runtime owns execution/freshness provenance; Notion owns durable decision/debt context |

All ten methods converge on the same bottleneck: **measurement integrity and execution provenance**, not additional visible reasoning procedures.

## Acceptance tests

### A. Goal contract
- ROOT_GOAL is explicit and stable.
- Hard boundaries between manifest claims, execution evidence, scoring evidence, judge evidence, and host-live evidence are explicit.

### B. Research coverage
- At least 100 unique, relevance-screened source groups are recorded.
- 2026-06 through 2026-09 is prioritized.
- Same paper mirrored through multiple providers counts once.
- Source count is not treated as independent corroboration count.

### C. Evaluation harness
- Manifest-only fresh-context claims fail closed.
- A target execution receipt binds suite/run/target/manifest/response set.
- Receipt tampering or response mutation is rejected.
- Receipt binding does not claim semantic truth of the external runtime's statements.
- Private scoring still requires frozen responses + salted commit-reveal + actual oracle scoring.
- Independent judging still requires a designated case actually judged by an independent judge.

### D. Hosted verification
- Exact GitHub Actions commit/run/job is retained.
- Synthetic CI receipts are labeled as harness evidence only.
- No target-model capability promotion is inferred from synthetic CI.

### E. Independent execution debt
- Real fresh-context target-model run: required for promotion beyond current evidence.
- Real private-holdout scoring: required.
- Independent judge: required for semantic judge promotion.
- Authentic five-agent runtime: required where five-agent unanimity is claimed.
- Local/RDC host-live regression: required before host-live claims.

## Non-goals

- maximizing procedure count for appearance of depth
- treating 100 sources as 100 independent confirmations
- treating five roles in one model context as five independent agents
- claiming local execution without owning-runtime read-back
- calling a synthetic CI receipt a real model execution

## Hard invariants

- `MANIFEST_CLAIM != EXECUTION_EVIDENCE`
- `FRESH_CONTEXT_FLAG != FRESH_CONTEXT_PROOF`
- `BOUND_RECEIPT != SEMANTIC_TRUTH_OF_RUNTIME_CLAIM`
- `SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`
- `ROLE_COUNT != INDEPENDENT_AGENT_COUNT`
- `SYNTHETIC_CI_PASS != TARGET_MODEL_CAPABILITY`
- `ROBUSTNESS != NEVER_CHANGING`
- `CALIBRATED_ROBUSTNESS = INVARIANCE_WHEN_IRRELEVANT + SENSITIVITY_WHEN_DECISIVE`
