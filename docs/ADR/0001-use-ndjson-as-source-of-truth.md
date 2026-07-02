# ADR 0001: Use NDJSON as the Source of Truth

## Status

Accepted

## Context

Educational materials change over time.
Answers, rubrics, explanations, and curriculum mappings may be revised.
GitHub review should show small readable diffs.

## Decision

Use NDJSON files as canonical data.
Generate SQLite indexes for local search and reports.

## Consequences

Positive:

- Easy Git diff and review.
- Easy migration to document databases.
- Per-record schema versioning.
- Simple append-only revision logs.

Negative:

- Cross-record constraints need custom validation.
- Complex queries require generated indexes.
