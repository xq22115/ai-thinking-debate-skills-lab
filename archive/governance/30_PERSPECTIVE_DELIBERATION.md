# 30-Perspective Deliberation / Audit

> These are 30 explicit review perspectives used to challenge the archive. They are not represented as 30 background processes.

| # / Role | Debate focus | Result |
|---|---|---|
| 1. Archive Historian | Separate chronology from current truth. | Preserve dates/version lineage; never silently modernize old claims. |
| 2. Evidence Auditor | Challenge every completion claim. | Use VERIFIED/PARTIAL/UNVERIFIED/ARCHIVAL/BLOCKED labels. |
| 3. Version Forensics | Detect stale or mixed version references. | Antigravity v7 naming drift is a canonical warning. |
| 4. Windows Compatibility | Reject Unix assumptions on Windows. | Hard-coded python3/path/hook assumptions require environment fingerprinting. |
| 5. macOS Compatibility | Check Gatekeeper/launchd/app lifecycle. | Do not infer macOS install success from ZIP tests. |
| 6. Dependency Auditor | Track exact package/runtime constraints. | cryptography 46.0.7 vs 46.0.4 blocked stable release. |
| 7. Security Reviewer | Minimize tool/MCP privilege. | Memory/MCP/plugin convenience must not outrank secret isolation. |
| 8. Privacy Reviewer | Limit transcript and credential exposure. | Event logs need redaction and least-privilege access. |
| 9. Reproducibility Engineer | Demand deterministic reruns. | Hashes, commit pins, fixtures and clean runners are essential. |
| 10. CI Specialist | Make completion machine-checkable. | Final verdict should depend on tests/status, not prose. |
| 11. Red-Team Hallucination | Find fake-complete statements. | Files created ≠ installed/deployed/verified. |
| 12. Root-Cause Engineer | Unify symptom chains. | Repair common mechanism behind A/B/C errors. |
| 13. Agent-Orchestration Architect | Design bounded multi-agent loops. | Roles need separate evidence and terminal criteria. |
| 14. Diversity Auditor | Detect fake multi-agent diversity. | Different names alone do not count as 30 independent strategies. |
| 15. Observability Engineer | Require progress/decision/evidence logs. | A stalled agent must be diagnosable. |
| 16. Recovery Engineer | Design rollback/replan paths. | Failure must transition explicitly, not silently continue. |
| 17. Human-Factors Reviewer | Prevent overload for beginners. | Production defaults should be stable; experiments isolated. |
| 18. Prompt Engineer | Version prompts like code. | Prompt registry + eval set + rollback beats ad-hoc prompt accumulation. |
| 19. Memory Architect | Keep memory useful but subordinate. | Mem0/Graphiti should not override repo/tests. |
| 20. MCP Architect | Separate transport from authority. | A relay does not imply unrestricted local or account access. |
| 21. GitHub Architect | Use repository as source of truth. | Task contracts, commits, diffs, CI and protections anchor history. |
| 22. Legal-AI Reviewer | Block unsupported capability claims. | U.S. Counsel artifacts were not lawyer-validated or fully deployed. |
| 23. Multimedia-AI Reviewer | Catalog domain skillpacks accurately. | Animation/voice systems should be kept distinct from core agent runtime. |
| 24. Evaluation Scientist | Distinguish local metrics from real utility. | Retrieval scores do not prove end-user model behavior. |
| 25. Release Manager | Require gates before stable labels. | RC/local pass cannot become stable while blockers remain. |
| 26. Data-Provenance Reviewer | Track where each statement came from. | This package is cross-chat summary recovery, not raw transcript export. |
| 27. Deduplication Reviewer | Collapse repeated versions/claims. | Preserve meaningful deltas instead of repeating near-identical entries. |
| 28. Contradiction Resolver | Surface conflicting claims. | Newer status corrections outrank older optimistic completion language. |
| 29. Research Librarian | Build navigable taxonomy. | Separate core governance, agents, prompt/memory, MCP, domains. |
| 30. Executive Integrator | Optimize for durable future use. | A smaller evidence-labeled vault is better than a huge unverifiable dump. |

## Consensus
1. Preserve evidence level per claim.
2. Do not turn old chat statements into current 2026 installation instructions without re-verification.
3. Do not call a file/package “deployed” unless account/runtime evidence exists.
4. Keep Windows/macOS/runtime/product-surface compatibility explicit.
5. Prefer repository evidence and reproducible tests over memory.
6. Treat agent diversity as methodological diversity, not role-count theater.
7. Dedicated-repository creation remains incomplete until the dedicated repository actually exists; staging on an isolated branch is evidence-preserving but not equivalent.
