---
summary: Human error text and machine error bodies are separate artefacts.
type: doctrine
tags: [eos]
id: DOC-WRIT-007
statement: Human error text and machine error bodies are separate artefacts.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [writes_user_facing_text]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0122]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-WRIT-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`writes_user_facing_text`. A problem-details response
(EV-0122) is for a client, not for a person, and neither is derived
from the other by string formatting. Prevents a machine `detail` field
being rendered to a user, and prevents a client parsing a translated
interface string. Basis: standard. Failed the seriousness leg here: a
badly rendered detail field is fixed in one place. Where an outside
client has started parsing the string, the lock-in is an accidental
public contract and `packs/api-integration/` owns it.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:defaults:003`, lines 226-234, SHA-256 `ad1f6cf551859250d1186d61e3c095c2a0925bae5e91c74f17560a3aa59f10e5`.
