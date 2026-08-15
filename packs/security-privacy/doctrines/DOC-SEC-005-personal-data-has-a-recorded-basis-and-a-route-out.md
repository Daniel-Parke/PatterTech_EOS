---
summary: Personal data has a recorded basis and a route out.
type: doctrine
tags: [eos]
id: DOC-SEC-005
statement: Personal data has a recorded basis and a route out.
kind: doctrine
authority: binding
basis: decision
evidence_grade: observational
scope: estate
applies_when: [handles_personal_data]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0041, EV-0225]
review: on-change-of:EV-0213
lifecycle: active
verification_refs: [packs/security-privacy/CHECKS.md]
migration_sources: [packs/security-privacy/PACK.md:requirements:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
accepted_adr: ADR-0012
---

# DOC-SEC-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Each
processing purpose records its lawful basis, and a named complaints
route exists and is reachable by the people whose data it is
(EV-0225, EV-0041). Personal data does not enter the repository, its
logs or its transcripts. Predicate: `handles_personal_data`. Prevents:
processing that cannot be defended when someone asks, and a complaint
with nowhere to land.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:requirements:005`, lines 145-151, SHA-256 `80907fbddda360f4a42acb2d60040c3c4b2750b6af71f8688a02e204502f5408`.
