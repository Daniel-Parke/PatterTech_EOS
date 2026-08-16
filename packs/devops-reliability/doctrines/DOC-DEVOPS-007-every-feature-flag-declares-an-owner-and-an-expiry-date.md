---
summary: Every feature flag declares an owner and an expiry date at creation, and long-term dependencies are taken only on stable observability signals.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-007
statement: Every feature flag declares an owner and an expiry date at creation, and long-term dependencies are taken only on stable observability signals.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0026, EV-0198, EV-0209]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:requirements:007]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Flag removal is only mechanisable if a flag
   declares an expiry and terminal value up front (EV-0209); the flag
   API standard itself does not address lifecycle (EV-0026). Signal
   stability is a per-signal contract, and anything below stable is
   pinned and schema-mapped (EV-0198). *Prevents*: permanent dead
   branches nobody owns, and dashboards and alerts silently emptying on
   a minor version bump. *Basis*: decision on the flag half, standard on
   the signal-stability half. Not tested by the audit, see above.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:requirements:007`, lines 212-221, SHA-256 `ee9e2422653c9da69b4995662f1d1de02ef16aa32b5e29d0f1300856133df2ca`.
