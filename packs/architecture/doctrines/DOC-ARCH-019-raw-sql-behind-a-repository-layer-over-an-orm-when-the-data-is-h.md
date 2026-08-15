---
summary: Raw SQL behind a repository layer, over an ORM, when the data is hot.
type: doctrine
tags: [eos]
id: DOC-ARCH-019
statement: Raw SQL behind a repository layer, over an ORM, when the data is hot.
kind: doctrine
authority: preference
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0010, EV-0023, EV-0024, EV-0025, EV-0057, EV-0097, EV-0098, EV-0099, EV-0100, EV-0101, EV-0102, EV-0146, EV-0147, EV-0148, EV-0149, EV-0150, EV-0151, EV-0152, EV-0153, EV-0154, EV-0155, EV-0156, EV-0157, EV-0158, EV-0159, EV-0160, EV-0161, EV-0162, EV-0163]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:preferences:004]
generated_by: tools.eos.migrate_doctrines
---

# DOC-ARCH-019

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Argued at `packs/architecture/guides/WG-ARCH-002-orm-or-raw-sql.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:preferences:004`, lines 239-240, SHA-256 `489414b96f1d386ba457140bb5f84107a2d01c2b5a35036f2fc963ec7429ae12`.
