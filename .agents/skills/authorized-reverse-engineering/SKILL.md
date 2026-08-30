---
name: authorized-reverse-engineering
description: Use for authorized inspection of software, binaries, protocols or artifacts when static/dynamic evidence is needed to understand behavior, compatibility or defects.
---

# Authorized Reverse Engineering

## Purpose
Produce reproducible technical understanding of an authorized target while preserving artifact identity, toolchain provenance and evidence lineage.

## Activate when
Use for owned/authorized binaries, undocumented file formats, compatibility diagnosis, crash analysis, protocol behavior or implementation verification that source alone cannot answer.

## Do not activate
Do not use to bypass licensing, DRM, authentication, access controls, anti-abuse systems or another party's authorization boundary.

## Antigravity-native execution
Fingerprint the exact artifact before analysis. Prefer source/config/log evidence first, then static inspection, then the least-invasive dynamic probe that the active workspace and OS actually permit. Keep scripts and extracted references inside the skill/project artifacts, not as hidden assumptions.

## Workflow
1. Record authorization, target hash/version/architecture and objective.
2. Build hypotheses from source, symbols, metadata, logs and behavior.
3. Use the smallest toolchain that can discriminate them.
4. Bind observations to command/tool version and artifact hash.
5. Reproduce the conclusion independently where material.
6. State what remains unknown.

## Validation
A conclusion must be reproducible against the same artifact and distinguish observation from inference. A tool exit code alone is not evidence of the intended property.

## Boundaries
Never convert analysis capability into permission to defeat product controls. Prefer reversible, read-only inspection and preserve rollback/backups for any authorized mutation.