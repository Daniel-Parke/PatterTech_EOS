---
summary: Meaningful native HTML semantics and behaviour are the default interaction substrate.
type: doctrine
tags: [eos]
id: DOC-UIUX-023
statement: Use meaningful native HTML semantics and behaviour first; a custom interaction names the missing native capability and proves its keyboard, focus and assistive-technology behaviour.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [requires_non_semantic_custom_control, operator_requests_doctrine_review]
sources: [EV-0027, EV-0576, EV-0577]
review: on-change-of:WCAG-2.2-or-WAI-ARIA-APG
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
---

# DOC-UIUX-023

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Native elements bring semantics and interaction behaviour that custom code
must otherwise reproduce and maintain. ARIA can expose meaning but does not
add the required behaviour. Where the product genuinely needs an interaction
that native HTML cannot express, the departure records the missing capability
and tests the hardest representative interaction with keyboard, focus and an
appropriate accessibility-tree or assistive-technology check.

This is not a ban on custom presentation or richer interaction. It is the
safe starting point and the evidence boundary for departing from it.
