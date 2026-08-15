---
summary: Recovery is forward-only and the change record says so.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-002
statement: Recovery is forward-only and the change record says so.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0207]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No down
   or undo scripts. The maintainer of the most used migration tool says
   plainly that undo cannot reverse destructive data change and cannot
   recover a script that failed on statement seven of ten (EV-0207).
   Corrections are new migrations. *Prevents*: a down function that has
   never executed against production-shaped data being treated as a
   safety net. *Basis*: decision, on a maintainer argument the pack
   notes below is not disinterested. Binds as a production-safety floor.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:requirements:002`, lines 149-156, SHA-256 `21ab56b867b90c1150bbd03c4e8bfb534519c8897d0ad74cf0a7fc3cb6cd01a6`.
