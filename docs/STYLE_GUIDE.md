# Style Guide

## Repository language

Use English for repository workflow files, GitHub Issues, PRs, commit
messages, scripts, schemas, file paths, stable IDs, status values, commands,
and internal developer-facing documentation.

For the Japanese High School Information I MVP, learner-facing and
teacher-facing educational content should be Japanese. This policy does not
approve, publish, or count any lesson or problem-bank record by itself.

Keep literal code, program output, command names, schema keys, record IDs,
file paths, and example identifiers unchanged when they are code or
machine-readable values. Explanatory comments inside code examples may be
Japanese when the comments are learner-facing prose.

## Language Scope

Use these categories when writing or reviewing content:

| Category | Audience | Language |
| --- | --- | --- |
| Internal repository/developer-facing material | Maintainers and agents | English |
| Learner-facing educational content | Japanese High School Information I learners | Japanese |
| Teacher-facing educational content | Teachers using the material instructionally | Japanese |
| Review-facing metadata | Maintainers and reviewers | English |
| Display metadata | Learners or teachers when surfaced in materials | Japanese |
| Stable machine-readable identifiers and schema fields | Tools, scripts, indexes, and references | English or machine literals |

### Markdown Classification

| Location or element | Classification | Language rule |
| --- | --- | --- |
| `lessons/highschool_information_i/programming/01_variables.md` headings | Learner-facing educational content | Japanese |
| Lesson learning objectives | Learner-facing educational content | Japanese |
| Lesson explanatory prose | Learner-facing educational content | Japanese |
| Lesson worked-example prose | Learner-facing educational content | Japanese |
| Lesson common mistakes | Learner-facing educational content | Japanese |
| Lesson self-check questions | Learner-facing educational content | Japanese |
| `teacher_guides/highschool_information_i/programming/01_variables.md` headings | Teacher-facing educational content | Japanese |
| Teacher-guide lesson intent, flow, misconceptions, and assessment prose | Teacher-facing educational content | Japanese |
| Code examples | Code literal | Keep executable code unchanged unless the task changes the code example itself |
| Variable names used in examples | Code literal | Keep unchanged unless the example intentionally teaches a different identifier |
| Literal output | Program output literal | Keep the exact output value unchanged |
| Repository docs under `docs/` that define process, policy, or review workflow | Internal or review-facing material | English |

## Educational writing

- Define terms before using them.
- Prefer concrete examples before abstraction.
- Keep each lesson focused on one learning goal cluster.
- Include common mistakes.
- Include self-check questions.
- Avoid unnecessary jokes, memes, or cultural references.
- For draft AI-assisted writing quality guidance, see
  `docs/WRITING_QUALITY_POLICY.md`.
- For draft Japanese educational prose cleanup guidance, see
  `prompts/japanese-educational-prose-cleanup.md`.
- For draft prose-linting option evaluation, see
  `docs/PROSE_LINTING_EVALUATION.md`.
- For warning-only prose review prompts, see
  `docs/PROSE_WARNING_CHECKS.md`.
- For external prose skill, rule set, and CLI adoption status, see
  `docs/EXTERNAL_PROSE_TOOLING_ADOPTION.md`.

## Code examples

- Prefer Python for Information I programming examples.
- Every code sample should be executable.
- Avoid network calls, secrets, or file-system side effects unless necessary.

## Markdown

- One H1 per file.
- Use stable section headings.
- Keep tables short.
- Use fenced code blocks with language labels.
