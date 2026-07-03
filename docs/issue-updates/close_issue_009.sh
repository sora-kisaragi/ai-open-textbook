#!/usr/bin/env bash
set -euo pipefail

# Run only after PR #20 has been merged.
gh issue close 9 --comment "$(cat docs/issue-updates/close_issue_009.md)"
