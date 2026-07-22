# Export and Index Workflow

Status: `draft`

## Purpose

This workflow keeps review builds reproducible from canonical repository
sources. NDJSON records under `data/collections/` remain the source of truth.
Generated review artifacts must be rebuilt from those sources, not edited by
hand.

## Validation Command Policy

Install the locked toolchain and run these commands before requesting review or
opening a pull request:

```bash
uv sync --locked --extra dev
uv run python -m playwright install chromium
uv run python scripts/check_revision_history.py --base-ref <pull-request-base>
uv run python scripts/validate_ndjson.py
uv run python scripts/build_sqlite_index.py
uv run python scripts/check_examples.py
uv run python scripts/build_static_site.py
uv run python scripts/verify_static_site.py
uv run python scripts/build_pdf.py --edition classroom
uv run python scripts/build_pdf.py --edition self-study
uv run python -m pytest
```

On Windows systems where `python3` is unavailable or only prints launcher
output such as `Python`, use the locked virtual-environment interpreter and
report the fallback in the pull request:

```bash
.venv\Scripts\python.exe scripts/validate_ndjson.py
.venv\Scripts\python.exe scripts/build_sqlite_index.py
.venv\Scripts\python.exe scripts/check_examples.py
.venv\Scripts\python.exe scripts/build_static_site.py
.venv\Scripts\python.exe scripts/verify_static_site.py
.venv\Scripts\python.exe scripts/build_pdf.py --edition classroom
.venv\Scripts\python.exe scripts/build_pdf.py --edition self-study
.venv\Scripts\python.exe -m pytest
```

If a generated index change is under review, run the SQLite build command twice
to confirm the rebuild path is repeatable.

## Generated-Only Build Policy

Files under `build/` are generated artifacts. Do not edit them manually. If a
generated artifact is wrong, fix the canonical source data or the generator,
then rebuild the artifact.

`build/index.sqlite` is disposable. Rebuild it from NDJSON with:

```bash
python3 scripts/build_sqlite_index.py
```

The builder writes a complete temporary database under `build/` and replaces
`build/index.sqlite` only after generation succeeds. If replacement fails
because the database is open, especially on Windows where file locks are strict,
close the application holding the file and rerun the command.

The builder runs production validation first and also projects the curriculum
plan into `curriculum_lessons`, `objectives`, and `coverage` tables. It never
replaces an existing index when source validation fails.

## Static Textbook Site

The static textbook site is a generated review and learning artifact under
`build/site/`. Its canonical inputs remain lesson Markdown, teacher-guide
Markdown, and NDJSON records. Do not edit or commit generated HTML or CSS.

Install the declared Python project dependencies, then build the site with:

```bash
python3 scripts/build_static_site.py
```

Windows fallback:

```bash
.venv\Scripts\python.exe scripts/build_static_site.py
```

The builder pre-renders answer-free classroom pages, self-study pages with
native `details`/`summary` answer reveals, and teacher/reviewer pages. It copies
local styles so `build/site/index.html` can be opened without a web server or
network access. It replaces only `build/site/`; it does not remove or modify
`build/index.sqlite`. Learner pages exclude answer, rubric, verification, and
review metadata, while teacher/reviewer pages present those records separately.
The self-study pages include canonical answers, acceptable answers,
explanations, and common-mistake feedback, but exclude rubrics, points,
verification evidence, internal IDs, and lifecycle metadata.

The same build writes deterministic reviewer artifacts to
`build/site/reports/semantic-coverage-audit.json` and
`build/site/reports/unit-balance-report.json`. The first classifies all
curriculum objective claims as supported, partial, or unsupported from their
declared cross-record links while retaining `needs_human_review` for semantic
quality. The second derives lesson counts and period allocation from the
curriculum source of truth.

Run `scripts/verify_static_site.py` after generation. The verifier checks the
actual output tree for broken local links and fragments, runtime remote assets,
expected page and answer-reveal counts, native keyboard-operable disclosure
controls, report consistency, and edition-specific learner-data separation.

## Runnable Examples and PDF

`scripts/check_examples.py` AST-checks Python examples, runs permitted examples
twice in isolated temporary directories with time and output limits, and verifies
predict-output answers without defining broader answer normalization policy.

`scripts/build_pdf.py` rebuilds the selected edition, prints it with the locked
Playwright/Chromium toolchain, normalizes review metadata, and verifies page
size, lesson headings, and edition-specific review-only token exclusion. Run it
once per edition. It writes:

- `build/information-i-textbook.pdf`
- `build/information-i-textbook.manifest.json`
- `build/information-i-self-study.pdf`
- `build/information-i-self-study.manifest.json`

This is a repeatable pinned workflow, not a cross-platform byte-identity claim.
Generated PDF and site artifacts remain uncommitted review outputs.

## Export Manifest Expectations

`MANIFEST.json` is the current review-build source manifest at the repository
root. It should track files that reviewers need to reproduce or inspect a
review build, including source documents, scripts, schemas, prompts, workflow
configuration, and checksums. It should not track generated `build/` contents.
The exporter reads the Git index rather than walking the working directory. New
source files must therefore be staged before a manifest refresh. It excludes
`MANIFEST.json` itself, local environments, test caches, temporary QA files, and
generated outputs. Ignored local files such as `.env` and
`.claude/settings.local.json` cannot enter the source manifest.

Regenerate the manifest only when the PR scope explicitly includes a manifest
refresh or when maintainers request updated checksums as review evidence. Use
the repository manifest exporter after staging the intended source scope:

```bash
git add <intended-source-files>
python3 scripts/export_manifest.py > MANIFEST.json
```

Windows fallback:

```bash
git add <intended-source-files>
.venv\Scripts\python.exe scripts/export_manifest.py > MANIFEST.json
```

The source manifest complements, but does not replace, the frozen Git commit
identity and the generated PDF manifest under `build/`. The current repository
keeps `MANIFEST.json` at the root. A future governance decision may add or move
release-specific manifests without changing the canonical-source policy.

## Failure Reporting

Do not hide validation, index-build, manifest-export, or CI failures. Report
failures in PR evidence with the command, the relevant error summary, and any
fallback command that was run. If a command cannot be run in the local
environment, state that explicitly.

## CI Relationship

`.github/workflows/validate.yml` runs on pull requests and pushes to `main`.
It installs the locked Python and Chromium toolchain plus Japanese PDF fonts,
runs revision-history, validation, example, site, PDF, pytest, and prose gates,
and uploads generated site/PDF artifacts for review. GitHub Actions are pinned
to reviewed commit SHAs.

Local validation should match CI as closely as practical. Windows fallback
commands are local compatibility steps; they do not change the CI command
policy.

## Open Maintainer Decisions

- Decide whether a future release should add a signed or release-specific
  manifest in addition to the source and PDF manifests.
