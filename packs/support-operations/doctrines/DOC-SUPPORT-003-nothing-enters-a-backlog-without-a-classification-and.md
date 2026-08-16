---
summary: Nothing enters a backlog without a classification, and untriaged is a state rather than an absence.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-003
statement: Nothing enters a backlog without a classification, and untriaged is a state rather than an absence.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0424, EV-0425, EV-0426]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-SUPPORT-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_customer_inbound`. Every
inbound item carries four independent values before it is ranked:
kind, priority, owning queue, and a triage state that is either
accepted or needs-info (EV-0424). Classification
comes before prioritisation, not after
(EV-0426). Where one cause explains several reports,
they carry one shared incident or defect id and get one answer
(EV-0425). A needs-info item carries the date its
next action is due. Basis: standard. Prevents three failures: work that
is invisible because nobody can query for it, a priority argued from
whoever wrote most recently, and five people receiving five different
accounts of one bug. Failed the seriousness leg: a misfiled item is
refiled, and the queue is recoverable at any point.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:001`, lines 165-178, SHA-256 `4856db1f23ff92270733499f9ef52f58bfedb76aac1428756d6f7446e1116a9c`.
