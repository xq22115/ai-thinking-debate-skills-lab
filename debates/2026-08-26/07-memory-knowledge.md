# Debate 07 — Memory / Knowledge

## Position
Add local-first, provenance-aware project memory; do not inject an unlimited global memory stream into every conversation.

## Adopt
1. Start with a small durable store (SQLite + FTS; optional embeddings only when semantic recall materially helps).
2. Store source/provenance, timestamp, workspace/project scope, retention class, and confidence with each memory item.
3. Separate ephemeral run state, durable project facts, and user-approved long-term preferences.
4. Expose narrow search/fetch tools; never dump the whole store into context.
5. Make retention/deletion and stale-memory invalidation explicit.
6. Evaluate third-party MCP memory servers only after code, license, auth, data-location, and deletion behavior are vetted.

## Reject
- Automatically saving every prompt/tool result forever.
- Treating model-generated conclusions as facts without provenance.
- Sending local project memory to random hosted 'free' memory services.
- A single cross-project namespace with no isolation.

## Acceptance
PASS when memory improves recall in an evaluation set, stale facts can be invalidated, data can be scoped/deleted, and retrieval returns provenance rather than unsupported assertions.
