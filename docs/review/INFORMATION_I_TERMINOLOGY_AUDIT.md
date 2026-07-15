# Information I Terminology Audit

Status: `draft`
Review status: `needs_human_review`
Evidence date: 2026-07-15
Tracking: #59, #66

## Purpose

Record preferred learner-facing Japanese terms across the 32-lesson review
candidate. This is an editorial consistency aid, not an official terminology or
curriculum-alignment decision.

## Preferred Forms

| Concept | Preferred form | Usage boundary |
| --- | --- | --- |
| Subject name | `情報I` | Use ASCII `I`; do not mix in Roman numeral `Ⅰ`. |
| World Wide Web | `Web` | Use for the named system or architecture. `ウェブ` remains acceptable inside a natural compound such as `ウェブ案内`. |
| Resource identifiers | `URI`, `URL` | Use uppercase literals and define the term before analytical use. |
| Assignment | `代入` | Explain `=` as storing a value; distinguish later comparison syntax from assignment. |
| Database | `データベース` | Avoid the nonstandard long-vowel form `データーベース`. |
| Query | `問い合わせ` | Introduce SQL-specific `SELECT` after the language-independent operation. |
| Authentication and authorization | `認証`, `認可` | Keep the two roles distinct and define both before comparing them. |
| Encryption | `暗号化` | Do not imply that encryption alone removes all risk. |
| Model and simulation | `モデル`, `モデル化`, `シミュレーション` | State assumptions, omissions, and limits before drawing conclusions. |
| Accessibility | `アクセシビリティ` | Pair the term with concrete non-visual, keyboard, structure, or contrast considerations. |

## Cross-Unit Boundaries

- Unit A introduces evidence, responsibility, risk, requirements, and models.
- Unit B reuses those terms for audience-aware and accessible information design.
- Unit C treats Python as an implementation language after the transferable
  concept, trace, or model is introduced.
- Unit D reuses evidence, risk, accessibility, and model limits for networks,
  security, data, visualization, and databases.
- B5 and D7 intentionally share visualization vocabulary: B5 emphasizes
  communication choices, while D7 emphasizes analysis and inference limits.

## Machine Evidence

Contract tests reject the following learner-facing variants:

- `情報Ⅰ`
- `Ｗｅｂ`
- `データーベース`
- `シュミレーション`

The audit permits context-sensitive synonyms when they are natural Japanese and
do not change the technical distinction. Human reviewers still decide whether
definitions, reading level, and usage are suitable for high-school learners.

## Human Review Needs

- Confirm that `情報I` is the preferred repository-wide display choice.
- Confirm that `Web` and context-specific `ウェブ` usage is sufficiently
  consistent for learners.
- Review age fit when a lesson introduces several related technical terms in one
  section.
- Record any future style-guide-wide spacing decision separately from content
  accuracy or curriculum review.
