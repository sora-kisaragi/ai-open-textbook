---
title: "Prepare export and index workflow for review builds"
labels: ["phase:mvp", "type:automation", "type:data-model"]
status: draft
---

## Purpose

Ensure generated indexes and review artifacts are reproducible from canonical NDJSON.

## Acceptance criteria

- [ ] Validation and SQLite index commands are documented (`python3 scripts/validate_ndjson.py`, `python3 scripts/build_sqlite_index.py`; Makefile targets if present).
- [ ] Generated files under `build/` are not manually edited; rebuild-from-source is the only update path.
- [ ] Export manifest expectations are listed (what `MANIFEST.json` should track for review builds).
- [ ] Failure reporting expectations are documented (failures surfaced in PRs, never hidden).
- [ ] CI relationship documented (`.github/workflows/validate.yml`).

## Dependencies

- Blocked by: draft 03.
- Blocks: draft 12.

## Suggested agent routing

- `schema-validator` (Sonnet-class).

## Review gates

- Maintainer review of workflow documentation.
