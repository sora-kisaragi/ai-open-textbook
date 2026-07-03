# Human Review Round 1 Packet: MVP Planning Baseline

Status: `draft`
Review status: `needs_human_review`

## Purpose

This packet identifies the MVP planning artifacts that need maintainer review
before additional learner-facing content is generated. It does not approve,
ratify, publish, or release any artifact.

Use the linked source documents for full policy and requirements text.

## Review Artifacts

| Artifact | Related issue or PR | Current status | Maintainer decision needed | Blocks learner-facing content generation? | Suggested follow-up action |
| --- | --- | --- | --- | --- | --- |
| [docs/MVP_SCOPE.md](../MVP_SCOPE.md) | #1 | `draft`; working MVP baseline for follow-up issues | Confirm the v0.1 boundary, lesson set, release stages, and remaining open decisions. | Yes | Record accepted amendments or create follow-up issues before expanding scope. |
| [docs/CURRICULUM_MAP.md](../CURRICULUM_MAP.md) | #2 | `draft`; `needs_human_review` | Confirm lesson order, objectives, prerequisites, dependency graph, and alignment-risk wording. | Yes | Record curriculum decisions, then use the map as the content planning baseline. |
| [docs/requirements/lesson-01-variables.md](../requirements/lesson-01-variables.md) | #4 | `draft`; `needs_human_review` | Confirm Lesson 01 scope, prerequisite treatment, `print` introduction, and `==` deferral. | Yes | Accept, amend, or defer requirements before expanding the seed lesson or problems. |
| [docs/requirements/lesson-02-conditionals.md](../requirements/lesson-02-conditionals.md) | #5 | `draft`; `needs_human_review` | Confirm `elif` placement, boundary-value load, indentation treatment, and nesting limits. | Yes | Resolve requirement questions before creating Lesson 02 content or records. |
| [docs/requirements/lesson-03-loops.md](../requirements/lesson-03-loops.md) | #6 | `draft`; `needs_human_review` | Confirm fixed-count and condition-controlled loop scope, trace-table load, and nested-loop exclusion. | Yes | Resolve requirement questions before creating Lesson 03 content or records. |
| [docs/requirements/teacher-guide-requirements.md](../requirements/teacher-guide-requirements.md) | #9 | `draft`; `needs_human_review` | Decide teacher-guide preview inclusion, timing assumptions, and whether lesson records need guide references. | Partly | Record whether teacher guides block v0.1 preview or remain beta support material. |
| [docs/PROBLEM_BANK_DESIGN.md](../PROBLEM_BANK_DESIGN.md) | #7 | `draft`; `needs_human_review` | Confirm 24-problem target, per-lesson distribution, type mix, seed-problem counting, and originality review path. | Yes | Resolve count and type decisions before generating problem, answer, or rubric records. |
| [docs/ANSWER_RUBRIC_VERSIONING.md](../ANSWER_RUBRIC_VERSIONING.md) | #8 | `draft`; `needs_human_review` | Confirm answer/rubric versioning expectations, supersession handling, and revision-record triggers. | Yes | Use confirmed rules before changing answer or rubric records. |
| [docs/review/MVP_REVIEW_CHECKLIST.md](MVP_REVIEW_CHECKLIST.md) | #10 | `draft`; `needs_human_review` | Confirm checklist scope, reviewer role routing, blocking criteria, and prose-review evidence handling. | Yes | Link this checklist from content PRs after maintainer amendments are recorded. |
| [docs/release/MVP_RELEASE_CHECKLIST.md](../release/MVP_RELEASE_CHECKLIST.md) | #12 | `draft`; `needs_human_review` | Confirm public-preview evidence, release-boundary language, and minimum release artifact set. | No | Keep as release-readiness guidance until learner-facing artifacts exist. |
| [docs/WRITING_QUALITY_POLICY.md](../WRITING_QUALITY_POLICY.md) | #22 | `draft`; `needs_human_review` | Confirm writing-quality scope, meaning-preservation rules, and human-review-only judgments. | Partly | Apply only as draft guidance until ownership and scope are confirmed. |
| [docs/PROSE_WARNING_CHECKS.md](../PROSE_WARNING_CHECKS.md) | #25 | `draft`; `needs_human_review` | Decide warning category ownership, false-positive triage, and whether current scope should expand. | No | Treat warnings as advisory review prompts and track rule changes separately. |
| [docs/EXTERNAL_PROSE_TOOLING_ADOPTION.md](../EXTERNAL_PROSE_TOOLING_ADOPTION.md) | #33 | `draft`; `needs_human_review` | Decide whether any external prose tool, rule set, or dependency should be adopted or rejected. | No | Keep external tooling out of release criteria until license, dependency, and ownership decisions are recorded. |
| [prompts/japanese-educational-prose-cleanup.md](../../prompts/japanese-educational-prose-cleanup.md) | #23 | `draft`; `needs_human_review` | Confirm whether and when this prompt can be used for Japanese learner-facing or teacher-facing drafts. | Partly | Use only for low-risk draft cleanup until pedagogy, copyright, accessibility, and maintainer gates are met. |

## Cross-Cutting Open Decisions

| Decision needed | Why it matters | Blocks learner-facing content generation? | Suggested owner or follow-up |
| --- | --- | --- | --- |
| Whether teacher guides are included in the v0.1 preview or deferred. | Affects release scope, teacher-guide drafting priority, and public-preview evidence. | Partly | Maintainer decision, then update #9 and #12 follow-up work. |
| Whether existing Lesson 01 seed problems count toward the 24-problem target. | Affects how many new Lesson 01 problem, answer, and rubric records are needed. | Yes | Maintainer and problem-bank review before Issue #7 generation work. |
| Where `MANIFEST.json` should live. | Affects export/index workflow documentation and generated-artifact expectations. | No | Maintainer and schema/validation owner follow-up before release packaging. |
| Who owns prose warning rule maintenance and false-positive triage. | Affects whether prose warnings stay useful and advisory without blocking review. | No | Maintainer decision before expanding warning scope or external tooling. |

## Decision Recording Format

Use this compact format when a maintainer records a decision from this packet:

```markdown
Decision:
Decider:
Date:
Follow-up issue or PR:
```

## Human Review Gate

This packet only prepares review evidence. Actual maintainer decisions must be
recorded separately before any artifact is used for generation, release-scope
planning, or publication.
