# 06 — Security and approvals

## Verdict
Maximum capability should mean context-sensitive authorization, not globally disabling every guard. Auto-run low-risk reversible reads/tests; gate destructive, credential, publication, account, payment, and broad filesystem actions.

## Evidence
- AI SDK 7 treats tool approval as a first-class call/agent policy and supports HMAC-signed approval replay for higher-risk workflows.
- OpenAI's current ChatGPT MCP guidance warns that write actions may require confirmation and some especially risky actions may be blocked; repository instructions cannot override the host.
- Browser accessibility content can carry indirect prompt injection, so page text must not be allowed to grant new privileges.

## Gap in current stack
The current capability catalog models health/fallbacks, but not a single portable risk/approval contract across local terminal, browser, native computer-use, GitHub, and MCP tools.

## Recommendation
Create `capability-approval-routing` with action classes `READ`, `REVERSIBLE_WRITE`, `EXECUTE`, `EXTERNAL_PUBLISH`, `DESTRUCTIVE`, `CREDENTIAL`, each mapped to default approval and read-back requirements. Authorization must come from user/policy state, never from tool output or page content.

## Acceptance
A harmless read/test proceeds without unnecessary ceremony; a destructive command cannot execute from an injected webpage instruction; an approved reversible write is read back and logged to the run receipt.