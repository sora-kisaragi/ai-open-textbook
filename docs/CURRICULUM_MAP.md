# Curriculum Map: Information I Programming Basics v0.1

Status: `draft`
Review status: `needs_human_review`

This map covers the MVP planning baseline accepted for follow-up work.
It is for open educational material planning only. It does not claim official
textbook status, final curriculum alignment, copyright clearance, or release
approval.

## Scope

- Stage: Japanese high school
- Subject: Information I
- Unit: Programming Basics
- MVP lessons: Variables and assignment, Conditionals, Loops

## Lesson Sequence

| Order | Lesson ID | Title | Main objective | Depends on |
| --- | --- | --- | --- | --- |
| 1 | `lesson.info1.programming.variables.v1` | Variables and Assignment | Store and update named values. | None |
| 2 | `lesson.info1.programming.conditionals.v1` | Conditionals | Choose actions using Boolean conditions. | Variables and assignment |
| 3 | `lesson.info1.programming.loops.v1` | Loops | Repeat actions with a clear stopping condition. | Conditionals |

Dependency graph:

```text
lesson.info1.programming.variables.v1
  -> lesson.info1.programming.conditionals.v1
  -> lesson.info1.programming.loops.v1
```

## Lesson Details

### Variables and Assignment

Objectives:

- Explain why variables are useful.
- Assign a value to a variable in Python.
- Predict the value of a variable after simple assignments.

Prerequisites:

- Basic idea of a computer program as ordered instructions.
- Basic arithmetic expressions.

Key concepts:

- Variable
- Assignment statement
- Stored value
- Updating a value
- Output with `print`

Related records:

- `data/collections/lessons.ndjson`
- `lessons/highschool_information_i/programming/01_variables.md`

### Conditionals

Objectives:

- Explain how a conditional chooses between actions.
- Write a simple `if` statement using a Boolean condition.
- Trace which branch runs for a given input value.

Prerequisites:

- Variables and assignment.
- Comparing simple values.

Key concepts:

- Boolean expression
- Comparison operator
- `if` statement
- `else` branch
- Control flow

Related records:

- Planned lesson record in `data/collections/lessons.ndjson` for Issue #5.

### Loops

Objectives:

- Explain why loops are useful for repeated actions.
- Trace a fixed-count loop and describe how the loop variable changes.
- Write a simple loop with a clear stopping condition.

Prerequisites:

- Variables and assignment.
- Conditionals and Boolean conditions.

Key concepts:

- Iteration
- Loop body
- Loop variable
- Fixed-count loop
- Condition-controlled loop
- Stopping condition

Related records:

- Planned lesson record in `data/collections/lessons.ndjson` for Issue #6.

## Review Notes

- Alignment statements must be reviewed by a human maintainer.
- Pedagogy review must confirm age fit and cognitive load before lesson drafts
  move beyond `draft`.
- Copyright review must confirm original wording and exercises before release.
- Accessibility review must confirm examples do not rely on color alone and use
  inclusive assumptions.
