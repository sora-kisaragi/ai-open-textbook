#!/usr/bin/env bash
set -euo pipefail

gh issue comment 12 --body 'Prepared an MVP release checklist draft in `docs/release/MVP_RELEASE_CHECKLIST.md`.

The checklist defines required content, data, review, validation, source/copyright, accessibility, release-note, and human approval gates for a future v0.1 release.

It preserves the distinction between draft, review candidate, public preview, and stable release, and does not allow approved/published status without explicit human approval.'
