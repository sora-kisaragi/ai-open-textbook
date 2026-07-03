# Prose Warning Checks

Status: `draft`
Review status: `needs_human_review`

## Purpose

Define the first warning-only prose check pilot for machine-detectable review
prompts. The pilot helps reviewers notice mechanical prose issues in low-risk
repository prose without adding dependencies or replacing human review.

Warnings do not approve, reject, or publish prose. They are not AI detector
scores and must not be used as evidence that text is human-written, correct,
age-appropriate, accessible, or release-ready.

## Scope

The default local and CI scope is:

- `docs/`
- `prompts/`
- `.github/ISSUE_TEMPLATE/`, when present
- `.github/PULL_REQUEST_TEMPLATE.md`, when present

The script excludes generated, binary, and canonical data paths, including:

- `build/`
- `.git/`
- binary files
- `data/collections/*.ndjson`

Student-facing Japanese material remains behind pedagogy, copyright,
accessibility, maintainer, and release review. It should not be treated as
approved or rejected because of this script.

## Non-goals

- Add Node, textlint, Vale, markdownlint, package-manager files, lockfiles, or
  external prose-lint configuration.
- Vendor external tools, prompts, dictionaries, rule sets, or source text.
- Use AI detector scores as pass/fail criteria.
- Auto-fix or rewrite prose.
- Block pull requests because prose warnings were found.
- Replace pedagogy, copyright, accessibility, maintainer, or human release
  review.

## Local Run Commands

Run the default low-risk scope:

```bash
python scripts/check_prose_warnings.py
```

Run specific paths:

```bash
python scripts/check_prose_warnings.py docs/STYLE_GUIDE.md prompts/
```

Emit GitHub Actions warning annotations locally:

```bash
python scripts/check_prose_warnings.py --format github
```

The script exits with status `0` when warning findings are present. It exits
non-zero only for invalid CLI usage, runtime errors, or unreadable files that
were explicitly requested.

## CI Behavior

`.github/workflows/validate.yml` runs:

```bash
python3 scripts/check_prose_warnings.py --format github
```

The prose check runs after the existing NDJSON validation and SQLite index
build. Warning findings emit GitHub Actions annotations and exit `0`, so they
do not block pull requests.

Runtime errors still fail the workflow because they indicate a tooling problem,
not a prose warning. This keeps the existing validation job meaningful without
weakening NDJSON or SQLite checks.

## Warning Categories

- `long-line`: a prose line may be difficult to scan.
- `long-sentence`: a sentence may be too long for reviewability.
- `repeated-phrase`: a phrase appears repeatedly within one file.
- `vague-phrase`: a phrase may be vague, inflated, or over-polished.
- `heading-duplicate`: the same heading text appears more than once in a file.
- `missing-final-newline`: a text file lacks a final newline.
- `detector-framing`: wording may imply AI detector bypass or humanizer goals.
- `stale-path`: a path reference may point to a superseded location.

## How to Interpret Warnings

Each warning is a review prompt only. A reviewer should check whether the
warning points to a real issue in context. Some warnings will be acceptable
because the repeated term, long sentence, or policy phrase is necessary.

Do not rewrite prose only to silence a warning. Preserve meaning, identifiers,
commands, paths, issue numbers, source status, review status, and uncertainty
markers.

## How to Override or Ignore Warnings in PR Review

A warning can be ignored in PR review with a short public reason, for example:

- The repeated phrase is a required policy term.
- The long line is a table row, command, or path.
- The detector-framing phrase appears in a policy warning, not as a goal.
- The stale path is quoted as a historical or superseded reference.

Repeated false positives should lead to rule adjustment or removal.

## Human-Review-Only Judgments

Human review is still required for:

- Factual correctness.
- Age fit.
- Cognitive load.
- Pedagogical usefulness.
- Curriculum alignment claims.
- Copyright and source risk.
- Accessibility.
- Appropriateness of examples.
- Meaning preservation after edits.
- Whether any draft should be accepted, approved, published, or released.

## False Positive Handling

False positives are expected during the pilot. Keep fixes small and avoid broad
rewrites. If a rule creates noise without useful review prompts, update or
remove the rule in a separate reviewable change.

## Relationship to `docs/PROSE_LINTING_EVALUATION.md`

`docs/PROSE_LINTING_EVALUATION.md` evaluated textlint, Vale, markdownlint, and
the existing Python-only workflow. It recommended a later warning-only pilot on
low-risk paths before adopting dependencies or applying checks to
learner-facing material.

This document records that pilot's scope and behavior. It does not approve a
full prose-linting policy or dependency choice.

## Relationship to `docs/WRITING_QUALITY_POLICY.md`

`docs/WRITING_QUALITY_POLICY.md` defines draft writing-quality principles,
meaning-preservation expectations, and human-review-only judgments. The prose
warning script implements only a small mechanical subset of those ideas.

The policy remains the higher-level review guide. The script is supporting
evidence only.

## Open Questions

- Who owns warning rule maintenance and false-positive triage?
- Should any warning categories be disabled before wider use?
- Should future checks include more repository-specific stale paths or terms?
- Should warning-only checks ever include lesson bodies, and under what human
  review gates?
- What evidence should be collected before considering external prose-lint
  dependencies?
