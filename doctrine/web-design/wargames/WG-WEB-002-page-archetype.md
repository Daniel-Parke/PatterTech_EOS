# WG-WEB-002: Which vocabulary does this page speak?

status: active
review_by: 2027-07

## The question

A new page is being built. Which archetype (and therefore which component
vocabulary) applies: landing, hub/index, long read, product page, app shell,
or utility?

## It depends on

- What the visitor is there to do: be convinced, browse a record, read for
  twenty minutes, evaluate a product, operate a tool, or complete an errand.
- Content lifetime: evergreen story vs growing index vs dated piece.
- Density and audience: an exec skims, a practitioner reads, an operator acts
  (see WG-WEB-006).

## Options

The archetypes and their vocabularies are described in ux/FLOWS.md: landing
(hero + marked sections + colophon), hub (journal index), long read (article
kit), product (panels + ledgers + plaques + status), app shell (outside this
module's scope today; wargame it when it first appears), utility (quiet
prose).

## Decision rule

Name the visitor's primary verb. Convince -> landing. Browse -> hub. Read ->
long read. Evaluate -> product. Operate -> app shell (and flag that this
module needs extending). Complete -> utility. If a page seems to need two
archetypes, split the page or subordinate one verb to the other; a page that
is half landing and half long read does both badly.

## Default

When genuinely unsure, build the quieter archetype. It is easier to add a
moment of theatre to an editorial page than to calm a marketing page down.

## Worked rulings

- **PatterTech Website (2026-07)**: home = landing (hero kept as the one loud
  moment); /research = hub as journal index (two entries now read curated,
  not empty); whitepaper and philosophy pieces = long reads on the article
  kit; /ventures = product page with Panels and a status legend; contact and
  legal = utility.
