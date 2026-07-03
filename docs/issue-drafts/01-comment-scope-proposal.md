# Comment draft for Issue #1 (post with gh when available)

Post via:

```bash
gh issue comment 1 --body-file docs/issue-drafts/01-comment-scope-proposal.md
```

(Remove this header block before posting, or post from the marker below.)

---

MVP scope proposal drafted in `docs/MVP_SCOPE.md` (status: draft, needs human review).

Summary:

- v0.1 covers exactly three lessons: variables and assignment, conditionals, loops.
- Positioned as open educational material; no official textbook or final alignment claims.
- Release boundary defined: draft -> review candidate -> public preview, mapped to `AGENTS.md` status values.
- Human review gates listed (alignment, pedagogy, copyright, accessibility, publish).
- Dependency order proposed for Issues #2–#12 (#2/#3 parallel, lessons sequential, #12 last).
- Risk table added: pedagogy, copyright, accessibility, data model, validation.

Checklist to close this issue:

- [ ] Maintainer reviews and accepts `docs/MVP_SCOPE.md`.
- [ ] Lesson set confirmed as exactly the three MVP lessons.
- [ ] Out-of-scope list confirmed or amended.
- [ ] Release boundary stages accepted.
- [ ] Review gates confirmed against `AGENTS.md`.
- [ ] Dependency order for #2–#12 accepted.

Open questions: problem counts per lesson (#7), pseudocode vs. concrete language, whether teacher guides ship in v0.1 preview.

Validation: `validate_ndjson.py` passed (10 records). Index build verified on a repo copy.
