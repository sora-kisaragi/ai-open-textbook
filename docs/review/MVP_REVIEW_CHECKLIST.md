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
- [ ] Required human review gates are identified and assigned.
- [ ] Copyright/source notes are present.
- [ ] Accessibility notes are present.
- [ ] Open maintainer decisions are listed.
- [ ] Public-preview wording does not imply stable, approved, published, or
      official status.

## PR Review Usage

In each PR, reviewers should record pass, non-blocking finding, blocking
finding, or not applicable for the checklist areas relevant to the change.
Include concrete file paths, record IDs, validation output, and open human
decisions. Do not paste private reasoning into PR comments.

## Human Review Gates

Human approval is required for public release, license changes, curriculum
alignment claims, copyright-risk decisions, sensitive social topics,
age-appropriateness decisions, accessibility acceptance for release-scope
material, and changes from `approved` to `published`.

## Open Questions

- Should teacher guides be included in v0.1 public preview or treated as beta
  support material?
- Should lesson records later add explicit teacher-guide reference fields?
- Should timing examples use flexible bands only, or include 45/50-minute
  examples?
- Should a named `pedagogy-reviewer` pass be mandatory before any full
  teacher-guide body draft?
