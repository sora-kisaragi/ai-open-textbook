---
title: "Strengthen schema and validation policy for NDJSON collections"
labels: ["phase:mvp", "type:data-model", "type:automation"]
status: draft
---

## Purpose

Improve validation around lessons, problems, answers, rubrics, sources, and revisions in `data/collections/*.ndjson`.

## Acceptance criteria

- [ ] Required fields are documented per collection (id, type, schema_version, status, created_at, updated_at).
- [ ] Identifier rules match `AGENTS.md` (stable, lowercase, dot-separated, version-aware).
- [ ] Supersession and revision rules are checked (`supersedes`, `superseded_by`, revision records for non-trivial changes).
- [ ] Validation commands are documented (`python3 scripts/validate_ndjson.py`, `python3 scripts/build_sqlite_index.py`).
- [ ] Generated SQLite artifacts under `build/` remain generated-only and are never hand-edited.

## Dependencies

- Blocked by: draft 01.
- Blocks: drafts 08, 11.

## Suggested agent routing

- `schema-validator` (Sonnet-class).

## Review gates

- Machine checks must pass; policy text needs maintainer review.
