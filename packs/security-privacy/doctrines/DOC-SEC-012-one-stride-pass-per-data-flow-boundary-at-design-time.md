---
summary: One STRIDE pass per data-flow boundary at design time, timeboxed, plus an agentic pass against the OWASP agentic catalogue.
type: doctrine
tags: [eos]
id: DOC-SEC-012
statement: One STRIDE pass per data-flow boundary at design time, timeboxed, plus an agentic pass against the OWASP agentic catalogue.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [runs_agents]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0213, EV-0224]
review: on-change-of:EV-0213
lifecycle: active
verification_refs: [packs/security-privacy/CHECKS.md]
migration_sources: [packs/security-privacy/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SEC-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

STRIDE is teachable and repeatable but has no vocabulary for a model that follows instructions in its input

EV-0224, EV-0213

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:defaults:002`, lines 175-175, SHA-256 `5f85013d53558244e2699ca36bb6613d41913972e718aeb9b9aa0897f00b0485`.
