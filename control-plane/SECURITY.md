# Security Policy

## Reporting a vulnerability

Do not disclose credentials, tokens, private keys, cookies, private data, or exploitable details in public issues, pull requests, commit messages, workflow logs, or screenshots.

For this private repository, report suspected security problems directly to the repository owner or organization administrators through an authenticated private GitHub channel or another trusted private channel.

Include, when safe:

- affected revision or component;
- reproducible steps;
- expected vs. observed behavior;
- impact and scope;
- suggested mitigation if known.

## Agent and automation safety

AI agents and automation must use least privilege, prefer read-only verification before mutation, avoid committing secrets, and preserve an auditable rollback path for material configuration changes.

Security-sensitive changes should use the normal branch/pull-request workflow. Rotate any credential immediately if exposure is suspected.
