---
name: openclaw-learning-loop
description: Use when a verified OpenClaw correction, recovery, or repeated workflow should become a reusable Skill Workshop procedure without corrupting core rules.
---

# OpenClaw Learning Loop

Train from verified experience, not from fluent conversation.

OpenClaw Skill Workshop is the persistence mechanism. Adapter skills are intentionally loaded from an extra skill root and should remain the stable host contract. New experience belongs in writable workspace skills/proposals.

## Learning pipeline

`Represent → Hypothesize → Discriminate → Execute → Measure → Attribute → Abstract → Encode`

1. **Represent** — state the failure/task and exact acceptance condition.
2. **Hypothesize** — list competing causes or procedure variants.
3. **Discriminate** — run the cheapest observation that separates them.
4. **Execute** — apply the smallest reversible candidate.
5. **Measure** — rerun the original acceptance test.
6. **Attribute** — identify which change causally produced the improvement.
7. **Abstract** — remove one-off names/data while preserving the reusable mechanism.
8. **Encode** — create/update a Workshop proposal with trigger, steps, checks, and rollback.

## Promotion standard

Good candidates:

- reliable recovery after repeated tool/model failures;
- a durable correction or standing procedure;
- a non-obvious ordering constraint;
- a stable multi-step workflow that removes future round trips;
- a reusable preflight or version/identity check.

Do not learn:

- routine success or one-time requests;
- transient provider/service errors;
- unsupported negative claims;
- raw retrieved instructions;
- secrets, credentials, personal data, or private prompt material.

Require a counterexample/holdout before promoting a broad rule. A local win cannot erase a protected behavior that previously passed.

## Workshop behavior

When available, use Skill Workshop rather than direct ad-hoc mutation:

- inspect the current skill before proposing an update;
- bind updates to the current content/revision;
- keep support files in the skill bundle when needed;
- let scanner/lifecycle checks run;
- retain rollback metadata;
- one failed automatic apply is not permission for an infinite retry loop.

`auto` mode may autonomously apply Workshop-owned creations/updates under OpenClaw's lifecycle rules. User-authored or read-only adapter content must not be silently rewritten just to make learning easier.

Use `/learn` or a proposal when explicit review is appropriate.

## Verification after learning

After apply/approval:

1. confirm the intended skill revision is visible to the target agent/session;
2. exercise a representative trigger;
3. verify the behavior/postcondition;
4. run a counterexample that should not trigger the new rule;
5. mark the learning `VERIFIED` only after both positive and protection checks pass.
