# Teacher Guide Requirements for MVP Programming Lessons

Status: `draft`
Review status: `needs_human_review`
Related issue: #9
Scope: requirements only; no teacher-guide body generation

This document defines requirements for future teacher-facing guidance for the
three MVP programming lessons. Teacher guides are supplemental support material
for open educational materials. They are not official guidance and must not be
described as official curriculum direction.

## Purpose

Define requirements for teacher-facing guidance that supports the three MVP
programming lessons:

- Variables and assignment.
- Conditionals.
- Loops.

These requirements should guide later teacher-guide drafts, review, and
integration. They do not create teacher-guide body content, lesson body
content, problem records, answer records, rubric records, schema changes, or
lesson-record changes.

## Applicable MVP Lessons

| Lesson | Lesson record status | Lesson requirement source |
| --- | --- | --- |
| Variables and assignment | Existing draft record: `lesson.info1.programming.variables.v1` | `docs/requirements/lesson-01-variables.md` |
| Conditionals | Planned record: `lesson.info1.programming.conditionals.v1` | `docs/requirements/lesson-02-conditionals.md` |
| Loops | Planned record: `lesson.info1.programming.loops.v1` | `docs/requirements/lesson-03-loops.md` |

Future teacher guides must remain aligned with the lesson sequence in
`docs/CURRICULUM_MAP.md`: variables before conditionals, then loops.

## Common Teacher-Guide Requirements

Every future teacher guide for the MVP programming lessons must include these
requirements before it can move beyond draft review.

| Requirement area | Required treatment |
| --- | --- |
| Lesson flow | Provide a suggested sequence for introducing the lesson idea, working examples, guided practice, misconception checks, and formative assessment. |
| Suggested teacher questions | Include question types that reveal learner reasoning, not only final answers. Questions should support prediction, tracing, explanation, and error diagnosis. |
| Timing guidance | Provide flexible timing bands for introduction, worked examples, practice, and assessment. Timing must remain draft until pedagogy review confirms classroom fit. |
| Assessment points | Identify formative checkpoints connected to the lesson objectives and later problem-bank targets. |
| Student misconceptions | List expected misconceptions from the relevant lesson requirements and connect each misconception to a feedback strategy. |
| Feedback strategies | Require feedback that points to the first trace step, condition, assignment, or loop-state decision where learner reasoning diverges. Avoid generic correctness-only feedback. |
| Prerequisite checks | Include quick checks for required prior knowledge and state whether a gap should be remediated inside the lesson or deferred. |
| Accessibility and inclusive examples | Require examples and teacher prompts that do not rely on color alone, visual-only cues, personal data, sensitive traits, wealth, family structure, region, or culturally narrow background knowledge. |
| Copyright/source discipline | Require original wording and original classroom prompts. Do not copy, closely paraphrase, or imitate textbooks, paid problem books, proprietary teacher manuals, answer keys, or hidden instructional materials. Do not invent citations. |
| Human review gates | Require human review before teacher-guide drafting from these requirements and again before any public-preview use. Pedagogy, copyright/source, accessibility, and release-scope decisions remain human-gated. |

## Lesson-Specific Requirements

### Lesson 01: Variables and Assignment

Expected lesson flow requirements:

- Start from the need for a named stored value.
- Introduce Python assignment with `=` before asking learners to trace updates.
- Introduce `print(...)` as a minimal observation tool before using it in
  examples.
- Move from assignment to reassignment and then to short prediction tasks.

Suggested question type requirements:

- Prediction questions for current variable values after each statement.
- Trace questions that ask when a value changes.
- Explanation questions about why assignment is not mathematical equality.
- Error-diagnosis questions for unassigned variables or stale-value reasoning.

Timing considerations:

- Reserve time for learners to say predictions before code is run.
- Keep arithmetic and `print(...)` explanation short so they support the
  variable objective rather than becoming separate topics.
- Treat detailed type discussion and `input()` as out of scope.

Assessment checkpoints:

- Learner can assign a value in Python.
- Learner can predict the current value after reassignment.
- Learner can explain that reassignment replaces the previous stored value.

Misconceptions to address:

- Reading `=` as mathematical equality.
- Treating the variable name as the stored value.
- Forgetting that reassignment replaces the prior value.
- Using a variable before assigning it.
- Confusing similar variable names.

Feedback strategy requirements:

- Feedback must identify the exact assignment where the stored value changes.
- Feedback for `=` versus `==` must avoid expanding into full Boolean logic
  before Lesson 02.
- Feedback on wrong predictions should show a short trace, not only the final
  value.

Connection to problem-bank design:

- Align with `prob.info1.variables.NNN.v1` future problem IDs.
- Support predict-output, fill-in-exact, multiple-choice, trace-table, short
  conceptual explanation, error-correction, and free-code-writing problem
  types.
- Keep the MVP target of 8 problems with 4 basic, 3 standard, and 1 advanced
  problem as a planning reference only.

Human review needs:

- Pedagogy review for no-prior-programming fit and cognitive load.
- Copyright/source review for original examples and prompts.
- Accessibility review for neutral scenarios and any future diagrams or
  tables.

### Lesson 02: Conditionals

Expected lesson flow requirements:

- Begin with why programs need choices.
- Introduce Boolean conditions as true-or-false expressions.
- Progress from single-branch `if` to `if` / `else`, then minimal `elif`.
- Make indentation and block structure visible as program structure.
- Use boundary-value checks before learners generate their own conditions.

Suggested question type requirements:

- Branch-prediction questions for given values.
- Boundary questions that include values below, equal to, and above a threshold.
- Explanation questions about why a branch ran.
- Error-diagnosis questions for `=` versus `==`, indentation, and overlapping
  conditions.

Timing considerations:

- Keep nested conditionals out of the core flow.
- Give enough time for learners to trace both taken and not-taken branches.
- Treat compound Boolean expressions as out of scope unless later reviewed.

Assessment checkpoints:

- Learner can trace a single-branch `if`.
- Learner can trace a two-way `if` / `else`.
- Learner can identify which branch runs for boundary and non-boundary values.
- Learner can recognize minimal `elif` as an else-if branch.

Misconceptions to address:

- Using `=` when `==` is needed in a condition.
- Assuming overlapping conditions are automatically exclusive.
- Missing exact boundary values.
- Misreading branch membership because of indentation.
- Assuming `else` has its own condition.

Feedback strategy requirements:

- Feedback must connect branch outcomes to the evaluated Boolean condition.
- Boundary-value feedback must state which comparison result controls the
  branch.
- Indentation feedback must identify which statements belong to the branch
  without treating indentation as mere formatting.

Connection to problem-bank design:

- Align with `prob.info1.conditionals.NNN.v1` future problem IDs.
- Support predict-output, fill-in-exact, multiple-choice, trace-table, short
  conceptual explanation, error-correction, and free-code-writing problem
  types.
- Use distractors and feedback that target branch-order, boundary, equality,
  and indentation misconceptions.

Human review needs:

- Pedagogy review for boundary-value load, `elif` placement, and nesting
  limits.
- Copyright/source review for original examples and prompts.
- Accessibility review for neutral scenarios and readable branch traces.

### Lesson 03: Loops

Expected lesson flow requirements:

- Begin with why programs need repetition.
- Introduce fixed-count loops before or alongside a carefully scaffolded
  condition-controlled loop.
- Use trace tables before asking learners to write loops independently.
- Make loop body, loop state, and stopping condition explicit.
- Keep examples short and avoid nested loops in the MVP core flow.

Suggested question type requirements:

- Iteration-count prediction questions.
- Trace-table questions for loop variable, condition result, and output.
- Explanation questions about the stopping condition.
- Error-diagnosis questions for off-by-one errors, missing updates, infinite
  loops, and indentation.

Timing considerations:

- Reserve time for learners to complete trace tables step by step.
- Keep loops short enough to trace by hand.
- Treat nested loops, `break`, `continue`, comprehensions, recursion, and long
  simulations as out of scope for MVP teacher guidance.

Assessment checkpoints:

- Learner can trace a fixed-count loop.
- Learner can trace a condition-controlled loop.
- Learner can identify the stopping condition.
- Learner can explain an off-by-one or missing-update mistake.

Misconceptions to address:

- Off-by-one errors in ranges or stopping conditions.
- Forgetting to update a value used by a `while` condition.
- Creating a condition that never becomes false.
- Misreading which statements belong to the loop body.
- Assuming a loop variable stores every previous value.

Feedback strategy requirements:

- Feedback must identify the first incorrect row or state in the trace.
- Infinite-loop feedback must connect the issue to the condition and missing or
  ineffective update.
- Off-by-one feedback must compare expected and actual iteration counts.

Connection to problem-bank design:

- Align with `prob.info1.loops.NNN.v1` future problem IDs.
- Support predict-output, fill-in-exact, multiple-choice, trace-table, short
  conceptual explanation, error-correction, and free-code-writing problem
  types.
- Use trace-table and feedback requirements from `docs/PROBLEM_BANK_DESIGN.md`
  as the main bridge between teacher guidance and later assessment records.

Human review needs:

- Pedagogy review for trace-table load, loop length, and exclusion of nested
  loops.
- Copyright/source review for original examples and prompts.
- Accessibility review for text-readable trace tables and non-color-dependent
  cues.

## Output Location Policy

Future teacher-guide body files should be created under `teacher_guides/` and
should mirror the lesson-body path structure:

| Lesson | Expected future teacher-guide path |
| --- | --- |
| Variables and assignment | `teacher_guides/highschool_information_i/programming/01_variables.md` |
| Conditionals | `teacher_guides/highschool_information_i/programming/02_conditionals.md` |
| Loops | `teacher_guides/highschool_information_i/programming/03_loops.md` |

Existing teacher-guide seed file:

- `teacher_guides/highschool_information_i/programming/01_variables.md`

The existing seed file is useful as early draft material, but it needs future
review against this requirements document, the Lesson 01 requirements,
`docs/MVP_REVIEW_CHECKLIST.md`, and the project human review gates. This PR
does not create or modify teacher-guide body files.

## Lesson-Record Reference Policy

Current inspection of `data/collections/lessons.ndjson` found one Lesson 01
record with a `body_ref` field but no explicit teacher-guide reference field.
`schemas/lesson.schema.json` requires `body_ref` and `learning_objectives`; it
does not define a required `teacher_guide_ref` or equivalent field.

Open maintainer decision:

- Decide whether lesson records should add an explicit teacher-guide reference
  field in the future.

Possible future additive approach, not implemented in this PR:

- Add an optional field such as `teacher_guide_ref` for one guide path per
  lesson, or `teacher_guide_refs` if multiple teacher-facing resources are
  expected.
- Keep the field additive and backwards-compatible.
- Update schemas, validation, and lesson records in a separate data/schema PR
  only after maintainer approval.

This PR does not modify `data/collections/lessons.ndjson`, schemas, validators,
or generated indexes beyond running validation commands.

## v0.1 Public Preview Boundary

- Whether full teacher guides are included in the v0.1 public preview remains
  a maintainer decision.
- Teacher-guide publication must not become a hidden requirement for unrelated
  MVP work.
- Teacher guides require human review before any public-preview use.
- Teacher guides must remain supplemental support material and must not be
  described as official guidance.

## Acceptance Criteria Mapping

| Issue #9 acceptance criterion | Document section |
| --- | --- |
| Lesson flow, suggested questions, timing, and assessment points are required per lesson. | `Lesson-Specific Requirements` |
| Student misconceptions are linked to feedback strategies. | `Common Teacher-Guide Requirements` and each lesson subsection |
| Teacher guide is explicitly supplemental support material, not official guidance. | Opening note, `Purpose`, and `v0.1 Public Preview Boundary` |
| Human review gates are listed. | `Common Teacher-Guide Requirements`, lesson-specific human review needs, and `v0.1 Public Preview Boundary` |
| Output location: `teacher_guides/`, referenced from lesson records. | `Output Location Policy` and `Lesson-Record Reference Policy` |

## Open Maintainer Decisions

- Decide whether teacher guides are included in the v0.1 public preview or
  handled as beta support material.
- Decide whether lesson records should add an explicit teacher-guide reference
  field.
- Decide whether timing guidance should assume a standard 45/50-minute lesson
  or remain flexible.
- Decide whether teacher-guide review requires a separate `pedagogy-reviewer`
  pass before content drafting.
