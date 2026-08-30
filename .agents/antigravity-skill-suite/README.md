# Antigravity Skill Suite v1

Status: `PACKAGED / TARGET-RUNTIME VERIFICATION PENDING`

This suite is a purpose-built Antigravity IDE projection of the connected GPT/agent skill estate. It audits 66 formal `SKILL.md` source instances across `ai-thinking-debate-skills-lab`, `chatgpt-mcp-codex`, `braintrust`, and `cursor`, and converges overlapping semantics into 33 canonical Antigravity skills.

## Design rules

1. **No blind copying.** Portable procedural semantics are retained; ChatGPT/Codex/Cursor-specific transport, memory, connector, approval, sandbox and product assumptions are rewritten.
2. **One semantic owner.** Duplicate skills are merged to avoid trigger collisions and context bloat.
3. **Antigravity-native packaging.** Deployable procedures live at `.agents/skills/<name>/SKILL.md`; persistent project-wide constraints live in `.agents/AGENTS.md`.
4. **MCP stays separate.** MCP server registration/auth/schema is a host adapter concern, not embedded into reusable skill logic.
5. **Evidence-gated completion.** `PACKAGED != HOST_LIVE`; static repository validation cannot prove the local Antigravity IDE loaded or exercised the exact revision.
6. **No capability downgrade.** Porting must preserve the source skill's useful outcome. A GPT-only mechanism is replaced by an equivalent Antigravity mechanism where available, not silently deleted.

## Canonical skills

The suite contains 33 owners covering: goal orchestration, planning, evidence, research, memory/state, convergence, autonomy, durable work state, capability routing/forensics, MCP, runtime forensics, reverse engineering, compatibility, hypotheses/root cause, multi-agent deliberation, legal research/writing, provider/runtime scaling and health, GitHub, source routing/benchmarks, writing cognition, web recovery, workspace execution and resilient tool acquisition.

See `source-inventory.json` for the 66→33 mapping.

## Release gates

A repository release is acceptable only when:
- every canonical skill has valid `name` + `description` frontmatter;
- directory and frontmatter names match and are unique;
- every skill declares activation, hard-negative, workflow, validation and boundary semantics;
- source inventory counts exactly 66 source instances and 33 canonical targets;
- every mapped target directory exists;
- prohibited host assumptions do not leak into canonical skills except where explicitly discussed as a bridge/boundary;
- the validation script passes in CI.

Target-runtime release remains pending until the local Antigravity IDE reads back discovery/load/invocation of this exact revision.