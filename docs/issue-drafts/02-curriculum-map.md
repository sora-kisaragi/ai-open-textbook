---
title: "Create curriculum map for Programming Basics"
labels: ["phase:mvp", "type:curriculum", "subject:information-i", "status:needs-human-review"]
status: draft
---

## Purpose

Create a concise curriculum map for the three MVP lessons (variables and assignment, conditionals, loops).

## Acceptance criteria

- [ ] Objectives, prerequisites, key concepts, and lesson dependencies are listed for each lesson.
- [ ] Alignment claims are marked as needing human review; no final official curriculum compliance claim is made.
- [ ] Lesson dependency graph is explicit (variables -> conditionals -> loops).
- [ ] Related NDJSON records are identified (`data/collections/lessons.ndjson`, `curriculum/highschool_information_i.curriculum.json`).
- [ ] Output stays `draft` or `human_review_requested`.

## Dependencies

- Blocked by: draft 01.
- Blocks: drafts 04, 05, 06.

## Suggested agent routing

- `curriculum-planner` (Fable-class) for the map; `pedagogy-reviewer` (Opus-class) for review criteria.

## Review gates

- `status:needs-human-review` — alignment statements require human sign-off.
