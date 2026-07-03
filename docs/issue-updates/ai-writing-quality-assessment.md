# AI Writing Quality Controls Assessment

## Scope

This note assesses the repository state before registering issues for practical
AI-assisted writing quality controls. It does not approve content, change
lesson material, or introduce new tooling.

## Repository Findings

- `docs/STYLE_GUIDE.md` exists and already covers repository language, educational writing, code examples, and Markdown basics.
- `docs/AI_USAGE_POLICY.md` exists and already prohibits publishing without
  human review, invented sources, hidden uncertainty, private chain-of-thought
  storage, and student personal data use without approval.
- `docs/REVIEW_GUIDE.md` exists and already defines review layers for data
  validation, code execution, pedagogy, accessibility, copyright/source
  review, and release review.
- No existing textlint, Vale, markdownlint, or prose-specific lint configuration was found by repository search.
- `pyproject.toml` exists. `package.json` and `requirements.txt` are not present.
- GitHub Actions exist in `.github/workflows/validate.yml` and currently run the NDJSON validator and SQLite index build.
- `.claude/agents/` exists with specialist agents for curriculum planning,
  lesson writing, problem writing, schema validation, pedagogy review,
  copyright review, and release editing.
- Open GitHub issues inspected through `gh issue list` did not show equivalent AI-writing quality control issues.

## Tooling Assessment

Adding textlint or Vale immediately should be deferred. The repository
currently has Python project metadata and validation scripts, but no Node
package management convention and no existing prose linter configuration.

A low-risk first step is to create issues that:

- define the writing policy before automation,
- evaluate prose lint options before adding dependencies,
- keep any first CI check warning-only,
- separate machine-detectable prose checks from human review,
- avoid AI detector bypass framing.

## Decision Summary

Register a small six-issue set for policy, agent guidance, lint evaluation,
warning-only CI, review checklist, and a later pilot. Keep this task limited to
assessment and issue registration.

## Validation Evidence

- Repository rules read: `AGENTS.md`, `CLAUDE.md`,
  `docs/OPERATING_RULES.md`, `docs/PROCESS.md`, `docs/DATA_MODEL.md`,
  `docs/STYLE_GUIDE.md`, `docs/REVIEW_GUIDE.md`,
  `docs/AI_USAGE_POLICY.md`.
- Agent definitions inspected under `.claude/agents/`.
- GitHub CLI authentication and remote were checked before issue registration.

## Open Questions

- Which maintainer should own the human review gate for the writing quality policy?
- Should the first prose automation target only Markdown docs, or also lesson Markdown under `lessons/` after the policy is reviewed?

## Related Issues

- #22: Define AI-assisted writing quality policy.
- #23: Add an agent skill for Japanese educational prose cleanup.
- #24: Evaluate prose linting options for Japanese writing quality.
- #25: Add warning-only CI for machine-detectable prose issues.
- #26: Add AI-assisted prose review checklist.
- #27: Pilot the writing-quality workflow on one existing draft only.
