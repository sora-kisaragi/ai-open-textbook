# Writing Quality Policy Draft

Status: `draft`
Review status: `needs_human_review`

## Purpose

Define draft guidance for AI-assisted writing quality controls in repository
prose and future localized educational outputs. The goal is clarity,
specificity, educational usefulness, meaning preservation, and reviewability.

This draft supports review. It does not approve content, replace human review,
or introduce automated prose linting.

## Non-Goals

- Do not frame writing quality work as AI detector bypass.
- Do not use AI detector scores as acceptance or CI pass/fail criteria.
- Do not publish, approve, or mark student-facing content as release-ready
  through this policy alone.
- Do not weaken copyright, source, pedagogy, accessibility, or release review
  gates.
- Do not add textlint, Vale, Node dependencies, package manager files, or CI
  jobs through this draft.

## Target Language Scope

The repository remains English-first for source files, policies, issues,
prompts, metadata, and review artifacts.

Learner-facing Japanese material is a future localized output target. It may be
introduced later through explicit localization or Japanese draft workflows.

AI-assisted writing quality controls should eventually apply to both:

- English source and repository prose.
- Future Japanese learner-facing or teacher-facing outputs.

Automation should be phased:

- Phase 1: English repository prose and low-risk docs or prompts.
- Phase 2: Japanese localized, learner-facing, or teacher-facing drafts after
  policy and review gates are defined.

## Scope Split

English source and repository prose includes policies, prompts, issues,
metadata, review artifacts, and documentation. It should stay concise,
explicit, and easy to review.

Future Japanese learner-facing or teacher-facing outputs need separate review
for learner comprehension, age fit, terminology, examples, and localization
quality before automation is treated as useful evidence.

Machine-checkable style issues include repeated filler phrases, broken Markdown
structure, inconsistent headings, very long sentences, repeated vague
modifiers, and repository-specific banned phrasing.

Human-review-only writing judgments include age fit, cognitive load, meaning
drift, factual accuracy, originality, source risk, inclusive examples,
curriculum alignment claims, and whether a localized draft is pedagogically
appropriate.

## Weak Writing Patterns to Avoid

- Vague generalities without concrete learner value.
- Unsupported factual, legal, curriculum, or release-readiness claims.
- Inflated framing such as implying official approval or publication readiness.
- Empty conclusions that restate the prompt without adding evidence.
- Excessive structure that makes a short draft harder to review.
- Uniform sentence rhythm that obscures priority or causality.
- Responsibility-free phrasing that hides uncertainty or review needs.

## Meaning-Preservation Rules

When revising AI-assisted drafts, preserve:

- Meaning, scope, and uncertainty.
- Numbers, identifiers, filenames, links, commands, and code.
- Definitions, examples, causal relationships, and prerequisites.
- Status language such as `draft`, `needs_human_review`, or maintainer decision
  required.
- Existing human review gates and copyright/source risk notes.

If a source, curriculum claim, factual point, or learner-fit decision is
uncertain, record an open question instead of smoothing over the uncertainty.

## Relationship to Existing Guides

- `docs/STYLE_GUIDE.md` remains the baseline for repository writing and
  educational style.
- `docs/REVIEW_GUIDE.md` remains the baseline for review layers and human
  review expectations.
- `docs/AI_USAGE_POLICY.md` remains the baseline for allowed AI uses,
  prohibited uses, and PR disclosure.

This draft should be reconciled with those files after maintainer review. Avoid
duplicating long policy text across multiple documents.

## Open Questions

- Which maintainer owns review of this policy draft?
- Should the first automation target only `docs/` and `prompts/`?
- Which future workflow will introduce Japanese learner-facing drafts?
- What repository-specific phrasing, if any, should be machine-checkable?
- Who will maintain any future prose-lint dependency or CI warning job?
