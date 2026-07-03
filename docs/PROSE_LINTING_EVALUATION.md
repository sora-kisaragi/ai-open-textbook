# Prose Linting Evaluation

Status: `draft`
Review status: `needs_human_review`

## Purpose

Evaluate prose linting and related writing-quality options for this repository.
This document informs a later warning-only CI pilot decision. It does not adopt
tooling, add dependencies, add configuration, approve generated writing, or
replace human review.

## Current Repository Tooling

- Canonical educational records are NDJSON files under
  `data/collections/*.ndjson`.
- `scripts/validate_ndjson.py` uses only the Python standard library. It checks
  collection presence, JSON parsing, required fields, ID formats, status
  values, dates, cross-record references, lesson body references, supersession
  links, and required revision records.
- `scripts/build_sqlite_index.py` builds the generated SQLite index at
  `build/index.sqlite` from the canonical NDJSON collections. The generated
  database is disposable and must not be edited manually.
- `.github/workflows/validate.yml` runs on pull requests and pushes to `main`.
  It installs Python 3.11 on Ubuntu, then runs
  `python3 scripts/validate_ndjson.py` and
  `python3 scripts/build_sqlite_index.py`.
- `pyproject.toml` declares project metadata, requires Python `>=3.10`, records
  the source-of-truth path, and records the generated SQLite index path. It does
  not declare prose-lint dependencies.
- No `package.json`, Node lockfile, textlint configuration, Vale configuration,
  markdownlint configuration, or `requirements.txt` is present.
- Existing writing guidance lives in `docs/STYLE_GUIDE.md`,
  `docs/WRITING_QUALITY_POLICY.md`, and
  `prompts/japanese-educational-prose-cleanup.md`.
- Existing review gates are defined across `AGENTS.md`,
  `docs/OPERATING_RULES.md`, `docs/REVIEW_GUIDE.md`,
  `docs/review/MVP_REVIEW_CHECKLIST.md`, and release/process documents.
  Machine checks support review but do not replace pedagogy, copyright,
  accessibility, maintainer, or release review.

## Evaluation Scope

- Repository English prose in `docs/`, `prompts/`, GitHub templates, and review
  artifacts.
- Future Japanese localized or learner-facing prose only as a later phase after
  review gates and maintainer ownership are clearer.
- Advisory or warning-only checks that can support PR review.
- Candidate tools, rule sets, skills, and prose guidance that may inform a
  future implementation issue.

## Non-Goals

- Add dependencies or package-manager files.
- Add linter configuration.
- Add GitHub Actions prose-lint jobs or CI enforcement.
- Vendor external tools, dictionaries, prompts, rule sets, or source text.
- Generate lesson content or problem-bank content.
- Approve, publish, or claim release readiness for any content.
- Use AI detector bypass as a project goal.

## Candidate Options

### textlint

textlint is a JavaScript-based pluggable linter for natural language text. It
has a mature ecosystem and Japanese rule presets, including AI-writing-oriented
rules. It fits customizable prose checks well, but would introduce a Node/npm
tooling decision that this repository has not made.

### Vale

Vale is a cross-platform command-line prose linter written in Go. It is
markup-aware, fast, and style-guide oriented. It has strong support for custom
rules and warning-only workflows, but Japanese educational prose support would
depend on repository-authored rules or carefully reviewed third-party styles.

### markdownlint

markdownlint checks Markdown structure and consistency. It is useful for
formatting, heading levels, fenced code blocks, and list consistency. It is not
a prose-quality tool and should not be used as evidence that writing is clear,
accurate, age-appropriate, or suitable for learners.

### Existing Python Validation Only

The repository can continue with existing Python validation and human review
while deferring prose linting. This keeps dependency risk low and preserves the
current workflow. It does not catch prose style issues automatically, so
reviewers would continue relying on policy documents and PR checklists.

## Comparison Table

| Option | License signal | Dependency footprint | Current tooling fit | Japanese support | English prose support | Custom rules | False positive risk | Warning-only fit | PR workflow fit | Meaning risk | Detector-bypass risk | Maintainability | Student-facing suitability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| textlint | MIT for core repository | Node/npm required | New toolchain decision | Strong ecosystem, but rules need review | Good | High | Medium to high with broad presets | Good | Good | Medium if autofix/rewrite is used | Depends on selected rules | Medium | Later phase only after human gates |
| Vale | MIT for core repository | Standalone Go binary or package install | New toolchain decision | Possible but repository rules likely needed | Strong | High | Medium | Good | Good | Low to medium if advisory only | Low for style-guide rules | Medium | Later phase only after human gates |
| markdownlint | MIT for common Node implementation | Node/npm or external binary/action | New toolchain decision | Not language-specific | Structure only | Medium | Low to medium | Good | Good | Low | Low | Medium | Supports Markdown hygiene only |
| Existing Python validation only | Existing project policy | None added | Best current fit | None beyond human review | None beyond human review | Low unless custom scripts are added | Low | Not applicable | Existing workflow | Low | Low | High | Safe default while evaluating |

## Automatable Checks

Automatable or semi-automatable checks may include:

- Markdown structure.
- Heading consistency.
- Repeated filler phrases.
- Stale path references.
- Long sentences.
- Banned vague phrases.
- Missing required sections.
- Terminology consistency.
- Link format.
- Checklist presence.

These checks should produce review prompts, warnings, or suggestions. They
should not approve content or block release without human policy decisions.

## Human-Review-Only Checks

Human review is required for:

- Factual correctness.
- Age fit.
- Cognitive load.
- Curriculum alignment claims.
- Copyright risk.
- Accessibility adequacy.
- Appropriateness of examples.
- Meaning preservation in substantive rewrites.
- Whether Japanese learner-facing prose is suitable for learners.
- Whether any draft should be accepted or published.

## False Positive and Override Policy

- Early prose linting should be warning-only.
- A warning should identify a concrete review concern, not assert that the text
  is unacceptable.
- Maintainers should be able to override a warning in PR discussion with a
  short public reason.
- Overrides should preserve meaning, identifiers, paths, commands, review
  status, source status, and uncertainty markers.
- Repeated false positives should lead to rule adjustment or removal.
- Autofix should be avoided for educational prose unless a reviewer confirms
  meaning preservation.

## Warning-Only Rollout Recommendation

Do not add a prose linter in this PR. If maintainers choose to pilot prose
linting later, start with warning-only checks on low-risk paths:

- `docs/`
- `prompts/`
- GitHub issue and PR templates, if scoped explicitly

Avoid student-facing lesson content, teacher-guide bodies, problem records, and
Japanese localized learner-facing text until pedagogy, copyright,
accessibility, and maintainer review gates are defined for that phase.

## Dependency and Maintenance Considerations

- Any Node-based option requires a separate reviewed decision about
  `package.json`, lockfiles, package-manager policy, update cadence, and CI
  installation behavior.
- Any standalone binary option requires a separate reviewed decision about
  install source, version pinning, caching, and cross-platform behavior.
- Third-party rule sets should not be vendored without license review,
  maintenance ownership, and false-positive testing.
- Repository-specific rules are safer than broad humanizer-style presets
  because they can map directly to local policy and review gates.
- A later pilot should define who owns rule changes and how false positives are
  tracked.

## External Candidate Notes

| Candidate | Identity found | Purpose | License signal | Language support | Kind | Detector-bypass framing risk | Japanese educational prose suitability | #24 disposition | Open questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `blader/humanizer` | GitHub repository `blader/humanizer` | Claude Code skill that removes signs of AI-generated writing and makes text sound more human | MIT shown in repository | General prose; Japanese support not clearly established | Agent skill / prompt guidance | High because the project framing centers on removing AI-writing signs | Low unless reframed as clarity review and reviewed for meaning preservation | Reject for adoption; record as risk reference | Does not appear aligned with this repository's no-detector-bypass policy |
| `conorbronsdon/avoid-ai-writing` | GitHub repository `conorbronsdon/avoid-ai-writing` | Audits and rewrites content to remove AI writing patterns; includes detect-only and edit modes | MIT shown in repository badges/search result | Primarily general/English-oriented from public description | Agent skill / detector-like guidance | High because scoring and rewrite goals can be read as AI-pattern removal | Low to medium only if detect-only findings are reframed and reviewed | Defer or reject for adoption; research only | Need detailed license/readme review before any reuse; avoid rewrite modes |
| `hardikpandya/stop-slop` | GitHub repository `hardikpandya/stop-slop` | Skill file for removing AI tells from prose | MIT shown in repository | Primarily English/general prose | Agent skill / prose advice | High because it targets AI tells and authenticity scoring | Low for direct adoption; some checklist ideas may inform local rules | Research only; do not adopt now | Need source and rule provenance review before borrowing ideas |
| `japanese-tech-writing` | GitHub Gist and community/verified-skill references found | Japanese technical writing and manuscript prose norms | License not clearly found from search results | Japanese technical prose | Skill / prose guidance | Medium because it mentions suppressing LLM-like empty phrases, but also covers structure and reader load | Potentially relevant for future Japanese technical prose review, not current CI | Defer | Need authoritative source, license, maintainer identity, and reuse terms |
| `stop-ai-slop-jp` | GitHub repository `iKora128/stop-ai-slop-jp` | Japanese version of `stop-slop` for reducing AI-like Japanese prose | MIT shown in repository | Japanese | Claude Skill / prompt guidance | High because the framing is explicitly AI-slop removal | Low for adoption; may be reviewed only as a risk/reference example | Reject for adoption now; research only | Need provenance review and confirmation that rules preserve educational meaning |
| `textlint-rule-preset-ai-writing` | GitHub repository `textlint-ja/textlint-rule-preset-ai-writing`; package likely under textlint-ja scope | textlint preset for detecting AI-like Japanese writing patterns and suggesting natural Japanese expressions | License not confirmed in this pass | Japanese, textlint v14.8+ workflows | textlint rule preset / possible MCP workflow | Medium because it targets AI-like patterns, but can be used as lint warnings | Potentially relevant after dependency and rule review | Consider for future pilot only | Confirm license, package name, rule list, false positives, and suitability for educational prose |
| `patina` | GitHub repository `devswha/patina` | Detects and rewrites AI writing patterns in Korean, English, Chinese, and Japanese; skill and Node.js CLI | MIT shown in repository | Korean, English, Chinese, Japanese | Skill and standalone Node.js CLI | High because detection and rewrite of AI writing patterns are core framing | Low for adoption in this repository without major reframing | Reject for adoption now; research only | Need detailed review of rules, rewrite behavior, dependencies, and license notices |

## External Source Notes

Research sources used for this evaluation include:

- textlint: <https://github.com/textlint/textlint>
- textlint website: <https://textlint.org/>
- Vale: <https://github.com/vale-cli/vale>
- Vale website: <https://vale.sh/>
- markdownlint: <https://github.com/DavidAnson/markdownlint>
- `blader/humanizer`: <https://github.com/blader/humanizer>
- `conorbronsdon/avoid-ai-writing`:
  <https://github.com/conorbronsdon/avoid-ai-writing>
- `hardikpandya/stop-slop`: <https://github.com/hardikpandya/stop-slop>
- `iKora128/stop-ai-slop-jp`: <https://github.com/iKora128/stop-ai-slop-jp>
- `textlint-ja/textlint-rule-preset-ai-writing`:
  <https://github.com/textlint-ja/textlint-rule-preset-ai-writing>
- `devswha/patina`: <https://github.com/devswha/patina>
- `japanese-tech-writing` Gist:
  <https://gist.github.com/k16shikano/fd287c3133457c4fd8f5601d34aa817d>

## Recommendation

Use a conservative path:

1. Do not add a prose linter, package-manager file, lockfile, configuration, or
   CI job in this PR.
2. Keep existing Python validation and human review as the active workflow.
3. For a later issue, pilot warning-only checks on `docs/` and `prompts/`.
4. Prefer a small repository-specific rule set over broad third-party
   humanizer-style tooling.
5. Treat humanizer, detector-oriented, and AI-slop rewrite tools as high-risk
   unless maintainers confirm compatible framing, license, review behavior, and
   meaning preservation.
6. Keep Japanese learner-facing checks behind pedagogy, copyright,
   accessibility, and maintainer review.

## Open Questions

- Should the first pilot use textlint, Vale, markdownlint, or a minimal custom
  Python check?
- Who owns prose-lint rule maintenance and false-positive triage?
- Should a future warning-only CI job run on all Markdown files or only
  selected paths?
- Which repository-specific phrases should be warnings rather than human-only
  review prompts?
- What package-manager or binary-install policy should be approved before any
  dependency is added?
- Should Japanese prose rules be limited to prompts and review notes until
  learner-facing localization gates are complete?

## Follow-Up Issues

- Decide whether to create a warning-only prose-lint pilot for `docs/` and
  `prompts/`.
- Decide package-manager or standalone-binary policy before adding any prose
  linting dependency.
- Draft a small repository-specific warning rule list mapped to
  `docs/WRITING_QUALITY_POLICY.md`.
- Test candidate rules on existing docs and record false positives before CI
  integration.
- Define Japanese learner-facing prose review gates before applying automated
  checks to localized student material.
