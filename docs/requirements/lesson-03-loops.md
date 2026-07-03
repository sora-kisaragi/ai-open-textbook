# Lesson 03 Requirements: Loops

Status: `draft`
Review status: `needs_human_review`

This document defines requirements only. It does not create a student-facing
lesson body, lesson record, problem record, answer, rubric, or teacher guide.
It does not claim official curriculum alignment.

## Metadata

- Issue: #6
- Last updated: 2026-07-03
- Scope type: requirements only
- Output status: `draft`
- Human decision applied: MVP v0.1 uses Python as the project-level example
  language.

## Planned Lesson ID

- Planned lesson record ID: `lesson.info1.programming.loops.v1`
- Planned body path: `lessons/highschool_information_i/programming/03_loops.md`
- Planned title: Loops
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

- Blocked by: Issues #2, #3, and #5.
- Blocks: Issues #7 and #9.
- Lesson dependencies:
  - `lesson.info1.programming.variables.v1`
  - `lesson.info1.programming.conditionals.v1`
- Related decision: Python is the MVP example language by project decision,
  not by an official curriculum requirement.

## Learning Objectives

Lesson 03 requirements must support learners who can:

- Explain that a loop repeats a block of statements.
- Trace a fixed-count loop and describe how the loop variable changes.
- Trace a condition-controlled loop and identify the stopping condition.
- Use a trace-table style explanation to track loop state across iterations.
- Recognize common loop errors such as off-by-one conditions and missing
  updates.

## Prerequisites

### Assumed

- Lesson 01 variables, assignment, and reassignment.
- Lesson 02 conditionals, Boolean conditions, comparisons, and indentation.
- Ability to trace short sequences of Python statements.

### Taught in This Lesson

- Iteration as repeated execution.
- Loop body and loop state.
- Fixed-count loop with a short Python `for` / `range(...)` pattern.
- Condition-controlled loop with a short Python `while` pattern.
- Trace-table style reasoning for loop variables, conditions, and outputs.

## Scope Boundaries

### In Scope

- Fixed-count loops.
- Condition-controlled loops.
- Short loops with one main changing value.
- Trace tables that show iteration number, relevant variable values, condition
  result, and any output.
- Clear stopping conditions.

### Out of Scope

- Nested loops, except as explicitly optional and human-reviewed.
- Lists, arrays, strings as sequences, file loops, graphics, libraries, and
  event loops.
- `break`, `continue`, `else` on loops, comprehensions, generators, recursion,
  and advanced `range` patterns.
- Long simulations or examples with many changing variables.
- Claims that Python syntax is required by an official curriculum.

## Required Lesson Sections

The later student-facing lesson body should include:

- Introduction: why programs need repetition.
- Worked examples: fixed-count loop and condition-controlled loop.
- Common mistakes: off-by-one errors, infinite loops, missing updates,
  indentation, and loop-variable confusion.
- Practice references: links to `prob.info1.loops.*` records after the problem
  bank is generated.
- Summary: loop, loop body, loop state, stopping condition, and trace-table
  takeaways.

## Example Constraints

- Use Python for executable examples.
- Keep examples short enough to trace by hand.
- Use trace-table style explanation for loop state.
- Use simple counters or small accumulations only when needed.
- Avoid nested loops in MVP examples unless explicitly marked optional and
  reviewed by a human.
- Avoid examples that depend on external files, network calls, personal data,
  sensitive traits, wealth, region, or culturally narrow contexts.

## Misconceptions to Address

- Off-by-one errors in loop ranges or stopping conditions.
- Forgetting to update a value used by a `while` condition.
- Creating an infinite loop by using a condition that never becomes false.
- Misreading which statements belong to the loop body because of indentation.
- Assuming the loop variable keeps every previous value rather than one current
  value at a time.
- Trying nested loops before mastering single-loop traces.

## Problem-Bank Hooks

- Problem ID pattern: `prob.info1.loops.NNN.v1`.
- Planned MVP target: 8 Lesson 03 problems.
- Planned difficulty distribution: basic 4, standard 3, advanced 1.
- Candidate machine-checkable types: predict output, fill in exact,
  multiple choice, trace table.
- Candidate human-reviewed types: short conceptual explanation, error
  identification and correction, free-code writing.
- Every problem must later reference separate `ans.*` and `rubric.*` records.
- Do not generate new problems in this task.

## Teacher-Guide Hooks

- Teacher guide dependency: Issue #9.
- Teacher guide should later describe how to scaffold trace tables before
  asking learners to write loops.
- Teacher guide should flag infinite-loop prevention and example length as
  classroom safety and cognitive-load concerns.
- Do not generate teacher guide content in this task.

## Data-Record Plan

- Later lesson record: `lesson.info1.programming.loops.v1`.
- Later body file:
  `lessons/highschool_information_i/programming/03_loops.md`.
- Later problem records should use `prob.info1.loops.NNN.v1`.
- Later answer records should use `ans.prob.info1.loops.NNN.v1`.
- Later rubric records should use `rubric.prob.info1.loops.NNN.v1`.
- Non-trivial future data changes must append records to
  `data/collections/revisions.ndjson`.
- This requirements document does not change NDJSON records.

## Pedagogy / Copyright / Accessibility Risks

- Pedagogy: tracing multiple changing values across iterations can overload
  learners; examples must stay short and use trace tables.
- Copyright: examples and future problems must be original and must not imitate
  textbook or paid problem-book wording.
- Accessibility: trace tables should be readable as text and should not depend
  on color alone.

## Human Review Gates

- Requirements review before creating the lesson body.
- Pedagogy review for trace-table load, loop length, and nested-loop exclusion.
- Copyright review before student-facing examples or problems are treated as
  review candidates.
- Accessibility review for trace tables and any future diagrams.
- Data/schema review before adding loop records.

## Open Questions

- Whether condition-controlled loops should use only `while` in the main lesson
  body or also compare the idea with fixed-count loops conceptually.
- Whether the first loop examples should show output each iteration or focus on
  state changes before output.
- Whether nested loops should be excluded entirely from v0.1 rather than listed
  as optional extension material.
