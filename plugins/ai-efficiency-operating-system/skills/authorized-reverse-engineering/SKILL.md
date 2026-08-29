---
name: authorized-reverse-engineering
description: Use when analyzing software, firmware, binaries, or protocols the user is authorized to inspect and static or dynamic reverse engineering is needed to understand behavior, compatibility, architecture, regressions, formats, or undocumented interfaces.
---

# Authorized Reverse Engineering

## Core principle

Reverse engineering is an evidence workflow: pin the exact artifact, build competing behavioral hypotheses, and move from static structure to dynamic observation only when the next layer adds material information.

## Entry contract

Before analysis, establish:

- authorized target/scope;
- exact artifact hash, version/build and architecture;
- analysis objective and prohibited effects;
- available analysis runtime/tool versions;
- whether observation must remain read-only/non-destructive.

If authorization or target identity is unclear, stop effectful analysis and resolve it first.

## Workflow

1. Fingerprint the artifact and toolchain.
2. Start static: headers, imports/exports, strings, symbols, sections, functions, xrefs, call graph, decompilation, control/data flow.
3. Turn findings into hypotheses with predicted observations.
4. Use dynamic instrumentation only when it discriminates unresolved hypotheses and is authorized.
5. Correlate static addresses/functions with runtime observations.
6. Preserve annotations, hashes, tool versions, evidence and uncertainty.
7. Compare versions with normalized symbols/function hashes when useful; do not copy annotations across builds without compatibility evidence.

**REQUIRED REFERENCE:** read `references/reverse-engineering-playbook.md` before material binary analysis.

## Useful expert patterns

- headless Ghidra/PyGhidra automation;
- MCP-mediated decompile/xref/call-graph/dataflow queries;
- atomic/batch annotations;
- cross-binary function-hash documentation transfer;
- static→dynamic handoff to authorized instrumentation;
- version-diff and regression localization.

## Output

Return artifact identity, architecture/behavior map, hypotheses, evidence, confidence, unresolved unknowns, and safe next discriminating action.

## Boundary

Do not use this skill to bypass authentication/access controls, licensing/DRM, extract credentials/secrets, establish persistence, evade monitoring, or analyze targets the user is not authorized to inspect.
