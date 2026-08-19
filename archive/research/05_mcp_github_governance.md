# MCP, GitHub and Governance Research

## Governance thesis
A serious AI engineering workflow should make repository evidence stronger than conversational memory.

## Recommended controls retained from prior research
- policy-as-code,
- TASK packet with revision and SHA256 digest,
- context receipt bound to repo/worktree/branch/base SHA,
- independent read-only reviewer,
- clean-runner verifier,
- append-only hash-chained event ledger,
- explicit state transitions,
- final-verdict CI,
- branch protections / rulesets / CODEOWNERS,
- pinned Actions,
- secret scanning.

## Known pitfalls
- stop hooks may fire on every response,
- worktree baseRef can miss unpushed HEAD,
- memory poisoning,
- MCP privilege risk,
- shells without sandbox,
- preview workflows and CI-trigger pitfalls,
- skipped-job/status spoofing,
- `pull_request_target` secret exposure risk,
- transcript/redaction leakage.

## MCP Sovereign line

### Relay v6.0.0
- partial SHA: `73905649...b2c7c`
- 168/168 tests reported
- 8 skills
- static audit 0 findings
- cloud relay and writable-app constraints remained.

### Relay v7.0.0
- partial SHA: `8dd4d6ab...5c848`
- 225/225 tests reported
- 78% combined coverage
- 8 skills
- 30 branch reports
- Mac/Gatekeeper/launchd/sync/app permissions not live-tested.

### Intelligence v8.0.0
- named in retained context.
- exact artifact metadata was not fully recoverable in this pass.

### Hard-Task Kernel v10.0.0
- 4 waves × 10 branches
- requirement-ID contract
- cross-examination
- evidence gates
- recovery
- blocked-on-failure semantics
- partial SHA: `90294f...a4150`

## Current GitHub connector fact for this archive run
- authenticated login: `xq22115-pixel`
- personal-account accessible repositories returned: `0`
- organization `xq22115` exposes writable repositories through the GitHub App
- available connector actions include repository file/branch/commit/PR operations
- no create-repository action was exposed

Therefore a dedicated new remote repository was **not** fabricated; this archive is staged on an isolated branch in `xq22115/demo-repository`.
