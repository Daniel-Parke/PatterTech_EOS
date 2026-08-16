---
summary: The privileged path is named, alarmed and reviewed.
type: doctrine
tags: [eos]
id: DOC-IDENT-009
statement: The privileged path is named, alarmed and reviewed.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_privileged_access_path]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
review: 2029-02
lifecycle: active
verification_refs: [packs/identity-access/CHECKS.md]
migration_sources: [packs/identity-access/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-IDENT-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Every route
that reaches data or actions it does not own is listed somewhere a
person can read: administrator views, support impersonation, and the
break-glass account. Each use raises an alert and leaves a record
carrying who, when, what for and what was reached. Each use gets a look
afterwards that says whether it was a drill, a real emergency or misuse.
The path is exercised on a schedule so that it is known to work before
it is needed. Predicate: `has_privileged_access_path`. Prevents: the
account that is outside every other control and that nobody watches
(Entra emergency access guidance). Detail in
`packs/identity-access/references/break-glass.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/identity-access/PACK.md:requirements:004`, lines 150-160, SHA-256 `3110b0e1ebd734499151e8dbc4ebf8d475d76524ea27fc7e64dd04558aeacb74`.
