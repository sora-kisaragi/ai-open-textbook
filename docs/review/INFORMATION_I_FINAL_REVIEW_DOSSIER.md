# Information I Final Review Dossier

Status: `draft`
Review status: `needs_human_review`
Tracking: #59, #66, #74
Evidence date: 2026-07-15

> Planning update, 2026-07-22: This dossier preserves the evidence snapshot
> assembled on 2026-07-15. Issue #74 and PR #82 supersede its 71-77-period band
> with the authoritative v0.3 route of 65 mandatory periods plus five
> recommended extension periods. Current review must use
> `curriculum/highschool_information_i.curriculum.json` and
> `docs/CURRICULUM_MAP.md` for timing and prerequisite decisions.

## Purpose and Decision Boundary

This dossier assembles the machine evidence and specialist findings for the
single final human review gate for the full Japanese Information I Draft PR
stack. It does not approve, publish, stabilize, authorize, or finally align the
material to a curriculum. The human reviewers retain every judgment listed in
the final checklist.

## Candidate Scope

| Measure | Candidate evidence |
| --- | ---: |
| Provisional units | 4 |
| Planned and implemented lessons | 32 / 32 |
| Provisional curriculum objectives | 96 |
| Structurally complete objective coverage rows | 96 / 96 |
| Classroom planning band at evidence date | 71-77 periods of 50 minutes |
| Learner lesson bodies | 32 |
| Teacher guides | 32 |
| Problems / answers / rubrics | 140 / 140 / 140 |
| Active / deprecated source records | 18 / 1 |
| Revision records | 715 |
| Canonical records including curriculum | 1,187 |

The four provisional units are:

1. A: Information society and problem solving, 7 lessons.
2. B: Communication and information design, 7 lessons.
3. C: Computers, algorithms, and programming, 9 lessons.
4. D: Networks, information systems, and data, 9 lessons.

The mapping to current MEXT primary sources is traceable but remains a human
curriculum judgment. The 32 canonical curriculum lesson entries are used as the
maintained requirements source to avoid duplicating them into 32 separate
requirements documents. Human review must confirm that this equivalence and the
lesson decomposition are acceptable.

## Pedagogical Integration

- Python remains the primary executable example language, while the lessons
  introduce transferable models before syntax and provide non-code reasoning
  routes where appropriate.
- B2 now teaches bit-to-byte conversion in the lesson instead of assuming it as
  a prerequisite.
- C6 removes an unintroduced nested conditional from the functions example.
- C7 states its algorithm definition as an explicit project operational model.
- D5 introduces optional dictionary, `None`, `int`, and `append` syntax and
  provides an equivalent non-code route.
- Learner practice is ordered from basic to standard to advanced.
- A7 and B7 performance rubrics split compound criteria into independently
  observable criteria without changing total scoring.
- Every Unit D teacher guide now includes concrete participation and
  accessibility support.
- Potentially real municipality wording was replaced by the explicitly
  fictional project setting `青葉野市`.

## Canonical Data Changes

The integration branch changes these canonical record groups relative to the
Unit D stack head:

- 15 lesson entities: A1, A2, A3, A6, B2, C6, C7, and D1-D8.
- 3 problem entities: the A1 fictional setting and the A7/B7 performance-task
  classifications.
- 2 rubric entities: A7 and B7 performance criteria.
- 1 answer entity: the B7 explanation and in-record revision counter only.
- 15 source entities: one legacy deprecation, nine bounded metadata updates,
  and five new primary-source records.
- 38 append-only revision events: `rev.20260715.0257` through
  `rev.20260715.0294`.

No canonical answer, acceptable answer, answer verification evidence, criteria
ID, total rubric points, stable entity ID, schema key, or lifecycle approval
state changes in this integration branch. The B7 answer remains semantically
unchanged; only its explanation and required in-record revision counter change.

## Source, Rights, and Attribution Boundary

- The legacy broad MEXT source is deprecated in favor of separate normative and
  interpretive records with exact locators.
- PPC, WCAG, RFC 1122, NIST CSF 2.0, SQLite, and Python records now state
  bounded uses and non-claims.
- Python documentation links are pinned to the 3.10 documentation line used by
  the examples; executable behavior is independently checked in the locked
  environment.
- New primary records cover the eight-bit byte convention, Python mappings,
  built-in functions, built-in constants, and the PSF trademark policy.
- The standalone HTML book and PDF include CC BY 4.0 attribution guidance,
  modification guidance, a non-endorsement statement, a Python trademark and
  non-affiliation notice, and an 18-entry active-source bibliography.
- Repository inspection found no copied diagrams, external datasets, personal
  data, decorative images, or substantial source quotations in the candidate.
  This is audit evidence, not a final copyright or legal decision.

Source titles, links, and metadata remain third-party material and are not
relicensed by this project. Source listing does not imply endorsement. Human
review must still decide originality, legal-risk boundaries, trademark wording,
and whether the fictional school name `星見高校` should be retained.

## Delivery and Accessibility Evidence

- Generated output contains 32 learner pages, 32 teacher/reviewer pages, one
  learner-only book, one local stylesheet, and a local content-license copy.
- The static verifier checks exact page sets, navigation and fragment targets,
  local assets, forbidden runtime elements, and learner/reviewer separation.
- The learner book contains no answer IDs, rubric IDs, canonical answers,
  acceptable answers, answer explanations, or verification evidence.
- External URLs are optional citation anchors only. No external script, style,
  image, font, frame, form, or other runtime dependency is present.
- `file://` navigation from the index to the full 32-lesson book succeeds with
  the stylesheet and imprint loaded.
- Automated browser QA covered 10 representative pages at 1440x900 and 390x844:
  index, book, A7, B1, B7, C1, C9, D1, D9, and the D5 teacher page.
- All 20 views passed Japanese language, landmark, heading-count, duplicate-ID,
  horizontal-overflow, license-link, and visible first-Tab-focus checks.
- No external runtime request occurred during the browser pass.

These checks support keyboard and screen-reader-oriented review but do not prove
conformance to WCAG or suitability with every assistive technology.

## PDF and Print Evidence

The pinned Chromium workflow produced a tagged 183-page A4 learner PDF.

| Evidence | Value |
| --- | --- |
| Exact SHA-256 | `61640a56d7939f697ef8a50851cea76d80635ff6eb28435b48540da72d42a64a` |
| Semantic SHA-256 | `340afca75e29bc7f82766a9391e767cf8feac66b380bf23e736cb7d435f22eb2` |
| Book HTML SHA-256 | `da92d0df25b645bf36b121a93da256b42e1d11f6739480c5ab10c84f38785a15` |
| Stylesheet SHA-256 | `f4c946623e8f7c2b9947125f5f7a63059cbc221e096bef9dfd68f301812426f0` |
| Renderer | Playwright 1.61.0 / Chromium 149.0.7827.55 / pypdf 6.14.2 |

All 183 pages were rendered to PNG and reviewed as ten contact sheets. Enlarged
checks covered the cover, table of contents, all four unit boundaries, a long
code page, a representative lesson, and all three license/source pages. No
blank content page, clipping, overlap, broken table, unreadable code, missing
glyph, or malformed source entry was observed. This visual pass remains subject
to final human print review.

## Validation Evidence

The final command ledger is recorded after the integration branch is frozen.
The required gate is:

```text
uv run python scripts/check_revision_history.py --base-ref 9e852fa
uv run python scripts/validate_ndjson.py
uv run python scripts/build_sqlite_index.py
uv run python scripts/check_examples.py
uv run python scripts/build_static_site.py
uv run python scripts/verify_static_site.py
uv run python scripts/build_pdf.py
uv run python -m pytest
uv run python scripts/check_prose_warnings.py
git diff --check
```

Local final-snapshot results, repeated on the resulting commit before push:
revision history passed against
`9e852fa`; 1,187 canonical records validated; SQLite projected 32 lessons, 96
objectives, 96 complete coverage rows, and 2,300 edges; 32 lesson blocks, 10
problem blocks, and 7 code-answer variants executed; the site verifier accepted
32 learner pages, 32 teacher pages, and one book; the PDF verifier accepted 183
tagged A4 pages; and 89 tests passed. The full default prose scan emitted 37
warning-only prompts in pre-existing prose-tooling evaluation and issue-draft
documents. The changed-file prose scan emitted zero warnings. CI must repeat the
required gates on the pushed commit.

Generated content under `build/` and QA captures under `tmp/` remain ignored and
must not be committed.

## Draft PR Stack and Squash Procedure

Merge order:

1. #67 `docs/60-information-i-architecture` -> `main`
2. #68 `feat/61-textbook-tooling` -> #67 branch
3. #69 `content/62-unit-a-information-society` -> #68 branch
4. #70 `content/63-unit-b-information-design` -> #69 branch
5. #71 `content/64-unit-c-programming` -> #70 branch
6. #72 `content/65-unit-d-networks-data` -> #71 branch
7. Final integration PR `integration/66-information-i-review-candidate` -> #72 branch

Repository policy requires squash merges. After human approval, merge #67 first.
Before each subsequent squash merge, rebase only that PR's delta onto current
`origin/main` with `git rebase --onto origin/main <previous-stack-head> <branch>`,
force-push with lease, retarget the PR to `main`, rerun CI, and confirm the diff
contains only that PR's intended scope. Repeat in order. Do not delete a parent
stack branch until its immediate child has been restacked successfully.

## Final Human Review Checklist

- [ ] Confirm the 4-unit, 32-lesson decomposition and the current 65-period
      mandatory route plus five recommended extension periods.
- [ ] Confirm the provisional MEXT mapping and the canonical-curriculum-as-
      requirements decision.
- [ ] Review Japanese accuracy, age fit, cognitive load, examples, and progression.
- [ ] Review all performance tasks, scoring criteria, and workload expectations.
- [ ] Review accessibility with keyboard, screen reader, zoom/reflow, contrast,
      print, and classroom accommodation scenarios.
- [ ] Review source locators, legal/ethical boundaries, originality, CC BY 4.0
      attribution, PSF trademark wording, and fictional names.
- [ ] Review the 183-page PDF on target printers and representative devices.
- [ ] Confirm each stacked PR diff and CI result immediately before its squash.
- [ ] Decide separately whether any content may transition beyond conservative
      draft or human-review-requested states.
- [ ] Authorize any public preview, release, publication, or curriculum claim only
      through a separate explicit decision.

Non-blocking maintenance after the review candidate includes refreshing the
package description that still refers to the repository starter. It has no
effect on canonical educational data or generated textbook behavior.
