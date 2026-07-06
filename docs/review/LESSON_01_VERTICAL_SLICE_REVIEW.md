# Lesson 01 Vertical Slice Review Evidence

Status: `human_review_requested`
Review status: `needs_human_review`
Related issue: #41

This document prepares the existing Lesson 01 vertical slice for human review.
It does not generate new learner-facing content, new problems, new answers, or
new rubrics. It does not approve, publish, stabilize, or release any material.

## Existing Assets

| Asset type | Existing asset | Status or review state |
| --- | --- | --- |
| Lesson record | `lesson.info1.programming.variables.v1` in `data/collections/lessons.ndjson` | `human_review_requested` |
| Lesson body | `lessons/highschool_information_i/programming/01_variables.md` | Referenced by the lesson record |
| Teacher guide | `teacher_guides/highschool_information_i/programming/01_variables.md` | Existing seed guide; not referenced from the lesson record schema |
| Problem | `prob.info1.variables.001.v1` | `human_review_requested` |
| Problem | `prob.info1.variables.002.v1` | `human_review_requested` |
| Answer | `ans.prob.info1.variables.001.v1` | `human_review_requested`; `review_status: needs_human_review`; `verification_status: not_run` |
| Answer | `ans.prob.info1.variables.002.v1` | `human_review_requested`; `review_status: needs_human_review`; `verification_status: machine_checkable` |
| Rubric | `rubric.prob.info1.variables.001.v1` | `human_review_requested` |
| Rubric | `rubric.prob.info1.variables.002.v1` | `human_review_requested` |
| Source reference | `src.mext.curriculum.general.v1` | Draft source record for curriculum-alignment review; no final alignment claim |
| Revision records | `rev.20260702.0001` through `rev.20260702.0008`; `rev.20260706.0001` through `rev.20260706.0007` | Creation history plus review-request events |

## Requirements Gap Analysis

Compared source: `docs/requirements/lesson-01-variables.md`.

### Covered Requirements

- The lesson record uses the planned ID
  `lesson.info1.programming.variables.v1`.
- The lesson body path matches the planned existing body path.
- The body introduces variables as names for stored values.
- The body includes Python assignment syntax with `=`.
- The body includes `print(...)` as an observation tool in a short example.
- The body includes reassignment through `x = x + 1`.
- The body includes common mistakes for assignment-as-equality and using an
  unassigned variable.
- The two seed problems use the `prob.info1.variables.NNN.v1` ID pattern.
- Problems reference separate answer and rubric records.
- Answers remain separate from problems and keep
  `review_status: needs_human_review`.
- Rubrics remain separate from problems and answers.

### Partial Coverage

- The lesson objectives cover usefulness, assignment, and prediction, but they
  do not explicitly name reassignment or tracing one or more variables.
- The lesson body uses `print(...)` before a separate introductory section
  explains it as an observation tool.
- The prerequisite list names basic arithmetic expressions, while the
  requirements treat simple arithmetic as taught minimally inside the lesson.
- The teacher guide includes lesson intent, flow, misconceptions, and
  formative assessment, but it does not yet cover all teacher-guide
  requirements for timing, feedback strategy, accessibility, and copyright
  source discipline.
- Problem coverage includes one short-code prompt and one predict-output
  prompt, but not the full planned type mix.

### Missing Requirements

- The lesson body does not include a separate summary section.
- The lesson body does not include practice references to
  `prob.info1.variables.*` records.
- The lesson record has an empty `prerequisites` field and does not represent
  the no-prior-programming baseline.
- The vertical slice has 2 Lesson 01 seed problems, not the planned 8 Lesson
  01 MVP problems.
- The existing problems are both `basic`; the planned Lesson 01 distribution
  is basic 4, standard 3, advanced 1.
- The seed problem set does not yet include multiple choice, trace table,
  short conceptual explanation, error identification and correction, or
  free-code writing.

### Blocking Gaps

- Human review is still required for pedagogy, age fit, cognitive load,
  copyright/source risk, accessibility, and maintainer acceptance.
- The existing two seed problems cannot be marked accepted or countable until
  Lesson 01 vertical-slice review is completed by a human reviewer.
- `ans.prob.info1.variables.001.v1` has `verification_status: not_run`, so its
  answer and accepted variant need reviewer or machine-check evidence before
  acceptance.
- `ans.prob.info1.variables.002.v1` is machine-checkable in type, but it still
  needs actual reviewer or machine-run evidence before acceptance.

### Non-Blocking Gaps

- The missing summary, practice references, fuller teacher-guide treatment,
  and broader problem-type mix can be handled in later content-generation or
  review-follow-up work because this task is review preparation only.
- The lesson-record prerequisite field can remain unchanged for this PR
  because changing it would be content/data expansion beyond the review-request
  status transition.

### Open Maintainer Questions

- Should Lesson 01 data later store prerequisite text directly, or keep it in
  requirements until a broader lesson-record update?
- How much `==` discussion should remain in Lesson 01 versus being deferred to
  Lesson 02?
- Should the lesson body include a trace table, or should trace tables remain
  in practice only?
- Should lesson records later add an explicit teacher-guide reference field?

## MVP Review Checklist Evidence

Checklist source: `docs/review/MVP_REVIEW_CHECKLIST.md`.

| Review area | Evidence | Review result |
| --- | --- | --- |
| Non-official status | Repository rules and this review document frame the work as open educational material and do not claim official textbook status. | Pass for review preparation; final curriculum alignment remains human-gated. |
| Pedagogy / age fit | Lesson targets high school Information I beginners and keeps examples short. Known risks are assignment-as-equality, early `print(...)`, arithmetic, string, and `==` load. | Human review required. |
| Prerequisite fit | The body lists ordered instructions and arithmetic expressions; requirements assume no prior programming and teach arithmetic only minimally. | Partial; maintainer decision needed. |
| Cognitive load | Existing examples are short, but `print`, arithmetic, strings, and equality comparison appear early. | Human review required before acceptance. |
| Copyright/source risk | Existing records have no copied source text identified during this review. The lesson record references `src.mext.curriculum.general.v1` only for draft curriculum review. | Copyright review still required. |
| Accessibility | Text-only examples do not rely on color, images, audio, or inaccessible visual cues. No personal data is required. | Accessibility review still required. |
| Data/model consistency | IDs, required fields, references, status values, and revision records are validated by `scripts/validate_ndjson.py`. | Machine validation passed. |
| Answer/rubric separation | Problem records reference separate answer and rubric records; answers and rubrics are not embedded only in problem text. | Pass for review preparation. |
| Prose quality | This evidence document was checked with the warning-only prose script. Warnings, if any, are review prompts only. | Machine prose check passed. |
| Review gates | Human review remains required for pedagogy, copyright/source risk, accessibility, answer correctness, rubric fit, seed-problem counting, and maintainer acceptance. | Required before acceptance. |

## Status and Revision Decisions

Existing repository rules allow `human_review_requested` as a lifecycle status.
`docs/MVP_SCOPE.md` defines a review candidate as existing lesson, teacher
guide, problems, answers, rubrics, revisions, machine checks, and checklist
evidence. This PR therefore moves only the existing Lesson 01 lesson, problem,
answer, and rubric records from `draft` to `human_review_requested`.

The records move directly from `draft` to `human_review_requested` because the
required machine checks were executed and recorded in this PR. This
review-preparation transition does not retain a separate `machine_checked`
state and does not approve, accept, publish, or release any record.

No learner-facing text, problem prompt, answer content, accepted answer,
rubric criterion, source record, schema, or generated artifact is edited by
hand.

Revision records added:

- `rev.20260706.0001` for `lesson.info1.programming.variables.v1`
- `rev.20260706.0002` for `prob.info1.variables.001.v1`
- `rev.20260706.0003` for `prob.info1.variables.002.v1`
- `rev.20260706.0004` for `ans.prob.info1.variables.001.v1`
- `rev.20260706.0005` for `ans.prob.info1.variables.002.v1`
- `rev.20260706.0006` for `rubric.prob.info1.variables.001.v1`
- `rev.20260706.0007` for `rubric.prob.info1.variables.002.v1`

## Seed Problem Counting

The existing Lesson 01 seed problems are candidate countable seed problems
pending human review:

- `prob.info1.variables.001.v1`
- `prob.info1.variables.002.v1`

They may count toward the 24-problem MVP target only after human review
confirms they satisfy the Lesson 01 requirements, problem-bank design, answer
and rubric separation, copyright/source expectations, accessibility
expectations, and review gates. They are not marked accepted, approved,
published, stable, verified, or release-ready in this PR.

## Validation Evidence

Commands run for this PR:

- `python scripts/validate_ndjson.py` - passed.
- `python scripts/build_sqlite_index.py` - passed.
- `python -m pytest` - passed.
- `python scripts/check_prose_warnings.py docs/review/LESSON_01_VERTICAL_SLICE_REVIEW.md` - passed with no warnings.
- `git diff --check` - passed.

## Human Review Still Required

- Pedagogy and age-fit review for no-prior-programming learners.
- Cognitive-load review for `print(...)`, arithmetic, strings, and `==`.
- Copyright/source review for lesson text, teacher-guide text, prompts,
  answers, and rubrics.
- Accessibility review for all learner-facing and teacher-facing material.
- Maintainer decision on whether the two seed problems count toward the MVP
  24-problem target after review.
- Maintainer decision on future prerequisite and teacher-guide reference
  fields.
