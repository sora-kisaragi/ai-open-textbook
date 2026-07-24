# Information I Integration Dossier

## Purpose

This dossier records the Issue 81 classroom and self-study candidate integration.
It is review evidence only. It does not mark the curriculum or any content
approved, published, release-ready, stable, or finally curriculum-aligned.

## Roadmap State

The candidate is a stacked continuation of Draft PRs #85, #86, #87, and #88.
Those prerequisite changes are not deferred; they must be reviewed and merged
in order before the Issue 81 integration can be merged. Issues #59 and #81
remain open for the final human gate.

## Integrated Contract

- 32 learner lessons each include one language-independent transfer probe.
- 32 teacher guides cover all 66 mandatory 50-minute periods. Every period has
  a learner outcome, stopping point, and observable continue condition.
- Mandatory unit periods are A=11, B=12, C=21, and D=22. Their shares are 16.7%, 18.2%, 31.8%, and 33.3%.
- A7, B7, C9, and D9 remain the four multi-session performance tasks. Each retains one optional feedback and revision period.
- The recommended classroom route is 70 periods: 66 mandatory and four project
  extensions. Diagnosis and targeted reteaching are embedded in lesson routes.
- All 96 objective coverage entries received a semantic evidence review. The
  audit retains 95 `complete` entries and keeps D6.O2 `partial` until a second
  direct assessment artifact exists. The per-objective
  record is in `docs/review/INFORMATION_I_COVERAGE_AUDIT.md`.
- Machine verification is required for code answers and `predict_output`
  answers. Eight additional integrated responses are allowed only because
  their evidence executes a bounded deterministic exemplar. Other qualitative
  responses must not claim machine verification.

## Verification Boundary

The integration checker verifies the transfer, schedule, period-balance,
performance-task, coverage-structure, and answer-verification contracts.
`check_examples.py` executes bounded Python evidence. Qualitative correctness,
age fit, classroom timing, accessibility on representative devices, copyright
interpretation, and curriculum interpretation remain human decisions.

## Edition Inspection

The static-site verifier passed with 32 classroom lesson pages, 32 self-study
lesson pages, 32 teacher pages, 140 self-study answer reveals, and two complete
book views. Representative transfer and teacher-schedule sections were
inspected at 1440 x 1000 and 390 x 844 without horizontal page overflow.

The classroom PDF passed at 228 A4 pages with no answer feedback. The self-study
PDF passed at 313 A4 pages with 140 answer-feedback sections. Representative
pilot and project pages were rendered with Poppler and visually checked. The D9
transfer-heading orphan and a D2 self-study feedback orphan were corrected and
re-rendered with their related content kept together.

## Final Human Gate

Human maintainers must decide whether the stacked roadmap is acceptable,
whether the 66-period sequence is workable, whether transfer tasks and stopping
points fit the intended learners, whether assessment and copyright decisions
are appropriate, and whether lifecycle status should advance. No lifecycle
status is advanced by this dossier.
