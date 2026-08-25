# 04 — Memory and continuity

## Verdict
Do not replace ChatGPT/persistent connected memory with a new memory framework by default. Add a memory router: native/connected memory first, GitHub checkpoint state for engineering continuity, Mem0 OSS only when an external agent runtime needs searchable long-term memory.

## Evidence
- Mem0's April 2026 algorithm adds entity linking, hybrid semantic/BM25/entity retrieval and temporal reasoning; its OSS stack is configurable and its skills are portable across Codex/Claude/Cursor/OpenCode.
- Mem0 documentation now supports expiration dates, which is important because local deployments otherwise accumulate stale memories and retrieval noise.
- Letta offers strong long-lived agents and self-modifying memory, but a June 2026 issue documents per-agent memory isolation across new agents/sessions; it is not the safest default continuity bus.

## Gap in current stack
The repository has GitHub continuity and chat memory assumptions but no memory-class router separating preferences, task checkpoints, procedural lessons, temporary state, and expiring facts.

## Recommendation
Create `memory-continuity-routing`; use: native ChatGPT/connected memory for user preferences, GitHub evidence/checkpoints for project state, Mem0 OSS for external agent semantic/temporal retrieval. Require expiration/lifecycle metadata for temporary facts.

## Acceptance
A fresh session must recover the current project checkpoint without copying the entire prior conversation, while an expired temporary fact must not be surfaced as current state.