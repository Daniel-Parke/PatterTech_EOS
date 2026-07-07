# Long-form reading

The article pattern: how a 10-20,000px read stays a pleasure. Built on the
reading grid (LAYOUT_AND_GRID.md).

## The kit

An article is composed from a small field kit, all width-agnostic on the
reading grid:

- **Chapter**: numbered section with hung margin number, kicker, title (the
  title carries the one-shot heading sweep), and a prose grid body.
- **P / Lead**: body paragraph and the brighter chapter opener. Static, always.
- **Pull**: inline pull-quote with a counter-accent left rule and mono
  attribution.
- **PullStat**: the ONE number the argument turns on, set monumentally
  between ruled hairlines in the reading column; counts up and glints once
  on ignite. A row of numbers is a stat readout (Plaque), not a PullStat.
- **Marginalia**: mono side-notes hanging in the outer gutter on wide
  viewports and folding inline below; asides and citations only, never body
  argument.
- **OneLine**: the "line to remember", a ruled band on the first surface step
  with a mono label.
- **Figure**: wide breakout with a quiet frame, a **plate number** ("Fig. 01",
  mono, joined to the left-aligned caption by a short hairline) and a corner
  zoom control. Number figures sequentially through the piece.
- **CardStrip**: a one-card carousel of branded cards, cited in the reading
  column like any figure. It used to sit on an interlude band; that doctrine
  caused the three-widths incident and was overturned by WG-WEB-014. Media is a
  citation.
- **Interlude / BigQuote**: the tonal steps, composed as their own contained
  monuments outside the prose grid. A band never wraps media.
- **TermTable**: ruled glossary rows (term, transliteration, translation,
  gloss, optional audio).
- **KeyTakeaways**: the gist near the top, a ruled band with dash-marked
  points, for the skimmer deciding whether to commit.

The kit's working contract (grid contract, media law, add-a-component
checklist) lives beside the code as a GUIDE.md in the kit folder, with a
JSDoc law header on every component and a design lint in the standard lint
command (WG-WEB-013). A law that lives only in module docs will eventually be
broken politely.

## Pacing rules

- Open with the standfirst, any primary media as a compact card, and the
  takeaways. A reader should know in one screen whether the piece is for them.
- Break chapters with interludes so the surface ladder gives the scroll a
  journey; at most one warm interlude per piece, spent on the piece's thesis
  moment.
- Reading matter never animates; furniture and figures reveal once.
- A sticky on-page navigator (current chapter, n / total, progress) earns its
  place at four or more chapters. Anchors and scroll margins are part of the
  chapter contract.
- Close with the artifact downloads (Panels), a fresh colophon, and the
  next-piece thread.

## Numbering

Chapters, figures and journal entries are numbered like a document, and the
numbers are stable. The numbering is part of the annotation identity, not
decoration.
