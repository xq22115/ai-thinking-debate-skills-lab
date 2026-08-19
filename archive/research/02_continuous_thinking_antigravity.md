# Continuous Thinking / Antigravity Research

## Research goal
Create a desktop/web continuous-thinking layer that behaves more like an agent loop: plan, act, observe, repair and continue until acceptance criteria are satisfied.

## Version lineage retained in cross-chat context
- v1.1.0 Web
- v1.0.0 Desktop
- v3.0.0
- v4.0.0
- v5.0.0 Continuity Mesh
- v6.0.0 Deliberation Kernel
- v6.1.0
- v6.2.0
- v7.0.0
- v8.0.0
- v8.1.0
- v8.2.0
- v8.3.0

These labels are archival; not every version had equal validation.

## Recurrent defects
- seconds-fast superficial replies,
- breakpoint discontinuity,
- weak memory,
- unclear before/after logic,
- name/entity misrecognition,
- unreliable enablement,
- new-window state loss,
- product-surface mixing,
- path/config drift,
- “fake complete” status.

## Concrete v7 findings
1. Package version shell and internal config naming diverged (`continuousThinkingV6` inside a v7 line).
2. `python3` was hard-coded, creating Windows portability problems.
3. Partial install plus rollback could leave a mixed state.

## v8.0.0-rc1 gate
Reported local package/ZIP tests passed, but stable release remained disallowed because:
- required `cryptography==46.0.7`,
- environment only had 46.0.4,
- live Antigravity was not verified.

## Live verification gaps
- actual account integration,
- agentapi/native subagents,
- Windows install/restart/hooks,
- macOS install/restart/hooks,
- rate limits,
- soak tests,
- semantic quality on real projects.

## Cross-platform rule
Never copy a macOS-oriented path/command directly into Windows setup, or vice versa. Environment fingerprint must include:
- OS and version,
- shell,
- Python/runtime path,
- package manager,
- architecture,
- permissions,
- product surface,
- extension/app version,
- restart/hook mechanism.

## Release policy
A ZIP passing local tests is not the same as:
- installed,
- account-enabled,
- compatible with both Windows and macOS,
- live-model validated,
- stable.
