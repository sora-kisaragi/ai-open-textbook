# Information I Review Candidate Scope (v0.2)

Status: `draft`
Review status: `needs_human_review`
Last updated: 2026-07-14
Tracking issue: #59

This document is the current planning baseline for a complete Japanese
Information I open educational material. It replaces the programming-only v0.1
MVP boundary as the active plan. The v0.1 decision remains available in Git
history and its completed Lesson 01 artifacts remain valid inputs.

This is not an official textbook, a publication decision, or a final curriculum
alignment claim. All curriculum, pedagogy, accessibility, copyright, and release
judgments remain subject to the final human review gate.

## 1. Target

- Stage: Japanese high school
- Subject: Information I
- Audience: first-time learners, classroom trial users, and self-study learners
- Educational language: Japanese
- Repository and review language: English
- Example programming language: Python, used to demonstrate transferable ideas
- Delivery: offline static HTML plus reproducible print/PDF output

## 2. Primary Scope Evidence

The provisional boundary is derived from two distinct MEXT primary sources:

- `src.mext.highschool.curriculum2018.v1`: normative High School Course of Study
- `src.mext.information.commentary2018.v1`: interpretive Information commentary

The four provisional content areas are:

1. Information society and problem solving
2. Communication and information design
3. Computers and programming
4. Information networks and data use

Exact source locations and project interpretations are recorded in
`docs/INFORMATION_I_COMPLETION_MATRIX.md`. Source use supports traceability but
does not constitute human-approved alignment.

## 3. Planned Curriculum

The review candidate contains 32 lessons:

| Unit | Lessons | Unit outcome |
| --- | ---: | --- |
| Information society and problem solving | 7 | Define an information-related problem, identify constraints and responsibilities, compare solutions, and evaluate evidence. |
| Communication and information design | 7 | Design, test, and improve an accessible information artifact for a defined audience and purpose. |
| Computers, algorithms, and programming | 9 | Explain computation, trace and create programs, compare algorithms, and use models and simulations to solve problems. |
| Networks, information systems, and data | 9 | Explain networked services and security, then collect, manage, analyze, and communicate data with stated limitations. |

The stable lesson IDs, objectives, prerequisites, dependencies, key concepts,
assessment intent, and source references are canonicalized in
`curriculum/highschool_information_i.curriculum.json`.

Objective IDs are lowercase, version-aware, and independent of display order.
Planning labels such as `C2.O3` may change when navigation changes, but canonical
objective IDs and their assessment history must remain stable.

The curriculum assumes everyday experience with digital information, basic
arithmetic, and basic chart reading. Required mathematical ideas are refreshed
where they are used, and no prior programming is assumed. The current time model
is 70-76 classroom periods of 50 minutes, with separate self-study estimates and
four multi-session performance tasks. These are planning bands for human review,
not official allocations.

## 4. Required Vertical Slice Per Lesson

Each lesson must include:

- A requirements document with measurable objectives and explicit prerequisites.
- A Japanese learner lesson with introduction, examples or worked analysis,
  common mistakes, practice, self-check, and summary.
- A Japanese supplemental teacher guide with timing bands, prerequisite checks,
  questions, misconceptions, feedback, assessment points, and accessibility notes.
- A lesson record and at least four aligned problem records unless a documented
  performance task provides equivalent objective coverage.
- Separate answer and rubric records for every problem.
- Revision events for every created or non-trivially changed NDJSON entity.
- Source references for curriculum, legal, factual, dataset, or standard-dependent
  claims; stable demonstrated facts do not receive ornamental citations.

The existing programming lessons for variables, conditionals, and loops retain
the earlier target of eight problems each. The full-scope minimum is therefore
140 problems unless a later reviewed assessment design changes the count.
This count is a capacity floor, not evidence that every objective is adequately
assessed; objective-level coverage remains the controlling completion measure.

## 5. Programming Pedagogy

Python is the default executable example language, not the learning goal by
itself. Programming lessons should normally progress through:

1. A language-independent concept or problem.
2. A trace, model, diagram, or structured procedure.
3. A short executable Python example.
4. A clear note identifying Python-specific syntax.
5. Practice that checks transfer beyond copying syntax.

Examples must be short enough to trace, deterministic where intended, and free
from unintended network, file-system, secret, or personal-data dependencies.

## 6. Delivery Requirements

- Generated learner pages must not expose answers, rubrics, verification evidence,
  review metadata, or internal IDs as primary labels.
- Teacher/reviewer pages must remain visibly separate and must not imply access
  control where none exists.
- The site must work offline, use no runtime CDN, and provide responsive, keyboard,
  screen-reader-oriented, and print-readable structure.
- Meaningful diagrams must be original, have alt text, and include an equivalent
  text explanation.
- Generated HTML, SQLite, PDF, and other artifacts remain under `build/` and are
  not edited or committed by hand.

## 7. Out of Scope

- Information II and specialist Information subjects.
- Official approval or final curriculum-alignment claims.
- Automatic transition to `approved` or `published`.
- LMS integration, accounts, learner analytics, remote code execution, or grading
  services.
- Copying or close imitation of textbooks, paid problem books, proprietary
  diagrams, teacher manuals, interfaces, or answer keys.
- Broad legal advice or unsupported statements about current law.

## 8. Workflow and Human Gate

Issues #60 through #66 implement this scope as an ordered stack of small Draft
PRs. Existing Issues #46 and #56 are reused. Autonomous work may draft, validate,
and review the complete stack, but it must not merge the stack, close Issue #59,
or mark any record approved or published.

The single final human gate covers:

- Curriculum interpretation and scope sufficiency.
- Pedagogy, age fit, accessibility, and inclusive examples.
- Copyright, quotation, source, dataset, asset, and legal-risk decisions.
- Teacher-guide classroom timing and assessment usability.
- Ordered PR approval and merge.
- Any later public-preview or publication decision.

## 9. Review-Candidate Completion

Completion is demonstrated only when:

- All 32 planned lesson packages and their mapped assessment coverage exist.
- Every objective is assessed by at least two items or one item plus a performance
  task with a reviewed rubric.
- All records, IDs, references, generated links, examples, and outputs validate.
- Offline HTML and print/PDF output pass desktop, mobile, accessibility-oriented,
  and visual inspection.
- Specialist review has no unresolved machine-detectable or clearly actionable
  blocker.
- The complete Draft PR stack is pushed and listed in merge order on Issue #59.
- Remaining decisions are explicitly reserved for the final human gate.

Passing these criteria does not itself approve or publish the material.
