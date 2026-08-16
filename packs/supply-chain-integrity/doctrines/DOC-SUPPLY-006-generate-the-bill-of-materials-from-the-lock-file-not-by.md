---
summary: Generate the bill of materials from the lock file, not by scanning a built tree.
type: doctrine
tags: [eos]
id: DOC-SUPPLY-006
statement: Generate the bill of materials from the lock file, not by scanning a built tree.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [publishes_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0038, EV-0068, EV-0069, EV-0155, EV-0156, EV-0549, EV-0550, EV-0551, EV-0552, EV-0553, EV-0554, EV-0555, EV-0556, EV-0557, EV-0558, EV-0559, EV-0560, EV-0561, EV-0562]
review: 2027-06
lifecycle: active
verification_refs: [packs/supply-chain-integrity/CHECKS.md]
migration_sources: [packs/supply-chain-integrity/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPLY-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The measurement study found lock-file generation accurate and consistent where other routes were not

Zhou et al. 2026

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/supply-chain-integrity/PACK.md:defaults:002`, lines 168-168, SHA-256 `b345e4174fda97ce99d5e368772f2733cbdef7c5523e992699f7db0e5ead195d`.
