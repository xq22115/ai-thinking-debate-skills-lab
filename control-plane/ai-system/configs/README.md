# Configs

Store safe, versioned configuration here.

Rules:
- Commit schemas, defaults, examples, and non-secret feature flags.
- Never commit tokens, passwords, private keys, cookies, or production credentials.
- Use environment-variable placeholders for secret values.
- Document which app/tool consumes each configuration and how to verify it was actually loaded.

A configuration file existing in GitHub does not prove a local app or SaaS product has applied it; verification must occur at the consumer.
