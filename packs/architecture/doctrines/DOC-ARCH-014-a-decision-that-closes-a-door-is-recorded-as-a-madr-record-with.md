---
summary: A decision that closes a door is recorded as a MADR record with two or more considered options.
type: doctrine
tags: [eos]
id: DOC-ARCH-014
statement: A decision that closes a door is recorded as a MADR record with two or more considered options.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0097]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:defaults:011]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D11]
---

# DOC-ARCH-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Options, why each lost, consequences
accepted. Immutable once accepted; reversal is a superseding record.
MADR (EV-0097) supplies the format, which scales from three lines to
three pages so ceremony stays opt-in. Reason: silent reversal and
re-litigation, which cost argument time rather than correctness. This is
a default rather than binding because its basis is an estate decision
and MADR itself notes there is no measured evidence that decision
records improve outcomes. Departing means writing down why this
particular door can be closed without a record, which is close enough to
writing the record that most changes will just write it.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:defaults:011`, lines 202-212, SHA-256 `00cf42bb360a373b9f05e48adb33efbcc1a8b231a3f55772d41263e683a67b21`.
