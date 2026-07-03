# Lesson 02 Requirements: Conditionals

Status: `draft`
Review status: `needs_human_review`

This document defines requirements only. It does not create a student-facing
lesson body, lesson record, problem record, answer, rubric, or teacher guide.
It does not claim official curriculum alignment.

## Metadata

- Issue: #5
- Last updated: 2026-07-03
- Scope type: requirements only
- Output status: `draft`
- Human decision applied: MVP v0.1 uses Python as the project-level example
  language.

## Planned Lesson ID

- Planned lesson record ID: `lesson.info1.programming.conditionals.v1`
- Planned body path:
  `lessons/highschool_information_i/programming/02_conditionals.md`
- Planned title: Conditionals
- Planned stage: high school
- Planned subject: Information I
- Planned unit: Programming Basics
- Planned locale: English source workflow

## Status

- Requirements status: `draft`
- Student-facing lesson body: not started
- Data records: not started
- Required review status before content drafting: `needs_human_review`

## Dependencies and Blocked Issues

- Blocked by: Issues #2, #3, and #4.
- Blocks: Issues #6, #7, and #9.
- Lesson dependency: `lesson.info1.programming.variables.v1`.
- Related decision: Python is the MVP example language by project decision,
  not by an official curriculum requirement.

## Learning Objectives

Lesson 02 requirements must support learners who can:

- Explain that a conditional chooses which statements run based on a Boolean
  condition.
- Write and trace a single-branch Python `if` statement.
- Write and trace a two-way Python `if` / `else` statement.
- Recognize a minimal Python `elif` form as an else-if branch.
- Use simple comparison operators in Boolean conditions.
- Predict which branch runs for boundary and non-boundary values.

## Prerequisites

### Assumed

- Lesson 01 variables and assignment.
- Reassignment and tracing short sequences of statements.
- Reading simple numeric values.

### Taught in This Lesson

- Boolean conditions as expressions that evaluate to true or false.
- Python comparison operators needed for examples, including `==`, `!=`, `<`,
  `<=`, `>`, and `>=`.
- Python indentation and block structure for conditionals.
- Minimal `elif` as the Python form of else-if.

## Scope Boundaries

### In Scope

- Single-branch `if`.
- Two-way `if` / `else`.
- Minimal `elif` with a small number of mutually exclusive cases.
- Simple numeric comparisons and boundary-value checks.
- Short branch traces that can be followed by hand.

### Out of Scope

- Deeply nested conditionals.
- Complex Boolean algebra and long compound conditions.
- Truthiness rules beyond explicit Boolean comparisons.
- Pattern matching, exceptions, functions, lists, files, libraries, and user
  input workflows.
- Claims that Python syntax is required by an official curriculum.

## Required Lesson Sections

The later student-facing lesson body should include:

- Introduction: why programs need choices.
- Worked examples: single branch, two-way branch, and minimal `elif`.
- Common mistakes: assignment versus equality, overlapping conditions,
  boundary values, indentation, and block structure.
- Practice references: links to `prob.info1.conditionals.*` records after the
  problem bank is generated.
- Summary: condition, branch, block, and trace takeaways.

## Example Constraints

- Use Python for executable examples.
- Scope examples to single branch, two-way branch, and minimal `elif`.
- Keep nested conditionals out of examples unless an optional note passes human
  review.
- Keep examples short enough to trace without tools.
- Use neutral, culturally independent scenarios and simple numeric values.
- Avoid examples that depend on personal data, sensitive traits, wealth,
  region, family structure, or school-specific policies.

## Misconceptions to Address

- Using `=` when `==` is needed in a condition.
- Treating overlapping conditions as if only one can ever be true without
  checking the branch order.
- Missing boundary values such as exactly equal to a threshold.
- Misreading which statements belong to a branch because of indentation.
- Assuming `else` has its own condition.
- Adding nested conditionals before the learner can trace simple branches.

## Problem-Bank Hooks

- Problem ID pattern: `prob.info1.conditionals.NNN.v1`.
- Planned MVP target: 8 Lesson 02 problems.
- Planned difficulty distribution: basic 4, standard 3, advanced 1.
- Candidate machine-checkable types: predict output, fill in exact,
  multiple choice, trace table.
- Candidate human-reviewed types: short conceptual explanation, error
  identification and correction, free-code writing.
- Every problem must later reference separate `ans.*` and `rubric.*` records.
- Do not generate new problems in this task.

## Teacher-Guide Hooks

- Teacher guide dependency: Issue #9.
- Teacher guide should later give strategies for teaching indentation as
  structure, not styling.
- Teacher guide should include prompts for checking boundary-value reasoning.
- Do not generate teacher guide content in this task.

## Data-Record Plan

- Later lesson record: `lesson.info1.programming.conditionals.v1`.
- Later body file:
  `lessons/highschool_information_i/programming/02_conditionals.md`.
- Later problem records should use `prob.info1.conditionals.NNN.v1`.
- Later answer records should use `ans.prob.info1.conditionals.NNN.v1`.
- Later rubric records should use `rubric.prob.info1.conditionals.NNN.v1`.
- Non-trivial future data changes must append records to
  `data/collections/revisions.ndjson`.
- This requirements document does not change NDJSON records.

## Pedagogy / Copyright / Accessibility Risks

- Pedagogy: nesting, compound conditions, and indentation can create excess
  cognitive load if introduced before learners can trace simple branches.
- Copyright: examples and future problems must be original and must not imitate
  textbook or paid problem-book wording.
- Accessibility: examples should not depend on color alone, local institutional
  rules, or culturally narrow contexts.

## Human Review Gates

- Requirements review before creating the lesson body.
- Pedagogy review for nesting limits, boundary-value load, and indentation
  explanation.
- Copyright review before student-facing examples or problems are treated as
  review candidates.
- Accessibility review for scenarios and any future diagrams.
- Data/schema review before adding conditionals records.

## Open Questions

- Whether `elif` should be required in the main lesson body or kept as a short
  extension after single and two-way branches.
- How much compound-condition syntax should be deferred to a later non-MVP
  lesson.
- Whether boundary-value practice should use trace tables, multiple choice, or
  both in the MVP problem bank.
