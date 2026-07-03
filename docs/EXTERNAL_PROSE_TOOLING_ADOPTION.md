# External Prose Tooling Adoption

Status: draft
Review status: needs_human_review
Scope: docs/prompts/review workflow only; not student-facing content approval

## Purpose

External prose-cleanup skills, humanizer-style prompts, anti-slop rule sets,
textlint presets, dictionaries, and CLI tools have been researched or
discussed for writing-quality work. Research does not mean adoption.

This document records the current repository decision for those external
candidates. It is a proposal and decision record, not an implementation.

## Current Decision

- No external prose skill, prompt, rule set, dictionary, or CLI tool is adopted
  yet.
- No external candidate is vendored or copied into this repository.
- No external tool is approved as release criteria.
- No AI detector score may be used as pass/fail evidence.
- Existing repository-local assets remain the active guidance, subject to their
  own draft / review status:
  - `docs/WRITING_QUALITY_POLICY.md`
  - `prompts/japanese-educational-prose-cleanup.md`
  - `docs/PROSE_LINTING_EVALUATION.md`
  - `docs/PROSE_WARNING_CHECKS.md`
  - `docs/review/MVP_REVIEW_CHECKLIST.md`

## Candidate Classification

These classifications are proposals until a maintainer ratifies them on Issue #33.

| Candidate | Type | Current decision | Rationale | License check needed? | Dependency impact | Detector-bypass / humanizer-framing risk | Allowed scope | Follow-up needed? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `blader/humanizer` | Agent skill / prompt guidance | `reject` | Framing centers on making prose sound less AI-generated, which conflicts with the repository goal of educational quality and transparent review. | Yes before any reuse, but reuse is not recommended. | None if rejected. | High. | Research risk reference only. | No workflow follow-up recommended. |
| `conorbronsdon/avoid-ai-writing` | Agent skill / detector-like guidance | `reference-only` | Some detect-only ideas may inform local review prompts, but rewrite and scoring framing is too close to AI-pattern removal. | Yes before any adaptation. | None unless adopted later. | High. | Research reference; no workflow use. | License, source, and rule review before any adaptation. |
| `hardikpandya/stop-slop` | Agent skill / prose advice | `reference-only` | Broad anti-slop ideas may be useful as review concerns, but direct adoption risks copying external prompt text and optimizing for AI tells. | Yes before any adaptation. | None unless adopted later. | High. | Research reference; no workflow use. | Provenance and license review before any adaptation. |
| `japanese-tech-writing` | Japanese prose guidance | `adapt, pending license/source/project-fit review` | Japanese technical-writing ideas may fit future repository-local guidance if rewritten in original words and reviewed for educational scope. | Yes. | None unless turned into tooling later. | Medium. | Maintainer-reviewed docs and prompts only. | Confirm the authoritative source URL or repository before any adaptation. |
| `stop-ai-slop-jp` | Japanese agent skill / prompt guidance | `reject` | Explicit AI-slop removal framing is not an acceptable repository goal, especially for learner-facing material. | Yes before any reuse, but reuse is not recommended. | None if rejected. | High. | Research risk reference only. | No workflow follow-up recommended. |
| `textlint-rule-preset-ai-writing` | textlint preset | `defer` | Potentially useful as warning-only Japanese prose prompts, but requires dependency, license, rule-by-rule, and false-positive review. | Yes. | Node/package-manager decision required. | Medium. | Future non-student-facing warning-only pilot only. | Create a separate pilot issue if maintainers want to evaluate it. |
| `patina` | Skill and Node.js CLI | `reference-only` | Multilingual detection and rewrite behavior is too broad for adoption, but it can remain a comparison point for risks. | Yes before any adaptation. | Node dependency if CLI is piloted. | High. | Research reference; no workflow use. | Scope, license, and dependency review if reconsidered. |
| textlint | Prose linter framework | `defer` | Strong ecosystem and Japanese support, but the repository has not adopted Node tooling or a package-manager convention. | Yes for selected packages and rules. | Node/package-manager and lockfile policy required. | Depends on selected rules. | Future warning-only pilot for `docs/` and `prompts/` only. | Separate issue for package policy and pilot design. |
| Vale | Prose linter framework | `defer` | Useful for English docs/style-guide checks, but repository-specific rules and install policy would be needed. | Yes for binary/source and any styles. | Binary install or package policy required. | Low for style-guide rules. | Future English docs-only warning pilot if needed. | Separate issue for install, versioning, and rule ownership. |
| markdownlint | Markdown structure linter | `defer` | Useful for Markdown hygiene, not prose quality or educational approval. | Yes for selected implementation. | Node/action/binary decision required. | Low. | Future Markdown-structure pilot only. | Separate issue if structure checks become useful. |
| current Python warning-only checker | Repository-local Python script | `retain as repository-local advisory pilot` | Already implemented as a dependency-free advisory pilot. This is not an external-adoption decision and does not make the pilot accepted policy. | No external license check needed for the local script. | None added. | Low to medium because it flags detector-framing terms for review, not as a goal. | Current low-risk scope in `docs/PROSE_WARNING_CHECKS.md`; advisory only. | Maintain false-positive triage and ownership. |

## Adoption Criteria

An external candidate cannot move to `adopt` until all of these conditions are
met and recorded:

- License compatibility is checked and recorded.
- Source provenance is reviewed.
- Detector-bypass framing is absent or explicitly rejected.
- The tool does not claim to prove human authorship or non-AI authorship.
- Dependency impact is approved.
- Package-manager convention is decided if applicable.
- Rollout starts warning-only.
- False-positive triage plan is defined.
- Override policy is defined.
- Maintainer ownership is defined.
- Human review gates are preserved.
- Student-facing Japanese material is excluded unless explicitly approved
  through pedagogy, copyright, accessibility, maintainer, and release review.

## Adaptation Criteria

Ideas may be adapted without copying when these conditions are met:

- A general idea is rewritten into repository-local guidance in original words.
- External prompt, rule, dictionary, or source text is not copied unless the
  license permits it and maintainers approve it.
- The adaptation preserves meaning, status, identifiers, code, examples,
  source status, and uncertainty markers.
- A source is cited or recorded when a specific external idea meaningfully
  influenced repository guidance.

## Rejection Criteria

Reject or keep a candidate out of workflow use when any of these apply:

- Detector-bypass or evasion framing.
- Humanizer goal without a clear educational quality purpose.
- Unclear license or provenance.
- Large dependency burden for a small review benefit.
- High false-positive risk without a triage plan.
- Poor fit for Japanese educational prose.
- Suggestions that imply automatic approval or correctness.
- Conflict with `docs/WRITING_QUALITY_POLICY.md`.

## Allowed and Disallowed Uses

Allowed uses:

- Research reference.
- Maintainer-reviewed adaptation.
- Warning-only review prompt.
- Documentation-only comparison.
- Non-student-facing pilot after approval.

Disallowed uses:

- Release gate.
- Student-facing approval gate.
- Detector bypass.
- Human authorship proof.
- Automatic rewrite acceptance.
- Bulk rewriting without review.
- Vendoring external content without license review.

## Relationship to Existing Docs

- `docs/WRITING_QUALITY_POLICY.md` defines the draft writing-quality principles,
  non-goals, meaning-preservation requirements, and human-review-only
  judgments.
- `docs/PROSE_LINTING_EVALUATION.md` records the earlier tooling evaluation and
  external candidate research notes.
- `docs/PROSE_WARNING_CHECKS.md` documents the current repository-local
  dependency-free warning-only pilot.
- `prompts/japanese-educational-prose-cleanup.md` provides repository-local
  draft cleanup guidance for small Japanese educational prose drafts.
- `docs/review/MVP_REVIEW_CHECKLIST.md` records review evidence expectations and
  human-review-only judgments for MVP material.

## Recommended Next Steps

- Use Issue #33 as the tracking issue for external prose adoption decisions.
- Do not implement external tools in this PR.
- If needed, create separate future issues for:
  - textlint warning-only pilot
  - Vale docs-only pilot
  - markdownlint Markdown-structure pilot
  - Japanese prose false-positive triage
  - external candidate license review

## Open Questions

- Which maintainer owns external prose-tooling adoption decisions?
- Which candidate, if any, should receive a license review first?
- Should dependency policy be decided before any textlint, Vale, or
  markdownlint pilot is scoped?
- What evidence is enough to expand warning-only checks beyond low-risk
  repository docs and prompts?
