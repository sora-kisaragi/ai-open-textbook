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

## SQLite projection

`scripts/build_sqlite_index.py` creates:

- `build/index.sqlite`

Tables:

- `documents`: all NDJSON records as JSON text.
- `edges`: references between records.
- `doc_fts`: optional FTS5 search index when available.

SQLite is disposable. Rebuild it from NDJSON.

## Future migration options

This model can be migrated to:

- MongoDB
- CouchDB
- DynamoDB
- Firestore
- PostgreSQL JSONB
- SQLite JSON1

The key is stable IDs and explicit schema versions.
