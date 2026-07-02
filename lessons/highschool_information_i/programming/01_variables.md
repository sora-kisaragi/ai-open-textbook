# Variables and Assignment

## Learning goals

After this lesson, learners can:

1. Explain why variables are useful.
2. Assign a value to a variable in Python.
3. Predict the value of a variable after simple assignments.

## Prerequisites

- Basic idea of a computer program as ordered instructions.
- Basic arithmetic expressions.

## Introduction

A program often needs to remember values.
A variable gives a name to a value so that the program can use it later.

## Example

```python
score = 80
print(score)
```

The variable `score` stores the value `80`.
The `print` function displays the current value of `score`.

## Common mistakes

### Mistake: Reading assignment as equality

```python
x = x + 1
```

In mathematics, this looks impossible as an equation.
In Python, it means: compute the current value of `x + 1`, then store the result back into `x`.

### Mistake: Using a variable before assigning it

```python
print(total)
```

This fails if `total` has not been assigned earlier.

## Self-check

- What is the value of `x` after `x = 3` and `x = x + 2`?
- Why is `name = "Aki"` different from `name == "Aki"`?
