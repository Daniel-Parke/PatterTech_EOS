---
summary: A support inbox is a personal-data store and is run as one.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-002
statement: A support inbox is a personal-data store and is run as one.
kind: doctrine
authority: binding
basis: law
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0041, EV-0425]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-SUPPORT-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_customer_inbound`, `exports_ticket_text`. Retention, access and
lawful basis follow `packs/security-privacy/`, and the ICO guidance the
estate already cites (EV-0041). No export of ticket text into a
synthesis, analytics or model tool without the recorded basis. Derived
artefacts such as triage files, theme reports and public postmortems
carry ids or hashes, never names, addresses or account numbers. Basis:
law, and data protection is a protected-set item under `GOVERNANCE.md`.
Prevents a support archive becoming an unrecorded personal-data store,
and prevents a convenience export becoming an unlawful transfer. An
export into a synthesis or model tool cannot be recalled, which is the
hard-to-reverse half.

**What deliberately does not bind.** Acknowledging a complaint on
receipt and closing it only once the complainant has been told the
outcome is the core of the complaints standard
(EV-0425). It sits below as the D3 default rather
than as a binding rule, because that standard is guidance written for
organisations large enough to run a quality management system, and the
research graded it accordingly. It is the default this pack expects the
fewest ventures to depart from.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:requirements:002`, lines 132-152, SHA-256 `89ded787b400ebd3ee58ee510c1245493d2d820b04c4e8cdf158c58b374154c0`.
