---
summary: No column that can identify a living person lands in the analytics layer without a recorded lawful basis and a named complaints path.
type: doctrine
tags: [eos]
id: DOC-DATA-001
statement: No column that can identify a living person lands in the analytics layer without a recorded lawful basis and a named complaints path.
kind: doctrine
authority: binding
basis: law
evidence_grade: observational
scope: estate
applies_when: [handles_analytics_identifier]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0041, EV-0225]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-DATA-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`handles_analytics_identifier`. UK duties are statutory: a recorded
lawful basis and a statutory complaints route are duties, not good
practice (EV-0225), with the ceremony around them proportionate to the
risk to people (EV-0041). Prevents source columns being copied forward
because they were in the source, which is how an email address ends up
in a marts table nobody meant to hold one. Basis: law.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:requirements:001`, lines 110-117, SHA-256 `2ae8e5f484e84899a002bfa691b2634de3c512f713070d9e43cf4444071059a6`.
