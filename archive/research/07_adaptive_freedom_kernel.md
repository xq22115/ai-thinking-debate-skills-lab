# Adaptive Freedom Kernel Research

## Artifact
**Adaptive Freedom Kernel v2.0.0**

Generated: 2026-08-11.

## Defensible status
`PACKAGE_TESTED / NEEDS_HOST_VERIFICATION / WINDOWS_NOT_TESTED_NO_PWSH / LIVE_PROVIDER_NOT_TESTED`

The final ZIP bytes were extracted to clean directories and re-tested. This proves package-level/runtime behavior in the build environment, not real ChatGPT/Codex/Cline/Claude/Copilot/OpenHands host loading or live-provider quality improvement.

## Validation evidence

### Package integrity
- Full package internal SHA: **100/100**
- Agent Skill: **9/9**
- Codex Plugin: **11/11**

### Behavior tests
- truth/completion/release: **51/51 PASS**
- recovery/concurrency/session/MCP/CLI: **21/21 PASS**
- installer/planning/scaling: **17/17 PASS**
- unique total: **89/89 PASS**
- `ResourceWarning` treated as an error

### Static architecture validation
- **71/71 PASS**

### Engineering audit
- first round: 10 deterministic OS review processes
- cross review: 10 deterministic OS review processes
- maximum in-flight per round: 10
- these were **not** statistically independent frontier-model agents

### Local installed-runtime smoke
- evidence level: `FILES_INSTALLED`
- host verified: false
- live provider verified: false
- path with spaces: tested
- stdio MCP started: true
- MCP tool count: **17**
- self-certification tools exposed: **0**
- observation remained `UNVERIFIED`
- completion gate correctly rejected unverified state
- integrity check passed

### Codex renderer smoke
- generated absolute Python, launcher and DB paths
- handled paths containing spaces
- generated machine-specific MCP wiring
- source Codex plugin intentionally remains Skill-only

## Evidence ladder

`UNVERIFIED → SOURCE_VERIFIED → PACKAGE_TESTED → FILES_INSTALLED → HOST_VERIFIED → LIVE_PROVIDER_VERIFIED`

No claim may be promoted beyond the highest level actually observed.

## Major defects fixed in v2

1. **Shallow completion booleans** — v1 could trust booleans instead of criterion/invariant evidence closure.
2. **Rigid dirty-state gate** — repair path added through trusted checkpoint repair without reopening normal writes.
3. **O(n²)-like snapshot growth** — replaced full snapshot per mutation with dirty/sealed event sealing and selective semantic checkpoints.
4. **Destructive checkpoint restore** — prototype could cascade-delete audit history; final restore is in-place with append-only events/checkpoints.
5. **Receipt/evidence misbinding** — verifier receipt identity/digest/URL is now bound to the exact evidence object.
6. **False IMPOSSIBLE conclusions** — recorded failed routes alone are insufficient; route-space coverage must be independently verified and invalidated when a new mechanism family appears.
7. **Provider-session cross-talk** — provider-session identity isolation and explicit-resume semantics added.
8. **Prompt-copy host adapters** — architecture split into thin Agent Skill, durable Control Plane and machine-observed capability adapters.
9. **Fragile Codex paths** — machine-specific absolute MCP wiring is rendered from a verified install receipt.
10. **Unsafe MCP write surface** — provisional exploration writes are allowed while attestation/certification operations are excluded.

## Trust boundary
The Control Plane can prevent self-certification through exposed MCP/Admin surfaces **only when host/OS tool boundaries are actually enforced**. It is not a sandbox against an actor with unrestricted same-user local Python/SQLite access.

## Explicitly not proven
- Windows PowerShell installer execution or physical Windows installation
- ChatGPT Desktop/Skills/Work loading
- Codex host loading of the rendered plugin
- Cline / Claude / GitHub Copilot / OpenHands / Microsoft Agent Framework / LangGraph live host loading
- statistically significant live-provider quality or completion-rate gains
- ten statistically independent frontier-model agents

## Artifact hashes
- `adaptive-freedom-kernel-v2.0.0.zip` — `f39b7ae1c01c22dfeab57bdb5d68668764112a8b0501af096cdc840b47a24e22`
- `adaptive-freedom-kernel-agent-skill-v2.0.0.zip` — `078b5dc0d71f3145da08d5c0af886997c578f9b93f2214b604a5d32986d52067`
- `adaptive-freedom-kernel-codex-plugin-v2.0.0.zip` — `48d55519b2e0cd4db2cd94195d78c0e523f6b8e66a7c8935955198eeb2bfe803`
- ChatGPT custom instructions — `4aed9032e9f198c833589de19fa199f51869b16f75afea48d74edc7a3222f505`
- compact custom instructions — `e79a58850d99da4ac889a4ecb42c6beb6f0b46b6e2545e0c4d842d5156038f9b`

## Architectural lesson
The key shift is from “a clever prompt that tries to be free” to a **portable exploration policy + persistent evidence/state control plane + host-specific capability observation**. Exploration may be broad; completion and external-impact claims remain evidence-gated.
