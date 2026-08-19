# Prompt, Memory and Skill Infrastructure

## Capability Hub

### v0.2.0
- SHA-256: `11509a1bc634e252519b938ba2ebf53dba38828a5b64bbf8f1b050b3a5dddfeb`
- 25/25 reported tests
- 20 eval cases
- 62 manifest files
- 4 skills
- 6 locked sources
- No HTTPS deployment, API-account access, or paid E2E test.

### v0.3.0
- SHA-256: `e8a077af99406890a4cd4ff85d257c3b4b83e1f5ea366bf453ba3108aa2816bc`
- 41/41 reported tests
- 40 eval cases
- 10/10 skills validated
- 28 source records
- 24 commit pins

## Universal Context Intelligence Skill v1.0.1
Reported:
- ZIP/wheel/docs/artifacts created,
- 21/21 Python tests,
- API/SQLite/CLI/install/parse/integrity checks.

Not verified:
- Docker,
- Raycast,
- real MCP runtime,
- real LLM providers,
- Qdrant/Graphiti/Neo4j adapters,
- LongMemEval/LoCoMo,
- human clinical/cultural review.

## Memory policy
Mem0 and Graphiti were treated as useful but **non-authoritative** memory layers.

Authoritative order for engineering work:
1. repository state,
2. task contract,
3. commit/diff,
4. raw tests,
5. CI evidence,
6. structured logs,
7. memory and chat summaries.

## Prompt engineering / management research themes
- prompt versioning,
- eval datasets,
- before/after scoring,
- failure-case storage,
- source pinning,
- semantic diff,
- rollback,
- prompt registry,
- automated evaluation before promotion.

## Named systems retained in archive
- Braintrust prompt/eval setup research,
- Agent Skills Governance v0.3.0,
- Deep Thinking v3.0.0-rc1,
- Multi-Agent Deliberation OS through v10.1.0.

Detailed payloads for every named version were not fully recoverable in this pass; preserve the names without inventing missing contents.
