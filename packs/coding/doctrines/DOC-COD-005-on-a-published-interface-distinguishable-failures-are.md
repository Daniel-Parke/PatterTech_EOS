---
summary: On a published interface, distinguishable failures are declared and versioned.
type: doctrine
tags: [eos]
id: DOC-COD-005
statement: On a published interface, distinguishable failures are declared and versioned.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0171, EV-0175]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-COD-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Published means an interface with a consumer the
venture does not control: another venture, another release train, a
paying customer. The set of failures such a caller may tell apart is
named in the interface documentation, and it changes only with a version
bump. Wrapping an error makes that error part of the contract (EV-0175);
version numbers mean nothing until the public surface is declared
precisely (EV-0171). Prevents callers writing recovery against a failure
mode that quietly disappears in a patch release, which they cannot see
coming and cannot undo once shipped. Inside the venture this is D9 and
not a rule, because the pack's own anti-pattern list already says
contract ceremony on a module with one caller buys rigidity and no
coordination. See `packs/coding/wargames/WG-COD-003-failure-mode-contract.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:requirements:004`, lines 135-147, SHA-256 `aa80105c163784c6c72f311ff1e8c2d5dde6128d704b964ca7ff02b73d01dffb`.
