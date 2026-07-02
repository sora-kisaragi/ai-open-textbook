---
title: "Define answer and rubric versioning workflow"
labels: ["phase:mvp", "type:data-model", "type:review"]
status: draft
---

## Purpose

Prevent silent overwrites when answers, explanations, or rubrics change.

## Acceptance criteria

- [ ] Active, superseded, deprecated, and draft states are documented and mapped to `AGENTS.md` status values.
- [ ] `valid_from`, `valid_to`, `supersedes`, and `superseded_by` usage is documented with examples.
- [ ] Revision records in `data/collections/revisions.ndjson` are required for non-trivial changes.
- [ ] Human review requirements are clear (answer changes to reviewed items require review).
- [ ] Workflow is consistent with `docs/DATA_MODEL.md` answer versioning fields.

## Dependencies

- Blocked by: drafts 03, 07.
- Blocks: draft 12.

## Suggested agent routing

- `schema-validator` (Sonnet-class); `release-editor` for workflow integration.

## Review gates

- Maintainer review of the workflow document.
