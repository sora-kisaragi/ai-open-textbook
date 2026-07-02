# AGENTS.md

This file is the repository-level operating manual for AI coding and writing agents.
Read this before making any changes.

## Prime directive

Build open educational materials through small, reviewable, testable changes.
Never treat AI output as publishable until it passes machine checks and human review.

## Repository language

Use English for repository documents, prompts, issue templates, comments, code, and data fields.
End-user localized material may be generated later, but the source workflow stays English to reduce context cost.

## Source of truth

- Canonical educational data lives in `data/collections/*.ndjson`.
- SQLite files under `build/` are generated artifacts and must not be edited by hand.
- Markdown lesson bodies live under `lessons/` and are referenced from NDJSON records.
- Every non-trivial content change must update `data/collections/revisions.ndjson`.

## Required checks

Before proposing a pull request, run:

```bash
python3 scripts/validate_ndjson.py
python3 scripts/build_sqlite_index.py
```

If a command fails, fix the issue or document the failure in the PR.

## Agent roles

Use specialist agents when possible:

- `curriculum-planner`: scope, objectives, prerequisites, lesson graph.
- `lesson-writer`: student-facing explanation and examples.
- `problem-writer`: exercises, answers, rubrics, distractors.
- `schema-validator`: data shape, identifiers, links, generated indexes.
- `pedagogy-reviewer`: age fit, learning path, cognitive load.
- `copyright-reviewer`: originality, quotation risk, source attribution.
- `release-editor`: final integration and release notes.

## Model routing guideline

- Planner/integrator: Fable 5 or highest-planning model available.
- Routine writing and implementation: Sonnet-class model.
- Difficult review and edge-case reasoning: Opus-class model.
- Lightweight validation or tagging: fast/low-cost model.

The model names are routing hints, not project requirements.

## Boundaries

Agents must not:

- Claim the material is an official approved textbook.
- Copy existing textbooks, paid problem books, proprietary diagrams, or hidden teacher manuals.
- Invent citations or source references.
- Mark a lesson as release-ready without human review.
- Store hidden chain-of-thought in files, PRs, issues, or comments.
- Add secrets, API keys, personal data, or student data.
- Change license policy without a governance decision.
- Rewrite unrelated files while working on a narrow task.

## Acceptable reasoning artifacts

Do not include private chain-of-thought.
Use short, public reasoning artifacts instead:

- Decision summary
- Review findings
- Trade-off table
- Assumptions
- Open questions
- Test evidence

## Content status values

Use these statuses consistently:

- `draft`
- `machine_checked`
- `human_review_requested`
- `approved`
- `published`
- `deprecated`
- `superseded`

## Identifier rules

IDs must be stable, lowercase, dot-separated, and version-aware where appropriate.

Examples:

- `lesson.info1.programming.variables.v1`
- `prob.info1.variables.001.v1`
- `ans.prob.info1.variables.001.v1`
- `rubric.prob.info1.variables.001.v1`

## Pull request rule

Follow the GitHub Flow rules in `docs/GIT_WORKFLOW.md` for branching, commits, and merges.

Each PR should include:

- Scope
- Files changed
- Data records changed
- Validation result
- AI usage summary
- Human review needs
- Copyright/source note
- Backward compatibility note

## Human review gates

Human approval is required for:

- Public release
- License changes
- Curriculum alignment claims
- Copyright-risk decisions
- Sensitive social topics
- Age-appropriateness decisions
- Changes from `approved` to `published`

## Imported Claude Cowork project instructions

Work as an AI coding and editorial coworker for this repository.

Read AGENTS.md first and treat it as the primary repository-level instruction file.
Also check CLAUDE.md and relevant files under docs/ before planning or editing.

Use concise English for repository files, prompts, GitHub Issues, PR text, comments, code, schemas, and data fields.
Use Japanese for final user-facing progress reports, result summaries, and questions to the project owner.

Do not expose private chain-of-thought.
Use brief public reasoning artifacts only: assumptions, decision summaries, trade-offs, validation evidence, risks, and open questions.

This project creates open educational materials, supplemental resources, self-study materials, and teacher support materials.
Do not describe the output as an official government-approved textbook.
Do not copy, paraphrase closely, or imitate existing textbooks, paid problem books, proprietary diagrams, teacher manuals, or answer keys.
Do not invent citations, curriculum references, legal claims, or review status.

Follow a planning-first workflow:
1. Inspect the repository rules and current files.
2. State a short plan before major edits.
3. Make small, reviewable changes.
4. Keep generated content in draft status unless human review has approved it.
5. Run available validation commands before reporting completion.

Data policy:
- Treat data/collections/*.ndjson as the canonical data source.
- Treat SQLite files under build/ as generated indexes.
- Do not manually edit generated build artifacts unless explicitly asked.
- Preserve answer, rubric, source, and revision history.

Validation policy:
Run these when relevant:
python3 scripts/validate_ndjson.py
python3 scripts/build_sqlite_index.py

GitHub workflow:
Use GitHub Issues and PR-oriented work units when possible.
If GitHub CLI is unavailable, unauthenticated, or no usable remote exists, create local drafts and report that fallback honestly.

Final reports must be in Japanese and include:
- 実施概要
- 作成・変更したファイル
- GitHub Issue登録結果 or フォールバック結果
- 実行した検証コマンドと結果
- 未解決のリスク
- 次に人間が判断すべきこと
