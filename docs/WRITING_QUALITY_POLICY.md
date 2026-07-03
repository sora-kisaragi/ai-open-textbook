# AI-Assisted Writing Quality Policy Draft

Status: `draft`
Review status: `needs_human_review`

## Purpose

Define draft guidance for AI-assisted writing quality controls in repository
prose and future localized educational outputs. The goal is clarity,
specificity, educational usefulness, reviewability, factual responsibility,
source and uncertainty handling, and preservation of meaning during rewrites.

This draft supports review. It does not approve content, replace human review,
or introduce automated prose linting.

Factual accuracy, age fit, copyright review, and accessibility review take
priority over making prose sound natural or human-written.

## Non-goals

- AI detector bypass.
- Using AI detector scores as acceptance criteria or CI pass/fail criteria.
- Hiding AI involvement or making generated writing look deceptively human.
- Automatic approval of generated material.
- Replacing pedagogy, copyright, accessibility, maintainer, or release review.
- Rewriting student-facing content before human review gates are satisfied.
- Adding textlint, Vale, Node dependencies, package manager files, or CI jobs
  through this draft.

## Target language scope

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

This is a proposed language scope. Maintainer confirmation is required before
using it as an implementation or release criterion.

## Scope Split

### English source and repository prose

English source and repository prose includes policies, prompts, issues,
metadata, review artifacts, and documentation. It should stay concise,
specific, easy to review, and explicit about source status, uncertainty, and
human review needs.

### Future Japanese learner-facing or teacher-facing outputs

Future Japanese learner-facing or teacher-facing outputs need separate review
for learner comprehension, age fit, terminology, examples, localization
quality, accessibility, and copyright/source risk before automation is treated
as useful evidence. Do not pilot this policy on learner-facing files until the
conditions in #27 are met.

## Weak Writing Patterns to Avoid

- Vague generalities without concrete learner value.
- Unsupported factual, legal, curriculum, or release-readiness claims.
- Inflated framing such as implying official approval or publication readiness.
- Empty conclusions that restate the prompt without adding evidence.
- Excessive structure without substance.
- Uniform rhythm or repetitive paragraph patterns that obscure priority or
  causality.
- Responsibility-free phrasing that hides uncertainty or review needs.
- Vague attribution such as "studies show" without a source.
- Polished wording that hides uncertainty, missing sources, or human review
  needs.
- Claims that are broader than the available evidence.
- Filler phrases or summaries that do not add a concrete decision, next step,
  or learning value.

These patterns are review prompts, not a style-policing checklist. Legitimate
writing should not be blocked only because it matches one pattern in isolation.

## Meaning-preservation requirements

When revising AI-assisted drafts, preserve:

- Numbers.
- Identifiers.
- Filenames and paths.
- Issue numbers.
- Code.
- Commands.
- Definitions.
- Examples.
- Causal relationships.
- Prerequisite relationships.
- Review status.
- Source status.
- Uncertainty markers.
- Non-official-material disclaimers.

If a rewrite changes any of these items, the change must be explicitly
summarized. If a source, curriculum claim, factual point, or learner-fit
decision is uncertain, record an open question instead of smoothing over the
uncertainty.

## Machine-checkable issues

Machine checks may support review, but they do not approve educational
content.

Examples of machine-checkable issues include:

- Markdown structure.
- Repeated phrases.
- Long sentences.
- Banned filler expressions.
- Stale path references.
- Missing required sections.
- Terminology consistency.
- Link format.
- Checklist presence.

## Human-review-only judgments

Human review is required for judgments that need subject, learner, legal,
accessibility, or release context. Examples include:

- Pedagogy fit.
- Age fit.
- Cognitive load.
- Factual correctness.
- Copyright risk.
- Accessibility adequacy.
- Curriculum alignment claims.
- Appropriateness of examples.
- Whether a Japanese localized output is suitable for learners.
- Whether a draft should be accepted or published.

## Relationship to existing policies

- `docs/STYLE_GUIDE.md` remains the baseline for repository writing and
  educational style.
- `docs/REVIEW_GUIDE.md` remains the baseline for review layers and human
  review expectations.
- `docs/AI_USAGE_POLICY.md` remains the baseline for allowed AI uses,
  prohibited uses, and PR disclosure.
- `docs/review/MVP_REVIEW_CHECKLIST.md` remains the canonical MVP review
  checklist path. Issue #26 should extend that file instead of the superseded
  `docs/MVP_REVIEW_CHECKLIST.md` pointer.

This draft should be reconciled with those files after maintainer review. Avoid
duplicating long policy text across multiple documents.

## Rollout guidance

- Start with policy and review guidance.
- Do not implement tooling until #24 evaluates options.
- Do not add warning-only CI until #25.
- Do not pilot on learner-facing files until #27 conditions are met.
- Prefer low-risk docs and prompts for early pilots.
- Treat Japanese learner-facing output as a later phase after review gates are
  defined.
- Keep initial automation warning-only if introduced later.

Issue dependencies:

- #22 defines the policy and language scope.
- #23 depends on #22 for skill behavior and language scope.
- #24 depends on #22 for textlint, Vale, and markdownlint evaluation scope.
- #25 depends on #24 and maintainer decision on dependencies.
- #26 depends on #22 and should extend
  `docs/review/MVP_REVIEW_CHECKLIST.md`.
- #27 depends on #22, #23, and #26, and should prefer non-learner-facing pilot
  targets.

## Open Questions

- Which maintainer owns review of this policy draft?
- Should the first automation target only `docs/` and `prompts/`?
- Which future workflow will introduce Japanese learner-facing drafts?
- What repository-specific phrasing, if any, should be machine-checkable?
- Who will maintain any future prose-lint dependency or CI warning job?
