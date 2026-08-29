---
name: capability-forensics
description: Use when an AI model, agent, plugin, desktop workflow, or tool appears unable to do something and the real bottleneck could be the model, harness, tool surface, permission, session, context, entitlement, environment, or runtime state.
---

# Capability Forensics

## Core principle

Diagnose the **actual limiting layer** before changing prompts, models, tools, or permissions. A reported inability is not yet a model limitation.

## Use this skill to answer

- What capability is required by the real end state?
- Which layer declares, exposes, authorizes, loads, invokes, and verifies that capability?
- Does the same model behave differently under another harness, session, or tool surface?
- Is a product/entitlement boundary being confused with a model limitation?

## Capability truth ladder

`DECLARED → VISIBLE → AUTHORIZED → LOADABLE → INVOKABLE → EFFECTIVE → VERIFIED`

Never collapse adjacent states. `installed != invokable`; `tool call returned != intended postcondition`.

## Workflow

1. Freeze the desired end state and protected capabilities.
2. Fingerprint model/preset, harness, host/OS/version, session, context/instructions, tool schemas, permissions/auth, entitlement/product gates, and required external surfaces.
3. Choose the smallest **differential probe** that changes one layer at a time.
4. Prefer same-model/different-harness and listed-tool/real-invocation comparisons before blaming model intelligence.
5. Read back the effective state or postcondition.
6. Classify the bottleneck and recommend the smallest reversible change that preserves the goal.

**REQUIRED REFERENCE:** read `references/capability-fingerprinting.md` for material investigations.

## Output

Return: required capability frontier, observed layer states, discriminating probes, bottleneck class, evidence, remaining unknowns, and the least-invasive next change.

## Boundary

Capability engineering maximizes **authorized** functionality and observability. It does not bypass provider safety controls, access controls, licensing/DRM, or authorization boundaries.
