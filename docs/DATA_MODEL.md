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

## Required fields by collection

All records in `data/collections/*.ndjson` must include the core fields:
`id`, `type`, `schema_version`, `status`, `created_at`, and `updated_at`.

Additional required fields are:

| Collection | Type | Additional required fields |
| --- | --- | --- |
| `lessons.ndjson` | `lesson` | `title`, `body_ref`, `learning_objectives` |
| `problems.ndjson` | `problem` | `question`, `question_type`, `lesson_refs`, `answer_refs`, `rubric_refs` |
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
same scripts with the available Python interpreter and document the fallback:

```bash
python scripts/validate_ndjson.py
python scripts/build_sqlite_index.py
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
