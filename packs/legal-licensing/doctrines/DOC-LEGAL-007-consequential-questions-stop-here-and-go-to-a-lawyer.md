---
summary: Consequential questions stop here and go to a lawyer.
type: doctrine
tags: [eos]
id: DOC-LEGAL-007
statement: Consequential questions stop here and go to a lawyer.
kind: doctrine
authority: binding
basis: decision
evidence_grade: observational
scope: estate
applies_when: [adds_dependency]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0041, EV-0069, EV-0225, EV-0337, EV-0338, EV-0339, EV-0340, EV-0341, EV-0342, EV-0343, EV-0344, EV-0345, EV-0346, EV-0347, EV-0348, EV-0349, EV-0350, EV-0351, EV-0352]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:requirements:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B7]
accepted_adr: ADR-0008
---

# DOC-LEGAL-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

All
predicates. Four triggers, all cheap to detect: copyleft code entering
something we distribute or host in modified form; any relicensing,
licence change or transfer of contributor rights; any personal data
leaving the UK, or any regulator contact including a data subject
complaint that escalates; and any letter alleging infringement. On a
trigger the agent records the facts, stops, and routes to a human
lawyer. Prevents a confident wrong answer in the one place where being
wrong is expensive and no source read settles it. Authority: binding,
and the audit under ADR-0008 kept it there as a safety floor rather
than on its basis field: three of the four triggers are consequential
external actions or data protection, and `kernel/GUARD_SPEC.md` already
rules accepting legal terms manual-only. Basis: decision. See
`packs/legal-licensing/references/ESCALATION.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:requirements:007`, lines 219-232, SHA-256 `dc0fb887d71f505114b41ff8724fdd2c4686fcb7ad1a79b3250367fac73cdef6`.
