# MCP Boundary for Antigravity Skill Suite

Skills and MCP are intentionally separate layers.

- `.agents/skills/<name>/SKILL.md` owns reusable procedural semantics.
- `.agents/AGENTS.md` owns persistent project-wide behavioral invariants.
- Antigravity's supported MCP configuration owns server registration, authentication, transport, namespaces and live tool schemas.
- Credentials/tokens never belong in this repository's skill text.

For the current 2026 Antigravity line, verify the installed build's MCP configuration contract before changing local config. Do not overwrite a user's entire MCP registry just to add one server.

MCP truth ladder:

`DECLARED -> REGISTERED -> AUTHORIZED -> LOADABLE -> INVOKABLE -> VERIFIED`

A server entry or tool listing is not runtime proof. Verify a harmless real invocation and the task-relevant postcondition. On schema/version drift, update the adapter/config rather than polluting portable skill logic with stale transport assumptions.