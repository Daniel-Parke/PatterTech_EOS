---
summary: Generated reference is verified as regenerated, not hand-edited.
type: doctrine
tags: [eos]
id: DOC-DOCS-004
statement: Generated reference is verified as regenerated, not hand-edited.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0023, EV-0102, EV-0332]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-DOCS-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Where reference material is produced from a schema, model or interface
document, CI regenerates it and fails on any difference (EV-0332,
EV-0102, EV-0023). Authority: binding. Basis: standard. Prevents the
patched artefact: someone fixes a wrong line in the generated file, the
generator keeps producing the wrong line, and the next regeneration
reverts the fix. It is the one requirement here the audit left binding,
because the repair does not hold. The person who made it believes it
landed, and the wrong line ships again on the next run. ADR-0008 names
the never-hand-edit-a-derived-file rule among the things it does not
loosen, and this is that rule stated for a venture. Annotations in code
comments do not satisfy it, because proximity is not accuracy and
nothing fails when a docstring is wrong about the function beneath it.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:requirements:004`, lines 155-167, SHA-256 `5b0caf31101f1b0a35a8e19bf1eae32cb5b4602a01312a7b1f168d72634cdded`.
