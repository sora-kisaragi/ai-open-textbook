# Lesson 01 Requirements: Variables and Assignment

Status: `draft`
Review status: `needs_human_review`

This document defines requirements only. It does not rewrite the existing
seed lesson, create new problems, create answers or rubrics, update NDJSON
records, or claim official curriculum alignment.

## Metadata

- Issue: #4
- Last updated: 2026-07-03
- Scope type: requirements only
- Output status: `draft`
- Human decisions applied:
  - MVP v0.1 uses Python as the project-level example language.
  - `print` and simple arithmetic expressions are taught minimally as tools
    for observing variable values.
  - `input()` and detailed type discussion are out of scope for MVP Lesson 01.

## Planned Lesson ID

- Lesson record ID: `lesson.info1.programming.variables.v1`
- Existing body path: `lessons/highschool_information_i/programming/01_variables.md`
- Planned title: Variables and Assignment
- Planned stage: high school
- Planned subject: Information I
- Planned unit: Programming Basics
- Planned locale: English source workflow

## Status

- Requirements status: `draft`
- Existing seed lesson status: `draft`
- Required review status before content expansion: `needs_human_review`
- Content expansion in this task: none
- Data changes in this task: none

## Dependencies and Blocked Issues

- Blocked by: Issues #2 and #3, represented by
  `docs/CURRICULUM_MAP.md`, `docs/DATA_MODEL.md`, and
  `scripts/validate_ndjson.py` on `main`.
- Blocks: Issues #5, #7, and #9.
- Related decisions: Python is the MVP example language by project decision,
  not by an official curriculum requirement.

## Learning Objectives

Lesson 01 requirements must support learners who can:

- Explain that a variable is a name used to store and later use a value.
- Assign a value to a variable in Python.
- Reassign a variable and trace how its stored value changes.
- Predict the current value of one or more variables after a short sequence of
  assignment statements.
- Use `print` minimally to observe a variable value after assignment.

## Prerequisites

### Assumed

- Basic computer operation, such as using a keyboard and reading text on a
  screen.
- Basic idea that a program is a sequence of instructions.
- No prior programming experience.

### Taught in This Lesson

- Python assignment syntax with `=`.
- Variable names as labels for stored values.
- Reassignment as updating the stored value.
- Simple arithmetic expressions only when needed to observe updates such as
  adding a small number.
- `print(...)` as a minimal observation tool.

## Scope Boundaries

### In Scope

- Creating a variable by assigning a value in Python.
- Reading and tracing simple assignment statements.
- Reassigning a variable based on its current value.
- Using short, executable Python examples.
- Mentioning simple numeric and text values only when needed for examples.

### Out of Scope

- `input()`.
- Detailed data-type taxonomy or conversion rules.
- Boolean logic beyond a brief warning that `=` and `==` are different.
- Functions, lists, loops, conditionals, files, libraries, and error handling
  beyond the narrow variable-use mistakes listed here.

## Required Lesson Sections

The later student-facing lesson body should include:

- Introduction: why programs need named stored values.
- Worked examples: assignment, reassignment, and observing a value with
  `print`.
- Common mistakes: equality reading, naming confusion, unassigned variables,
  and stale-value tracing.
- Practice references: links to `prob.info1.variables.*` records after the
  problem bank is generated.
- Summary: variable, assignment, reassignment, and tracing takeaways.

## Example Constraints

- Use Python for executable examples.
- Keep examples short enough to trace by hand.
- Use only simple values and simple arithmetic.
- Introduce `print` before using it in examples.
- Avoid `input()`, nested control flow, hidden state, external files, network
  calls, and culturally dependent contexts.

## Misconceptions to Address

- Reading `=` as mathematical equality instead of assignment.
- Assuming a variable name is the same as the stored value.
- Forgetting that reassignment replaces the previous value.
- Using a variable before assigning it.
- Confusing similar variable names.
- Treating `==` as an assignment operator.

## Problem-Bank Hooks

- Problem ID pattern: `prob.info1.variables.NNN.v1`.
- Planned MVP target: 8 Lesson 01 problems.
- Planned difficulty distribution: basic 4, standard 3, advanced 1.
- Candidate machine-checkable types: predict output, fill in exact,
  multiple choice, trace table.
- Candidate human-reviewed types: short conceptual explanation, error
  identification and correction, free-code writing.
- Every problem must later reference separate `ans.*` and `rubric.*` records.
- Do not generate new problems in this task.

## Teacher-Guide Hooks

- Teacher guide dependency: Issue #9.
- Teacher guide should later explain how to introduce `print` and simple
  arithmetic without assuming prior programming knowledge.
- Teacher guide should flag the `=` versus `==` distinction as a future bridge
  to conditionals.
- Do not generate teacher guide content in this task.

## Data-Record Plan

- Existing lesson record: `lesson.info1.programming.variables.v1`.
- Existing body file:
  `lessons/highschool_information_i/programming/01_variables.md`.
- Later problem records should use `prob.info1.variables.NNN.v1`.
- Later answer records should use `ans.prob.info1.variables.NNN.v1`.
- Later rubric records should use `rubric.prob.info1.variables.NNN.v1`.
- Non-trivial future data changes must append records to
  `data/collections/revisions.ndjson`.
- This requirements document does not change NDJSON records.

## Gaps From Existing Seed Assets

Only gaps are listed here; this task does not rewrite the seed assets.

### Seed Lesson Body

- The existing prerequisite list includes basic arithmetic expressions, but
  the current requirement treats simple arithmetic as taught minimally inside
  Lesson 01.
- `print` appears in the first worked example, but the requirement needs it to
  be explicitly introduced as an observation tool before use.
- The existing lesson does not yet include a separate summary section.
- The existing lesson has self-check questions, but it does not yet provide
  practice references to `prob.info1.variables.*` records.
- The self-check that uses `name = "Aki"` and `name == "Aki"` may invite more
  string or equality detail than Lesson 01 should cover.

### Existing Lesson Record

- The record ID and status already match the required pattern and draft state.
- The `prerequisites` field is empty, so the basic-operation and no-prior-
  programming baseline is not represented in data.
- The objectives mention assignment and prediction, but do not explicitly call
  out reassignment/tracing as a requirement.
- The record currently points to a source reference; any future curriculum
  wording must avoid official-alignment claims unless reviewed by a human.

### Existing Sample Problems

- There are only two seed problems, both basic; the MVP target is eight Lesson
  01 problems with basic 4, standard 3, and advanced 1.
- Existing problem types do not yet cover the full planned mix of predict
  output, fill in exact, multiple choice, trace table, conceptual explanation,
  error correction, and free-code writing.
- Existing common-mistake metadata is useful but not yet systematic across the
  planned problem set.

### Existing Answers

- Answer records are separated from problems and remain in `draft` with
  `needs_human_review`, which matches the workflow.
- Machine-check status is inconsistent across the two seed answers; later work
  should define when code answers are executed or manually reviewed.
- Feedback expectations for common mistakes are not yet represented as a
  complete answer/rubric strategy.

### Existing Rubrics

- Rubric records are separated and in `draft`, which matches the workflow.
- Current rubrics are minimal and do not yet cover the full range of tracing,
  explanation, error-correction, and free-code-writing criteria planned for
  the MVP problem bank.
- Later rubrics should align with the difficulty distribution and
  machine-checkable versus human-reviewed problem type decisions.

## Pedagogy / Copyright / Accessibility Risks

- Pedagogy: learners may read assignment as equality or may be overloaded if
  `print`, arithmetic, strings, and equality are introduced too quickly.
- Copyright: examples and future problems must be original and must not imitate
  textbook or paid problem-book wording.
- Accessibility: examples should not rely on color, wealth, family structure,
  regional knowledge, or inaccessible visual-only cues.

## Human Review Gates

- Requirements review before expanding the lesson body.
- Pedagogy review for no-prior-programming fit and cognitive load.
- Copyright review before any student-facing examples or problems are treated
  as review candidates.
- Accessibility review for examples, practice prompts, and any future diagrams.
- Data/schema review before modifying lesson, problem, answer, rubric, or
  revision records.

## Open Questions

- Whether future Lesson 01 data should explicitly store prerequisite text or
  keep prerequisites only in requirements until lesson records are revised.
- How much `==` discussion should remain in Lesson 01 versus being deferred to
  Lesson 02.
- Whether Lesson 01 should include a trace table in the lesson body or reserve
  trace tables for practice.
