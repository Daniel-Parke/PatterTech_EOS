---
summary: The publish path is separate, and nothing untrusted shares it.
type: doctrine
tags: [eos]
id: DOC-SUPPLY-004
statement: The publish path is separate, and nothing untrusted shares it.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [builds_release_artefact]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0038, EV-0068, EV-0069, EV-0155, EV-0156, EV-0549, EV-0550, EV-0551, EV-0552, EV-0553, EV-0554, EV-0555, EV-0556, EV-0557, EV-0558, EV-0559, EV-0560, EV-0561, EV-0562]
review: 2027-06
lifecycle: active
verification_refs: [packs/supply-chain-integrity/CHECKS.md]
migration_sources: [packs/supply-chain-integrity/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-SUPPLY-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Publishing credentials and signing identity are reachable only from the
release path. No workflow that reads untrusted input, runs a fork's
code, or executes on a shared or self-hosted runner has access to them,
and the default token starts read-only. Predicate:
`builds_release_artefact`. Prevents: a compromised build signing a real
release, which is the one failure that defeats every other control in
this pack at once, because the signature will verify. Evidence: the
platform's own statement that anyone with write access reads every
secret, that self-hosted runners give no isolation guarantee, and that
untrusted pull-request text reaches shell context.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/supply-chain-integrity/PACK.md:requirements:004`, lines 148-158, SHA-256 `50836c175aa590008583ad5ccacc6fc15c3bf6b53154b6286df8dacf36254c12`.
