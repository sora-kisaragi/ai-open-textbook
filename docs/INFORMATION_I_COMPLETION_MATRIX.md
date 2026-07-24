# Information I Completion Matrix

Status: `draft`
Review status: `needs_human_review`
Tracking: #59, #74, #91
Baseline date: 2026-07-14
Evidence updated: 2026-07-23

## Purpose

Provide measurable evidence for subject-wide completeness without confusing
machine completeness with human approval. This matrix is the completion contract
for the autonomous Draft PR stack.

## Baseline, Evidence, and Target

| Artifact | Initial baseline | Integrated Draft evidence | Review-candidate target |
| --- | ---: | ---: | ---: |
| Planned curriculum lessons | 3 | 32 | 32 |
| Structured lesson requirements | 3 standalone documents | 32 validated curriculum lesson entries | 32 |
| Learner lesson bodies | 1 | 32 | 32 |
| Teacher guides | 1 | 32 | 32 |
| Canonical lesson records | 1 | 32 | 32 |
| Problem records | 2 | 140 | At least 140 |
| Answer records | 2 | 140 | One resolving answer per problem |
| Rubric records | 2 | 140 | One resolving rubric per problem |
| Source records | 1 generic draft | 35 active draft records plus 2 deprecated legacy records | Distinct claim-appropriate primary sources |
| Executable evidence | 2 answers | 32 lesson blocks, 10 problem blocks, and 7 code-answer variants checked | Every deterministic executable example and answer |
| Offline learner pages | 1 | 32 with complete navigation | 32 plus complete navigation |
| Offline teacher/reviewer pages | 1 | 32 with source and revision context | 32 plus complete navigation |
| Print/PDF workflow | Print CSS QA only | Reproducible 228-page classroom and 313-page self-study A4 PDFs | Reproducible full-book PDFs with visual QA |

The canonical curriculum lesson objects are the maintained requirements source.
They avoid 32 duplicated Markdown documents drifting away from validated IDs,
objectives, dependencies, time bands, sources, and assessment coverage. The
three standalone v0.1 requirements documents remain in history and are not
counted as the current source for other lessons.

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
| A. Information society and problem solving | 7 | 7/7 | 7/7 | 7/7 packages, 28 problems | 1/1 inquiry task |
| B. Communication and information design | 7 | 7/7 | 7/7 | 7/7 packages, 28 problems | 1/1 design task |
| C. Computers, algorithms, and programming | 9 | 9/9 | 9/9 | 9/9 packages, 48 problems | 1/1 programming task |
| D. Networks, information systems, and data | 9 | 9/9 | 9/9 | 9/9 packages, 36 problems | 1/1 investigation task |

Lesson C2 now has one learner body, one teacher guide, eight problems, eight
answers, and eight rubrics. All three C2 objectives meet the structural coverage
rule. This does not make the lesson approved or prove that the assessment design
is age-appropriate.

## Instructional Time Baseline

| Measure | Planning total |
| --- | ---: |
| Mandatory classroom periods (50 minutes) | 66 |
| Recommended extension periods | 4 |
| Recommended classroom route | 70 |
| Self-study time | 2,735-4,260 minutes |
| Multi-session performance tasks | 4 |

The mandatory unit allocations are 11 periods for Unit A, 12 for Unit B, 21 for
Unit C, and 22 for Unit D. The four performance tasks are A7, B7, C9, and D9;
each has one recommended extension period for feedback and revision. Diagnosis
and targeted reteaching remain embedded in lesson stopping and recovery rules. These
routes are design inputs for teacher review and learner trials, not official
allocations or evidence that the planned workload is age-appropriate. Ordinary
lesson assessment is included, while school events and local examinations
require separate scheduling buffer.

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
- `python scripts/verify_static_site.py`
- `python scripts/check_examples.py`
- `python scripts/build_pdf.py --edition classroom`
- `python scripts/build_pdf.py --edition self-study`
- `python -m pytest`
- Relevant `python scripts/check_prose_warnings.py ...`
- Execution checks for changed runnable examples
- Generated link, offline asset, classroom answer-leakage, and self-study
  teacher-data leakage checks
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

Current result: **machine-evidence targets satisfied; final human decisions
pending**. All measured artifact and structural coverage targets have direct
repository evidence. Treating the 32 canonical curriculum entries as the current
requirements source is a provisional anti-duplication decision that remains in
the final human checklist. This state does not approve, publish, stabilize,
release, or finally curriculum-align the material. Issue #66 records the final
integration evidence, and Issue #59 remains open through the human review and
ordered merge decision.
