---
summary: Promote data compute only when the current representation is measured and insufficient.
type: doctrine
tags: [eos]
id: DOC-DATA-021
statement: Data compute starts at the highest-level sufficient representation and moves to arrays, compiled kernels, alternate engines or distributed execution only when representative measurement proves the current boundary insufficient.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [reads_for_decision]
challenge_triggers: [requires_tabular_engine_choice, crosses_dataframe_array_boundary, has_profiled_numeric_kernel, working_set_exceeds_memory]
sources: [EV-0566, EV-0567, EV-0568, EV-0569, EV-0570, EV-0571, EV-0572, EV-0573, EV-0574]
review: 2027-02
lifecycle: active
verification_refs: [registry/stacks/STACK-data-compute.md, registry/stacks/probes/STACK-data-compute-2026-08-15.json]
---

# DOC-DATA-021

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Each promotion pays a different price in semantic fit, conversion, memory,
compilation, deployment or distributed operation. Measurement therefore moves
one boundary at a time under the same correctness oracle. A current package
choice, tested version and interoperability limit belongs in the dated stack
profile, not in this standing proposition.

The highest-level sufficient representation is workload-dependent. It may be
a table, query, array or domain object. This Doctrine does not make any named
library an unconditional winner and sets no universal data-size threshold.
