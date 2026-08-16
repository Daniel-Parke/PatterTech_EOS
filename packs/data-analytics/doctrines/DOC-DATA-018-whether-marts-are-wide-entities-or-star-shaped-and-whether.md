---
summary: Whether marts are wide entities or star-shaped, and whether dimensions carry surrogate keys.
type: doctrine
tags: [eos]
id: DOC-DATA-018
statement: Whether marts are wide entities or star-shaped, and whether dimensions carry surrogate keys.
kind: doctrine
authority: preference
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0307, EV-0308]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:preferences:004]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DATA-018

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The sources disagree and neither argues it (EV-0307, EV-0308).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:preferences:004`, lines 251-253, SHA-256 `706eba08990e602e9a23a8f41aacf5bad8a1837db88df8bb435442cf745833fa`.
