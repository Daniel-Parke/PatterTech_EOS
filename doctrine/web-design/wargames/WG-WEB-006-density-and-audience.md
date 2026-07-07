---
summary: How dense, for whom?
type: wargame
tags: [web, density, content]
status: active
review_by: 2027-07
---

# WG-WEB-006: How dense, for whom?

## The question

How much information per screen, and which reading aids, for this page's
audience?

## It depends on

- Who arrives: executives skimming for the gist, practitioners reading
  end-to-end, operators looking something up.
- Session shape: one long visit (a read) vs many short visits (a reference).
- The content's natural length: a 20,000px piece needs pacing machinery a
  2,000px page does not.

## Options

- **Skim-first**: gist band (key takeaways) at the top, plaques for the
  numbers, strong section marks so headings alone tell the story, a colophon
  with the one next step.
- **Read-first**: the full article kit with chapters, figures, interludes and
  an on-page navigator; the skim layer still present at the top.
- **Reference-first**: tables, ruled glossaries, anchor-stable headings,
  dense ledgers; minimal theatre.

## Decision rule

Every long read gets the skim layer anyway (the takeaways band); the fork is
how much pacing machinery follows. Four or more chapters -> on-page
navigator. Numbers that matter -> a plaque near where they are argued, with
an honesty footnote for sourced figures. If practitioners and executives both
matter, structure so the headings, takeaways and plaques alone carry the
argument (the exec path) while the prose carries the depth.

## Default

Skim layer plus read-first structure: takeaways at the top, chapters below.

## Worked rulings

- **PatterTech Website (2026-07)**: both long reads carry "In brief"
  takeaways up top, plaques beside the argued numbers with an "illustrative,
  directional" footnote, and an 11- and 8-chapter navigator respectively.
  The journal index carries type and reading-time meta so the choice to
  commit is informed from the hub.
