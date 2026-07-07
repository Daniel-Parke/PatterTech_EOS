---
summary: Card, ledger, plaque, table or prose?
type: wargame
tags: [web, layout, density]
status: active
review_by: 2027-07
---

# WG-WEB-003: Card, ledger, plaque, table or prose?

## The question

A set of content needs a container. Which one?

## It depends on

- What the content **is**: parallel facts, numbers, self-contained things,
  reading matter, or truly tabular data.
- Whether items are links (whole-row click changes the anatomy).
- How many items and how often the set grows.
- Whether the set carries per-item status or brand accents.

## Options

### A. Ledger (ruled list)
Parallel facts: features, services, principles, ways, layers. Scales from 3
to 30 rows, one or two columns, indices keep it document-like.

### B. Plaque (ruled figures)
Numbers with captions. Never more than one row of 4 per moment.

### C. Panel (quiet box)
Only for self-contained things: a diagram, a product, a document, a contact
channel. If you can imagine the box's title as a heading in a list instead,
it is not a Panel.

### D. Table
Real records with 3+ comparable fields (a glossary, a spec sheet). Ruled
rows, mono headers, no zebra fills.

### E. Prose
It was reading matter all along. The commonest correct answer.

## Decision rule

Ask "what is this content?" before "how should it look". Facts -> A.
Numbers -> B. Things -> C. Records -> D. Sentences -> E. If the draft has
three icon-tile cards each holding one sentence, the answer was A or E and
the icons were decoration (Doctrine 5).

## Default

A ledger. It is the workhorse that replaced the card grid, and it degrades
gracefully in every direction (add meta, add links, add columns).

## Worked rulings

- **PatterTech Website (2026-07)**: every icon-tile FeatureGrid became a
  Ledger (forces, tailwinds, applications, principles, services, ways,
  interests, what-we-do); StatBands became Plaques; ventures, whitepapers,
  the contact channels and the "talk to us" block became Panels; the five S
  glossary stayed a ruled table with audio; several boxed asides went back to
  prose or a tone-ruled callout.
