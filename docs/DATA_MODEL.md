# Data Model

## Decision

Use NDJSON as the source of truth.
Generate SQLite as an index.

## Why not SQLite as the only source?

SQLite is excellent for local querying, but the canonical educational data changes in ways that are easier to review as documents:

- Answers can be superseded.
- Rubrics can change.
- Explanations can be rewritten.
- Curriculum mappings can be updated.
- Review status is per item.
- Evidence can vary by item.
- Git diffs should remain readable.

## Collections

Canonical collections live in `data/collections/`:

- `lessons.ndjson`
- `problems.ndjson`
- `answers.ndjson`
- `rubrics.ndjson`
- `sources.ndjson`
- `revisions.ndjson`

The subject-wide planning graph lives in
`curriculum/highschool_information_i.curriculum.json`. It is validated as the
canonical curriculum record `curriculum.info1.v1` but remains separate from the
educational NDJSON collections.

## Core fields

Every record should include:

```json
{
  "id": "stable.dot.separated.id",
  "type": "record_type",
  "schema_version": "1.0",
  "status": "draft",
  "created_at": "2026-07-02",
  "updated_at": "2026-07-02"
}
```

Allowed `status` values are defined in `AGENTS.md`:

- `draft`
- `machine_checked`
- `human_review_requested`
- `approved`
- `published`
- `deprecated`
- `superseded`

## Field Language Policy

`locale` describes the language of the educational content for a record. It
does not describe the language used for repository management, GitHub Issues,
PRs, scripts, schemas, or internal review notes.

For the Japanese High School Information I MVP, display fields shown to
learners or teachers should be Japanese. Internal metadata, review metadata,
stable identifiers, schema keys, commands, code literals, and source tracking
metadata remain English or machine-readable literals.

For records whose `locale` is `ja`, display metadata that is directly shown to
learners or teachers should be Japanese in the record value. This includes
`subject`, `unit`, `title`, learning objectives, prompts, feedback, and
instructional rubric prose. Do not overload one field with both an internal
canonical label and a localized display label. If the project later needs both,
add explicit separate fields instead.

| Collection | Field or content | Classification | Language rule |
| --- | --- | --- | --- |
| All NDJSON collections | `id`, `type`, `schema_version`, field names | Stable machine-readable identifiers and schema fields | English or machine literals |
| All NDJSON collections | `status`, `review_status`, `verification_status`, `change_type`, `actor` | Review-facing metadata or lifecycle values | English enum values |
| All NDJSON collections | dates, revision numbers, references, file paths | Internal metadata | Machine-readable literals |
| `lessons.ndjson` | `locale` | Educational-content language metadata | Use the BCP 47 language tag for the educational content, such as `ja` for Japanese learner-facing content |
| `lessons.ndjson` | `title` | Display metadata | Japanese when shown to learners or teachers |
| `lessons.ndjson` | `subject`, `unit` | Display metadata | Translate in place for Japanese MVP records when shown to learners or teachers; keep internal planning docs in English |
| `lessons.ndjson` | `learning_objectives`, `prerequisites` | Learner-facing educational content | Japanese |
| `lessons.ndjson` | `body_ref`, `source_refs` | Stable references | Keep file paths and IDs unchanged |
| `problems.ndjson` | `question` | Learner-facing educational content | Japanese, except code blocks and literal output |
| `problems.ndjson` | `common_mistakes` | Learner- or teacher-facing instructional content by default | Japanese when attached to learner or teacher instructional records; English is acceptable only for explicitly documented internal-only review metadata |
| `problems.ndjson` | `difficulty`, `question_type`, `lesson_refs`, `objective_refs`, `answer_refs`, `rubric_refs` | Machine-readable metadata | English enum values or stable IDs |
| `answers.ndjson` | `canonical_answer` | Answer value | Keep exact code/output literals unchanged; use Japanese only when the canonical answer is prose |
| `answers.ndjson` | `acceptable_answers` | Answer values | Keep exact code/output variants unchanged; use Japanese for accepted prose variants |
| `answers.ndjson` | `explanation` | Learner-facing feedback | Japanese |
| `answers.ndjson` | `verification_evidence`, `source_refs`, `valid_from`, `valid_to`, `supersedes` | Review-facing or machine metadata | English or machine-readable literals |
| `rubrics.ndjson` | rubric criteria prose such as `criteria[].description` | Teacher-facing instructional content | Japanese when used for instruction or scoring guidance |
| `rubrics.ndjson` | criteria IDs, points, `problem_id` | Machine-readable rubric metadata | English or machine-readable literals |
| `sources.ndjson` | `title`, `source_type`, `url`, `accessed_at`, source IDs | Source metadata | Keep English or source-provided titles; do not translate official titles unless a reviewed display title field is added |
| `sources.ndjson` | `notes` | Review-facing metadata | English unless explicitly surfaced to learners or teachers |
| `revisions.ndjson` | `reason` | Review-facing metadata | English concise public summary |

Do not translate GitHub operational text, schema keys, commands, scripts,
record IDs, or internal developer-facing documentation as part of educational
localization work. Do not infer approval, publication, official textbook
status, or curriculum alignment from a language update.

Initial localization of draft records may be handled as an in-place edit while
the record is still draft, needs human review, and has not been published.
Non-trivial localization edits that change learner-facing or teacher-facing
educational content must append revision records in
`data/collections/revisions.ndjson`. Update `locale` to match the localized
educational content language. Reserve superseding records or parallel-locale
records for already published or stable records, or for a future multilingual
delivery requirement. Localized content still requires human review before it
can be approved or published.

## Required fields by collection

All records in `data/collections/*.ndjson` must include the core fields:
`id`, `type`, `schema_version`, `status`, `created_at`, and `updated_at`.

Additional required fields are:

| Collection | Type | Additional required fields |
| --- | --- | --- |
| `lessons.ndjson` | `lesson` | `title`, `body_ref`, `learning_objectives` |
| `problems.ndjson` | `problem` | `question`, `question_type`, `lesson_refs`, `objective_refs`, `answer_refs`, `rubric_refs` |
| `answers.ndjson` | `answer` | `problem_id`, `canonical_answer`, `answer_type`, `review_status`, `revision` |
| `rubrics.ndjson` | `rubric` | `problem_id`, `criteria` |
| `sources.ndjson` | `source` | `title`, `source_type`, `url` |
| `revisions.ndjson` | `revision` | `entity_id`, `change_type`, `reason`, `actor` |

## Identifier rules

Identifiers must be lowercase, dot-separated, and stable.
Records that represent versioned educational artifacts should end with a
version segment such as `.v1`.

Examples:

- `lesson.info1.programming.variables.v1`
- `prob.info1.variables.001.v1`
- `ans.prob.info1.variables.001.v1`
- `rubric.prob.info1.variables.001.v1`
- `src.mext.curriculum.general.v1`

Revision IDs are append-only event IDs and use the pattern
`rev.YYYYMMDD.NNNN`.

## Answer versioning

Answers are not treated as permanent truth.
They are versioned claims with review status.

Recommended fields:

```json
{
  "id": "ans.prob.example.001.v1",
  "problem_id": "prob.example.001.v1",
  "canonical_answer": "...",
  "valid_from": "2026-07-02",
  "valid_to": null,
  "review_status": "needs_human_review",
  "source_refs": [],
  "rubric_refs": [],
  "supersedes": null,
  "revision": 1
}
```

## Revision and supersession rules

- Every non-trivial content or data change must append a record to
  `data/collections/revisions.ndjson`.
- Every non-revision record should have at least one revision record whose
  `entity_id` matches the record `id`.
- The curriculum record also requires revision events even though its structured
  body is stored outside the NDJSON collections.
- `supersedes` points to the previous record version when a record replaces an
  earlier version.
- `superseded_by` points to the replacement record version when known.
- `supersedes` and `superseded_by` references must not point to the same record
  and must resolve to existing records when the target is in an NDJSON
  collection.
- Do not delete or silently overwrite old answers, rubrics, explanations, or
  sources. Add a new version and record the change.

## SQLite projection

`scripts/build_sqlite_index.py` creates:

- `build/index.sqlite`

Tables:

- `documents`: all NDJSON records as JSON text.
- `edges`: references between records.
- `curriculum_lessons`: the 32 planned lessons in curriculum order.
- `objectives`: stable objective IDs and learner-navigation labels.
- `coverage`: objective-level assessment evidence state.
- `doc_fts`: optional FTS5 search index when available.

SQLite is disposable. Rebuild it from NDJSON.

Files under `build/` are generated artifacts. Do not edit them by hand.

## Validation commands

Run these before requesting human review or proposing a pull request:

```bash
python3 scripts/validate_ndjson.py
python3 scripts/build_sqlite_index.py
```

On Windows systems where `python3` is an unavailable launcher alias, run the
same scripts with the locked virtual-environment interpreter and document the
fallback:

```bash
.venv\Scripts\python.exe scripts/validate_ndjson.py
.venv\Scripts\python.exe scripts/build_sqlite_index.py
```

## Future migration options

This model can be migrated to:

- MongoDB
- CouchDB
- DynamoDB
- Firestore
- PostgreSQL JSONB
- SQLite JSON1

The key is stable IDs and explicit schema versions.
