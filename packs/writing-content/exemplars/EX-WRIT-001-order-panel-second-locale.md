---
summary: The pack applied end to end to an order-status panel, a concatenated count and a banner error made survivable in a second language
kind: exemplar
scope: estate
type: example
tags: [content, forms, a11y]
---

# EX-WRIT-001: an order panel prepared for a second language

The situation. One venture ships an order-status panel in English only.
Next quarter it ships in Polish. Today it fails an accessibility
review. The team has ten string keys, one React component and no
localisation discipline. The panel is the cheapest possible place to
apply this pack, because ten strings is the point at which the format
decision is nearly free.

## What was there

Five defects, each a different requirement in
`packs/writing-content/PACK.md`.

1. The item count read `You have ` plus a number plus ` item` plus a
   conditional `s`. Four lookups and a ternary, assembled in the
   component.
2. The quantity error read `Invalid input`, rendered in a red banner
   above the panel, and the quantity field was cleared on failure.
3. The refresh button was a fixed 96-pixel box around the label
   `Update`.
4. The string `Try again` was written straight into the template and
   never passed through the lookup function.
5. The string file used `basket` in three places and `cart` in two,
   for one concept.

## What was decided, and why

**Philosophy.** Content design for the panel copy, message data
underneath it, per
`packs/writing-content/guides/GD-WRIT-001-clarity-philosophy.md`. Not
plain language alone, because the failures here were structural rather
than a matter of wording, and no amount of rewriting fixes defect 1.

**Format.** MessageFormat 2.0, pinned, per
`packs/writing-content/guides/GD-WRIT-002-message-structure.md`. Ten
strings is the cheapest moment this decision will ever have. The team
recorded the pin and the Draft status of parts of the default function
set as a known risk.

**Voice.** Venture default, per
`packs/writing-content/guides/GD-WRIT-003-voice-scope.md`. The venture
has not adopted a brand voice, so none applies. The literal-instruction
register overrides on the quantity error, because the reader must act
correctly there.

**Gate.** A term list plus a pseudo-locale build, per
`packs/writing-content/guides/GD-WRIT-004-prose-gate.md`. No readability
threshold, because B10 forbids one.

## What changed

**Defect 1, B1 and B2.** The count became one message id with plural
selection inside the message. The component passes a number and nothing
else. Adding a Polish locale file with four plural categories now
renders the correct form for 1, 2, 5 and 22 with no change to the
component, which is the property being bought. The English file is not
the source of the Polish forms, per
`packs/writing-content/refs/I18N_MECHANICS.md`.

**Defect 2, B4 and B5.** `Invalid input` became a statement of what a
valid quantity looks like, naming the range. It moved next to the
quantity field and is associated with it programmatically, so a screen
reader reaches it from the input. It fires on submit rather than on
keystroke. The typed value survives the failure. The detail is in
`packs/writing-content/refs/ERROR_CONTRACT.md`. The machine half of the
same failure stayed in the API response and was not reused as the
rendered string, which is B6.

**Defect 3, expansion default.** The fixed width became a minimum width
with the label free to grow. `Update` is six characters, which sits in
the two-to-three-times expansion band, so it was the highest-risk
string on the panel despite being the shortest.

**Defect 4, B3.** The pseudo-locale build failed on `Try again`
appearing untransformed, which is exactly the signal it exists to give.
The string was externalised and the build passed.

**Defect 5, B7.** `cart` was chosen, `basket` was banned, and the term
list ran over the string file in CI. The team injected `basket` once to
confirm the step actually fails, because a check nobody has seen fail
is a check nobody has tested.

## What was deliberately not done

- No readability score was computed or gated. B10.
- No termbase was built. Five terms is a list, not a termbase, and
  GD-WRIT-004 says reach for the heavier option only where a misread
  step causes harm.
- No claim was made that the new copy is easier to understand. Nobody
  tested it on a reader. The team may say the panel now survives a
  second locale and meets the error criteria, and may not say it is
  clearer, per the counter-evidence in PACK.md.
- The venture's em-dash usage was left alone. The EOS voice law has no
  authority in a venture repository.

## What it cost

One afternoon, one dependency, one CI step and a pinned format version
the team now owns. The same work at ten thousand strings would have
been a quarter.
