# ChatGPT Web/Desktop live probe

Purpose: prove the exact imported plugin revision is actually discoverable and routes correctly on the owning ChatGPT surface. Repository/package validation is insufficient.

## Install/import boundary

Current OpenAI guidance supports plugin use in ChatGPT web and desktop and supports workspace marketplace import from GitHub. The repository provides `.agents/plugins/marketplace.json` for that path.

Actual availability still depends on workspace permissions, plan, surface and import/install state. Do not convert a GitHub commit into a `HOST_LIVE` claim.

## Probe order

1. Import/sync the repository marketplace through the actual workspace/admin plugin control available to the target account.
2. Confirm `AI Efficiency Operating System` is listed and installable.
3. Confirm the plugin reports the expected `1.1.0-rc1` package/revision if the UI exposes it.
4. Run a small positive/negative routing set before enabling the full workflow:
   - plan comparison containing the word `verify` → planning behavior;
   - completion claim such as "agent says migration completed" → postcondition verification;
   - current technical research → research behavior;
   - simple arithmetic/translation → no heavy research ceremony;
   - autonomy and persistent ledger do not appear implicitly.
5. Test a research-integrity case: a load-bearing claim must not be released merely because a citation link exists; the source/content must support the claim.
6. Test a validation-boundary case: repository/static PASS must not be described as ChatGPT behavioral PASS.
7. Test a real state claim with an owning-runtime/read-back proof path.

## Acceptance layers

- repository/schema CI establishes only the layers it actually exercised;
- marketplace/import observation can establish installed-template presence;
- invoking/routing the exact plugin on the target host can establish executable behavior in that scope;
- `CHATGPT_DESKTOP_HOST_LIVE` requires observed plugin availability plus at least one owning-surface behavioral postcondition.

`CHATGPT_ROUTING_VERIFIED` additionally requires positive and hard-negative routing cases without a material collision.

If the UI/workspace does not expose import/install for this repository, report `HOST_IMPORT_BLOCKED`; do not rewrite the skill package to pretend that product capability exists.
