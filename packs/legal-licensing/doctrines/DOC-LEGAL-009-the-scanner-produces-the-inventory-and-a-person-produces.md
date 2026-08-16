---
summary: The scanner produces the inventory and a person produces the verdict.
type: doctrine
tags: [eos]
id: DOC-LEGAL-009
statement: The scanner produces the inventory and a person produces the verdict.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [adds_dependency]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0346]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-LEGAL-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A licence scan is wired as an inventory step routed to a
human, never as a gate that passes silently
(EV-0346). Reason: detection compares texts against a
curated database and reports what a file claims about itself, which is
not a compliance result. Scope note: the accuracy claim on that project
is a vendor claim with no published figure, and accuracy is not
portable between codebases anyway.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:defaults:002`, lines 252-259, SHA-256 `dcf1954cee8048f4e56a45aef70ffcbb70678d49d2fbf100748cc298d01b3ae3`.
