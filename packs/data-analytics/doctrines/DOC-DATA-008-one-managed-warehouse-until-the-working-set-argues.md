---
summary: One managed warehouse until the working set argues otherwise.
type: doctrine
tags: [eos]
id: DOC-DATA-008
statement: One managed warehouse until the working set argues otherwise.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0310, EV-0311]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-DATA-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Size the stack to the query working set rather than the storage total
(EV-0311). Reason: below a few terabytes the catalogue, compaction and
snapshot maintenance an open format asks for usually exceeds the
coupling it avoids (EV-0310).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:005`, lines 178-182, SHA-256 `ad80716a774e270dac5dbbd59d13d6f2b290b08b590c6c19fff01afc94a4ceec`.
