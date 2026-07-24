# Content Depth Standard

Status: `draft`
Review status: `needs_human_review`
Tracking issues: #90, #91

## Purpose

This standard defines observable evidence for a teachable 50-minute Information I
period. It does not use character counts as a proxy for quality and does not
authorize approval, publication, curriculum-alignment, age-fit, or copyright
decisions. Machine checks report structural evidence; humans judge whether that
evidence is accurate, coherent, usable, original, accessible, and sufficient.

## Per-Period Contract

Every mandatory period should provide reviewable evidence for the following.

| Evidence area | Required observable evidence | Human review question |
| --- | --- | --- |
| Outcome | One observable outcome mapped to one objective or a tightly coupled pair. | Is the outcome worthwhile and achievable in the allotted period? |
| Readiness and recovery | A short readiness check and an explicit route to prerequisite review, retry, or help. | Does the recovery route address the likely prerequisite gap? |
| Concept model | A language- and tool-independent representation of the central state, flow, relationship, or decision. | Is the model accurate and cognitively manageable? |
| Reasoned example | At least one worked example that exposes decisions, plus a contrasting error or non-example where relevant. | Does the reasoning transfer beyond the example? |
| Guided attempt | A supported learner attempt with feedback, including one misconception-targeted attempt. | Does support fade without creating a hidden leap? |
| Independent transfer | A task using a different context, dataset, representation, or input. | Does it require transfer rather than recall? |
| Exit artifact | A visible product or response and a continue / review / seek-help decision. | Is the decision rule usable by a novice and a teacher? |
| Teacher operation | Timing, materials, expected responses, feedback moves, accessibility fallback, stopping point, and extension. | Can a teacher operate and adapt the period safely? |
| Self-study equivalence | Two staged hints, a full explanation, success criteria, a retry or remediation route, and a mastery decision. | Can a learner recover without an answer-first path? |

Multi-session projects may satisfy the contract through milestone artifacts,
criteria, evidence, recovery paths, and revision decisions instead of repeating
uniform prose sections in every period.

## Visual Evidence

- Use an original figure only when it carries instructional meaning.
- Every meaningful image requires specific alt text and a complete text, table,
  data, or ordered-step equivalent in the learning flow.
- Do not rely on color alone. The equivalent must preserve labels,
  relationships, direction, values, and the conclusion learners are expected to
  inspect.
- Figures must use the offline `figure:NAME.svg` Markdown target. `NAME.svg`
  resolves under `site/assets/figures/`; nested names are allowed only when they
  stay within that directory.
- Figure evidence must remain available in classroom lessons, self-study
  lessons, teacher pages, both book views, and both PDF editions.

## Practice and Feedback

- A hint is not a shortened answer. Hint 1 should orient attention or recall a
  prerequisite; Hint 2 may narrow the method while leaving the final work to the
  learner.
- When an answer has `hints`, it must contain exactly two non-empty Japanese
  learner-facing strings.
- Self-study output uses answer-neutral learner checks before hints and answers.
  Teacher rubric descriptions, internal record IDs, and point values remain
  review-only unless a task explicitly teaches a separately reviewed scoring model.
- Strict-pilot problem records define two to four task-specific `learner_checks`.
  These checks describe required reasoning or evidence without containing the
  canonical result. Generic question-type checks are only a fallback for older
  non-pilot records while their content is deepened.
- Classroom output must not expose answer records, hints, rubric criteria, review
  metadata, verification evidence, or internal answer/problem/rubric IDs.

## Claims and Sources

Externally checkable factual, legal, statistical, standards, and technical
claims require claim-level review evidence or an explicit open question. This
ledger is separate from publisher-feature comparison. Publisher pages are not
educational source records and must not supply wording, examples, datasets,
exercise logic, diagrams, layouts, teacher guidance, or answers.

Use the following review-facing ledger fields when a lesson introduces such a
claim. The ledger may be a concise Markdown table in the teacher/review evidence
for the lesson.

| Field | Required content |
| --- | --- |
| Claim locator | Stable lesson ID plus heading, table row, example, or figure name. |
| Exact claim | The bounded claim being checked, not a whole-section summary. |
| Claim type | `factual`, `legal`, `statistical`, `standard`, `technical`, `deterministic calculation`, `methodological guidance`, or `artifact observation`. The last two project-authored evidence types do not replace external sources for externally checkable claims. |
| Evidence | Canonical source ID and exact section, page, clause, or deterministic command. |
| Check | Review date, reviewer role, and `supported`, `needs_revision`, or `open_question`. |
| Scope note | Jurisdiction, version, date range, assumptions, or limits needed to avoid overclaiming. |

Publisher-feature observations must never appear in this ledger as support for
an educational claim.

## Audit Semantics

`scripts/audit_lesson_depth.py` reports every canonical lesson. Missing evidence
is a warning for the 32-lesson baseline and an error for the Issue #91 pilots
`A3`, `B5`, `C1`, and `D2`. A clean structural report means only that named
evidence was found. It never changes lifecycle status and never replaces
pedagogy, accessibility, factual, copyright, classroom-timing, or learner-trial
review.
