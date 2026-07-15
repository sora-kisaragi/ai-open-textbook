# MVP Release Checklist

Status: `draft`
Review status: `needs_human_review`

## Purpose

Define the evidence needed before a future v0.2 public preview or stable
release decision. This checklist does not grant approval and does not make this
project an official textbook.

## Release Boundary

Release candidates must follow the release boundary terminology in
`docs/MVP_SCOPE.md` and distinguish these states:

- Draft: work exists but has not completed machine checks or human review.
- Review candidate: required files exist and machine checks have passed.
- Public preview: maintainer-approved preview material with known limitations.
- Stable release: a separate future release stage unless maintainers explicitly decide
  otherwise; requires completed review gates and release notes.

The v0.2 public preview is not the same as a stable release. No file or record
may use `approved`, `published`, `stable`, or equivalent final status without
explicit human approval. Do not introduce status values that conflict with
`AGENTS.md` or `docs/DATA_MODEL.md`.

## Required Content Artifacts

- [ ] All 32 structured lesson requirements in the canonical curriculum.
- [ ] All 32 Japanese learner lesson bodies.
- [ ] All 32 supplemental teacher guides.
- [ ] All 140 problem prompts and their objective coverage.
- [ ] Separate answer and rubric materials for all 140 problems.
- [ ] Release notes or changelog entry for the release candidate.

## Required Data Artifacts

- [ ] Canonical NDJSON records in `data/collections/*.ndjson`.
- [ ] Lesson records for included lessons.
- [ ] Problem, answer, and rubric records for included exercises.
- [ ] Source records where factual or curriculum claims require references.
- [ ] Revision records for non-trivial content or data changes.
- [ ] Generated SQLite index rebuilt from canonical NDJSON for validation
      evidence only.

## Required Review Artifacts

- [ ] MVP review checklist evidence from
      `docs/review/MVP_REVIEW_CHECKLIST.md`.
- [ ] Pedagogy review findings or explicit human deferral.
- [ ] Copyright/source-risk review findings.
- [ ] Accessibility review notes.
- [ ] Data/schema validation evidence.
- [ ] Open maintainer decisions list.

## Required Validation Evidence

- [ ] `python3 scripts/validate_ndjson.py` passed, or Windows fallback
      `python scripts/validate_ndjson.py` passed with the launcher issue
      documented.
- [ ] `python3 scripts/build_sqlite_index.py` passed, or Windows fallback
      `python scripts/build_sqlite_index.py` passed with the launcher issue
      documented.
- [ ] `git diff --check` passed.
- [ ] Any additional repository validation command clearly available at release
      time has passed or its failure is documented.

## Copyright and Source Notes

- [ ] Originality review covers lesson text, teacher-guide text, problems,
      answers, rubrics, examples, feedback, and diagrams.
- [ ] No copied or closely paraphrased textbook, paid problem-book,
      proprietary diagram, hidden teacher manual, or answer-key material is
      included.
- [ ] Quotations are minimized, attributed, and reviewed.
- [ ] Factual or curriculum claims have source references or are marked as
      needing review.
- [ ] Copyright-risk decisions are made by human maintainers.

## Accessibility Notes

- [ ] Images and diagrams include alt text or text equivalents.
- [ ] No content relies on color alone.
- [ ] Tables, code, and trace examples are readable in text form.
- [ ] Web or interactive materials include keyboard and screen-reader
      considerations.
- [ ] Inclusive examples avoid unnecessary personal data, sensitive traits,
      wealth, family structure, region, or narrow cultural assumptions.
- [ ] Non-visual alternatives exist where visual explanation is used.

## Public Preview Rules

- [ ] Public preview material is clearly labeled as preview or draft support
      material.
- [ ] Teacher guides, if included, are supplemental support material only.
- [ ] Known gaps and open maintainer decisions are listed.
- [ ] Preview status does not imply official approval, stable release,
      curriculum alignment, or publication.

## Prohibited Release Claims

- [ ] Do not claim official textbook status.
- [ ] Do not claim final curriculum alignment without human approval and
      source evidence.
- [ ] Do not claim copyright clearance or legal approval by AI review.
- [ ] Do not claim material is approved, published, stable, or production-ready
      without explicit human approval.

## Release Notes Requirements

- [ ] Release scope and included artifacts are listed.
- [ ] Changed files and data records are summarized.
- [ ] Validation evidence is included.
- [ ] AI usage summary is included.
- [ ] Human review completed and still needed are both listed.
- [ ] Copyright/source note is included.
- [ ] Accessibility note is included.
- [ ] Release notes state that the material is not an official
      government-approved textbook, is open educational material or
      supplemental/self-study/teacher support material, and remains subject to
      human review and correction.
- [ ] Backward compatibility and known limitations are included.

## Human Approval Gates

Human approval is required for public release, stable release, license changes,
curriculum alignment claims, copyright-risk decisions, sensitive social topics,
age-appropriateness decisions, accessibility acceptance for release-scope
material, and changes from `approved` to `published`.

## Open Maintainer Decisions

- Whether teacher guides are included in a future v0.2 public preview or treated as beta
  support material.
- Whether lesson records should add explicit teacher-guide reference fields.
- Whether timing guidance should remain flexible or include 45/50-minute
  examples.
- Whether pedagogy review is mandatory before teacher-guide body drafting.
- Which artifacts define the minimum v0.2 public preview boundary.
