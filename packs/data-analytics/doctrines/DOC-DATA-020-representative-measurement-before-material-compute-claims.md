---
summary: Representative measurement precedes a material compute, capacity or tool-selection claim.
type: doctrine
tags: [eos]
id: DOC-DATA-020
statement: A material compute, capacity or tool-selection claim starts from a correctness-checked baseline measured on a representative workload in a recorded environment.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [reads_for_decision]
challenge_triggers: [operator_requests_doctrine_review, working_set_exceeds_memory, has_profiled_numeric_kernel]
sources: [EV-0566, EV-0568, EV-0570, EV-0573, EV-0574]
review: 2027-02
lifecycle: active
verification_refs: [registry/stacks/probes/STACK-data-compute-2026-08-15.json]
---

# DOC-DATA-020

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Tool names and scale labels do not establish suitability. The baseline must
exercise the operation that matters, preserve a correctness oracle and record
the data shape, environment, first-run effects, steady-state behaviour and
material representation changes. A cheaper sample is acceptable for an early
spike when its mismatch from the target workload is explicit.

This Doctrine does not demand a benchmark for an immaterial implementation
choice. It applies when performance, capacity or tool suitability is used to
justify a decision. A Wargame decides which comparison is proportionate and
what result is sufficient for the venture.
