# Master Timeline

## 2026-07-26
### Adlerian KnowledgeBase v6.0
- Prior result: artifact/parsing/SQLite/scripts/ZIP reported complete.
- Reported retrieval metrics: Recall@5 0.978469, MRR 0.912888, nDCG@10 0.933423.
- Reported safety examples blocked: 4/4.
- Important limitation: no model fine-tuning; no claim of clinical validation.
- Status: `PARTIALLY_VERIFIED`.

### Universal Context Intelligence Skill v1.0.1
- Reported 21/21 Python tests plus API/SQLite/CLI/install/parse/integrity checks.
- Explicitly unsupported/unverified: Docker, Raycast, MCP runtime, real LLM providers, Qdrant/Graphiti/Neo4j adapters, LongMemEval/LoCoMo, human clinical/cultural review.
- Status: `PARTIALLY_VERIFIED`.

## 2026-07-27
### Multi-agent governance research
- Prior conclusion: architecture was partially verified.
- Key governance principle: Git task packets, commits, diffs, raw tests and CI outrank memory/summaries/chat.
- Recommended controls included:
  - policy-as-code,
  - versioned TASK contract + SHA256 digest,
  - context receipt binding repo/worktree/branch/base SHA,
  - independent read-only reviewer,
  - clean-runner verifier,
  - append-only hash-chained event ledger,
  - explicit state-machine transitions,
  - final-verdict CI,
  - rulesets/CODEOWNERS,
  - pinned GitHub Actions,
  - secret scanning.
- Memory layers such as Mem0/Graphiti were treated as non-authoritative.

### Editor agent caveat
- Prior research stated Roo Code official extension had stopped on 2026-05-15 and Cline Agent Teams did not provide the same full multi-agent behavior inside VS Code/JetBrains extensions.
- This is preserved as an `ARCHIVAL_CLAIM` and should be re-verified before current use.

## 2026-07-28
### Capability Hub v0.2.0
- SHA-256: `11509a1bc634e252519b938ba2ebf53dba38828a5b64bbf8f1b050b3a5dddfeb`
- Reported: 25/25 tests, 20 eval cases, 62 manifest files, 4 skills, 6 locked sources.
- Limitations: not deployed to HTTPS; no API-key/account access; no paid end-to-end test.
- Status: `PARTIALLY_VERIFIED`.

### Capability Hub v0.3.0
- SHA-256: `e8a077af99406890a4cd4ff85d257c3b4b83e1f5ea366bf453ba3108aa2816bc`
- Reported: 41/41 tests, 40 eval cases, 10/10 skills validated, 28 source records, 24 commit pins.
- Status: `PARTIALLY_VERIFIED`.

### MCP Sovereign Relay v6.0.0
- SHA-256 prefix/suffix preserved from prior context: `73905649...b2c7c`
- Reported: 168/168 tests, 8 skills, static audit 0 findings.
- Limitation: writable app and cloud relay constraints; no direct localhost/web assumption.
- Status: `PARTIALLY_VERIFIED`.

### MCP Sovereign Relay v7.0.0
- SHA-256 prefix/suffix: `8dd4d6ab...5c848`
- Reported: 225/225 tests, 78% combined coverage, 8 skills, 30 branch reports.
- Unverified: user Mac/Gatekeeper/launchd/sync/app permissions; private MCP not assumed native in ChatGPT Plus.
- Status: `PARTIALLY_VERIFIED`.

### MCP Sovereign Hard-Task Kernel v10.0.0
- Architecture: 4 waves × 10 branches, requirement-ID contract, cross-examination, evidence gates, recovery and blocked-on-failure semantics.
- SHA-256 preserved partially: `90294f...a4150`
- Status: `PARTIALLY_VERIFIED`.

## 2026-08-01 to 2026-08-03
### Continuous Thinking / Antigravity
- Version line progressed through v7 and v8 release candidates and later archive labels up to v8.3.0.
- v7 concrete drift found:
  - v7 shell containing `continuousThinkingV6`,
  - hard-coded `python3`,
  - partial-install/rollback mixed-state risk.
- v8.0.0-rc1 local ZIP tests were reported passing, but stable release was blocked.
- Dependency mismatch: package expected `cryptography==46.0.7`; environment had 46.0.4.
- Unverified:
  - live Antigravity lifecycle,
  - Windows/macOS install/restart/hooks,
  - native subagent lifecycle,
  - soak behavior,
  - rate limits,
  - real-project semantic quality.
- Status: `UNVERIFIED_LIVE` / `BLOCKED`.

## 2026-08-11
### Reusable agent patterns identified
- LangGraph: checkpoint/replay/interrupt/retry.
- AutoGen Magentic-One: facts / plan / progress ledgers plus stall-triggered replanning.
- OpenHands: idle should not equal terminal completion.
- Aider: lint/tests feed failures back into repair.
- Status: `ARCHIVAL_CLAIM` until refreshed against current upstream versions.

## 2026-08-13 to 2026-08-16
### OpenClaw
Prior chat research recorded:
- stable `v2026.7.1-2` with GitHub latest dated 2026-08-04,
- extended-stable `2026.6.34` dated 2026-08-08,
- stable vs beta/dev/main separation,
- production/lab split,
- macOS: OpenClaw.app + Local Gateway,
- Windows: Hub + app-owned WSL Gateway + native node + Local MCP,
- stable config references such as `agents.list[]` and Skill Workshop `autonomous.enabled=false`,
- 2026-08-16 main-branch drift toward `agents.entries.*` and Workshop `mode=off|propose|auto`,
- use of ACP/acpx, Task/Task Flow, Cron command/condition in the researched line.
Status: `ARCHIVAL_CLAIM` — must be rechecked before direct installation because OpenClaw was moving quickly.

## 2026-08-18
### Archive consolidation
- Cross-chat material consolidated into this GitHub-ready package.
- GitHub App access was found on organization `xq22115`; because no create-repository action exists, the archive was staged non-destructively on branch `ai-research-vault-2026-import` inside `xq22115/demo-repository`.
- Dedicated repository creation remains a separate unresolved step.
