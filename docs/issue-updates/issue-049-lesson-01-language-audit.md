# Issue 49 Lesson 01 Language Audit

## Summary

PR #50 merged the language policy for the Japanese High School Information I
MVP. Lesson 01 and its related records still contain English learner-facing and
teacher-facing educational content. This audit identifies the fields and
sections that need Japanese localization in a later PR.

This audit does not translate content, approve content, publish content, close
Issue #49, merge PR #48, or count Lesson 01 seed problems toward the final
problem-bank target.
Issue #49 was already closed after the language policy work; this audit records
follow-up evidence and handoff details, and does not reopen or re-close the
issue.

## Policy basis

- `AGENTS.md` keeps repository documents, prompts, issues, PR text, comments,
  code, schemas, data fields, and internal metadata in concise English.
- `docs/STYLE_GUIDE.md` now classifies learner-facing and teacher-facing
  educational content for the Japanese High School Information I MVP as
  Japanese.
- `docs/DATA_MODEL.md` now classifies display metadata and instructional
  content as Japanese when the record `locale` is `ja`, while schema keys,
  stable IDs, review metadata, source metadata, commands, file paths, code
  literals, and output literals remain English or machine-readable.

## Files inspected

- `lessons/highschool_information_i/programming/01_variables.md`
- `teacher_guides/highschool_information_i/programming/01_variables.md`
- `data/collections/lessons.ndjson`
- `data/collections/problems.ndjson`
- `data/collections/answers.ndjson`
- `data/collections/rubrics.ndjson`
- `data/collections/revisions.ndjson`
- `data/collections/sources.ndjson`
- GitHub Issue #49
- Merged PR #50 diff
- Open draft PR #48 discussion and diff

## Already compliant

### Markdown lesson file

- Code blocks are code literals and may remain unchanged unless a later task
  intentionally changes the executable example.
- Variable names such as `score`, `x`, `total`, and `name` are code or example
  identifiers and may remain unchanged.
- Numeric values, string literals, operators, and literal output values such as
  `80`, `3`, `2`, `5`, `"Aki"`, `=`, and `==` may remain unchanged.

### Teacher guide

- Code examples and code literals such as `score = 80` and
  `score = score + 10` may remain unchanged.
- Variable names and output literals used as code examples may remain unchanged.

### NDJSON records

- Stable IDs, schema keys, record `type`, `schema_version`, `status`,
  `review_status`, `verification_status`, `change_type`, `actor`, timestamps,
  references, file paths, and enum values are internal or machine-readable and
  must remain English or machine-readable.
- `sources.ndjson` uses source metadata. The inspected source title, URL,
  source type, access date, and review note do not need localization unless a
  future learner-facing display field is added.
- Existing statuses remain `human_review_requested` for Lesson 01 educational
  records and `draft` for revision/source records. No record is approved or
  published by this audit.

## Requires Japanese localization

### Markdown lesson file

- Headings: H1 and section headings are learner-facing.
- Learning objectives: the numbered goals under `Learning goals` are
  learner-facing.
- Prerequisites: the prerequisite bullets are learner-facing context.
- Explanatory prose: the introduction and explanation sentences are
  learner-facing.
- Worked examples: prose around code examples is learner-facing.
- Common mistakes: mistake headings and explanatory prose are learner-facing.
- Self-check: questions are learner-facing.
- Code comments, if added later and surfaced to learners, should be Japanese.

### Teacher guide

- Headings are teacher-facing educational content.
- Lesson intent, suggested flow, suggested questions, timing guidance,
  expected misconceptions, and formative assessment guidance are
  teacher-facing instructional prose and should be Japanese.
- Any future teacher-facing assessment guidance should also be Japanese.

### `lessons.ndjson`

- `locale`: update from `en` to `ja` when the educational content in the
  lesson record and referenced body is localized.
- `title`: display metadata; localize.
- `subject`: display metadata; localize if surfaced to learners or teachers.
- `unit`: display metadata; localize if surfaced to learners or teachers.
- `learning_objectives`: learner-facing; localize.
- `prerequisites`: learner-facing if populated later; localize any displayed
  prose.

### `problems.ndjson`

- `question`: learner-facing prompt; localize the prose while preserving code
  blocks and literal output.
- `common_mistakes`: learner- or teacher-facing instructional content; localize
  the prose while preserving code literals such as `==`, `=`, `80`, and
  `score`.
- `subject` and `unit`: display metadata; localize if surfaced to learners or
  teachers.

### `answers.ndjson`

- `explanation`: learner-facing feedback; localize.
- `canonical_answer`: keep unchanged when it is code or exact output, such as
  `score = 80` or `5`; localize only if a canonical answer is prose.
- `acceptable_answers`: keep code or exact-output variants unchanged; localize
  prose accepted-answer variants if they remain part of the record.

### `rubrics.ndjson`

- Rubric criteria prose such as `criteria[].description` is teacher-facing
  instructional scoring guidance; localize.
- Scoring labels, if added later and surfaced to teachers or learners, should
  be Japanese unless they are machine-readable enum values.

## Must remain English or unchanged

- File paths, GitHub text, scripts, commands, schema keys, record IDs, stable
  references, source IDs, and status or review enum values.
- `id`, `type`, `schema_version`, `status`, `review_status`,
  `verification_status`, `change_type`, `actor`, `created_at`, `updated_at`,
  `valid_from`, `valid_to`, `supersedes`, `superseded_by`, `body_ref`,
  `lesson_refs`, `answer_refs`, `rubric_refs`, `source_refs`, `problem_id`,
  `difficulty`, `question_type`, `answer_type`, criterion IDs, and point
  values.
- Code examples, variable names, operators, string literals, command/file
  literals, and canonical output values unless a later educational task
  intentionally changes the example itself.
- Source metadata in `sources.ndjson`, including official titles and review
  notes, unless a reviewed learner-facing display field is added later.

## Required revision-record handling

- The later localization PR will make non-trivial learner-facing and
  teacher-facing educational content changes, so it must append revision
  records in `data/collections/revisions.ndjson`.
- Existing `change_type` value `update` is sufficient for localization edits
  to existing draft records. A new `change_type` value is not needed unless
  maintainers want finer reporting semantics.
- Revision `reason` values should stay concise English public summaries, for
  example: `Localized Lesson 01 learner-facing prose to Japanese without
  changing code literals or approval status.`
- The later localization PR should not silently overwrite history and should
  not mark any record as `approved` or `published`.

## Required `locale` handling

- Keep `locale: "en"` until the associated educational content is actually
  localized.
- In the localization PR, update `locale` to `ja` for the Lesson 01 lesson
  record when the referenced lesson body and display fields are Japanese.
- If future problem, answer, or rubric schemas add `locale`, set it consistently
  with the localized educational content. The current inspected problem,
  answer, and rubric records do not include `locale`.
- Do not use `locale` to describe repository management language or GitHub
  operational text.

## Open questions

- Should `subject` and `unit` be localized in every problem record now, or only
  after the project confirms those fields are displayed directly to learners or
  teachers?
- Should future schemas add explicit `locale` fields to problem, answer, and
  rubric records for clearer multilingual handling?
- Should PR #48 be merged before localization so its exact-output and
  `verification_evidence` changes are included in the localization edit base?

## Recommended follow-up Issue

Created one combined follow-up Issue:

`Localize Lesson 01 learner-facing and teacher-facing content to Japanese`

- GitHub Issue: #51

The Issue should cover:

- Lesson 01 Markdown learner-facing prose.
- Lesson 01 teacher-guide instructional prose.
- Lesson 01 lesson display metadata and learning objectives.
- Lesson 01 related problem prompts and common mistakes.
- Lesson 01 related answer explanations and prose accepted-answer variants.
- Lesson 01 related rubric criteria prose.
- Required revision records and `locale` handling.

One combined Issue is cleaner than splitting the work now because the same
language policy, revision handling, and human review gate apply across the
Lesson 01 vertical slice.

## PR #48 note

PR #48 can be reviewed independently for its #44/#45 technical scope. Its
`verification_evidence`, exact-output handling, canonical outputs, schema keys,
record IDs, and revision metadata are internal or machine-readable and do not
need Japanese localization. The learner-facing answer explanations and
teacher-facing rubric criteria touched by PR #48 still need localization in a
later localization PR if PR #48 is merged.
