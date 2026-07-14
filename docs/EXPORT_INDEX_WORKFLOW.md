# Export and Index Workflow

Status: `draft`

## Purpose

This workflow keeps review builds reproducible from canonical repository
sources. NDJSON records under `data/collections/` remain the source of truth.
Generated review artifacts must be rebuilt from those sources, not edited by
hand.

## Validation Command Policy

Run these commands before requesting review or opening a pull request:

```bash
python3 scripts/validate_ndjson.py
python3 scripts/build_sqlite_index.py
```

On Windows systems where `python3` is unavailable or only prints launcher
output such as `Python`, use the available Python interpreter and report the
fallback in the pull request:

```bash
python scripts/validate_ndjson.py
python scripts/build_sqlite_index.py
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
python scripts/build_static_site.py
```

The builder pre-renders all pages and copies local styles so the generated
`build/site/index.html` can be opened without a web server or network access.
It replaces only `build/site/`; it does not remove or modify
`build/index.sqlite`. Learner pages exclude answer, rubric, verification, and
review metadata, while teacher/reviewer pages present those records separately.

## Export Manifest Expectations

`MANIFEST.json` is the current review-build file manifest at the repository
root. It should track files that reviewers need to reproduce or inspect a
review build, including source documents, scripts, schemas, prompts, workflow
configuration, and checksums. It should not track generated `build/` contents.

Regenerate the manifest only when the PR scope explicitly includes a manifest
refresh or when maintainers request updated checksums as review evidence. Use
the repository manifest exporter:

```bash
python3 scripts/export_manifest.py > MANIFEST.json
```

Windows fallback:

```bash
python scripts/export_manifest.py > MANIFEST.json
```

The long-term manifest location is still a maintainer decision. The current
repository keeps `MANIFEST.json` at the root, while a future workflow may move
release-specific manifests under `build/` or another generated review-artifact
directory. Maintainers should also decide whether the root manifest should
continue tracking `MANIFEST.json` itself.

## Failure Reporting

Do not hide validation, index-build, manifest-export, or CI failures. Report
failures in PR evidence with the command, the relevant error summary, and any
fallback command that was run. If a command cannot be run in the local
environment, state that explicitly.

## CI Relationship

`.github/workflows/validate.yml` runs on pull requests and pushes to `main`.
It installs Python on Ubuntu and runs:

```bash
python3 scripts/validate_ndjson.py
python3 scripts/build_sqlite_index.py
```

Local validation should match CI as closely as practical. Windows fallback
commands are local compatibility steps; they do not change the CI command
policy.

## Open Maintainer Decisions

- Decide whether `MANIFEST.json` remains committed at the repository root.
- Decide whether release-specific manifests should instead be generated under
  `build/` and excluded from commits.
- Decide when manifest regeneration is required for documentation-only workflow
  changes.
