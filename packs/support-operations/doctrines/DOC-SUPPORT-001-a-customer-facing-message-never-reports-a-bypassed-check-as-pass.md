---
summary: A customer-facing message never reports a bypassed check as passing.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-001
statement: A customer-facing message never reports a bypassed check as passing.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_customer_visible_incident]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0020, EV-0041, EV-0055, EV-0095, EV-0096, EV-0122, EV-0200, EV-0210, EV-0211, EV-0233, EV-0421, EV-0422, EV-0423, EV-0424, EV-0425, EV-0426, EV-0427, EV-0428, EV-0429, EV-0430, EV-0431, EV-0432]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-SUPPORT-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_customer_visible_incident`. If a gate was skipped,
waived or run under an emergency route to get the fix out, the incident
record and any all-clear say so in those words. A status update states
what has been verified and by what, and "not yet verified" and "cause
unknown" are legal things to publish. No update asserts a cause the
incident record does not support. Basis: decision, and it binds as a
protected-set floor rather than on the support literature:
`kernel/GUARD_SPEC.md` records a bypassed gate as bypassed and lets no
emergency overlay lower it, and this is that rule pointed at the people
outside the venture. Prevents the two failures that cost the most trust:
an all-clear resting on verification nobody performed, and a second
outage from an unverified fix that the record made look verified. A
published all-clear cannot be unpublished, which is the hard-to-reverse
half.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:requirements:001`, lines 116-130, SHA-256 `d09134c5f3dca2b8f987a9593649962d73b39a50b1d4c879fbd9e83708134e6d`.
