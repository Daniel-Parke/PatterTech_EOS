---
summary: UK data protection for a small venture, lawful basis register, complaints route, DPIA threshold and what is unsettled
type: guide
tags: [security, pii]
review_by: 2028-01
kind: fact
scope: estate
volatility: event-driven
review: on-change-of:EV-0225
sources: [EV-0041, EV-0225, EV-0226]
---

# Reference: UK data protection for a small venture

Level 3 detail behind binding requirement B5. This is not legal advice.
It records what the pack asks for and where the ground is uncertain.

## What B5 actually requires

Two artefacts and one prohibition.

**A lawful basis register.** One row per processing purpose, not per
system. Each row names the purpose in plain words, the lawful basis
relied on, the categories of people, the categories of data, the
retention period, and who else sees it. A purpose with no row is a
purpose nobody has thought about.

**A named complaints route.** A named person or role, a working
contact address, and a stated response time. It has to be reachable by
the people whose data it is, which means it appears where they are, not
only in an internal document.

**The prohibition.** Personal data does not enter the repository, its
logs, its test fixtures or its agent transcripts. Test data is
synthetic. A support ticket pasted into an issue is a breach of this
rule even though it feels like ordinary work.

## Proportionality and the DPIA threshold

The regulator's posture is proportionality: the obligation scales with
the risk to people, and a small venture doing low-risk processing is
not asked for the same apparatus as a large one (EV-0041). A data
protection impact assessment is triggered by high risk to people, and
the reliable signals for a small venture are automated decisions with
an effect on someone, special-category data, systematic monitoring, and
processing at a scale the venture has not handled before.

When in genuine doubt, write the assessment. It is a page, and the cost
of having one you did not need is smaller than the cost of the argument
about whether you needed one.

## The Act and what it changed

The Data (Use and Access) Act 2025 is on the statute book, with data
protection provisions commencing in phases through to 19 June 2026
(EV-0225). It is Crown copyright under the Open Government Licence,
which permits reuse with attribution, so the Act text may be quoted
where that helps.

## Where this is thin, honestly

The regulator's site refused automated access at the research cutoff,
so we have the Act but not the interpretive guidance that normally
tells a small venture what the Act means in practice. B5 is therefore
deliberately modest: it requires a recorded basis and a route out,
which were true before the Act and remain true after it, and it does
not attempt to state what the new provisions change. Treat any
confident claim about DUAA practice, including one from a model, as
unsourced until the guidance publishes.

The review trigger on this file is the guidance landing. That is the
event that should cause this page to be rewritten rather than patched.

## Operating environment

Data protection sits on top of a working environment, and the NCSC
small-organisation baseline is five topics rather than fifty
(EV-0226): backing up, protecting against malware, keeping devices
safe, using strong passwords, and avoiding phishing. A short list done
beats a long list partly done, and the pack takes that as a default
rather than restating the five here.
