# Japanese Educational Prose Cleanup Guide

## Status

Status: `draft`
Review status: `needs_human_review`

## Purpose

This repository-local guide supports revising small AI-assisted Japanese
educational drafts for clarity, specificity, student comprehension, and
educational tone.

The goal is not AI detector bypass, hiding AI involvement, or making text seem
deceptively human-written. The rewrite must not change meaning.

## Scope

This guide applies to repository-local cleanup of small Japanese educational
prose drafts. It may be used for low-risk draft cleanup only.

It must not be used as approval evidence for student-facing material until
pedagogy review and copyright review are complete.

## Non-goals

- AI detector bypass.
- Hiding AI involvement.
- Changing facts, examples, definitions, identifiers, commands, or code.
- Making unsupported curriculum, legal, release, or approval claims.
- Replacing pedagogy, copyright, accessibility, maintainer, or release review.
- Applying the guide to full lesson content as part of Issue #23.

## Meaning Preservation Rules

Preserve these items exactly unless the requester explicitly authorizes a
specific change:

- Numbers.
- Definitions.
- Code.
- Identifiers.
- Filenames and paths.
- Issue numbers.
- Examples.
- Causal relationships.
- Prerequisite relationships.
- Source status.
- Uncertainty markers.
- Review status.
- Non-official-material disclaimers.

If any preserved item may be inaccurate, incomplete, or mismatched to the
target audience, keep the item unchanged and record an open question instead of
silently correcting or smoothing it.

## Japanese Educational Prose Cleanup Rules

- Use concrete wording that helps the learner identify the action, concept, or
  mistake being discussed.
- Prefer learner comprehension over polished or dramatic phrasing.
- Keep explanations age-appropriate for the stated audience.
- Avoid unnecessary flourish, slogans, dramatic emphasis, and decorative
  conclusions.
- Avoid excessive politeness, vague reassurance, and broad praise that does not
  improve understanding.
- Preserve technical terms unless a glossary, issue decision, or human review
  decision says to replace them.
- Avoid examples that assume a specific family structure, region, income level,
  gender, or cultural background unless the assumption is pedagogically
  necessary and reviewable.

## Before/After Change Summary

When substantial rewriting is performed, provide a short public summary. Do not
include private chain-of-thought.

The summary should list:

- What was clarified.
- What was preserved.
- What changed structurally.
- Any unresolved questions.

## Open Questions Instead of Guessing

Record open questions when uncertain about:

- Factual points.
- Source status.
- Curriculum alignment claims.
- Copyright risk.
- Age fit.
- Accessibility.
- Terminology.
- Intended audience.

Do not convert uncertainty into confident wording.

## Safe Output Format

For future cleanup tasks, use this output format:

```markdown
## Revised Draft

[Revised Japanese draft.]

## Change Summary

- Clarified:
- Preserved:
- Structural changes:

## Preserved Items

- Numbers:
- Definitions:
- Code, identifiers, filenames, paths, and issue numbers:
- Review status and disclaimers:

## Open Questions

- [Question or "None."]

## Human Review Needed

- Pedagogy review:
- Copyright review:
- Accessibility review:
- Maintainer review:
```

## Review Gates

Pedagogy review and copyright review are required before using this guide on
student-facing materials.

Accessibility review is required when wording affects examples, visuals,
inclusive language, or learner interaction.

Maintainer review is required before treating this guide as release criteria.

## Future Tooling Evaluation

This guide does not vendor or adopt external humanizer, anti-slop, textlint,
or CLI review tools. Future tooling evaluation should happen under Issue #24
or later issues.

The evaluation should check:

- License compatibility.
- Detector-bypass framing risk.
- Japanese educational prose fit.
- Meaning-preservation behavior.
- False positive risk.
- Maintainability.
- Whether the tool should remain advisory or become warning-only CI.

## Relationship to Existing Policy

Use this guide together with:

- `docs/WRITING_QUALITY_POLICY.md`
- `docs/STYLE_GUIDE.md`
- `docs/AI_USAGE_POLICY.md`
- `docs/REVIEW_GUIDE.md`

If this guide conflicts with those files, follow the stricter review gate and
record an open question for maintainer review.

## Minimal Example

AI-like sentence:

```text
変数はとても便利なもので、使うことでプログラムがすごく分かりやすくなります。
```

Cleaned-up version:

```text
変数は、値に名前を付けて後で使うためのしくみです。変数を使うと、同じ値の意味をコードの中で確認しやすくなります。
```

Change summary:

- Clarified that a variable names a value for later use.
- Preserved the general claim that variables can make code easier to
  understand.
- Replaced vague praise with a concrete reason.

Open question:

- Confirm whether this wording matches the intended grade level and glossary
  definition for "variable."
