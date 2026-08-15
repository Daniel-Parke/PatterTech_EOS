---
summary: Contracts on public models only.
type: doctrine
tags: [eos]
id: DOC-DATA-009
statement: Contracts on public models only.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0057]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D6]
---

# DOC-DATA-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Freeze the interface of models
other people read, leave private models uncontracted (EV-0057). Reason:
contract discipline on a model with one caller buys rigidity and no
coordination.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:006`, lines 184-187, SHA-256 `15fed6dabaf56b17a51b35395f5dadd09257f0f4236a5f9476b9de2d7019c96b`.
