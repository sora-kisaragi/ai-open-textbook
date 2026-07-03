# MVP Review Checklist

Status: `draft`
Review status: `needs_human_review`

## Purpose

Provide one PR-ready review checklist for the MVP v0.1 materials. This
checklist coordinates pedagogy, copyright/source, accessibility, data/model,
Python/example-code, problem-bank, answer/rubric, teacher-guide, and release
readiness review.

Machine checks and checklist completion do not replace human review. This
project remains an open educational material and must not be described as an
official approved textbook.

## Scope

Use this checklist for MVP work on:

- Three programming lessons: variables and assignment, conditionals, and loops.
- Lesson requirements and later student-facing lesson bodies.
- Problem, answer, and rubric records.
- Teacher-guide drafts.
- Generated indexes and validation evidence.
- Public-preview readiness reviews.

Out of scope:

- Official curriculum alignment approval.
- License policy changes.
- Public release approval without maintainer review.
- Copying, paraphrasing, or imitating existing textbooks, paid problem books,
  proprietary diagrams, teacher manuals, answer keys, or proprietary content.

## How to Use This Checklist in PR Reviews

1. Add the relevant checklist sections to the PR body or a review comment.
2. Mark each item as pass, non-blocking finding, blocking finding, or not
   applicable.
3. Link concrete files, record IDs, and validation output when making a
   finding.
4. Keep educational content in `draft`, `machine_checked`, or
   `human_review_requested` until the required human review gate passes.
5. Do not approve public release, official alignment claims, copyright-risk
   decisions, or age-appropriateness decisions by machine review alone.

## Pedagogy Checklist

- [ ] Target age fit is appropriate for Japanese high school learners and
      does not assume advanced programming experience.
- [ ] Prerequisite fit is explicit, including prerequisite gaps and whether a
      concept is assumed or taught in the lesson.
- [ ] Cognitive load is controlled by short examples, limited new concepts,
      and clear sequencing.
- [ ] Lesson sequence consistency matches the MVP order: variables,
      conditionals, then loops.
- [ ] Misconceptions are identified before practice or assessment is generated.
- [ ] Worked examples are short, traceable, and aligned with lesson objectives.
- [ ] Practice progression moves from basic to standard to advanced work.
- [ ] Assessment items align with the stated learning objectives.
- [ ] Objectives, problems, answers, and rubrics are traceable to each other.

## Copyright/Source Checklist

- [ ] Explanations use original wording.
- [ ] Problems, answers, explanations, distractors, and rubrics are original.
- [ ] Content does not copy, closely paraphrase, or imitate existing
      textbooks, paid problem books, proprietary diagrams, teacher manuals,
      answer keys, or proprietary educational content.
- [ ] Citations and source references are not invented.
- [ ] Source references are separated from curriculum alignment claims.
- [ ] Quotations are minimized, attributed, and used only when necessary.
- [ ] Public-release copyright/source decisions are left for human review.

## Accessibility Checklist

- [ ] Meaningful images and diagrams have alt text or equivalent text.
- [ ] No meaning depends on color alone.
- [ ] Tables are readable as text and have clear headings.
- [ ] Examples are inclusive and broadly understandable.
- [ ] Scenarios are culturally neutral unless specific context is educationally
      necessary and reviewed.
- [ ] Materials avoid unnecessary personal data, sensitive traits, secrets, and
      learner-identifying information.
- [ ] Future web or interactive materials consider keyboard access,
      screen-reader structure, and text alternatives.

## Data/Model Consistency Checklist

- [ ] NDJSON under `data/collections/` remains the canonical source.
- [ ] SQLite files under `build/` are treated as generated-only artifacts.
- [ ] IDs are stable, lowercase, dot-separated, and version-aware where
      appropriate.
- [ ] Required references resolve, including lesson, problem, answer, rubric,
      source, revision, and supersession references.
- [ ] Non-trivial content or data changes append revision records.
- [ ] Answers and rubrics are not silently overwritten; meaningful changes use
      revision history or versioned replacements.

## Python/Example-Code Checklist

- [ ] Examples intended to run are executable.
- [ ] Python is described as the project MVP example language, not as an
      official curriculum requirement.
- [ ] Examples do not hide external dependencies.
- [ ] Beginner lesson examples stay short enough to trace by hand.
- [ ] MVP examples avoid network calls, file-system side effects, secrets, and
      personal data unless explicitly reviewed.

## Problem-Bank Checklist

- [ ] MVP target remains 8 problems per lesson and 24 problems total.
- [ ] Per-lesson distribution is basic 4, standard 3, advanced 1.
- [ ] At least 5 machine-checkable problems per lesson is used as a target.
- [ ] Every problem references separate answer and rubric records.
- [ ] Common mistakes and feedback requirements are defined for each problem
      type before answer/rubric generation.
- [ ] Originality review happens before problem generation or release-scope
      review.

## Answer/Rubric Checklist

- [ ] Answer records are separate from problem records.
- [ ] Rubric records are separate from problem and answer records.
- [ ] Canonical answers and accepted variants are explicit when needed.
- [ ] Rubric criteria match the problem objective and difficulty.
- [ ] Human-reviewed problem types are not treated as machine-checked without a
      reviewed rubric decision.
- [ ] Answer and rubric records use `needs_human_review` until reviewed.
- [ ] Meaningful answer or rubric changes preserve revision history.

## Teacher-Guide Checklist

- [ ] Teacher guides are supplemental support only.
- [ ] Teacher guides are not described as official guidance.
- [ ] Lesson flow is clear and aligned with the lesson requirements.
- [ ] Suggested questions support misconceptions and formative checks.
- [ ] Timing guidance is realistic and marked as draft until reviewed.
- [ ] Assessment points are connected to objectives and practice.
- [ ] Misconception feedback strategies are included.
- [ ] Human review is required before any public preview.

## Release-Readiness Relationship

This checklist supports release readiness, but it is not the release decision.
Before public preview, the release review must confirm:

- Machine validation has passed.
- Required human review gates have passed.
- Status values are appropriate.
- Release notes include non-official positioning and copyright/source notes.
- No content is moved to `published` without maintainer approval.

## Reviewer Role Routing

- `curriculum-planner`: objectives, prerequisites, sequence, and lesson graph.
- `lesson-writer`: lesson requirements and student-facing explanation quality.
- `problem-writer`: problem design, difficulty, feedback, and answer/rubric
  separation.
- `schema-validator`: NDJSON shape, identifiers, links, and generated indexes.
- `pedagogy-reviewer`: age fit, cognitive load, practice progression, and
  misconception coverage.
- `copyright-reviewer`: originality, quotation risk, source attribution, and
  public-release copyright risk.
- `release-editor`: integration, release notes, checklist evidence, and final
  release-readiness coordination.

## Human Review Gates

Human approval is required for:

- Public release.
- License changes.
- Curriculum alignment claims.
- Copyright-risk decisions.
- Sensitive social topics.
- Age-appropriateness decisions.
- Accessibility acceptance for release-scope material.
- Changes from `approved` to `published`.

## Blocking vs Non-Blocking Findings

Blocking findings should stop merge or release review until resolved. Examples:

- Broken validation, unresolved required references, or invalid status values.
- Missing answer/rubric separation for problem records.
- Copied, closely paraphrased, or suspiciously imitative educational content.
- Missing human gate for age fit, copyright risk, accessibility, release, or
  curriculum alignment.
- Examples with unreviewed network, file-system, secret, or personal-data side
  effects.

Non-blocking findings may be tracked as follow-up work when they do not affect
current scope. Examples:

- Minor wording improvements in draft-only docs.
- Additional optional examples beyond the accepted MVP scope.
- Formatting cleanup that does not affect validation, meaning, or review
  evidence.

## Required PR Evidence

Each PR should include:

- Scope.
- Files changed.
- Data records changed.
- Validation result for `python3 scripts/validate_ndjson.py` or documented
  Windows fallback `python scripts/validate_ndjson.py`.
- Validation result for `python3 scripts/build_sqlite_index.py` or documented
  Windows fallback `python scripts/build_sqlite_index.py`.
- `git diff --check` result.
- AI usage summary.
- Human review needs.
- Copyright/source note.
- Backward compatibility note.
- Related issues.

## Open Questions

- Should every content PR paste this whole checklist, or should PR authors link
  this file and include only relevant findings?
- Should the repository add a PR template section that maps directly to this
  checklist?
- Should release-scope accessibility acceptance be a separate named status
  field or remain a review note?
- Should teacher guides be included in the v0.1 public preview or handled as
  beta support material?
