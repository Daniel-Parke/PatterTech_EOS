# Web design doctrine

The non-negotiables. These hold for every web project regardless of brand,
stack or audience. Everything else in this module is derivation and pattern;
this page is law. To change it, wargame it first (see /START.md).

## 1. Restraint over ornament

Quiet beats loud. When a choice exists between the calmer and the flashier
treatment, take the calmer one and spend the saved attention on typography and
content. Sites do not become premium by adding effects; they become premium by
removing them until what remains is deliberate.

## 2. Semantic ornament

Nothing glows, pulses, shimmers or moves unless it is genuinely live: an
animated visual, a live status, data in motion. Static content earns attention
through structure (rules, labels, space, scale), never through borrowed
energy. Each project may name a very small set of sanctioned exceptions in its
lock-in (a hero, a logomark), and each exception must itself be animated.

## 3. Structure over memory

Consistency must be structural, not disciplinary. Build layout systems that
make drift impossible rather than rules people must remember: a reading grid
where every block sits in the measure by default and opts wider explicitly,
vertical rhythm owned by the grid gap rather than per-block margins, tokens
that components consume rather than restate. If a mistake keeps happening, the
fix is a primitive, not a reminder.

## 4. Typography carries the design

Three type roles: a display face for headings, a text face for reading, and a
mono face as the annotation voice (indices, kickers, meta, captions, data).
Scale contrast and the mono voice do the work that boxes, icons and colour
used to fake. If a layout feels flat, fix the type before reaching for
decoration.

## 5. There is no universal card

The boxed-card grid is the single strongest generic-template tell. Choose the
container by what the content is: a ruled list (ledger) for parallel facts, a
ruled figure row (plaque) for numbers, a quiet panel only for genuinely
self-contained things (a diagram, a product, a document, a contact), plain
prose for reading matter. Panels never lift, tilt or shine on hover; the hover
affordance is a border or rule brightening and an arrow nudging.

## 6. Editorial asymmetry

Sections open flush left with annotation furniture (index, hairline, kicker,
title), and indices may hang into the margin like clause numbers. Centring is
reserved for monuments: the hero and standalone quotes. A page of centred
headings above centred card grids is the template rhythm we exist to avoid.

## 7. One signature motif, promoted everywhere

Every project names one motif that is genuinely its own and applies it at
every scale, from page furniture to figure captions. PatterTech's is its
diagram annotation language (mono labels, hairline connectors, node dots,
semantic two-colour accents). A motif used once is decoration; used
everywhere, it is identity. Deriving the motif is part of project lock-in.

## 8. Motion means something

Three kinds of motion are allowed: live visuals (the signature animated
pieces), one-shot reveals on section furniture and figures, and functional
feedback (hover, focus, progress). Reading matter never animates in.
Everything respects `prefers-reduced-motion`, and content must remain visible
without JavaScript.

## 9. Measure, don't eyeball

Ship against gates, not vibes: build passes, no horizontal scroll at 375px,
alignment measured, media inside budget, diagrams free of box-on-line
overlaps. A page is done when the gates say so.

## 10. Voice parity

The copy is part of the design and is held to the same bar. Design cannot
rescue template writing, and one AI-cliché line undoes a page of careful
typography. Each project's lock-in names its voice reference and its banned
list.

## 11. Media earns its weight

Media is a cited reference, not a spectacle. Every image that ships has a
web-sized variant, intrinsic dimensions and lazy loading; embeds are facades
until clicked; budgets are written down and gated.

## 12. The generic-tell test

Before shipping a section, ask: could this section be dropped into any
AI-generated site unchanged? If yes, it is not designed yet. The usual
suspects: centred eyebrow + heading + icon-tile card grid, glowing pill
buttons, gradient text on statistics, reveal-on-scroll on every paragraph, a
closing CTA slab identical on every page.
