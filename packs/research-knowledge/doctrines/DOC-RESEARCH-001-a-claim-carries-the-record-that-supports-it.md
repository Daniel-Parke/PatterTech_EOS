---
summary: A claim carries the record that supports it.
type: doctrine
tags: [eos]
id: DOC-RESEARCH-001
statement: A claim carries the record that supports it.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [records_external_claim]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0538, EV-0539]
review: 2029-08
lifecycle: active
verification_refs: [packs/research-knowledge/CHECKS.md]
migration_sources: [packs/research-knowledge/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-RESEARCH-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Every claim written
into a knowledge base names the source it rests on, pinned to a version,
commit, tag or dated revision, with the date it was read and the licence
or terms read off the source rather than inferred from its class. The
record is the durable artefact and outlives the source (EV-0539 A2 and
R1.2, EV-0538). Predicate: `records_external_claim`. Prevents: a
decision nobody can re-examine, because the only thing that knew what it
rested on was the person who wrote it. The field list and why each field
is there are in `packs/research-knowledge/refs/record-shape.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/research-knowledge/PACK.md:requirements:001`, lines 119-127, SHA-256 `5a5fe461eb2b7376eebd29d3f5ead71aaa89961c5860bf67e30cddacf1362e64`.
