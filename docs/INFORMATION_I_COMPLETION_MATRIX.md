# Information I Completion Matrix

Status: `draft`
Review status: `needs_human_review`
Tracking: #59, #60
Baseline date: 2026-07-14

## Purpose

Provide measurable evidence for subject-wide completeness without confusing
machine completeness with human approval. This matrix is the completion contract
for the autonomous Draft PR stack.

## Baseline and Target

| Artifact | Baseline | Review-candidate target |
| --- | ---: | ---: |
| Planned curriculum lessons | 3 | 32 |
| Requirements documents | 3 | 32 |
| Learner lesson bodies | 1 | 32 |
| Teacher guides | 1 | 32 |
| Canonical lesson records | 1 | 32 |
| Problem records | 2 | At least 140 |
| Answer records | 2 | One or more resolving answers per problem as designed |
| Rubric records | 2 | At least one resolving rubric per problem |
| Source records | 1 generic draft | Distinct claim-appropriate primary sources |
| Executable answer evidence | 2 | Every deterministic executable answer |
| Offline learner pages | 1 | 32 plus complete navigation |
| Offline teacher/reviewer pages | 1 | 32 plus complete navigation |
| Print/PDF workflow | Print CSS QA only | Reproducible full-book PDF with visual QA |

The 140-problem minimum uses four problems for every lesson and preserves the
earlier eight-problem target for C2, C3, and C4. A performance task may assess
multiple objectives, but it still requires an explicit rubric and coverage map.
The number is a capacity floor and does not by itself prove objective coverage.

## Objective Coverage Rule

Every lesson objective must map to:

- At least two assessment items; or
- One assessment item plus one performance task criterion.

Coverage must distinguish recall, explanation or tracing, application, and
evaluation where the objective requires them. Passing record validation does not
prove objective coverage.

Objectives use stable lowercase canonical IDs independent of display order, such
as `obj.info1.programming.variables.003.v1`. Labels such as `A1.O1` and `C2.O3`
are navigation aids only. Coverage is recorded as `not_started`, `partial`, or
`complete`; only `complete` satisfies the rule above. Assessment-item references
and performance-criterion references are stored separately and must resolve to
their problem and rubric records. One item may support multiple objectives only
when the required evidence for each objective is explicit in its prompt and
rubric.

## Unit Completion

| Unit | Lessons | Learner content | Teacher support | Assessment | Integration |
| --- | ---: | --- | --- | --- | --- |
| A. Information society and problem solving | 7 | 0/7 | 0/7 | 0/7 packages | 0/1 inquiry task |
| B. Communication and information design | 7 | 0/7 | 0/7 | 0/7 packages | 0/1 design task |
| C. Computers, algorithms, and programming | 9 | 1/9 | 1/9 | 1/9 partial packages | 0/1 programming task |
| D. Networks, information systems, and data | 9 | 0/9 | 0/9 | 0/9 packages | 0/1 investigation task |

Lesson C2 currently has one learner body, one teacher guide, two problems, two
answers, and two rubrics. It remains incomplete against the full-scope assessment
target and must not be counted as approved. Its current records provide partial
evidence for `C2.O2` and `C2.O3`; `C2.O1` remains `not_started`.

## Instructional Time Baseline

| Measure | Planning total |
| --- | ---: |
| Classroom periods (50 minutes) | 70-76 |
| Self-study time | 2,665-4,200 minutes |
| Multi-session performance tasks | 4 |

The four performance tasks are A7, B7, C9, and D9. Time bands are design inputs
for teacher review and learner trials, not official allocations or evidence that
the planned workload is age-appropriate. The 70-period route is the core plan;
the six-period upper-range allowance supports extension, reteaching, and longer
project feedback. Ordinary lesson assessment is included, while school events
and local examinations require separate scheduling buffer.

## Source Traceability

| Source ID | Role | Required use | Must not be used as |
| --- | --- | --- | --- |
| `src.mext.highschool.curriculum2018.v1` | Normative curriculum boundary | Claims that Information I includes an objective or content area | Ready-made learner prose, lesson order, or project approval |
| `src.mext.information.commentary2018.v1` | Interpretive commentary | Interpretation and planning notes with exact section/page | A substitute for the normative document or text to paraphrase closely |
| Claim-specific official sources | Legal, standards, statistics, datasets | Current factual or legal claims and externally supplied data | Decorative citations or implied legal advice |
| Official Python documentation plus execution | Python behavior | Language-specific behavior not proven by a local deterministic check alone | Curriculum evidence |

Drafting must begin from independently stated objectives and close the source
before writing learner prose. Official area names may be used, but source sentence
order, examples, and explanation structure must not be imitated.

## Machine Evidence Required Per PR

- `python scripts/validate_ndjson.py`
- `python scripts/build_sqlite_index.py`
- `python scripts/build_static_site.py`
- `python -m pytest`
- Relevant `python scripts/check_prose_warnings.py ...`
- Execution checks for changed runnable examples
- Generated link, offline asset, and learner answer-leakage checks
- `git diff --check`
- Desktop, mobile, accessibility-oriented DOM, keyboard, and print visual QA when
  rendering changes or generated pages are in scope

## Final Human-Only Evidence

- The 32-lesson decomposition is sufficient and appropriately sequenced.
- Curriculum interpretations and source locators support the stated mapping.
- Japanese prose, examples, workload, timing, and assessment are age-appropriate.
- Accessibility is adequate for release-scope content.
- Copyright, quotation, dataset, asset, trademark, and legal-risk findings are
  acceptable.
- The Draft PR stack may be merged in the listed order.
- Any public preview, approval, or publication transition is authorized separately.

## Completion State

Current result: **not complete**. This baseline establishes measurable targets for
Issues #61 through #66. Updating a count requires direct artifact evidence; planned
or partially drafted work does not count.
