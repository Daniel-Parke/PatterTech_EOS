---
summary: Anatomy of the house vocabulary, containers, section furniture, the long-read kit, diagrams, media and chrome
kind: fact
scope: brand:pattertech
sources: [EV-0027, EV-0239]
volatility: slow
review: 2028-09
type: pattern
tags: [web, layout, content, media, nav]
---

# The house kit

Level-three anatomy for the vocabulary the pack names. The forks live in
`packs/pattertech-house/guides/`, the numbers in
`packs/pattertech-house/refs/BUDGETS.md`, and none of them are repeated
here.

## Containers

**Ledger.** A ruled editorial list. Each row carries a hairline top
rule, a mono index in the accent, a display title, an optional accent
strap line, a muted body and a right-hand mono meta column. The list
closes with a bottom rule. A row that links is clickable across its full
width, and the hover affordance is the rule brightening and an arrow
nudging. One or two columns, and width-agnostic.

**Plaque.** Numbers as an instrument readout. Values in the display face
with tabular figures, hairline rules top and bottom, hairline column
separators, mono uppercase captions with a small accent tick where the
section owns an accent. Values may count up once on first view. They
never glow.

**Panel.** The rare box. A quiet border on the first surface step, a
modest radius, an optional accent tick on the top edge. A panel that is
a link brightens its border and nothing moves except an arrow. Panels
never lift, tilt or shine.

**Spec table.** Facts as a ruled mono manifest: a term column in the
mono voice, a short value, an optional note per row, hairline rules
between rows. If a value needs a sentence it belongs in the body.

**Data rule.** A hairline carrying mono tick labels, the diagram kit's
annotation voice applied between sections. It may charge once as it
reveals, and it marks one measured transition rather than repeating.

**Reticle.** Four corner ticks and up to two mono labels around a single
self-contained artefact, so the thing reads as calibrated. At most one
per section, and never around running text.

**Interlude band.** A contained band one surface step up, hairline rules
top and bottom, composed as its own monument outside the prose grid
rather than through a bleed. It paces a long read with the piece's own
moments, and never wraps media.

## Section furniture

**The section mark.** In order: mono index, short hairline, mono kicker,
display title, optional muted lead. Flush left. Centring is reserved for
monuments, meaning the hero and standalone quotes, so an ordinary
section carries none of it. On wide viewports the
index hangs into a reserved left rail the way a clause number juts into
the margin of a technical document; below the breakpoint it joins the
annotation row. The index sequence runs per page and matches any on-page
navigator's count. Titles are left-aligned from the display ladder, and
where the light posture allows the title carries the one-shot heading
sweep as its reveal fires. The mark is real heading structure, so it is
readable as an outline (EV-0027).

**Chapter marks.** The same anatomy inside the reading grid, with the
number hung in the gutter and a small measurement tick beneath it. The
heading carries the anchor id and scroll margin the navigator depends
on.

**The colophon.** One per page, in place of a closing call-to-action
slab: a full-width hairline, a mono kicker, one display sentence, an
optional quieter second line, then onward paths as mono text links with
nudging arrows and at most one quiet button. The rule charges once as
the band reveals. Copy is written fresh per page.

**The andon line.** One accent hairline across the top of the chrome, as
the brand thread. If it is used, it is the chrome's only accent gesture
and the header call to action goes quiet to pay for it.

## The long-read kit

Chapter, lead and body paragraph, pull quote, the one monumental number
an argument turns on, marginalia hanging in the outer gutter, the line
to remember as a ruled band, figures with plate numbers, a one-card
carousel cited in the reading column, interludes and big quotes as
contained monuments, ruled glossary rows, and the gist near the top for
the reader deciding whether to commit.

Pacing: open with the standfirst, any primary media as a compact card,
and the gist, so a reader knows in one screen whether the piece is for
them. Break chapters with interludes so the surface ladder gives the
scroll a journey. Reading matter never animates. A sticky on-page
navigator earns its place at four chapters or more. Close with the
artefact downloads, a fresh colophon and the next-piece thread.

Numbering is part of the identity rather than decoration. Chapters,
figures and journal entries are numbered like a document and the numbers
are stable.

## The reading grid

Named columns run full, wide, reading, wide, full. Every direct child
sits in the reading measure by default and goes wider only by opting in.
A bleed means the same width in every wrapper, so the full column is
capped with outer tracks outside the full boundary. Vertical rhythm is
the grid row gap, and blocks never set their own vertical margins.
Shared components are width-agnostic and never carry their own maximum
width. Nothing gets automatic margins on a direct grid child, because
the child then gives up stretch and shrinks to its content.

## Diagrams

Positions come from data: scales and spread functions place every node,
and a node dot sits exactly on its datapoint. No label or box overlaps a
line, each label joins its node with a hairline connector, and arrows
end at their final node. Boxes are small, anchored, restrained in fill
and sentence-case in label. No glow on a line. Two-colour semantics hold
across every figure and never swap. Diagrams reflow rather than shrink
on narrow viewports, and dense figures carry a corner control opening a
full-screen view. A diagram may animate only where the motion shows the
system working, and it freezes under reduced motion.

Build figures from a small shared kit of scale helpers and primitives
rather than one-off drawings, so the rules hold by construction and every
figure has the same voice (EV-0239).

## Media and chrome

Media is a cited reference rather than a spectacle. Every image ships
with a web-sized variant, intrinsic dimensions, lazy loading below the
fold and real alternative text. Carousels show one readable card at a
time with grouped arrows, dot indicators, a mono counter, keyboard and
swipe, and no autoplay. Video embeds are facades: a poster card whose
play control loads the player on click, opening in the site's own
full-screen overlay, and closing the overlay unmounts the player so the
audio stops. Documents get panels with a mono badge, a title, one line
of body and a quiet download control.

The header is one row: wordmark left, quiet text links with an underline
active state, a quiet bordered call to action right. Hubs are journal
indexes with numbered ruled entries and mono text-tab filters rather
than card grids, so two entries read as a curated record. Every page
ends in exactly one colophon, and no page dead-ends.
