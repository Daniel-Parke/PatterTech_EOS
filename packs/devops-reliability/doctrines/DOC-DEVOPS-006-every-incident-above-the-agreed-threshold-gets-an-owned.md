---
summary: Every incident above the agreed threshold gets an owned postmortem with a deadline, a timeline reconstructed from evidence, and follow-ups filed as tickets.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-006
statement: Every incident above the agreed threshold gets an owned postmortem with a deadline, a timeline reconstructed from evidence, and follow-ups filed as tickets.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0200]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:requirements:006]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The incident commander names the
   owner; the owner files the actions and does not then chase them
   (EV-0200, which is Apache-2.0 and so reusable directly). *Prevents*:
   the same outage twice, and a timeline reconstructed from memory that
   flatters everyone in it. *Basis*: decision, on one exemplar's process
   documentation. Not tested by the audit, see above.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:requirements:006`, lines 203-210, SHA-256 `78995ceb8eebd81c4139481395b4c3737e4b079e0b789fe38215007e45fbf1b1`.
