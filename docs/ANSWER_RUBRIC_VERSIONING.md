# Answer and Rubric Versioning Walkthrough

Status: `draft`
Review status: `needs_human_review`

This walkthrough explains how to apply answer and rubric versioning during
routine problem-bank work. `docs/DATA_MODEL.md` remains the canonical source
for field requirements, status values, validation behavior, and supersession
rules.

## Core idea

Do not silently overwrite educational truth. If an answer or rubric changes in
a meaningful way, keep the old record, add or update explicit version metadata,
and append a `revisions.ndjson` record for the change.

Use this document as an operational checklist, not as a replacement for the
full data model.

## Field meanings

`valid_from`
: The first date when this answer or rubric version should be treated as
applicable for its problem.

`valid_to`
: The last date when this version should be treated as applicable. Use `null`
for the current open-ended version. When a version is replaced, close the old
version by setting `valid_to` to the replacement date when the schema supports
that field for the record.

`supersedes`
: The previous record ID that this version replaces. A v2 record normally
points back to the v1 record it replaces.

`superseded_by`
: The replacement record ID for an older version, when known. A v1 record may
point forward to the v2 record that replaces it.

## Status and review status

`status` and `review_status` are different concepts.

- `status` is the repository lifecycle enum defined in `AGENTS.md` and
  `docs/DATA_MODEL.md`, such as `draft`, `machine_checked`,
  `human_review_requested`, `approved`, `published`, `deprecated`, or
  `superseded`.
- `review_status` describes review needs for a specific educational artifact.
  Values such as `needs_human_review` are not `status` values and must not be
  added to the `status` enum.

For a new version of a reviewed answer, start conservatively with
`status: "draft"` and `review_status: "needs_human_review"`.

For a new version of a reviewed rubric, start conservatively with
`status: "draft"`. If a rubric record uses an approved `review_status` field,
set it to `needs_human_review` until review is complete.

## Active version

The project does not need a separate `active` field.

An answer or rubric is operationally active when all of the following are true:

- It is the intended current version for its `problem_id`.
- Its `valid_from` has started.
- Its `valid_to` is `null` or has not passed.
- It is not marked `superseded` or `deprecated`.
- It is not known to have a `superseded_by` replacement.

Being active does not mean being approved or published. A draft answer can be
the current active draft for review, while still requiring human review before
release.

## Answer supersession example

Illustrative snippets only:

```json
{
  "id": "ans.prob.example.001.v1",
  "status": "superseded",
  "review_status": "needs_human_review",
  "valid_from": "2026-07-02",
  "valid_to": "2026-07-10",
  "supersedes": null,
  "superseded_by": "ans.prob.example.001.v2"
}
```

```json
{
  "id": "ans.prob.example.001.v2",
  "status": "draft",
  "review_status": "needs_human_review",
  "valid_from": "2026-07-10",
  "valid_to": null,
  "supersedes": "ans.prob.example.001.v1",
  "superseded_by": null
}
```

Use this pattern when the canonical answer, accepted variants, explanation, or
verification meaning changes enough that reviewers should see a new version.

## Rubric meaningful-change example

Illustrative snippets only:

```json
{
  "id": "rubric.prob.example.001.v1",
  "status": "superseded",
  "valid_to": "2026-07-10",
  "superseded_by": "rubric.prob.example.001.v2"
}
```

```json
{
  "id": "rubric.prob.example.001.v2",
  "status": "draft",
  "valid_from": "2026-07-10",
  "valid_to": null,
  "supersedes": "rubric.prob.example.001.v1",
  "criteria": [
    { "id": "c1", "points": 1, "description": "Identifies the final value." },
    { "id": "c2", "points": 1, "description": "Explains the state update." }
  ]
}
```

Use a new rubric version when point allocation, criteria meaning, scoring
thresholds, or review expectations change. Minor typo fixes can be handled as
ordinary edits only if they do not change the educational meaning, but they
still need appropriate revision history when non-trivial.

## Revision record expectation

Every non-trivial answer or rubric change requires an appended
`data/collections/revisions.ndjson` record. The revision should explain what
changed and why, using a short public reason rather than private reasoning.

Do not modify lesson, problem, answer, rubric, or teacher-guide records as part
of documentation-only walkthrough work unless the issue explicitly asks for
data changes.
