---
summary: The Article 13 notice checklist with both complaint routes, the separate registration duty, and where this pack hands over to security-privacy
type: guide
tags: [pii, security]
kind: fact
scope: estate
sources: [EV-0349, EV-0350, EV-0225, EV-0041]
volatility: event-driven
review: on-change-of:https://www.legislation.gov.uk/eur/2016/679/article/13
---

# Reference: the UK notice checklist and the registration duty

Level-three detail behind B5 in `packs/legal-licensing/PACK.md`. This is
not legal advice. It records a statutory checklist and a statutory
charge, both of which are cheap to check and expensive to miss.

## Who owns what

This pack owns two things only: what the notice must say, and whether
the registration duty has been discharged. The lawful basis register,
the complaints handling route as an operational matter, the impact
assessment threshold and the prohibition on personal data entering the
repository sit in `packs/security-privacy/references/data-protection-uk.md`
and are not restated here. Ceremony scales with risk to people
(EV-0041), and that proportionality rule is that pack's, applied here
without being re-argued.

## The notice checklist

Due at the moment of collection, not when convenient
(EV-0349). Ten items, each of which is a marker a check
can look for:

1. The controller's identity and contact details.
2. The data protection officer's contact details, where one exists.
3. The purposes of the processing.
4. The lawful basis for each purpose.
5. The legitimate interests relied on, where that is the basis.
6. The categories of recipient.
7. Any third-country transfer and the safeguard relied on.
8. The retention period, or the criteria used to determine it.
9. The rights: access, rectification, erasure, restriction, objection,
   portability, and withdrawal of consent where consent is the basis.
10. The automated decision-making position, including profiling.

The revised UK text now names two distinct complaint routes, and the
notice tells the person about both: to the controller, and to the
Commissioner. A notice that offers only the regulator, or only an
internal address, is short of the checklist.

## Why the checklist and not a template

The statute states what must be said. It does not state how to say it,
at what reading level, or in what format, and it is silent on the two
harder questions of whether the chosen basis is correct and whether the
processing is fair (EV-0349). So the ten items and the
two routes are checkable by a machine, and the quality of the notice
stays a judgement call. Both facts are in `packs/legal-licensing/CHECKS.md`.

## The registration duty is separate

There is a statutory duty on controllers to pay a charge to the
Commissioner and to supply information, with special handling for
partnerships and a schedule of exempt processing
(EV-0350). It exists independently of how good the
notice is, which is what makes it easy to forget. The routing rule is
binary: before any personal data is processed, run the registration
self-assessment and record the outcome, either the payment or the named
schedule exemption.

**Never quote a fee figure from this pack.** Only the structure of the
regulations was retrieved at the research cutoff, not the tier amounts,
and the version read is the text as originally made, so the amounts may
have been uprated since. Check the current fee at source every time.

## A correction worth recording

An earlier ledger row records that the regulator's own pages refused
automated access, so the reading of the 2025 Act rested on the statute
plus secondary reporting (EV-0225). The revised Article 13 text on the
statute site is machine-readable and shows the amendments in force from
2026-02-05, which gives a primary route to the same answer without the
regulator's site (EV-0349). That does not restore the
interpretive guidance, which is still missing, and the caution in the
security-privacy reference still stands.

## What escalates

A data subject complaint that does not resolve, any regulator contact,
and any personal data leaving the UK. These are escalation triggers
under B7, and they are listed in
`packs/legal-licensing/references/ESCALATION.md`. An agent does not answer a
regulator.
