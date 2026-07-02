# MVP Scope: Information I — Programming Basics (v0.1)

Status: `draft` — accepted by the project owner on 2026-07-02 as the
working MVP planning baseline for Issues #2 and #3.
This project is an open educational material / supplemental resource.
It is not an official government-approved textbook, and no final curriculum
alignment claim is made here. This acceptance is not final publication
approval, official curriculum alignment approval, copyright clearance, or
stable release approval.

## 1. Target

- Stage: Japanese high school
- Subject: Information I
- Unit: Programming Basics
- Lessons (fixed set for v0.1):
  1. Variables and assignment
  2. Conditionals
  3. Loops

## 2. In scope for v0.1

- Curriculum map for the three lessons (objectives, prerequisites, key
  concepts, lesson dependency graph), marked as needing human review.
- Lesson requirements and student-facing lesson drafts for the three lessons
  (`lessons/`, `data/collections/lessons.ndjson`).
- Teacher guide drafts for the three lessons (`teacher_guides/`), positioned
  as supplemental support material.
- MVP problem bank limited to the three lessons, with separated problem,
  answer, and rubric records and original content only.
- Answer/rubric versioning workflow (revision and supersession fields).
- Validation and index workflow (`scripts/validate_ndjson.py`,
  `scripts/build_sqlite_index.py`) with generated-only `build/` artifacts.
- Unified pedagogy / copyright / accessibility review checklist usable in PRs.
- Release checklist for a v0.1 public preview.

## 3. Out of scope for v0.1

- Other programming topics: functions, lists/arrays, data structures,
  algorithms beyond basic control flow, external libraries.
- Other Information I units (information design, networks, data analysis,
  information society and ethics).
- Full problem bank beyond the counts to be agreed in Issue #7.
- Localization or translation of source materials (English-first workflow).
- Interactive execution environments, auto-graders, LMS integration.
- Official curriculum compliance claims of any kind.
- License policy changes.
- Any `approved` or `published` status without human review.

## 4. Release boundary

| Stage | Meaning | Entry conditions |
|---|---|---|
| Draft | Work-in-progress content and records | Records exist with status `draft`; IDs follow `AGENTS.md` rules; validation passes |
| Review candidate | Ready for human review | Definition of done artifacts exist (lesson, teacher guide, problems, answers, rubrics, revisions); status `machine_checked` then `human_review_requested`; review checklist attached |
| Public preview (v0.1) | First public release | All human review gates passed; status `approved`; release notes include non-official disclaimer and copyright/source notes; human sets `published` |

## 5. Human review gates

Per `AGENTS.md`, human approval is required for:

- Curriculum alignment statements (Issue #2 output).
- Age-appropriateness and pedagogy decisions (lessons, problems).
- Copyright-risk decisions and source attribution.
- Accessibility acceptance (alt text, color independence, inclusive examples).
- Transition from `approved` to `published` (release itself).
- License changes (declared out of scope for v0.1; any exception needs a
  governance decision).
- Sensitive social topics (not expected in this programming unit; gate applies
  if any example touches one).

Machine validation must pass before any human review is requested
(Operating Rule 7). Machine checks never replace human review.

## 6. Dependency order for Issues #2–#12

```
#1 (this scope)
├─> #2 curriculum map ──> #4 lesson 01 ─> #5 lesson 02 ─> #6 lesson 03
├─> #3 schema/validation ─┬─> #8 answer/rubric versioning
│                         └─> #11 export/index workflow
└─> #10 review checklist
#4,#5,#6 ──> #7 problem bank design ─> #8
#4,#5,#6 ──> #9 teacher guide requirements
#7,#8,#9,#10,#11 ──> #12 release checklist
```

Suggested execution order: #2 and #3 in parallel, then #4 -> #5 -> #6,
then #7 and #9 in parallel, then #8, #10, #11, finally #12.
(#10 may start any time after #1.)

## 7. Risk table

| Risk | Description | Mitigation |
|---|---|---|
| Pedagogy | Lessons too dense for first-time programmers; prerequisite gaps between lessons | Fixed lesson order, misconception lists required, `pedagogy-reviewer` pass, human gate |
| Copyright | Unintentional similarity to existing textbooks or paid problem books | Original wording/exercises only, `copyright-reviewer` pass, no unverified citations, human gate |
| Accessibility | Examples relying on color, missing alt text, culturally narrow scenarios | Checklist from Issue #10 applied in every content PR (Operating Rule 8) |
| Data model | Silent answer/rubric overwrites; broken references between records | Versioning workflow (Issue #8), revision records required, reference checks in validation |
| Validation | Generated index edited by hand or drifting from NDJSON | `build/` treated as disposable and generated-only; rebuild in CI; failures reported, never hidden |

## 8. Acceptance criteria for closing Issue #1

- [x] This document reviewed and accepted by a human maintainer.
- [x] In-scope lesson set confirmed as exactly: variables, conditionals, loops.
- [x] Out-of-scope list confirmed (or explicitly amended with rationale).
- [x] Release boundary stages accepted as the working definition for v0.1.
- [x] Human review gates confirmed against `AGENTS.md`.
- [x] Dependency order accepted for Issues #2–#12.
- [x] No official-textbook claim anywhere in the document.

## Open questions

- Problem counts and difficulty distribution per lesson (decided in Issue #7).
- Pseudocode style vs. a specific language for examples (human decision;
  affects Issues #4–#7).
- Whether v0.1 public preview includes teacher guides or ships them as beta.
- Prerequisite baseline for Lesson 01 (what is assumed vs. taught: expressions,
  data types, basic I/O) — to be captured in the Issue #2 curriculum map.

Remaining open decisions are delegated to the follow-up issues listed above.
