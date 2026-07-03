# Merge PR #20 Instructions

PR #20 was reviewed locally and no requirements-content blocker was found.
Merge was not performed because the PR is still a draft and has no human
approval.

Maintainer steps after review approval:

```bash
gh pr ready 20
gh pr merge 20 --squash --delete-branch
```

Recommended squash commit message:

```text
docs: define teacher guide requirements
```

Validation evidence from local review:

- `python scripts/validate_ndjson.py`: passed
- `python scripts/build_sqlite_index.py`: passed
- `git diff --check`: passed
- `python3 scripts/validate_ndjson.py`: failed with Windows launcher output `Python`
- `python3 scripts/build_sqlite_index.py`: failed with Windows launcher output `Python`
