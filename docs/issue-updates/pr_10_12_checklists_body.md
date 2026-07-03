## Summary

- Adds MVP review checklist for pedagogy, copyright/source risk, accessibility, data/versioning, and teacher-guide review.
- Adds MVP release checklist for v0.1 public preview readiness.
- Preserves human review gates and non-official textbook status.

## Related Issues

- Related/follow-up: #10
- Closes #12
- follows #9 / PR #20

## Validation

- [x] `python scripts/validate_ndjson.py` passed: 16 records checked
- [x] `python scripts/build_sqlite_index.py` passed: 16 records / 21 edges / FTS5=True
- [x] `git diff --check` passed
- [x] `python3 scripts/validate_ndjson.py` failed with Windows launcher output: `Python`
- [x] `python3 scripts/build_sqlite_index.py` failed with Windows launcher output: `Python`

## Scope Notes

This PR does not create lesson content, teacher guide bodies, full problem banks, NDJSON records, schema fields, or published/approved statuses.

## Open Maintainer Decisions

- Whether teacher guides are included in v0.1 public preview or treated as beta support material.
- Whether explicit teacher-guide reference fields should be added later.
- Whether timing guidance should include 45/50-minute examples.
- Whether pedagogy review is mandatory before teacher-guide body drafting.
