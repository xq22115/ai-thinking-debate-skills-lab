# Contributing

## Change workflow

1. Create a focused branch from `main`.
2. Keep the diff scoped to one clear goal.
3. Run the relevant checks locally when available.
4. Open a pull request using the repository template.
5. Address failing checks and review feedback without weakening the acceptance criteria.
6. Merge only after the exact revision has the required evidence.

## Quality expectations

- Preserve existing behavior unless the change intentionally modifies it.
- Prefer root-cause fixes and small reversible changes.
- Add or update tests/checks when the changed behavior is testable.
- Do not commit secrets, credentials, tokens, private keys, generated caches, or unrelated files.
- AI-assisted changes remain subject to the same verification and review requirements as human-authored changes.
