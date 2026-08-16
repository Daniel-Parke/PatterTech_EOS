---
summary: Every published table and every tracked event has one named owner, and its schema, quality rules, freshness expectation and owner live in one document.
type: doctrine
tags: [eos]
id: DOC-DATA-012
statement: Every published table and every tracked event has one named owner, and its schema, quality rules, freshness expectation and owner live in one document.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0305]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-DATA-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`publishes_analytics_table`, `defines_events`. Reason:
the unowned gap. A schema contract with no freshness rule and a
freshness monitor with no owner produce the same outage, and the
structural point behind the data-contract standard is that they belong
in one document with a named team, not that the document uses a
particular format (EV-0305). This is a default rather than binding
because the estate chose it: no law, standard or measurement says the
five elements must sit in one file, and the outage it prevents is one a
rerun fixes. Departing means saying who owns the gap instead.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:009`, lines 203-213, SHA-256 `363ee8f5f0ee100bcbc61a9d11e6a62107b496887ff584c5b6016a8bfdddaac5`.
