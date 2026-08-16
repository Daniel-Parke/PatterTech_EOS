---
summary: A refusal suppresses before the next send, mechanically.
type: doctrine
tags: [eos]
id: DOC-MKTG-003
statement: A refusal suppresses before the next send, mechanically.
kind: doctrine
authority: binding
basis: law
evidence_grade: observational
scope: estate
applies_when: [sends_marketing_message]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0359]
review: on-change-of:PECR-reg-22-amendment
lifecycle: active
verification_refs: [packs/marketing-growth/CHECKS.md]
migration_sources: [packs/marketing-growth/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-MKTG-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`sends_marketing_message`. A valid unsubscribe request writes to a
suppression store; the send path reads that store and fails closed on
any address in it. Suppression survives list re-import and a change of
provider. Prevents the usual shape of a breach, which is not a missing
link but a link whose effect never reached the sending system. RFC 8058
fixes the signal and says nothing about how fast the effect must land
(EV-0359), so this pack rules the timing: before the next send,
not on a nightly job. Basis: law, because a refusal with no effect is
the same as no refusal.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/marketing-growth/PACK.md:requirements:003`, lines 135-144, SHA-256 `e05f9e7cddfccfef1c22b2d0ce4c547c940bd4f499b3c6b79989c5f6088703b8`.
