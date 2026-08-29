# Control contract

## Requirement IR

Keep requirements traceable to the user's source request:

- `source_fragment`
- `normalized_meaning`
- `strength = HARD | IMPORTANT | OPTIONAL`
- `forbidden_substitutions`
- `success_criterion`
- `failure_criterion`
- `required_proof_surface`
- `dependencies`
- `supersession`

A derived requirement may refine a parent but cannot weaken it.

## Uncertainty resolver

Classify uncertainty before deciding the next action:

- **fact uncertainty** → primary sources, code/data/environment observation;
- **preference uncertainty** → user choice or an explicitly stated default;
- **behavior uncertainty** → cheap executable prototype/reproduction.

Do not ask the user for a fact that can be retrieved. Do not research a preference as if it were an external fact. Do not settle runtime behavior only by prose.

## Work topology

For large work maintain:

- destination — state that ends the task;
- frontier — actionable questions/steps;
- fog — in-scope uncertainty not yet ready to plan deeply;
- out-of-scope — intentionally excluded work.

Plan the frontier, not imaginary detail deep inside the fog.

## Capability truth

Track capability stages separately:

`DISCOVERED → CONFIGURED → INSTALLED → LOADABLE → INVOKABLE → VERIFIED`

A skill/plugin can guide behavior but cannot mint missing filesystem, subagent, background, browser or write permissions.

## One primary phase owner

If multiple skills seem relevant, choose the owner whose output changes the next state transition. Other skills may advise but do not compete for final phase authority.

Keyword collisions never decide ownership by themselves. Example: a request to compare two plans "and verify assumptions" is still plan-owned until a specific factual gate becomes the blocker.

## Scope-loss test

Before accepting a workaround ask:

1. Which required capability is preserved?
2. Which is reduced or removed?
3. Is that tradeoff allowed by the current contract?
4. Can the result be verified at the required proof surface?

If a required capability is silently dropped, reject the workaround as a final solution.
