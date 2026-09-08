# Reference Architecture — Evidence-Gated Deliberation & Skills OS

Version: `1.4`

## Core architecture

```text
USER INTENT
  ↓
GOAL CONTRACT / OBJECTIVE AUDIT
  ├─ ROOT_GOAL / stated request / true outcome
  ├─ HARD_CONSTRAINTS / NON_GOALS
  ├─ ACCEPTANCE_TESTS vs PROXIES
  ├─ TARGET_IDENTITY / ENVIRONMENT
  ├─ specification uncertainty / intent drift
  └─ latest authorized goal revision
  ↓
CAPABILITY / COMPATIBILITY PRECHECK
  ↓
EPISTEMIC GATE
  ├─ claim ledger
  ├─ evidence sufficiency
  ├─ source provenance / dependence
  ├─ contradiction ledger
  └─ highest-value missing evidence
  ↓
SEMANTIC / ARGUMENT GATE (only when wording/inference is contested)
  ├─ literal vs pragmatic meaning
  ├─ QUD / crux
  ├─ claim / grounds / warrant
  ├─ argument scheme
  └─ decision-critical questions
  ↓
CAUSAL / ABDUCTIVE GATE (only when the crux is why/what-caused/what-if)
  ├─ candidate causal graph
  ├─ confounder / reverse / selection checks
  ├─ association vs intervention vs counterfactual
  └─ competing causal explanations
  ↓
HYPOTHESIS / ROOT-CAUSE LAYER
  ├─ materially different hypotheses
  ├─ discriminating tests
  └─ mechanism-level clustering
  ↓
DELIBERATION ROUTER (only if another independent role can change the decision)
  ├─ independent methods / evidence channels
  ├─ specialist roles
  ├─ red team / falsifier
  ├─ minority preservation
  └─ bias-resistant evidence-weighted judge
  ↓
VERIFIER / METAMORPHIC GATE (when consequence or brittleness warrants it)
  ├─ deterministic invariants first
  ├─ evaluator swap / blind labels
  ├─ semantics-preserving perturbations
  └─ hidden/adversarial variants
  ↓
VOI ROUTER
  ├─ next test/search/action value
  ├─ decision sensitivity
  ├─ expected information gain
  └─ stop / continue
  ↓
DECISION ROBUSTNESS GATE (when action is consequential)
  ├─ belief ≠ action separation
  ├─ asymmetric loss / regret
  ├─ reversibility / rollback
  ├─ distribution-shift transfer check
  ├─ sensitivity / threshold flip
  ├─ open-world / misspecification check
  └─ COMMIT / PROBE / PILOT / DEFER / ABSTAIN / ROBUST_FALLBACK
  ↓
PLAN / PRECHECK
  ├─ permissions
  ├─ security
  ├─ rollback
  └─ target/environment binding
  ↓
EXECUTION HARNESS
  ├─ goal-contract revision binding
  ├─ sandbox/tool boundary
  ├─ skill loader
  ├─ deterministic action layer
  └─ durable task state
  ↓
OBSERVE / EVAL
  ├─ tests / measurements
  ├─ traces / receipts
  ├─ contradiction updates
  ├─ counterexample checks
  ├─ goal/proxy drift checks
  ├─ shift / sensitivity updates
  └─ confidence update with evidence delta
  ↓
COMPLETION GATE
  ├─ outcome bound to current Goal Contract
  ├─ acceptance tests not gamed
  └─ status exactly matches evidence
  ↓
CHECKPOINT / ARCHIVE / DEPLOY
```

## Goal Contract rule

Before consequential work, normalize only the parts of the user's objective that affect the terminal state:

- `ROOT_GOAL`
- `HARD_CONSTRAINTS`
- `ACCEPTANCE_TESTS`
- `PROXIES / METRICS`
- `NON_GOALS`
- `TARGET_IDENTITY / ENVIRONMENT`
- material `OPEN_SPECIFICATION_UNCERTAINTY`
- `GOAL_CONTRACT_REVISION`

Consult `durable-agent-control-plane/GOAL_OBJECTIVE_AUDIT.md` when intent is ambiguous, mixed, dynamic, proxy-scored, or likely to drift.

Never invent private motives. The contract is a task-local interpretation, not a psychological profile.

## Progressive-disclosure rule

Do **not** execute every reasoning layer on every task.

At each gate ask:

1. Is the current goal/terminal state sufficiently specified for this action?
2. Is there a material unresolved uncertainty?
3. Can a cheaper direct observation/test settle it?
4. Will the next reasoning layer produce information that can change the decision?
5. Is the decision robust enough to act without that next layer?

If goal ambiguity can change an irreversible terminal state, resolve the highest-value specification uncertainty first.
If uncertainty is model/world-state rather than specification uncertainty, prefer internal evidence/tools over unnecessary user questions.
If a direct observation dominates, test rather than debate.

`DEPTH = GOAL FIDELITY + RELEVANT DISCRIMINATION + DECISION ROBUSTNESS, NOT MAXIMUM PROCEDURE COUNT`

## Goal / epistemic / decision state machine

`INTAKE → GOAL_NORMALIZE → SPECIFICATION_CHECK → CLAIM_NORMALIZE → EVIDENCE_SUFFICIENCY → INTERPRET → CAUSALIZE(if needed) → HYPOTHESIZE → TEST/DELIBERATE(if useful) → VERIFY(if useful) → UPDATE → DECIDE_ACTION → EXECUTE → OBSERVE → GOAL/PROXY_AUDIT → VERIFY_TARGET → COMMIT`

Valid non-success terminal/intermediate states include:

- `SPECIFICATION_UNCERTAIN`
- `GOAL_DRIFT_DETECTED`
- `UNRESOLVED_WITH_EVIDENCE_GAP`
- `BLOCKED_WITH_TARGET_BOUND_EVIDENCE`
- `DEFERRED_LOW_VOI`
- `PROBE_REQUIRED`
- `PILOT_REQUIRED`
- `SHIFT_UNSAFE`
- `THRESHOLD_SENSITIVE`
- `ROBUST_FALLBACK_SELECTED`
- `REPLAN`
- `ROLLBACK`

Do not force every path into a definitive yes/no conclusion or immediate commitment.

## Goal / evidence / decision invariants

- `USER_WORDING != FULL_INTENT`
- `STATED_PREFERENCE != VERIFIED_HELPFULNESS`
- `PROXY_SCORE != TRUE_GOAL`
- `TASK_COMPLETION != USER_SUCCESS`
- `SPECIFICATION_UNCERTAINTY != MODEL_UNCERTAINTY`
- `GOAL_DRIFT != PROGRESS`
- `ACCEPTANCE_TEST != LICENSE_TO_GAME_THE_TEST`
- `SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`
- `CONFIDENCE_CHANGE REQUIRES EVIDENCE_DELTA`
- `CONFLICTING_EVIDENCE != LICENSE_TO_PICK_ONE_SIDE`
- `RELEVANCE != RELIABILITY != DIAGNOSTICITY`
- `MORE_REASONING != BETTER_CALIBRATION`
- `MOST_LIKELY_STATE != BEST_ACTION`
- `CONFIDENCE != UTILITY`
- `CALIBRATED_IN_DOMAIN != CALIBRATED_UNDER_SHIFT`
- `IRREVERSIBLE_ACTION REQUIRES STRONGER_DECISION_EVIDENCE`
- `UNRESOLVED_STATE != NO_ACTION_POSSIBLE`
- `CONSENSUS != CORRECTNESS`
- `RHETORICAL_WIN != EPISTEMIC_WIN`
- `ASSOCIATION != INTERVENTION`
- `LOCAL_CAUSAL_PLAUSIBILITY != GLOBAL_GRAPH_COHERENCE`
- `VERIFIER_PASS != TASK_TRUTH`

## Change-authority rule

Classify changes to the task as:

- `METHOD_UPDATE`
- `WORLD_STATE_UPDATE`
- `AUTHORIZED_GOAL_UPDATE`
- `UNAUTHORIZED_GOAL_DRIFT`

Only an authorized goal update changes the desired terminal state. A blocker, tool limitation, model preference, metric improvement, or easier implementation route does not gain that authority.

## Status vocabulary

Never collapse these states:

`DRAFTED`, `PACKAGED`, `STATIC_VALIDATED`, `TESTED`, `REVIEWED`, `VERIFIED`, `HOST_LIVE_UNVERIFIED`, `HOST_LIVE_VERIFIED`, `DEPLOYED`, `HEALTHY`.

A task can be successfully researched while the underlying claim remains unresolved. An unresolved belief can still permit a justified `PROBE`, `PILOT`, or `ROBUST_FALLBACK`. Neither permits silently weakening the Goal Contract.

## Deliberation routing

Use more roles when uncertainty, conflicting evidence, impact, irreversibility, cross-platform compatibility, security risk, suspected distribution shift, or material objective ambiguity is high **and** another role provides a distinct method/evidence channel.

Do not use multiple agents to create different hidden versions of the user's goal. All roles share one Goal Contract revision; disagreement belongs in hypotheses/methods/evidence unless alternative goals are explicitly the task.

## Decision routing

Before a consequential commitment, separate:

- what the user-authorized outcome is;
- what is believed about the world;
- how uncertain that belief is;
- what each action costs under each live state;
- whether calibration is transferable;
- whether a small plausible assumption change flips the recommendation;
- whether a reversible probe/pilot or robust fallback dominates commitment.

Do not treat a calibrated probability estimate, a high preference score, or an acceptance-test pass as a complete decision policy.

## Anti-fake-completion gate

A task may declare `VERIFIED` only when all critical acceptance conditions have target-bound evidence, no blocking red-team finding remains, no critical unknown was closed without evidence, tests/proxies remain valid evidence of the intended outcome, regression scope was checked, and the status label exactly matches what was tested.

`UNRESOLVED` is preferable to fabricated certainty; `PROBE` or `PILOT` is preferable to brittle commitment; and a lower proxy score is preferable to gaming a metric that no longer tracks the user's goal.

## Compatibility adapter layer

Do not assume one skill format is natively portable everywhere. Keep a portable procedural core and host adapters for OpenAI/ChatGPT/Agents SDK, Claude/Claude Code/Agent Skills, MCP, OpenClaw, IDE agents, Windows, and macOS.

Host adapters may change invocation mechanics but must not weaken goal fidelity, epistemic, decision-robustness, verification, or completion invariants.