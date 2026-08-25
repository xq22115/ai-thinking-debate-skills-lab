# 02 — Browser control

## Verdict
Use Playwright CLI + SKILL as the deterministic/default coding-agent route; use browser-use only when the task specifically requires the user's real signed-in Chrome/profile. Keep Playwright MCP optional rather than always loaded.

## Evidence
- Microsoft now explicitly recommends CLI + SKILL for coding agents when context efficiency matters; Playwright MCP remains valuable for structured accessibility snapshots and persistent browser sessions.
- browser-use supports `--profile Default` and `--connect` to a running Chrome with existing logins/cookies, but August 2026 issues show long-session tab accumulation and stale input-session regressions.
- Accessibility snapshots can carry indirect prompt injection; browser content must remain untrusted evidence.

## Gap in current stack
The catalog already says CLI before MCP, but there is no ordinary-chat skill that chooses among native browser, Playwright CLI, Playwright MCP, browser-use real-profile mode, and connector/browser-app routes based on login/state needs.

## Recommendation
Create `browser-control-routing` with explicit route matrix: deterministic test → Playwright CLI; persistent isolated state → Playwright MCP; existing logged-in Chrome → browser-use/authorized browser connector; native-app/browser hybrid → Cua Driver.

## Acceptance
The router must state which browser/session it is controlling, prove page identity after navigation, and read back the resulting state after every consequential interaction.