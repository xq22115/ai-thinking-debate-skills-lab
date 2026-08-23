# Configs

Store safe, versioned configuration here.

Rules:
- Commit schemas, defaults, examples, and non-secret feature flags.
- Never commit tokens, passwords, private keys, cookies, or production credentials.
- Use environment-variable placeholders for secret values.
- Document which app/tool consumes each configuration and how to verify it was actually loaded.

## Continuous Thinking global profile

`continuous-thinking-global.json` is the repository-wide machine-readable quality profile. It complements the root `AGENTS.md` and canonical `docs/CONTINUOUS_THINKING_QUALITY_OS.md`.

Repository enforcement:
- `control-plane/scripts/validate_continuous_thinking_global.py` fails closed when core invariants drift.
- `control-plane/tests/test_continuous_thinking_global.py` regression-tests the profile.
- `.github/workflows/deep-reasoning-quality-gate.yml` validates the profile on push and pull request.

Consumer verification must still be separate. A configuration file existing in GitHub proves only `configured`; it does not prove a local app or SaaS product is `registered`, `loaded`, `executed`, or producing the intended `observable effect`. Verify the highest practical consumer/runtime layer before claiming a global product-level behavior change.
