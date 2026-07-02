---
title: "Design the MVP problem bank"
labels: ["phase:mvp", "type:problem-bank", "subject:information-i", "status:needs-human-review"]
status: draft
---

## Purpose

Plan exercises for the three MVP lessons. Design only — do not generate the full bank yet.

## Acceptance criteria

- [ ] Problem counts per lesson and difficulty level are proposed (e.g., basic/standard/advanced per lesson).
- [ ] Each problem requires answer and rubric separation (`prob.*`, `ans.*`, `rubric.*` records).
- [ ] Common mistakes and feedback requirements are specified per problem type.
- [ ] Machine-checkable problem types are identified (e.g., output prediction, fill-in with exact match).
- [ ] Non-machine-checkable items require human review.
- [ ] All problems must be original; no copying or imitation of existing problem books.

## Dependencies

- Blocked by: drafts 04, 05, 06.
- Blocks: drafts 08, 12.

## Suggested agent routing

- `problem-writer` (Sonnet-class) for design; `copyright-reviewer` (Opus-class) for originality criteria.

## Review gates

- `status:needs-human-review`; originality check required.
