---
summary: A change that publishes or consumes events names which of the four patterns it means.
type: doctrine
tags: [eos]
id: DOC-BLM-013
statement: A change that publishes or consumes events names which of the four patterns it means.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0163]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:011]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D11]
---

# DOC-BLM-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`crosses_consistency_boundary`. Event
notification, event-carried state transfer, event sourcing and CQRS are
four different things, and failures get attributed to event-driven
architecture in general when one of them was responsible (EV-0163). A
change record saying "we went event-driven" does not satisfy it. Reason:
otherwise the argument cannot be settled, because the parties mean
different things. This is a default rather than binding because the
failure is an argument nobody can settle, which costs time and nothing
else, and because EV-0163 is a definitional essay with no measurement.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:011`, lines 216-225, SHA-256 `f3da20696e4f7b712f9e236fb1342e30e2113d91cbf73ec36156093895b750a3`.
