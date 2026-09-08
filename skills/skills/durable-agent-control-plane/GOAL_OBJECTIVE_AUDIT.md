# Goal Contract & Objective Uncertainty Audit

Status: `EXPERIMENTAL REFERENCE / USE BEFORE CONSEQUENTIAL EXECUTION`

Purpose: prevent capable reasoning/execution from optimizing the wrong target. Separate what the user literally requested, what outcome they actually need, what proxy/metric is used to measure success, and what constraints must not be traded away. Use when goals are ambiguous, multi-part, evolving, proxy-scored, high-impact, or delegated across agents/tools.

## Core invariants

- `USER_WORDING != FULL_INTENT`
- `STATED_PREFERENCE != VERIFIED_HELPFULNESS`
- `PROXY_SCORE != TRUE_GOAL`
- `TASK_COMPLETION != USER_SUCCESS`
- `MODEL_STATED_OBJECTIVE != REVEALED_DECISION_POLICY`
- `ACCEPTANCE_TEST != LICENSE_TO_GAME_THE_TEST`
- `LOCALLY_OPTIMAL_SUBTASK != GLOBALLY_GOAL_FAITHFUL`
- `GOAL_DRIFT != PROGRESS`
- `AMBIGUITY != PERMISSION_TO_CHOOSE_THE_EASIEST_INTERPRETATION`
- `CLARIFICATION_COST != ZERO`
- `SPECIFICATION_UNCERTAINTY != MODEL_UNCERTAINTY`

## 1. Goal Contract

For consequential or complex tasks, maintain a compact contract with only decision-relevant fields:

- `ROOT_GOAL` — the outcome the work is meant to achieve;
- `USER_STATED_REQUEST` — literal instruction/request;
- `SUCCESS_OUTCOME` — observable state that would actually count as useful success;
- `HARD_CONSTRAINTS` — conditions that cannot be traded away for performance;
- `ACCEPTANCE_TESTS` — observations/tests used as evidence of success;
- `PROXIES / METRICS` — measurable approximations, explicitly labeled as proxies;
- `NON_GOALS` — tempting adjacent outcomes that must not replace the task;
- `TARGET_IDENTITY / ENVIRONMENT` — which account, host, version, artifact, user context, or system the goal applies to;
- `OPEN_SPECIFICATION_UNCERTAINTY` — unresolved ambiguity that could change the final state;
- `LATEST_AUTHORIZED_UPDATE` — the newest user-authoritative correction to the contract.

Do not make every field verbose. The point is to preserve identity and detect drift.

## 2. Four layers of objective meaning

Keep these distinct:

1. **Literal request** — what the words explicitly ask for.
2. **Instrumental subgoal** — a method believed to help achieve the goal.
3. **Acceptance proxy** — a measurable signal used to verify progress/success.
4. **Outcome intent** — the state that would make the task genuinely successful for the user.

Example pattern:

`outcome intent -> chosen method -> proxy -> observed score`

Never silently reverse this into:

`maximize observed score -> therefore outcome achieved`.

## 3. Specification uncertainty vs model uncertainty

### Specification uncertainty
Uncertainty about what the user wants or what counts as success.

Examples:
- ambiguous target/account/version;
- unclear tradeoff between speed and accuracy;
- mixed goals in one conversation;
- unclear whether a metric is a means or the true end;
- conflicting user instructions from different times.

### Model uncertainty
Uncertainty about facts, predictions, causal mechanisms, tool state, or implementation.

Do not answer specification uncertainty by searching harder for facts. Do not answer model uncertainty by asking the user questions that an authoritative read/test can resolve.

## 4. Clarification value gate

Clarifying questions have cost. Ask only when unresolved specification uncertainty can materially change the final state or risk.

For each possible clarification, estimate qualitatively:

- probability different answers lead to materially different action;
- consequence of choosing the wrong interpretation;
- whether the uncertainty can be resolved internally from existing user-authoritative context;
- cost/friction of asking;
- whether a reversible default is available.

Prefer:

`highest decision-value clarification` over `ask everything uncertain`.

If clarification is low-value and a reversible, clearly labeled default exists, proceed with that default and preserve the assumption.

## 5. Goal drift detection

Trigger a drift audit when:

- the task becomes mostly about a blocker/controller rather than the original outcome;
- a metric/benchmark starts replacing the user outcome;
- an intermediate artifact becomes treated as the final deliverable;
- a tool's easiest capability shapes the goal;
- repeated failures cause silent lowering of constraints or acceptance criteria;
- multi-agent branches optimize different interpretations;
- new evidence changes feasibility and someone changes the goal instead of the method;
- the latest plan cannot be mapped back to `ROOT_GOAL` or an acceptance test.

Classify changes as:

- `METHOD_UPDATE` — same goal, better route;
- `WORLD_STATE_UPDATE` — new evidence changes feasibility/uncertainty;
- `AUTHORIZED_GOAL_UPDATE` — user explicitly changed the goal;
- `UNAUTHORIZED_GOAL_DRIFT` — system/agent changed desired terminal state without user authority.

Only `AUTHORIZED_GOAL_UPDATE` changes `ROOT_GOAL`.

## 6. Proxy / Goodhart audit

For every decision-critical proxy/metric, ask:

- What true outcome is this proxy intended to measure?
- Can the proxy improve while the true outcome stays flat or worsens?
- Can the agent directly manipulate the measurement/evaluator instead of the outcome?
- Does the proxy omit quality dimensions the user cares about?
- Are there threshold effects where optimizing beyond a point becomes harmful?
- Is the proxy being used outside the context where it correlated with the true goal?

Mark a proxy:

- `TIGHT_PROXY` — strong target-bound evidence it tracks the outcome;
- `USEFUL_BUT_GAMEABLE` — informative but exploitable/incomplete;
- `WEAK_PROXY` — low diagnosticity for the true outcome;
- `UNVALIDATED_PROXY` — relationship to the true outcome is not established.

Never treat a proxy label as permanent; distribution shift can weaken it.

## 7. Revealed-goal / behavior consistency

When a system, agent, or planner claims to optimize objective O, compare that claim with observed choices under controlled tradeoffs.

Ask:

- Do choices remain consistent with O when costs change?
- Does the policy sacrifice the stated priority for another latent objective such as speed, score, brevity, approval, or test passing?
- Can the system accurately state the tradeoff it is behaviorally making?

`SELF_DESCRIPTION_OF_GOAL` is evidence about the model's report, not proof of the operative policy.

For user goals, do not infer deep personal values from isolated behavior. Use revealed-behavior analysis only for task-local tradeoffs and keep interpretation bounded.

## 8. Preference vs helpfulness

A preferred-looking answer/plan is not automatically the one that produces better task outcomes.

When practical, separate:

- `PREFERENCE_SIGNAL` — which output the user/model/judge likes;
- `TASK_SUCCESS_SIGNAL` — whether the user actually completes/achieves the target;
- `INTERACTION_QUALITY` — friction, pacing, clarity, confirmations;
- `OUTCOME_QUALITY` — correctness, utility, durability, side effects.

Do not optimize one dimension as a universal substitute for the others.

## 9. Constraint hierarchy

Some objectives are lexicographic rather than compensatory: a hard constraint may not be traded for more score on another dimension.

Represent when needed:

`HARD_CONSTRAINTS -> must pass first`
`PRIMARY_OUTCOME -> optimize subject to constraints`
`SECONDARY_PREFERENCES -> optimize only after higher levels are satisfied`

Do not average a hard veto into a scalar score.

## 10. Multi-agent goal coherence

Before parallelizing:

- all agents receive the same `ROOT_GOAL`, `HARD_CONSTRAINTS`, `ACCEPTANCE_TESTS`, and `NON_GOALS`;
- role diversity may change methods/evidence, not terminal-state authority;
- any proposed goal update is returned to the coordinator as a proposal, not silently adopted;
- the judge scores contributions against the shared contract rather than role rhetoric.

An agent that optimizes a different terminal state is not a useful independent perspective unless the task explicitly asks for alternative goals.

## 11. Acceptance-test integrity

Acceptance tests are evidence instruments, not the objective itself.

Rules:

- do not modify/disable/weaken tests merely to pass unless changing the test is explicitly the task;
- do not count evaluator manipulation as task progress;
- verify that passing tests still imply the intended outcome after material system changes;
- include at least one outcome-oriented check when proxy gaming is plausible;
- preserve failed/negative evidence rather than suppressing it.

## 12. Objective update protocol

When the user changes direction:

1. identify whether the new message changes method, constraint, priority, or terminal outcome;
2. update only affected Goal Contract fields;
3. preserve superseded values and the reason/date when durable traceability matters;
4. invalidate plans/tests that depended on the old contract;
5. re-run decision/acceptance checks only where the change is material.

Do not treat every conversational refinement as a full task reset.

## 13. Output contract

When objective uncertainty is material, expose a compact auditable summary:

- normalized root goal;
- hard constraints / non-goals;
- key proxy vs true-outcome distinction;
- material specification uncertainty;
- highest-value clarification or safe default;
- goal-drift/proxy-gaming warnings;
- acceptance tests that actually bind to the intended outcome;
- any authorized goal update.

Do not reveal private chain-of-thought.

## 14. Research signal

Recent evidence supports several cautions:

- real conversational intent is often ambiguous, dynamic, or mixed-goal, and explicit intent rewriting can improve downstream planning;
- structured clarification should distinguish specification uncertainty from model uncertainty and ask only high-value questions;
- preference signals can diverge from actual user task helpfulness;
- aggregate preferences can differ sharply from individual preferences;
- a model's stated preferences/objective can diverge from the cost function implied by its behavior;
- reasoning-capable agents can exploit imperfect specifications at non-negligible rates, so proxy/test optimization must be audited separately from genuine goal completion.

Use this reference to preserve goal fidelity, not to invent hidden user motives.