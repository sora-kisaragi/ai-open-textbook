# MVP Review Checklist

Status: `draft`
Review status: `needs_human_review`

## Purpose

Provide a PR-review checklist for MVP educational materials before public
preview or release-scope decisions. The checklist supports review; it does not
grant approval by itself.

## Scope

Use this checklist for MVP lesson requirements, lesson drafts, problem-bank
planning, teacher-guide requirements or drafts, data records, generated index
evidence, and public-preview readiness review.

Do not use it to approve publication, official curriculum alignment, copyright
risk, license policy changes, or final age-appropriateness decisions without
explicit human maintainer approval.

## PR Review Usage

In each PR, reviewers should record pass, non-blocking finding, blocking
finding, or not applicable for the checklist areas relevant to the change.
Include concrete file paths, record IDs, validation output, and open human
decisions. Do not paste private reasoning into PR comments.

PR authors should link this canonical checklist and include only the evidence
that applies to the PR scope. A content PR may need pedagogy,
copyright/source-risk, accessibility, and content accuracy evidence. A
data-only PR may need data/versioning and validation evidence.

## Non-Official Status Check

- [ ] The material is described as open educational material, supplemental
      resource, self-study material, or teacher support material.
- [ ] No file claims official government approval or official textbook status.
- [ ] No final curriculum alignment claim is made without a human decision and
      supporting source evidence.
- [ ] Public-preview language is clearly separated from stable release or
      published status.

## Pedagogy Review

- [ ] Target age fit is appropriate for high school learners.
- [ ] Cognitive load is controlled by short examples and limited new concepts.
- [ ] Prerequisite gaps are identified and either remediated or deferred.
- [ ] Lesson order is consistent with the MVP path: variables, conditionals,
      then loops.
- [ ] Expected misconceptions are listed before practice or assessment is
      generated.
- [ ] Feedback strategy addresses the reasoning step behind each misconception.
- [ ] Assessment intent is connected to learning objectives, not only final
      answers.
- [ ] Practice progression moves from basic to standard to advanced work.
- [ ] Objectives, problems, answers, and rubrics are traceable to each other
      when those artifacts are in scope.

## Copyright and Source-Risk Review

- [ ] Explanations, prompts, examples, answers, rubrics, and feedback use
      original wording.
- [ ] Close paraphrase risk has been checked against known source material used
      during drafting.
- [ ] Quotations are avoided unless necessary, attributed, and scoped for human
      review.
- [ ] Source attribution is present where factual or curriculum claims need it.
- [ ] Generated diagrams are original and do not imitate proprietary diagrams.
- [ ] Paid problem books, proprietary teacher manuals, hidden answer keys, and
      protected textbook wording are not used as source material.
- [ ] Any unresolved source-risk question is listed as a human review need.

## Accessibility Review

- [ ] Meaningful images and diagrams have alt text or equivalent text.
- [ ] Meaning does not depend on color alone.
- [ ] Tables, traces, and code examples are readable in text form.
- [ ] Language is readable for the target learners and avoids unnecessary
      jargon.
- [ ] Web or interactive materials include keyboard and screen-reader
      considerations.
- [ ] Examples avoid unnecessary personal data, sensitive traits, wealth,
      family structure, region, or narrow cultural knowledge.
- [ ] Non-visual alternatives are available for visual explanations or
      diagrams.

## Content Accuracy Review

- [ ] Definitions are technically correct and appropriate for the lesson
      scope.
- [ ] Answers and accepted variants are correct when answer materials are in
      scope.
- [ ] Edge cases required by the objective or problem are handled.
- [ ] Executable examples run as intended when they are meant to run.
- [ ] Factual, curriculum, legal, or technical claims cite sources when needed
      or are marked as needing review.

## Data and Versioning Review

- [ ] Canonical records remain in `data/collections/*.ndjson`.
- [ ] Generated SQLite files under `build/` are not edited by hand.
- [ ] IDs are stable, lowercase, dot-separated, and version-aware where
      appropriate.
- [ ] New or meaningfully changed educational records have revision history.
- [ ] Problem records, answer records, and rubric records remain separate.
- [ ] Status values stay within the allowed repository status set.
- [ ] No record is moved to `approved` or `published` without explicit human
      approval.

## Python and Example-Code Safety Review

- [ ] Examples intended to run are executable.
- [ ] Python is described as the project MVP example language, not as an
      official curriculum requirement.
- [ ] Examples do not hide external dependencies.
- [ ] Beginner lesson examples stay short enough to trace by hand.
- [ ] Examples do not perform unintended network access.
- [ ] Examples do not perform unintended file-system writes.
- [ ] Examples do not include secrets, tokens, API keys, or credentials.
- [ ] Examples do not depend on personal data or learner-identifying
      information.
- [ ] Examples avoid unsafe side effects unless explicitly reviewed and in
      scope.

## Problem-Bank Review

- [ ] MVP target remains 8 problems per lesson and 24 problems total unless a
      maintainer changes the scope.
- [ ] Per-lesson difficulty distribution follows the accepted design when
      problem generation is in scope.
- [ ] Machine-checkable and human-reviewed problem types are clearly
      distinguished.
- [ ] Every problem references separate answer and rubric records.
- [ ] Common mistakes and feedback requirements are defined before answer or
      rubric generation.
- [ ] Originality review happens before problem generation or release-scope
      review.

## Answer and Rubric Review

- [ ] Answer records are separate from problem records.
- [ ] Rubric records are separate from problem and answer records.
- [ ] Canonical answers and accepted variants are explicit when needed.
- [ ] Rubric criteria match the problem objective and difficulty.
- [ ] Human-reviewed problem types are not treated as machine-checked without a
      reviewed rubric decision.
- [ ] Answer and rubric records use review status values that preserve human
      review gates.
- [ ] Meaningful answer or rubric changes preserve revision history.

## Teacher Guide Review

- [ ] Teacher guides are supplemental support material only.
- [ ] Teacher guides are not described as official guidance.
- [ ] Full teacher-guide body drafting waits for pedagogy review unless a
      maintainer explicitly decides otherwise.
- [ ] Lesson flow, teacher questions, timing, assessment points,
      misconceptions, and feedback strategies are present.
- [ ] Timing guidance remains draft until reviewed for classroom fit.
- [ ] Teacher-guide public-preview inclusion remains a maintainer decision.

## Public Preview Readiness

- [ ] Required validation commands passed or failures are documented.
- [ ] Validation evidence includes `python3 scripts/validate_ndjson.py` and
      `python3 scripts/build_sqlite_index.py`, or the documented Windows
      fallback commands with the launcher issue recorded.
- [ ] `git diff --check` passed.
- [ ] Required human review gates are identified and assigned.
- [ ] Copyright/source notes are present.
- [ ] Accessibility notes are present.
- [ ] Open maintainer decisions are listed.
- [ ] Public-preview wording does not imply stable, approved, published, or
      official status.

## Human Review Gates

Human approval is required for public release, license changes, curriculum
alignment claims, copyright-risk decisions, sensitive social topics,
age-appropriateness decisions, accessibility acceptance for release-scope
material, and changes from `approved` to `published`.

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

## Blocking vs Non-Blocking Findings

Blocking findings should stop merge or release review until resolved. Examples:

- Broken validation, unresolved required references, or invalid status values.
- Missing answer/rubric separation for problem records.
- Copied, closely paraphrased, or suspiciously imitative educational content.
- Missing human gate for age fit, copyright risk, accessibility, release, or
  curriculum alignment.
- Examples with unreviewed network access, file-system writes, secrets,
  personal data, or unsafe side effects.

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
- Link to this checklist plus relevant MVP review evidence or findings.
- AI usage summary.
- Human review needs.
- Copyright/source note.
- Backward compatibility note.
- Related issues.

## Open Questions

- Should teacher guides be included in v0.1 public preview or treated as beta
  support material?
- Should lesson records later add explicit teacher-guide reference fields?
- Should timing examples use flexible bands only, or include 45/50-minute
  examples?
- Should a named `pedagogy-reviewer` pass be mandatory before any full
  teacher-guide body draft?
