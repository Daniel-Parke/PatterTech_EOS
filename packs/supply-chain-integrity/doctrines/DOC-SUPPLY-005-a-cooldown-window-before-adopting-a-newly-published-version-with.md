---
summary: A cooldown window before adopting a newly published version, with security fixes deliberately exempted.
type: doctrine
tags: [eos]
id: DOC-SUPPLY-005
statement: A cooldown window before adopting a newly published version, with security fixes deliberately exempted.
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
migration_sources: [packs/supply-chain-integrity/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPLY-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Compromised releases are usually caught in hours; a window trades patch latency for that head start, and the trade should be made on purpose

npm and Renovate release-age documentation

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/supply-chain-integrity/PACK.md:defaults:001`, lines 167-167, SHA-256 `6b5eefea428693c872424344078701639fca219e1ae4f68e27df21de67e2fa1d`.
