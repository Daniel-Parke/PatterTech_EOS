---
summary: How to compile the venture's wargame walk from the index, filter by triggers, canonical order
type: kernel
tags: [eos, wargame]
---

# WALK_ORDER

How phase C of INCEPTION.md builds the list of wargames a venture
actually walks, and the order it walks them in. The walk is bounded by
design: only triggered wargames are argued; everything else inherits
its default silently and costs nothing.

## Build the walk

1. Start from `doctrine/WARGAME_INDEX.md` (derived, one row per
   wargame: id, question, module, tags, status).
2. Collect the venture's trigger set: the domains and trigger tags the
   interview surfaced (for example `web`, `auth`, `money`, `pii`,
   `motion`, `hosting`), plus the add-ons the scale ruling attached.
3. Keep a wargame if its module is a triggered domain or any of its
   tags is in the trigger set. Drop superseded rows. Rows with status
   contested are walked with fresh eyes and their tension noted in the
   ruling.
4. Two wargames always walk regardless of triggers: WG-EOS-001
   (venture scale) and WG-EOS-002 (repo shape). The voice register
   (WG-VOX-001) walks whenever the venture has any written surface,
   which in practice is always.

## Canonical order

Walk in this order, ascending WG number within each step:

1. WG-EOS-001, the scale ruling. It gates the matrix column and the
   ceremony of everything after it.
2. WG-EOS-002, the repo shape.
3. WG-VOX (voice): the register ruling colours every surface written
   after it.
4. WG-ARCH (architecture): structure before surface.
5. WG-WEB (web design): the surface, ruled with the register and
   architecture already fixed.
6. WG-DEL (delivery), then WG-OPS (devops): how it is proven, then how
   it runs.

A wargame whose decision rule names another wargame's ruling as an
input jumps behind that prerequisite; the index's question column makes
these visible. Cross-module conflicts go to the module that owns the
decision (GOVERNANCE.md precedence), and the stricter rule applies
until a joint wargame exists.

## Record the rulings

Every walked wargame lands as one rulings row in the lock-book header,
`WG-ID · ruling · argued|inherited · note`:

- **argued** means the triggers were engaged afresh against the
  venture's facts. Any wargame a trigger names must be argued, not
  inherited.
- **inherited** means the default was taken without new argument,
  legitimate when the triggers are silent. Inherited rulings never
  count as promotion evidence.

A fork the walk hits that no wargame covers: file a draft wargame in
`docs/EOS_FEEDBACK.md` using the wargame template, with the venture's
ruling as its first worked entry, and record the ruling in the
lock-book as `WG-DRAFT-NNN` (numbered per venture). The harvest
(PB-E02) assigns the real module id later and rewrites the row.

## Budget

The walk at S is typically eight to twelve rulings and one sitting; M
and L add the modules their triggers pull in. A walk running past
twenty rulings means the trigger set is wrong (too broad) or the
venture is bigger than its scale ruling; stop and re-run WG-EOS-001
before continuing.
