# Task Goal Intelligence Native Skill Specification

Version: `4.0.0-native`

This specification is host-neutral. Runtime projections for Codex, ChatGPT, Claude-compatible harnesses, or other Agent Skills consumers may differ in metadata and tool syntax, but they must preserve the behavior below.

## Package shape

A conforming projection contains:

- one thin `SKILL.md` router;
- host policy metadata (`agents/...`) when the host supports it;
- progressively disclosed `references/`;
- deterministic `scripts/` for machine-checkable behavior when execution is available;
- separate eval corpora and validators;
- an exact upstream provenance lock for borrowed mechanisms.

The router is not the complete policy database. Large mechanisms belong in references and are loaded only at the phase that needs them.

## Required runtime behavior

### Entry

For substantive work, the goal gate runs before specialist routing. It establishes the current Goal Contract or identifies the exact decision-critical field that is missing.

### State

The canonical states are:

`ORIENT`, `DISCRIMINATE`, `COMMIT`, `EXECUTE`, `VERIFY`, `RECOVER`, `LEARN`.

A user correction is an interrupt. A route/tool failure is not a goal mutation.

### Complexity

The execution path is `DIRECT`, `INVESTIGATIVE`, or `ARCHITECTURAL`.

Hidden complexity can only ratchet upward during the same semantic goal. The harness may not downgrade a live task to evade evidence, coordination, acceptance tests, or a blocker. A user-specified semantic scope change creates a new goal event and may reclassify the path.

### Progress

Material progress requires at least one acceptance/evidence/decision-critical-uncertainty/observable-state delta. Activity volume is insufficient.

### Verification

A current success claim requires fresh evidence at the strongest owning layer practical for that claim. The harness must distinguish package presence, host load, invocation, effect, and verification.

### Recovery

Recovery identifies the first upstream failure and chooses a causally different route. A blocked slice is isolated while separable work continues. Three materially distinct failed repairs to one mechanism trigger architectural review.

### Learning

Real failures and user corrections may become candidate regression cases. They do not become permanent rules until target/protection/holdout/adversarial promotion slices pass.

## Progressive disclosure contract

The runtime router must point to, not duplicate, the detailed owners:

- `references/phase-machine.md` — state and transition semantics;
- `references/runtime-preamble.md` — machine protocol, trust boundary, degraded mode;
- `references/evidence-and-optimization.md` — root cause, fresh verification, evidence mesh, optimizer loop;
- `references/upstream-lock.json` — exact provenance.

## Native preamble contract

When executable, `goal_skill_start.py` returns protocol version, phase, path, goal version, goal fingerprint, missing core fields, and boolean gates. The host may add telemetry around this protocol but must not change its goal semantics.

When the script is not executable, the host uses degraded inline state evaluation without lowering the Goal Contract. It must not claim native preamble execution.

## Behavioral conformance

Repository conformance requires:

- package quick validation;
- full native state-machine oracle;
- old plugin routing protection;
- old Task Goal Intelligence v3 protection;
- no duplicate case IDs;
- all seven states exercised;
- exact upstream lock intact.

Hosted `HOST_LIVE` conformance is separate: the owning surface must prove discovery/load, implicit invocation, route selection, effect where applicable, and fresh verification behavior on that exact installed revision.
