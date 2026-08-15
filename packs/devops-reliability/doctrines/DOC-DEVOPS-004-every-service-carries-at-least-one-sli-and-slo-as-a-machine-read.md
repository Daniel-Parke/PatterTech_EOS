---
summary: Every service carries at least one SLI and SLO as a machine-readable object.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-004
statement: Every service carries at least one SLI and SLO as a machine-readable object.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0020]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

OpenSLO gives a vendor-neutral declarative
   shape for SLI, SLO, error budget and alert policy, so the target is
   checkable rather than prose in a wiki (EV-0020). *Prevents*:
   reliability arguments with no shared referent, where whoever speaks
   last wins. *Basis*: standard. Not tested by the audit, see above.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:requirements:004`, lines 183-188, SHA-256 `daac778b02f027eb608ac8ac23a08991bb9e5f81afa4ece37e3c8e980c899047`.
