# MVP Problem Bank Design

Status: `draft`
Review status: `needs_human_review`

This document defines the MVP v0.1 problem-bank design for Issues #4, #5,
#6, and #7. It is design only: it does not generate problem records, answer
records, rubric records, teacher guides, or lesson bodies.

This design remains the lesson-level assessment baseline for C2 through C4 in
the v0.2 full-scope plan. Subject-wide counts and objective coverage are defined
in `docs/INFORMATION_I_COMPLETION_MATRIX.md`; this historical v0.1 document does
not define completeness for the other 29 lessons.

## Scope

- Stage: high school
- Subject: Information I
- Unit: Programming Basics
- Lessons:
  - `lesson.info1.programming.variables.v1`
  - `lesson.info1.programming.conditionals.v1`
  - `lesson.info1.programming.loops.v1`
- Example language: Python, as a project-level MVP decision.

Python is used for executable examples and machine-checkable exercises in this
project. This is not an official curriculum requirement or an official
curriculum alignment claim.

## Fixed MVP Target

The MVP v0.1 problem bank target is fixed at:

| Lesson | Problem target |
| --- | ---: |
| Lesson 01: Variables and assignment | 8 |
| Lesson 02: Conditionals | 8 |
| Lesson 03: Loops | 8 |
| Total | 24 |

This target is a planning limit for the MVP problem bank. It is not permission
to generate the problem bank in this design task.

## Fixed Difficulty Distribution

Per lesson:

| Difficulty | Count |
| --- | ---: |
| basic | 4 |
| standard | 3 |
| advanced | 1 |

Across the full MVP problem bank:

| Difficulty | Count |
| --- | ---: |
| basic | 12 |
| standard | 9 |
| advanced | 3 |
| Total | 24 |

Difficulty labels should be used consistently in `problem` records.

## Problem Type Review Classes

### Machine-Checkable Problem Types

Machine-checkable problems should have deterministic expected outputs or exact
accepted values.

| Type | Machine-check rule | Notes |
| --- | --- | --- |
| predict output | Exact output match | Include whitespace rules when output has multiple lines. |
| fill in exact | Exact text or token match | Keep accepted variants explicit and small. |
| multiple choice | Exact option ID match | Distractors must target known misconceptions. |
| trace table | Exact cell-value match | Use only small tables with clear iteration/state columns. |

### Human-Reviewed Problem Types

Human-reviewed problems require rubric judgment before they can be treated as
review candidates.

| Type | Review need | Notes |
| --- | --- | --- |
| short conceptual explanation | Conceptual accuracy and clarity | Keep prompts narrow. |
| error identification and correction | Correct diagnosis plus corrected code or reasoning | Separate diagnosis from correction in rubrics. |
| free-code writing | Functional intent, code clarity, and boundary behavior | Do not assume auto-grading in v0.1. |

## Machine-Checkable Ratio

- Target: at least 60% of the MVP problem bank should be machine-checkable.
- Operational target: at least 15 of 24 problems should be machine-checkable.
- Suggested per-lesson target: at least 5 of 8 problems machine-checkable.

The ratio supports lightweight validation and learner self-checks while keeping
space for human-reviewed reasoning and code-writing tasks.

## Lesson-Level Planning Matrix

This matrix defines volume targets only. It does not define problem prompts.

| Lesson | Basic | Standard | Advanced | Machine-checkable target | Human-reviewed target |
| --- | ---: | ---: | ---: | ---: | ---: |
| Variables and assignment | 4 | 3 | 1 | at least 5 | up to 3 |
| Conditionals | 4 | 3 | 1 | at least 5 | up to 3 |
| Loops | 4 | 3 | 1 | at least 5 | up to 3 |
| Total | 12 | 9 | 3 | at least 15 | up to 9 |

## Lesson-Specific Coverage Hooks

### Lesson 01: Variables and Assignment

- Include assignment, reassignment, and tracing stored values.
- Treat `print` and simple arithmetic as minimally taught observation tools.
- Keep `input()` and detailed type discussion out of scope.
- Use `prob.info1.variables.NNN.v1` IDs.

### Lesson 02: Conditionals

- Include single branch, two-way branch, and minimal `elif`.
- Include boundary-value reasoning.
- Include risks around `=` versus `==`, overlapping conditions, and Python
  indentation/block structure.
- Use `prob.info1.conditionals.NNN.v1` IDs.

### Lesson 03: Loops

- Include fixed-count loops and condition-controlled loops.
- Require trace-table style reasoning for loop state.
- Keep nested loops out of MVP scope unless explicitly marked optional in a
  later reviewed artifact.
- Use `prob.info1.loops.NNN.v1` IDs.

## Answer and Rubric Separation Rules

Every problem record must reference separate answer and rubric records:

- Problem record: `prob.info1.<lesson-slug>.NNN.v1`
- Answer record: `ans.prob.info1.<lesson-slug>.NNN.v1`
- Rubric record: `rubric.prob.info1.<lesson-slug>.NNN.v1`

Rules:

- `problem` records contain prompts, lesson references, difficulty,
  question type, answer references, rubric references, and common mistakes.
- `answer` records contain canonical answers, accepted variants when needed,
  explanations, review status, verification status, source references, rubric
  references, and revision metadata.
- `rubric` records contain scoring criteria and review criteria.
- Answers and rubrics must not be embedded only in problem text.
- If an answer or rubric changes meaningfully, add a new version or update with
  revision history according to `docs/DATA_MODEL.md`; do not silently overwrite
  educational truth.

## Common Mistake and Feedback Requirements

Every problem should define common mistakes before answer/rubric generation.

| Problem type | Required common-mistake focus | Feedback requirement |
| --- | --- | --- |
| predict output | skipped assignment, stale value, wrong branch, wrong iteration count | Explain the trace step where the error occurs. |
| fill in exact | wrong operator, wrong variable name, missing update, syntax mismatch | State the exact expected form and why variants are or are not accepted. |
| multiple choice | plausible misconception for each distractor | Explain why the correct option works and why each distractor fails. |
| trace table | missing row, wrong condition value, off-by-one row, stale variable value | Identify the first incorrect cell and the rule used to derive it. |
| short conceptual explanation | vague term use, equality/assignment confusion, branch/loop confusion | Rubric should separate concept accuracy from wording quality. |
| error identification and correction | correct output but wrong diagnosis, partial correction, new introduced error | Rubric should score diagnosis and correction separately. |
| free-code writing | code works only for one case, unclear names, missing boundary behavior | Rubric should distinguish behavior, readability, and scope fit. |

## Originality Constraints

- Problems, answers, explanations, distractors, and rubrics must be original.
- Do not copy, closely paraphrase, or imitate existing textbooks, paid problem
  books, proprietary diagrams, hidden teacher manuals, answer keys, or
  proprietary educational content.
- Do not invent citations or source references.
- Do not use examples that require personal data, secrets, network calls,
  file-system side effects, or culturally narrow background knowledge.
- Copyright and source discipline require human review before release-scope
  decisions.

## ID Scheme

Use lowercase, dot-separated, version-aware IDs.

| Artifact | Pattern | Example |
| --- | --- | --- |
| Lesson | `lesson.info1.programming.<lesson-slug>.v1` | `lesson.info1.programming.variables.v1` |
| Problem | `prob.info1.<lesson-slug>.NNN.v1` | `prob.info1.variables.001.v1` |
| Answer | `ans.prob.info1.<lesson-slug>.NNN.v1` | `ans.prob.info1.variables.001.v1` |
| Rubric | `rubric.prob.info1.<lesson-slug>.NNN.v1` | `rubric.prob.info1.variables.001.v1` |

Lesson slugs:

- `variables`
- `conditionals`
- `loops`

Numbering rules:

- Use three-digit sequence numbers.
- Keep IDs unchanged after human review starts unless a versioned replacement
  is created.
- Do not renumber existing reviewed records for cosmetic reasons.
- Use a new version suffix when superseding an educational artifact.

## Validation and Record-Volume Implications

This design implies the following eventual record volume for the MVP problem
bank:

| Collection | Target record count for problem bank |
| --- | ---: |
| `data/collections/problems.ndjson` | 24 problem records |
| `data/collections/answers.ndjson` | 24 answer records |
| `data/collections/rubrics.ndjson` | 24 rubric records |
| `data/collections/revisions.ndjson` | At least one revision per created or meaningfully changed record |

Additional implications:

- Existing Lesson 01 seed problem, answer, and rubric records may count toward
  the target only after they are reviewed against the Lesson 01 requirements.
- If seed records need meaningful changes, preserve revision history rather
  than silently overwriting them.
- `scripts/validate_ndjson.py` must verify required fields, status values,
  answer/rubric references, and supersession references.
- `scripts/build_sqlite_index.py` must rebuild `build/index.sqlite` from
  NDJSON; generated SQLite remains disposable and must not be hand-edited.
- Problem-bank changes must include revision records for non-trivial data
  changes.

## Required Generation Order

Generate artifacts in this order:

1. Lesson requirements first.
2. Lesson records and body files before generated problems.
3. Problems before answers and rubrics.
4. Answers and rubrics after problem IDs and prompt scope are fixed for review.
5. Revisions for non-trivial data changes.
6. Validation and generated index rebuild before requesting human review.

This order prevents orphan answer/rubric records and reduces prompt drift
between lessons, problems, and review criteria.

## Human Review Items

- Confirm whether teacher guides are included in the v0.1 public preview or
  handled as beta support material.
- Confirm whether existing Lesson 01 seed problems count toward the 24-problem
  target after review.
- Confirm the exact machine-checkable type mix per lesson before generation.
- Confirm whether trace-table problems use exact table-cell matching or a
  narrower output format.
- Confirm originality and copyright-risk review before any generated problem
  set is sent for human review.

## Out of Scope for This Design Task

- Generating the 24 problems.
- Creating answer records.
- Creating rubric records.
- Creating teacher guides.
- Creating Lesson 02 or Lesson 03 student-facing lesson bodies.
- Adding or modifying NDJSON records.
- Changing license policy.
