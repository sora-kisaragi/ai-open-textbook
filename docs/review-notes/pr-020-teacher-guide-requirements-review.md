# PR #20 Review Note: Teacher Guide Requirements

## Summary

PR #20 adds `docs/requirements/teacher-guide-requirements.md` for Issue #9.
The change is requirements-only and covers future teacher guides for the MVP
programming lessons: variables and assignment, conditionals, and loops.

Review result: no content blocker found for the requirements document. Merge
was not performed because the PR is still a draft and has no human approval.

## Acceptance Criteria Check

- Lesson flow is required: present in common requirements and each lesson
  section.
- Suggested teacher questions are required: present in common requirements and
  each lesson section.
- Timing is required: present as flexible timing guidance and lesson-specific
  timing considerations.
- Assessment points are required: present in common requirements and each
  lesson section.
- Student misconceptions are linked to feedback strategies: present in common
  requirements and lesson-specific feedback strategy requirements.
- Teacher guide remains supplemental, not official guidance: explicitly stated
  in the opening note, purpose, and public preview boundary.
- Human review gates are listed: pedagogy, copyright/source, accessibility,
  data/schema, and release-scope review needs are identified.

## Scope Check

- No official textbook claim found.
- No final curriculum alignment claim found.
- No invented citation found.
- No full teacher guide body generation found.
- No lesson body, problem-bank, answer, or rubric generation found.
- No NDJSON, schema, validator, or generated SQLite changes are part of the PR
  diff.
- No unexpected generated artifact is committed in the PR diff.
- No conflict found with `AGENTS.md` or `docs/OPERATING_RULES.md`.

## Validation Evidence

- `python scripts/validate_ndjson.py`: passed, 16 records checked.
- `python scripts/build_sqlite_index.py`: passed, 16 records and 21 edges,
  FTS5=True.
- `git diff --check`: passed.
- `python3 scripts/validate_ndjson.py`: failed with Windows launcher output
  `Python`.
- `python3 scripts/build_sqlite_index.py`: failed with Windows launcher output
  `Python`.

The `python3` failures match the documented Windows launcher limitation and do
not indicate a repository defect.

## Open Maintainer Decisions

- Whether teacher guides are included in v0.1 public preview or treated as beta
  support material.
- Whether lesson records should later add `teacher_guide_ref` or
  `teacher_guide_refs`.
- Whether timing guidance should remain flexible or include 45/50-minute
  examples.
- Whether a `pedagogy-reviewer` pass is required before full teacher-guide
  body drafting.

## Recommendation

PR #20 can proceed after maintainers mark it ready for review and complete the
required human approval step. Use squash merge and delete the source branch
after merge, following `docs/GIT_WORKFLOW.md`.
