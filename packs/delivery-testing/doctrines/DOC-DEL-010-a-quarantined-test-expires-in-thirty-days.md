---
summary: A quarantined test expires in thirty days.
type: doctrine
tags: [eos]
id: DOC-DEL-010
statement: A quarantined test expires in thirty days.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0006, EV-0007, EV-0009, EV-0015, EV-0016, EV-0017, EV-0018, EV-0019, EV-0036, EV-0053, EV-0090, EV-0091, EV-0092, EV-0093, EV-0094, EV-0096, EV-0105, EV-0184, EV-0185, EV-0186, EV-0187, EV-0188, EV-0189, EV-0190, EV-0191, EV-0192, EV-0193, EV-0194, EV-0195, EV-0196, EV-0480]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

An expired quarantine
  is a finding. Reason: containment has to end somewhere or the
  quarantine becomes the graveyard in the anti-pattern list. Thirty days
  is our number and not a measured one, which is why it is here and not
  in requirement 4. Override with a recorded reason and a date.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:defaults:005`, lines 236-240, SHA-256 `998781a83668ba024349dfad6bb744c1af78898cc1eb96a835e28dcd79605975`.
