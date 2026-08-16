---
summary: Builds are reproducible from pinned inputs, and verified by rebuilding.
type: doctrine
tags: [eos]
id: DOC-ARCH-015
statement: Builds are reproducible from pinned inputs, and verified by rebuilding.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0155, EV-0156]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:defaults:012]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D12]
---

# DOC-ARCH-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Tools are versioned dependencies rather than host
installations, inputs are identified by content, and where a timestamp
is embedded the SOURCE_DATE_EPOCH rules apply exactly as written
(EV-0155, EV-0156). Reason: without it a change cannot be proved
harmless, because the output was never stable to begin with. This is a
default rather than binding because what it names is a missing
capability rather than a serious or irreversible failure, and because
both sources specify how to reach reproducibility rather than measuring
what goes wrong without it. Both also state the limit: clamping
timestamps does not buy reproducibility on its own. Where the build
produces something a third party installs, the artefact verification
default in `packs/security-privacy/PACK.md` is the neighbouring rule.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:defaults:012`, lines 214-226, SHA-256 `d1f541dd885337e85b99639ec155e04c9eea35b573bb499d518811cdaebdd07d`.
