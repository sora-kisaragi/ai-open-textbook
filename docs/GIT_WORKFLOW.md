# Git Workflow

This project uses **GitHub Flow**.
`main` is always releasable. All changes go through pull requests.

## Branching model

- `main` is the only long-lived branch.
- Never push directly to `main`. Every change goes through a pull request.
- Create a short-lived branch from the latest `main` for each issue.
- Delete the branch after the pull request is merged.

## Branch naming

```text
<type>/<issue-number>-<short-description>
```

| Type | Use for |
| --- | --- |
| `feature` | New lessons, exercises, teacher guides, or tooling |
| `fix` | Corrections to content, data, or scripts |
| `docs` | Documentation and policy changes |
| `data` | NDJSON schema or data-only changes |
| `chore` | Maintenance, CI, and configuration |

Examples:

```text
feature/12-variables-lesson
fix/34-rubric-answer-mismatch
docs/40-git-workflow
```

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <summary>
```

- Types: `feat`, `fix`, `docs`, `data`, `refactor`, `test`, `chore`.
- Scope is optional. Use the unit or area, such as `programming` or `schema`.
- Write the summary in English, imperative mood, under 72 characters.

Examples:

```text
feat(programming): add variables lesson draft
data(schema): add supersession field to answer records
docs: define git workflow
```

## Pull requests

- One PR changes one coherent unit (Operating Rule 10).
- Link the issue the PR resolves.
- Fill in the pull request template completely.
- Run machine validation before requesting human review (Operating Rule 7).
- A PR needs at least one human approval before merge (Operating Rule 3).
- Keep the branch up to date with `main` before merge.

## Merge strategy

- Use **squash merge** only.
- The squash commit message must follow Conventional Commits.
- Delete the source branch after merge.

## Releases

- Tag releases on `main` as `vMAJOR.MINOR.PATCH` (semantic versioning).
- Update `CHANGELOG.md` in the release pull request before tagging.
- Follow `docs/RELEASE_POLICY.md` for release requirements.

## Quick reference

```bash
git switch main
git pull origin main
git switch -c feature/12-variables-lesson
# ... edit, then commit
git commit -m "feat(programming): add variables lesson draft"
git push -u origin feature/12-variables-lesson
# open a PR, get review, squash merge, delete branch
```
