---
summary: Every marketing message carries a refusal route that works without a conversation.
type: doctrine
tags: [eos]
id: DOC-MKTG-002
statement: Every marketing message carries a refusal route that works without a conversation.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [sends_marketing_message]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0359, EV-0360, EV-0361]
review: on-change-of:PECR-reg-22-amendment
lifecycle: active
verification_refs: [packs/marketing-growth/CHECKS.md]
migration_sources: [packs/marketing-growth/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-MKTG-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`sends_marketing_message`. Mail carries a
`List-Unsubscribe` header with an HTTPS URI and
`List-Unsubscribe-Post: List-Unsubscribe=One-Click`, both inside the
DKIM signed-header list, with an opaque hard-to-forge token the server
validates, no cookies, no HTTP authentication and no confirmation page
(EV-0359). A visible in-body link stands beside it (EV-0360).
Prevents a refusal route that exists on paper and fails in the hand,
which is what PECR asks for at collection and in every message
(EV-0361). The token closes the mirror failure, an unsubscribe
endpoint anyone can forge into a denial-of-subscription hole. Basis:
standard, discharging a legal duty. See
`packs/marketing-growth/references/SEND_PREFLIGHT.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/marketing-growth/PACK.md:requirements:002`, lines 121-133, SHA-256 `67295b9a7c0ade0ab3a9e615a0085f0986a28c383771e9aa3c37006f3e19c0bb`.
