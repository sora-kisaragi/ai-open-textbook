# Information I Semantic Coverage Audit

## Method

This table records one canonical row for each of the 96 objectives. `Supported`
means the referenced problem or criterion directly elicits the objective, while
the second artifact requires a distinct application, synthesis, or performance
observation. `check_integration_contract.py` compares every row with the
canonical objective ID, status, assessment items, and performance criteria.
Structural link and criterion validity are checked separately by
`validate_ndjson.py`.

One row remains `partial`. D6.O2 has direct numerical calculation evidence but
no second artifact that requires calculating token frequencies. D2.O1 now has
a direct distinction item and a changed-context synthesis item that explicitly
distinguishes the Internet, Web, an information service, and a URL as a URI.

## Verdicts

| Lesson | Objective ID | Verdict | Assessment items | Performance criteria |
| --- | --- | --- | --- | --- |
| A1 | `obj.info1.society.information.media.001.v1` | Supported | `prob.info1.society.information.media.001.v1`<br>`prob.info1.society.information.media.004.v1` | None |
| A1 | `obj.info1.society.information.media.002.v1` | Supported | `prob.info1.society.information.media.002.v1`<br>`prob.info1.society.information.media.004.v1` | None |
| A1 | `obj.info1.society.information.media.003.v1` | Supported | `prob.info1.society.information.media.003.v1`<br>`prob.info1.society.information.media.004.v1` | None |
| A2 | `obj.info1.society.source.evaluation.001.v1` | Supported | `prob.info1.society.source.evaluation.001.v1`<br>`prob.info1.society.source.evaluation.004.v1` | None |
| A2 | `obj.info1.society.source.evaluation.002.v1` | Supported | `prob.info1.society.source.evaluation.002.v1`<br>`prob.info1.society.source.evaluation.004.v1` | None |
| A2 | `obj.info1.society.source.evaluation.003.v1` | Supported | `prob.info1.society.source.evaluation.003.v1`<br>`prob.info1.society.source.evaluation.004.v1` | None |
| A3 | `obj.info1.society.rights.responsibility.001.v1` | Supported | `prob.info1.society.rights.responsibility.001.v1`<br>`prob.info1.society.rights.responsibility.004.v1` | None |
| A3 | `obj.info1.society.rights.responsibility.002.v1` | Supported | `prob.info1.society.rights.responsibility.002.v1`<br>`prob.info1.society.rights.responsibility.004.v1` | None |
| A3 | `obj.info1.society.rights.responsibility.003.v1` | Supported | `prob.info1.society.rights.responsibility.003.v1`<br>`prob.info1.society.rights.responsibility.004.v1` | None |
| A4 | `obj.info1.society.problem.definition.001.v1` | Supported | `prob.info1.society.problem.definition.001.v1`<br>`prob.info1.society.problem.definition.004.v1` | None |
| A4 | `obj.info1.society.problem.definition.002.v1` | Supported | `prob.info1.society.problem.definition.002.v1`<br>`prob.info1.society.problem.definition.004.v1` | None |
| A4 | `obj.info1.society.problem.definition.003.v1` | Supported | `prob.info1.society.problem.definition.003.v1`<br>`prob.info1.society.problem.definition.004.v1` | None |
| A5 | `obj.info1.society.decomposition.modeling.001.v1` | Supported | `prob.info1.society.decomposition.modeling.001.v1`<br>`prob.info1.society.decomposition.modeling.004.v1` | None |
| A5 | `obj.info1.society.decomposition.modeling.002.v1` | Supported | `prob.info1.society.decomposition.modeling.002.v1`<br>`prob.info1.society.decomposition.modeling.004.v1` | None |
| A5 | `obj.info1.society.decomposition.modeling.003.v1` | Supported | `prob.info1.society.decomposition.modeling.003.v1`<br>`prob.info1.society.decomposition.modeling.004.v1` | None |
| A6 | `obj.info1.society.solution.evaluation.001.v1` | Supported | `prob.info1.society.solution.evaluation.001.v1`<br>`prob.info1.society.solution.evaluation.004.v1` | None |
| A6 | `obj.info1.society.solution.evaluation.002.v1` | Supported | `prob.info1.society.solution.evaluation.002.v1`<br>`prob.info1.society.solution.evaluation.004.v1` | None |
| A6 | `obj.info1.society.solution.evaluation.003.v1` | Supported | `prob.info1.society.solution.evaluation.003.v1`<br>`prob.info1.society.solution.evaluation.004.v1` | None |
| A7 | `obj.info1.society.inquiry.project.001.v1` | Supported | `prob.info1.society.inquiry.project.001.v1` | `rubric.prob.info1.society.inquiry.project.004.v1#c1` |
| A7 | `obj.info1.society.inquiry.project.002.v1` | Supported | `prob.info1.society.inquiry.project.002.v1` | `rubric.prob.info1.society.inquiry.project.004.v1#c2` |
| A7 | `obj.info1.society.inquiry.project.003.v1` | Supported | `prob.info1.society.inquiry.project.003.v1` | `rubric.prob.info1.society.inquiry.project.004.v1#c3` |
| B1 | `obj.info1.design.communication.media.001.v1` | Supported | `prob.info1.design.communication.media.001.v1`<br>`prob.info1.design.communication.media.004.v1` | None |
| B1 | `obj.info1.design.communication.media.002.v1` | Supported | `prob.info1.design.communication.media.002.v1`<br>`prob.info1.design.communication.media.004.v1` | None |
| B1 | `obj.info1.design.communication.media.003.v1` | Supported | `prob.info1.design.communication.media.003.v1`<br>`prob.info1.design.communication.media.004.v1` | None |
| B2 | `obj.info1.design.digital.representation.001.v1` | Supported | `prob.info1.design.digital.representation.001.v1`<br>`prob.info1.design.digital.representation.004.v1` | None |
| B2 | `obj.info1.design.digital.representation.002.v1` | Supported | `prob.info1.design.digital.representation.002.v1`<br>`prob.info1.design.digital.representation.004.v1` | None |
| B2 | `obj.info1.design.digital.representation.003.v1` | Supported | `prob.info1.design.digital.representation.003.v1`<br>`prob.info1.design.digital.representation.004.v1` | None |
| B3 | `obj.info1.design.audience.accessibility.001.v1` | Supported | `prob.info1.design.audience.accessibility.001.v1`<br>`prob.info1.design.audience.accessibility.004.v1` | None |
| B3 | `obj.info1.design.audience.accessibility.002.v1` | Supported | `prob.info1.design.audience.accessibility.002.v1`<br>`prob.info1.design.audience.accessibility.004.v1` | None |
| B3 | `obj.info1.design.audience.accessibility.003.v1` | Supported | `prob.info1.design.audience.accessibility.003.v1`<br>`prob.info1.design.audience.accessibility.004.v1` | None |
| B4 | `obj.info1.design.information.structure.001.v1` | Supported | `prob.info1.design.information.structure.001.v1`<br>`prob.info1.design.information.structure.004.v1` | None |
| B4 | `obj.info1.design.information.structure.002.v1` | Supported | `prob.info1.design.information.structure.002.v1`<br>`prob.info1.design.information.structure.004.v1` | None |
| B4 | `obj.info1.design.information.structure.003.v1` | Supported | `prob.info1.design.information.structure.003.v1`<br>`prob.info1.design.information.structure.004.v1` | None |
| B5 | `obj.info1.design.data.visualization.001.v1` | Supported | `prob.info1.design.data.visualization.001.v1`<br>`prob.info1.design.data.visualization.004.v1` | None |
| B5 | `obj.info1.design.data.visualization.002.v1` | Supported | `prob.info1.design.data.visualization.002.v1`<br>`prob.info1.design.data.visualization.004.v1` | None |
| B5 | `obj.info1.design.data.visualization.003.v1` | Supported | `prob.info1.design.data.visualization.003.v1`<br>`prob.info1.design.data.visualization.004.v1` | None |
| B6 | `obj.info1.design.prototype.usability.001.v1` | Supported | `prob.info1.design.prototype.usability.001.v1`<br>`prob.info1.design.prototype.usability.004.v1` | None |
| B6 | `obj.info1.design.prototype.usability.002.v1` | Supported | `prob.info1.design.prototype.usability.002.v1`<br>`prob.info1.design.prototype.usability.004.v1` | None |
| B6 | `obj.info1.design.prototype.usability.003.v1` | Supported | `prob.info1.design.prototype.usability.003.v1`<br>`prob.info1.design.prototype.usability.004.v1` | None |
| B7 | `obj.info1.design.project.001.v1` | Supported | `prob.info1.design.project.001.v1` | `rubric.prob.info1.design.project.004.v1#c1` |
| B7 | `obj.info1.design.project.002.v1` | Supported | `prob.info1.design.project.002.v1` | `rubric.prob.info1.design.project.004.v1#c6` |
| B7 | `obj.info1.design.project.003.v1` | Supported | `prob.info1.design.project.003.v1` | `rubric.prob.info1.design.project.004.v1#c8` |
| C1 | `obj.info1.programming.computer.systems.001.v1` | Supported | `prob.info1.programming.computer.systems.001.v1`<br>`prob.info1.programming.computer.systems.004.v1` | None |
| C1 | `obj.info1.programming.computer.systems.002.v1` | Supported | `prob.info1.programming.computer.systems.002.v1`<br>`prob.info1.programming.computer.systems.004.v1` | None |
| C1 | `obj.info1.programming.computer.systems.003.v1` | Supported | `prob.info1.programming.computer.systems.003.v1`<br>`prob.info1.programming.computer.systems.004.v1` | None |
| C2 | `obj.info1.programming.variables.001.v1` | Supported | `prob.info1.variables.003.v1`<br>`prob.info1.variables.004.v1`<br>`prob.info1.variables.008.v1` | None |
| C2 | `obj.info1.programming.variables.002.v1` | Supported | `prob.info1.variables.005.v1`<br>`prob.info1.variables.007.v1`<br>`prob.info1.variables.008.v1` | None |
| C2 | `obj.info1.programming.variables.003.v1` | Supported | `prob.info1.variables.006.v1`<br>`prob.info1.variables.007.v1`<br>`prob.info1.variables.008.v1` | None |
| C3 | `obj.info1.programming.conditionals.001.v1` | Supported | `prob.info1.conditionals.001.v1`<br>`prob.info1.conditionals.004.v1`<br>`prob.info1.conditionals.007.v1`<br>`prob.info1.conditionals.008.v1` | None |
| C3 | `obj.info1.programming.conditionals.002.v1` | Supported | `prob.info1.conditionals.002.v1`<br>`prob.info1.conditionals.004.v1`<br>`prob.info1.conditionals.006.v1`<br>`prob.info1.conditionals.008.v1` | None |
| C3 | `obj.info1.programming.conditionals.003.v1` | Supported | `prob.info1.conditionals.003.v1`<br>`prob.info1.conditionals.005.v1`<br>`prob.info1.conditionals.007.v1`<br>`prob.info1.conditionals.008.v1` | None |
| C4 | `obj.info1.programming.loops.001.v1` | Supported | `prob.info1.loops.001.v1`<br>`prob.info1.loops.007.v1`<br>`prob.info1.loops.008.v1` | None |
| C4 | `obj.info1.programming.loops.002.v1` | Supported | `prob.info1.loops.002.v1`<br>`prob.info1.loops.003.v1`<br>`prob.info1.loops.005.v1`<br>`prob.info1.loops.008.v1` | None |
| C4 | `obj.info1.programming.loops.003.v1` | Supported | `prob.info1.loops.004.v1`<br>`prob.info1.loops.006.v1`<br>`prob.info1.loops.007.v1`<br>`prob.info1.loops.008.v1` | None |
| C5 | `obj.info1.programming.collections.strings.001.v1` | Supported | `prob.info1.programming.collections.strings.001.v1`<br>`prob.info1.programming.collections.strings.004.v1` | None |
| C5 | `obj.info1.programming.collections.strings.002.v1` | Supported | `prob.info1.programming.collections.strings.002.v1`<br>`prob.info1.programming.collections.strings.004.v1` | None |
| C5 | `obj.info1.programming.collections.strings.003.v1` | Supported | `prob.info1.programming.collections.strings.003.v1`<br>`prob.info1.programming.collections.strings.004.v1` | None |
| C6 | `obj.info1.programming.functions.001.v1` | Supported | `prob.info1.programming.functions.001.v1`<br>`prob.info1.programming.functions.004.v1` | None |
| C6 | `obj.info1.programming.functions.002.v1` | Supported | `prob.info1.programming.functions.002.v1`<br>`prob.info1.programming.functions.004.v1` | None |
| C6 | `obj.info1.programming.functions.003.v1` | Supported | `prob.info1.programming.functions.003.v1`<br>`prob.info1.programming.functions.004.v1` | None |
| C7 | `obj.info1.programming.algorithms.001.v1` | Supported | `prob.info1.programming.algorithms.001.v1`<br>`prob.info1.programming.algorithms.004.v1` | None |
| C7 | `obj.info1.programming.algorithms.002.v1` | Supported | `prob.info1.programming.algorithms.002.v1`<br>`prob.info1.programming.algorithms.004.v1` | None |
| C7 | `obj.info1.programming.algorithms.003.v1` | Supported | `prob.info1.programming.algorithms.003.v1`<br>`prob.info1.programming.algorithms.004.v1` | None |
| C8 | `obj.info1.programming.modeling.simulation.001.v1` | Supported | `prob.info1.programming.modeling.simulation.001.v1`<br>`prob.info1.programming.modeling.simulation.004.v1` | None |
| C8 | `obj.info1.programming.modeling.simulation.002.v1` | Supported | `prob.info1.programming.modeling.simulation.002.v1`<br>`prob.info1.programming.modeling.simulation.004.v1` | None |
| C8 | `obj.info1.programming.modeling.simulation.003.v1` | Supported | `prob.info1.programming.modeling.simulation.003.v1`<br>`prob.info1.programming.modeling.simulation.004.v1` | None |
| C9 | `obj.info1.programming.project.001.v1` | Supported | `prob.info1.programming.project.001.v1` | `rubric.prob.info1.programming.project.004.v1#c1_validation`<br>`rubric.prob.info1.programming.project.004.v1#c2_fifo_ordering`<br>`rubric.prob.info1.programming.project.004.v1#c5_executable_evidence` |
| C9 | `obj.info1.programming.project.002.v1` | Supported | `prob.info1.programming.project.002.v1` | `rubric.prob.info1.programming.project.004.v1#c6_test_classes` |
| C9 | `obj.info1.programming.project.003.v1` | Supported | `prob.info1.programming.project.003.v1` | `rubric.prob.info1.programming.project.004.v1#c7_requirement_evaluation`<br>`rubric.prob.info1.programming.project.004.v1#c8_limitations_retest` |
| D1 | `obj.info1.networks.protocols.001.v1` | Supported | `prob.info1.networks.protocols.001.v1`<br>`prob.info1.networks.protocols.004.v1` | None |
| D1 | `obj.info1.networks.protocols.002.v1` | Supported | `prob.info1.networks.protocols.002.v1`<br>`prob.info1.networks.protocols.004.v1` | None |
| D1 | `obj.info1.networks.protocols.003.v1` | Supported | `prob.info1.networks.protocols.003.v1`<br>`prob.info1.networks.protocols.004.v1` | None |
| D2 | `obj.info1.networks.internet.web.001.v1` | Supported | `prob.info1.networks.internet.web.001.v1`<br>`prob.info1.networks.internet.web.004.v1` | None |
| D2 | `obj.info1.networks.internet.web.002.v1` | Supported | `prob.info1.networks.internet.web.002.v1`<br>`prob.info1.networks.internet.web.004.v1` | None |
| D2 | `obj.info1.networks.internet.web.003.v1` | Supported | `prob.info1.networks.internet.web.003.v1`<br>`prob.info1.networks.internet.web.004.v1` | None |
| D3 | `obj.info1.networks.security.001.v1` | Supported | `prob.info1.networks.security.001.v1`<br>`prob.info1.networks.security.004.v1` | None |
| D3 | `obj.info1.networks.security.002.v1` | Supported | `prob.info1.networks.security.002.v1`<br>`prob.info1.networks.security.004.v1` | None |
| D3 | `obj.info1.networks.security.003.v1` | Supported | `prob.info1.networks.security.003.v1`<br>`prob.info1.networks.security.004.v1` | None |
| D4 | `obj.info1.data.lifecycle.001.v1` | Supported | `prob.info1.data.lifecycle.001.v1`<br>`prob.info1.data.lifecycle.002.v1`<br>`prob.info1.data.lifecycle.004.v1` | None |
| D4 | `obj.info1.data.lifecycle.002.v1` | Supported | `prob.info1.data.lifecycle.002.v1`<br>`prob.info1.data.lifecycle.004.v1` | None |
| D4 | `obj.info1.data.lifecycle.003.v1` | Supported | `prob.info1.data.lifecycle.003.v1`<br>`prob.info1.data.lifecycle.004.v1` | None |
| D5 | `obj.info1.data.cleaning.001.v1` | Supported | `prob.info1.data.cleaning.001.v1`<br>`prob.info1.data.cleaning.004.v1` | None |
| D5 | `obj.info1.data.cleaning.002.v1` | Supported | `prob.info1.data.cleaning.002.v1`<br>`prob.info1.data.cleaning.004.v1` | None |
| D5 | `obj.info1.data.cleaning.003.v1` | Supported | `prob.info1.data.cleaning.003.v1`<br>`prob.info1.data.cleaning.004.v1` | None |
| D6 | `obj.info1.data.descriptive.analysis.001.v1` | Supported | `prob.info1.data.descriptive.analysis.001.v1`<br>`prob.info1.data.descriptive.analysis.004.v1` | None |
| D6 | `obj.info1.data.descriptive.analysis.002.v1` | Partial | `prob.info1.data.descriptive.analysis.002.v1` | None |
| D6 | `obj.info1.data.descriptive.analysis.003.v1` | Supported | `prob.info1.data.descriptive.analysis.003.v1`<br>`prob.info1.data.descriptive.analysis.004.v1` | None |
| D7 | `obj.info1.data.visualization.interpretation.001.v1` | Supported | `prob.info1.data.visualization.interpretation.001.v1`<br>`prob.info1.data.visualization.interpretation.004.v1` | None |
| D7 | `obj.info1.data.visualization.interpretation.002.v1` | Supported | `prob.info1.data.visualization.interpretation.002.v1`<br>`prob.info1.data.visualization.interpretation.004.v1` | None |
| D7 | `obj.info1.data.visualization.interpretation.003.v1` | Supported | `prob.info1.data.visualization.interpretation.003.v1`<br>`prob.info1.data.visualization.interpretation.004.v1` | None |
| D8 | `obj.info1.data.databases.queries.001.v1` | Supported | `prob.info1.data.databases.queries.001.v1`<br>`prob.info1.data.databases.queries.004.v1` | None |
| D8 | `obj.info1.data.databases.queries.002.v1` | Supported | `prob.info1.data.databases.queries.002.v1`<br>`prob.info1.data.databases.queries.004.v1` | None |
| D8 | `obj.info1.data.databases.queries.003.v1` | Supported | `prob.info1.data.databases.queries.003.v1`<br>`prob.info1.data.databases.queries.004.v1` | None |
| D9 | `obj.info1.data.investigation.project.001.v1` | Supported | `prob.info1.data.investigation.project.001.v1` | `rubric.prob.info1.data.investigation.project.004.v1#c1_question_ethics` |
| D9 | `obj.info1.data.investigation.project.002.v1` | Supported | `prob.info1.data.investigation.project.002.v1` | `rubric.prob.info1.data.investigation.project.004.v1#c2_reproducible_workflow`<br>`rubric.prob.info1.data.investigation.project.004.v1#c3_accessible_evidence`<br>`rubric.prob.info1.data.investigation.project.004.v1#c6_provenance_dictionary`<br>`rubric.prob.info1.data.investigation.project.004.v1#c7_transformation_log`<br>`rubric.prob.info1.data.investigation.project.004.v1#c8_independent_check` |
| D9 | `obj.info1.data.investigation.project.003.v1` | Supported | `prob.info1.data.investigation.project.003.v1` | `rubric.prob.info1.data.investigation.project.004.v1#c4_bounded_conclusion`<br>`rubric.prob.info1.data.investigation.project.004.v1#c5_limits_improvement`<br>`rubric.prob.info1.data.investigation.project.004.v1#c9_sensitivity_results`<br>`rubric.prob.info1.data.investigation.project.004.v1#c10_presentation_revision` |

## Pilot Task-to-Rubric Semantic Bindings

These rows are review evidence for the Issue 91 synthesis tasks. They do not
change the canonical `performance_criterion_refs` contract, which is reserved
for records whose problem `question_type` is `performance_task`.

| Objective | Synthesis task evidence | Scoring evidence |
| --- | --- | --- |
| B5.O2 | The supplied defective display requires the learner to identify a misleading encoding and an inaccessible color-only encoding, then repair them. | `rubric.prob.info1.design.data.visualization.004.v1#c1` |
| C1.O2 | Four named events require an event-by-event application-state trace, with OS-mediated resources in a separate column. | `rubric.prob.info1.programming.computer.systems.004.v1#c1` |
| D2.O2 | Observations A-C require separate DNS and Web communications with local network, router, IP, transport, TLS, HTTP, and service-processing roles. | `rubric.prob.info1.networks.internet.web.004.v1#c3` |
| D2.O3 | Observations D-E require success evidence, bounded candidates, unknowns, a next check, and possible user impact. | `rubric.prob.info1.networks.internet.web.004.v1#c3` |

## Review Boundary

This semantic audit supports the Draft PR review. It does not substitute for
the final human decisions on curriculum interpretation, age appropriateness,
scoring validity, or classroom use.
