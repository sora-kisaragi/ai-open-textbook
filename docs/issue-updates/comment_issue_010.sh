#!/usr/bin/env bash
set -euo pipefail

gh issue comment 10 --body 'Prepared an MVP review checklist draft in `docs/review/MVP_REVIEW_CHECKLIST.md`.

The checklist covers pedagogy, copyright/source risk, accessibility, teacher-guide review, data/versioning review, and public-preview readiness.

It does not grant approval by itself. Human review remains required before publication or any approved/published status change.'
