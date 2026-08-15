---
summary: Verification exists on the consuming side and fails closed.
type: doctrine
tags: [eos]
id: DOC-SUPPLY-003
statement: Verification exists on the consuming side and fails closed.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [consumes_prebuilt_artefact]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0038, EV-0068, EV-0069, EV-0155, EV-0156, EV-0549, EV-0550, EV-0551, EV-0552, EV-0553, EV-0554, EV-0555, EV-0556, EV-0557, EV-0558, EV-0559, EV-0560, EV-0561, EV-0562]
review: 2027-06
lifecycle: active
verification_refs: [packs/supply-chain-integrity/CHECKS.md]
migration_sources: [packs/supply-chain-integrity/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-SUPPLY-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Where an artefact we consume offers a signature, an attestation or a
published digest, a step checks it, and a failed or missing check stops
the build rather than logging a warning. Predicate:
`consumes_prebuilt_artefact` or `adds_dependency`. Prevents: the
observed failure mode of this whole domain, which is not absent
signatures but unchecked ones. In the four-registry measurement, a
majority of the signatures present would not verify on two of the four,
and better than a quarter would not on a third; over 99 percent of the
failures on the two that were analysed came down to keys that were
expired, revoked or unfindable. Nobody was looking.
See `packs/supply-chain-integrity/refs/admission-checklist.md`
for what a check consists of per ecosystem.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/supply-chain-integrity/PACK.md:requirements:003`, lines 134-146, SHA-256 `7c0c77ef5b7edd0f0f0c95ff8c592e70726d0580ff6d8a47254af08d1f6813c5`.
