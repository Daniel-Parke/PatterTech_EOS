---
summary: Who owns a published page, and how fast may a venture publish?
kind: guide
authority: default
basis: decision
evidence_grade: not-applicable
scope: estate
sources: [EV-0095, EV-0353, EV-0354, EV-0356]
review: on-change-of:Google-spam-policies-revision
type: guide
tags: [content, seo, voice]
---

# GD-MKTG-004: Who owns a published page and why does it exist?

## The question

An agent can write a hundred pages in an afternoon. The index operator
does not test how text was produced; it tests why the page exists
(EV-0354). PACK.md D6 requires a named owner and a stated purpose
per page. This guide decides how much provenance machinery a venture
needs and what publishing rate that machinery supports.

## It depends on

- **Whether a real reader is identifiable** for each page, by name of
  need rather than by keyword.
- **Who answers for the page** when it is wrong.
- **Whether the page would exist if search did not.** If not, it is
  ranking bait and the policy names it.
- **How much automation went in**, since the guidance asks that
  substantial automation be evident to the visitor (EV-0356).
- **Whether the venture publishes third-party content on its domain**,
  which is where site reputation abuse lives (EV-0354).

## Options

### A. Manifest with a named owner and a one-line purpose per page
A machine-readable file listing every published page with its human
owner and why it exists, validated against the actual page set so
neither can drift. Buys a check a script runs, and a person to ask.
Costs a file that must be updated in the same commit as the page.

### B. Front-matter provenance on each page
Owner, purpose and automation disclosure carried in the page's own
metadata, with the manifest derived from it. Buys locality: the fact
travels with the artefact and cannot be forgotten separately. Costs a
generator and the habit of never editing the derived file.

### C. Editorial review before publication, no artefact
A person reads everything before it ships. Buys judgement, which is the
thing the questionnaire actually asks for. Costs the one resource a
small venture does not have, and it leaves no evidence afterwards that a
check happened.

### D. Publish freely, prune on measured failure
Ship at volume and remove what performs badly. Buys speed. Costs the
exact thing the spam policy names: scaled content abuse is defined by
purpose, and a page published to see whether it ranks has declared its
purpose. This option is excluded, and it is listed so the argument
against it is on the record rather than assumed.

## Decision rule

If pages number in the tens, run A: it is one file and one test. If
pages number in the hundreds or several people write them, run B and
derive A from it. Run C beside either where the subject carries real
consequence for a reader, never instead of them. Never D. Publishing
rate then follows from ownership: the rate a venture can sustain is the
rate at which it can name an owner and a reader, and no faster.

## Default

A. It satisfies D6 with a single artefact and a single check, and it
upgrades into B without changing what is asserted. The manifest is
checked by a test that fails on a page missing from it and on a manifest
entry with no page, so the two sets are identical by construction.

## Worked rulings

- **marketing-growth pack exemplar (2026-08, argued)**: A, with five
  pages, five owners and a test asserting set equality in both
  directions, plus an assertion that no page carries a keywords meta tag
  because the index operator says it is unused (EV-0353). See
  `packs/marketing-growth/exemplars/EX-MKTG-001-launch-and-first-sequence.md`.
- **Estate default (2026-08, argued)**: machine authorship is not the
  test and this pack does not treat it as one. A page drafted by an
  agent, owned by a person and written for a reader is in policy. The
  open question the pack records is whether such content is detectably
  worse rather than merely against someone's policy, which nothing in
  the source set measures. The publishing stance itself, opinionated or
  hedged, is a preference and sits in PACK.md rather than here
  (EV-0095).
