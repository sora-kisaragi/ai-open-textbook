# Full-Scope Tooling Gates

Status: `draft`
Tracking: #59, #61

## Purpose

Define the machine evidence required before the full Information I Draft PR
stack reaches its final human gate. Passing these checks does not approve,
publish, stabilize, or finally align any educational content.

## Locked Environment

`pyproject.toml` declares runtime and test dependencies. `uv.lock` fixes their
resolved versions for local and CI use.

```bash
uv sync --locked --extra dev
uv run python -m playwright install chromium
```

## Canonical Validation

`scripts/validate_ndjson.py` validates all NDJSON records and
`curriculum/highschool_information_i.curriculum.json` against executable JSON
Schemas. It then checks typed references, reciprocal problem links, source and
body paths, revision events, answer revision counters, supersession chains,
curriculum dependencies, objective ownership, instructional-time totals, and
assessment coverage.

A `complete` objective requires either:

- Two distinct assessment-item problem records; or
- One assessment-item problem plus a rubric criterion from a distinct
  performance-task problem.

Every referenced problem must belong to the lesson and explicitly list the
objective in `objective_refs`. This proves structural coverage only; humans must
still judge whether the evidence is pedagogically adequate.

`scripts/check_revision_history.py --base-ref <ref>` compares canonical records,
lesson bodies, and teacher guides with a Git base. Changed entities require a
new revision event, revision history is append-only, and direct invalid
lifecycle transitions are rejected. CI supplies the exact pull-request or push
base commit.

## Runnable Python

`scripts/check_examples.py` parses Python fences and machine-checkable answers,
rejects imports and file, network, process, interactive, or dynamic-execution
operations, and runs permitted code twice in isolated temporary directories.
Source and literal bounds, timeouts, output limits, exit status, and
deterministic stdout are enforced. POSIX validation children also receive a
memory limit. This catches trusted textbook examples; it is not an operating
system security sandbox for hostile code.

For `predict_output`, the checker removes at most one process-added final CR/LF
before exact comparison. It does not define whitespace, code, or prose answer
normalization policy; that separate decision remains tracked in Issue #46.

## Generated Delivery

- `scripts/build_static_site.py` creates curriculum-ordered learner,
  teacher/reviewer, and learner-only print pages under `build/site/`.
- `scripts/verify_static_site.py` checks actual generated links, fragments,
  local assets, expected page counts, structure, and learner/reviewer separation.
  CSS escapes are rejected so runtime references cannot bypass offline checks.
- `scripts/build_pdf.py` prints learner-only `book.html` with the locked Chromium
  toolchain and verifies A4 page structure, implemented lesson headings, and
  review-only token exclusion.

The PDF workflow is repeatable with the pinned toolchain. Cross-platform
byte-identical output is not claimed. Rendered-page visual inspection remains a
specialist and final-human review task.

## Required Sequence

```bash
uv run python scripts/check_revision_history.py --base-ref <pull-request-base>
uv run python scripts/validate_ndjson.py
uv run python scripts/build_sqlite_index.py
uv run python scripts/check_examples.py
uv run python scripts/build_static_site.py
uv run python scripts/verify_static_site.py
uv run python scripts/build_pdf.py
uv run python -m pytest
uv run python scripts/check_prose_warnings.py
```

Generated SQLite, HTML, PDF, and manifests remain disposable artifacts under
`build/` and must not be edited or committed by hand.
