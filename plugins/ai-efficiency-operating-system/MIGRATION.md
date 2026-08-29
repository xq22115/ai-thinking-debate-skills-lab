# Migration from v0.4 mega-skill

The v0.4 package accumulated useful mechanisms but made one model-facing skill own too many unrelated decisions. This migration retires the monolithic runtime entry while retaining its history and moving each responsibility to one semantic owner.

## Owner map

| v0.4 concept | New owner |
|---|---|
| task contract, correction/supersession, target identity, no-goal-shrink | `chief-of-staff-core` |
| plan selection, dependency graph, alternative routes | `plan-arbiter` |
| E0–E6 evidence, completion state, verifier admission, postcondition | `evidence-watchdog` |
| model-delta depth, coverage frontier, hypotheses, temporal/version search | `executive-research` |
| memory provenance, authority ceiling, rehydration | `memory-policy` |
| adaptive review, retry pivot, skill lifecycle, holdout promotion | `convergence-controller` |
| effect authority, approval and irreversible delegation | `autonomy-contract` |
| event journal, CAS/fencing, UNKNOWN effect, replay, delivery ACK | `persistent-work-ledger` |

## Retired as active runtime contracts

- private `57-module` count as a quality target;
- `T01–T70` count as a definition of completeness;
- one giant `SKILL.md` that duplicates specialists;
- package-specific schemas loaded into every reasoning turn;
- fixed time/source/agent counts as general depth proxies.

The old artifacts remain available in Git history. Their mechanisms are retained only where they have a clear owner and a current acceptance case.

## Preserved hard invariants

`FAILED_PATH != FAILED_GOAL`

`VISIBLE != AUTHORIZED != VERIFIED`

`CONFIGURED != LOADED != EXECUTED != OBSERVABLE_EFFECT`

`SOURCE_COUNT != EVIDENCE_INDEPENDENCE`

`ELAPSED_TIME != REASONING_DEPTH`

`EXECUTOR_SELF_REPORT != COMPLETION_PROOF`

`logical rewind != authority rewind != effect rewind != delivery rewind`
