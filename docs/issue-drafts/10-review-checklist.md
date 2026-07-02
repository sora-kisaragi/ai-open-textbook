---
title: "Define pedagogy, copyright, and accessibility review checklist"
labels: ["phase:mvp", "type:review", "risk:pedagogy", "risk:copyright", "risk:accessibility"]
status: draft
---

## Purpose

Create one unified review checklist for the MVP release, usable in PR reviews.

## Acceptance criteria

- [ ] Pedagogy checklist covers age fit, cognitive load, and prerequisite gaps.
- [ ] Copyright checklist covers originality, quotation risk, and source attribution (per `docs/COPYRIGHT_POLICY.md` and Operating Rule 5).
- [ ] Accessibility checklist covers alt text, color independence, and inclusive examples (per `docs/ACCESSIBILITY_POLICY.md` and Operating Rule 8).
- [ ] Checklist can be used in PR reviews (fits `docs/REVIEW_GUIDE.md` and PR template).

## Dependencies

- Blocked by: draft 01.
- Blocks: draft 12.

## Suggested agent routing

- `pedagogy-reviewer` and `copyright-reviewer` (Opus-class) for criteria; `release-editor` for integration.

## Review gates

- Maintainer approval of the checklist itself.
