---
name: evidence-gap-research
description: Identify the minimum evidence needed to accept or reject important claims. Use for research, diagnosis, verification, high-stakes decisions, and any task where unsupported confidence would be costly.
---

# Evidence Gap Research

Version: `0.1.0-rc1`

## Objective

Convert a vague research task into a claim-evidence program. Do not treat search volume as proof.

## Workflow

1. Restate the decision or deliverable in testable terms.
2. Enumerate material claims that must be true for success.
3. Classify each claim as `FACT`, `INFERENCE`, `ASSUMPTION`, or `UNKNOWN`.
4. For each non-trivial claim, record the strongest available evidence and the strongest plausible contradiction.
5. Prefer current primary/spec/vendor sources for unstable technical claims.
6. Search specifically for missing evidence and counterexamples, not only confirming sources.
7. Stop only when every critical claim is either supported, rejected, or explicitly unresolved.

## Output Contract

Return:
- claim ledger;
- evidence gaps;
- contradictions;
- source freshness/version notes;
- unresolved critical unknowns;
- confidence with reasons.

## Completion Gate

Never say `verified` when a critical claim has no evidence bound to the actual target environment.