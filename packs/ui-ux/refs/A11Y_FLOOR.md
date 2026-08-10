---
summary: The accessibility floor in detail, the six gated classes, tag pinning, incomplete triage and what overlays cannot do
kind: fact
scope: estate
sources: [EV-0027, EV-0028, EV-0029, EV-0104, EV-0235, EV-0236, EV-0237]
volatility: slow
review: on-change-of:WCAG-2.2
type: ux
tags: [a11y, web, forms]
---

# Accessibility floor

Reference for PACK.md B1 to B5. Principles extracted, not quoted: the
standard and its authoring guide are readable under licences that do
not permit reuse of their prose.

## What a conformance claim means

WCAG 2.2 is a set of individually testable statements arranged in
levels. A claim at a level means the named criteria for that level pass
on the named pages, in the named technologies, at a stated date
(EV-0027). Anything less specific is marketing. Criteria are added and
retired over versions, so a claim also names the version.

## The six classes gated individually

The February 2026 census of one million home pages found failure
concentrated in six cheap defects, present on most pages, and getting
worse year on year as pages grow (EV-0235). Each gets its own
assertion, so one aggregate pass can never hide a regression:

| Class | Assertion |
| --- | --- |
| Contrast | every text and non-text pair meets its ratio in a real browser |
| Image alternatives | every image resolves to text or is marked decorative |
| Form labels | every input has a programmatic label |
| Empty links | no link with no accessible name |
| Empty buttons | no button with no accessible name |
| Page language | the document declares its language, and parts declare theirs |

The census is automated and covers home pages only. Its own authors say
no detected errors does not mean a page is accessible. Treat the six as
a floor to automate, never as a definition.

## Tag pinning and the incomplete list

Scanners ship rules spanning several WCAG versions and levels plus
non-normative best practice, so an unpinned run conflates house opinion
with conformance (EV-0236). Pin the rule tags to the version and levels
being claimed. Contrast checks need a real browser engine, since they
depend on computed style.

Every `incomplete` result is a question the tool refused to answer.
Each one gets a written verdict in a manual file, and the file's entry
count equals the report's incomplete count, so an empty file next to a
green build is visibly wrong. Plan against roughly a third of defects
being machine-findable; the tool maintainer claims about 57 per cent,
commonly repeated docs say about a third, and the lower figure is the
safer basis for planning (EV-0236, EV-0104).

## Behaviour, not appearance

The authoring practices guide defines each pattern as expected keyboard
behaviour plus roles, states and properties, independent of any visual
system, and it is explicitly non-prescriptive about looks (EV-0028,
EV-0029). That separation is what lets one behaviour layer serve
several design philosophies.

Per component, record the pattern name, the keys it must answer, and
the state change each key produces. A deviation from a pattern is
allowed and must be written down with a test that pins the behaviour
actually shipped.

## Practices that carry across philosophies

- A skip link as the first focusable element, targeting the main
  landmark, hidden until focused.
- One main landmark, plus header, footer and labelled navigation where
  duplicated.
- Focus visible everywhere, with any replacement outline at least as
  discoverable as the one removed.
- Custom controls are real buttons or links, in the natural tab order,
  with real accessible names. Icon-only controls carry a name.
- Errors on a form are summarised at the top, linked to the fields, and
  repeated at the field. Never colour alone.
- Anchored headings carry ids and scroll margins so in-page navigation
  lands under any fixed header.
- Zoom is never disabled, and the viewport declaration allows it.
- Content stays visible without scripting; reveal patterns hide content
  only where scripting is known to be on.

## Overlays

A bolt-on script cannot deliver conformance. It cannot supply
meaningful alternative text, cannot label form fields it does not
understand, cannot fix keyboard access in scripted components, and
sniffing assistive-technology use exposes disability status without
consent (EV-0237). The source is an advocacy consensus rather than a
controlled comparison, and many signatories compete commercially with
overlay vendors; the technical claims are checkable against the
standard, and no counter-evidence of comparable standing was found.
