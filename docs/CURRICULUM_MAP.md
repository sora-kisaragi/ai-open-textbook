# Curriculum Map: Information I Review Candidate v0.3

Status: `draft`
Review status: `needs_human_review`
Tracking issues: #59, #74, #91

This map is an original project decomposition of the four Information I content
areas identified in current MEXT primary sources. It is a planning artifact, not
an official sequence or final alignment decision.

## Sequence

| Order | Lesson ID | Planning title | Depends on |
| ---: | --- | --- | --- |
| A1 | `lesson.info1.society.information.media.v1` | Information and Media | None |
| A2 | `lesson.info1.society.source.evaluation.v1` | Reliability and Source Evaluation | A1 |
| A3 | `lesson.info1.society.rights.responsibility.v1` | Rights, Responsibility, Privacy, Copyright, and Risk | A1, A2 |
| A4 | `lesson.info1.society.problem.definition.v1` | Problem Definition and Requirements | A1 |
| A5 | `lesson.info1.society.decomposition.modeling.v1` | Decomposition and Modeling | A4 |
| A6 | `lesson.info1.society.solution.evaluation.v1` | Comparing and Evaluating Solutions | A2, A5 |
| A7 | `lesson.info1.society.inquiry.project.v1` | Information Society Inquiry Project | A3, A6 |
| B1 | `lesson.info1.design.communication.media.v1` | Communication and Media Choice | A1 |
| B2 | `lesson.info1.design.digital.representation.v1` | Digital Representation of Media | B1 |
| B3 | `lesson.info1.design.audience.accessibility.v1` | Audience, Purpose, and Accessibility | A2, B1 |
| B4 | `lesson.info1.design.information.structure.v1` | Information Structure and Visual Hierarchy | B2, B3 |
| B5 | `lesson.info1.design.data.visualization.v1` | Data Visualization and Misleading Presentation | A2, B4 |
| B6 | `lesson.info1.design.prototype.usability.v1` | Prototyping and Usability Evaluation | B3, B4 |
| B7 | `lesson.info1.design.project.v1` | Information Design Project | B5, B6 |
| C1 | `lesson.info1.programming.computer.systems.v1` | Computer Systems and Information Processing | B2 |
| C2 | `lesson.info1.programming.variables.v1` | Variables and Assignment | None |
| C3 | `lesson.info1.programming.conditionals.v1` | Comparisons and Conditionals | C2 |
| C4 | `lesson.info1.programming.loops.v1` | Repetition | C3 |
| C5 | `lesson.info1.programming.collections.strings.v1` | Collections and Strings | C2, C4 |
| C6 | `lesson.info1.programming.functions.v1` | Functions and Decomposition | C2, C3, C4, C5 |
| C7 | `lesson.info1.programming.algorithms.v1` | Algorithms and Efficiency | C4, C5, C6 |
| C8 | `lesson.info1.programming.modeling.simulation.v1` | Modeling and Simulation | A5, C3, C4, C6 |
| C9 | `lesson.info1.programming.project.v1` | Tested Programming Project | A6, B6, C7, C8 |
| D1 | `lesson.info1.networks.protocols.v1` | Networks and Protocols | B1, C1 |
| D2 | `lesson.info1.networks.internet.web.v1` | Internet, Web, and Information Services | D1 |
| D3 | `lesson.info1.networks.security.v1` | Authentication, Encryption, and Security | A3, D2 |
| D4 | `lesson.info1.data.lifecycle.v1` | Data Lifecycle, Measurement, Bias, and Ethics | A2, A4 |
| D5 | `lesson.info1.data.cleaning.v1` | Tabular Data and Cleaning | D4 |
| D6 | `lesson.info1.data.descriptive.analysis.v1` | Descriptive Analysis | D5 |
| D7 | `lesson.info1.data.visualization.interpretation.v1` | Visualization and Interpretation | B5, D6 |
| D8 | `lesson.info1.data.databases.queries.v1` | Databases and Queries | D2, D5, D6 |
| D9 | `lesson.info1.data.investigation.project.v1` | Data Investigation Project | A6, B6, D3, D7, D8 |

## Dependency Graph

```text
A1 -> A2 -> A3
A1 -> A4 -> A5 -> A6 -> A7
A2 -> A6

A1 -> B1 -> B2 -> C1
A2 + B1 -> B3 -> B4 -> B5
B3 + B4 -> B6
B5 + B6 -> B7

C2 -> C3 -> C4
C2 + C4 -> C5
C2 + C3 + C4 + C5 -> C6
C4 + C5 + C6 -> C7
A5 + C3 + C4 + C6 -> C8
A6 + B6 + C7 + C8 -> C9

B1 + C1 -> D1 -> D2 -> D3
A2 + A4 -> D4 -> D5 -> D6
B5 + D6 -> D7
D2 + D5 + D6 -> D8
A6 + B6 + D3 + D7 + D8 -> D9
```

## Cross-Cutting Design Decisions

- Problem discovery, evaluation, information ethics, security, accessibility,
  and improvement recur across units rather than appearing once as isolated facts.
- Existing Lesson 01 maps to C2. All 32 planned lessons now have learner bodies,
  teacher guides, canonical lesson records, and aligned assessment packages in
  the stacked Draft PR review candidate.
- C2 is a true beginner entry point. It introduces ordered execution and simple
  arithmetic expressions in context; C1 is recommended background, not a hard
  prerequisite.
- Python demonstrates C2 through C9, but algorithms, models, and evaluation are
  introduced independently of Python syntax.
- B5 and D7 intentionally revisit visualization: B5 emphasizes communication and
  misleading presentation; D7 emphasizes analytical interpretation and limits.
- A7, B7, C9, and D9 are performance tasks and do not replace prerequisite lessons.

## Objective and Assessment Identity

- Every objective has a stable lowercase canonical ID independent of lesson order,
  such as `obj.info1.programming.variables.003.v1`.
- Labels such as `A1.O1` and `C2.O3` are navigation aids only. Reordering a
  lesson must not rename its canonical objective IDs.
- Each lesson records objective-level assessment coverage as `not_started`,
  `partial`, or `complete`.
- `complete` requires two assessment items or one item plus a performance-task
  criterion. A single item may support more than one objective only when the
  evidence for each objective is explicit.
- Assessment-item references and performance-criterion references are stored
  separately so the completion rule can be checked mechanically.
- All 96 objective coverage entries are `complete` against the structural rule.
  This proves resolving assessment evidence, not pedagogical adequacy.

## Instructional Time Model

- One classroom period is 50 minutes.
- The curriculum JSON is authoritative for lesson timing and prerequisite edges.
- The mandatory route totals 66 periods: Unit A uses 11, Unit B uses 12, Unit C
  uses 21, and Unit D uses 22.
- The recommended route adds exactly four periods. A7, B7, C9, and D9 each have
  one additional feedback-and-revision period, bringing the route to 70 periods.
- Diagnosis and targeted reteaching are embedded in lesson stopping rules and
  recovery routes rather than assigned a separate extension period.
- These routes are project planning decisions, not mandatory allocations or an
  official timetable. Ordinary lesson assessment is included, while school
  events and local examinations require separate scheduling buffer.
- Ordinary lessons use one to three periods according to concept density. Dense
  lessons must use worked examples and staged practice instead of adding more
  objectives to a single sitting.
- A7 and B7 use three to four periods, C9 uses five to six periods, and D9 uses
  four to five periods. These projects include planning, production, feedback,
  revision, and reflection.
- Self-study estimates are recorded separately in the curriculum JSON and must be
  checked during learner trials.

Planning labels `A1` through `D9` are used for navigation and review. Stable IDs
and existing file paths remain unchanged; the historical name "Lesson 01" maps
to C2 only.

## Source Interpretation

| Area | Normative locator | Commentary locator | Project interpretation |
| --- | --- | --- | --- |
| A | Course of Study, Information I content (1), PDF pp. 191-192 | Information commentary, PDF pp. 30-34 | Seven lessons introduce problem solving and revisit it through an inquiry task. |
| B | Course of Study, Information I content (2), PDF p. 192 | Information commentary, PDF pp. 34-38 | Seven lessons move from media choice to accessible design, evaluation, and improvement. |
| C | Course of Study, Information I content (3), PDF p. 192 | Information commentary, PDF pp. 38-42 | Nine lessons connect computer representation, programming, algorithms, models, and simulation. |
| D | Course of Study, Information I content (4), PDF pp. 192-193 | Information commentary, PDF pp. 42-48 | Nine lessons connect networks, services, security, data management, analysis, and evaluation. |

The lesson count, sequence, titles, examples, and assessment design are project
decisions. They must not be described as MEXT-prescribed.

## Completion Evidence

The detailed baseline counts, objective-to-assessment rule, source-use boundary,
and final human decisions are maintained in
`docs/INFORMATION_I_COMPLETION_MATRIX.md`.
