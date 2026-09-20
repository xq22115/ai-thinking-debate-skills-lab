# Skill Authoring Contract Reference

This reference expands the canonical `skill-authoring-engine` without bloating its routing surface.

## Capability contract template

```yaml
name: <lowercase-hyphenated>
purpose: <user-visible outcome>
triggers:
  positive: []
  negative: []
  ambiguous: []
  collisions: []
inputs: []
outputs: []
hosts: []
tools: []
permissions: []
side_effects: []
verification: []
rollback: []
status: experimental
```

## Multi-agent topology

Use an orchestrator-worker pattern for complex skill work.

The orchestrator owns:

- final Skill Contract;
- shared constraints;
- write-set assignment;
- dependency ordering;
- merge order;
- acceptance ledger;
- release decision.

Workers should receive bounded tasks and return artifacts/evidence, not competing final answers.

Parallel candidates:

- current host-spec research;
- trigger fixture generation;
- compatibility analysis;
- adversarial review;
- documentation/example drafting.

Serialize:

- edits to the same `SKILL.md`;
- registry/manifests;
- generated lock files;
- final merge/conflict resolution;
- release-status changes.

## Trigger-quality matrix

A mature skill should be evaluated against:

| Class | Goal |
| --- | --- |
| Positive | obvious intended requests select the skill |
| Negative | unrelated requests do not select it |
| Ambiguous | uncertain wording either routes conservatively or requests only necessary clarification |
| Collision | neighboring skills keep clear semantic ownership |
| Unsupported host | skill does not fabricate unavailable tools/runtime |
| Permission gap | skill reports authorization blockers accurately |
| Stale syntax | compatibility audit catches outdated packaging |
| Adversarial | prompt wording cannot force false completion claims |
| Regression | previously working triggers remain working |

## Progressive disclosure

Keep `SKILL.md` focused on:

- trigger;
- ownership;
- workflow;
- invariants;
- output contract;
- completion gate.

Move to `references/`:

- long examples;
- host matrices;
- API/version details;
- schemas;
- migration notes;
- deep rationale.

Move to `scripts/`:

- deterministic lint;
- manifest consistency;
- package generation;
- schema checks;
- reproducible transforms.

Move to tests/evals:

- trigger fixtures;
- routing collisions;
- host compatibility cases;
- negative/failure behavior;
- regression corpus.

## Promotion ladder

Recommended evidence states:

`DRAFT -> STATIC_VALIDATED -> ROUTING_EVALUATED -> INTEGRATION_VERIFIED -> HOST_LIVE_VERIFIED -> STABLE`

Do not skip directly from file creation to `STABLE`.
