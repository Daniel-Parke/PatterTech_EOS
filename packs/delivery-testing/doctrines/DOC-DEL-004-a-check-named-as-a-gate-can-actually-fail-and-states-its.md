---
summary: A check named as a gate can actually fail, and states its threshold, its scope and its command.
type: doctrine
tags: [eos]
id: DOC-DEL-004
statement: A check named as a gate can actually fail, and states its threshold, its scope and its command.
kind: doctrine
authority: binding
basis: standard
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0009, EV-0190, EV-0191]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:requirements:005]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A gate that cannot go red is
   documentation. A mutation gate with no number is the standard
   example: the tool default is to report and never fail (EV-0190).
   Coverage percentage is never a universal gate. Basis standard
   (EV-0190) with empirical support for why unqualified numbers mislead
   (EV-0009, EV-0191). Prevents: assurance that does not exist and that
   everybody believes in, which is the same failure whether it comes
   from a threshold nobody set or from a checklist nothing runs.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:requirements:005`, lines 131-139, SHA-256 `01656fe429cdf14cf969c0ee9db6a83ad19dceb3e83dca873911da5e73989020`.
