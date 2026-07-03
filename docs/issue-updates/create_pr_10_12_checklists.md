# Create PR for Issue #10 and Issue #12 Checklists

Use after PR #20 has been merged and `main` is up to date.

```bash
git checkout main
git pull --ff-only
git checkout -b docs/10-12-review-release-checklists
git add docs/review/MVP_REVIEW_CHECKLIST.md docs/release/MVP_RELEASE_CHECKLIST.md docs/review-notes/pr-020-teacher-guide-requirements-review.md docs/issue-updates/
git commit -m "docs: add MVP review and release checklists"
git push -u origin docs/10-12-review-release-checklists
gh pr create --draft --title "[codex] Add MVP review and release checklists" --body-file docs/issue-updates/pr_10_12_checklists_body.md
```

Do not run the issue comment scripts until the branch has been pushed or the
draft PR has been created.
