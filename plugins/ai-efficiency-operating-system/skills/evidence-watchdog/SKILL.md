---
name: evidence-watchdog
description: Use when a claim of fixed, configured, installed, tested, live, deployed, delivered or complete must be proven, or when a stateful mutation requires postcondition/read-back evidence.
---

# Evidence Watchdog

A successful command, tool call, write, PR, CI check or executor statement is not the intended state transition.

## Separate state levels

Use the strongest level actually observed:

`DRAFTED → PACKAGED → IMPLEMENTED → TESTED → VERIFIED → HOST_LIVE → DEPLOYED → HEALTHY`

Do not skip levels by rhetoric.

For GitHub-backed skills/plugins, also keep the activation chain separate:

`SOURCE_RESOLVED → REGISTRATION_RESOLVED → VERSION_RESOLVED → INSTALLED → READ_BACK → DISCOVERED/REGISTERED → EXECUTED → OBSERVABLE_EFFECT → REGRESSION_PRESERVED`

A lower layer can never certify a higher layer. In particular, a source fetch, installer exit code, commit SHA, PR, or green CI does not prove that the owning runtime loaded or used the skill.

## Evidence hierarchy

Prefer the evidence that most directly observes the claim under test:

1. owning-runtime/user-path postcondition;
2. independent deterministic reproduction/read-back;
3. exact current implementation/configuration evidence bound to the reported revision;
4. maintainer/implementation evidence and high-signal practitioner/tooling evidence when it independently discriminates the mechanism;
5. authoritative static documentation for documented support/semantics;
6. indirect/reporting evidence;
7. unsupported hypothesis.

This is claim-specific, not a blanket source prestige ranking. Official documentation is evidence of documented support; it is not execution proof. A third-party recipe is operational evidence only when its mechanism, target/version and result can be independently checked. When sources disagree, use a discriminating target-runtime or exact-revision test rather than choosing by reputation alone.

Bind evidence to target identity, revision/version, requirement, observed time and expiry when state can drift.

## System invariants for material mutations

Before a material repair, declare the applicable invariants; after the repair, retest them on the exact reported state:

- existing working capability is preserved;
- permissions are not silently reduced;
- externally consumed input/output contracts remain compatible unless migration is explicitly accepted;
- failure is detectable rather than swallowed or presented as partial success;
- success has postcondition/read-back evidence;
- adjacent supported paths are not broken by the local change;
- an exact rollback target exists;
- evidence is bound to the exact target/revision;
- a search miss is not treated as absence until a causally distinct lookup/fetch route is tried;
- configured, registered, loaded, executed and observable-effect states are not collapsed;
- write/install success is not task success;
- feasibility conclusions are evidence-bound rather than decided by a single authority.

Any applicable invariant violation blocks `PASS`, even when the happy path succeeds.

## GitHub mutation closure

For repository writes, plugin/skill pulls, dependency updates and GitHub-backed configuration, require this closure when the layers are available:

`target identity → source identity → exact revision → write/install → read-back → requested behavior → adversarial/regression check → exact-run CI/runtime verification`

Track repository/default branch, current HEAD commit, search-hit commit when relevant, file/blob SHA, release/tag/package/marketplace version and installed revision separately. Never compress them into one ambiguous “version”.

If fuzzy search or a cached index says an object is missing while an exact repo/path/ref is known, pivot to exact lookup, direct fetch, code/tree/contents lookup or known-ref resolution before declaring absence. After two materially similar failures, changing wording alone is not a new route.

## Independence

The executor cannot self-certify material completion. When independent verification is required, evidence must come from a distinct observer/tool/runtime route, not a renamed role that shares the same unverified output.

If a state-sensitive epoch changes — resume, compaction, target/ref, cwd, tool/permission, instruction or skill revision — old evidence becomes history until refreshed.

`UNKNOWN` is first-class. If an effect may have happened but confirmation was lost, read back the postcondition before replay.

Read `references/evidence-completion.md` for the detailed gate and strict completion vocabulary. For repository-level GitHub work inside this project, also apply `docs/GITHUB_EXECUTION_INTEGRITY_POLICY.md` and `control-plane/ai-system/configs/execution-integrity-global.json` when those files are available in the active workspace.
