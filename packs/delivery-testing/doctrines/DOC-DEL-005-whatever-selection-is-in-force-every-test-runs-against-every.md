---
summary: Whatever selection is in force, every test runs against every changeset at some point.
type: doctrine
tags: [eos]
id: DOC-DEL-005
statement: Whatever selection is in force, every test runs against every changeset at some point.
kind: doctrine
authority: binding
basis: standard
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0016, EV-0194, EV-0480]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:requirements:006]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A selected subset may gate the merge; the
   remainder runs after it, or a full unselected run happens on a
   stated cadence. Basis standard (EV-0016, EV-0194). Prevents: a test
   that has silently not run for a year.

The strongest available measurement behind requirement 1 is EV-0480.
Prompted with the buggy implementation, eleven frontier models produced
104.15 bug-revealing tests on average, against 304.08 prompted with the
correct implementation and 186.77 when the code was swapped for a
specification. So a contaminated context does not just bless the bug, it
suppresses the tests that would have caught anything. That row's licence
was recorded from a research packet rather than read at the source, so
it carries no observation date.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:requirements:006`, lines 140-153, SHA-256 `cd135d58dfc1311e179588198ee52ebf338251f96faa9d4e156afdb05623841e`.
