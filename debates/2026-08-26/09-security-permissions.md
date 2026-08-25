# Debate 09 — Security / Permissions

## Position
A useful ordinary-chat agent needs broader *authorized reach*, not a deliberate sandbox escape. Capability should expand through explicit bridges, scoped credentials, and auditable mutations.

## Adopt
1. Workspace-root allowlists for local file operations and agent runs.
2. Host/origin/domain allowlists for MCP/browser interfaces.
3. Secrets only in environment/keychain/secret stores; never prompts, receipts, logs, or Git.
4. Separate read, write, destructive, and open-world actions with accurate annotations and confirmation boundaries.
5. Prompt-injection and untrusted-content boundaries for browser/web/email/documents.
6. Fail closed if device, auth, attestation, receipt, or freshness checks fail.
7. Log the capability route selected and the mutation outcome without logging secret values.

## Reject
- Disabling OS/browser/security controls to make an agent feel 'unrestricted'.
- Raw unrestricted shell/filesystem/browser-JS as default ordinary-chat tools.
- Auto-approving destructive changes globally.
- Installing arbitrary MCP registry servers because they are free or popular.

## Acceptance
PASS when the system can perform legitimate local work inside explicit scopes, mutations are attributable and reversible where practical, secret-leak tests pass, and a compromised webpage/tool response cannot silently escalate privileges.
