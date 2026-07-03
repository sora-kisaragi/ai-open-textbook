Closed by PR #20.

This issue defined teacher guide requirements for the three MVP lessons.

The work intentionally did not:
- create full teacher guide content
- change NDJSON lesson records
- add schema fields
- modify validators
- mark teacher guides as approved or published

The teacher guide is defined as supplemental support material, not official guidance.

Remaining maintainer decisions:
- whether teacher guides are included in v0.1 public preview or treated as beta support material
- whether lesson records should later add an explicit teacher guide reference field
- whether timing guidance should remain flexible or include 45/50-minute examples
- whether a pedagogy-reviewer pass is required before drafting full teacher guide bodies

Validation evidence:
- `python scripts/validate_ndjson.py`: passed
- `python scripts/build_sqlite_index.py`: passed
- `git diff --check`: passed
