---
summary: A check is never weakened to make it pass.
type: doctrine
tags: [eos]
id: DOC-DEL-001
statement: A check is never weakened to make it pass.
kind: doctrine
authority: binding
basis: law
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0006, EV-0007, EV-0009, EV-0015, EV-0016, EV-0017, EV-0018, EV-0019, EV-0036, EV-0053, EV-0090, EV-0091, EV-0092, EV-0093, EV-0094, EV-0096, EV-0105, EV-0184, EV-0185, EV-0186, EV-0187, EV-0188, EV-0189, EV-0190, EV-0191, EV-0192, EV-0193, EV-0194, EV-0195, EV-0196, EV-0480]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No lowered floor, no
   skip, no deleted assertion, no added retry, no loosened tolerance in
   the change that the check caught. A gate believed wrong is escalated
   with evidence. Basis law: this is an article of the venture
   constitution in `kernel/templates/org/CONSTITUTION.tpl.md`, not a
   preference carried forward from v1, which is how it survives the
   authority audit unchanged. Prevents: a suite that converges on
   whatever the code already does.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:requirements:002`, lines 101-108, SHA-256 `7fbe5877c61ce7661b4c11b2eded56cb89f488f1c4568cb0a108c9592a7044f6`.
