---
summary: Short-lived signing identity where the ecosystem supports it.
type: doctrine
tags: [eos]
id: DOC-SUPPLY-008
statement: Short-lived signing identity where the ecosystem supports it.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [publishes_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0068]
review: 2027-06
lifecycle: active
verification_refs: [packs/supply-chain-integrity/CHECKS.md]
migration_sources: [packs/supply-chain-integrity/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPLY-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Key custody is the dominant observed failure, and a ten-minute certificate removes the thing that fails

Sigstore (EV-0068), signing measurement

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/supply-chain-integrity/PACK.md:defaults:004`, lines 170-170, SHA-256 `5a6142afbdb1a9866d28e8e62777ce745ddc9dd3a19c44fffe458c39722f73f9`.
